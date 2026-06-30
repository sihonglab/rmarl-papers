# 93. Sample Efficient Robust Offline Self-Play for Model-Based Reinforcement Learning

## Metadata
- **Title**: Sample Efficient Robust Offline Self-Play for Model-Based Reinforcement Learning
- **Authors**: Anonymous authors (paper under double-blind review)
- **Affiliation**: Not specified (anonymized for double-blind review)
- **Venue**: Under review as a conference paper at ICLR 2025
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty (transition-kernel perturbations); distributionally robust transition dynamics; each player has its own uncertainty set centered on a nominal kernel, capturing the sim-to-real gap.
- **Method paradigm**: Robust two-player zero-sum Markov games (RTZMGs) / distributionally robust optimization (DRO); model-based robust value iteration with lower confidence bounds (pessimism / LCB); minimax game-theoretic equilibrium; finite-sample (sample-complexity) theory.
- **Keywords**: robust Markov games, offline RL, two-player zero-sum, robust Nash equilibrium, sample complexity, partial coverage, distributionally robust RL

## TL;DR
The paper proposes RTZ-VI-LCB, a model-based robust value-iteration algorithm with a data-driven (Bernstein-style) penalty for offline robust two-player zero-sum Markov games, and proves the first sample-complexity upper bound that is optimal in state size S and action sizes {A, B} under only partial dataset coverage, together with matching information-theoretic lower bounds; it also extends to multi-player general-sum games (Multi-RTZ-VI-LCB), breaking the curse of multiagency.

## Problem & Motivation
Standard MARL algorithms trained under ideal conditions are highly sensitive and can fail catastrophically under small adversarial perturbations in deployment, motivating robust MARL. In offline (batch) MARL, historical data is gathered under an assumption of model stability that is unrealistic given time-varying, non-stationary real systems, so a robust guarantee is critical. Within two-player zero-sum Markov games (TZMGs), robust TZMGs (RTZMGs) introduce adversaries that select worst-case transition kernels from a predefined uncertainty set for each player. Despite recent efforts, there is no algorithm achieving optimal sample complexity under partial coverage while accounting for the uncertainty level: the best prior offline result (P2M2PO, Blanchet et al., 2024) is near-optimal in H, S, {A, B} but overlooks the influence of the uncertainty levels and uses a less tight maximum-density-ratio concentrability measure. The paper asks whether one can simultaneously achieve effective sample complexity, robustness, and Nash-policy learning under partial/limited coverage in TZMGs.

## Robustness Setting
- **Threat model / uncertainty set**: Transition-kernel uncertainty. Each player (max-player and min-player) independently defines its own uncertainty set Uσ+ρ(P0), Uσ−ρ(P0) centered on a nominal kernel P0, with radii σ+, σ− and a divergence ρ. The paper adopts "two-player-wise (s,a,b)-rectangularity," decomposing each set into a product of per-(s,a,b) subsets, and instantiates ρ as total-variation (TV) distance (general f-divergences, Wasserstein, ℓq norms are discussed as options). Players optimize worst-case (inf/sup over the uncertainty set) robust value functions.
- **Setting**: Competitive (two-player zero-sum), plus an extension to multi-player general-sum; centralized/model-based; offline (learning from a fixed historical dataset of K episodes collected by a behavior policy in the nominal MDP, under partial coverage).

