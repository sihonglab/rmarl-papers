# 176. Less Is More: Robust Robot Learning via Partially Observable Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Less Is More: Robust Robot Learning via Partially Observable Multi-Agent Reinforcement Learning
- **作者**: Wenshuai Zhao, Eetu-Aleksi Rantala, Sahar Salimpour, Joni Pajarinen, Jorge Peña-Queralta（前两位同等贡献）
- **机构**: Aalto University（Finland）；University of Turku, TIERS Lab（Finland）；ETH Zurich（Institute of Robotics and Intelligent Systems）
- **发表**: arXiv 2023（arXiv:2309.14792，v2 2025-02-28）
- **链接/arXiv**: arXiv:2309.14792

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 智能体/组件失效（agent/component failure，如机械臂被禁用）与观测扰动；通过去中心化局部观测获得鲁棒性
- **方法范式**: SARL 与 MARL 的等价性分析、partially observable MARL（Dec-POMDP）、policy-gradient、去中心化控制
- **关键词**: partial observability, Dec-POMDP, decentralized control, robustness to failure, SARL vs MARL equivalence, mobile manipulation

## TL;DR（一句话总结）
系统比较在同一机器人任务上 SARL 与 MARL 的鲁棒性与性能：先解析证明在全状态观测下二者的独立高斯策略等价，再实证表明在本质单智能体任务中可用多个仅有局部观测的智能体来控制机器人——"少看一点"反而带来对扰动与组件失效的额外鲁棒性，在真实移动操作机器人上当机械臂被禁用时，partial-observation MARL 优于 SARL 与 global MARL。

## 问题与动机 (Problem & Motivation)
许多机器人任务既可用 SARL 中心化控制，也可拆成 MARL 去中心化控制（如把腿式机器人各关节分给不同智能体），但两种范式的关系、以及为新任务该如何选择，缺乏系统研究。已有去中心化控制研究多在"弥补局部信息的不足"，而非主动利用这种结构。本文从控制论与 RL 双视角探究：当智能体不依赖全状态信息时，去中心化 MARL 能否在组件失效时提供更强鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 系统部分失效（如移动操作机器人的机械臂被禁用 disabled）以及对状态的扰动；鲁棒性来源是智能体不依赖全状态、仅用局部观测
- **设定**: cooperative；Dec-MDP / Dec-POMDP；decentralized 执行；online 学习；机器人控制（含真实机器人）

## 方法 (Method)
- 解析证明：在全状态（full-state）观测下，由 policy-gradient 优化的独立高斯策略，SARL 与 MARL 等价
- 实证：在若干本质上"单智能体"的任务中，把控制拆给多个仅有 partial observation 的智能体，性能可逼近全观测情形（"less is more"）
- 用比例-积分（PI）控制的示例，解析说明含全局信息的中心化控制器可能引入的不稳定性
- 在真实移动操作机器人上对比三种控制器：SARL、global MARL、partial MARL（本文方法），考察组件失效下的鲁棒性

## 理论贡献 (Theoretical Contributions)
给出 SARL 与 MARL 在全状态观测下、由 policy-gradient 优化的独立高斯策略之等价性证明；并用 PI 控制示例解析地说明中心化全局信息控制器可能导致不稳定。属"分析 + 实证"型贡献，非样本复杂度类。

## 实验 (Experiments)
- **环境/Benchmark**: 一个示意性的去中心化控制 toy 任务、若干 toy MARL 任务，以及真实世界的移动操作（mobile manipulation）机器人任务（含机械臂被禁用的失效场景）
- **Baselines**: SARL（中心化全观测）、global MARL（全观测多智能体）；与 partial MARL（本文）对比
- **评估指标**: 名义（nominal）行为下的任务成功/性能，以及组件失效/扰动下的成功率与鲁棒性

## 主要结果 (Key Results)
- 全观测下 SARL 与 MARL 等价（解析 + toy 实验印证）；局部观测的 MARL 在某些任务上可达到接近全观测的性能
- 真实机器人实验中，名义条件下三种方法都能工作，但当机械臂被禁用时只有 partial MARL 成功，SARL 与 global MARL 均失败
- 不依赖全状态信息的去中心化多智能体结构能对组件失效与扰动提供额外鲁棒性（"Less is more"）

## 局限与未来工作 (Limitations & Future Work)
结论主要针对可自然拆分为局部观测的特定机器人任务，普适性需进一步验证；如何为一般任务划分智能体/观测仍是开放问题；实验任务与失效类型有限；缺乏对更广泛扰动谱与大规模系统的系统评估。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[智能体失效/容错]] 与 [[partial observability]] 线的工作，提供了一个不同于对抗训练的视角——通过去中心化与局部观测（Dec-POMDP）的结构性选择来获得对组件失效的鲁棒性，并澄清 [[SARL vs MARL]] 在全观测下的等价关系；与机器人/具身控制、[[decentralized control]] 主题相关。
