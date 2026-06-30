# 2. Sample-Efficient Robust Multi-Agent Reinforcement Learning in the Face of Environmental Uncertainty

## Metadata
- **Title**: Sample-Efficient Robust Multi-Agent Reinforcement Learning in the Face of Environmental Uncertainty
- **Authors**: Laixi Shi, Eric Mazumdar, Yuejie Chi, Adam Wierman
- **Affiliation**: California Institute of Technology (Shi, Mazumdar, Wierman); Carnegie Mellon University (Chi)
- **Venue**: ICML 2024 (Forty-First International Conference on Machine Learning)
- **Link/arXiv**: arXiv:2404.18909v3

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental uncertainty (model mismatch / sim-to-real gap in the transition kernel); distributionally robust, worst-case over prescribed uncertainty sets
- **Method paradigm**: Model-based; distributionally robust Markov games (RMGs); (s,a)-rectangular uncertainty sets (TV distance); generative model setting; DR-NVI algorithm; information-theoretic lower bound
- **Keywords**: Robust Markov games, DR-NVI, TV uncertainty, (s,a)-rectangularity, near-optimal sample complexity, curse of multiagency, robust NE/CE/CCE, generative model

## TL;DR
Proposes DR-NVI, the first near-optimal sample-efficient model-based algorithm for n-player distributionally robust Markov games under TV-distance (s,a)-rectangular uncertainty sets with a generative model; also establishes the first information-theoretic lower bound for RMGs, confirming near-optimality with respect to state space size, target accuracy, and horizon length.

## Problem & Motivation
Standard MARL algorithms are trained in simulated environments but deployed in slightly different real ones. Even small environmental perturbations can cause Nash equilibria to change dramatically (illustrated with a fishing-protection two-player game where p=0.049 vs. p=0.051 yields opposite equilibria). Single-agent robust RL (robust MDPs) is well-studied but multi-agent robust RL (RMGs) remains largely underexplored, especially regarding finite-sample guarantees. Existing works on RMGs either focus only on asymptotic convergence or require restricted uncertainty levels that reduce to near-standard MARL. This paper asks: can we learn near-optimal robust equilibria in RMGs with provably near-optimal sample complexity?

## Robustness Setting
- **Threat model / uncertainty set**: Total variation (TV) distance, (s,a)-rectangular. Each agent i has its own uncertainty set Uσi centered at a shared nominal transition kernel P^0: for each (s,a) pair, the adversary can choose any kernel within TV distance σi of P^0(·|s,a). Agents' uncertainty sets are independent across (s,a) pairs and across agents. Uncertainty levels σi ∈ (0,1) can differ per agent.
- **Setting**: n-player finite-horizon episodic general-sum Markov games; generative model (non-adaptive sampling); solution concepts: robust NE, robust CE, robust CCE; purely theoretically motivated (no deep-learning experiments).

## Method
- **DR-NVI (Distributionally Robust Nash Value Iteration)**: A model-based algorithm that (1) samples N independent transitions from each (s,a) pair via the generative model to form empirical models; (2) runs backward value iteration from step H to 1; at each step, solves a distributionally robust version of the Bellman equations for each agent, where the worst-case transition over the TV uncertainty ball is computed analytically using the dual of the TV robust objective (a scalar clipping formula); (3) solves the resulting matrix game at each (s,h) to produce policies for robust CCE/CE/NE.
- The robustified Bellman operator replaces the standard linear expectation with a nonlinear worst-case expectation, computed via the closed-form TV dual: σ_P[V] = E_{P^0}[V] − σ·(max V − E_{P^0}[V]).
- Handles n-player general-sum games; does not require zero-sum structure.

## Theoretical Contributions
- **Theorem 1 (Upper bound)**: DR-NVI outputs an ε-robust CCE/CE/NE with probability ≥ 1−δ provided the total sample count is  
  Ñ = Õ(S ∏_{i=1}^n A_i · H^3/ε^2 · min{H, 1/min_i σ_i}).
- **Theorem 2 (Lower bound)**: For any algorithm, any instance in the hard class of RMGs requires at least  
  Ω(S · max_i A_i · H^3/ε^2 · min{H, 1/min_i σ_i}) total samples.
  This is the first minimax lower bound for RMGs.
- **Single-agent RMDP corollary**: When n=1, the bound yields Õ(SA₁H^3/ε^2 · min{H,1/σ₁}), matching the lower bound — the first minimax-optimal finite-sample result for RMDPs in the finite-horizon setting.
- **Comparison**: DR-NVI achieves the same or fewer samples than standard NVI for standard MGs when min σi ≳ 1/H, showing robustness comes "for free" in this regime.

