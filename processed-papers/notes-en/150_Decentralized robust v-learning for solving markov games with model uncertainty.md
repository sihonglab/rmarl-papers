# 150. Decentralized Robust V-learning for Solving Markov Games with Model Uncertainty

## Metadata
- **Title**: Decentralized Robust V-learning for Solving Markov Games with Model Uncertainty
- **Authors**: Shaocong Ma, Ziyi Chen, Shaofeng Zou, Yi Zhou
- **Affiliation**: University of Utah (ECE); University at Buffalo, SUNY (EE)
- **Venue**: Journal of Machine Learning Research (JMLR) 24, 2023
- **Link/arXiv**: http://jmlr.org/papers/v24/23-0310.html

## Taxonomy
- **Robustness / perturbation type targeted**: Environment model uncertainty (uncertain transition kernel queried from an uncertainty set; sim-to-real / model mismatch gap)
- **Method paradigm**: Robust Markov game theory, robust correlated equilibrium, decentralized V-learning, robust TD learning, worst-case (minimax) value function, distributionally robust (KL / R-contamination uncertainty sets)
- **Keywords**: robust Markov games, model uncertainty, robust correlated equilibrium, V-learning, decentralized RL, sample complexity

## TL;DR
The paper proposes a new tractable notion of robust correlated equilibrium (robust CE) for general-sum Markov games with environment model uncertainty and develops the first fully decentralized, polynomial-complexity stochastic algorithm (decentralized robust V-learning) that provably computes an ε-approximate robust CE with episode complexity Õ(SA²H⁵ε⁻²).

## Problem & Motivation
Standard Markov games model only the competition among players but ignore environment model uncertainty, which is ubiquitous in practice (real-world noise, sensor errors, dynamic changes, and the sim-to-real gap where simulator-trained policies degrade in the real environment). Computing robust Nash equilibria (NE) of general-sum Markov games with model uncertainty is in general a PPAD-complete problem, so it is unknown whether polynomial-time algorithms exist; prior robust MARL work (Kardeş et al., 2011; Zhang et al., 2020) either lacks an explicit analytical form or gives only asymptotic convergence to robust NE. Motivated by the success of tractable surrogate notions (CE, CCE) in the non-robust setting, the authors observe that a robust version of correlated equilibria has not been studied, and aim to (i) propose a tractable robust equilibrium notion with its fundamental properties, and (ii) construct a fully decentralized, provably convergent, polynomial-complexity algorithm to compute it.

## Robustness Setting
- **Threat model / uncertainty set**: At every time step h and every state-action pair (s, a), the transition kernel P̃ₕ(·|s,a) is uncertain and belongs to a general uncertainty set Pₕ(s,a). Concrete examples: KL-divergence ball (dKL(P, P̃) ≤ ρ) and R-contamination model ((1−R)P + Rq, q ∈ Δ|S|). The robust value function is the worst-case (infimum over the product uncertainty set P) expected cumulative reward; each player's worst-case (adversarial) transition kernel may differ. The uncertainty diameter D characterizes the level of uncertainty.
- **Setting**: competitive / general-sum episodic m-player Markov game; fully decentralized (each player keeps its own value tables and runs an adversarial-bandit actor update with no coordination); online / model-free (sample-based estimator of the worst-case operator).

## Method
- Defines a **robust value function** V⁽ʲ⁾_{π,h}(s) = inf_{P̃∈P} E[Σ rℓ | π, P̃], i.e., the worst-case expected total reward over the uncertainty set, and uses it to define **robust NE** and the surrogate **robust CE** (no player can improve its robust value via a stochastic modification φ⁽ʲ⁾ of its own actions).
- Establishes structural properties: robust CE can be characterized via deterministic modifications (Proposition 7), any robust NE is a robust CE (Proposition 8.1), and the robust CE set can strictly include the robust NE set, depending critically on the uncertainty set (Proposition 8.2).
- **Decentralized robust V-learning** (Algorithm 1) with a critic step and an actor step. Critic: a robust TD-learning update where the standard expected next-state value is replaced by the worst-case operator σ_{Pₕ(s,a)}(V) = inf_{P̃∈Pₕ(s,a)} ⟨P̃, V⟩, solved via a one-dimensional convex program (KL case) or a closed-form sample estimator (R-contamination case), followed by an upper truncation to H+1−h.
- Actor: each player feeds the adversarial loss 1 − (rₕ + σ̂(V))/H into the V-learning adversarial-bandit subroutine (ADV_BANDIT, from Jin et al. 2022a) to update its policy; the final output is a non-Markov policy produced by random episode resampling (Algorithm 2).
- Optimality is measured by an optimality gap (max over players and states of V_{φ*∘π} − V_π); convergence is established under conditions on the uncertainty diameter D relative to ε and the state-exploration probability p_min, using a stronger convergence metric and an upper-triangular Toeplitz linear system.

