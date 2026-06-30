# 68. Robust Multi-agent Communication Based on Decentralization-Oriented Adversarial Training (DMAC)

## 元信息 (Metadata)
- **标题**: Robust Multi-agent Communication Based on Decentralization-Oriented Adversarial Training
- **作者**: Xuyan Ma, Yawen Wang, Junjie Wang, Xiaofei Xie, Boyu Wu, Shoubin Li, Fanjiang Xu, Qing Wang
- **机构**: State Key Laboratory of Intelligent Game / Institute of Software, Chinese Academy of Sciences (ISCAS); University of Chinese Academy of Sciences; Singapore Management University
- **发表**: IJCAI 2025（arXiv:2504.21278v1，2025年4月；网址含 IJCAI2025）
- **链接/arXiv**: arXiv:2504.21278

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击 / 关键通信信道失效与遮蔽（critical channel masking）、消息扰动；针对"非均衡通信结构"的脆弱性
- **方法范式**: 对抗训练（adversarial training）、对抗者建模为 MARL（value-based CTDE, IGM/QMIX 风格）、去中心化理论、关键信道识别、GNN 特征聚合
- **关键词**: communicative MARL, communication robustness, adversarial training, decentralization, critical channel masking

## TL;DR（一句话总结）
DMAC 借鉴社会学去中心化理论，训练一个能动态识别并遮蔽关键通信信道的对抗者，用其生成的对抗样本对已有通信策略做对抗训练，迫使通信从集中式转向去中心化结构，从而提升通信策略对各类攻击的鲁棒性。

## 问题与动机 (Problem & Motivation)
现有可学习通信策略（如 T2MAC、I2C）训练易陷入局部最优，导致通信集中在少数信道上（统计显示 T2MAC 中 30% 信道承担近 70% 通信频率），形成不均衡结构。按去中心化理论，过度集中的网络在关键节点失效时易整体崩溃。已有通信防御方法（AME、R-MACRL、GP 过滤）多是对异常消息额外处理而不真正调整通信策略本身。本文目标是让通信策略本身变得去中心化、从而抗攻击。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者遮蔽（mask/关闭）智能体间的关键通信信道（ac_{i,j}∈{0,1}），破坏消息交换。评估时考虑两类攻击：(1) Learned adaptive attack（白盒、用 RL 学最强对抗通信以最小化受害者奖励）；(2) Heuristic attack（在合法范围内随机生成消息扰动）。
- **设定**: cooperative；CTDE（目标策略 π 固定，训练对抗者与重训通信策略 CP）；online。DMAC 为通用训练方法，可与任意可学习通信策略融合。

## 方法 (Method)
- **整体框架**: 已有通信策略 CP 输出良性通信决策；构建对抗者 DMAC_Adv 输出遮蔽决策扰动信道；用对抗样本对 CP 做对抗训练，使其减少对关键信道依赖、转向去中心化。
- **对抗者建模**: 将"识别关键信道"建模为 MARL（masking agents），每个 masking agent 决定是否遮蔽信道 (i,j)，建模为 Dec-POMDP，动作空间 {0,1}，masking agent 数 = n(n-1)/2。
- **双目标奖励**: 对抗者奖励 ˆr 与"目标系统奖励 r"和"遮蔽信道数 rm"成反比（obj = max 1/(Σγ^t(w1·R + w2·Rm)+ξ)），既最大化降低目标系统性能又限制遮蔽数量，避免无差别遮蔽。
- **特征提取**: 将 agent 团队建模为无向图（顶点=agent 属性如位置/速度/血量，边权=智能体间距离），用基于边权的聚合得到 embedding e_v，与观测拼接 h_i = o_i ⊕ e_i 作为遮蔽决策输入。
- **训练**: value-based CTDE，遵循 IGM 原则，critic 网络权重非负（QMIX 风格，可替换为 VDN/QPLEX/QTRAN），用 TD loss 迭代优化 πc 与 critic；再用对抗样本重训 CP。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（采用 IGM 原则与非负权重保证个体-全局最大一致性，但无新收敛/认证理论分析）。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC(1c3s5z, 9 agents)、Cooperative Navigation (CN, 7 agents)、Predator-Prey (PP, 8 agents)、Traffic Junction (TJ, 10 agents)
- **Baselines**: AME（认证防御, 消息集成）、R-MACRL（异常检测+消息重构）；目标通信策略为 T2MAC 与 I2C
- **评估指标**: win rate（任务完成率），分别在 learned adaptive attack 与 heuristic attack 下；正常条件下性能；通信频率热力图与标准差（去中心化程度）

## 主要结果 (Key Results)
- 鲁棒性：面对 learned adaptive attack，DMAC 较 baselines 提升 T2MAC 47.9%-81.9%、I2C 54.4%-99.0%；面对 heuristic attack 提升 T2MAC 37.9%-90.5%、I2C 38.3%-117.7%。例如 SC 中 T2MAC 受攻击 win rate 从 27.8% 提升到 60.4%。
- 正常性能：DMAC 不仅未损害、反而小幅提升 clean win rate（如 SC 中 T2MAC 81.2%→83.7%），优于 AME/R-MACRL（R-MACRL 因误改正确消息略降）。
- 去中心化：通信频率标准差显著下降（如 SC 中 T2MAC SD 14.0→9.0），通信结构更均衡，且通信成本几乎不增甚至下降。

## 局限与未来工作 (Limitations & Future Work)
论文未设独立局限章节。可推断局限：对抗者建模随 agent 数呈 O(n²) masking agents，扩展性受限；依赖能获取 agent 状态/距离构图的环境；仅在小规模任务（≤10 agents）验证；未给出理论鲁棒保证。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"通信鲁棒性 + 对抗训练"主题线，独特之处在于从"通信结构（拓扑集中度）"而非"单条消息内容"角度提升鲁棒性，将社会学去中心化理论引入 CMARL。可与 ADMAC(#60)、Certified Communication(#61/#62)、Mis-spoke/R-MACRL(#63)、AME 等通信防御工作对照——后者多为消息级被动/认证防御，本文为结构级主动重训。
