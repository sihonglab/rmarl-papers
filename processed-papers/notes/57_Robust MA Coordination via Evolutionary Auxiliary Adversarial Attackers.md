# 57. Robust Multi-Agent Coordination via Evolutionary Generation of Auxiliary Adversarial Attackers (ROMANCE)

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Coordination via Evolutionary Generation of Auxiliary Adversarial Attackers
- **作者**: Lei Yuan†, Ziqian Zhang†, Ke Xue, Hao Yin, Feng Chen, Cong Guan, Lihe Li, Chao Qian, Yang Yu（†共同一作；通讯 Yang Yu）
- **机构**: National Key Laboratory for Novel Software Technology, Nanjing University；Polixir Technologies
- **发表**: AAAI 2023（The Thirty-Seventh AAAI Conference on Artificial Intelligence）
- **链接/arXiv**: 代码 https://github.com/zzq-bot/ROMANCE

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 动作扰动 / 恶意动作攻击（policy perturbation：部分协作者被迫执行恶意动作，类似队友失效/被劫持）
- **方法范式**: 对抗训练 / minimax；进化生成多样化攻击者种群（population-based）；价值分解（QMIX）；质量-多样性优化（quality + behavior diversity，sparse action regularizer）
- **关键词**: cooperative MARL, robust coordination, adversarial training, attacker population, behavior diversity, LPA-Dec-POMDP

## TL;DR（一句话总结）
将"部分协作者意外遭受有限次恶意动作攻击"形式化为 LPA-Dec-POMDP，提出 ROMANCE：进化地维护一组兼具高攻击质量与行为多样性的辅助对抗攻击者，让 ego-system 在训练中对抗不断进化的多样强攻击者，从而对各种动作扰动获得高鲁棒性与泛化能力。

## 问题与动机 (Problem & Motivation)
CMARL 多关注非平稳性、credit assignment、可扩展性等协调难题，却忽视了部署时测试环境与训练环境不一致带来的 policy perturbation——尤其当队中部分协作者意外、不可预测地遭受有限次恶意动作攻击时，常规协作者仍需完成目标。该问题在 CMARL 中既无问题形式化也无高效算法。单智能体鲁棒 RL 多用 minimax 对抗训练，但多智能体更复杂且只学单一对手往往不足以泛化。本文针对"恶意动作攻击导致策略扰动"这一未被充分探索的方向。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: LPA-Dec-POMDP——团队中一部分 coordinator 可能被攻击者强制替换其动作（forced/malicious action），攻击总次数受固定预算限制（limited），攻击发生时机/对象不可预测；被攻击者成为对常规智能体而言"未知且可能破坏性"的队友。
- **设定**: cooperative（CMARL）；CTDE；online 对抗训练；基于 Dec-POMDP

## 方法 (Method)
- 维护一个攻击者集合（attacker set），通过进化生成与选择，保证攻击者既有高攻击质量（quality：最小化 ego-system 协调奖励），又有行为多样性（diversity），避免 ego-system 过拟合特定攻击者。
- 引入基于 sparse action 的新颖 diversity regularizer，促使不同攻击者产生不同行为。
- 限制攻击总次数为固定预算，防止攻击者过强使任务无法完成。
- ego-system 与从集合中选出的攻击者种群配对，交替训练；按定制的 quality score 与 diversity distance 迭代选择/更新攻击者种群，最终得到对多种类型/强度动作扰动鲁棒的协调策略。基于 QMIX 实现。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（贡献为 LPA-Dec-POMDP 问题形式化与算法设计，无收敛/复杂度理论证明）

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（StarCraft II 微操），多张地图：2s3z、3m、3s_vs_3z、8m、MMM、1c3s5z
- **Baselines**: vanilla QMIX、RANDOM（训练加随机攻击）、RARL（单一对抗攻击者）、RAP（population-based 对抗训练）
- **评估指标**: 测试胜率/回报（在 Natural 无攻击、Random Attack、EGA 强攻击等设定下，不同攻击次数）、攻击者攻击质量与多样性、可视化行为分析；5 个随机种子、95% 置信区间

## 主要结果 (Key Results)
- ROMANCE 在多张 SMAC 地图、不同攻击次数与攻击类型下，鲁棒性与泛化均优于或可比于 vanilla QMIX、RANDOM、RARL、RAP；RARL 因仅学单一攻击者表现较差。
- 进化框架确实能得到攻击质量高且行为多样的攻击者集合，避免被特定攻击者利用。
- 可视化（MMM 地图）显示：受攻击时 vanilla QMIX 仍按原协调模式忽视突发情况，而 ROMANCE 学会让幸存者撤退/重组、补位掩护被攻击队友，体现真正的鲁棒协调。
- 可集成进多种 CMARL 方法。

## 局限与未来工作 (Limitations & Future Work)
- 方法依赖启发式的 policy perturbation（动作攻击）函数；未来探索更合理高效的扰动方式（如 observation perturbation）。
- 自动搜索不同任务的最佳攻击预算（budget）。
- 面向 open-environment 设定设计高效鲁棒 MARL 算法。

## 与综述的关联 (Relevance to Survey)
属于 robust cooperative MARL 中"对抗训练 + 攻击者种群（population-based / 进化）应对动作扰动/队友被劫持"线，与 RARL、RAP（单智能体鲁棒 RL 的种群扩展）、M3DDPG、RADAR（adversarial value decomposition）、ad-hoc teamwork / zero-shot coordination 相关。其 quality-diversity 的攻击者生成思想与对抗课程/co-evolution（如 #55、#56）相呼应，是动作扰动鲁棒性方向的代表性 CTDE 工作。