## Theoretical Contributions
- **New equilibrium notion**: robust correlated equilibrium for Markov games with model uncertainty, with its modification structure (Proposition 7) and its relation to robust NE (Proposition 8); single-agent reduction (Proposition 10).
- **First non-asymptotic convergence result** for solving Markov games with model uncertainty: under low uncertainty (D ≤ ε/(SH²)), episode complexity Õ(SA²H⁵ε⁻²) (Theorem 12); under sufficient exploration with higher uncertainty (ε/(SH²) ≤ D < p_min/H), complexity Õ(SA²H⁵p_min⁻²ε⁻²) (Theorem 13).
- **Novel analysis techniques**: properties of the worst-case operator σ (boundedness, monotonicity, L1-Lipschitzness — Lemmas 19, 25), a decomposition that introduces a stronger convergence metric Δ⁽ʲ⁾_{k,h}, and solving the resulting recursion via the spectrum of an upper-triangular Toeplitz matrix (Lemmas 26, 27).

## Experiments
- **Environment/Benchmark**: Not specified (the paper is theoretical; it gives an illustrative two-player coordination game with five states, parameterized transition Pₕ,p, to demonstrate Proposition 8, but reports no learning-curve / benchmark experiments).
- **Baselines**: Not specified
- **Evaluation metrics**: Not specified (theoretical optimality gap / episode complexity used in the analysis)

## Key Results
- Robust CE inherits the deterministic-modification structure of standard CE, and the characterization of equilibria critically depends on the uncertainty set; an illustrative example shows that for some uncertainty sets the set of robust CE strictly includes the set of robust NE (e.g., p ∈ (10/29, 1/2) yields two robust NE whose convex combinations are robust CE but not robust NE).
- Decentralized robust V-learning achieves Õ(SA²H⁵ε⁻²) episode complexity for an ε-approximate robust CE when D ≤ ε/(SH²) (Theorem 12), the first such polynomial guarantee for Markov games with model uncertainty.
- With sufficient exploration (p_min > ε/(SH)) the diameter requirement is relaxed from ε/(SH²) to p_min/H, at the cost of complexity Õ(SA²H⁵p_min⁻²ε⁻²) (Theorem 13).
- The algorithm cannot guarantee ε-accuracy when the uncertainty diameter D is too large relative to p_min and ε; the uncertainty set cannot be arbitrarily large.

## Limitations & Future Work
- Convergence/ε-accuracy holds only under an upper bound on the uncertainty diameter D (relative to p_min and ε); the uncertainty set cannot be arbitrarily large.
- The analysis is theoretical; no empirical/benchmark evaluation is reported.
- Future work: explore whether convergence can be established under relaxed requirements on the uncertainty diameter.

## Relevance to Survey
This is a core theory paper in the "environment/model uncertainty" line of robust MARL, directly extending the robust Markov game framework of Zhang et al. (2020) and Kardeş et al. (2011). Its distinctive contribution is bringing the tractable correlated-equilibrium notion (and decentralized V-learning) from non-robust Markov games into the robust/model-uncertainty regime, providing the first non-asymptotic, polynomial sample-complexity result for solving general-sum Markov games with model uncertainty. It connects the robust-MDP / robust RL line (KL and R-contamination uncertainty sets, robust TD updates) with the decentralized multi-agent equilibrium-computation line (V-learning, adversarial bandits, CE/CCE), making it a key reference for the intersection of distributionally robust RL and scalable, decentralized MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.2, Related Work — "Markov games"]_

