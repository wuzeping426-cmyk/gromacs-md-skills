---
name: gromacs-md-workflow
description: Set up, run, validate, analyze, and document GPU-accelerated protein-ligand molecular dynamics simulations with GROMACS in WSL. Use for requests to run or resume GROMACS MD, audit mdp/topology/ligand parameters, compare protein-ligand trajectories, calculate RMSD/RMSF/Rg/contact/hydrogen-bond/PCA/free-energy analyses, or create a reproducible report.
---

# GROMACS MD Workflow

Use this workflow for protein-ligand MD in WSL. Prefer the user's existing GROMACS version, directory layout, and scripts after verifying them. Preserve existing results and never overwrite a completed trajectory without explicit approval.

## 1. Discover and verify inputs

1. Identify the project root, protein PDB/GRO, ligand coordinates, topology, index file, MDP files, TPR, checkpoint, trajectory, and analysis outputs.
2. Check the executable with `gmx --version`; for this workspace the validated executable is `/mnt/g/software/gromacs/bin/gmx`.
3. Check the GPU with `nvidia-smi` and record GPU model, driver, CUDA support, MPI ranks, and OpenMP threads.
4. Inspect the ligand residue name, atom count, atom order, total charge, and topology/coordinate atom order before `grompp`.
5. Parameterize every new ligand from the actual ligand structure. Do not reuse an old ligand topology merely because the residue is chemically similar or the name is the same. For this workspace the validated route is ACPYPE with GAFF2 and AM1-BCC/`bcc` charges, followed by a topology-coordinate atom-order check.

## 2. Build the system

Use the existing force-field convention when comparing systems. The validated AvaAGE profile uses `amber99sb-ildn` with a three-site water model, a cubic box with 1.0 nm clearance, PME electrostatics, and neutralizing sodium ions.

Run, in order:

1. Combine the protein and freshly parameterized ligand while preserving the ligand coordinates.
2. Create the box and solvate.
3. Add ions using a dedicated ions MDP and `genion`; record the selected solvent group and final ion counts.
4. Run `grompp` and fail on warnings. Do not use `-maxwarn` as a routine bypass. If an existing project used `-maxwarn`, inspect the generated log and resolve each warning before treating the workflow as reusable.

## 3. Recommended MDP profile

Use 2 fs (`dt=0.002`) with `constraints=h-bonds`, LINCS, PME, `rcoulomb=rvdw=1.0 nm`, `pme_order=4`, and `fourierspacing=0.16 nm` as the starting profile. Use `cutoff-scheme=Verlet` and leave the Verlet buffer tolerance at the GROMACS default/validated value `0.005` unless there is a documented reason to change it.

For energy minimization, use steepest descent with at least 50,000 maximum steps. `emtol=1000` is acceptable for the first clash-removal pass; if the final maximum force remains high or the structure has severe contacts, run a second minimization with a stricter target such as 100. Record the final Fmax and whether GROMACS reports convergence.

For restrained equilibration:

- NVT: 100-500 ps, `V-rescale`, 300 K, `gen_vel=yes` only for the first equilibration stage.
- NPT: 100-1000 ps, `V-rescale`, isotropic `C-rescale` pressure coupling, 1 bar, `tau_p` around 2 ps, and `refcoord_scaling=com` when position restraints are active.
- Keep the ligand restrained during early equilibration only when needed to protect a fragile starting pose; release restraints before production unless the scientific design explicitly requires them.
- `nstlist=10` during short restrained equilibration is conservative. For production, `nstlist=100` is acceptable with Verlet buffering and `dt=0.002`.
- Remove obsolete `ns_type`; current GROMACS ignores it.

For production, use the same physical model as equilibration, `continuation=yes`, `gen_vel=no`, and a checkpoint interval. A 100 ns production run at 2 fs is 50,000,000 steps. Write compressed coordinates every 5,000 steps (10 ps) as a practical starting point; reduce the interval only when analysis or restart requirements justify the larger files.

## 4. GPU execution and restart

Start with one MPI rank and benchmark OpenMP threads. For the validated RTX 3070 Laptop GPU profile, the mutant used `-ntmpi 1 -ntomp 8`; the larger WT system used `-ntmpi 1 -ntomp 16`. Use:

```bash
-ntmpi 1 -ntomp N -pin on
-nb gpu -pme gpu -bonded gpu -update gpu
```

Select `N` from a short benchmark, not from CPU thread count alone. Confirm the log says that one GPU is selected and that PP, PME, bonded, and coordinate-update tasks are on the GPU. Record the final `Performance` line and distinguish active compute throughput from wall-clock time across sleep or checkpoint gaps.

Resume only from a matching checkpoint and TPR:

```bash
gmx mdrun -deffnm 01_Production/md_100ns \
  -cpi 01_Production/md_100ns.cpt -append \
  -ntmpi 1 -ntomp N -pin on \
  -nb gpu -pme gpu -bonded gpu -update gpu
```

Do not launch a second `mdrun` against the same `deffnm`. Use a PID check or an explicit process check for background runs.

## 5. Validation gates

Before calling a run complete, check all of the following:

- `grompp` logs contain no unresolved Warning or Error.
- `gmx check` accepts the trajectory and the final frame/box are present.
- No LINCS warning, NaN, constraint failure, or fatal error appears in the production log.
- Temperature is centered near the target; pressure is noisy but its mean and density/box trend are physically plausible after NPT equilibration.
- The final box, molecule counts, total charge, and ligand atom order match the intended system.
- Protein backbone RMSD and radius of gyration are inspected before interpreting ligand motion.
- PBC-corrected, fitted trajectories are used for structural analyses.
- A single trajectory is not treated as proof of a binding free-energy ranking; use replicas and uncertainty estimates for publication-level claims.

## 6. Standard analyses and reporting

For a completed protein-ligand trajectory, generate at minimum:

- protein backbone and ligand RMSD;
- protein C-alpha RMSF;
- protein radius of gyration;
- protein-ligand minimum distance, COM distance, contacts, and hydrogen bonds;
- ligand displacement/escape trajectory and representative structures;
- PCA and a free-energy landscape when enough frames are available;
- MM/PBSA preparation and calculation only when `gmx_MMPBSA`, AmberTools, and compatible ligand topology are installed and verified.

Use independent group selections for protein, ligand, and protein-ligand complex. State the fitting group and ligand reference used for each RMSD. For MM/PBSA, use a fresh, compatible ligand topology and report frame range, stride, dielectric settings, decomposition settings, and uncertainty. Never claim MM/PBSA is complete when only preprocessing has been done.

Embed the plots next to their corresponding Chinese interpretation in the DOCX report. Structural DOCX checks are not a substitute for visual rendering; state when Word/LibreOffice rendering was not verified.

## Reusable checker

Run `scripts/audit_mdp.py` against each MDP before generating a new TPR. Read `references/validated-profile.md` when deciding whether a deviation is intentional or requires a short benchmark/validation run.
