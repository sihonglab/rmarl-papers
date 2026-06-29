# 4. Taming the Curses of Multiagency in Robust Markov Games with Large State Space through Linear Function Approximation

## Metadata
- **Title**: Taming the Curses of Multiagency in Robust Markov Games with Large State Space through Linear Function Approximation
- **Authors**: Jingchu Gai, Laixi Shi
- **Affiliation**: Carnegie Mellon University (Gai); Johns Hopkins University (Shi)
- **Venue**: arXiv preprint arXiv:2605.03125v2 (2026)
- **Link/arXiv**: arXiv:2605.03125v2

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental uncertainty (sim-to-real gap, dynamics shift); distributionally robust with fictitious TV uncertainty sets under per-agent (s,ai)-rectangularity
- **Method paradigm**: Linear function approximation (LFA), fictitious uncertainty sets; L-Robust-Q-FTRL (generative model) and Online-L-Robust-Q-FTRL (online interactive); breaks curse of multiagency for RMGs with infinite/large state spaces
- **Keywords**: Linear function approximation, robust linear Markov games (R-LMGs), fictitious uncertainty sets, L-Robust-Q-FTRL, curse of multiagency, ridge regression, hybrid sampling, online interactive protocol

## TL;DR
First provably sample-efficient algorithms for distributionally robust Markov games (RMGs) with large-scale (possibly infinite) state spaces using per-agent independent linear function approximation (LFA); breaks the curse of multiagency in both the generative model setting (sample complexity Õ(H⁹d³/ε⁴)) and a new online interactive setting (regret Õ(d·max_i A_i·H²√T)).

## Problem & Motivation
Current provably data-efficient algorithms for RMGs are confined to tabular finite-state-action settings, which are computationally intractable for large or continuous state spaces prevalent in real-world applications (robotics, autonomous driving, energy systems). The only prior work extending beyond tabular RMGs [Zheng and Lin, 2025] uses centralized LFA, requires a vanishing minimal value assumption, and still suffers from the curse of multiagency (sample complexity scales as ΠA_i). The paper addresses the open question: Can the curse of multiagency be tamed in robust Markov games with large-scale state spaces?

## Robustness Setting
- **Threat model / uncertainty set**: Fictitious TV uncertainty sets (from Shi et al. 2024b). For each agent i, the uncertainty set U^σi(P^0, π) = ⊗ U^σi(P^{π_{-i}}_{h,s,ai}), where P^{π_{-i}}_{h,s,ai} is the nominal transition marginalized over others' policies at (s,ai,h). The radius σi ≥ 0 controls agent i's uncertainty. This is (s,ai)-rectangular (fictitious), not (s,a)-rectangular.
- **Setting**: n-player finite-horizon general-sum Markov games; large-scale (possibly infinite) state spaces; per-agent independent LFA with feature dimension d; solution concept: ε-approximate robust CCE; generative model setting and online interactive setting.

## Method
**L-Robust-Q-FTRL (generative model, Algorithm 3):**
- Uses an infinite-to-finite reduction (Lemma 1): constructs a finite support set Y_i ⊂ S×A_i of size ≤ d(d+1)/2 for each agent i, enabling feasible sampling over the (possibly infinite) state space.
- Queries the generative model to collect N samples per (s,ai) pair in Y_i; estimates nominal transitions and rewards via ridge regression.
- Runs a K-iteration backward FTRL procedure over h=H,...,1: estimates robust Q-functions using the dual form of the robust Bellman equation with TV distance, adds bonus terms β_{i,h}, and updates policies via FTRL.

**Online-L-Robust-Q-FTRL (online interactive, Algorithm 2):**
- Introduces a new online interactive protocol: agents can sample from transition kernels within the uncertainty set (approximate adversarial environment), not just the nominal kernel.
- Hybrid-Sampling (Algorithm 1): for each episode t and step h, rolls out approximate worst-case trajectories using pessimistic robust value estimates {V^l_j} for the first h-1 steps, then samples from the nominal kernel at step h. This allows nominal model estimation while preserving the adversarial occupancy distribution.
- Maintains both optimistic and pessimistic estimates of the robust value function; uses FTRL for policy updates.
- The pessimistic estimates approximate the adversarial environment without knowing the ground-truth robust value function.

Both algorithms exploit independent per-agent LFA (feature ϕ_i : S×A_i → R^d per agent), which avoids the curse of multiagency by not requiring joint state-action enumeration.

