---
name: gromacs-md-force-fields
description: Select and audit compatible GROMACS force fields for proteins, ligands, carbohydrates, lipids, water, ions, cofactors, and coarse-grained systems. Use when starting a new MD system, changing force fields, parameterizing a ligand, or checking whether an existing topology is scientifically compatible.
---

# Force-Field Selection and Compatibility

Choose one coherent parameter ecosystem before building the system. A force-field name on the protein does not make an arbitrary ligand, water model, lipid, or ion topology compatible.

## Practical families

- AMBER protein families such as ff14SB/ff19SB: pair with the documented AMBER water/ion convention; use GAFF2 plus a documented charge method for ordinary organic ligands. Use GLYCAM for carbohydrates when carbohydrate stereochemistry and torsions are central, following its combination rules.
- CHARMM36m: strong default for proteins and membranes; use CHARMM-compatible TIP3P, CGenFF for ligands, and CHARMM lipid parameters. CHARMM-GUI outputs are useful because they preserve the required topology and restraint conventions.
- OPLS-AA/M: use the matching OPLS water, ion, and ligand parameterization route such as LigParGen where appropriate. Do not silently mix OPLS ligand charges with AMBER bonded terms.
- GROMOS families: use only when the project requires the corresponding GROMOS water/ion and parameterization conventions; avoid starting new projects with legacy combinations without a reason.
- Martini 3: coarse-grained protein, lipid, and ligand parameters must remain in the Martini ecosystem. Do not combine atomistic bonded parameters with Martini beads.
- OpenFF ligands: use only with a documented protein/solvent integration route and validate charges, atom types, 1-4 scaling, and nonbonded combination behavior.

## Mandatory compatibility checks

1. Confirm protein, lipid, ligand, water, ion, and cofactor sources.
2. Inspect `[defaults]`, combination rules, 1-4 scaling, duplicate atom types, and molecule exclusions.
3. Verify ligand topology atom order matches the actual coordinate order; compare atom names, elements, masses, charges, bonds, and total charge.
4. Reparameterize a new ligand pose from its actual structure. Never reuse a topology from a different conformer, tautomer, protonation state, stereoisomer, or atom order without a documented validation.
5. Check protonation and net charge at the simulation pH. Neutralize the system and separately set the intended salt concentration.
6. Run a ligand-only or small-solvent sanity check when the ligand is unusual, charged, flexible, or carbohydrate-like.

## Do not mix silently

Do not combine AMBER protein with CHARMM lipids, CHARMM water with an unvalidated AMBER ion set, GAFF2 bonded terms with CGenFF atom types, or atomistic parameters with Martini. Mixed systems can be made valid in specialized workflows, but require explicit cross-force-field validation and should not be the default.

## Evidence to record

Record force-field version, water model, ligand tool/version, charge method, protonation method, net charge, ion concentration, topology source, and any manual edits. A successful `grompp` only proves syntactic compatibility; it does not prove that the parameters are physically appropriate.
