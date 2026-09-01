# Detailed enzyme engineering workflow

## Workflow

```text
Objective and constraints
→ input and environment QC
→ structure/ligand preparation
→ GNINA/DiffDock multi-pose docking
→ catalytic-core and pocket annotation
→ VenusREM whole-site scan
→ EVOLVEpro ESM2 embedding plus assay regression
→ LigandMPNN ligand-conditioned design
→ independent rank-based cross-validation
→ retain approximately 20–30 candidates
→ Boltz-2/ESMFold mutant structure rebuilding
→ GNINA/DiffDock re-docking
→ SolubleMPNN and ThermoMPNN risk filtering
→ UniKP kinetic-trend support
→ Dyna-1 fast dynamics screen
→ GROMACS for approximately 3–5 validated candidates when justified
→ experimental panel
→ chronological assay feedback into the next round
```

## Model roles

- VenusREM: structure/evolution acceptability from protein structure and MSA; not direct substrate-specific activity.
- EVOLVEpro: ESM2 mutant embeddings plus target-protein assay data, usually with a top-layer regressor such as random forest.
- LigandMPNN: local ligand-conditioned sequence design; not an activity predictor.
- GNINA/DiffDock: comparative pose and interaction evidence; not measured affinity or catalytic rate.
- SolubleMPNN/ThermoMPNN: solubility and stability risk filters.
- UniKP: auxiliary relative trends for kcat, Km, or kcat/Km; validate experimentally.
- Dyna-1/GROMACS: dynamic stability and complex persistence; not proof of improved activity.

## Non-negotiable safeguards

1. Default-protect catalytic-core residues; cautiously handle direct substrate contacts; prioritize second-shell and entrance positions.
2. Do not add raw scores from different tools. Convert each to an internal percentile/rank and prefer candidates supported independently by multiple models.
3. Rebuild and re-dock each shortlisted mutant; do not reuse the wild-type pose as evidence.
4. Keep experimental rounds chronological. Train only on data available before the prediction round.
5. Record input hashes, software/model versions, parameters, outputs, uncertainty, and rejection reasons.
6. If sequence, structure, ligand chemistry, a model dependency, or a docking pose is unreliable, lower confidence or stop the affected stage rather than fabricate certainty.
