# 186. Adversarial Policy Gradient for Alternating Markov Games

## 元信息 (Metadata)
- **标题**: Adversarial Policy Gradient for Alternating Markov Games
- **作者**: Chao Gao, Martin Müller, Ryan Hayward
- **机构**: University of Alberta
- **发表**: ICLR 2018 Workshop track
- **链接/arXiv**: 未明确（ICLR 2018 Workshop）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体（two-player zero-sum 中的最坏情况对手），self-play 中对对手过优估计
- **方法范式**: policy gradient、generalized policy iteration、minimax/adversarial critic、self-play
- **关键词**: Alternating Markov Game, adversarial policy gradient, zero-sum self-play, REINFORCE, Hex

## TL;DR（一句话总结）
针对两人轮流零和博弈（Alternating Markov Game, AMG）与单智能体 MDP 在 Bellman 方程上的本质差异，提出 adversarial policy gradient——在估计 critic 时取 minimum（最坏对手）而非 mean，从而得到比 self-play REINFORCE 更强的纯神经网络策略，在 Hex 上结合搜索持续击败前 SOTA MoHex 2.0。

## 问题与动机 (Problem & Motivation)
AlphaGo 等用 self-play REINFORCE 把零和棋类当作普通 MDP 处理，简单地对对手回合取反奖励。但 AMG 是 Stochastic Game 的特化、MDP 的泛化，含两个目标对立的玩家，其 Bellman 方程与 MDP 不同，导致 policy iteration 算法也不同。作者认为直接套用标准 RL（取均值 critic）忽视了博弈的对抗结构，未能利用"对手是 min player"这一事实。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手在轮到其行动时采取最优 counter-policy（最小化共享奖励）；通过 minimax 形式的 Bellman 方程刻画最坏对手
- **设定**: competitive（two-player zero-sum, alternating turns）；model-free RL；self-play 训练

## 方法 (Method)
- 从 AMG 的 Bellman 方程出发，区分 max player π1 与 min player π2，推导出与 MDP 不同的 policy iteration
- 把 critic 的目标从估计 self-play 回报的 mean 改为估计 minimum（最坏情况对手回报），即 adversarial policy gradient 目标
- 由此改造 Monte Carlo policy gradient（REINFORCE 变体），得到针对 AMG 的对抗式 policy gradient 方法
- 提出 board-size independent 的神经网络结构，使单一模型可应用于多种棋盘尺寸的 Hex

## 理论贡献 (Theoretical Contributions)
偏算法/概念性：阐明 AMG 与 MDP 在 Bellman 方程与 policy iteration 上的差异，并据此构造 adversarial policy gradient 目标；无收敛率/样本复杂度型定理。

## 实验 (Experiments)
- **环境/Benchmark**: 围棋类对抗棋 Hex（9×9 至 13×13 多种棋盘尺寸）
- **Baselines**: self-play REINFORCE 变体；前 SOTA 计算机 Hex 程序 MoHex 2.0
- **评估指标**: 纯神经网络策略对弈胜率、结合搜索后的对局胜率

## 主要结果 (Key Results)
- 取 minimum 而非 mean 的 critic 估计能学到更强的纯神经网络 Hex 策略，优于 REINFORCE 变体
- 单一 board-size independent 模型结合搜索后，在 9×9 到 13×13 各尺寸上持续击败 MoHex 2.0

## 局限与未来工作 (Limitations & Future Work)
方法限定于两人轮流零和博弈，难以直接推广到一般 Markov game 或合作/混合场景；实验仅在 Hex 单一领域；属 workshop 短文，理论分析有限。

## 与综述的关联 (Relevance to Survey)
属"对抗智能体/最坏情况对手"线的早期 policy gradient 工作，把 minimax 思想注入 critic 估计，是 [[adversarial policy gradient]] 与 [[minimax MARL]] 主题在零和博弈下的代表案例，可与 §对抗训练、§博弈论均衡（Nash/zero-sum）的方法线对照。
