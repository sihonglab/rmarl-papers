# 97. Empirical Study on Robustness and Resilience in Cooperative Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Empirical Study on Robustness and Resilience in Cooperative Multi-Agent Reinforcement Learning
- **作者**: Simin Li, Zihao Mao, Hanxiao Li, ... Yaodong Yang, Weifeng Lv, Xianglong Liu (et al.)
- **机构**: Beihang University; Zhongguancun Laboratory; Peking University; Hefei Comprehensive National Science Center; Nanyang Technological University
- **发表**: NeurIPS 2025
- **链接/arXiv**: arXiv:2510.11824v2；代码 https://github.com/BUAA-TrustworthyMARL/adv_marl_benchmark

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 观测扰动（Gaussian / greedy worst-case / learned optimal attack）、动作扰动（random / greedy / learned policy）、环境不确定性（动力学参数如质量/速度）；区分 all-agent vs single-agent 作用域
- **方法范式**: 大规模实证基准研究（非新算法）；robustness vs resilience 形式化定义；超参数对可信 MARL 的影响分析
- **关键词**: Trustworthy MARL, Robustness, Resilience, Hyperparameters, Uncertainty, Empirical Benchmark

## TL;DR（一句话总结）
通过 82,620 次实验，跨 4 个真实世界环境、13 种不确定性、15 个超参数，系统区分并评估合作 MARL 的 robustness（抗扰）与 resilience（恢复力），发现合作性能与鲁棒性的关联随扰动强度增强而减弱、鲁棒性不跨不确定性模态/作用域泛化，且超参数调优（而非算法本身）对可信性起关键作用。

## 问题与动机 (Problem & Motivation)
合作 MARL 常在理想仿真中调超参以最大化合作性能，但部署于现实时面临观测/动作/环境不确定性导致性能崩溃。控制论中 robustness（抗扰稳定）与 resilience（从冲击恢复）是互补且不同的概念，但 MARL 文献常将二者混淆且忽视 resilience。同时超参数在 RL/MARL 中的作用常被理论分析忽视，其对鲁棒性与恢复力的影响尚未充分研究。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: U 为决策过程上的不确定性分布。Robustness：固定合作策略，在持续不确定性 u∼U 下度量累积回报。Resilience：从经历不确定性后到达的扰动状态 s_u 重新开始一个 episode（之后无额外扰动），度量恢复能力。观测攻击 ε=0.1（all）/0.2（single）；动作扰动建模为 επ̂+(1−ε)π；环境不确定性取 50 rollout 的最坏情况。共 27 评估设置（1 合作 + 13 robustness + 13 resilience）。
- **设定**: cooperative（Dec-POMDP）；CTDE；online 训练（默认超参，逐一变更），部署期注入扰动评估

## 方法 (Method)
- 形式化区分 robustness（J_robust，持续扰动下的期望回报）与 resilience（J_resilience，从扰动后状态 s_u 恢复的期望回报），并以电网类比说明二者互补。
- 评估三类连续/离散控制 MARL 算法：MADDPG、MAPPO、HAPPO。
- 系统扫描 15 个通用与算法专属超参数（hidden size、γ、激活函数、初始化、网络类型、学习率、critic LR、feature norm、参数共享、early stop、N-step、探索噪声、entropy、GAE、PopArt），每次只变一个，得 34 个实现变体。
- 实验流程：默认超参训练→固定模型测 robustness→从扰动状态重启测 resilience；5 种子 × 27 设置 × 18 任务 × 34 超参 = 82,620 实验（约 230K GPU 小时）。

## 理论贡献 (Theoretical Contributions)
偏实证；主要理论性贡献为对 robustness 与 resilience 的形式化定义（J_robust / J_resilience）及二者区别的概念框架与 case study，非收敛性/复杂度结果。

## 实验 (Experiments)
- **环境/Benchmark**: 4 个真实世界环境共 18 任务——DexHand（灵巧手操作，Isaac Gym）、Quads（四旋翼集群导航）、Traffic（SUMO 智能交通信控）、Voltage（IEEE 标准主动电压控制）。
- **Baselines**: MADDPG、MAPPO、HAPPO 三个 backbone 及其超参数变体；并验证结论可推广到基于这些 backbone 的 robust MARL 方法。
- **评估指标**: episode reward；cooperation/robustness/resilience 的归一化得分；三者间 Pearson 相关；性能退化百分比；two-way ANOVA。

## 主要结果 (Key Results)
- 合作与鲁棒性/恢复力的相关性随扰动强度线性减弱：cooperation–robustness 相关随退化加剧 r=0.85，cooperation–resilience r=0.76（均 p<.001）；即温和扰动可靠优化合作应对，强扰动需专门策略。算法敏感性不同：MADDPG 对动作噪声更鲁棒，MAPPO/HAPPO 对观测不确定性更优。
- 鲁棒性/恢复力不跨不确定性模态或作用域泛化：对 all-agent 动作噪声鲁棒的策略可能在 single-agent 观测噪声下失效；需分别评估 obs/act/env 与个体/全局扰动。
- 超参数调优至关重要且有反直觉发现：parameter sharing、GAE、PopArt 在不确定性下可能损害鲁棒性；early stop、critic LR > actor LR、Leaky ReLU 持续有益。仅优化超参即平均提升 cooperation 52.60%、robustness 34.78%、resilience 60.34%；推广到 robust MARL 方法时提升达 89.43%/65.83%/82.96%。
- two-way ANOVA 显示 18 个任务中有 9 个超参数比算法选择对三项指标影响更显著（p<.001）。

## 局限与未来工作 (Limitations & Future Work)
研究聚焦基于 policy gradient 的 MARL 算法（因多数环境需连续控制），可通过将新算法集成进开源 codebase 缓解。未来可扩展到 value-based 方法、更多环境与不确定性类型，并发展显式针对 resilience（从扰动状态主动恢复）的算法。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的“大规模实证基准/评估协议”主题，并引入与 robustness 互补的 resilience 维度。横跨观测/动作/环境三类不确定性与多种攻击强度（Gaussian、greedy worst-case、learned optimal），可作为综述中“评估与可信性”及“超参数/实现因素影响”一节的核心参考，与其它鲁棒性测试工作（critical agent、state perturbation 等）互补。
