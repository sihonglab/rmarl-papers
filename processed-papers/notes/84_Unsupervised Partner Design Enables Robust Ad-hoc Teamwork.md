# 84. Unsupervised Partner Design Enables Robust Ad-hoc Teamwork

## 元信息 (Metadata)
- **标题**: Unsupervised Partner Design Enables Robust Ad-hoc Teamwork
- **作者**: Constantin Ruhdorfer, Matteo Bortoletto, Victor Oei, Anna Penzkofer, Andreas Bulling
- **机构**: Collaborative Artificial Intelligence, University of Stuttgart, Germany
- **发表**: ICML 2026 (PMLR 306)
- **链接/arXiv**: arXiv:2508.06336v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 未知合作伙伴 (partner uncertainty) / ad-hoc teamwork 中的分布偏移，以及程序化生成的未知环境 (level) 不确定性
- **方法范式**: 课程学习 (curriculum learning)、Unsupervised Environment Design (UED) 思想迁移到 partner 空间、learnability 驱动的自适应选择、population-free 自博弈训练
- **关键词**: ad-hoc teamwork, unsupervised partner design, learnability, zero-shot coordination, curriculum learning

## TL;DR（一句话总结）
提出 Unsupervised Partner Design (UPD)，一种无需预训练伙伴种群、无需手调混合系数的 population-free MARL 方法，通过在线生成伙伴并基于 learnability（回报方差）自适应筛选来训练对未知伙伴鲁棒的 ad-hoc teamwork ego agent，并可扩展到 partner-环境联合课程 (JUPD)。

## 问题与动机 (Problem & Motivation)
鲁棒地与未知伙伴（含人类）协作即 ad-hoc teamwork (AHT)，是合作型 AI 的核心需求。已有方法依赖大规模多样化伙伴种群 (FCP, MEP) 或专家知识，训练成本随任务/伙伴多样性规模化而高 (O(NC) 量级)。population-free 的 E3T 用 ego 与随机策略的混合在线生成伙伴，但需对每个任务/评估场景手调固定混合系数 ε，限制了可扩展性与适应性。同时 UED 表明对环境参数的自适应课程能显著提升泛化，但现有 UED 只针对环境参数，不把伙伴策略纳入课程空间。本文要回答：能否像设计环境那样廉价、自适应地生成训练伙伴；该机制能否自然扩展到 partner-环境联合课程。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 评估伙伴集合 Πeval 未知（含人类及 BRDiv 等不兼容策略）；目标是 max E_{πp∼Πeval}[J(πego,πp)]。在 under-specified game 中环境参数 θ（墙体/物体/智能体位置）也不确定，每个 θeval 关联各自的 Πeval。
- **设定**: cooperative（两智能体共享奖励的 stochastic game）；自博弈训练 + ego/partner 视角，online；可处理 fixed 环境与 procedurally-generated 环境

## 方法 (Method)
- 固定一个伙伴策略 πp 即把多智能体博弈"诱导"为 ego 的单智能体训练环境 G_{πp,θ}；从伙伴生成器 Sp 采样伙伴即定义诱导训练环境的分布。
- learnability 评分：用回报方差 ℓ_var = Var_τ[R(τ)] 衡量伙伴的学习潜力（方差高=中等难度=既非总成功也非总失败），并引用 Foster et al. 的结论说明对 PPO 类方法期望改进正比于学习信号方差；跨 level 时用 CV² 归一化 (ℓ_CV2 = Var/(E+δ)²)。
- 在线伙伴生成器 Sp (Alg.2)：扩展 E3T，混合系数 ε∼U(0,1)（覆盖全竞争力范围），并以概率 pbias 从 Dirichlet(α·1) 采样持久化 bias mask 引入系统性动作偏好 (πp=ε·πr,m+(1−ε)·πego)。
- UPD 主循环 (Alg.1)：周期性 (R) 采样大量候选伙伴，N 次 rollout 估计 ℓ，取 top-|B| 入缓冲 B；按 ℓ 与 SFL 比例 ρ 采样 (πp,θ) 用 PPO 更新 ego。单阶段训练。
- 联合扩展 JUPD：同时对 (πp,θ)∼Sp×Θ 采样评分，实现 partner+level 联合课程。理论分析（4.4）说明 learnability 偏好打破当前 convention 的伙伴，从而隐式实现 convention breaking。

## 理论贡献 (Theoretical Contributions)
偏实证。提供概念性论证：基于 Foster et al. (2026) 的结果，将 learnability（回报方差）与 PPO 类方法的期望一步策略改进联系起来；并在 2×2 协调矩阵博弈上分析 UPD 如何偏向选择最模糊 (p=0.5) 伙伴以打破自博弈 convention（无形式化收敛/样本复杂度定理）。

## 实验 (Experiments)
- **环境/Benchmark**: Level-Based Foraging (LBF)、Overcooked-AI（5 个标准 layout: CRoom, AA, CR, CC, FC）、Overcooked Generalisation Challenge (OGC, 5×5 程序化生成)；共训练 282 个策略
- **Baselines**: SP (IPPO 自博弈)、FCP、MEP（种群 48）、E3T；消融 UPD w/o bias、UPD w/o ℓ；JUPD 对比 DR-DR、CEC、SFLE3T；含 12 人双盲人机用户研究
- **评估指标**: 与多样化未见伙伴/人类的平均 episodic return；人类主观问卷（frustrating↓, adaptive↑, human-like↑, coordinated↑）

## 主要结果 (Key Results)
- LBF 中 UPD 优于所有手调 ε 的 E3T；Overcooked-AI 平均 return 94.4，较 E3T 提升 +18.0%，整体优于 population-based (FCP 70.0, MEP 75.3) 与 population-free (E3T 78.8)，且全部 layout 用同一组超参。
- 消融显示大规模伙伴生成+biasing 贡献主要增益，learnability 提供额外提升（尤其 AA layout）。
- 人机研究中 UPD 平均 return 更高，且在 adaptive / human-like / 协作 / 不令人沮丧 等主观项上显著优于基线 (Holm-Bonferroni 校正 p<0.05)。
- JUPD 在 OGC 5×5 上平均 58.9，优于 DR-DR (49.9)、SFLE3T (44.0)、CEC (23.9)。
- 观察到 emergent convention breaking（伙伴动作偏好随训练翻转）与 learnability 偏好中等难度伙伴的训练动态。

## 局限与未来工作 (Limitations & Future Work)
- 将计算从种群预训练转移到大规模在线伙伴评估，在高度向量化模拟器 (JAX) 中划算，但在交互昂贵的场景中可能不利。
- 当前伙伴空间由特定随机生成器实例化；可探索更丰富的伙伴空间（种群、latent partner space）与其他 UED 方法。
- 不在每个 layout 都占优 (CRoom 上他法更好)，定位为"单一 population-free 配置即可保持竞争力"而非全面最优。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对未知合作伙伴的鲁棒性 / ad-hoc teamwork / zero-shot coordination"这一线，与基于种群多样性、对抗训练、open-ended/curriculum learning 的方法相关。其核心贡献是把 UED 的 learnability 课程思想从环境参数迁移到伙伴策略，连接了 AHT 与 unsupervised environment design 两条研究线，是 robust cooperation 在合作型 MARL 下的代表性方法。