## Theoretical Contributions
- **Theorem 1 (Existence)**: Robust NE and robust CCE exist for R-LMGs with fictitious uncertainty sets (extends Shi et al. 2024b to infinite state spaces via Glicksberg's fixed-point theorem).
- **Theorem 2 (L-Robust-Q-FTRL, generative model)**: Given N ≥ CH⁴d³/ε² and K ≥ CH⁴/ε², the algorithm outputs an ε-robust CCE w.p. ≥ 1−δ. Total samples: Ñ_all = Õ(H⁹d³/ε⁴). In tabular reduction (d = S·max_i A_i): Õ(H⁹S³(max_i A_i)³/ε⁴), polynomial in all parameters.
- **Theorem 3 (Online-L-Robust-Q-FTRL, online)**: With N=K=T, regret ≤ Õ(H²d·max_i A_i·√T). Outputs ε-CCE if T > H⁴d²(max_i A_i)²/ε². In tabular reduction: regret Õ(H²S(max_i A_i)²√T) — breaks curse of multiagency (ΣA_i scaling vs. ΠA_i in [Zheng and Lin, 2025]).
- First algorithms breaking the curse of multiagency for large/infinite-state RMGs in either setting.

## Experiments
Not applicable — purely theoretical paper.

## Key Results
- Generative model: Õ(H⁹d³/ε⁴) samples, breaking curse of multiagency (no ΠA_i dependence).
- Online interactive: Õ(d·max_i A_i·H²√T) regret, breaking curse of multiagency.
- Strictly improves upon prior robust linear MG work [Zheng and Lin, 2025] which requires the vanishing minimal value assumption and still suffers from ΠA_i scaling.
- Introduces the first practically motivated online interaction protocol for RMGs (agents sample from adversarial environments within the uncertainty set) that is also provably well-posed for sublinear regret.

## Limitations & Future Work
- H and ε dependencies have gaps vs. tabular lower bounds (Theorem 2 gives ε⁴ vs. conjectured ε² optimal).
- Specific to TV distance and fictitious uncertainty sets; extensions to other divergences remain open.
- Online regret bound scales as max_i A_i² (Theorem 3 tabular reduction); optimal action-set dependence unknown.
- Gap between online (requires adversarial interaction) and generative model settings motivates further study of interaction protocols.

## Relevance to Survey
Directly extends the fictitious uncertainty set paradigm (Paper 3) to the LFA setting for infinite state spaces; first work to break the curse of multiagency for robust linear MGs; introduces a novel online adversarial interaction protocol; central contribution to the LFA + robust MARL thread in the survey.

## Related Work (verbatim excerpts from the paper)

> _[Section 2, Related work]_

**Distributionally Robust RL.**

"Standard reinforcement learning (RL) methods can be highly sensitive to perturbations of environment dynamics (transition kernels and reward function) [Zhang et al., 2020a, Mahmood et al., 2018]. To enhance robustness, distributionally robust RL (robust RL) seeks policies that optimize worst-case performance over a prescribed uncertainty set by incorporating distributionally robust optimization (DRO) into sequential decision making. DRO has also been extensively studied in supervised learning Rahimian and Mehrotra [2019], Gao [2020], Bertsimas et al. [2018], Duchi and Namkoong [2018], Blanchet and Murthy [2019], Gao and Kleywegt [2023].

Distributionally robust RL was first studied in the single-agent setting [Nilim and El Ghaoui, 2005, Iyengar, 2005, Badrinath and Kalathil, 2021, Zhou et al., 2021, Shi and Chi, 2022, Shi et al., 2023]. More recently, DRO formulations have been incorporated to multi-agent RL and formulates robust Markov games (RMGs) Zhang et al. [2020a], Kardeş et al. [2011], Ma et al. [2023], Blanchet et al. [2023], Shi et al. [2024a]. Existing sample-complexity guarantees for algorithms of RMGs largely focus on tabular settings with finite state and action spaces Ma et al. [2023], Blanchet et al. [2024], Shi et al. [2024a,b], while comparatively few results address large-scale or infinite state spaces. To our knowledge, the only existing work [Zheng and Lin, 2025] studied RMGs under linear function approximation. [Zheng and Lin, 2025] focuses on a restrictive class of RMGs [Zheng and Lin, 2025, Lu et al., 2024] that requires an additional vanishing minimal value assumption, which is a more restrictive subclass of RMGs than the setting considered in this work; moreover, its sample complexity still suffers from the curse of multiagency when transferred to the tabular setting. In this work, we focus on general RMGs under independent per-agent linear function approximation modeling with no further assumption on the structure of the value function, and achieve sample complexity that breaks the curse of multi-agency."

**Multi-Agent RL with Function Approximation.**

"Linear function approximation (LFA) was first studied in the single-agent setting [Jin et al., 2020, Yang and Wang, 2020]. Building on these techniques, Xie et al. [2020] and Chen et al. [2024] investigated Markov games under centralized LFA, where a central function class models value functions across the joint actions of all agents. This setting makes circumventing the curse of multi-agency challenging. To address this issue, Wang et al. [2023], Cui et al. [2023] introduced independent per-agent linear function classes and correspondingly developed provably efficient algorithms that break the curse of multi-agency; further, Dai et al. [2024] obtained optimal dependence on the action-set size via sharper analysis. Beyond LFA, several works have studied Markov games with general function approximation in both centralized settings [Huang et al., 2022, Ni et al., 2022, Xiong et al., 2022, Chen et al., 2022, Zhan et al., 2023, Jin et al., 2022] and per-agent settings [Wang et al., 2023]. In this paper, we extend independent per-agent LFA to a popular robust counterpart of standard MGs—robust linear MGs (R-LMGs). Compared to standard MGs, in both generative and online settings, we must handle the additional statistical error induced by the high nonlinearity of R-LMGs with respect to the nominal transition kernel. In the online interactive setting in particular, additional challenges arise from the need to sample from the approximate adversarial environment and from the fact that the LFA assumption applies solely to the nominal kernel; kernels within the uncertainty set do not necessarily preserve this linear structure. To address this, we introduce a hybrid sampling strategy that uses a sequence of pessimistic robust value estimates, allowing us to estimate the nominal transition kernel satisfying LFA through ridge regression and then apply the pessimistic estimates to approximate the adversarial model for subsequent robust objective estimation."

**Breaking the Curse of Multiagency in Multi-Agent RL.**

"In multi-agent reinforcement learning (MARL), the joint action space grows exponentially with the number of agents, making it crucial to develop algorithms whose sample complexity does not scale exponentially in the number of agents—often referred to as breaking the curse of multi-agency. This challenge is ubiquitous in MARL and has attracted substantial interest. Song et al. [2021], Rubinstein [2017], Bai and Jin [2020] show that learning a Nash equilibrium in general Markov games can require sample complexity exponential in the number of agents. This has motivated work on alternative solution concepts, such as correlated equilibrium (CE) and coarse correlated equilibrium (CCE), for which non-exponential guarantees are possible. For standard MGs, Daskalakis et al. [2023] provide a complexity bound of Õ(H¹¹S³ max_{i∈[n]} A_i/ε³) for learning a CCE, and Jin et al. [2021], Song et al. [2021], Li et al. [2022] also propose algorithms with non-exponential sample complexity, both for tabular MGs. Beyond the tabular setting, Cui et al. [2023] and Wang et al. [2023] develop algorithms that break the curse of multi-agency under independent per-agent LFA. Beyond standard Markov games, Song et al. [2021], Alatur et al. [2024], Dong et al. [2024] study Markov potential games and give algorithms that learn Nash equilibria with sample complexity that does not scale exponentially with the number of agents.

For robust Markov games, breaking the curse remains largely underexplored. The only existing results that breaks the curse of multi-agency Shi et al. [2024b], Jiao and Li [2024] are restricted to tabular RMGs with R-contamination or TV distance. To the best of our knowledge, this is the first work to break the curse of multi-agency for large-scale (continuous) state space, in both generative model and online data collection setting."

### Cited references (resolved from the paper's bibliography)
- **Zhang et al. (2020a)** Zhang, Kakade, Basar, Yang. *Model-based multi-agent RL in zero-sum Markov games with near-optimal sample complexity.* NeurIPS 2020.
- **Mahmood et al. (2018)** Mahmood, Korenkevych, Vasan, Ma, Bergstra. *Benchmarking reinforcement learning algorithms on real-world robots.* CoRL 2018.
- **Rahimian and Mehrotra (2019)** Rahimian, Mehrotra. *Distributionally robust optimization: A review.* arXiv:1908.05659, 2019.
- **Gao (2020)** Gao. *Finite-sample guarantees for Wasserstein distributionally robust optimization.* arXiv:2009.04382, 2020.
- **Bertsimas et al. (2018)** Bertsimas, Gupta, Kallus. *Data-driven robust optimization.* Mathematical Programming, 2018.
- **Duchi and Namkoong (2018)** Duchi, Namkoong. *Learning models with uniform performance via distributionally robust optimization.* arXiv:1810.08750, 2018.
- **Blanchet and Murthy (2019)** Blanchet, Murthy. *Quantifying distributional model risk via optimal transport.* Mathematics of Operations Research, 2019.
- **Gao and Kleywegt (2023)** Gao, Kleywegt. *Distributionally robust stochastic optimization with Wasserstein distance.* Mathematics of Operations Research, 2023.
- **Nilim and El Ghaoui (2005)** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 2005.
- **Iyengar (2005)** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **Badrinath and Kalathil (2021)** Badrinath, Kalathil. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML 2021.
- **Zhou et al. (2021)** Zhou, Bai, Zhou, Qiu, Blanchet, Glynn. *Finite-sample regret bound for distributionally robust offline tabular reinforcement learning.* AISTATS 2021.
- **Shi and Chi (2022)** Shi, Chi. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* arXiv:2208.05767, 2022.
- **Shi et al. (2023)** Shi, Li, Wei, Chen, Geist, Chi. *The curious price of distributional robustness in reinforcement learning with a generative model.* arXiv:2305.16589, 2023.
- **Kardeş et al. (2011)** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **Ma et al. (2023)** Ma, Chen, Zou, Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR, 2023.
- **Blanchet et al. (2023)** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* arXiv:2305.09659, 2023.
- **Shi et al. (2024a)** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* arXiv:2404.18909, 2024.
- **Blanchet et al. (2024)** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning.* NeurIPS 2024.
- **Shi et al. (2024b)** Shi, Gai, Mazumdar, Chi, Wierman. *Can we break the curse of multiagency in robust multi-agent reinforcement learning?* arXiv:2409.20067, 2024.
- **Zheng and Lin (2025)** Zheng, Lin. *Distributionally robust online Markov game with linear function approximation.* arXiv:2511.07831, 2025.
- **Lu et al. (2024)** Lu, Zhong, Zhang, Blanchet. *Distributionally robust reinforcement learning with interactive data collection: Fundamental hardness and near-optimal algorithm.* arXiv:2404.03578, 2024.
- **Jin et al. (2020)** Jin, Yang, Wang, Jordan. *Provably efficient reinforcement learning with linear function approximation.* COLT 2020.
- **Yang and Wang (2020)** Yang, Wang. *Reinforcement learning in feature space: Matrix bandit, kernels, and regret bound.* ICML 2020.
- **Xie et al. (2020)** Xie, Chen, Wang, Yang. *Learning zero-sum simultaneous-move Markov games using function approximation and correlated equilibrium.* COLT 2020.
- **Chen et al. (2024)** Chen, Mei, Bai. *Unified algorithms for RL with decision-estimation coefficients.* arXiv:2209.11745, 2024.
- **Wang et al. (2023)** Wang, Liu, Bai, Jin. *Breaking the curse of multiagency: Provably efficient decentralized multi-agent RL with function approximation.* COLT 2023.
- **Cui et al. (2023)** Cui, Zhang, Du. *Breaking the curse of multiagents in a large state space: RL in Markov games with independent linear function approximation.* COLT 2023.
- **Dai et al. (2024)** Dai, Cui, Du. *Refined sample complexity for Markov games with independent linear function approximation.* arXiv:2402.07082, 2024.
- **Huang et al. (2022)** Huang, Lee, Wang, Yang. *Towards general function approximation in zero-sum Markov games.* ICLR 2022.
- **Ni et al. (2022)** Ni, Song, Zhang, Jin, Wang. *Representation learning for general-sum low-rank Markov games.* arXiv:2210.16976, 2022.
- **Xiong et al. (2022)** Xiong, Zhong, Shi, Shen, Zhang. *A self-play posterior sampling algorithm for zero-sum Markov games.* ICML 2022.
- **Chen et al. (2022)** Chen, Zhou, Gu. *Almost optimal algorithms for two-player zero-sum linear mixture Markov games.* ALT 2022.
- **Zhan et al. (2023)** Zhan, Lee, Yang. *Decentralized optimistic hyperpolicy mirror descent: Provably no-regret learning in Markov games.* ICLR 2023.
- **Jin et al. (2022)** Jin, Liu, Yu. *The power of exploiter: Provable multi-agent RL in large state spaces.* ICML 2022.
- **Song et al. (2021)** Song, Mei, Bai. *When can we learn general-sum Markov games with a large number of players sample-efficiently?* arXiv:2110.04184, 2021.
- **Rubinstein (2017)** Rubinstein. *Settling the complexity of computing approximate two-player Nash equilibria.* ACM SIGecom Exchanges, 2017.
- **Bai and Jin (2020)** Bai, Jin. *Provable self-play algorithms for competitive reinforcement learning.* ICML 2020.
- **Daskalakis et al. (2023)** Daskalakis, Golowich, Zhang. *The complexity of Markov equilibrium in stochastic games.* COLT 2023.
- **Jin et al. (2021)** Jin, Liu, Wang, Yu. *V-learning — a simple, efficient, decentralized algorithm for multiagent RL.* arXiv:2110.14555, 2021.
- **Li et al. (2022)** Li, Chi, Wei, Chen. *Minimax-optimal multi-agent RL in Markov games with a generative model.* NeurIPS 2022.
- **Alatur et al. (2024)** Alatur, Barakat, He. *Independent policy mirror descent for Markov potential games: Scaling to large number of players.* arXiv:2408.08075, 2024.
- **Dong et al. (2024)** Dong, Wang, Yu. *Convergence to Nash equilibrium and no-regret guarantee in (Markov) potential games.* arXiv:2404.06516, 2024.
- **Jiao and Li (2024)** Jiao, Li. *Minimax-optimal multi-agent robust reinforcement learning.* arXiv:2412.19873, 2024.
