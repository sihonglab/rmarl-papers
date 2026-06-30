# 8. Distributionally Robust Online Markov Game with Linear Function Approximation

## Metadata
- **Title**: Distributionally Robust Online Markov Game with Linear Function Approximation
- **Authors**: Zewu Zheng, Yuanyuan Lin
- **Affiliation**: Department of Statistics and Data Science, The Chinese University of Hong Kong
- **Venue**: Not specified (arXiv:2511.07831v1 [stat.ML], 11 Nov 2025; copyright notice "Copyright © 2026")
- **Link/arXiv**: arXiv:2511.07831v1

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty (distributional shift of the transition dynamics between simulator and test environment; sim-to-real gap), modeled via d-rectangular total-variation uncertainty sets.
- **Method paradigm**: Distributionally robust Markov game (DRMG) theory; robust least-square value iteration with exploration bonus; minimax/worst-case over uncertainty sets; coarse correlated equilibrium (CCE); linear function approximation; regret/sample-complexity analysis.
- **Keywords**: distributionally robust RL, online Markov game, linear function approximation, d-rectangular uncertainty set, coarse correlated equilibrium, regret bound

## TL;DR
Proposes DR-CCE-LSI, the first sample-efficient algorithm for online distributionally robust general-sum Markov games with linear function approximation, achieving an Õ(dH·min{H, 1/min{σᵢ}}·√K) regret toward an ε-approximate robust CCE that matches the single-agent result and is minimax optimal in the feature dimension d.

## Problem & Motivation
The sim-to-real gap (degraded performance of policies trained in a simulator when deployed in a perturbed real environment) is a fundamental challenge in RL, and is especially acute in MARL where equilibrium solutions are highly sensitive to small environmental perturbations. Distributionally robust RL learns policies that act robustly under worst-case environment shift, but for large state spaces requires function approximation. While online linear MDPs (single agent) and non-robust online linear Markov games have been studied, online robust general-sum Markov games with linear function approximation remained an open problem. The paper asks whether one can design a provably sample-efficient algorithm for this setting, and must overcome a fundamental hardness (support shift) result for online robust learning.

## Robustness Setting
- **Threat model / uncertainty set**: The test-environment transition kernel P lies in a prescribed uncertainty set Uᵟᵢ_TV(P⁰) centered at the nominal (simulator) kernel P⁰, with a separate uncertainty level σᵢ per player i. The set uses the d-rectangular structure under total variation distance: each coordinate j of the linear factorization µ_{h,j} is perturbed within TV-radius σᵢ. The robust value functions take an inf over P in the uncertainty set (worst-case dynamics). To circumvent the support-shift hardness, the paper adopts a vanishing minimal value assumption (min_s Vᵖ,σ_{i,h}(s) = 0).
- **Setting**: competitive/cooperative mixed (multi-player general-sum Markov game); centralized learning with global linear function approximation; online (interactive data collection, episodic, finite horizon H).

