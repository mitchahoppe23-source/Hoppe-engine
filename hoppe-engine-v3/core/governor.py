"""Hoppe Engine v3 — the Governor.

The Governor law: the seven labels are a closed set, and no status is
ever upgraded on internal evidence alone. Agreement between models,
internal consistency, and confidence of tone are not evidence.

What v2 changes against v1 (the audit's gaps, closed):

- decide() takes a structured EvidenceRecord — claim, route, premises,
  inputs, tolerance declared in advance, checker identity, tier — never
  a caller-supplied kind string. A bare word raises TypeError.
- Every decision is appended to the ledger with its evidence record.
  There is no silent finalization.
- Checker tiers C0-C4 and finalization stages F0-F4 carry label
  ceilings: a decision can grant only what its tier and route support.
    C0 echo (a caller's word)            -> F0, grants nothing
    C1 internal recomputation            -> F1
    C2 independent route, same house     -> F2
    C3 independent external evidence     -> F3
    C4 external challenge / replication  -> F4
- The asymmetric REFUTED rule: one checked counterexample on a stated
  route refutes a claim AS STATED at any tier C1 or above. Refutation
  is cheap; confirmation is expensive. That asymmetry is deliberate.
- Disagreement between two evidence records on one claim freezes the
  claim and files a mandatory Miss Report.
- A composite claim's standing is its weakest link.
- K (the scale/tier index in a state's address) is data. It changes
  only through a Governor decision backed by independent evidence
  (tier C3 or above); the attempt and its outcome are both logged.
"""
from dataclasses import dataclass, field

LABELS = ["OBSERVED", "DERIVED", "FRAMEWORK RESULT", "SUPPORTED",
          "HYPOTHESIS", "OPEN", "REFUTED"]

# Rank used only for upgrade comparisons. REFUTED is handled by its own
# asymmetric rule, not by rank.
RANK = {"OPEN": 0, "HYPOTHESIS": 1, "OBSERVED": 2, "SUPPORTED": 2,
        "DERIVED": 3, "FRAMEWORK RESULT": 3, "REFUTED": 3}

TIERS = ["C0", "C1", "C2", "C3", "C4"]
STAGE_OF_TIER = {"C0": "F0", "C1": "F1", "C2": "F2", "C3": "F3", "C4": "F4"}
ROUTE_KINDS = ["proof", "measurement", "consistency", "counterexample", "none"]


@dataclass
class EvidenceRecord:
    claim_id: str
    route: str                      # how the evidence was produced
    kind: str                       # one of ROUTE_KINDS
    checker: str                    # who or what checked it
    tier: str                       # C0..C4
    premises: list = field(default_factory=list)
    inputs: dict = field(default_factory=dict)
    tolerance: str = ""             # declared in advance, as text

    def as_dict(self):
        return {"claim_id": self.claim_id, "route": self.route, "kind": self.kind,
                "checker": self.checker, "tier": self.tier,
                "premises": list(self.premises), "inputs": dict(self.inputs),
                "tolerance": self.tolerance}