## Experiments
Not applicable — this is a theory paper with no empirical experiments beyond the motivating fishing-protection example illustration in Figure 1.

## Key Results
- DR-NVI: first near-optimal sample complexity for RMGs with TV uncertainty and generative model.
- Lower bound: first information-theoretic lower bound for RMGs; together with the upper bound, confirms near-optimality up to logarithmic factors in S, ε, H, {σi}.
- Sample complexity is inversely proportional to min σi when min σi ≳ 1/H, meaning robustness strictly helps efficiency.
- Full n-player general-sum setting handled (beyond two-player zero-sum).

## Limitations & Future Work
- Sample complexity still scales as ∏A_i (curse of multiagency); breaking this remains an open problem.
- Only TV-distance uncertainty; extending to KL, χ², Wasserstein is noted as future direction.
- Online exploration (beyond generative model) and offline settings are not covered.
- Transition uncertainty only; reward uncertainty is mentioned briefly.

## Relevance to Survey
Foundational sample-complexity paper for distributionally robust MARL; establishes the first near-optimal and first lower-bound results for n-player RMGs; motivates the fictitious uncertainty set and curse-of-multiagency research (papers 3 and 4); defines the standard (s,a)-rectangular TV-distance RMG baseline that subsequent papers compare against.

## Related Work (verbatim excerpts from the paper)

> _[Section 5, Related Works]_

"In this section, we discuss a non-exhaustive set of related works, limiting our discussions primarily to provable RL algorithms in the tabular setting, which are most related to this paper."

**Finite-sample studies of standard Markov games.**

"Multi-agent reinforcement learning (MARL), originated from the seminal work (Littman, 1994), has been widely studied under the framework of standard Markov games (Shapley, 1953); see Busoniu et al. (2008); Oroojlooy and Hajinezhad (2023); Zhang et al. (2021b) for detailed reviews. There has been no shortage of provably convergent MARL algorithms with asymptotic guarantees (Littman et al., 2001; Littman and Szepesvári, 1996).

A line of recent efforts have concentrated on understanding and developing algorithms for standard MGs with non-asymptotic guarantees (finite-sample analysis). Within this field, Nash equilibrium (NE) is arguably one of the most compelling solution concepts for standard MGs. Research on calculating NE primarily focuses on an important basic class: standard two-player zero-sum MGs (Bai and Jin, 2020; Chen et al., 2022; Cui and Du, 2022a,b; Dou et al., 2022; Jia et al., 2019; Mao and Başar, 2022; Tian et al., 2021; Wei et al., 2017, 2021; Yan et al., 2022b; Yang and Ma, 2022; Zhong et al., 2022). This focus arises because computing NEs in scenarios beyond the standard two-player zero-sum MGs is generally computationally intractable (i.e., PPAD-complete) (Daskalakis, 2013; Daskalakis et al., 2009).

For discounted infinite-horizon two-player zero-sum Markov games, the state-of-the-art sample complexity for learning NE (Zhang et al., 2020e) remains suboptimal due to the "curse of multiple agents" issue (Zhang et al., 2020e). In contrast, for episodic finite-horizon two-player zero-sum Markov games standard MGs, Bai et al. (2020); Jin et al. (2021a); Li et al. (2022a) have overcome this curse, progressively achieving minimax-optimal sample complexity in the order of O(S max_{1≤i≤n} A_i H^4/ε^2). Besides NE, Daskalakis et al. (2022); Jin et al. (2021a); Li et al. (2022a); Liu et al. (2021); Mao and Başar (2022); Song et al. (2021) have extended this achievement to other computationally tractable solution concepts (e.g., CE/CCE) in general-sum multiplayer MGs. Focusing on the same non-adaptive sampling mechanism considered in this work, the sample complexity for learning NE/CE/CCE in standard MGs with the state-of-the-art approaches (Liu et al., 2021; Zhang et al., 2020e) still suffers from the curse of multiple agents, calculated as O(S ∏_{1≤i≤n} A_i H^4/ε^2)."

**Robustness in MARL.**

"Despite significant advances in standard MARL, current algorithms may fail dramatically due to perturbations or uncertainties in game components, resulting in significantly deviated equilibrium, as illustrated in Figure 1. A growing body of research is now addressing the robustness of MARL algorithms against uncertainties in various components of Markov games, such as state (Han et al., 2022; He et al., 2023; Zhang et al., 2023c; Zhou and Liu, 2023), environment (reward and transition kernel), the type of agents (Zhang et al., 2021a), or other agents' policies (Kannan et al., 2023; Li et al., 2019); see Vial et al. (2022) for a recent review.