## Method
- Formalizes a distributionally robust general-sum Markov game MG_rob = (S, {Aᵢ}, {Uᵟᵢ_ρ(P⁰)}, r, H) under the linear Markov game assumption (reward and transition kernel are linear in a known feature map ϕ), with a d-rectangular TV uncertainty set so the robust action-value function stays linear (avoiding a completeness assumption).
- Establishes an online regret lower bound Ω(σ·HK) showing learning is impossible without extra assumptions (support shift), then adopts the vanishing minimal value assumption (from Lu et al. 2024); Proposition 4.3 shows this restricts the worst-case kernel to the support of the nominal kernel, with sup_{s'} P̃_h(s'|s,a)/P⁰_h(s'|s,a) ≤ 1/σᵢ, avoiding support shift.
- DR-CCE-LSI: in each episode, each agent estimates its robust Q via ridge regression (with dual/strong-duality reformulation max_α{ν_{i,h,j}(α) − σᵢα}), adds an agent-specific optimistic exploration bonus Γⁱ_{h,k}(s,a) = βᵢ Σⱼ √(ϕⱼ 1ⱼᵀ(Λᵏ_h)⁻¹1ⱼ ϕⱼ) (a sum of d UCB terms, distinct from the non-robust linear-MDP bonus), and clips the Q estimate by min{H, 1/σᵢ}.
- Uses a Find-CCE subroutine: because CCEs of general-sum games are unstable (not Lipschitz) w.r.t. payoff changes, it solves the CCE on a point from an ε-cover of the Q-function class so that a fixed 2−ε approximate CCE works for nearby games, enabling a covering-number argument while staying computationally feasible.
- Joint policy is updated each step by computing a CCE of the n-player matrix game; the policy collects new interactive data and the design matrix Λ is updated via rank-one feature outer products.

## Theoretical Contributions
- **Online regret lower bound (Theorem 4.1)**: for two-player general-sum robust Markov games, inf_ALG sup_θ E[Regret] = Ω(σ·HK), proving impossibility of learning without further assumptions (support-shift hardness in MARL).
- **Instance-dependent upper bound (Theorem 5.1)**: high-probability regret bound for DR-CCE-LSI expressed via the self-normalized bonus sum.
- **Bonus-term hardness (Theorem 5.2)**: constructs a 3-state, 2-action, horizon-2 MDP where the bonus sum Σ √(ϕⱼ 1ⱼᵀ(Λᵏ)⁻¹1ⱼ ϕⱼ) is Ω(K), showing the term cannot be bounded without extra assumptions.
- **Sufficient condition (Corollary 5.3)**: under non-degenerate feature mapping, a lower-bounded feature covariance condition, and absolute continuity of P⁰, the regret is of order Õ(dH·min{H, 1/min{σᵢ}}·√K); this matches the single-agent rate (Liu, Wang, and Xu 2024) and is minimax optimal in d (the first such result for online robust linear function approximation).
- Supporting lemmas: shrinkage of robust value function (|Vᵖ,σ| ≤ min{1/σᵢ, H}), self-normalizing concentration, martingale-difference bounds, UCB, and covering-number bounds for the Q/V function classes.

## Experiments
- **Environment/Benchmark**: A constructed simulated two-player general-sum linear Markov game with 5 states (s0, s1, s2, sf, sn), horizon H = 3, where sf is a self-absorbing fail state satisfying the minimum value assumption; a parameter (ρ / rn) governs the chance of transitioning to the fail state, controlling sensitivity to environment perturbation. Results averaged over 100 seeds.
- **Baselines**: NQOVI (Cisneros-Velarde and Koyejo 2023), the state-of-the-art for non-robust online linear Markov games.
- **Evaluation metrics**: Average reward per player (and their average) under increasing uncertainty / perturbation sensitivity level.

## Key Results
- As the uncertainty level between the nominal and target Markov game increases, DR-CCE-LSI's performance is significantly better than NQOVI, validating its handling of the sim-to-real gap.
- In environments with low sensitivity to transition changes, DR-CCE-LSI underperforms NQOVI because it prioritizes robust over optimal policies; in perturbation-sensitive environments it significantly outperforms NQOVI.
- The regret bound Õ(dH·min{H, 1/min{σᵢ}}·√K) depends on maxᵢ{βᵢ}, implying that for best sample efficiency players should share a common risk-preference (uncertainty) level, since a single risk-seeking player (small σᵢ) can inflate the bound.

## Limitations & Future Work
- The upper bound is loose in the horizon length H relative to the information-theoretic lower bound Ω(dH^{1/2}·min{H,1/σ}·√K); closing this gap is left to future work.
- A natural fix (variance-weighted ridge regression, as used single-agent) is highly non-trivial in the Markov game setting because learning a monotonic value function — required by that framework — is not accessible in the multi-agent case.
- Relies on a vanishing minimal value assumption and centralized global linear function approximation; robustness in decentralized settings with independent linear function approximation remains an open and challenging problem.

## Relevance to Survey
A core theory contribution on the "distributionally robust MARL" line, bridging robust RL/robust MDP, online linear function approximation, and general-sum Markov game equilibrium learning. It sits at the intersection of the model/environment-uncertainty robustness theme and the sample-efficient (regret/sample-complexity) method line, extending single-agent online robust linear MDP results (Liu and Xu 2024; Liu, Wang, and Xu 2024) to multi-player general-sum games and complementing offline/generative-model robust MARL works (Blanchet et al. 2023; Shi et al. 2024a,b; Jiao and Li 2024). Directly builds on and cites foundational robust-MARL works (Kardeş, Ordóñez, and Hall 2011; Zhang et al. 2020).

## Related Work (verbatim excerpts from the paper)

> _[Section 2, Related work — "Robust online linear MDPs"]_

"The setting of online linear Markov Decision Processes (MDPs) (Yang and Wang 2019, 2020; Zanette et al. 2020; Jin et al. 2020; He, Zhou, and Gu 2021; He et al. 2023; Zhou, Gu, and Szepesvari 2021) has been extensively studied. The work of (He et al. 2023) achieved minimax optimality in this setting by incorporating variance-weighted ridge regression into their algorithm. In contrast, the study of online robust linear MDPs has only recently been explored in two works (Liu and Xu 2024; Liu, Wang, and Xu 2024). Specifically, (Liu, Wang, and Xu 2024) introduced a robust variant of variance-weighted ridge regression, achieving a regret bound of order O(dH min{1/σ, H}√K) under full data coverage assumption. However, this result still falls short of the constructed lower bound, which is of order Ω(dH^{1/2} min{1/σ, H}√K), highlighting that the single-agent counterpart of this setting remains insufficiently explored."

> _[Section 2, Related work — "Robust Markov game"]_

"While there has been extensive research on distributionally robust MDPs (Liu et al. 2022; Clavier, Pennec, and Geist 2023; Shi and Chi 2024; Shi et al. 2023; Wang et al. 2023a; Lu et al. 2024), the study of robust Markov games remains relatively underexplored. Existing works, such as (Kardeş, Ordóñez, and Hall 2011; Zhang et al. 2020), primarily focus on proving the existence of equilibria and analyzing convergence properties. In offline setting, a unified framework P2M2PO has been proposed by (Blanchet et al. 2023), with sample complexity of O(H⁵|S|²|A|²/ϵ). (Shi et al. 2024a,b; Jiao and Li 2024) extended this framework to generative model setting, where samples can be obtained from any state-action pair. In particular, (Jiao and Li 2024) proposed a Q-FTRL type algorithm, demonstrating that it is minimax optimal and breaking the curse of multi-agency with a sample complexity of O(H³|S| Σ^m_{i=1}|Aᵢ|/ε² min{H, 1/σ}). In the more realistic online setting, the work most relevant to ours is (Ma et al. 2023). However, their approach requires the uncertainty level σᵢ ≤ max{ε/(|S|H²), pmin/H} for all i ∈ [n]. This constraint limits the robustness of their framework, especially when high accuracy is required (ε → 0) or the minimum positive transition probabilities (pmin → 0)."

> _[Section 2, Related work — "Online linear Markov games"]_

"The study of sample complexity in online linear Markov games encompasses both centralized learning (Xie et al. 2020; Chen, Zhou, and Gu 2022; Cisneros-Velarde and Koyejo 2023), which employs global linear function approximation, and decentralized learning, which relies on independent linear function approximation (Cui, Zhang, and Du 2023; Wang et al. 2023b; Dai, Cui, and Du 2024). While decentralized learning is often more favorable in tabular Markov games due to its ability to alleviate the curse of multi-agency, extending this approach to linear function approximation requires adopting independent linear function approximation. However, this deviates from the linear MDP setting commonly used in single-agent reinforcement learning. Furthermore, addressing robustness in such decentralized settings remains an open and challenging problem."

> "In the context of centralized learning, (Xie et al. 2020; Chen, Zhou, and Gu 2022) focus on two-player zero-sum games, which are less general compared to the multi-player general-sum games considered in (Cisneros-Velarde and Koyejo 2023). The work in (Cisneros-Velarde and Koyejo 2023) introduced the NQOVI algorithm, achieving a regret bound of O(√(d³H⁵K)). Notably, the incorporation of robustness into online linear Markov games has not yet been studied, underscoring the significance of our work in addressing this gap."

> _[Introduction — "Robustness is essential"]_

"A critical challenge in reinforcement learning (RL) is the sim-to-real gap, characterized by discrepancies between simulated training environments and real-world deployment settings, which often result in degraded performance (Koos, Mouret, and Doncieux 2012; Jiang et al. 2021). This issue has motivated extensive research into distributionally robust reinforcement learning, where the objective is to develop policies that maintain robustness against variations in environmental dynamics (Iyengar 2005; Nilim and El Ghaoui 2005; Shi et al. 2023; Liu et al. 2022). The challenge is particularly pronounced in MARL, as highlighted by (Shi et al. 2024b), where the sensitivity of equilibrium solutions to minor environmental perturbations exacerbates the problem."

### Cited references (resolved from the paper's bibliography)
- **[Yang and Wang 2019]** Yang, Wang. *Sample-optimal parametric Q-learning using linearly additive features.* ICML 2019.
- **[Yang and Wang 2020]** Yang, Wang. *Reinforcement learning in feature space: Matrix bandit, kernels, and regret bound.* ICML 2020.
- **[Zanette et al. 2020]** Zanette, Brandfonbrener, Brunskill, Pirotta, Lazaric. *Frequentist regret bounds for randomized least-squares value iteration.* AISTATS 2020.
- **[Jin et al. 2020]** Jin, Yang, Wang, Jordan. *Provably efficient reinforcement learning with linear function approximation.* COLT 2020.
- **[He, Zhou, and Gu 2021]** He, Zhou, Gu. *Logarithmic regret for reinforcement learning with linear function approximation.* ICML 2021.
- **[He et al. 2023]** He, Zhao, Zhou, Gu. *Nearly minimax optimal reinforcement learning for linear Markov decision processes.* ICML 2023.
- **[Zhou, Gu, and Szepesvari 2021]** Zhou, Gu, Szepesvari. *Nearly minimax optimal reinforcement learning for linear mixture Markov decision processes.* COLT 2021.
- **[Liu and Xu 2024]** Liu, Xu. *Distributionally robust off-dynamics reinforcement learning: Provable efficiency with linear function approximation.* AISTATS 2024.
- **[Liu, Wang, and Xu 2024]** Liu, Wang, Xu. *Upper and Lower Bounds for Distributionally Robust Off-Dynamics Reinforcement Learning.* arXiv 2024 (arXiv:2409.20521).
- **[Liu et al. 2022]** Liu, Bai, Blanchet, Dong, Xu, Zhou, Zhou. *Distributionally Robust Q-Learning.* ICML 2022.
- **[Clavier, Pennec, and Geist 2023]** Clavier, Le Pennec, Geist. *Towards minimax optimality of model-based robust reinforcement learning.* arXiv 2023 (arXiv:2302.05372).
- **[Shi and Chi 2024]** Shi, Chi. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* JMLR 2024.
- **[Shi et al. 2023]** Shi, Li, Wei, Chen, Geist, Chi. *The Curious Price of Distributional Robustness in Reinforcement Learning with a Generative Model.* NeurIPS 2023.
- **[Wang et al. 2023a]** Wang, Si, Blanchet, Zhou. *A finite sample complexity bound for distributionally robust Q-learning.* AISTATS 2023.
- **[Lu et al. 2024]** Lu, Zhong, Zhang, Blanchet. *Distributionally Robust Reinforcement Learning with Interactive Data Collection: Fundamental Hardness and Near-Optimal Algorithm.* arXiv 2024 (arXiv:2404.03578).
- **[Kardeş, Ordóñez, and Hall 2011]** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **[Zhang et al. 2020]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Blanchet et al. 2023]** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* NeurIPS 2023.
- **[Shi et al. 2024a]** Shi, Gai, Mazumdar, Chi, Wierman. *Breaking the Curse of Multiagency in Robust Multi-Agent Reinforcement Learning.* arXiv 2024 (arXiv:2409.20067).
- **[Shi et al. 2024b]** Shi, Mazumdar, Chi, Wierman. *Sample-Efficient Robust Multi-Agent Reinforcement Learning in the Face of Environmental Uncertainty.* arXiv 2024 (arXiv:2404.18909).
- **[Jiao and Li 2024]** Jiao, Li. *Minimax-Optimal Multi-Agent Robust Reinforcement Learning.* arXiv 2024 (arXiv:2412.19873).
- **[Ma et al. 2023]** Ma, Chen, Zou, Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR 2023.
- **[Xie et al. 2020]** Xie, Chen, Wang, Yang. *Learning zero-sum simultaneous-move Markov games using function approximation and correlated equilibrium.* COLT 2020.
- **[Chen, Zhou, and Gu 2022]** Chen, Zhou, Gu. *Almost optimal algorithms for two-player zero-sum linear mixture Markov games.* ALT 2022.
- **[Cisneros-Velarde and Koyejo 2023]** Cisneros-Velarde, Koyejo. *Finite-sample guarantees for Nash Q-learning with linear function approximation.* UAI 2023.
- **[Cui, Zhang, and Du 2023]** Cui, Zhang, Du. *Breaking the curse of multiagents in a large state space: RL in Markov games with independent linear function approximation.* COLT 2023.
- **[Wang et al. 2023b]** Wang, Liu, Bai, Jin. *Breaking the curse of multiagency: Provably efficient decentralized multi-agent RL with function approximation.* COLT 2023.
- **[Dai, Cui, and Du 2024]** Dai, Cui, Du. *Refined sample complexity for Markov games with independent linear function approximation.* arXiv 2024 (arXiv:2402.07082).
- **[Koos, Mouret, and Doncieux 2012]** Koos, Mouret, Doncieux. *The transferability approach: Crossing the reality gap in evolutionary robotics.* IEEE Transactions on Evolutionary Computation, 2012.
- **[Jiang et al. 2021]** Jiang, Zhang, Ho, Bai, Liu, Levine, Tan. *SimGAN: Hybrid simulator identification for domain adaptation via adversarial reinforcement learning.* ICRA 2021.
- **[Iyengar 2005]** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **[Nilim and El Ghaoui 2005]** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 2005.
