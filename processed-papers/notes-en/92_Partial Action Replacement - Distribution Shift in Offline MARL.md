# 92. Partial Action Replacement: Tackling Distribution Shift in Offline MARL

## Metadata
- **Title**: Partial Action Replacement: Tackling Distribution Shift in Offline MARL
- **Authors**: Yue Jin, Giovanni Montana
- **Affiliation**: Warwick Manufacturing Group, University of Warwick (Coventry, UK); Department of Statistics, University of Warwick; The Alan Turing Institute (London, UK)
- **Venue**: AAAI 2026 (Copyright © 2026, AAAI; arXiv preprint dated 10 Nov 2025)
- **Link/arXiv**: arXiv:2511.07629v1 [cs.LG]

## Taxonomy
- **Robustness / perturbation type targeted**: Distribution shift / out-of-distribution (OOD) joint actions in offline MARL (curse of dimensionality in the joint-action space; mismatch between behavior policy μ and learned policy π)
- **Method paradigm**: Conservative Q-Learning (CQL) extension, partial action replacement, uncertainty-weighted Bellman backups (Q-ensemble variance), value regularization, contraction-mapping theory
- **Keywords**: Offline MARL, distribution shift, out-of-distribution actions, partial action replacement, conservative Q-learning, uncertainty estimation

## TL;DR
The paper introduces partial action replacement (PAR) — updating only one or a few agents' actions while fixing the others to logged data — and builds SPaCQL, an algorithm that adaptively mixes PAR strategies via Q-ensemble-uncertainty weights, proving that under factorized behavior policies the induced distribution shift scales linearly (not exponentially) with the number of deviating agents, yielding a tighter value-error bound.

## Problem & Motivation
Offline MARL learns from fixed datasets but is hampered by the combinatorial curse of dimensionality in the joint-action space: any finite dataset sparsely covers possible action combinations, forcing value-based methods to evaluate countless OOD joint actions for which a function approximator can produce arbitrarily high Q-values, leading to policy divergence. Prior offline-MARL work either constrains learned policies or regularizes value functions but still typically evaluates fully new joint actions that are almost certainly OOD. The paper's core insight is geometric: by changing only one or a few action coordinates of a known data point, the Q-function is queried close to familiar territory, requiring only small local extrapolation rather than a large leap into the unknown.

## Robustness Setting
- **Threat model / uncertainty set**: Distribution shift between the learned joint policy π and the data-collecting behavior policy μ. Uncertainty about value estimates of OOD joint actions is quantified via the standard deviation / variance of a Q-function ensemble. A "factorized behavior policy" assumption (agents acted fully or partially independently during data collection, μ(a|s) = Π_i μ_i(a_i|s)) is central; a relaxation introduces a maximal excess correlation κ ∈ [0,1] measuring deviation from factorization.
- **Setting**: Cooperative (Dec-MDP); centralized training with a shared Q-function; offline (learning solely from a static dataset, no environment interaction).

## Method
- Formalizes partial action replacement (PAR): construct Bellman targets where only one or a subset of agents' next actions are sampled from their learned policies while the remaining agents' actions are taken from the logged data, keeping queries anchored near the data manifold.
- ICQL-QS (Individual CQL with Q-sharing): a stable baseline using an individual Bellman operator T_i^ind that changes only agent i's action at a time, training a single shared Q-function by minimizing the average per-agent loss (squared Bellman error plus a CQL-style conservative regularizer). The shared Q-function implicitly couples agents and fosters coordination.
- SPaCQL (Soft-Partial Conservative Q-Learning): the primary contribution. It defines base operators T^(k) for k = 1..n, each replacing exactly k uniformly-chosen agents' actions, and forms the soft-partial operator T^SP as a convex combination Σ_k w_k T^(k); as a convex combination of γ-contractions it is itself a γ-contraction.
- Adaptive weighting: uncertainty u_k is measured as the Q-ensemble standard deviation at the next state for the k-deviation backup; weights are set to w_k = (1/u_k)/Σ_k(1/u_k), so higher disagreement (poorer coverage) down-weights riskier larger-k deviations. The learning objective combines TD error on T^SP with the CFCQL-style conservative penalty ξ_c, using an ensemble min for conservatism in the target.

