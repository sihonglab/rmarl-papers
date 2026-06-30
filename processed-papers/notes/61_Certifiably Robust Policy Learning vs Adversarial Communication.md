# 61. Certifiably Robust Policy Learning against Adversarial Multi-Agent Communication

## 元信息 (Metadata)
- **标题**: Certifiably Robust Policy Learning against Adversarial Multi-Agent Communication
- **作者**: Yanchao Sun, Ruijie Zheng, Parisa Hassanzadeh, Yongyuan Liang, Soheil Feizi, Sumitra Ganesh, Furong Huang
- **机构**: University of Maryland, College Park；JPMorgan AI Research；Shanghai AI Lab
- **发表**: ICLR 2023
- **链接/arXiv**: https://github.com/umd-huang-lab/cmarl_ame

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击（最多 C 条消息被任意/无界扰动，含多攻击者协同），属 ℓ0 型威胁
- **方法范式**: 认证鲁棒 (certifiable defense)、随机消融 + 集成 (ablation & ensemble)、多数投票/中位数共识
- **关键词**: certifiable robustness, communicative MARL, message ablation, ensemble, adversarial communication

## TL;DR（一句话总结）
提出 Ablated Message Ensemble (AME)：通过对收到的多条消息随机消融成子集、由单一策略在多个子集上投票/取中位数聚合决策，在最多 C < (N-1)/2 条消息被任意扰动时仍可证明鲁棒，且不依赖攻击算法。

## 问题与动机 (Problem & Motivation)
通信对协作 MARL 至关重要，但部署时消息可能被噪声或恶意攻击者篡改，依赖通信的策略会被误导酿成灾难。通信攻击的三大挑战：(I) 攻击可隐蔽且强，伪造消息可远离原值但语义合理，常用 ℓp 威胁模型覆盖不到；(II) 攻击者可自适应针对受害者大幅降低回报；(III) 可能有多个攻击者协同。已有经验防御无理论保证，尤其在自适应攻击下不可靠。需要带证书的防御。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 测试时受害者从 N-1 条消息中最多 C 条被任意扰动（无界、任意算法），受害者不知哪些被改。假设 3.1：C < (N-1)/2（攻击者控制不到半数消息）。不假设攻击算法，仅需 C 的上界。
- **设定**: cooperative；Dec-POMDP with communication；CTDE 训练 / decentralized 执行；防御独立于通信策略 ξ 与动作策略 π

## 方法 (Method)
- **k-消融消息样本**：从 N-1 条消息中随机取 k 条组成 k-sample；训练阶段策略 ˆπ 仅以一个随机 k-sample（加自身历史）为输入学习动作（任意策略优化算法可用，单一网络）。
- **消息集成策略 ˜π（防御阶段）**：枚举所有 C(N-1, k) 个 k-sample，离散动作取多数投票、连续动作取逐坐标中位数，输出"良性共识"动作。
- **核心直觉**：良性消息含冗余/共识信息；只要多数智能体良性且一致，集成结果即为良性，对任意强扰动免疫。
- **可扩展变体 D-ensemble**：N 大时只随机抽 D 个 k-sample 聚合，以高概率保证（概率随 D 增大）。

## 理论贡献 (Theoretical Contributions)
- 离散动作：Condition 4.4（良性投票占优）下 Theorem 4.5 给出动作证书——集成动作必属良性动作集 Abenign；并导出奖励证书（攻击不会使回报低于基策略在随机良性子集下的最差自然回报）。
- 连续动作：Condition 4.6 下 Theorem 4.7 保证动作落入 Range(Abenign)，并给出奖励差界 (ϵR+γVmax·ϵP)/(1-γ)。
- 消融尺寸 k 刻画鲁棒性-性能权衡（小 k 容忍更大 C）；D-ensemble 给出高概率保证公式。是 MARL 中首个针对通信攻击的认证防御。

## 实验 (Experiments)
- **环境/Benchmark**: FoodCollector（离散/连续动作，预定义通信）、InventoryManager（连续，预定义）、MARL-MNIST（离散，学习通信）、Traffic Junction（离散，学习通信）
- **Baselines**: Vanilla（无防御）、Adversarial Training (AT)
- **评估指标**: 受害者局部奖励/精度，在无攻击与不同 C 下；攻击含 Heuristic（随机/Perm/Swap/Flip）与 Learned adaptive（RL 白盒最坏攻击）

## 主要结果 (Key Results)
- AME 在所有任务、自适应与非自适应攻击下均优于 Vanilla 与 AT，并随 C 变化保持鲁棒。
- 取 k=2（N=9/10 时对应 C=2 的最大解）时，C=1/2 下回报与无攻击相近，符合理论；即使 C=3 超出保证范围仍优于基线。
- Vanilla 与 AT 在强自适应攻击下回报骤降，甚至不如无通信智能体——通信是双刃剑；AT 对任意消息扰动无效。
- 消融：k 越大自然性能越高但鲁棒性越差；D 越小鲁棒性下降但仍优于基线，验证集成的作用。

## 局限与未来工作 (Limitations & Future Work)
依赖若干条件（虽可量化检查）；未来放松条件或直接学习满足条件的通信策略。AME 依赖通信信息冗余/共识，可通过学习通信策略来构造。

## 与综述的关联 (Relevance to Survey)
robust MARL 中"通信攻击 + 认证鲁棒"线的代表作，首次把随机消融/集成的认证思想（类比 ℓ0 randomized ablation）引入序贯决策的多智能体通信，是后续 ADMAC 等通信鲁棒方法的重要对照基线。
