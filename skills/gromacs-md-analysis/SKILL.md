---
name: gromacs-md-analysis
description: Analyze protein, protein-ligand, membrane, and protein-protein GROMACS trajectories with reproducible PBC correction, fit-aware stability and binding metrics, Nature-style figures, projected population landscapes, MM/PBSA preparation, and Chinese DOCX reporting.
---

# GROMACS Trajectory Analysis

Start by inventorying the TPR, trajectory, index groups, topology, checkpoint/log, and simulation intervals. State whether the analysis includes equilibration or production only.

## Coordinate preprocessing

1. Make a whole-molecule, PBC-corrected trajectory. Keep a protein-ligand or complex trajectory for visual inspection and separate protein/ligand groups for metrics.
2. Fit protein backbone or C-alpha coordinates for protein RMSD/RMSF and ligand-in-pocket motion. Do not fit on the ligand when measuring ligand displacement relative to the protein.
3. Verify atom counts, residue numbering, ligand atom order, box vectors, frame time, and selection groups before plotting.

### Complexes, dimers, and PBC artifacts

- For dimers, multimers, or multi-ligand systems, cluster complete solute (all protein chains plus all ligands) before centering and fitting. Protein-only clustering can leave a ligand in a neighboring image; including ions can destabilize the imaging group.
- Confirm `trjconv` receives clustering, centering, and output selections. Inspect the clean trajectory and raw RMSD before interpretation.
- A repeated jump from near-zero to several nm that returns at adjacent frames is normally a periodic-image artifact. Correct PBC and recompute all dependent metrics; never smooth or clip it.
- Split RMSF by chain for homo-oligomers. Duplicate residue numbers from different chains must not be connected on one curve.

See `references/nature_report_workflow.md` for the reproducible figure and report contract.

### Structural panels

- Export representative structures only from the PBC-clean trajectory. Record the frame time, fitting procedure, selection, and why each frame represents the reported state.
- Use `scripts/run_pymol_render.py` to run a reviewed PML script headlessly and check that its PNG was created. Run `--self-test` after configuring `PYMOL_EXE` before promising a batch render.
- Read `references/pymol-md-figures.md` for reproducible protein-ligand, aligned-state, and MD snapshot PML recipes. Keep structural panels sparse and use them to support a metric-derived conclusion.
- A single-frame geometric donor/acceptor selection is a visual aid, not a trajectory hydrogen-bond occupancy calculation. Use GROMACS or a validated analysis package for the quantitative result.

## Core metrics

Generate and report:

- protein backbone RMSD and ligand RMSD after protein fitting;
- protein C-alpha RMSF with residue numbers and chain IDs;
- protein radius of gyration and, for membranes, membrane area/thickness;
- protein-ligand or inter-chain minimum distance, COM distance, contacts, hydrogen bonds, and representative structures;
- ligand displacement, orientation, pocket residence, and possible escape episodes;
- temperature, pressure, density, box size, and energy sanity plots.

Report mean, standard deviation, range, and time-window statistics. For a late RMSD spike, check PBC, fitting group, ligand atom order, contacts, COM distance, and the trajectory itself before calling it dissociation.

### Binding-state interpretation

- Do not infer unbinding from ligand RMSD alone. Combine protein-fitted ligand RMSD with ligand SASA, protein-ligand COM distance, minimum distance, local contact-residue occupancy, and representative pre/post-event structures.
- State the cutoff and definition of every contact metric. Raw `gmx mindist -on` counts atom pairs and can be thousands; it is not a residue-contact count.
- For a pose switch, compare matched windows before and after the event, calculate residue contact occupancy in each, and plot the difference with chain-qualified labels.
- If `gmx hbond` fails to recognize chemically plausible donor/acceptor atoms, treat this as a topology-recognition limitation. Do not report zero hydrogen bonds; define chemistry explicitly or use a validated external method.

## PCA and free-energy landscapes

Run covariance/PCA on a clearly stated group, normally fitted protein C-alpha atoms. Plot eigenvalue variance, PC projections, and a two-dimensional population-based free-energy landscape. Label this as a projected population landscape, not a rigorous thermodynamic free energy, unless a validated enhanced-sampling/PMF method was used. Use consistent temperature and reference conventions between systems.

For a conventional 100 ns trajectory, RMSD-Rg and ligand RMSD-pocket/COM projections are useful sampling summaries. A histogram transform `-kBT ln(P/Pmax)` is not a converged binding free energy or barrier; state frame range, stride, bins, temperature, and this boundary.

## Nature-style figures

Before plotting, define a one-sentence conclusion, panel map, evidence hierarchy, source data, and reviewer risks. Use a restrained color-blind-safe palette. A protein-ligand report normally contains:

1. Main stability figure: protein RMSD, ligand RMSD after protein fitting, chain-separated RMSF, Rg.
2. Main binding-state figure: ligand COM distance and a local contact-residue or contact-atom metric.
3. Event figure when needed: early-versus-late residue occupancy plus protein-fitted representative poses.
4. Supplementary controls: temperature/pressure/density, potential energy, protein/ligand SASA, PCA sampling, and projected population landscapes.

Export editable SVG/PDF, 600 dpi TIFF, and PNG preview. Use 5-7 pt body text at final width, lower-case bold panel labels, no top/right spines, and no rainbow palette. Verify all PNGs. Never place an unvalidated MM/PBSA value or a strict free-energy claim in a figure.

## MM/PBSA

Prepare compatible complex, receptor, and ligand topologies and a PBC-clean trajectory. Check that `gmx_MMPBSA` and AmberTools are installed before starting. Record frame range, stride, dielectric constants, salt settings, radii, decomposition choices, and all warnings. Check convergence by blocks or windows and report uncertainty. Do not present a prep directory as a completed MM/PBSA result.

## Comparison and reporting

For WT/mutant or two complexes, use identical frame windows, stride, fitting group, atom selections, plot scales, and units. Overlay the curves and provide a delta plot where useful. Separate direct observations from mechanistic interpretation.

Put each figure beside its Chinese interpretation in the DOCX. Captions state data source, selection, time window, units, and limitations. The report states force field, duration, PBC/fit procedure, and replicate count.

For a net-new report include: conclusion summary, methods table, stability results, binding-state interpretation, thermodynamic controls, projected-landscape boundary, limitations, and next steps. Render DOCX to page PNGs and inspect them. If LibreOffice/Word rendering is unavailable, run structural checks and explicitly state that visual QA was not completed.
