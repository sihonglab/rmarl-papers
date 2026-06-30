# 16. Robustness to Multi-Modal Environment Uncertainty in MARL using Curriculum Learning

## 元信息 (Metadata)
- **标题**: Robustness to Multi-Modal Environment Uncertainty in MARL using Curriculum Learning
- **作者**: Aakriti Agrawal, Rohith Aralikatti, Yanchao Sun, Furong Huang
- **机构**: Department of Computer Science, University of Maryland
- **发表**: Pre-print, Under Review（arXiv:2310.08746, 2023）
- **链接/arXiv**: arXiv:2310.08746v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 多模态环境不确定性（同时含 reward、state/observation、action、transition dynamics 不确定性中的两种）
- **方法范式**: 课程学习（curriculum learning, lookahead CL）、robust Markov game、maximin/minimax、robust Nash Equilibrium
- **关键词**: multi-modal uncertainty, curriculum learning, robust MARL, Nash Equilibrium, reward/state/action perturbation

## TL;DR（一句话总结）
本文首次形式化定义 MARL 中的多模态环境不确定性鲁棒问题，并提出基于课程学习（逐步增大噪声参数）的高效训练方法，可同时应对两种不确定性（state/reward/action），在合作与竞争环境中达到 SOTA 鲁棒性。

## 问题与动机 (Problem & Motivation)
MARL sim-to-real 迁移要求策略对各类环境不确定性鲁棒。现有工作只单独研究 action / state / reward / transition 中某一种不确定性，因为 MARL 本身复杂、非平稳、求 NE 困难。但真实世界往往多个环境变量同时存在不确定性，且无法预知是哪一种。本文是首个处理 MARL 多模态（同时两种）不确定性的工作，也是首个处理 MARL 中 action 不确定性的工作。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 定义 general robust Markov game，含 reward 不确定集 R̄、transition 不确定集 P̄、扰动状态集 Ō、扰动动作集 Ā；各扰动用 truncated normal 分布建模（reward 标准差 ϵ、state µ、action ν，截断于 2 倍标准差）。状态扰动只改变其他 agent 观测，不改变真实状态。属 aleatoric uncertainty。
- **设定**: cooperative + competitive + mixed（三个环境）；采用 maximin（policy 最大化、不确定集最小化）；训练阶段引入不确定性；transition 确定故不单独处理

## 方法 (Method)
- 形式化 robust Bellman 方程：对每个 agent i，policy 取 max，同时对四个不确定集（P̄, R̄, s̄, ā）取 min。
- 定义 Robust Nash Equilibrium (RNE) 作为 robust Markov game 的解。
- 课程学习核心：用噪声参数（ϵ/µ/ν）衡量任务难度，从低噪声起 TrainTillSuccess 后逐步增大噪声（lookahead CL），低噪声习得知识迁移加速高噪声学习，提高样本效率。
- 单一不确定性算法（Algorithm 1）与多不确定性算法（Algorithm 2/3：reward+state/action、state+action），多不确定性时用 SkipAhead 同步推进两个参数。
- base model 采用 Zhang et al. 2020（model uncertainty MARL）。

## 理论贡献 (Theoretical Contributions)
- Theorem 1：robust Nash Equilibrium 存在 → 最优值函数存在；证明算子 L 为 contraction mapping（附录给出 reward+transition、state 不确定下的 NE 存在性论证）。NE 在 general 多模态情形下的存在性证明被认为超出本文范围（偏经验为主，理论为辅）。

## 实验 (Experiments)
- **环境/Benchmark**: 三个 multi-particle 环境——Cooperative Navigation（合作）、Keep Away（竞争）、Physical Deception（混合）
- **Baselines**: 不使用 CL 的 base method（Zhang et al. 2020 model-uncertainty MARL）；state 不确定参考 Han et al. 2022
- **评估指标**: success rate（成功率 >90% 视为收敛）、可收敛的最高噪声值、reward 训练曲线（评估时各跑 1000 次取均值/方差）

## 主要结果 (Key Results)
- Cooperative Navigation：CL 将可学习的 reward 噪声从 ϵ=9 提升到 ϵ=47/48；state 从 µ=0.5 到 µ=1.1；action 从 ν=2.0 到 ν=2.4，均超 baseline 达 SOTA。
- 多模态（两种）不确定性下 CL 仍优于 baseline；同时支持两个参数的不确定性，代价是单参数最高噪声略降。
- 三个环境一致表明 CL 单参数优于无 CL；首次给出 MARL action 不确定性结果。

## 局限与未来工作 (Limitations & Future Work)
- 仅处理同时两种不确定性，三种合并会显著降低最终鲁棒性（未给出结果）；general 多模态 NE 存在性缺乏完整理论保证；尚未做真正 sim-to-real 验证。未来：处理三种不确定性、给出 NE 存在条件性理论保证、测试 sim-to-real。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"环境/模型不确定性 + 课程学习"线路，统一了 state/action/reward/transition 多种扰动并首提 multi-modal 设定；与 robust Markov game、minimax、Nash Equilibrium 存在性、curriculum-based robustness、state-adversarial MARL（Han/He et al.）等主题紧密相关，可作为多扰动统一视角的代表工作。
