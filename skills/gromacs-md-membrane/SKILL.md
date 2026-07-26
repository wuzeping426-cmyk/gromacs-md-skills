---
name: gromacs-md-membrane
description: Prepare, run, validate, and analyze atomistic GROMACS simulations of membrane proteins, lipid bilayers, and membrane-bound complexes. Use when the system contains a lipid membrane, transmembrane protein, receptor, transporter, channel, or membrane-associated ligand.
---

# Membrane Protein MD

Treat a membrane simulation as a coupled protein-lipid-water-ion system. Do not reuse a soluble-protein protocol without checking membrane orientation, lipid topology, box geometry, and semi-isotropic pressure coupling.

## Inputs and construction

1. Identify the membrane type, lipid composition, protein orientation, leaflet asymmetry, protonation state, cofactors, ligand, salt concentration, and target temperature.
2. Prefer a validated builder such as CHARMM-GUI for CHARMM36m systems. If using a custom builder, record the lipid coordinates, solvent model, ion parameters, and exact topology source.
3. Keep the force-field ecosystem consistent. For example, use CHARMM36m protein/lipid parameters with the CHARMM-compatible TIP3P water and CGenFF ligand parameters. Do not combine CHARMM lipids with an unrelated water/ion/ligand parameter set without validation.
4. Check protein orientation and membrane overlap visually or by residue depth. Verify that no lipid atom is placed inside the protein and that both leaflets have the intended composition.
5. Solvate, add ions to the target salt concentration and net charge, and record the final lipid, water, and ion counts.

## Equilibration

Use the builder's validated equilibration schedule when available. Otherwise use staged restraints: heavy restraints during initial temperature and pressure equilibration, then gradually release protein backbone and lipid restraints before production. Avoid restraining the membrane and protein indefinitely unless that is the scientific design.

For a bilayer, use semi-isotropic pressure coupling rather than isotropic coupling:

```ini
pcoupl       = C-rescale
pcoupltype   = semiisotropic
ref_p        = 1.0 1.0
tau_p        = 5.0
compressibility = 4.5e-5 4.5e-5
```

Use the exact values supplied by the force-field/builder documentation when they differ. The xy plane must be allowed to equilibrate independently from the membrane normal. Check temperature groups, periodicity, PME, LINCS, and the membrane-specific position-restraint files before `grompp`.

## Production checks

Before accepting production, verify:

- temperature is stable for protein, lipids, and solvent groups;
- area per lipid, box xy area, membrane thickness, and bilayer volume stabilize;
- no leaflet mixing, vacuum layer, water leak, lipid explosion, or protein drift through the membrane occurs;
- pressure coupling is semi-isotropic and the final box is physically plausible;
- no LINCS warning, NaN, or periodic-boundary artifact appears.

Use 2 fs with hydrogen-bond constraints for standard atomistic runs. Use Verlet buffering and PME. Benchmark GPU thread settings after the physical setup is fixed; never trade away membrane pressure-coupling or equilibration quality to improve ns/day.

## Analyses

In addition to common protein analyses, generate area per lipid, leaflet thickness, lipid order parameters, protein tilt and insertion depth, residue-lipid contacts, water occupancy/permeation, pore radius for channels, and ligand depth/orientation. Use membrane-aware PBC treatment and remove whole-molecule jumps before fitting.

For membrane binding or permeation claims, use multiple replicas or enhanced sampling. A single spontaneous binding/unbinding event is descriptive, not an equilibrium free-energy estimate.
