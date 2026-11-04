"""Hoppe Engine v3 — graph loading and load-time validation.

The audit's first gap, closed: every status in the graph is checked
against the closed label set at load. An illegal status (the audit's
'PROVEN' test) fails the load, loudly, before anything runs. Every
entry must also carry its (X, Y, Z, K) address fields: K is data, and
an entry without address fields does not load.
"""
import json
from pathlib import Path

from governor import LABELS


class GraphValidationError(Exception):
    pass


def _validate_entry(entry, where):
    eid = entry.get("id", "<no id>")
    statuses = entry.get("status")
    if statuses is None:
        raise GraphValidationError("%s %s: no status field" % (where, eid))
    if isinstance(statuses, str):
        statuses = [statuses]
    for s in statuses:
        if s not in LABELS:
            raise GraphValidationError(
                "%s %s: illegal status %r (closed set: %s)"
                % (where, eid, s, ", ".join(LABELS)))
    addr = entry.get("address")
    if not isinstance(addr, dict) or any(k not in addr for k in ("X", "Y", "Z", "K")):
        raise GraphValidationError(
            "%s %s: address fields (X, Y, Z, K) required; K is data" % (where, eid))
    k = addr["K"]
    if k is not None and (not isinstance(k, int) or isinstance(k, bool) or k < 0):
        raise GraphValidationError("%s %s: K must be null or a non-negative integer" % (where, eid))


def load_graph(path):
    graph = json.loads(Path(path).read_text())
    for section in ("core_objects", "entries", "register_items"):
        for entry in graph.get(section, []):
            _validate_entry(entry, section)
    for flag_name, flag in graph.get("open_flags", {}).items():
        if flag.get("status") not in LABELS:
            raise GraphValidationError("open flag %s: illegal status %r"
                                       % (flag_name, flag.get("status")))
    return graph


def find_entry(graph, entry_id):
    for section in ("core_objects", "entries", "register_items"):
        for entry in graph.get(section, []):
            if entry.get("id") == entry_id:
                return entry
    raise KeyError(entry_id)
