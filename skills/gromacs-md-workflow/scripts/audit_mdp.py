#!/usr/bin/env python3
"""Audit a GROMACS MDP against the validated protein-ligand MD profile."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = {
    "integrator": "md",
    "dt": "0.002",
    "cutoff-scheme": "verlet",
    "rcoulomb": "1.0",
    "rvdw": "1.0",
    "coulombtype": "pme",
    "pme_order": "4",
    "fourierspacing": "0.16",
    "constraint_algorithm": "lincs",
    "constraints": "h-bonds",
}


def read_mdp(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip().lower()] = " ".join(value.split()).lower()
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mdp", type=Path)
    args = parser.parse_args()
    values = read_mdp(args.mdp)
    errors = []
    notes = []

    for key, expected in REQUIRED.items():
        actual = values.get(key)
        if actual != expected:
            errors.append(f"{key}: expected {expected}, found {actual or '<missing>'}")

    if values.get("nstlist") not in {"10", "20", "50", "100"}:
        notes.append(f"nstlist={values.get('nstlist', '<missing>')}: benchmark or justify this value")
    if "ns_type" in values:
        notes.append("ns_type is obsolete in current GROMACS and should be removed")
    if values.get("dt") == "0.002" and values.get("constraints") != "h-bonds":
        notes.append("2 fs usually requires constraining at least hydrogen bonds")
    if values.get("pcoupl") not in {None, "no", "c-rescale", "berendsen", "parrinello-rahman"}:
        notes.append(f"unusual pressure coupling: {values['pcoupl']}")

    print(f"MDP: {args.mdp}")
    print("STATUS: PASS" if not errors else "STATUS: REVIEW")
    for item in errors:
        print(f"ERROR: {item}")
    for item in notes:
        print(f"NOTE: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