"Markov games, also known as stochastic games, are standard formalism in multi-agent RL (Littman, 1994). The existence of NE for multi-player general-sum Markov games has been established in Fink (1964). Various algorithms have been designed to find NE, such as Nash-Q learning (Hu and Wellman, 2003), FF-Q learning (Littman et al., 2001), and correlated-Q learning (Greenwald et al., 2003). The first polynomial-time algorithm for finding NE is developed in Hansen et al. (2013), but works only for zero-sum games. Recent studies showed that finding NE of general-sum multi-player games is PPAD-complete (Daskalakis, 2013), so there are currently no polynomial-time algorithms for solving them (Deng et al., 2021; Jin et al., 2022b). Another notable goal in Markov games is to find a weaker version of NE, such as the correlated equilibrium (CE) or coarse correlated equilibrium (CCE). Polynomial-time algorithms such as V-learning (Jin et al., 2022a; Mao and Başar, 2022; Song et al., 2021) and Nash value iteration (Liu et al., 2021) have been developed for computing these notions."

> _[Section 1.2, Related Work — "Robust reinforcement learning"]_

"Single-agent robust reinforcement learning has been widely explored (Nilim and Ghaoui, 2003; Nilim and El Ghaoui, 2005; Wiesemann et al., 2013; Satia and Lave Jr, 1973), which assume the environment transition kernel belongs to a given uncertainty set. Under a specific uncertainty model, Roy et al. (2017) and Wang and Zou (2021) developed model-free online robust Q-learning algorithms to solve the robust reinforcement learning problem. For robust multi-agent reinforcement learning, value iteration-based algorithm has been developed in Kardeş et al. (2011) but with no explicit analytical form. For cooperative multi-agent reinforcement learning with model uncertainty, Huang et al. (2021) proposed a robust policy iteration algorithm to maximize the gain of the whole group. For non-cooperative Markov games with model uncertainty, Zhang et al. (2020) introduced robust Q-learning and actor-critic algorithms with asymptotic convergence guarantees of finding robust NE. To the best of our knowledge, there is no existing polynomial-time algorithm for solving Markov games with model uncertainty."

> _[Section 1.2, Related Work — "Existence of Nash equilibria"]_

"The existence of Nash equilibria for the discounted stochastic games is provided by Fink (1964), which also implies the existence of correlated equilibria and coarse correlated equilibria. Though the existence of robust Nash equilibria doesn't hold in general, it is ensured under some mild regularity assumptions (Perchet, 2014, 2020; Kardeş et al., 2011)."

> _[Section 1, Introduction — model uncertainty motivation]_

"To address model uncertainty, numerous robust reinforcement learning approaches have been developed and extensively studied in the single-agent case (Wang and Zou, 2021; Li et al., 2022b,a; Neufeld and Sester, 2022). However, model uncertainty is still underexplored in the general case with multiple competing agents, where only two works (Kardeş et al., 2011; Zhang et al., 2020) exist to our knowledge. Specifically, Kardeş et al. (2011) applied the robust Markov game with model uncertainty to the application of queueing control. Zhang et al. (2020) proposed provably convergent Q-learning and actor-critic type algorithms to compute a certain robust variant of NE of robust Markov games. However, computing robust NE of general Markov games with model uncertainty is in general a PPAD-complete problem and therefore it remains open if any polynomial-time algorithms exist."

