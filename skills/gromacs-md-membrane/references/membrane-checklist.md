# Membrane MD Checklist

## Before `grompp`

- Confirm lipid names and molecule counts in both coordinate and topology files.
- Confirm protein orientation, leaflet asymmetry, membrane clearance, and solvent/ion counts.
- Confirm the force-field-specific water and ion parameters.
- Confirm semi-isotropic pressure coupling and two pressure components.
- Confirm restraint files target the intended protein, lipid, and solvent atoms.

## After equilibration

- Plot temperature by component.
- Plot xy area, area per lipid, z box length, density, and pressure.
- Check membrane thickness and leaflet composition.
- Inspect a PBC-corrected trajectory for water leaks, voids, lipid overlap, and protein drift.

## Publication-facing extras

Report the lipid composition, leaflet counts, protein orientation source, force-field version, water model, salt concentration, equilibration schedule, pressure-coupling method, and number of replicas.
