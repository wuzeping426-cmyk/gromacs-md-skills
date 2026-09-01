---
name: general-enzyme-engineering
description: Design and execute a general multi-model enzyme engineering workflow from protein sequence, structure, ligand, and experimental activity data.
metadata:
  short-description: Multi-model enzyme engineering workflow
---

# General enzyme engineering

Use this skill when the user asks to improve an enzyme, rank mutations, design an experimental round, combine protein language models with docking/structure/stability tools, or iterate from assay data.

Read [references/workflow_protocol.md](references/workflow_protocol.md) before executing a nontrivial workflow.

## Required behavior

- Start with objective definition and input/tool smoke tests.
- Distinguish sequence-only, structure-only, ligand-conditioned, and assay-supervised modes.
- Protect catalytic-core residues by default; treat direct substrate contacts cautiously and prioritize second-shell/entrance positions unless evidence supports otherwise.
- Use VenusREM for structure/evolution acceptability, EVOLVEpro for ESM2-embedding plus assay-trained activity regression, LigandMPNN for ligand-conditioned local design, SolubleMPNN/ThermoMPNN for risk filtering, UniKP for kinetic trends, Dyna-1 for fast dynamics, and GROMACS only for a small validated shortlist.
- Keep VenusREM, EVOLVEpro, and LigandMPNN as independent evidence sources. Normalize within each tool and use consensus/rank intersection; never add incomparable raw scores.
- Rebuild and re-dock shortlisted mutants rather than reusing the wild-type pose.
- Preserve experimental chronology and prevent future-round leakage.
- Clearly label measured facts, predictions, hypotheses, and unverified or failed stages.
- Never present docking, PLM, stability, solubility, or MD scores as measured activity, affinity, free energy, Km, or kcat.

## Deliverables

Produce a reproducible manifest, candidate table, parameter record, rejection reasons, and an experimental shortlist with diversity and uncertainty noted. If a required model or dependency is unavailable, perform a safe validated fallback or stop that stage explicitly; do not fabricate output.
