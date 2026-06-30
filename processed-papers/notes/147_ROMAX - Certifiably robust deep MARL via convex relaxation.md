# 147. ROMAX: Certifiably Robust Deep Multiagent Reinforcement Learning via Convex Relaxation

## 元信息 (Metadata)
- **标题**: ROMAX: Certifiably Robust Deep Multiagent Reinforcement Learning via Convex Relaxation
- **作者**: Chuangchuang Sun, Dong-Ki Kim, Jonathan P. How
- **机构**: MIT, Laboratory for Information & Decision Systems (LIDS)
- **发表**: ICRA 2022；arXiv:2109.06795
- **链接/arXiv**: arXiv:2109.06795；doi:10.1109/ICRA46639.2022.9812321

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗/最坏情况的其他智能体策略（cyber-physical attacks：通信劫持、观测扰动），以及 MARL 非平稳导致的对未见对手的脆弱性
- **方法范式**: minimax MARL、神经网络凸松弛 (convex relaxation)、认证鲁棒 (certified bound)
- **关键词**: minimax MARL, convex relaxation, certified robustness, worst-case opponent, mixed cooperative-competitive

## TL;DR（一句话总结）
针对 MARL 中对其他智能体策略过拟合、面对新策略/攻击崩溃的问题，提出 ROMAX——用神经网络凸松弛近似求解 minimax 内层"最坏情况其他智能体动作"，既能探索近似全局最坏情形又给出认证鲁棒界，在混合合作-竞争任务上显著超越 M3DDPG 等基线。

## 问题与动机 (Problem & Motivation)
MARL 中智能体同时学习造成环境非平稳，CTDE 等方法虽缓解非平稳但策略普遍过拟合当前其他智能体行为，遇到训练中未见过的新策略表现骤降；竞争场景下对手还可主动施加 cyber-physical 攻击充分利用脆弱策略。已有 minimax 方法（如 M3DDPG）仅用单步梯度近似最坏对手，只能探索局部最坏，仍不稳定。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 其他智能体可采取最坏情况（对抗）策略更新；用 minimax 形式刻画——本智能体在其他智能体最坏动作下最大化收益
- **设定**: mixed cooperative-competitive；深度策略 (DNN) 参数化；CTDE 式训练、去中心化执行

## 方法 (Method)
- 将鲁棒策略学习写成 nonconvex-nonconcave minimax 优化（内层求其他智能体最坏动作），该问题一般不可解
- 假设各智能体策略由 DNN 参数化，对 DNN 施加 **convex relaxation**，把内层最小化松弛为可高效求解的凸问题，近似得到全局最坏情况动作
- 凸松弛同时给出原问题的 **guaranteed bound**，从而获得 certified robustness
- 用得到的最坏情况估计进行鲁棒策略更新（minimax actor-critic）

## 理论贡献 (Theoretical Contributions)
凸松弛提供原 minimax 目标的可证明 bound（certified robustness），将不可解的 nonconvex-nonconcave 内层问题转化为有保证的凸近似；偏算法+认证，非样本复杂度型理论。

## 实验 (Experiments)
- **环境/Benchmark**: 多个 mixed cooperative-competitive 任务（MPE 类多智能体粒子环境）
- **Baselines**: M3DDPG（单步梯度 minimax）、MADDPG 等
- **评估指标**: 与不同/未见对手交互时的回报、鲁棒性

## 主要结果 (Key Results)
- ROMAX 在多个任务上显著优于此前 SOTA（尤其 M3DDPG），凸显"计算近似全局最坏情形"对提升 MARL 鲁棒性的必要性
- 凸松弛带来的认证 bound 使最坏情况探索更稳定、不再局限于局部最坏

## 局限与未来工作 (Limitations & Future Work)
凸松弛对深层/大型网络的紧致性与可扩展性受限；实验局限于中小规模 MPE 类任务；认证 bound 的紧度与计算开销之间存在权衡。

## 与综述的关联 (Relevance to Survey)
属"对抗智能体/最坏情况对手"线的代表性早期工作，是把单智能体 certified robustness（凸松弛/区间界）迁移到 MARL minimax 框架的桥梁；被本语料大量引用（被引 10×），与 §1（minimax/M3DDPG）与 §4（certified）均有交叉。
