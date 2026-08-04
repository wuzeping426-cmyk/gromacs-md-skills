# Protein-Protein Interface Analysis

Use the same fitted, PBC-corrected trajectory for comparable metrics, but define selections explicitly for chain A and chain B.

- Chain-wise backbone RMSD and C-alpha RMSF.
- Inter-chain heavy-atom contacts at 0.35 and 0.40 nm.
- Inter-chain hydrogen bonds and salt bridges with occupancy.
- Buried and exposed SASA, preferably with a consistent probe radius.
- Chain COM separation and relative orientation.
- Interface residue contact maps and representative structures.

Use persistent contact loss plus separation/orientation evidence before describing dissociation. Report the analysis window after restraints are released.

## Reproducible snapshot panel

Use a PBC-corrected representative snapshot rather than an unprocessed coordinate file:

```powershell
<pymol-python> scripts/render_interface_polar_contacts.py `
  --pdb representative_75ns.pdb --chain-a A --chain-b B --out-dir figures
```

The command writes a PNG, editable PML, and TSV table of cross-chain donor/acceptor geometry returned by PyMOL. This is suitable for selecting residues for a structural panel. It is not a hydrogen-bond occupancy calculation, does not identify water-mediated interactions, and does not establish interaction persistence. Reconcile shown contacts with the quantitative GROMACS analysis before interpretation.