## Theoretical Contributions
- **Lemma 1 (Linear Divergence Bound)**: under a factorized behavior policy, W1(d(S), d(∅)) ≤ (γ/(1−γ)) Σ_{i∈S} TV(π_i, μ_i) — occupancy shift grows additively with the number of deviating agents despite the exponential joint-action space.
- **Theorem 1 (Tight Value-Error Bound)**: |V^π − V̂^π| ≤ ε_Subopt + ε_FQI + (4γ/(1−γ)²) Σ_i TV(π_i, μ_i), scaling linearly in n; a remark shows a single-agent deviation strictly improves on the usual joint-TV bound.
- **Lemma 2 / Theorem 2 (with correlations)**: relaxing factorization adds a single additive penalty κ (maximal excess correlation) that is independent of n, so the bound stays linear in n and is merely shifted upward.
- **Theorem 3 (SPaCQL Value-Error Bound)**: error scales with the state-dependent effective number of deviations k_eff = Σ_k w_k·k, recovering the tight ICQL-QS bound when weights concentrate on k=1 and approaching the looser full-joint bound when weights shift to k=n.
- **Proposition 1 (Gradient equivalence of ICQL-QS)**: the per-agent TD update is equivalent (under the semi-gradient assumption) to SGD on a centralized TD loss with the averaged-individual operator T^ai = (1/n)Σ_i T_i^ind, justifying implicit coordination.

## Experiments
- **Environment/Benchmark**: Multi-Agent Particle Environments (MPE) — Cooperative Navigation (CN), Predator-Prey (PP), World — and Multi-Agent MuJoCo (MaMujoco) — Half-Cheetah. Each task uses four dataset types: Expert (Exp), Medium (Med), Medium-Replay (Med-R), Random (Rand). 10-network Q-ensemble; 5 random seeds; same datasets as recent works (Shao et al. 2023; Pan et al. 2022; Kostrikov et al. 2022); PyTorch on NVIDIA Tesla V100 GPUs.
- **Baselines**: OMAR, IQL, MA-TD3+BC (policy-constrained); MACQL, CFCQL (value-constrained); DoF (diffusion-model-based).
- **Evaluation metrics**: Average normalized score (mean ± std over seeds); analysis of Q-estimate uncertainty (ensemble standard deviation); visualization of learned adaptive weights w_k.

## Key Results
- SPaCQL outperforms all baselines on 10 of 16 tasks, with the largest gains on low-quality / uncoordinated data: it is consistently superior on every "Random" and "Medium-Replay" dataset across all four tasks (e.g., World/Random: SPaCQL 94.3 ± 7.4 vs. next-best CFCQL 68 ± 20.8).
- On high-quality "Expert" datasets performance is comparable across methods; DoF tops all three MPE Expert datasets, indicating that when data already contains highly coordinated trajectories, staying close to the underlying policies suffices.
- Empirically, partial action replacement (ICQL-QS) yields significantly lower Q-estimation uncertainty than full joint-action updates (CFCQL), especially on Random datasets.
- The learned weights confirm adaptivity: w1 (single-agent deviation) dominates on Random/Medium-Replay, while w2, w3 (coordinated deviations) increase on Expert datasets.

## Limitations & Future Work
- Theorem 1's Lipschitz assumption on the learned Q̂ (2/(1−γ)-Lipschitz under the 0-1 metric) is not automatically guaranteed for neural networks and must be encouraged with techniques like spectral normalization or gradient clipping.
- Complete theoretical safety guarantees are stated as pending analysis; the support is primarily empirical motivation.
- Advantage is most pronounced under independence-structured / less-coordinated data; on highly coordinated expert datasets PAR can be "coordination-blind" and overly pessimistic.
- Future work: more sophisticated weighting schemes and uncertainty estimation techniques.

## Relevance to Survey
This paper sits on the offline-MARL / distribution-shift robustness line of the survey, addressing robustness to out-of-distribution joint actions rather than environment or adversarial perturbations. It extends conservative value-regularization methods (CQL/CFCQL) with an uncertainty-weighted, locally-anchored backup, and connects to ensemble-based uncertainty estimation and the broader theme of mitigating the curse of dimensionality in multi-agent value learning. It complements robust-MARL works by providing provable error bounds that degrade gracefully (additive κ penalty) when modeling assumptions are violated.

