# Force-Field Compatibility Matrix

| Protein/system | Typical ligand route | Water/ions | Important boundary |
|---|---|---|---|
| AMBER protein | GAFF2 + documented charge method | AMBER-compatible convention | Check 1-4 scaling and carbohydrate choice |
| CHARMM36m / membrane | CGenFF; CHARMM lipids | CHARMM-modified TIP3P and CHARMM ions | Prefer CHARMM-GUI conventions |
| OPLS-AA/M | OPLS-compatible ligand tool | OPLS-compatible water/ions | Do not mix bonded terms across families |
| GROMOS legacy | GROMOS parameter route | Matching SPC/SPC-E convention | Use only with a documented reason |
| Martini 3 | Martini bead parameters | Martini solvent/ions | Do not mix atomistic and CG parameters |

This table is a triage aid, not a substitute for the force-field manual or validation literature. The topology must be audited for atom types, combination rules, exclusions, charges, and 1-4 interactions.
