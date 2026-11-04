"""Hoppe Engine v3 — the reading grammar as data structures.

Tonight's worksheet (m0-axis-assignment-worksheet-2026-10-31) as working
architecture, with candidate status preserved: every assignment here
that awaits the framework author's ruling carries its label in the
graph data and in these tables, and nothing in this module upgrades a
label because a run passed.

The grammar in one paragraph. A state carries a four-part address
(X, Y, Z, K): X, Y, Z spatial; K the scale/tier index. Movement runs on
three Möbius strips — matter, energy, transition — each with an
outbound leg and a return leg: six degrees of movement. A boundary is a
smart filter: it selects, filters, can change the state of what it
passes, and can refuse; a refused crossing is recorded, never dropped.
Inlays (six kinds of energy; states of mass; transition marks) are
READINGS on a state, never extra axes: the address stays four parts.
Sequence on the flower timeline is carried by PATH POSITION — an arc
count along the traced stroke — which is not clock time and is not
part of the address.
"""

# --- the three strips and the six degrees ------------------------------
STRIPS = ("matter", "energy", "transition")
DIRECTIONS = ("outbound", "return")
SIX_DEGREES = tuple((s, d) for s in STRIPS for d in DIRECTIONS)

# --- inlays: readings, never axes --------------------------------------
ENERGY_INLAYS = ("kinetic", "thermal", "electrical", "chemical",
                 "radiant", "nuclear/binding")
TRANSITION_MARKS = ("accepted", "refused", "return", "branch")

# --- the flower path -----------------------------------------------------
# Traced data (DERIVED): circles per generation, cumulative arcs on the
# generation stroke, ring completions on the generation-4 stroke.
FLOWER_CIRCLES = {0: 1, 1: 7, 2: 19, 3: 37, 4: 61}
FLOWER_ARCS = {1: 36, 2: 108, 3: 216, 4: 360}
GEN4_CLOSURES = (42, 114, 222, 360)
PATH_MIN, PATH_MAX = 0, 360


class State:
    """A state: label, four-part address, the kind it is being read as,
    and its inlay readings. The kind is a reading carried by the strip
    the state travels on (worksheet candidate, unruled) — it is not a
    fifth address part."""

    def __init__(self, label, address, kind="matter", inlays=None):
        address = tuple(address)
        if len(address) != 4:
            raise ValueError("a state's address is exactly four parts (X, Y, Z, K)")
        self.label = label
        self.address = address
        self.kind = kind
        self.inlays = dict(inlays or {})
        for key in self.inlays:
            if key == "energy" and self.inlays[key] not in ENERGY_INLAYS:
                raise ValueError("energy inlay %r is not one of the six kinds"
                                 % (self.inlays[key],))

    def as_dict(self):
        return {"label": self.label,
                "address": {"X": self.address[0], "Y": self.address[1],
                            "Z": self.address[2], "K": self.address[3]},
                "kind": self.kind, "inlays": dict(self.inlays)}

    def resembles(self, other):
        """The return-leg test: same address and same energy reading.
        Resemblance is not identity — a return lands on a NEW state
        that resembles the earlier one, graded, with any loss recorded."""
        return (self.address == other.address
                and self.inlays.get("energy") == other.inlays.get("energy"))


class Boundary:
    """A smart filter / processor: a selective interface that evaluates
    what crosses, holds a gradient, can change the state of what it
    passes — and can refuse. `accepts` is the set of transition names
    this boundary passes; anything else is refused, with the reason
    recorded. A boundary with no receiving state on the far side
    refuses everything: a leg that terminates in the void is a bleed,
    and the filter will not pass it."""

    def __init__(self, label, accepts=(), refuse_reason="", has_receiving_state=True):
        self.label = label
        self.accepts = set(accepts)
        self.refuse_reason = refuse_reason
        self.has_receiving_state = has_receiving_state

    def admit(self, state, transition):
        """Returns (True, None) to pass the crossing, or (False, reason)
        to refuse it. Refusal is a result, not an error."""
        if not self.has_receiving_state:
            return False, ("no receiving state on the far side: the leg would "
                           "terminate in the void (a bleed)")
        if transition not in self.accepts:
            return False, self.refuse_reason or (
                "boundary does not pass transition %r" % (transition,))
        return True, None
