"""Hoppe Engine v3 — hops: H(S, B, T) = S' as recorded events.

A hop is the event that advances the path; it is not the path. The
operator is an application: a state S, crossing a boundary B, under a
transition T, comes out as the new state S'. It is never an addition.

Ledger semantics (append-only, superseding v1's simpler transitions):

- A hop records FROM state, boundary, transition, strip, direction,
  TO state, and its path position (sequence on the flower stroke —
  separate from the state address, never clock time).
- A RETURN hop lands on a NEW ledger entry whose state resembles the
  earlier one. Resemblance is graded (perfect / partial / irreversible)
  and any loss is recorded. A return never edits, overwrites, or
  re-enters an old entry: you do not go back to the old state, you
  arrive at a new one that resembles it.
- A REFUSED hop is preserved as a branch entry: the attempt as stated
  is REFUTED for that boundary, and the branch itself stays OPEN for
  later work. Nothing is silently dropped.
- Every hop verifies its named invariants across the actual (S, B, T).
  An empty invariant set is rejected: transitions are checked, not
  assumed (the audit's gap 4).
"""
import invariants as inv
from state import DIRECTIONS, PATH_MAX, PATH_MIN, STRIPS

REVERSIBILITY = ("perfect", "partial", "irreversible")


class HopEngine:
    def __init__(self, ledger):
        self.ledger = ledger
        self._count = 0
        self._last_path_position = None
        self.states = {}          # label -> State, as first recorded

    # -- helpers ---------------------------------------------------------
    def _verify(self, state_from, boundary, transition, invariant_names):
        if not invariant_names:
            raise ValueError("a hop must name at least one invariant to verify "
                             "across the transition (empty invariant set rejected)")
        ctx = {"S": state_from.label, "B": boundary.label, "T": transition}
        results = {}
        for name in invariant_names:
            fn, _required, _designed = inv.CHECKS[name]
            ok, detail = fn(ctx)
            results[name] = {"ok": ok, "detail": detail}
        return results

    def _check_path(self, path_position):
        if path_position is None:
            return
        if not (PATH_MIN <= path_position <= PATH_MAX):
            raise ValueError("path position %r outside the traced stroke [0, 360]"
                             % (path_position,))
        if self._last_path_position is not None and path_position < self._last_path_position:
            raise ValueError("path positions are sequence: they do not run backwards")
        self._last_path_position = path_position

    def _record(self, entry):
        self._count += 1
        entry = dict(entry)
        entry["hop_id"] = "HOP-%03d" % self._count
        self.ledger.append("HOP", entry)
        return entry

    # -- the hop -----------------------------------------------------------
    def hop(self, state_from, boundary, transition, strip, direction,
            state_to, invariant_names, path_position=None):
        """Apply H(S, B, T) = S'. The boundary is asked first: a smart
        filter may refuse, and the refusal is recorded as a branch."""
        if strip not in STRIPS:
            raise ValueError("strip %r is not one of the three strips" % (strip,))
        if direction not in DIRECTIONS:
            raise ValueError("direction %r is not outbound or return" % (direction,))
        self._check_path(path_position)
        self.states.setdefault(state_from.label, state_from)

        admitted, reason = boundary.admit(state_from, transition)
        base = {"kind": "hop", "from": state_from.as_dict(), "boundary": boundary.label,
                "transition": transition, "strip": strip, "direction": direction,
                "path_position": path_position}

        if not admitted:
            entry = dict(base)
            entry.update({"kind": "refused-branch", "to": None,
                          "mark": "refused",
                          "attempt_status": "REFUTED",
                          "attempt_note": "the attempt as stated is refuted for "
                                          "this boundary",
                          "branch_status": "OPEN",
                          "refusal_reason": reason,
                          "continuity": "PRESERVED (branch recorded, not dropped)"})
            return self._record(entry)

        results = self._verify(state_from, boundary, transition, invariant_names)
        preserved = all(r["ok"] for r in results.values())
        self.states.setdefault(state_to.label, state_to)
        entry = dict(base)
        entry.update({"kind": "hop", "to": state_to.as_dict(), "mark": "accepted",
                      "invariants": results, "invariants_preserved": preserved,
                      "continuity": "PRESERVED"})
        return self._record(entry)

    def return_hop(self, state_from, boundary, transition, strip,
                   state_back, resembles_state, reversibility, loss,
                   invariant_names, path_position=None):
        """The return leg. Lands on a NEW entry whose state resembles an
        earlier one (the round trip out along one curve and back along
        the opposite curve). Reversibility is graded and loss recorded;
        perfect reversal is never assumed."""
        if reversibility not in REVERSIBILITY:
            raise ValueError("reversibility must be graded: perfect, partial, "
                             "or irreversible")
        entry = self.hop(state_from, boundary, transition, strip, "return",
                         state_back, invariant_names, path_position)
        if entry["kind"] == "refused-branch":
            return entry
        entry["return_of"] = resembles_state.label
        entry["resembles"] = state_back.resembles(resembles_state)
        entry["reversibility"] = reversibility
        entry["loss"] = loss
        entry["note"] = ("a return path is a recorded relationship back through "
                         "the same boundary, not a reversal of reality and not "
                         "a re-entry of the old entry")
        # The hop() call already appended; the return metadata rides as a
        # superseding annotation entry so history is never edited.
        self.ledger.append("HOP-RETURN-DETAIL",
                           {"hop_id": entry["hop_id"], "return_of": resembles_state.label,
                            "resembles": entry["resembles"],
                            "reversibility": reversibility, "loss": loss})
        return entry
