---
name: gromacs-md-analysis
description: Analyze protein, protein-ligand, membrane, and protein-protein GROMACS trajectories with reproducible PBC correction, fitting, RMSD/RMSF/Rg, contacts, hydrogen bonds, PCA, free-energy landscapes, MM/PBSA preparation, plots, and DOCX reporting.
---

# GROMACS Trajectory Analysis

Start by inventorying the TPR, trajectory, index groups, topology, checkpoint/log, and simulation intervals. State whether the analysis includes equilibration or production only.

## Coordinate preprocessing

1. Make a whole-molecule, PBC-corrected trajectory. Keep a protein-ligand or complex trajectory for visual inspection and separate protein/ligand groups for metrics.
2. Fit protein backbone or C-alpha coordinates for protein RMSD/RMSF and ligand-in-pocket motion. Do not fit on the ligand when measuring ligand displacement relative to the protein.
3. Verify atom counts, residue numbering, ligand atom order, box vectors, frame time, and selection groups before plotting.

## Core metrics

Generate and report:

- protein backbone RMSD and ligand RMSD after protein fitting;
- protein C-alpha RMSF with residue numbers and chain IDs;
- protein radius of gyration and, for membranes, membrane area/thickness;
- protein-ligand or inter-chain minimum distance, COM distance, contacts, hydrogen bonds, and representative structures;
- ligand displacement, orientation, pocket residence, and possible escape episodes;
- temperature, pressure, density, box size, and energy sanity plots.

Report mean, standard deviation, range, and time-window statistics. For a late RMSD spike, check PBC, fitting group, ligand atom order, contacts, COM distance, and the trajectory itself before calling it dissociation.

## PCA and free-energy landscapes

Run covariance/PCA on a clearly stated group, normally fitted protein C-alpha atoms. Plot eigenvalue variance, PC projections, and a two-dimensional population-based free-energy landscape. Label this as a projected population landscape, not a rigorous thermodynamic free energy, unless a validated enhanced-sampling/PMF method was used. Use consistent temperature and reference conventions between systems.

## MM/PBSA

Prepare compatible complex, receptor, and ligand topologies and a PBC-clean trajectory. Check that `gmx_MMPBSA` and AmberTools are installed before starting. Record frame range, stride, dielectric constants, salt settings, radii, decomposition choices, and all warnings. Check convergence by blocks or windows and report uncertainty. Do not present a prep directory as a completed MM/PBSA result.

## Comparison and reporting

For WT/mutant or two complexes, use identical frame windows, stride, fitting group, atom selections, plot scales, and units. Overlay the curves and provide a delta plot where useful. Separate direct observations from mechanistic interpretation.

Put each figure beside its Chinese result interpretation in the DOCX. Include data source, selection, time window, and units in captions. Structural DOCX validation is not visual rendering; report when LibreOffice/Word rendering was unavailable.
