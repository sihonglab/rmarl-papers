# 77. Towards Fault Tolerance in Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Towards Fault Tolerance in Multi-Agent Reinforcement Learning
- **作者**: Yuchen Shi, Huaxin Pei, Liang Feng, Yi Zhang, Danya Yao
- **机构**: Tsinghua University (Dept. of Automation, BNRist); QiYuan Lab
- **发表**: arXiv preprint 2024（疑似面向 IEEE T-ASE，Note to Practitioners 风格）
- **链接/arXiv**: arXiv:2412.00534v1；代码 https://github.com/xbgit/FaultTolerance_AACFT

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 智能体失效/故障 (system-level agent fault)，失效 agent 丧失观测、移动、通信能力；故障随机发生于任意 agent 与任意时刻
- **方法范式**: attention 机制（actor/critic）、Prioritized Experience Replay (PER)、CTDE (MADDPG 骨干)、模型架构 + 采样策略
- **关键词**: fault tolerance, attention, prioritized experience replay, MADDPG, CTDE

## TL;DR（一句话总结）
提出 AACFT，在 MADDPG 的 actor/critic 中引入 attention 机制自动检测故障并动态调节对失效 agent 的关注，并用扩展的 PER 解决 fault 前后样本不平衡，从而提升 MARL 的容错性。

## 问题与动机 (Problem & Motivation)
协作多智能体系统中个体故障不可避免，故障会导致两大挑战：(1) chaotic 输入——失效 agent 产生的无效信息扰乱网络的状态空间；(2) 样本不平衡——replay buffer 中故障前 transition 大量相似而故障后 transition 差异大，均匀采样降低训练效率。已有 robust MARL 关注动作偏离而非特定故障，传统容错方法不针对 MARL 算法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 建模为 Dec-POMDP 加入故障概率 p=F(s,t)；system-level fault 使 agent j 完全失效（不能观测/移动/通信）。故障随机分配到不同 agent、不同时刻。非对抗性、非策略性故障。
- **设定**: cooperative；CTDE（centralized critic, decentralized actor）；online

## 方法 (Method)
- 输入配置：critic 接收所有 agent 观测+动作；失效 agent 设 o_j=z·1（异常 flag）、a_j=0 使异常突出。actor 中对失效 agent 的观测 o_ij 按其阶段重要性配置（仍有意义则保留，否则设 z·1）。
- Critic 端 attention：通过 attention 权重将注意力从失效 agent 的观测移开，聚焦相关信息后解码出 Q 值；用 F_i 排除失效 agent 的 loss 项。
- Actor 端 attention：引入分类式 token e_i0，attention 动态决定是否关注失效 agent，再解码输出动作。
- 扩展 PER：为 critic 设单一优先队列、每个 actor 设独立队列，按各自 loss 的 rank-based 优先级采样，缓解样本不平衡；用 importance-sampling 权重保证无偏。
- 开源高度解耦的 FTMAL 平台（Fault Controller、Curriculum Controller 等），便于故障注入与对比研究。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（主要为架构与采样策略设计 + 实验验证）

## 实验 (Experiments)
- **环境/Benchmark**: 基于 MPE 改造的 4 个场景：Abandonment、Recovery、Navigation、Patrol（predator-prey 类，含通信中断、任务重分配、恢复、新任务）
- **Baselines**: MADDPG（自动识别）、MADDPG+MC（多 critic 手动识别）、M3DDPG（robust MARL）
- **评估指标**: task completion rate、episode reward；attention 分布可视化、采样 transition 分布分析

## 主要结果 (Key Results)
- 验证必要性：vanilla MADDPG 在 agent 2 于 t=5 失效时任务完成率从 0.872 降到 0.382。
- AACFT 在故障场景下显著优于所有 baseline；M3DDPG（robust MARL）在各场景均逊于 AACFT，表明提升鲁棒性不直接解决容错问题。
- attention 可视化显示故障后注意力从失效 agent 移开；ablation 证明 critic/actor attention 与 PER 各自有效。
- AACFT 能适应不同时刻发生的故障及无故障条件。

## 局限与未来工作 (Limitations & Future Work)
- Patrol 场景对 vanilla AACFT 与 baseline 都较难，未在该场景做完整对比。
- 偏实证，缺乏理论保证。
- 主要针对完全失效的 system-level fault，未涵盖部件级或对抗性故障。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"智能体失效/容错 (fault tolerance)"主题，强调与 robust MARL（动作偏离）的区别。方法线为 attention-based 架构改造 + 优先经验回放，并贡献了一个解耦的容错 MARL 实验平台，可作为容错应用与 benchmark 的参考。
