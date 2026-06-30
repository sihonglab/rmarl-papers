# 60. Robust Communicative Multi-Agent Reinforcement Learning with Active Defense (ADMAC)

## 元信息 (Metadata)
- **标题**: Robust Communicative Multi-Agent Reinforcement Learning with Active Defense
- **作者**: Lebin Yu, Yunbo Qiu, Quanming Yao, Yuan Shen, Xudong Zhang, Jian Wang
- **机构**: Department of Electronic Engineering, BNRist, Tsinghua University
- **发表**: AAAI 2024 (The Thirty-Eighth AAAI Conference on Artificial Intelligence)
- **链接/arXiv**: arXiv:2312.11545

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击（部分消息被任意扰动/伪造），含噪声与对抗攻击
- **方法范式**: 主动防御 (active defense)、可靠性估计 + 可分解消息聚合、监督学习分类、对抗训练对比
- **关键词**: communicative MARL, active defense, message reliability, robust communication, Dec-POMDP

## TL;DR（一句话总结）
提出主动防御框架 ADMAC，让每个智能体基于自身未被扰动的观测与历史隐状态评估收到消息的可靠性，并通过可分解的消息聚合策略网络按可靠性加权降低恶意消息影响，在三个通信关键任务、四类攻击下优于被动防御方法。

## 问题与动机 (Problem & Motivation)
通信能促进 MARL 协作，但真实无线信道易受噪声与对抗攻击。已有 robust communicative MARL 多采用被动防御（平等接收所有消息再做稳健决策），导致"garbage in, garbage out"，难以同时兼顾性能与鲁棒性。作者指出该问题区别于 robust RL 的关键特征：攻击者只能修改部分消息且扰动无界，而智能体自身观测/隐状态可帮助识别假消息。需主动利用这一特征。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 每条消息以概率 p 被攻击者替换为 ˆm，扰动幅度 ||ˆm−m|| 无界（强攻击）；智能体不知道哪些被扰动。攻击目标可为最小化最佳动作概率 (fA) 或最大化动作分布 KL 散度 (fB)。
- **设定**: cooperative；带通信的 Dec-POMDP；CTDE/decentralized 执行；online（含 broadcast 通信）

## 方法 (Method)
- **可分解消息聚合策略网 (DPN)**：将每条消息对决策的影响限制在"动作偏好向量"上。总偏好向量 = 基础偏好（来自隐状态）+ Σ_j w_i(m_j)·消息偏好（来自观测与消息），再经 Softmax 得动作分布；权重 w 控制单条消息影响（Proposition 1 给出单调性刻画）。
- **可靠性估计器 (RE)**：分类器 fR(h, o, m) 输出消息可靠度（0~1）作为权重 w。判据：若消息推荐了"无扰动下最可能选的最佳动作"则标为可靠，否则不可靠，转化为二分类监督学习。
- **三阶段训练**：(1) 常规通信 MARL 训练策略网；(2) 注入随机扰动与梯度对抗攻击生成带标签数据集；(3) 用交叉熵训练 RE。
- 框架与多种通信架构/训练算法兼容（本文用 broadcast + 改进 REINFORCE）。

## 理论贡献 (Theoretical Contributions)
Proposition 1：刻画消息权重对最终动作概率的单调影响（附录给出证明）。整体偏实证。

## 实验 (Experiments)
- **环境/Benchmark**: Food Collector（预定义通信）、Predator Prey（学习通信）、Treasure Hunt（学习通信），均 N=5
- **Baselines**: TARMAC（注意力，无防御）、Adversarial Training (AT)、Ablated Message Ensemble (AME)
- **评估指标**: 完成任务所需 timesteps（越低越好），不同攻击概率 p 下的性能；消融含 RE recall/precision、理想 RE (IRE)

## 主要结果 (Key Results)
- ADMAC 总体性能最优；在 Predator Prey 中无攻击基线甚至优于 TARMAC（得益于 DPN 结构）。
- AT 在强攻击下优于基线但无攻击时性能略降（鲁棒性-性能权衡）；AME 提供一定鲁棒性但因取消息共识而牺牲独占信息，基线很差。
- 消融：RE 提供显著鲁棒性（尤其对抗攻击）；DPN+IRE（理想分类器）效果最佳，验证标注方式有效；RE 分类性能（recall/precision 约 0.76~0.90）决定 DPN+RE 与 IRE 的差距。
- ADMAC 评测时所用四类攻击（Gaussian/Monte-Carlo/FGSM/PGD）与训练所用攻击分布不同，体现泛化性。

## 局限与未来工作 (Limitations & Future Work)
当消息携带智能体未知的独占信息时，判断可靠性困难，鲁棒性会下降。未来：聚合更广来源信息以更好评估消息；扩展到连续动作空间。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"通信攻击防御"线，代表从被动防御转向主动防御的范式创新；与 AME（认证鲁棒通信）、R-MACRL（消息纠正）、Mis-spoke/mis-lead 等通信鲁棒工作互补对照。
