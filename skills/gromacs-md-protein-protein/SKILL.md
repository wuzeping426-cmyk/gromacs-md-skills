---
name: gromacs-md-protein-protein
description: Build, equilibrate, run, validate, and analyze GROMACS molecular dynamics simulations of protein-protein complexes, oligomers, antibody-antigen systems, enzyme complexes, and multimeric interfaces.
---

# Protein-Protein Complex MD

Use a complex-specific workflow. Preserve chain identities and distinguish internal chain stability from interface stability.

## Preparation

1. Validate each chain's sequence, termini, protonation, cofactors, disulfides, missing residues, and biological assembly.
2. Assemble the complex without changing the experimentally or computationally proposed interface. Check chain IDs, residue numbering, inter-chain atom contacts, and total charge.
3. Use one coherent protein force field, water model, ion model, and ligand/cofactor parameter set. Freshly parameterize nonstandard residues and cofactors.
4. Solvate with at least 1.0 nm clearance unless the system size or experimental design requires more. Neutralize and set the intended ionic strength, not only the net charge.

## Equilibration

Use energy minimization, restrained NVT, restrained NPT, then an unrestrained or lightly restrained pre-production phase. Restrain backbone or heavy atoms only long enough to relax solvent and box density. Do not use permanent interface restraints when the goal is to test interface stability.

Use 2 fs with `constraints=h-bonds`, PME, Verlet buffering, and a reproducible checkpoint schedule. For large complexes benchmark one MPI rank plus GPU offload against a small number of MPI ranks; retain the fastest stable setting only after checking the trajectory.

## Validation gates

- Check each chain's backbone RMSD/RMSF separately and for the full complex.
- Check inter-chain distance, center-of-mass separation, interface contacts, salt bridges, hydrogen bonds, buried SASA, and minimum distance.
- Check whether the interface is stable after excluding the restrained equilibration period.
- Inspect PBC-corrected representative structures for chain separation, artificial periodic contacts, and water penetration.
- Review temperature, density, box size, pressure trend, LINCS warnings, and checkpoint continuity.

For a reproducible interface structure panel, use `scripts/render_interface_polar_contacts.py` on a PBC-clean representative PDB. It exports PNG, PML, and TSV evidence. Its single-snapshot donor/acceptor geometry is a candidate polar-contact display only; validate occupancy with trajectory analysis before calling any pair a persistent hydrogen bond. See `references/interface-analysis.md`.

## Interpretation

High whole-complex RMSD can coexist with a stable interface if the complex rotates or undergoes domain motion. Report chain-wise RMSD and interface metrics together. Interface contact loss is not proof of dissociation unless it persists and agrees with separation/orientation measures.

For binding free energy, MM/PBSA is an endpoint approximation and should be accompanied by frame convergence, decomposition uncertainty, and ideally independent replicas. Do not compare absolute values across incompatible force-field or protonation setups.
