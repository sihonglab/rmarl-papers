# 3. Breaking the Curse of Multiagency in Robust Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Breaking the Curse of Multiagency in Robust Multi-Agent Reinforcement Learning
- **Authors**: Laixi Shi, Jingchu Gai, Eric Mazumdar, Yuejie Chi, Adam Wierman
- **Affiliation**: California Institute of Technology (Shi, Mazumdar, Wierman); Peking University (Gai); Carnegie Mellon University (Chi)
- **Venue**: ICML 2025 (Forty-Second International Conference on Machine Learning)
- **Link/arXiv**: arXiv:2409.20067v3

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental uncertainty (sim-to-real gap, dynamics shift); distributionally robust, worst-case over agent-wise fictitious uncertainty sets incorporating other agents' integrated behavior
- **Method paradigm**: Model-based; fictitious uncertainty sets (inspired by behavioral economics / quantal response); (s,ai)-rectangularity (marginal over others' policies); generative model; Robust-Q-FTRL algorithm (online learning with FTRL + variance bonus); breaks curse of multiagency
- **Keywords**: Fictitious uncertainty sets, Robust-Q-FTRL, curse of multiagency, robust CCE, generative model, behavioral economics, (s,ai)-rectangularity, TV uncertainty

## TL;DR
Introduces a new class of RMGs with fictitious uncertainty sets — where each agent's uncertainty is shaped by both the environment and the aggregated behavior of other agents (inspired by behavioral economics) — and proposes Robust-Q-FTRL, the first algorithm to break the curse of multiagency for robust Markov games, achieving sample complexity linear in the sum ΣA_i rather than the product ΠA_i.

## Problem & Motivation
Existing provable algorithms for RMGs all use (s,a)-rectangular uncertainty sets and suffer from the curse of multiagency: sample complexity scales exponentially as ΠA_i with the joint action space. Standard MARL has broken this curse (e.g., Jin et al. 2021 achieves ΣA_i), but robust MARL remains stuck. Furthermore, the (s,a)-rectangularity construction is behaviorally unrealistic: behavioral economics shows that people handling uncertainty from others consider the risk-aware outcome of other agents' joint policy in an integrated manner, rather than flipping the expectation and risk metric. Two open questions are therefore: (1) How to construct more natural/realistic uncertainty sets for RMGs? (2) Can robust MARL break the curse of multiagency?

## Robustness Setting
- **Threat model / uncertainty set**: Fictitious TV-distance uncertainty sets. For each agent i at (s,ai,h), the adversary's uncertainty set is centered at the expected nominal transition marginalized over other agents' policies: P^{π_{-i}}_{h,s,ai}(s') := Σ_{a_{-i}} [π_h(ai,a_{-i}|s)/π_{i,h}(ai|s)] P^0_h(s'|s,a). This is a (s,ai)-rectangular construction that is policy-dependent and captures how each agent views aggregate environmental uncertainty conditioned only on its own action.
- **Setting**: n-player finite-horizon episodic general-sum Markov games; generative model (adaptive sampling); solution concept: robust CCE; purely theoretical.

## Method
- **Fictitious uncertainty sets**: Each agent i's uncertainty set Uσi(P^{π_{-i}}, ·) is centered at P^{π_{-i}} (which depends on other agents' current policies) and defined by TV radius σi. This captures a more realistic "integrated" view of environment uncertainty.
- **Robust-Q-FTRL**: Combines three modules — (1) N-sample estimation of empirical models {r̂_{i,h}, P̂_{i,h}} for each agent i separately (using their own (s,ai) marginals); (2) variance-style uncertainty quantification to handle nonlinearity of the robust Bellman operator; (3) Follow-the-Regularized-Leader (FTRL) policy updates using optimistic robust Q-estimates with confidence bonus terms β_{i,h}(s).
- Backward induction over h = H,...,1 with K FTRL iterations per step.
- Key: since uncertainty sets use P^{π_{-i}}, the model estimation for agent i only requires sampling from agent i's own (s,ai) pairs (not the full joint (s,a)), enabling the sum-of-actions sample scaling.

## Theoretical Contributions
- **Theorem 1 (Existence)**: Robust NE and robust CCE exist for fictitious RMGs under mild assumptions.
- **Theorem 2 (Upper bound)**: Robust-Q-FTRL finds an ε-robust CCE with probability ≥ 1−δ provided  
  N ≥ C₁H²/ε² · min{1/min_i σi, H} and K ≥ C₁H³/ε²,  
  giving total samples Ñ = Õ(SH⁶ Σ_{i=1}^n A_i / ε⁴ · min{H, 1/min_i σi}).
- **Lower bound**: Invoking Shi et al. (2024) lower bound on single-agent RMDPs (a special case), the lower bound for fictitious RMGs is Ω(SH³ max_i A_i / ε² · min{H, 1/min_i σi}).
- **Curse of multiagency broken**: The upper bound scales with Σ_i A_i (linear in agents) rather than Π_i A_i (exponential). This is the first such result for any class of RMGs.

