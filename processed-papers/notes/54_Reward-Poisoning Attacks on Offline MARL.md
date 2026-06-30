# 54. Reward-Poisoning Attacks on Offline Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Reward-Poisoning Attacks on Offline Multi-Agent Reinforcement Learning
- **作者**: Young Wu, Jeremy McMahan, Xiaojin Zhu, Qiaomin Xie
- **机构**: University of Wisconsin-Madison
- **发表**: AAAI 2023（The Thirty-Seventh AAAI Conference on Artificial Intelligence）
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 奖励投毒（reward poisoning）/ 数据投毒攻击（offline 数据集篡改）
- **方法范式**: 攻击侧（adversarial attack）；博弈论均衡（Markov Perfect Dominant Strategy Equilibrium, MPDSE）；线性规划求解；攻击代价上下界分析
- **关键词**: reward poisoning, offline MARL, Markov Game, MPDSE, linear programming, attack cost bounds

## TL;DR（一句话总结）
研究 offline MARL 中的奖励投毒攻击：外部攻击者在智能体看到数据集前篡改奖励，以最小 Lp 修改代价把目标策略 π† 安装为 Markov Perfect Dominant Strategy Equilibrium（MPDSE），使理性智能体必然遵循，并给出可用线性规划高效求解的攻击框架及代价上下界。

## 问题与动机 (Problem & Motivation)
MARL 在自动驾驶、协作机器人、经济决策、游戏等领域成功，但对数据投毒脆弱：攻击者操纵反馈可使智能体收敛到错误均衡。已有奖励投毒研究多集中于 single-agent RL/bandit 或假设攻击者控制其中一个 learner；offline 多智能体场景（攻击者非参与者、可同时篡改所有 learner 的奖励，对应存在与各智能体利益不一致的中央控制器）尚缺研究。作者指出"把多智能体攻击拆成独立的单智能体攻击"必然次优，需要新方法，并为未来防御研究奠基。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者为 exogenous（非参与博弈的 learner），在智能体读取数据集前修改其中奖励向量，目标是用最小 Lp 范数代价把任意目标策略 π†（无需是原博弈均衡）安装为 ι-MPDSE。攻击对一大类 offline MARL learner（含 uncertainty-aware learner）有效；支持部分去中心化（智能体仅能看到自身奖励 ri,h）；仅假设 learner 不选被支配动作（最小理性假设）。
- **设定**: general-sum n-player Markov Game；competitive/mixed（一般和）；offline（固定批数据 D，不再采样）；部分去中心化数据访问

## 方法 (Method)
- 将攻击建模为：在不确定性约束（learner 对博弈的 MLE 及置信区间 ρ）下，找到最小代价的奖励修改使 π† 成为 ι-Dominant Strategy / MPDSE。
- 证明 MPDSE 一旦存在，任何理性智能体都会遵循，从而保证目标策略被采纳；并证明逐独立 single-agent 攻击必次优、联合攻击可显著更便宜。
- 给出线性规划（LP）来高效构造最优攻击；攻击对算法无关（适用一大类 learner）。
- 通过将 Markov Game 投毒代价归约到逐周期 Bandit Game 代价，建立代价分析；定义 ι-dominance gaps 刻画安装支配策略的难易。

## 理论贡献 (Theoretical Contributions)
- 证明 π† 可被安装为 ι-MPDSE，且攻击可由 LP 高效求解（理论保证理性智能体遵循）。
- Universal 代价上界：0 ≤ C*(I) ≤ NH|S|^n A^{n^2} b，并构造高代价实例证明近紧。
- Instance-dependent 上下界：将 Markov Game 代价用各周期 bandit 实例代价 C*(Ih) 之和加上与 learner 不确定性 ρ 相关的项约束（Theorem 9, Lemma 10, Theorem 12）；揭示 learner 不确定性越大、攻击代价越高，并使问题"退化"为独立周期博弈。
- 刻画哪些博弈结构对攻击者特别便宜或昂贵。

## 实验 (Experiments)
- **环境/Benchmark**: 偏理论分析（含 bandit / Markov Game 构造性实例说明代价上下界紧性）；未明确大规模实证 benchmark
- **Baselines**: 与"独立逐单智能体攻击"对比（理论上证明其次优）
- **评估指标**: 攻击代价（奖励修改的 Lp 范数）、是否成功安装 π† 为 MPDSE

## 主要结果 (Key Results)
- 联合多智能体奖励投毒可显著比独立的单智能体攻击更便宜，独立攻击必然次优。
- 攻击对包括 uncertainty-aware learner 在内的一大类 offline MARL 算法均有效，且可用 LP 高效求解。
- 给出近紧的攻击代价上下界，并将其与博弈/数据集结构（如转移不确定性、dominance gap）联系起来，识别易/难被攻击的博弈类别。

## 局限与未来工作 (Limitations & Future Work)
- 偏理论，缺乏大规模深度 MARL 实证验证；假设 learner 理性（不取被支配动作）。
- 通用代价界较松。
- 明确将防御（defense against offline MARL reward poisoning）列为后续方向——目前尚无针对该多智能体 offline 设定的防御方法。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"攻击侧 / 威胁建模"线，特别是奖励投毒（reward poisoning）与 offline MARL 安全；以博弈论均衡（MPDSE）刻画攻击有效性，可与 single-agent reward poisoning、observation poisoning（如 #103）、对手控制 learner 的攻击工作对照，并为 offline MARL 的认证/防御（如 COPA 类）提供动机。
