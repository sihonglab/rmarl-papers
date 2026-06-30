# 86. Robust Multi-Agent Bandits Over Undirected Graphs

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Bandits Over Undirected Graphs
- **作者**: Daniel Vial, Sanjay Shakkottai, R. Srikant
- **机构**: University of Texas at Austin; University of Illinois Urbana-Champaign
- **发表**: Proc. ACM Meas. Anal. Comput. Syst. (POMACS / SIGMETRICS) Vol.6 No.3, Article 53, 2022
- **链接/arXiv**: arXiv:2203.00076v2；DOI 10.1145/3570614

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 恶意智能体 (malicious agents)、Byzantine/容错（任意恶意的 arm 推荐，如评论 spam、服务器失效）
- **方法范式**: 多智能体多臂赌博机 (multi-armed bandits)、gossip/信息扩散、blocking（屏蔽可疑恶意者）、regret 分析理论
- **关键词**: multi-agent bandits, malicious agents, undirected graphs, blocking, gossip, regret bounds

## TL;DR（一句话总结）
研究网络（连通无向图）上含 m 个任意恶意智能体的 n-honest 协作多臂赌博机，证明面向完全图设计的现有 blocking 算法在 line graph 上会出现双指数级慢扩散（近线性 regret），并提出一种 refined blocking 规则，使每个 honest 智能体的 regret 为 O((d_mal(i)+K/n)log T/Δ)，即恶意者影响是完全局部的（只受其直接相连的恶意邻居数 d_mal(i) 影响）。

## 问题与动机 (Problem & Motivation)
多智能体赌博机中 n 个智能体在带宽受限网络上协作学习同一 K 臂赌博机以加速学习（应用：分布式计算、社交推荐、联邦学习）。已有完全合作算法可达 O((K/n)log T/Δ + poly) regret。但现实中部分智能体可能恶意（评论 spam = 坏 arm 推荐）或失效。已有工作 [56] 在完全图上提出 blocking 算法（honest 屏蔽推荐表现差的邻居），达 O((K/n+m)log T/Δ)，并证明 blocking 必要（一个恶意者即可抹掉对单智能体基线的改进）。本文目标：把该结果从完全图推广到仅连通无向图，这非平凡——[56] 依赖完全图假设（i★ 直接是所有 honest 的邻居），一般图上需要 gossip 扩散最佳 arm，而 blocking 会让 honest 互相误屏蔽，使扩散在动态图上进行，bandit 与通信随机性耦合，难以分析。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 图 G=([n+m],E)，[n] 为 honest 执行算法，m 个 malicious 可任意（adversarially）推荐 arm；假设 honest 子图 G_hon 连通（Assumption 1）。奖励 [0,1] 取值，最佳 arm 唯一（Assumption 2）。注意与"对抗腐蚀奖励"设定不同——这里是恶意 agent 给坏推荐。
- **设定**: 协作（honest 之间合作）+ 含对抗（malicious）；decentralized / 网络化 pairwise bit-limited 通信 (o(T) 次)；online，目标最小化每个 honest 的累积 regret

## 方法 (Method)
- 负面结果（揭示问题）：构造"坏实例" n=K、honest 子图为无向 line、所有 honest 共享一个恶意邻居，设计恶意策略使 honest 反复互相 block，最佳 arm 到达 line 末端智能体需双指数时间 (exp(exp(n/3)))，远差于经典 rumor 过程的指数级慢扩散。
- Refined blocking 规则（核心算法贡献）：agent i 屏蔽推荐了 arm k 的 i'，当且仅当 (1) arm k 在 UCB 下表现差（未被足够选择）且 (2) i 自己的 best-arm 估计近期未变更。第二条是与 [56] 的关键区别——agent 在自己的 best-arm 估计尚未稳定到真正好的 arm 之前，不应因看似差的推荐而 block，避免 honest 互相误屏蔽。
- Gossip 分析：证明用 refined 规则后 honest 最终停止互相 block，进而把 arm 扩散过程与一个不含 bandit/blocking 的可处理 noisy rumor 过程耦合，保证多项式时间扩散。
- 沿用 [18] 框架的 sticky set（每个 agent 负责探索 O(K/n) 个固定 arm）+ phase + 邻居推荐机制。

## 理论贡献 (Theoretical Contributions)
理论为主。(1) Theorem 1（负面）：现有 [56] 算法在 line graph 上 R_T^(n)=Ω(min{log T + exp(exp(n/3)), T/log^7 T})，即双指数时间内近线性 regret。(2) Theorem 2（正面）：refined 算法在任意连通无向图上 R_T^(i)=O((K/n+d_mal(i))log T/Δ + poly(K,n,m,1/Δ))，附加项为多项式而非双指数。(3) Corollary：d_mal(i)=0 的 honest 其 log T 项常数都与无恶意者的 [18] 匹配——恶意影响不超过一跳邻居（完全局部）。

## 实验 (Experiments)
- **环境/Benchmark**: 复现 [56] 实验并从完全图扩展到 G(n+m, p) 随机图（变化连接概率 p）
- **Baselines**: [18] 非 blocking 算法、[56] blocking 算法、单智能体基线
- **评估指标**: 累积 regret（均值与方差），随 p 变化

## 主要结果 (Key Results)
- 现有 [56] blocking 规则随 p 从 1 减小成为负担：p=1/2 时可能比 [18] 非 blocking 还差，p=1/4 时甚至比单智能体基线还差。
- 本文 refined 规则在所有测试 p 上 regret 都低于 [18]；除最大的 p 外平均优于 [56]，且在小 p 时方差显著更低。
- 关键定性结论：可同时做到 (1) gossip 扩散有用信息 (2) 识别并 block 恶意者，且恶意危害局部化于一跳邻居；但 blocking 须谨慎，完全图算法在一般图上可双指数慢扩散。

## 局限与未来工作 (Limitations & Future Work)
- 假设 honest 子图连通、最佳 arm 唯一、奖励有界；恶意模型为推荐型而非奖励腐蚀型。
- 附加 poly 项依赖多参数；规则需 UCB 设定。
- 文中未明确列出未来工作章节细节（未明确）；自然方向包括更弱图假设、自适应 blocking 阈值等。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"网络化/去中心化协作下对恶意/Byzantine 智能体的鲁棒性"这条偏理论的线，与分布式学习的容错、Byzantine-resilient 协作相关。区别于深度 MARL 实证工作，本文给出严谨的 regret 上下界，揭示了网络拓扑（完全图 vs 一般连通图）对鲁棒协作算法的关键影响，是综述中 bandit/理论分支与"通信/拓扑下的鲁棒性"主题的代表。
