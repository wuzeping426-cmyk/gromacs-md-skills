# Nature-Style MD Analysis and Chinese Report Workflow

## Figure contract

Before plotting, record the conclusion, figure archetype, output formats, panel map, evidence hierarchy, trajectory interval/stride, fit and metric groups, PBC strategy, replicate count, and reviewer risks.

For a late ligand event, use language such as `pose reorganization with retained protein proximity` or `candidate escape requiring confirmation`. Do not make an energy claim from RMSD alone.

## Preprocessing checklist

1. Inventory TPR, XTC/TRR, EDR, log, index, topology, production interval, and groups.
2. Run `gmx check` and scan logs for `LINCS`, `NaN`, and fatal errors.
3. Cluster complete solute for oligomer/multi-ligand systems, center on protein, and inspect the output trajectory.
4. Fit on protein backbone for protein stability and ligand displacement. Never fit on the measured ligand.
5. Verify chain IDs, residue numbering, atom order, frame time, and PBC continuity before plotting.

## Useful command patterns

Use group names from the actual index:

```bash
# Cluster protein plus ligands, center protein, and retain all coordinates.
printf 'Solute\nProtein\nSystem\n' | gmx trjconv -s md.tpr -f md.xtc -n index.ndx \
  -o complex_pbc.xtc -pbc cluster -center -ur compact -tu ns -skip 10

# Protein-fitted complex.
printf 'Backbone\nSystem\n' | gmx trjconv -s md.tpr -f complex_pbc.xtc -n analysis.ndx \
  -o complex_protein_fit.xtc -fit rot+trans -tu ns

# Ligand displacement relative to protein and protein-ligand COM distance.
printf 'Backbone\nCPM\n' | gmx rms -s md.tpr -f complex_pbc.xtc -n analysis.ndx -o cpm_rmsd.xvg -tu ns
gmx distance -s md.tpr -f complex_pbc.xtc -n analysis.ndx \
  -select 'com of group "Protein" plus com of group "CPM"' -oav cpm_com.xvg -tu ns

# Dynamic residue identities for an early event window.
gmx select -s md.tpr -f complex_pbc.xtc -n analysis.ndx -resnr index -seltype res_com \
  -b 20000 -e 70000 \
  -select 'same residue as (group "Protein" and within 0.45 of group "CPM")' \
  -oi cpm_contact_residue_early.dat
```

## Evidence for pose reorganization

- Sustained protein-fitted ligand RMSD transition, not an isolated spike.
- PBC-clean trajectory removes periodic-image jumps.
- COM distance, SASA, local contacts, and minimum distance distinguish retained binding from escape.
- Contact-residue occupancies identify interactions lost and gained in matched windows.
- Protein-fitted snapshots span before, transition, and after the event.
- One trajectory establishes a candidate event; independent replicas are needed for robustness.

## Projected population landscapes

For an equilibrium trajectory, form a 2D histogram and transform occupied bins with `-kBT ln(P/Pmax)`. Captions must state variables, selections, frame range, stride, bins, temperature, and `projected population landscape from conventional MD`. It is not a converged PMF, binding free energy, or kinetic barrier.

Appropriate pairs include protein RMSD-Rg and ligand RMSD-protein COM distance. Match windows and bins between systems.

## Report and verification

The Chinese report contains a conclusion summary, methods table, main figures with local interpretations, supplementary controls, limitations, and recommendations. Include force field, ligand parameter source, system size, duration, PBC/fit groups, stride, and replica count.

Embed PNG previews in DOCX but retain SVG/PDF/TIFF separately. Render the DOCX to page PNGs and inspect every page. If no renderer is available, check headings, tables, embedded images, and figure count structurally, then state that visual render QA was unavailable.