## Experiments
Not applicable — purely theoretical paper. The motivating context (fishing-protection game, sim-to-real gap) is discussed qualitatively.

## Key Results
- First algorithm to break the curse of multiagency in robust Markov games.
- Sample complexity scales as Õ(SH⁶ ΣA_i / ε⁴ · min{H, 1/min σi}) — polynomial in all parameters.
- New class of fictitious RMGs shown to be well-posed (equilibria exist) and interpretable via behavioral economics (risk-aware people consider integrated uncertainty over others' strategies).
- Gap between upper (ε⁴ denominator) and lower (ε² denominator) bounds leaves room for future improvement.

## Limitations & Future Work
- H dependency in the upper bound (H⁶) and ε⁴ leave a gap vs. the lower bound (H³, ε²).
- Fictitious uncertainty sets are specific to TV distance; other divergences require future work.
- Online setting (beyond generative model) for fictitious RMGs remains open.
- The paper focuses on CCE; robust NE learning with the sum-action complexity is unresolved.

## Relevance to Survey
Central to the curse-of-multiagency thread in robust MARL; introduces the fictitious uncertainty set concept that is subsequently extended to linear function approximation (paper 4); shows how behavioral economics motivates novel mathematical structures in RMGs; companion paper to [2] (same research group, same authors).

## Related Work (verbatim excerpts from the paper)

> _[Section 1.3, Related works]_

**Breaking curse of multiagency for standard Markov games.**

"Breaking the curse of multiagency is a major and prevalent challenge in sequential games. In standard multi-agent general-sum MGs, it has been shown that learning a Nash equilibrium requires an exponential sample complexity (Bai and Jin, 2020; Rubinstein, 2017; Song et al., 2021). However, for other types of equilibria, such as CE and CCE, many works have successfully broken the curse of multiagency. Specifically, for finite-horizon general-sum MGs in the tabular setting with finite state and action spaces, Jin et al. (2021) developed the V-learning algorithm for learning CE and CCE with the sample complexity of Õ(H⁶S(max_{i∈[n]} A_i)²/ε²) and Õ(H⁶S max_{i∈[n]} A_i/ε²), respectively; Daskalakis et al. (2023) achieved a sample complexity of Õ(H¹¹S³ max_{i∈[n]} A_i/ε³) for learning a CCE. Beyond tabular settings, Wang et al. (2023) and Cui et al. (2023) extended these results to linear function approximation, achieving sample complexities of Õ(d⁴H⁶(max_{i∈[n]} A_i⁵)/ε²) and Õ(H¹⁰d⁴ log(max_{i∈[n]} A_i)/ε⁴), respectively, where d is the dimension of the linear features. For Markov potential games, a subclass of MGs, Song et al. (2021) provided a centralized algorithm that learns a NE with a sample complexity of Õ(H⁴S² max_{i∈[n]} A_i/ε³)."

**Finite-sample analysis for distributionally robust Markov games.**

"Robust Markov games under environmental uncertainty are largely underexplored, with only a few provable algorithms (Blanchet et al., 2023; Kardeş et al., 2011; Ma et al., 2023; Shi et al., 2024; Zhang et al., 2020a). Existing sample complexity analyses all suffer from the daunting curse of multiagency issues, or impose an extremely restricted uncertainty level that can fail to deliver the desired robustness (Blanchet et al., 2024; Ma et al., 2023; Shi et al., 2024). Specifically, they all consider a class of RMGs with the (s, a)-rectangularity condition, where the uncertainty sets for each agent can be decomposed into independent sets over each (s, a) pair. Shi et al. (2024) considered the generative model with an uncertainty set measured by the TV distance, Blanchet et al. (2023) treated a different sampling mechanism with offline data for both the TV distance and KL divergence. In addition, Ma et al. (2023) required the uncertainty level be much smaller than the accuracy-level and an instance-dependent parameter (i.e., σ_i ≤ max{ε/(SH²), p_min/H} for all i ∈ [n]). This can thus fail to maintain the desired robustness, especially when the accuracy requirement is high (i.e., ε → 0) or the RMG has small minimal positive transition probabilities (i.e., p_min → 0)."

**Robust MARL.**

"Standard MARL algorithms may overfit the training environment and could fail dramatically due to the perturbations and variability of both agents' behaviors and the shared environment, leading to performance drop and large deviation from the equilibrium. To address this, this work considers a robust variant of MARL adopting the distributionally robust optimization (DRO) framework that has primarily been investigated in supervised learning (Bertsimas et al., 2018; Blanchet and Murthy, 2019; Duchi and Namkoong, 2018; Gao, 2020; Rahimian and Mehrotra, 2019) and has attracted a lot of attention in promoting robustness in single-agent RL (Badrinath and Kalathil, 2021; Iyengar, 2005; Nilim and El Ghaoui, 2005; Shi and Chi, 2024; Shi et al., 2023; Wang et al., 2024; Zhou et al., 2021). Beyond the RMG framework considered in this work, recent research has advanced the robustness of MARL algorithms from various perspectives, including resilience to uncertainties or attacks on states (Han et al., 2022; Zhou and Liu, 2023), the type of agents (Zhang et al., 2021), other agents' policies (Kannan et al., 2023; Li et al., 2019), offline data poisoning (McMahan et al., 2024; Wu et al., 2024), and nonstationary environment (Szita et al., 2003). A recent review can be found in Vial et al. (2022)."

### Cited references (resolved from the paper's bibliography)
- **Bai and Jin (2020)** Bai, Jin. *Provable self-play algorithms for competitive reinforcement learning.* ICML 2020.
- **Rubinstein (2017)** Rubinstein. *Settling the complexity of computing approximate two-player Nash equilibria.* ACM SIGecom Exchanges, 2017.
- **Song et al. (2021)** Song, Mei, Bai. *When can we learn general-sum Markov games with a large number of players sample-efficiently?* arXiv:2110.04184, 2021.
- **Jin et al. (2021)** Jin, Liu, Wang, Yu. *V-learning — a simple, efficient, decentralized algorithm for multiagent RL.* arXiv:2110.14555, 2021.
- **Daskalakis et al. (2023)** Daskalakis, Golowich, Zhang. *The complexity of Markov equilibrium in stochastic games.* COLT 2023.
- **Wang et al. (2023)** Wang, Liu, Bai, Jin. *Breaking the curse of multiagency: Provably efficient decentralized multi-agent RL with function approximation.* COLT 2023.
- **Cui et al. (2023)** Cui, Zhang, Du. *Breaking the curse of multiagents in a large state space: RL in Markov games with independent linear function approximation.* COLT 2023.
- **Blanchet et al. (2023)** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning.* arXiv:2305.09659 / NeurIPS 2024.
- **Kardeş et al. (2011)** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **Ma et al. (2023)** Ma, Chen, Zou, Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR, 2023.
- **Shi et al. (2024)** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* ICML 2024.
- **Zhang et al. (2020a)** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **Bertsimas et al. (2018)** Bertsimas, Gupta, Kallus. *Data-driven robust optimization.* Mathematical Programming, 2018.
- **Blanchet and Murthy (2019)** Blanchet, Murthy. *Quantifying distributional model risk via optimal transport.* Mathematics of Operations Research, 2019.
- **Duchi and Namkoong (2018)** Duchi, Namkoong. *Learning models with uniform performance via distributionally robust optimization.* arXiv:1810.08750, 2018.
- **Gao (2020)** Gao. *Finite-sample guarantees for Wasserstein distributionally robust optimization.* arXiv:2009.04382, 2020.
- **Rahimian and Mehrotra (2019)** Rahimian, Mehrotra. *Distributionally robust optimization: A review.* arXiv:1908.05659, 2019.
- **Badrinath and Kalathil (2021)** Badrinath, Kalathil. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML 2021.
- **Iyengar (2005)** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **Nilim and El Ghaoui (2005)** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 2005.
- **Shi and Chi (2024)** Shi, Chi. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* JMLR, 2024.
- **Shi et al. (2023)** Shi, Li, Wei, Chen, Geist, Chi. *The curious price of distributional robustness in reinforcement learning with a generative model.* NeurIPS 2023.
- **Zhou et al. (2021)** Zhou, Bai, Zhou, Qiu, Blanchet, Glynn. *Finite-sample regret bound for distributionally robust offline tabular reinforcement learning.* AISTATS 2021.
- **Han et al. (2022)** Han, Su, He, Han, Yang, Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **Zhou and Liu (2023)** Zhou, Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv:2306.06136, 2023.
- **Zhang et al. (2021)** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **Kannan et al. (2023)** Kannan, Venkatesh, Min. *Smart-LLM: Smart multi-agent robot task planning using large language models.* arXiv:2309.10062, 2023.
- **Li et al. (2019)** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **McMahan et al. (2024)** McMahan, Artiglio, Xie. *Roping in uncertainty: Robustness and regularization in Markov games.* arXiv:2406.08847, 2024.
- **Wu et al. (2024)** Wu, McMahan, Zhu, Xie. *Data poisoning to fake a Nash equilibria for Markov games.* AAAI 2024.
- **Szita et al. (2003)** Szita, Takács, Lorincz. *ε-MDPs: Learning in varying environments.* JMLR, 2003.
- **Vial et al. (2022)** Vial, Shakkottai, Srikant. *Robust multi-agent bandits over undirected graphs.* ACM MACS, 2022.
- **Wang et al. (2024)** Wang, Shi, Chi. *Sample complexity of offline distributionally robust linear Markov decision processes.* arXiv:2403.12946, 2024.