## Method
- Build an empirical nominal model: from the dataset, construct plug-in estimates of the nominal transition kernel P̂0 and reward r̂ via empirical transition frequencies; apply a two-stage subsampling technique (Algorithm 1) adapted from single-agent RL to remove within-episode statistical dependencies and yield a distributionally equivalent dataset with independent samples (Lemma 1).
- Robust value iteration with LCB (RTZ-VI-LCB, Algorithm 2): proceed backward from h=H, computing optimistic/pessimistic robust Q-value estimates Q̂+ and Q̂− that incorporate inf/sup over the uncertainty set plus a data-driven penalty β_h.
- Dual reformulation: strong duality for TV distance (Iyengar, 2005) turns the inf/sup over the S-dimensional simplex into a one-dimensional dual maximization over a clipped value function, making the robust Bellman update computationally tractable.
- Penalty / pessimism: β_h is a Bernstein-style penalty built from the empirical variance Var_{P̂0}(V̂) and the visitation count N_h(s,a,b); it is tailored to the non-linear, implicit dependency introduced by the uncertainty set, unlike penalties in standard offline TZMGs.
- Policy extraction: for each state, solve the robust matrix game via ComputNash on Q̂+ and Q̂− (generally PPAD-hard because players may select different worst-case kernels); output the policy pair (µ̂ = {µ−}, ν̂ = {ν+}).
- Quality of data is measured by a novel "robust unilateral clipped concentrability coefficient" C⋆r ∈ [1/(S(A+B)), ∞), which captures distribution shift between behavior and single-side optimal robust policies under perturbation without requiring full coverage.

## Theoretical Contributions
- **Upper bound (Theorem 1)**: Under TV uncertainty sets with σ+, σ− ∈ (0,1], RTZ-VI-LCB attains an ε-robust NE with sample size Õ( C⋆r H4 S (A+B) / ε2 · min{ (Hσ+−1+(1−σ+)^H)/(σ+)2, (Hσ−−1+(1−σ−)^H)/(σ−)2, H } ), after a burn-in cost independent of ε. First optimal dependency on S and {A, B} for offline RTZMGs.
- **Lower bounds (Theorem 2)**: Information-theoretic lower bounds across uncertainty levels — Ω( C⋆r S H4 (A+B) / ε2 ) when min{σ+, σ−} ≲ 1/H (matching non-robust offline TZMGs, so RTZMGs are at least as hard as standard TZMGs for small uncertainty), and Ω( C⋆r S H3 (A+B) / (ε2 min{σ+,σ−}) ) when min{σ+, σ−} ≳ 1/H. These confirm optimality of RTZ-VI-LCB w.r.t. S, A, B and ε.
- **Multi-player extension (Theorem 3)**: Multi-RTZ-VI-LCB attains an ε-robust NE for robust multi-player general-sum MGs with sample size Õ( C⋆r H4 S Σ_i A_i / ε2 · min{ {(Hσi−1+(1−σi)^H)/(σi)2}_i, H } ), demonstrating a breakthrough in breaking the curse of multiagency.
- Supporting results: strong-duality of the robust Bellman operator under TV distance (Lemma 2), a Bernstein-type concentration / variance-matching lemma that decouples statistical dependency via leave-one-out analysis (Lemma 3), optimism of the estimate (Lemma 4), and a bound on the robust value-function range shrinking with uncertainty level (Lemma 5).

## Experiments
- **Environment/Benchmark**: Not specified (the paper is theoretical; no empirical experiments are reported).
- **Baselines**: Not specified (P2M2PO (Blanchet et al., 2024) is used as a theoretical comparison in Table 1, not an empirical baseline).
- **Evaluation metrics**: Not specified (theoretical sample complexity / suboptimality gap Gap(µ̂, ν̂) is the object of study).

## Key Results
- RTZ-VI-LCB achieves the first sample-complexity upper bound for offline RTZMGs that is optimal with respect to state S and action sizes {A, B}, while explicitly incorporating the full range of uncertainty levels (via the factor f(σ+, σ−, H)).
- It works under partial coverage: it requires only the mild "robust unilateral clipped concentrability" assumption (C⋆r) on the behavior policy rather than full state-action coverage, and uses a tighter concentrability measure than the maximum density ratio Cr of P2M2PO.
- Matching information-theoretic lower bounds (Theorem 2) certify the tightness/optimality of the bound across uncertainty regimes and show learning RTZMGs is at least as hard as standard TZMGs when uncertainty is small.
- The Multi-RTZ-VI-LCB extension attains an ε-robust NE for robust multi-player general-sum games whose sample complexity scales with Σ_i A_i (rather than the product of action sizes), breaking the curse of multiagency.

