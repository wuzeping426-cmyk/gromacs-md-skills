#!/usr/bin/env python3
"""Render cross-chain candidate polar contacts from one protein-only PDB snapshot.

Adapted from Ling-MD/md-agent-skills under the MIT License. See the
repository-root THIRD_PARTY_NOTICES.md for attribution and license terms.
"""

from __future__ import print_function

import argparse
import csv
import math
import os
import sys
from pathlib import Path


def parse_color(value):
    value = value.lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("colour must be RRGGBB")
    return [int(value[index:index + 2], 16) / 255.0 for index in (0, 2, 4)]


def pymol_cmd():
    try:
        import pymol
        from pymol import cmd
    except ImportError as exc:
        raise SystemExit("Run this with PyMOL's Python interpreter.") from exc
    pymol.finish_launching(["pymol", "-qc"])
    return cmd


def collect_atoms(cmd, selection):
    atoms = {}
    cmd.iterate_state(
        1,
        selection,
        "atoms[index] = {'name': name, 'resn': resn, 'resi': resi, 'chain': chain, 'coord': (x, y, z)}",
        space={"atoms": atoms},
    )
    return atoms


def atom_label(atom):
    return "%s:%s%s:%s" % (atom["chain"], atom["resn"], atom["resi"], atom["name"])


def distance(left, right):
    return math.sqrt(sum((left[index] - right[index]) ** 2 for index in range(3)))


