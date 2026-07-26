# Validated AvaAGE Profile

This reference profile is derived from the completed AvaAGE-GlcNAc runs in `G:\MD_Project`. Treat it as a starting point and revalidate input-specific details for every new system.

## Production MDP

```ini
integrator = md
dt = 0.002
nsteps = 50000000
continuation = yes
constraint_algorithm = lincs
constraints = h-bonds
cutoff-scheme = Verlet
nstlist = 100
rcoulomb = 1.0
rvdw = 1.0
coulombtype = PME
pme_order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = Protein_ligand Water_and_ions
tau_t = 0.1 0.1
ref_t = 300 300
pcoupl = C-rescale
pcoupltype = isotropic
tau_p = 2.0
compressibility = 4.5e-5
gen_vel = no
```

GROMACS 2024.1 generated `verlet-buffer-tolerance=0.005`. The completed runs used `rlist` around 1.157-1.159 nm and an inner pair-list update every 6 steps while the outer list was updated every 100 steps.

## Completed run evidence

| System | Atoms | Water | Na+ | Box (nm) | Performance |
|---|---:|---:|---:|---|---:|
| A172G/A198D | 69,297 | 20,974 | 12 | 8.849^3 | 136.282 ns/day |
| WT | 88,781 | 27,438 | 11 | 9.620^3 | 133.767 ns/day |

Both runs used one RTX 3070 Laptop GPU. The mutant completed at 8 OpenMP threads; the WT completed at 16. A mutant 12-thread test was slower at 114.282 ns/day, so thread count must be benchmarked.

## Known deviations to audit

- Existing setup scripts use `-maxwarn 1`; new workflows should remove it and resolve warnings.
- Existing energy minimization uses `emtol=1000`; this is acceptable as an initial clash-removal pass, but a stricter second minimization may be appropriate.
- Existing NVT/NPT MDPs contain obsolete `ns_type=grid`; GROMACS 2024.1 ignores it. Omit it in new MDPs.
- The WT project uses an older ligand topology, while the mutant project uses freshly generated ACPYPE/GAFF2 ligand parameters. Do not use the WT topology for a new ligand pose without fresh parameterization and atom-order verification.