This work considers the robustness against environmental uncertainty, adopting distributionally robust optimization (DRO) that has primarily been investigated in the context of supervised learning (Bertsimas et al., 2018; Blanchet and Murthy, 2019; Duchi and Namkoong, 2018; Gao, 2020; Rahimian and Mehrotra, 2019). Applying DRO for single-agent RL (Iyengar, 2005) to handle model uncertainty has garnered significant attention. When turning to MARL, the problem is conceptualized as robust Markov games within the DRO framework, an area that remains relatively underexplored with only a few provable algorithms developed (Blanchet et al., 2023; Kardeş et al., 2011; Ma et al., 2023; Zhang et al., 2020c). Notably, Kardeş et al. (2011) verifies the existence of Nash equilibrium for robust Markov games under mild assumptions; Zhang et al. (2020c) derives asymptotic convergence for a Q-learning type algorithm under certain conditions; Blanchet et al. (2023); Ma et al. (2023) are the most related works that provide algorithms with finite-sample guarantees for various types of uncertainty set. Especially, Ma et al. (2023) considers a restricted uncertainty level that could fail to bring robustness to MARL in certain scenarios."

**Single-agent distributionally robust RL (robust MDPs).**

"For single-agent RL, considering robustness to model uncertainty using DRO framework — i.e., distributionally robust dynamic programming and robust MDPs — has gained significant attention across both theoretical and practical domains (Badrinath and Kalathil, 2021; Derman et al., 2018; Derman and Mannor, 2020; Goyal and Grand-Clement, 2022; Ho et al., 2018, 2021; Iyengar, 2005; Kaufman and Schaefer, 2013; Mankowitz et al., 2019; Roy et al., 2017; Smirnova et al., 2019; Tamar et al., 2014; Wolff et al., 2012; Xu and Mannor, 2012). Recently, a substantial body of work has been dedicated to exploring the finite-sample performance of provable robust single-agent RL algorithms, where different sampling mechanisms, diverse divergence function of the uncertainty set, and other related problems/issues has been investigated a lot (Badrinath and Kalathil, 2021; Blanchet et al., 2023; Clavier et al., 2023; Dong et al., 2022; Kumar et al., 2023; Li and Lan, 2023; Li et al., 2022b; Liang et al., 2023; Liu et al., 2022; Ma et al., 2022; Panaganti and Kalathil, 2022; Panaganti et al., 2022; Ramesh et al., 2023; Shi and Chi, 2022; Shi et al., 2023; Wang et al., 2024, 2023a,b,c; Wang and Zou, 2021; Xu et al., 2023; Yang et al., 2023, 2022; Zhang et al., 2023a; Zhou et al., 2021).

Among the studies of robust MDPs, those particularly relevant to this paper employ the uncertainty set using total variation (TV) distance in a tabular setting (Dong et al., 2022; Liu and Xu, 2024; Panaganti and Kalathil, 2022; Xu et al., 2023; Yang et al., 2022). It has been established that solving robust MDPs requires no more samples than solving standard MDPs in terms of the sample requirement (Shi et al., 2023) with a generative model. However, robust MARL involves additional complexities compared to robust single-agent RL. It remains an open question whether the findings from robust MDPs can be generalized to robust MARL, which includes more technical challenges and strategic interactions. Our work takes a step towards the question, confirming that similar phenomena apply in robust MARL, albeit with increased difficulties due to the multi-agent dynamics."

**RL with a generative model.**

"Access to a generative model (or simulator) serves as a fundamental and idealistic sampling protocol that has been widely used to study finite-sample guarantees for diverse types of RL algorithms, such as various model-based, model-free, and policy-based algorithms (Agarwal et al., 2020; Azar et al., 2013; Beck and Srikant, 2012; Even-Dar and Mansour, 2003; Kakade, 2003; Kearns et al., 2002; Khamaru et al., 2020; Li et al., 2023, 2020; Pananjady and Wainwright, 2020; Sidford et al., 2018; Wainwright, 2019; Woo et al., 2023; Yang and Wang, 2019; Zanette et al., 2019). This work follows this fundamental protocol with a non-adaptive sampling mechanism to understand and design algorithms for robust Markov games."

