"""Hoppe Engine v3 — append-only ledger.

One JSON object per line. Entries are never edited, reordered, or
deleted by this code; corrections arrive as new entries (supersession).
Sequence numbers are logical (line count + 1), never wall-clock stamps,
so a run's printed output is deterministic: same inputs, same outputs.
"""
import json
from pathlib import Path


class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("")
        self._count = sum(1 for line in self.path.read_text().splitlines() if line.strip())

    def append(self, kind, detail):
        self._count += 1
        entry = {"seq": self._count, "kind": kind, "detail": detail}
        with self.path.open("a") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry

    def entries(self):
        out = []
        for line in self.path.read_text().splitlines():
            if line.strip():
                out.append(json.loads(line))
        return out
