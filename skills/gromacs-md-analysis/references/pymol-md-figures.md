# PyMOL MD Snapshot Figures

Use this reference after selecting frames from PBC-clean trajectories. Set `input.pdb`, residue names, and output paths explicitly; do not edit an untracked GUI scene.

## Publication setup

```pml
reinitialize
bg_color white
set ray_opaque_background, off
set antialias, 2
set ray_trace_mode, 1
set ray_shadows, off
set ambient, 0.35
set direct, 0.65
set spec_reflect, 0.15
set cartoon_fancy_helices, on
set cartoon_smooth_loops, on
set depth_cue, off
set orthoscopic, on
```

## Protein-ligand state

```pml
load input.pdb, complex
remove solvent
hide everything
show cartoon, complex and polymer.protein
color gray80, complex and polymer.protein
select ligand, complex and resn LIG
select pocket, byres (complex and polymer.protein within 4.0 of ligand)
show sticks, ligand or pocket
color orange, ligand
color slate, pocket and elem C
color red, pocket and elem O
color blue, pocket and elem N
set stick_radius, 0.20
zoom ligand or pocket, 8
png binding_state.png, width=2400, height=1800, dpi=300, ray=1
quit
```

Use actual residue names and show only residues that support the conclusion. Dashed distances are coordinate measurements, not interaction labels unless independently validated. For an early/late pose comparison, use identical colors, representation, and image dimensions, then state the source frame time in the panel caption.

## Run and verify

```powershell
python scripts/run_pymol_render.py --pml binding_state.pml --output binding_state.png
python scripts/run_pymol_render.py --self-test --output pymol_self_test.png
```

Set `PYMOL_EXE` or pass `--pymol-exe` when `pymol` is not on `PATH`. The output check verifies file creation only; visually inspect the PNG for clipping, ligand occlusion, and label collisions.