### Cited references (resolved from the paper's bibliography)
- **Blanchet et al. (2023)** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* NeurIPS 2023 / arXiv:2305.09659.
- **Busoniu et al. (2008)** Busoniu, Babuska, De Schutter. *A comprehensive survey of multiagent reinforcement learning.* IEEE Transactions on Systems, Man, and Cybernetics Part C, 2008.
- **Oroojlooy and Hajinezhad (2023)** Oroojlooy, Hajinezhad. *A review of cooperative multi-agent deep reinforcement learning.* Applied Intelligence, 2023.
- **Zhang et al. (2021b)** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, 2021.
- **Littman (1994)** Littman. *Markov games as a framework for multi-agent reinforcement learning.* ICML 1994.
- **Littman et al. (2001)** Littman et al. *Friend-or-foe Q-learning in general-sum games.* ICML 2001.
- **Littman and Szepesvári (1996)** Littman, Szepesvári. *A generalized reinforcement-learning model: Convergence and applications.* ICML 1996.
- **Bai and Jin (2020)** Bai, Jin. *Provable self-play algorithms for competitive reinforcement learning.* ICML 2020.
- **Jin et al. (2021a)** Jin, Liu, Wang, Yu. *V-learning — a simple, efficient, decentralized algorithm for multiagent RL.* arXiv:2110.14555, 2021.
- **Li et al. (2022a)** Li, Chi, Wei, Chen. *Minimax-optimal multi-agent RL in Markov games with a generative model.* NeurIPS 2022.
- **Liu et al. (2021)** Liu, Yu, Bai, Jin. *A sharp analysis of model-based reinforcement learning with self-play.* ICML 2021.
- **Song et al. (2021)** Song, Mei, Bai. *When can we learn general-sum Markov games with a large number of players sample-efficiently?* arXiv:2110.04184, 2021.
- **Daskalakis (2013)** Daskalakis. *On the complexity of approximating a Nash equilibrium.* ACM Transactions on Algorithms, 2013.
- **Daskalakis et al. (2009)** Daskalakis, Goldberg, Papadimitriou. *The complexity of computing a Nash equilibrium.* SIAM Journal on Computing, 2009.
- **Zhang et al. (2020e)** Zhang, Zhou, Ji. *Model-free reinforcement learning: from clipped pseudo-regret to sample complexity.* arXiv:2006.03864, 2020.
- **Han et al. (2022)** Han, Su, He, Han, Yang, Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **He et al. (2023)** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research, 2023.
- **Zhang et al. (2023c)** Zhang, Sun, Huang, Miao. *Safe and robust multi-agent reinforcement learning for connected autonomous vehicles under state perturbations.* arXiv:2309.11057, 2023.
- **Zhou and Liu (2023)** Zhou, Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv:2306.06136, 2023.
- **Zhang et al. (2021a)** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **Kannan et al. (2023)** Kannan, Venkatesh, Min. *Smart-LLM: Smart multi-agent robot task planning using large language models.* arXiv:2309.10062, 2023.
- **Li et al. (2019)** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **Vial et al. (2022)** Vial, Shakkottai, Srikant. *Robust multi-agent bandits over undirected graphs.* ACM MACS, 2022.
- **Iyengar (2005)** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **Kardeş et al. (2011)** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **Ma et al. (2023)** Ma, Chen, Zou, Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR, 2023.
- **Zhang et al. (2020c)** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **Bertsimas et al. (2018)** Bertsimas, Gupta, Kallus. *Data-driven robust optimization.* Mathematical Programming, 2018.
- **Blanchet and Murthy (2019)** Blanchet, Murthy. *Quantifying distributional model risk via optimal transport.* Mathematics of Operations Research, 2019.
- **Duchi and Namkoong (2018)** Duchi, Namkoong. *Learning models with uniform performance via distributionally robust optimization.* arXiv:1810.08750, 2018.
- **Gao (2020)** Gao. *Finite-sample guarantees for Wasserstein distributionally robust optimization: Breaking the curse of dimensionality.* arXiv:2009.04382, 2020.
- **Rahimian and Mehrotra (2019)** Rahimian, Mehrotra. *Distributionally robust optimization: A review.* arXiv:1908.05659, 2019.
- **Shi et al. (2023)** Shi, Li, Wei, Chen, Geist, Chi. *The curious price of distributional robustness in reinforcement learning with a generative model.* NeurIPS 2023 / arXiv:2305.16589.
- **Yang et al. (2022)** Yang, Zhang, Zhang. *Toward theoretical understandings of robust Markov decision processes: Sample complexity and asymptotics.* Annals of Statistics, 2022.
- **Panaganti and Kalathil (2022)** Panaganti, Kalathil. *Sample complexity of robust reinforcement learning with a generative model.* AISTATS 2022.
- **Xu et al. (2023)** Xu, Panaganti, Kalathil. *Improved sample complexity bounds for distributionally robust reinforcement learning.* arXiv:2303.02783, 2023.
- **Dong et al. (2022)** Dong, Li, Wang, Zhang. *Online policy optimization for robust MDP.* arXiv:2209.13841, 2022.
- **Liu and Xu (2024)** Liu, Xu. *Distributionally robust off-dynamics reinforcement learning: Provable efficiency with linear function approximation.* arXiv:2402.15399, 2024.
