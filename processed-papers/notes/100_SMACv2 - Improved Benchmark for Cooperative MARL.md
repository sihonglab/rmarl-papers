# 100. SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning
- **作者**: Benjamin Ellis, Jonathan Cook, Skander Moalla, Mikayel Samvelyan, Mingfei Sun, Anuj Mahajan, Jakob N. Foerster, Shimon Whiteson
- **机构**: University of Oxford; University College London; Meta AI; University of Manchester; EPFL
- **发表**: NeurIPS 2023 (Datasets and Benchmarks Track)
- **链接/arXiv**: https://github.com/oxwhirl/smacv2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 泛化/分布偏移鲁棒性（要求对未见场景泛化）、随机性（stochasticity）与有意义的部分可观测性；非攻击型，而是 benchmark 层面对鲁棒闭环策略的需求
- **方法范式**: Benchmark 设计、procedural content generation (PCG)、CTDE 评测；非算法
- **关键词**: SMACv2, benchmark, CTDE, partial observability, procedural generation, closed-loop policy

## TL;DR（一句话总结）
指出原 SMAC 因缺乏随机性与有意义的部分可观测性，使得仅依赖时间步的 open-loop 策略即可取得高胜率，并提出通过程序化生成场景（随机队伍组成与初始位置）+ 扩展部分可观测挑战 (EPO) 的 SMACv2，迫使算法学习需泛化的闭环策略。

## 问题与动机 (Problem & Motivation)
SMAC 长期作为 cooperative MARL (CTDE) 主流测试平台，但近年算法在多数场景接近满胜率，出现 ceiling effect。作者通过分析证明：仅以 timestep 为条件、忽略所有观测的 open-loop 策略即可在许多 SMAC 场景取得非平凡胜率；且即便屏蔽全部特征，QMIX 的 joint Q-function 仍可从 timestep 以 <10% 误差回归。说明 SMAC 不够随机、部分可观测性不足，无法逼出复杂闭环策略，需要新基准。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 通过 PCG 每个 episode 随机生成 team composition 与起始位置，制造场景多样性/分布偏移；EPO 仅允许首个发现敌人的 agent 确定看到敌人，制造需隐式通信的有意义部分可观测性；调整视野与攻击范围增加多样性。
- **设定**: cooperative；CTDE（训练集中、执行去中心化）；online

## 方法 (Method)
1. 诊断分析：用 open-loop（仅条件于 timestep）策略与对 joint Q-function 的特征屏蔽回归，量化 SMAC 缺乏随机性。
2. SMACv2 用 procedural content generation 随机化每个 episode 的队伍组成与初始位置，使固定动作序列失效。
3. 引入 extended partial observability challenge (EPO)：限制敌人可见性，要求 agent 隐式通信敌情以优先选择目标。
4. 更新 sight/attack range 增加 agent 多样性；实现可扩展，便于自定义分布。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（benchmark 与诊断分析）

## 实验 (Experiments)
- **环境/Benchmark**: SMAC vs SMACv2（Terran/Zerg/Protoss 多种 5v5、10v10、20v20、非对称如 10_vs_11、20_vs_23 等场景）
- **Baselines**: MAPPO、QMIX（open-loop vs closed-loop 对比），以及 SOTA CTDE 算法
- **评估指标**: Mean Test Win Rate；特征 ablation 对难度贡献

## 主要结果 (Key Results)
- 在 SMAC 上 open-loop（仅 timestep）策略对许多场景仍获高胜率，仅约 4 个地图 open-loop 完全失败，证实 SMAC 随机性不足。
- 在 SMACv2 上 open-loop 策略无法成功学习，必须条件于 ally/enemy 特征，确证新基准需要闭环策略。
- SOTA 算法在许多 SMACv2 场景表现挣扎，表明新基准提供了实质性挑战；ablation 揭示各新观测特征对难度的贡献。

## 局限与未来工作 (Limitations & Future Work)
局限于 StarCraft II 单一游戏环境，无法代表所有多智能体动态，评测应结合多样基准。当前仅一方由 RL 控制；未来可通过双客户端 LAN 实现两队 self-play 对抗训练。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的"评测/基准"维度：强调对未见场景的泛化与有意义部分可观测性是鲁棒、可去中心化策略的前提。为评估鲁棒 cooperative MARL 算法（对环境随机性与分布偏移的鲁棒性）提供标准平台，常与 QMIX/MAPPO 等 CTDE 方法配套使用。
