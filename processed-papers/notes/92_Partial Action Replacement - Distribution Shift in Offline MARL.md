# 92. Partial Action Replacement: Tackling Distribution Shift in Offline MARL

## 元信息 (Metadata)
- **标题**: Partial Action Replacement: Tackling Distribution Shift in Offline MARL
- **作者**: Yue Jin, Giovanni Montana
- **机构**: University of Warwick (WMG, Dept. of Statistics); The Alan Turing Institute, UK
- **发表**: AAAI 2026（版权页标注 Copyright © 2026, AAAI；arXiv preprint）
- **链接/arXiv**: arXiv:2511.07629v1 [cs.LG], 10 Nov 2025

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 分布偏移 (distribution shift) / OOD joint actions，offline MARL 中的外推误差导致的价值高估
- **方法范式**: 保守价值正则化 (CQL 系)、partial action replacement、不确定性加权 (Q-ensemble)、价值误差界理论分析
- **关键词**: offline MARL, distribution shift, conservative Q-learning, factorized behavior policy, uncertainty-weighted backup

## TL;DR（一句话总结）
提出 partial action replacement (PAR) 原理——只替换部分智能体的动作而其余保持数据集动作，并据此设计 SPaCQL，通过 Q-ensemble 不确定性自适应加权不同偏离规模的 Bellman backup，理论证明在 factorized behavior policy 下分布偏移随偏离智能体数线性（而非指数级）增长。

## 问题与动机 (Problem & Motivation)
Offline MARL 面临联合动作空间随智能体数指数增长带来的“维数灾难”：任何有限数据集对联合动作覆盖稀疏，标准 Q-learning 对 OOD joint actions 给出任意高的错误估值，导致策略发散。已有 offline RL/MARL 方法（CQL、IQL、CFCQL 等）虽约束策略或正则化价值，但对全联合动作更新仍需大范围不可靠外推。核心洞见：若行为策略是 factorized（智能体独立或松散协调采集数据，现实常见），只改一个或少数智能体动作可使查询点贴近数据流形，大幅减小分布偏移。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非对抗，而是数据集稀疏覆盖引起的分布偏移；不确定性通过 Q-ensemble 标准差度量。理论假设行为策略 factorized（μ(a|s)=∏μi(ai|s)），并推广到带 maximal excess correlation κ 的相关行为策略。
- **设定**: cooperative；centralized training（共享 Q-function，隐式协调）；offline

## 方法 (Method)
- **PAR 原理**: 构造 Bellman target 时仅让 k 个智能体按学习策略偏离、其余 n-k 个用数据集动作，使查询联合动作只做小范围局部外推。
- **ICQL-QS（基线）**: individual Bellman operator T_i^ind 每次只改一个智能体动作，配合共享 Q 与 CQL 保守正则项，最稳定但“近视”、忽略协调收益。
- **SPaCQL（主贡献）**: 定义替换恰好 k 个智能体的算子 T^(k)，最终算子为 n 个算子的凸组合 T^SP=Σ w_k T^(k)（仍是 γ-contraction）。
- **不确定性加权**: 用 Q-ensemble 方差 u_k 度量第 k 种偏离的风险，权重 w_k=(1/u_k)/Σ(1/u_k)，高不确定性将权重推向更保守的小 k backup。
- target 取 ensemble 最小值以增强保守性，策略更新用共享 Q。

## 理论贡献 (Theoretical Contributions)
- **Lemma 1（线性散度界）**: factorized 下 W1(d(S),d(∅)) ≤ γ/(1-γ) Σ_{i∈S} TV(πi,μi)，分布偏移随偏离智能体数线性增长。
- **Theorem 1（紧价值误差界）**: |V^π−V̂^π| ≤ ε_Subopt+ε_FQI+ 4γ/(1-γ)² Σ TV(πi,μi)，单智能体偏离时严格优于联合-TV 界。
- **Theorem 2**: 放松 factorized 假设，相关性仅引入与 n 无关的加性惩罚 κ，仍避免维数灾难。
- **Theorem 3**: SPaCQL 误差随有效偏离数 k_eff=Σ w_k·k 缩放，自适应在 ICQL-QS 紧界与全联合松界之间插值。
- **Proposition 1**: ICQL-QS 的 TD 梯度等价于在 averaged-individual 算子上的中心化 TD 损失梯度（隐式协调）。

## 实验 (Experiments)
- **环境/Benchmark**: MPE (Cooperative Navigation, Predator-Prey, World) 与 Multi-Agent MuJoCo (Half-Cheetah)；每任务 4 种数据质量 Expert/Medium/Medium-Replay/Random。
- **Baselines**: OMAR, MACQL, IQL, MA-TD3+BC, DoF (diffusion), CFCQL。
- **评估指标**: 归一化得分（5 个随机种子的均值±标准差）；并测 Q-估计不确定性、自适应权重可视化。

## 主要结果 (Key Results)
- SPaCQL 在 16 个任务中 10 个超过所有 baseline；在每个 Random 与 Medium-Replay 数据集上一致显著领先（如 World-Random 94.3 vs CFCQL 68）。
- Expert 数据集上各方法相近，DoF 在 MPE Expert 上最强——高质量协调数据时贴近行为策略已足够。
- 自适应权重验证：Random/Medium-Replay 上 w1（单智能体偏离）占主导以求稳定；Expert 上 w2、w3 增大以捕捉协调。
- PAR (ICQL-QS) 的 Q-估计不确定性始终低于全联合更新 (CFCQL)。

## 局限与未来工作 (Limitations & Future Work)
- 理论需 Q̂ 满足 2/(1-γ)-Lipschitz（神经网络不自动满足，需谱归一化/梯度裁剪）；有限离散状态-动作、i.i.d. 转移等假设。
- 完整理论安全保证尚未给出；高度协调 (tight correlation) Expert 数据集上 PAR 优势有限。
- 未来：更精细的加权方案与不确定性估计技术。

## 与综述的关联 (Relevance to Survey)
属于 robust/offline MARL 中“缓解分布偏移与 OOD 鲁棒性”的价值正则化线，延续 CQL/CFCQL，贡献在于把 robustness 问题形式化为随偏离智能体数线性而非指数缩放的价值误差界，并用 ensemble 不确定性自适应。与不确定性估计、保守 RL、factorization、价值分解等主题相关。