## Related Work (verbatim excerpts from the paper)
> _[Section: Related Work — opening paragraph]_

"Offline reinforcement learning addresses learning effective policies from static datasets without environment interaction. Single-agent methods like CQL (Kumar et al. 2020), IQL (Kostrikov, Nair, and Levine 2022), and BEAR (Kumar et al. 2019) tackle distribution shift by constraining policies or regularizing value functions. The multi-agent setting amplifies these challenges due to exponential joint-action space growth and coordination requirements. Offline MARL research focuses on two main approaches: constraining learned policies or regularizing value functions. Our work builds on the latter with a novel adaptive mechanism."

> _[Section: Related Work — "Policy-Constrained Methods"]_

"Building on single-agent approaches like AWR (Peng et al. 2019) and AWAC (Nair et al. 2020), these methods ensure policies don't deviate excessively from the behavior policy (Pan et al. 2022; Tseng et al. 2022). (Pan et al. 2022) use evolution strategies for decentralized regularization, while (Tseng et al. 2022) employs a Teacher-Student paradigm where a centralized transformer predicts joint actions and individual policies mimic both actions and structural relationships."

> _[Section: Related Work — "Value-Constrained Methods"]_

"These methods constrain the value function, penalizing OOD actions (Yang et al. 2021; Shao et al. 2023; Barde et al. 2024; Ma and Wu 2023; Wang and Zhan 2023; Wang et al. 2023).

CFCQL (Shao et al. 2023) extends CQL (Kumar et al. 2020) to multi-agent settings, penalizing each agent's OOD action individually while holding others constant—sharing motivation with our partial replacement. However, we use partial replacement for target value computation (not just regularization) and introduce adaptive weighting based on uncertainty.

Others adapt online MARL mechanisms like QMIX (Rashid et al. 2018) and QTRAN (Son et al. 2019) to offline settings. (Wang and Zhan 2023) and (Wang et al. 2023) decompose global Q-functions: the former uses IQL's expectile regression, the latter formulates convex optimization. We differ by using centralized training with shared Q-functions, capturing coordination implicitly.

(Barde et al. 2024) use world models to generate trajectories with uncertainty-modified rewards. Recent works employ diffusion models: DoF (Li et al. 2025), MADIFF (Zhu et al. 2024), and INS (Fu et al. 2025).

Uncertainty estimation via ensembles (An et al. 2021; Bai et al. 2022; Zhang et al. 2020; Osband et al. 2016; Lakshminarayanan, Pritzel, and Blundell 2017) helps avoid overestimating OOD actions. We use ensemble variance to weight partial replacement strategies—higher uncertainty reduces contribution in Q-updates, adapting to dataset characteristics."

> _[Introduction — on prior work and the OOD challenge]_

"Standard value-based methods, like Q-learning, are notoriously prone to failure in this regime (Kumar et al. 2020, 2019). A function approximator, such as a neural network, can produce arbitrarily high Q-values for these unseen OOD actions. These erroneous estimates guide agents toward divergent policies that fail to generalize, making robust offline MARL a significant challenge (Yang et al. 2021; Shao et al. 2023)."

> _[Introduction — on the factorized / independent data collection scenario]_

"Crucially, this approach is most effective when the offline dataset was collected by agents acting independently or whose behaviors are loosely coordinated—a common scenario in practice, including independent human demonstrations, independently trained agents, or decentralized systems (Chen et al. 2017; Tampuu et al. 2017; Leibo et al. 2017)."

