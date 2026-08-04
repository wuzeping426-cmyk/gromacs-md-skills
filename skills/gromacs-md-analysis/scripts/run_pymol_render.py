#!/usr/bin/env python3
"""Run a PyMOL PML script headlessly and verify its requested image output.

Adapted from Ling-MD/md-agent-skills under the MIT License. See the
repository-root THIRD_PARTY_NOTICES.md for attribution and license terms.
"""

from __future__ import print_function

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_pymol(explicit):
    candidates = [explicit, os.environ.get("PYMOL_EXE"), shutil.which("pymol")]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    raise FileNotFoundError("PyMOL was not found. Set --pymol-exe or PYMOL_EXE.")


def write_self_test(pml_path, output_path):
    pml_path.write_text(
        "\n".join(
            [
                "reinitialize",
                "bg_color white",
                "set ray_opaque_background, off",
                "pseudoatom first, pos=[0,0,0]",
                "pseudoatom second, pos=[2,0,0]",
                "show spheres, first or second",
                "color cyan, first",
                "color orange, second",
                "zoom all, 3",
                "ray 900, 650",
                "png %s, dpi=150" % output_path.as_posix(),
                "quit",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="Run a PyMOL PML script headlessly.")
    parser.add_argument("--pml", help="PML script to run.")
    parser.add_argument("--output", help="Expected image output to verify.")
    parser.add_argument("--pymol-exe", help="PyMOL executable path.")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout in seconds.")
    parser.add_argument("--self-test", action="store_true", help="Render a small PyMOL test image.")
    args = parser.parse_args()

    pymol = find_pymol(args.pymol_exe)
    temporary = None
    if args.self_test:
        temporary = tempfile.TemporaryDirectory(prefix="pymol-render-test-")
        root = Path(temporary.name)
        output = Path(args.output).resolve() if args.output else root / "self_test.png"
        pml = root / "self_test.pml"
        write_self_test(pml, output)
    else:
        if not args.pml:
            parser.error("--pml is required unless --self-test is supplied")
        pml = Path(args.pml).resolve()
        if not pml.exists():
            raise FileNotFoundError("PML script not found: %s" % pml)
        output = Path(args.output).resolve() if args.output else None

    result = subprocess.run([pymol, "-cq", str(pml)], text=True, capture_output=True, timeout=args.timeout)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.returncode:
        return result.returncode
    if output:
        if not output.exists() or not output.stat().st_size:
            sys.stderr.write("Expected image was not created: %s\n" % output)
            return 2
        print("Rendered: %s (%d bytes)" % (output, output.stat().st_size))
    if temporary:
        temporary.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
