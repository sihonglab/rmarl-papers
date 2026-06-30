# 165. Robustness Evaluation of Multi-Agent Reinforcement Learning Algorithms Using GNAs

## 元信息 (Metadata)
- **标题**: Robustness Evaluation of Multi-Agent Reinforcement Learning Algorithms Using GNAs
- **作者**: Xusheng Zhang, Wei Zhang, Yishu Gong, Liangliang Yang, Jianyu Zhang, Zhengyu Chen, Sihong He
- **机构**: Penn State；Harvard；Washington State University；University of Michigan；Zhejiang University；University of Connecticut（多机构合作）
- **发表**: Tiny Papers @ ICLR 2023
- **链接/arXiv**: 未明确（ICLR 2023 Tiny Papers Track）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 观测扰动（observation-wise）与动作/执行扰动（execution-wise），以 i.i.d. Gaussian noise 注入；对应测量误差、操作误差等不确定性
- **方法范式**: 鲁棒性评估/基准（Gaussian Noise Attack, GNA）、实证分析，非新算法
- **关键词**: robustness evaluation, Gaussian noise attack, MADDPG, observation/execution perturbation, MPE

## TL;DR（一句话总结）
提出用 Gaussian noise attack (GNA) 作为通用基线，系统评估基准 MARL 算法 MADDPG 对观测信息与执行信息扰动的鲁棒性，是首个在 8 个 MPE 场景上分别注入 observation-wise 与 execution-wise 高斯噪声的工作，发现两类攻击呈现完全不同的模式，并报告若干反直觉现象（在某些复杂场景下加噪反而提升回报）。

## 问题与动机 (Problem & Motivation)
MARL 在博弈、交通、机器人等顺序决策问题上表现优异，但部署到现实时，来自观测与执行的不确定性（测量、模型、操作误差）会显著降低性能。尽管鲁棒性对部署至关重要，目前缺乏对 MARL 算法的系统化鲁棒性评估协议。ML 领域常用向输入注入高斯噪声（GNA）来量化鲁棒性，提供通用基线。本文据此首次系统评估 MADDPG 对观测与执行高斯噪声的鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 向策略输入（observation）或策略输出（execution/action）注入 i.i.d. 高斯噪声 N(µ, σ)；µ ∈ {−3,…,3}、σ ∈ {3,2,1,0.5,0.25,0.1} 网格扫描；测试期施加，不改训练
- **设定**: cooperative / competitive / mixed（MPE 8 场景）；CTDE（MADDPG）；评估为部署后（执行期）鲁棒性测试

## 方法 (Method)
- 在 MPE 的 8 个场景（MC、CC、CN、PD、EC、KA、PP、CG）训练 MADDPG 策略，以无噪声下 10000 步的智能体平均回报为 baseline
- **observation-wise GNA**：在策略输入的状态观测上加 N(µ, σ)，使智能体仿佛看到不同状态
- **execution-wise GNA**：在策略输出动作参数上加 N(µ, σ)，使实际执行动作偏离最优
- 每组实验只施加一种噪声，扫描 µ、σ 网格，比较各场景智能体（及对手）平均回报相对 baseline 的变化

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（提供系统化的 GNA 鲁棒性评估协议与实验观察，无理论分析）。

## 实验 (Experiments)
- **环境/Benchmark**: MPE（multiagent-particle-envs）8 个场景，含 cooperative/competitive/mixed
- **Baselines**: 无噪声下 MADDPG 的智能体平均回报
- **评估指标**: 10000 步测试的智能体（及对手）mean reward 相对 baseline 的变化

## 主要结果 (Key Results)
- observation-wise 与 execution-wise GNA 呈现完全不同的影响模式，且效果高度依赖场景
- observation-GNA：在 MC/CC/CN/KA/CG 等场景显著降低回报（甚至 N(0,0.1) 这种近 baseline 噪声也致下降）；而 PP/EC/PD 在某些参数下回报反而提升
- execution-GNA：CN/CC/KA 对 µ 不敏感、小 σ 下较鲁棒；PD/PP/CG 中 σ 起主导作用，PD 在大 σ 下回报反升，PP/CG 出现"小 σ 升、大 σ 降"的反向效应
- 多处反直觉现象表明复杂环境中加噪有时反而有益，可指导未来鲁棒 MARL 算法设计

## 局限与未来工作 (Limitations & Future Work)
仅评估单一算法 MADDPG 与单一噪声类型（高斯）；现实噪声常为非高斯分布，作者将其他类型噪声/攻击下的评估列为未来工作；Tiny Paper 篇幅有限，缺少机理性解释与更多算法对比。

## 与综述的关联 (Relevance to Survey)
本文属 robust MARL 中 [[鲁棒性评估/基准]] 线，把单智能体 ML 常用的 [[Gaussian noise attack]] 引入 MARL，区分 [[观测扰动]] 与 [[动作/执行扰动]] 两类威胁，为综述提供评估协议视角与脆弱性实证；其反直觉发现为 [[状态对抗 MARL]]、[[对抗训练]] 等防御方法的必要性提供动机性证据。