### Cited references (resolved from the paper's bibliography)
- **[An et al. 2021]** An, Moon, Kim, Song. *Uncertainty-Based Offline Reinforcement Learning with Diversified Q-Ensemble.* NeurIPS 2021.
- **[Bai et al. 2022]** Bai, Wang, Yang, Deng, Garg, Liu, Wang. *Pessimistic Bootstrapping for Uncertainty-Driven Offline Reinforcement Learning.* ICLR 2022.
- **[Barde et al. 2024]** Barde, Foerster, Nowrouzezahrai, Zhang. *A Model-Based Solution to the Offline Multi-Agent Reinforcement Learning Coordination Problem.* AAMAS 2024, 141–150.
- **[Chen et al. 2017]** Chen, Liu, Everett, How. *Decentralized non-communicating multiagent collision avoidance with deep reinforcement learning.* IEEE ICRA 2017, 285–292.
- **[Fu et al. 2025]** Fu, Zhu, Zhao, Chai, Zhao. *INS: Interaction-aware Synthesis to Enhance Offline Multi-agent Reinforcement Learning.* ICLR 2025.
- **[Kostrikov, Nair, and Levine 2022]** Kostrikov, Nair, Levine. *Offline Reinforcement Learning with Implicit Q-Learning.* ICLR 2022.
- **[Kumar et al. 2019]** Kumar, Fu, Tucker, Levine. *Stabilizing off-policy Q-learning via bootstrapping error reduction (BEAR).* NeurIPS 2019.
- **[Kumar et al. 2020]** Kumar, Zhou, Tucker, Levine. *Conservative Q-Learning for Offline Reinforcement Learning (CQL).* NeurIPS 2020.
- **[Lakshminarayanan, Pritzel, and Blundell 2017]** Lakshminarayanan, Pritzel, Blundell. *Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles.* NeurIPS 2017.
- **[Leibo et al. 2017]** Leibo, Zambaldi, Lanctot, Marecki, Graepel. *Multi-agent Reinforcement Learning in Sequential Social Dilemmas.* AAMAS 2017, 464–473.
- **[Li et al. 2025]** Li, Deng, Lin, Chen, Fu, Liu, Ab, Wang, Shen. *DoF: A diffusion factorization framework for offline multi-agent reinforcement learning.* ICLR 2025.
- **[Ma and Wu 2023]** Ma, Wu. *Learning to Coordinate from Offline Datasets with Uncoordinated Behavior Policies.* AAMAS 2023, 1258–1266.
- **[Nair et al. 2020]** Nair, Gupta, Dalal, Levine. *AWAC: Accelerating Online Reinforcement Learning with Offline Datasets.* arXiv:2006.09359, 2020.
- **[Osband et al. 2016]** Osband, Blundell, Pritzel, Van Roy. *Deep exploration via bootstrapped DQN.* NeurIPS 2016, 4033–4041.
- **[Pan et al. 2022]** Pan, Huang, Ma, Xu. *Plan Better Amid Conservatism: Offline Multi-Agent Reinforcement Learning with Actor Rectification (OMAR).* PMLR 162: 17221–17237, 2022.
- **[Peng et al. 2019]** Peng, Kumar, Zhang, Levine. *Advantage-Weighted Regression: Simple and Scalable Off-Policy Reinforcement Learning (AWR).* arXiv:1910.00177, 2019.
- **[Rashid et al. 2018]** Rashid, Samvelyan, De Witt, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018, 6846–6859.
- **[Shao et al. 2023]** Shao, Qu, Chen, Zhang, Ji. *Counterfactual Conservative Q Learning for Offline Multi-agent Reinforcement Learning (CFCQL).* NeurIPS 2023.
- **[Son et al. 2019]** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning.* ICML 2019, 10329–10346.
- **[Tampuu et al. 2017]** Tampuu, Matiisen, Kodelja, Kuzovkin, Korjus, Aru, Aru, Vicente. *Multiagent cooperation and competition with deep reinforcement learning.* PLoS ONE 12(4), 2017.
- **[Tseng et al. 2022]** Tseng, Wang, Yen-Chen, Isola. *Offline Multi-Agent Reinforcement Learning with Knowledge Distillation.* NeurIPS 2022, vol. 35.
- **[Wang et al. 2023]** Wang, Xu, Zheng, Zhan. *Offline Multi-Agent Reinforcement Learning with Implicit Global-to-Local Value Regularization.* NeurIPS 2023.
- **[Wang and Zhan 2023]** Wang, Zhan. *Offline Multi-Agent Reinforcement Learning with Coupled Value Factorization.* AAMAS 2023, 2781–2783.
- **[Yang et al. 2021]** Yang, Ma, Li, Zheng, Zhang, Huang, Yang, Zhao. *Believe What You See: Implicit Constraint Approach for Offline Multi-Agent Reinforcement Learning.* NeurIPS 2021.
- **[Zhang et al. 2020]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Zhu et al. 2024]** Zhu, Liu, Mao, Kang, Xu, Yu, Ermon, Zhang. *MADIFF: Offline Multi-agent Learning with Diffusion Models.* NeurIPS 2024.