def write_pml(path, args, pairs):
    output = args.output_png.as_posix()
    pdb = args.pdb.as_posix()
    lines = [
        'load "%s", snapshot' % pdb,
        "remove snapshot and not polymer.protein",
        "bg_color white",
        "set ray_opaque_background, off",
        "set antialias, 2",
        "set ray_trace_mode, 1",
        "set ray_shadows, off",
        "set ambient, 0.35",
        "set direct, 0.65",
        "set spec_reflect, 0.15",
        "set cartoon_fancy_helices, on",
        "set cartoon_smooth_loops, on",
        "set depth_cue, off",
        "set orthoscopic, on",
        "set_color chain_a_blue, [%0.3f, %0.3f, %0.3f]" % tuple(args.chain_a_color),
        "set_color chain_b_orange, [%0.3f, %0.3f, %0.3f]" % tuple(args.chain_b_color),
        "set_color polar_green, [%0.3f, %0.3f, %0.3f]" % tuple(args.contact_color),
        "hide everything, snapshot",
        "show cartoon, snapshot and polymer.protein",
        "color chain_a_blue, snapshot and chain %s" % args.chain_a,
        "color chain_b_orange, snapshot and chain %s" % args.chain_b,
        "set cartoon_transparency, %0.2f, snapshot and polymer.protein" % args.cartoon_transparency,
        "set dash_width, 3",
        "set dash_gap, 0.25",
        "set dash_length, 0.20",
    ]
    residues = set()
    for index, pair in enumerate(pairs, 1):
        left, right, _value = pair
        residues.add((left["chain"], left["resi"]))
        residues.add((right["chain"], right["resi"]))
        lines.extend(
            [
                "show sticks, snapshot and chain %s and resi %s" % (left["chain"], left["resi"]),
                "show sticks, snapshot and chain %s and resi %s" % (right["chain"], right["resi"]),
                "distance polar_%02d, index %d, index %d" % (index, left["index"], right["index"]),
                "color polar_green, polar_%02d" % index,
            ]
        )
    for chain, resi in sorted(residues):
        lines.append("label snapshot and chain %s and resi %s and name CA, \"%%s%%s\" %% (resn, resi)" % (chain, resi))
    lines.extend(
        [
            "zoom snapshot and polymer.protein, %0.1f" % args.zoom_buffer,
            "orient snapshot",
            "png %s, width=%d, height=%d, dpi=%d, ray=1" % (output, args.width, args.height, args.dpi),
            "quit",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Render cross-chain candidate polar contacts from one PDB snapshot.")
    parser.add_argument("--pdb", required=True, type=Path)
    parser.add_argument("--chain-a", default="A")
    parser.add_argument("--chain-b", default="B")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--prefix")
    parser.add_argument("--cutoff", type=float, default=3.6, help="PyMOL donor/acceptor heavy-atom cutoff in Angstrom.")
    parser.add_argument("--angle", type=float, default=55.0, help="PyMOL find_pairs angle parameter.")
    parser.add_argument("--width", type=int, default=2400)
    parser.add_argument("--height", type=int, default=1800)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--cartoon-transparency", type=float, default=0.35)
    parser.add_argument("--zoom-buffer", type=float, default=8.0)
    parser.add_argument("--chain-a-color", type=parse_color, default=parse_color("0B7DB3"))
    parser.add_argument("--chain-b-color", type=parse_color, default=parse_color("E69F00"))
    parser.add_argument("--contact-color", type=parse_color, default=parse_color("009E73"))
    args = parser.parse_args()
    args.pdb = args.pdb.resolve()
    if not args.pdb.exists():
        parser.error("PDB does not exist: %s" % args.pdb)
    output_dir = args.out_dir.resolve() if args.out_dir else args.pdb.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or args.pdb.stem
    args.output_png = output_dir / (prefix + "_interface_polar_contacts.png")
    output_pml = output_dir / (prefix + "_interface_polar_contacts.pml")
    output_tsv = output_dir / (prefix + "_interface_polar_contacts.tsv")

    cmd = pymol_cmd()
    cmd.reinitialize()
    cmd.load(str(args.pdb), "snapshot")
    protein = "snapshot and polymer.protein"
    atoms = collect_atoms(cmd, protein)
    left = "(%s and chain %s and elem N+O+S)" % (protein, args.chain_a)
    right = "(%s and chain %s and elem N+O+S)" % (protein, args.chain_b)
    raw_pairs = cmd.find_pairs(left, right, mode=1, cutoff=args.cutoff, angle=args.angle)
    pairs = []
    seen = set()
    for pair in raw_pairs:
        left_index, right_index = int(pair[0][1]), int(pair[1][1])
        key = tuple(sorted((left_index, right_index)))
        if key in seen or left_index not in atoms or right_index not in atoms:
            continue
        seen.add(key)
        first, second = atoms[left_index], atoms[right_index]
        first["index"], second["index"] = left_index, right_index
        pairs.append((first, second, distance(first["coord"], second["coord"])))
    if not pairs:
        raise SystemExit("No cross-chain candidate polar contacts found with the current chains/cutoff.")

    cmd.remove("snapshot and not polymer.protein")
    cmd.hide("everything", "snapshot")
    cmd.show("cartoon", "snapshot and polymer.protein")
    cmd.set_color("chain_a_blue", args.chain_a_color)
    cmd.set_color("chain_b_orange", args.chain_b_color)
    cmd.set_color("polar_green", args.contact_color)
    cmd.color("chain_a_blue", "snapshot and chain %s" % args.chain_a)
    cmd.color("chain_b_orange", "snapshot and chain %s" % args.chain_b)
    cmd.set("cartoon_transparency", args.cartoon_transparency, "snapshot and polymer.protein")
    for number, (first, second, _value) in enumerate(pairs, 1):
        cmd.show("sticks", "snapshot and chain %s and resi %s" % (first["chain"], first["resi"]))
        cmd.show("sticks", "snapshot and chain %s and resi %s" % (second["chain"], second["resi"]))
        cmd.distance("polar_%02d" % number, "index %d" % first["index"], "index %d" % second["index"])
        cmd.color("polar_green", "polar_%02d" % number)
    cmd.zoom("snapshot and polymer.protein", args.zoom_buffer)
    cmd.orient("snapshot")
    cmd.png(str(args.output_png), width=args.width, height=args.height, dpi=args.dpi, ray=1)
    write_pml(output_pml, args, pairs)
    with output_tsv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["atom_1", "atom_2", "distance_angstrom", "definition"])
        for first, second, value in pairs:
            writer.writerow([atom_label(first), atom_label(second), "%.2f" % value, "PyMOL mode=1 snapshot candidate"])
    print("PNG: %s" % args.output_png)
    print("PML: %s" % output_pml)
    print("TSV: %s" % output_tsv)
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