### Cited references (resolved from the paper's bibliography)
- **[Littman, 1994]** Michael L. Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994 (Elsevier), pp. 157–163.
- **[Fink, 1964]** Arlington M. Fink. *Equilibrium in a stochastic n-person game.* Journal of Science of the Hiroshima University, Series A-I (Mathematics), 28(1):89–93, 1964.
- **[Hu and Wellman, 2003]** Junling Hu, Michael P. Wellman. *Nash Q-learning for general-sum stochastic games.* Journal of Machine Learning Research, 4(Nov):1039–1069, 2003.
- **[Littman et al., 2001]** Michael L. Littman et al. *Friend-or-foe Q-learning in general-sum games.* ICML 2001, vol. 1, pp. 322–328.
- **[Greenwald et al., 2003]** Amy Greenwald, Keith Hall, Roberto Serrano, et al. *Correlated Q-learning.* ICML 2003, vol. 3, pp. 242–249.
- **[Hansen et al., 2013]** Thomas Dueholm Hansen, Peter Bro Miltersen, Uri Zwick. *Strategy iteration is strongly polynomial for 2-player turn-based stochastic games with a constant discount factor.* Journal of the ACM, 60(1):1–16, 2013.
- **[Daskalakis, 2013]** Constantinos Daskalakis. *On the complexity of approximating a Nash equilibrium.* ACM Transactions on Algorithms (TALG), 9(3):1–35, 2013.
- **[Deng et al., 2021]** Xiaotie Deng, Yuhao Li, David Henry Mguni, Jun Wang, Yaodong Yang. *On the complexity of computing Markov perfect equilibrium in general-sum stochastic games.* arXiv:2109.01795, 2021.
- **[Jin et al., 2022a]** Chi Jin, Qinghua Liu, Yuanhao Wang, Tiancheng Yu. *V-learning — a simple, efficient, decentralized algorithm for multiagent RL.* ICLR 2022 Workshop on Gamification and Multiagent Solutions, 2022.
- **[Jin et al., 2022b]** Yujia Jin, Vidya Muthukumar, Aaron Sidford. *The complexity of infinite-horizon general-sum stochastic games.* arXiv:2204.04186, 2022.
- **[Mao and Başar, 2022]** Weichao Mao, Tamer Başar. *Provably efficient reinforcement learning in decentralized general-sum Markov games.* Dynamic Games and Applications, pp. 1–22, 2022.
- **[Song et al., 2021]** Ziang Song, Song Mei, Yu Bai. *When can we learn general-sum Markov games with a large number of players sample-efficiently?* arXiv:2110.04184, 2021.
- **[Liu et al., 2021]** Qinghua Liu, Tiancheng Yu, Yu Bai, Chi Jin. *A sharp analysis of model-based reinforcement learning with self-play.* ICML 2021, pp. 7001–7010 (PMLR).
- **[Nilim and Ghaoui, 2003]** Arnab Nilim, Laurent Ghaoui. *Robustness in Markov decision problems with uncertain transition matrices.* NeurIPS 16, 2003.
- **[Nilim and El Ghaoui, 2005]** Arnab Nilim, Laurent El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 53(5):780–798, 2005.
- **[Wiesemann et al., 2013]** Wolfram Wiesemann, Daniel Kuhn, Berç Rustem. *Robust Markov decision processes.* Mathematics of Operations Research, 38(1):153–183, 2013.
- **[Satia and Lave Jr, 1973]** Jay K. Satia, Roy E. Lave Jr. *Markovian decision processes with uncertain transition probabilities.* Operations Research, 21(3):728–740, 1973.
- **[Roy et al., 2017]** Aurko Roy, Huan Xu, Sebastian Pokutta. *Reinforcement learning under model mismatch.* NeurIPS 30, 2017.
- **[Wang and Zou, 2021]** Yue Wang, Shaofeng Zou. *Online robust reinforcement learning with model uncertainty.* NeurIPS 34:7193–7206, 2021.
- **[Kardeş et al., 2011]** Erim Kardeş, Fernando Ordóñez, Randolph W. Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 59(2):365–382, 2011.
- **[Huang et al., 2021]** Feng Huang, Ming Cao, Long Wang. *Optimal control of robust team stochastic games.* arXiv:2105.07405, 2021.
- **[Zhang et al., 2020]** Kaiqing Zhang, Tao Sun, Yunzhe Tao, Sahika Genc, Sunil Mallya, Tamer Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 33:10571–10583, 2020.
- **[Perchet, 2014]** Vianney Perchet. *A note on robust Nash equilibria with uncertainties.* RAIRO-Operations Research, 48(3):365–371, 2014.
- **[Perchet, 2020]** Vianney Perchet. *Finding robust Nash equilibria.* Algorithmic Learning Theory (ALT), pp. 725–751 (PMLR), 2020.
- **[Li et al., 2022a]** Jialian Li, Tongzheng Ren, Dong Yan, Hang Su, Jun Zhu. *Policy learning for robust Markov decision process with a mismatched generative model.* arXiv:2203.06587, 2022.
- **[Li et al., 2022b]** Yan Li, Tuo Zhao, Guanghui Lan. *First-order policy optimization for robust Markov decision process.* arXiv:2209.10579, 2022.
- **[Neufeld and Sester, 2022]** Ariel Neufeld, Julian Sester. *Robust Q-learning algorithm for Markov decision processes under Wasserstein uncertainty.* arXiv:2210.00898, 2022.
