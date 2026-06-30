# 14. Robust Mean-Field Games with Risk Aversion and Bounded Rationality

## Metadata
- **Title**: Robust Mean-Field Games with Risk Aversion and Bounded Rationality
- **Authors**: Bhavini Jeloka, Yue Guan, Panagiotis Tsiotras
- **Affiliation**: School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA, USA
- **Venue**: Not specified (arXiv preprint, 2026)
- **Link/arXiv**: arXiv:2602.13353v1 [cs.MA], 13 Feb 2026

## Taxonomy
- **Robustness / perturbation type targeted**: Distributional uncertainty in the initial population (mean-field) distribution; sensitivity of open-loop policies to unexpected/erroneous initial conditions; also models cognitive constraints (bounded rationality / deviations from full rationality).
- **Method paradigm**: Risk-sensitive / risk-averse optimization (convex risk measures with dual representation), mean-field games (MFG), quantal response equilibrium / convex regularization for bounded rationality, fixed-point iteration, fictitious play, actor-critic deep RL.
- **Keywords**: Mean-field games, risk aversion, bounded rationality, quantal response equilibrium, MF-RQE, distributional robustness

## TL;DR
The paper introduces a risk-averse mean-field game framework that combines risk aversion over a set of possible initial population distributions with bounded rationality (convex regularization), yielding a new equilibrium concept, the mean-field risk-averse quantal response equilibrium (MF-RQE), with existence/convergence guarantees and a scalable RL algorithm that produces policies robust to initial-distribution uncertainty.

## Problem & Motivation
Classical mean-field games (MFGs) reduce large-scale multi-agent problems to a representative agent interacting with the population mean-field, but rely on strong assumptions: a fixed initial population distribution, perfect rationality, and risk neutrality. In practice, agents operate across varying initial distributions; since MFE policies are open-loop with respect to the mean-field (avoiding costly/unreliable real-time population feedback), a policy optimized for one initial distribution can perform poorly under a different, "unexpected" initial condition, and recomputing policies for each condition is computationally infeasible and would require real-time mean-field information. Moreover, expectation-based objectives ignore rare-but-high-impact events (e.g., a small persistent infected population in an epidemic model), and perfect rationality is rarely realistic since agents exhibit errors, biases, and systematic deviations. The paper addresses these gaps by jointly incorporating risk aversion over initial distributions and bounded rationality into the mean-field framework.

## Robustness Setting
- **Threat model / uncertainty set**: A finite set M of possible initial mean-field distributions with an underlying probability distribution Γ*_M ∈ P(M). Uncertainty in the realized initial condition is hedged via a convex risk measure (KL-penalized worst case), interpreted as fictitious adversaries that maximize the agents' cost at each time step and state but are penalized (by KL-divergence) for deviating from the realized initial distribution Γ*_M; as the risk parameter τ → ∞ the initial-distribution selection becomes entirely adversarial. Robustness is sought within the class of policies that are open-loop w.r.t. the mean-field (no real-time MF feedback).
- **Setting**: Non-cooperative mean-field game (large-population limit), decentralized identical open-loop policies; finite-horizon, discrete-time, finite state–action spaces; both model-based (known dynamics/rewards) and model-free / sample-based (deep RL).

## Method
- Formulate a Risk-Averse Quantal Response Mean-Field Game (RQ-MFG) specified by the tuple ⟨X, U, T, f, r, ν, M, Γ*_M, D⟩, where (M, Γ*_M, D) capture risk aversion over the initial MF distribution and ν is a convex regularizer capturing bounded rationality.
- Define a per-time-step, per-state risk-averse objective cπ_t(x; S_M) = ρ_{Γ*_M}(V^π_{µ,t}(x)) using a convex risk measure; via the Dual Representation Theorem this becomes a sup over adversarial distributions penalized by D, and with a KL penalty admits a closed-form log-sum-exp aggregation over the |M| initial distributions. Adding the convex regularizer αν(π_t(·|x)) gives the combined boundedly rational objective (Eq. 8).
- Introduce the solution concept MF-RQE as a consistent pair (π*_RQE, S*_M) where the policy is the risk-averse quantal best response to the induced set of mean-field flows and the flows are propagated from π*_RQE (operators B^RQE_opt and B^RQE_prop).
- Solve MF-RQE under known dynamics with Risk-Averse Quantal Fixed-Point Iteration (RQ-FPI, via dynamic programming) and Risk-Averse Quantal Fictitious Play (RQ-Fictitious Play, via policy averaging).
- For large/unknown environments, propose Deep Risk-Averse Quantal Fixed-Point Iteration (D-RQ-FPI), a model-free actor-critic method maintaining |M| critics (one per initial distribution µ^k_0) trained with a TD loss, plus a time-dependent actor optimized to solve the risk-averse quantal response objective.

