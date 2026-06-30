# 102. Mava: a research library for distributed multi-agent reinforcement learning in JAX

## 元信息 (Metadata)
- **标题**: Mava: a research library for distributed multi-agent reinforcement learning in JAX
- **作者**: Ruan de Kock, Omayma Mahjoub, Sasha Abramowitz, Wiem Khlifi, et al.
- **机构**: InstaDeep
- **发表**: arXiv (技术报告) 2023（arXiv:2107.01460v2, 2023-12-15）
- **链接/arXiv**: arXiv:2107.01460v2；https://github.com/instadeepai/Mava

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 不直接针对扰动；面向"统计鲁棒的实验评估"（statistically robust benchmarks/evaluation）的工具支持
- **方法范式**: MARL 软件库 / 基础设施（JAX 加速、distributed training、CTDE/DTDE 下的 MAPPO/IPPO）
- **关键词**: JAX, distributed MARL, MAPPO/IPPO, Anakin architecture, reproducibility

## TL;DR（一句话总结）
提出 Mava——一个纯 JAX 编写的分布式 MARL 研究库，通过向量化与多设备加速实现比现有框架快 10–100x 的训练，并集成 MARL-eval 等工具以支持统计上可靠（robust）的实验评估。

## 问题与动机 (Problem & Motivation)
MARL 研究计算昂贵、采样难、算法实现复杂，难以获得足够样本做出统计稳健的结论；现有框架要么过慢要么过于僵化。需要一个既易读易扩展、又高性能可扩展的工具来快速验证想法并支持可复现研究。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不涉及对抗/扰动威胁模型；"robust"指实验结果的统计稳健性与可复现性（依赖 MARL-eval 的聚合与置信区间报告）
- **设定**: cooperative；支持 CTDE 与 DTDE；以 online 为主，并通过 OG-MARL/Flashbax Vault 支持 offline

## 方法 (Method)
- 采用 CleanRL/PureJAXRL 式"单文件核心算法逻辑"的 clean code 哲学，仅做必要抽象（Hydra 配置、类型定义、环境封装）。
- 基于 Anakin podracer 架构，通过 jax.pmap（跨设备）+ jax.vmap（多 update/多环境）实现可扩展分布式训练。
- 实现 feedforward 与 recurrent 版本的 IPPO 与 MAPPO（CTDE/DTDE）。
- 在训练循环中交错插入评估块（pmap 化），解决端到端 JIT 编译下无法持续评估/checkpoint 的问题，支持 Tensorboard/Neptune/JSON 日志。
- 集成生态：JAX 原生环境（Matrax、Jumanji、JaxMARL/SMAX）、MARL-eval（统计评估）、Flashbax Vault 与 OG-MARL（offline）。

## 理论贡献 (Theoretical Contributions)
无 / 偏工程实证（库与基准报告）。

## 实验 (Experiments)
- **环境/Benchmark**: RWARE、Level-Based Foraging (LBF)、SMAX（SMAC in JAX），矩阵游戏 Matrax
- **Baselines**: EPyMARL (PyTorch)、JaxMARL 的 PPO baselines、OG-MARL 的 MAICQ（offline）
- **评估指标**: Episode return、win rate、steps per second、wallclock 运行时间（遵循 Gorsane et al. 2022 评估协议）

## 主要结果 (Key Results)
- 相同并行环境数下比 EPyMARL 快约 10x；256 个向量化环境时加速超过 100x，性能保持相当或更优。
- 借助 TPU-V3，可在 5 分钟内（部分任务 ~2 分钟）训练至收敛。
- 在 SMAX 上 recurrent IPPO/MAPPO 性能与 JaxMARL baselines 持平；演示了 online-to-offline 流水线（Mava 录制 → OG-MARL MAICQ 离线训练）。

## 局限与未来工作 (Limitations & Future Work)
当前仅支持 JAX 原生环境；实验为初步、未充分调参；路线图包括加入 off-policy 算法、Sebulba 架构以支持非 JAX 环境分布式训练、覆盖全部 SMAX 场景。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 综述中的"工具/基础设施与评估方法论"分支：它本身不提出鲁棒算法，但通过高吞吐实验与 MARL-eval 的统计稳健评估，为开展可复现、统计可靠的 robust MARL 研究提供平台支撑。