class Governor:
    def __init__(self, ledger):
        self.ledger = ledger
        self.frozen = set()
        self._seen_outcomes = {}

    # -- ceilings ------------------------------------------------------
    def _ceiling(self, record, current_status):
        """Highest label this evidence may grant, or None for no grant."""
        if record.kind == "none" or record.tier == "C0":
            return None
        if record.kind == "consistency":
            return current_status            # consistency never upgrades
        if record.kind == "proof":
            # Terminal court A: dimensionless mathematics and known
            # proofs, premises stated, are admissible at C1 and above.
            if not record.premises:
                return None
            return "DERIVED"
        if record.kind == "measurement":
            if record.tier in ("C3", "C4"):
                return "SUPPORTED"
            return "HYPOTHESIS"
        return None

    def _record_complete(self, record):
        if record.kind in ("proof", "measurement", "counterexample"):
            if not record.tolerance:
                return "tolerance not declared in advance"
            if not record.checker:
                return "checker identity missing"
        if record.kind == "proof" and not record.premises:
            return "proof route without stated premises"
        return None

    # -- decisions -----------------------------------------------------
    def decide(self, record, current_status, proposed_status):
        """Decide a proposed status for a claim from an evidence record.
        Returns a decision dict; the decision is appended to the ledger
        with the full evidence record either way."""
        if not isinstance(record, EvidenceRecord):
            raise TypeError(
                "Governor decisions require a structured EvidenceRecord, "
                "never a bare word (got %r)" % (record,))
        if record.tier not in TIERS:
            raise ValueError("unknown checker tier %r" % (record.tier,))
        if record.kind not in ROUTE_KINDS:
            raise ValueError("unknown route kind %r" % (record.kind,))
        if proposed_status not in LABELS or current_status not in LABELS:
            raise ValueError("status outside the closed label set")

        stage = STAGE_OF_TIER[record.tier]
        incomplete = self._record_complete(record)

        if record.claim_id in self.frozen:
            outcome, granted, reason = ("FREEZE", None,
                                        "claim frozen by disagreement; Miss Report mandatory")
        elif incomplete:
            outcome, granted, reason = ("DEFER", None, "evidence record incomplete: " + incomplete)
        elif record.kind == "counterexample" and record.tier != "C0":
            # Asymmetric rule: one checked counterexample refutes as stated.
            outcome, granted, reason = ("GRANT", "REFUTED",
                                        "asymmetric rule: checked counterexample on a stated route")
        else:
            ceiling = self._ceiling(record, current_status)
            if ceiling is None:
                outcome, granted, reason = ("DEFER", None,
                                            "evidence kind/tier grants nothing (internal "
                                            "consistency is not evidence)")
            elif proposed_status == current_status:
                outcome, granted, reason = ("GRANT", current_status,
                                            "standing confirmed at ceiling %s; no upgrade" % ceiling)
            elif RANK[proposed_status] <= RANK[ceiling]:
                outcome, granted, reason = ("GRANT", proposed_status,
                                            "within ceiling %s at %s/%s" % (ceiling, record.tier, stage))
            else:
                outcome, granted, reason = ("DEFER", None,
                                            "proposed %s exceeds ceiling %s at %s/%s"
                                            % (proposed_status, ceiling, record.tier, stage))

        decision = {"claim_id": record.claim_id, "current": current_status,
                    "proposed": proposed_status, "outcome": outcome,
                    "granted": granted, "stage": stage, "reason": reason,
                    "evidence": record.as_dict()}

        # Disagreement bookkeeping: two different granted outcomes on one
        # claim freeze it and demand a Miss Report.
        key = record.claim_id
        prev = self._seen_outcomes.get(key)
        if granted is not None and prev is not None and prev != granted:
            self.frozen.add(key)
            self.ledger.append("MISS-REPORT",
                               {"claim_id": key, "kind": "governor disagreement",
                                "detail": "outcomes %s vs %s; claim frozen" % (prev, granted)})
        if granted is not None:
            self._seen_outcomes[key] = granted

        self.ledger.append("GOVERNOR-DECISION", decision)
        return decision

    def note_disagreement(self, claim_id, detail):
        self.frozen.add(claim_id)
        return self.ledger.append("MISS-REPORT",
                                  {"claim_id": claim_id, "kind": "disagreement", "detail": detail})

    # -- K is data -------------------------------------------------------
    def change_k(self, entry, new_k, record):
        """Change an entry's K only on independent evidence (C3+).
        entry is a mutable graph-entry dict carrying address.K. The
        attempt is logged either way; a refused change leaves K intact."""
        if not isinstance(record, EvidenceRecord):
            raise TypeError("K changes require a structured EvidenceRecord")
        addr = entry.setdefault("address", {"X": None, "Y": None, "Z": None, "K": None})
        old_k = addr.get("K")
        if record.tier in ("C3", "C4") and record.kind in ("measurement", "proof"):
            addr["K"] = new_k
            self.ledger.append("K-CHANGE", {"entry": entry.get("id"), "from": old_k,
                                            "to": new_k, "evidence": record.as_dict()})
            return True, "K changed %s -> %s on %s evidence" % (old_k, new_k, record.tier)
        self.ledger.append("K-CHANGE-REFUSED", {"entry": entry.get("id"), "from": old_k,
                                                "to": new_k,
                                                "reason": "K changes only on independent "
                                                          "evidence (tier C3+)",
                                                "evidence": record.as_dict()})
        return False, "K change refused: tier %s is not independent evidence" % record.tier


def weakest_link(statuses):
    """A composite claim stands at its weakest component's label."""
    if not statuses:
        return "OPEN"
    return min(statuses, key=lambda s: RANK[s])
