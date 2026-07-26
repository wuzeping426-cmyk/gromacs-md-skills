# GROMACS MD Skills

可复用的 GROMACS 分子动力学 Skill 集合，面向 WSL + GPU 环境下的蛋白、配体、膜蛋白和蛋白-蛋白复合物模拟。

## Skills

| Skill | 用途 |
|---|---|
| `gromacs-md-workflow` | 通用蛋白-配体 MD 建系、GPU 运行、断点续跑、验证和报告 |
| `gromacs-md-membrane` | 膜蛋白、脂双层、膜结合体系，含半各向异性压强耦合和膜专属分析 |
| `gromacs-md-protein-protein` | 蛋白-蛋白复合物、抗体-抗原、多聚体和界面稳定性 |
| `gromacs-md-force-fields` | AMBER、CHARMM、OPLS、GROMOS、Martini、OpenFF 的选择和兼容性核对 |
| `gromacs-md-analysis` | PBC 修正、RMSD/RMSF/Rg、接触、氢键、PCA/FEL、MM/PBSA 和 DOCX 报告 |

## 安装到 Codex

将 `skills` 下需要的 Skill 文件夹复制到本机 Skill 目录：

```powershell
Copy-Item -Recurse -Force .\skills\gromacs-md-workflow "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse -Force .\skills\gromacs-md-membrane "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse -Force .\skills\gromacs-md-protein-protein "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse -Force .\skills\gromacs-md-force-fields "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse -Force .\skills\gromacs-md-analysis "$env:USERPROFILE\.codex\skills\"
```

安装后可直接使用：

```text
Use $gromacs-md-membrane to audit and run this membrane-protein simulation.
Use $gromacs-md-force-fields to check whether this ligand topology is compatible.
Use $gromacs-md-analysis to analyze this trajectory and produce a Chinese report.
```

## 设计原则

- 新配体必须从实际结构重新参数化，禁止按名称套用旧配体拓扑。
- `grompp` Warning 必须解释和修复，不能把 `-maxwarn` 当作默认解决方案。
- 运行速度、结构稳定性、参数物理兼容性和自由能结论分开验证。
- MM/PBSA 只有在实际运行并检查收敛后才能报告。
- 不同体系比较时统一力场、时间窗口、采样间隔、拟合组和图形尺度。

## 校验

```powershell
python .\scripts\validate_collection.py
```

本集合中的 Skill 遵循 Codex Skill 目录规范；每个 Skill 的 `SKILL.md` 保持短小，细节放在同目录的 `references/` 或 `scripts/` 中。