## Theoretical Contributions
- Existence of an MF-RQE (Proposition 1), established via Kakutani's fixed-point theorem (Appendix C).
- Finite-population guarantee (Theorem 2): an MF-RQE policy played by all N agents is an ϵ-RQE in the finite N-agent game with ϵ = O(1/√N), overcoming the curse of dimensionality identified for finite-agent RQE.
- Convergence of fixed-point iteration to an MF-RQE for sufficiently large α (Theorem 3), via showing Φ = B^RQE_opt ∘ B^RQE_prop is a contraction (Lipschitz operators, Banach fixed-point theorem; uses m-strong convexity of ν, Assumption 3).
- Convergence of RQ-Fictitious Play to an MF-RQE for sufficiently large α (Theorem 4).
- Supporting results: dual representation of convex risk measures (Theorem 1), continuity/Lipschitz properties of the Q-function and cost (Lemmas 2, 5–7).

## Experiments
- **Environment/Benchmark**: Benchmark environments from MFGLib, including the epidemiological SIS game and a newly proposed one-dimensional Congestion game; additional environments (Beach Bar, Conservative Treasure Hunting, Linear Quadratic, Random Linear, Rock–Paper–Scissors).
- **Baselines**: (i) entropy-regularized Nash equilibrium (NE) policies computed under a single initial distribution and evaluated under the risk-averse objective over M; (ii) a risk-neutral policy π*_avg that maximizes expected cumulative reward averaged over initial distributions; and per-initial-distribution optimal policies π*_{µ^k_0}.
- **Evaluation metrics**: An exploitability-like metric ∆c(π) (Eq. 10) measuring sensitivity to adverse realizations of the initial distribution; expected/average returns (over 10,000 episodes, five random seeds, under optimal MF flows S*_M); and the distance d_S(S^{RQ-FPI}_M, S^{D-RQ-FPI}_M) between empirical and analytical mean-field flows for the deep RL setting.

## Key Results
- The RQ-FPI MF-RQE policy is non-exploitable (∆c(π*_RQE) = 0.00) across SIS and Congestion games, whereas risk-neutral / single-initial-distribution policies are exploitable under initial-distribution uncertainty; RQ-Fictitious Play recovers the same policies as RQ-FPI.
- Robustness comes at the cost of only a modest reduction in expected returns; e.g., in SIS the per-distribution policy π*_{µ^1_0} attains higher expected return (−22.003) but ∆c = 0.090, while π*_RQE attains −22.165 with ∆c = 0.00 (empirical return differences across policies remain relatively small).
- D-RQ-FPI converges with sampling noise: empirical exploitability falls below 10^−2 (SIS) and to order 10^−4 (Congestion), with d_S ≈ 10^−3 (and < 10^−3 for Congestion), consistent with magnitudes reported in standard MFGs.
- The framework extends beyond entropy regularization (validated with a log-barrier regularizer); ablations without convex regularization show neither tractability nor convergence to an MF-RQE can be guaranteed, highlighting the critical role of bounded rationality.

## Limitations & Future Work
- Restricts to a finite set M of initial distributions; extending the framework to continuous and compact sets M is left for future work.
- Theoretical guarantees require m-strong convexity of ν (Assumption 3) and a "sufficiently large α"; the authors note empirically that algorithms still perform well under weaker conditions (strict convexity).
- Finite-sample stochasticity in the deep RL setting prevents exploitability from converging exactly to zero.
- Future work: extend to heterogeneous and team-based mean-field settings, where risk aversion may arise with respect to adversarial populations.

## Relevance to Survey
This paper sits on the "distributional / environment-uncertainty" line of robust (multi-agent) RL, specialized to the mean-field large-population regime. It combines distributionally-robust / risk-sensitive optimization (convex risk measures with an adversarial dual representation over initial distributions) with a bounded-rationality / quantal-response equilibrium formulation, connecting robust MARL to behavioral-economics-inspired solution concepts (RQE) and to mean-field game theory. The adversarial interpretation of risk aversion (fictitious adversaries selecting worst-case initial distributions, KL-penalized) links it to minimax / worst-case robust RL, while the open-loop, decentralized, scalable design connects it to CTDE-style robustness for large populations.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — preamble]_

"Risk aversion and bounded rationality have largely been studied in isolation—through risk-averse and quantal response equilibria, respectively—with growing adoption in MARL and learning theory; see Mazumdar et al. [2025] and references therein for Markov games. We focus on related work that examines their integration with MFGs."

> _[Section 2, Related Work — "Risk Analysis in MFGs"]_

"Risk Analysis in MFGs. Risk-sensitive mean-field games have been studied in both continuous and discrete-time settings. Continuous-time analyses [Moon and Bas¸ar, 2014; Tembine et al., 2013; Tembine, 2015; Perrin et al., 2020] typically rely on common-noise formulations and differ fundamentally from the finite-horizon, discrete-time framework considered here. In discrete time, prior work [Saldi et al., 2020; Cheng and Jaimungal, 2023; Bonnans et al., 2021] often assumes Polish state–action spaces or linear feedback control, whereas our finite state–action formulation admits a standard MDP structure with explicit dynamics and does not require real-time mean-field feedback, enabling scalability with large state-action spaces. While our approach is related to exponential utility-based risk-sensitive formulations [Saldi et al., 2020], our framework—unlike theirs—accounts for uncertainty in the mean-field flow itself, induced by uncertainty in the initial distribution, yielding a log-sum-exp aggregation over multiple initial distributions. Finally, all existing risk-sensitive MFG frameworks predominantly rely on Nash equilibrium as the solution concept and do not account for deviations from perfect rationality."