## Limitations & Future Work
- The sample complexity is optimal in S and {A, B} but the dependency on the horizon H is not claimed optimal (the lower bounds match in S, A, B and ε but not in H).
- The algorithm is model-based; designing efficient model-free algorithms for robust offline TZMGs with partial coverage is left open.
- Exploring ways to adjust the size and metric (divergence function) of the uncertainty set to complete the algorithmic design is identified as future work.
- Purely theoretical; no empirical validation is provided.

## Relevance to Survey
This paper sits on the "model/environment uncertainty" main line of robust MARL, formalized as distributionally robust two-player zero-sum (and multi-player general-sum) Markov games. It connects the robust-MDP / DRO single-agent robustness line (Iyengar 2005; Shi et al.) to the finite-sample, provably-efficient offline MARL / self-play line (Bai & Jin; Blanchet et al. 2024). It complements foundational robust-MARL works (e.g., Zhang et al. 2020, paper #1 in this corpus; Kardeş et al. 2011; Ma et al. 2023; Shi et al. 2024b) by providing tight sample-complexity theory under partial coverage and an explicit treatment of the uncertainty level, and by giving a "breaking the curse of multiagency" result for the general-sum robust setting. It is a key theoretical reference for the offline / sample-complexity and distributionally-robust subthemes of the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.2, Related Work — "Finite-sample studies of standard TZMGs."]_

"Markov games (MGs), or called stochastic games, were first proposed in the early 1950s (Shapley, 1953). Since then, extensive research has been conducted, and MARL has gained significant attention (Oroojlooy & Hajinezhad, 2023), particularly around Nash equilibrium (Littman, 1994; Lee et al., 2020). Numerous MARL algorithms with provable convergence and asymptotic guarantees have been developed (Rashid et al., 2020). More recent work has focused on creating algorithms for standard MARL with non-asymptotic guarantees through finite-sample analysis. In this area, most efforts to compute Nash equilibria are focused on TZMGs. The studies in (Bai & Jin, 2020) and (Xie et al., Jun. 2022) were the first to provide non-asymptotic sample complexity guarantees for model-based (e.g., VI-Explore and VI-ULCB) and model-free algorithms (e.g., OMNI-VI). Further improvements in sample complexity have been explored (Cui et al., 2023; Chen et al., 2022; Liu et al., July 2021; Feng et al., 2023; Li et al., 2024c)."

> _[Section 1.2, Related Work — "Robustness in MARL."]_

"Although progress has been made in standard MARL, existing algorithms may struggle when faced with environmental disturbances or uncertainties, leading to significantly deviated equilibria. Increasing research now focuses on enhancing MARL robustness against uncertainties in different parts of MGs (Vial et al., 2022), including state (Zhou & Liu, 2023), environment (reward and transition dynamics), agent types (Zhang et al., 2021), and other agents' policies (Kannan et al., 2023). A typical method to address robustness against uncertainties of the environment is distributionally robust optimization (DRO), which is a method predominantly explored in supervised learning (Bertsimas et al., 2018; Gao, 2023; Blanchet & Murthy, 2019). The application of DRO to manage model uncertainty in single-agent RL (Iyengar, 2005) has attracted considerable attention. However, when extended to MARL, researchers formulated the problem as robust MGs armed with DRO and developed a relatively understudied field with only a few proven algorithms (Blanchet et al., 2024; Kardeş et al., 2011; Ma et al., 2023; Zhang et al., 2020; Shi et al., 2024b). Thus, relevant algorithms based on partial coverage of datasets while considering the uncertainty level are lacking."

> _[Section 1.2, Related Work — "Single-agent robust RL."]_

"In single-agent RL, addressing uncertainties of environments using DRO—such as robust Markov decision processes (MDPs) and distributionally robust dynamic programming—has attracted considerable interest in both theoretical research and practical applications (Badrinath & Kalathil, 2021; Goyal & Grand-Clement, 2023). Recent work has focused on the finite-sample performance of provable robust RL algorithms, exploring different divergence functions for uncertainty sets, various sampling mechanisms, and related challenges (Yang et al., 2023; Blanchet et al., 2024; Shi et al., 2024a). Studies on robust MDPs, particularly relevant here, use uncertainty sets based on TV distance (Liu & Xu, 2024) or Kullback-Leibler (KL) divergence (Shi & Chi, 2024) in tabular settings. It has been shown that addressing robust MDPs does not demand more samples compared with those needed for standard MDPs (Shi et al., 2024a). However, RTZMGs present additional complexities beyond those in robust single-agent RL."

> _[Introduction — prior-work / motivation passage]_

"Standard MARL algorithms that train in ideal conditions are highly sensitive and prone to catastrophic failure when faced with even small adversarial perturbations in the deployment environment (Zhang et al., 2020; Yeh et al., 2021; Zeng et al., 2022). ... Despite recent efforts (Kardeş et al., 2011; Blanchet et al., 2024; Zhang et al., 2020; Ma et al., 2023), there is still a lack of fundamental understanding in learning for RTZMGs. For a tabular RTZMG with horizon length H, states S, actions {A, B}, and uncertainty sizes {σ+, σ−} for the two players, the best sample complexity for offline setting so far is achieved by P2M2PO (Blanchet et al., 2024) with a near-optimal sample complexity on H, S, {A, B}, where however the influence of uncertainty levels is overlooked."

### Cited references (resolved from the paper's bibliography)
- **[Shapley, 1953]** Lloyd S. Shapley. *Stochastic games.* Proceedings of the National Academy of Sciences, 39(10):1095–1100, 1953.
- **[Oroojlooy & Hajinezhad, 2023]** A. Oroojlooy, D. Hajinezhad. *A review of cooperative multi-agent deep reinforcement learning.* Applied Intelligence, 53(11):13677–13722, 2023.
- **[Littman, 1994]** Michael L. Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994, pp. 157–163, Elsevier.
- **[Lee et al., 2020]** C.-W. Lee, H. Luo, C.-Y. Wei, M. Zhang. *Linear last-iterate convergence for matrix games and stochastic games.* arXiv preprint arXiv:2006.09517, 2020.
- **[Rashid et al., 2020]** T. Rashid, G. Farquhar, B. Peng, S. Whiteson. *Weighted QMIX: Expanding monotonic value function factorisation for deep multi-agent reinforcement learning.* NeurIPS 33:10199–10210, 2020.
- **[Bai & Jin, 2020]** Yu Bai, Chi Jin. *Provable self-play algorithms for competitive reinforcement learning.* ICML, pp. 551–560, PMLR, 2020.
- **[Xie et al., Jun. 2022]** Q. Xie, Y. Chen, Z. Wang, Z. Yang. *Learning zero-sum simultaneous-move Markov games using function approximation and correlated equilibrium.* Mathematics of Operations Research, 48(1):433–462, Jun. 2022.
- **[Cui et al., 2023]** Q. Cui, K. Zhang, S. Du. *Breaking the curse of multiagents in a large state space: RL in Markov games with independent linear function approximation.* COLT, pp. 2651–2652, PMLR, 2023.
- **[Chen et al., 2022]** Z. Chen, D. Zhou, Q. Gu. *Almost optimal algorithms for two-player zero-sum linear mixture Markov games.* International Conference on Algorithmic Learning Theory (ALT), pp. 227–261, PMLR, 2022.
- **[Liu et al., July 2021]** Q. Liu, T. Yu, Y. Bai, C. Jin. *A sharp analysis of model-based reinforcement learning with self-play.* ICML, vol. 139, pp. 7001–7010, PMLR, July 2021.
- **[Feng et al., 2023]** S. Feng, M. Yin, Y.-X. Wang, J. Yang, Y. Liang. *Model-free algorithm with improved sample efficiency for zero-sum Markov games.* 2023.
- **[Li et al., 2024c]** Na Li, Y. Jiao, H. Shan, S. Yan. *Provable memory efficient self-play algorithm for model-free reinforcement learning.* ICLR 2024.
- **[Vial et al., 2022]** D. Vial, S. Shakkottai, R. Srikant. *Robust multi-agent bandits over undirected graphs.* Proceedings of the ACM on Measurement and Analysis of Computing Systems, 6(3):1–57, 2022.
- **[Zhou & Liu, 2023]** Z. Zhou, G. Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv preprint arXiv:2306.06136, 2023.
- **[Zhang et al., 2021]** Huan Zhang, Hongge Chen, Duane S. Boning, Cho-Jui Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[Kannan et al., 2023]** S. S. Kannan, V. L. N. Venkatesh, B.-C. Min. *SMART-LLM: Smart multi-agent robot task planning using large language models.* arXiv preprint arXiv:2309.10062, 2023.
- **[Bertsimas et al., 2018]** D. Bertsimas, V. Gupta, N. Kallus. *Data-driven robust optimization.* Mathematical Programming, 167:235–292, 2018.
- **[Gao, 2023]** Rui Gao. *Finite-sample guarantees for Wasserstein distributionally robust optimization: Breaking the curse of dimensionality.* Operations Research, 71(6):2291–2306, 2023.
- **[Blanchet & Murthy, 2019]** Jose Blanchet, Karthyek Murthy. *Quantifying distributional model risk via optimal transport.* Mathematics of Operations Research, 44(2):565–600, 2019.
- **[Iyengar, 2005]** Garud N. Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 30(2):257–280, 2005.
- **[Blanchet et al., 2024]** Jose Blanchet, Miao Lu, Tong Zhang, Han Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* NeurIPS 36, 2024.
- **[Kardeş et al., 2011]** Erim Kardeş, Fernando Ordóñez, Randolph W. Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 59(2):365–382, 2011.
- **[Ma et al., 2023]** Shaocong Ma, Ziyi Chen, Shaofeng Zou, Yi Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR, 24(371):1–40, 2023.
- **[Zhang et al., 2020]** Kaiqing Zhang, Tao Sun, Yunzhe Tao, Sahika Genc, Sunil Mallya, Tamer Başar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 33:10571–10583, 2020.
- **[Shi et al., 2024b]** Laixi Shi, Eric Mazumdar, Yuejie Chi, Adam Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* ICML 2024.
- **[Badrinath & Kalathil, 2021]** Kishan Panaganti Badrinath, Dileep Kalathil. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML, pp. 511–520, PMLR, 2021.
- **[Goyal & Grand-Clement, 2023]** Vineet Goyal, Julien Grand-Clement. *Robust Markov decision processes: Beyond rectangularity.* Mathematics of Operations Research, 48(1):203–226, 2023.
- **[Yang et al., 2023]** Wenhao Yang, Han Wang, Tadashi Kozuno, Scott M. Jordan, Zhihua Zhang. *Avoiding model estimation in robust Markov decision processes with a generative model.* arXiv preprint arXiv:2302.01248, 2023.
- **[Shi et al., 2024a]** Laixi Shi, Gen Li, Yuting Wei, Yuxin Chen, Matthieu Geist, Yuejie Chi. *The curious price of distributional robustness in reinforcement learning with a generative model.* NeurIPS 36, 2024.
- **[Liu & Xu, 2024]** Zhishuai Liu, Pan Xu. *Distributionally robust off-dynamics reinforcement learning: Provable efficiency with linear function approximation.* AISTATS, pp. 2719–2727, PMLR, 2024.
- **[Shi & Chi, 2024]** Laixi Shi, Yuejie Chi. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* JMLR, 25(200):1–91, 2024.
- **[Yeh et al., 2021]** Christopher Yeh, Chenlin Meng, Sherrie Wang, et al. *SustainBench: Benchmarks for monitoring the sustainable development goals with machine learning.* arXiv preprint arXiv:2111.04724, 2021.
- **[Zeng et al., 2022]** Lanting Zeng, Dawei Qiu, Mingyang Sun. *Resilience enhancement of multi-agent reinforcement learning-based demand response against adversarial attacks.* Applied Energy, 324:119688, 2022.