> _[Section 2, Related Work — "Bounded Rationality in MFGs"]_

"Bounded Rationality in MFGs. In MFGs, bounded rationality has primarily appeared through entropy regularization to compute approximate Nash equilibria [Cui and Koeppl, 2022; Guan et al., 2022], and was explicitly interpreted as bounded rationality in Eich et al. [2025], where the authors analyzed a stochastically perturbed mean-field game and computed the resulting mean-field quantal response equilibria (QRE). Under suitable assumptions, Eich et al. [2025] show that bounded rationality yields both more realistic agent behavior and computational advantages, as the resulting QRE can be computed via fixed-point iteration and, under specific noise assumptions, reduces to an entropy-regularized MFG. Building on these insights, we model bounded rationality in MFGs using a general class of convex regularizers, enabling richer behavioral representations beyond entropy regularization while retaining computational tractability. Moreover, unlike Eich et al. [2025], we explicitly incorporate risk aversion into the boundedly rational mean-field framework, thereby capturing agents' preferences for the initial population distribution."

> _[Section 2, Related Work — "Impact of Initial Distributions"]_

"Impact of Initial Distributions. Mean-field games under uncertainty in the initial distribution remain relatively underexplored, with limited theory and few design methodologies offering performance guarantees under risk aversion or modeling error. Jin et al. [2025] propose an initial-error-tolerant distributed mean-field control (IET-DMFC) framework, but it is limited to linear–quadratic models and does not incorporate risk preferences. Cui et al. [2023] empirically study sensitivity to initial conditions in the MFC regime using open-loop policies learned via Dec-POMFPPO, but do not provide theoretical robustness guarantees."

> _[Introduction — on the originating risk-averse equilibrium concept]_

"The recent work of Mazumdar et al. [2025] introduced the risk-averse quantal response equilibrium (RQE) for finite-agent Markov games, but suffers from the curse of dimensionality. To address the shortcomings associated with large population regimes, in this work we introduce a risk-averse MFG framework that explicitly accounts for uncertainty in initial population distributions and deviations from perfect rationality. We formulate the problem as a convex risk-averse optimization problem and introduce a new solution concept, the mean-field risk-averse quantal response equilibrium (MF-RQE)."

### Cited references (resolved from the paper's bibliography)
- **[Mazumdar et al., 2025]** Mazumdar, Panaganti, Shi. *Tractable multi-agent reinforcement learning through behavioral economics.* ICLR (The Thirteenth International Conference on Learning Representations) 2025.
- **[Moon and Bas¸ar, 2014]** Moon, Başar. *Linear-quadratic risk-sensitive mean field games.* 53rd IEEE Conference on Decision and Control (CDC) 2014.
- **[Tembine et al., 2013]** Tembine, Zhu, Başar. *Risk-sensitive mean-field games.* IEEE Transactions on Automatic Control, 2013.
- **[Tembine, 2015]** Tembine. *Risk-sensitive mean-field-type games with lp-norm drifts.* Automatica, 2015.
- **[Perrin et al., 2020]** Perrin, Pérolat, Laurière, Geist, Elie, Pietquin. *Fictitious play for mean field games: Continuous time analysis and applications.* NeurIPS 2020.
- **[Saldi et al., 2020]** Saldi, Başar, Raginsky. *Approximate Markov-Nash equilibria for discrete-time risk-sensitive mean-field games.* Mathematics of Operations Research, 2020.
- **[Cheng and Jaimungal, 2023]** Cheng, Jaimungal. *Risk-averse mean field games: exploitability and non-asymptotic analysis.* arXiv preprint arXiv:2301.06930, 2023.
- **[Bonnans et al., 2021]** Bonnans, Lavigne, Pfeiffer. *Discrete-time mean field games with risk-averse agents.* ESAIM: Control, Optimisation and Calculus of Variations, 2021.
- **[Cui and Koeppl, 2022]** Cui, Koeppl. *Approximately solving mean field games via entropy-regularized deep reinforcement learning.* 2022.
- **[Guan et al., 2022]** Guan, Zhou, Pakniyat, Tsiotras. *Shaping large population agent behaviors through entropy-regularized mean-field games.* American Control Conference (ACC) 2022.
- **[Eich et al., 2025]** Eich, Fabian, Cui, Koeppl. *Bounded rationality equilibrium learning in mean field games.* AAAI Conference on Artificial Intelligence 2025.
- **[Jin et al., 2025]** Jin, Wang, Yao, Zhang. *Initial error tolerant distributed mean field control under partial and discrete information.* 2025.
- **[Cui et al., 2023]** Cui, Hauck, Fabian, Koeppl. *Learning decentralized partially observable mean field control for artificial collective behavior.* arXiv preprint arXiv:2307.06175, 2023.
