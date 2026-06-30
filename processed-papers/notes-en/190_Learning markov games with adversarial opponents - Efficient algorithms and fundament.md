# 190. Learning Markov Games with Adversarial Opponents: Efficient Algorithms and Fundamental Limits

## Metadata
- **Title**: Learning Markov Games with Adversarial Opponents: Efficient Algorithms and Fundamental Limits
- **Authors**: Qinghua Liu, Yuanhao Wang, Chi Jin (equal contribution: Liu, Wang)
- **Affiliation**: Princeton University
- **Venue**: Not specified (arXiv:2203.06803v4, 14 Jun 2022)
- **Link/arXiv**: arXiv:2203.06803v4 [cs.LG]

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial opponents in two-player zero-sum Markov games; the opponent may play arbitrary, history-dependent (general) or Markov policies that can change adversarially across episodes. The learner seeks to exploit suboptimal/adaptive opponents while remaining invulnerable to optimal ones.
- **Method paradigm**: No-regret learning (regret against the best fixed policy in hindsight), online learning, EXP3 / optimistic policy evaluation (UCB-style exploration bonus), minimax / game-theoretic equilibrium, statistical and computational lower bounds (reductions to POMDPs / latent MDPs / 3-SAT).
- **Keywords**: Markov games, adversarial opponents, no-regret learning, best fixed policy in hindsight, EXP3, statistical/computational hardness

## TL;DR
The paper studies no-regret learning in two-player zero-sum Markov games against adversarial opponents while competing with the best fixed policy in hindsight, giving efficient √K-regret algorithms (OP-EXP3 and adaptive OP-EXP3) in a revealed-policy setting when either the baseline or the opponent policy class is small, together with matching exponential statistical lower bounds and a computational hardness result that hold even under very favorable conditions.

## Problem & Motivation
A central open question in MARL is how to exploit (adaptive) suboptimal opponents while staying invulnerable to optimal opponents — an objective that goes beyond Nash equilibria. In normal-form games this is addressed by no-regret learning against the best fixed policy in hindsight, but general MARL adds unknown dynamics and sequential correlations between player and opponent, so all existing Markov-game results only compete against the Nash value when facing adversarial opponents. The paper asks whether one can compete against the best fixed policy in hindsight and achieve no-regret learning in MARL, modeled as two-player zero-sum Markov games. Playing a Nash equilibrium (e.g., uniform in rock-paper-scissors) cannot exploit an exploitable opponent, motivating a stronger solution concept.

## Robustness Setting
- **Threat model / uncertainty set**: The opponent (min-player) is adversarial and may change her policy across episodes; she can play general (history-dependent) policies or Markov policies. Two information settings are studied: (i) the standard setting, where only the opponent's actions are observed; (ii) the revealed-policy setting, where the opponent reveals the policy she played at the end of each episode. Performance is measured by regret against the best fixed policy in hindsight from a prespecified baseline policy class Φ⋆.
- **Setting**: Competitive (two-player zero-sum Markov game; results extend to general-sum); tabular episodic; online learning; the learner controls one player while the other is potentially adversarial. The reward function is assumed known.

## Method
- Formalizes the objective as regret against the best fixed policy in hindsight (Definition 1), a strictly stronger criterion than comparing to the Nash value, since it forces the algorithm to exploit exploitable opponents while remaining well-defined even in the general-sum setting.
- **OP-EXP3 (Algorithm 1)** for a finite baseline policy class Φ⋆: runs anytime EXP3 over Φ⋆ by treating each baseline policy as an "action"; after observing the opponent's revealed policy νk, it computes an optimistic value estimate of each µ × νk via an Optimistic Policy Evaluation subroutine (Bellman dynamic programming from step H to 1 on the empirical transition with a UCB bonus β to ensure optimism), then performs an EXP3 update using these optimistic values as negative gradients, while updating the empirical MG model.
- **Adaptive OP-EXP3 (Algorithm 2)** for an unknown finite opponent policy class Ψ⋆ with a general baseline class: adds (i) a lazy model update (uses a lazy model estimate refreshed when a counter doubles or a new opponent policy appears) and (ii) an adaptive player policy class recomputed via an Optimistic Best Response subroutine over an ε-cover of all mixtures of historical opponent policies, restarting EXP3 each time. This shrinks the effective log-cardinality of the baseline class to ˜O(|Ψ⋆|) while remaining competitive with any general policy.
- **Lower bounds**: statistical hardness reductions simulate POMDPs (opponent plays a fixed general policy) and latent MDPs (opponent plays a small set of Markov policies) by Markov games of similar size; computational hardness reduces 3-SAT to finding the best Markov policy in a latent MDP.

## Theoretical Contributions
- **Standard-setting lower bounds**: Ω(min{K, 2^H}) regret for competing with the best Markov policy when the opponent plays a fixed general policy (Theorem 2, via POMDP ⊆ MG, Proposition 3); Ω(min{K, 2^H}/H) when the opponent uniformly samples from an unknown set of H Markov policies (Theorem 4, via latent MDP ⊆ MG, Proposition 5).
- **Revealed-policy upper bounds**: OP-EXP3 achieves ˜O(√(H⁴S²AK)) regret with a finite baseline class against arbitrary general opponents (Theorem 6); adaptive OP-EXP3 achieves ˜O(√(H⁴S²AK) + √(|Ψ⋆|SAH³K) + √(|Ψ⋆|²H²K)) regret when the opponent draws from a finite unknown class Ψ⋆ (Theorem 7).
- **Revealed-policy lower bound**: Ω(min{K, 2^H}) when competing with the best general policy and both Φ⋆ and Ψ⋆ are large, even if the opponent plays only deterministic Markov policies and reveals her policy each episode (Theorem 8).
- **Computational hardness**: achieving poly(S,A,H)·K^{1−c} expected regret cannot be done in poly(S,A,H,K) time unless NP ⊆ BPP, even with known transitions, revealed policies, and a small known set of Markov opponent policies (Theorem 9, reduction from 3-SAT).

## Experiments
- **Environment/Benchmark**: Not specified (theoretical paper; no empirical experiments).
- **Baselines**: Not specified.
- **Evaluation metrics**: Regret against the best fixed policy in hindsight (Definition 1); regret bounds expressed in terms of H, S, A, K, |Φ⋆|, |Ψ⋆|.

## Key Results
- In the standard setting, no-regret learning is statistically intractable: exponential-in-H regret lower bounds hold even when the baseline class consists only of Markov policies and the opponent only alternates among a small (H) set of Markov policies.
- In the revealed-policy setting, √K-regret is achievable whenever either the log-cardinality of the baseline policy class or the cardinality of the opponent's policy class is small (OP-EXP3 and adaptive OP-EXP3); adaptive OP-EXP3 remains sublinear even if the opponent policy class grows, as long as its cardinality is o(√k).
- A matching exponential lower bound shows √K-regret is impossible when both the baseline class is doubly exponential and the opponent class is exponential.
- The hardness results are stronger than prior ones: the statistical lower bound holds without restricting algorithms or relying only on computational hardness, and the computational lower bound (NP ⊆ BPP) holds under very weak/favorable conditions and rules out statistically efficient value-iteration / Q-learning style algorithms unless they use NP-hard subroutines.

## Limitations & Future Work
- The positive results require the revealed-policy setting; in the standard (actions-only) setting no-regret learning is statistically impossible in general.
- The best achievable algorithm is statistically efficient but computationally intensive (computational hardness under NP ⊆ BPP), so it is not poly-time.
- The work assumes tabular episodic two-player zero-sum Markov games with known reward; extensions to function approximation, large state spaces, or fully unknown rewards are not the focus (the authors note results extend to unknown rewards and to the general-sum setting). No explicit future-work section is given.

## Relevance to Survey
This paper sits on the "adversarial agents / adversarial opponents" line of robust MARL, where robustness is to an adaptively adversarial opponent rather than to environment/model uncertainty. It strengthens the solution concept from competing with the Nash value to competing with the best fixed policy in hindsight (exploiting suboptimal opponents), and contributes fundamental statistical and computational limits via connections to POMDPs and latent MDPs. It complements the adversarial-MDP / online-learning-in-Markov-games literature and the robust-RL-via-zero-sum-game framing, providing the theoretical boundary of what is learnable against adversarial opponents.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Learning Nash equilibria in Markov games."]_

"There has been a long line of literature focusing on learning the Nash equilibrium of Markov games when either the dynamics are known, or the amount of collected data goes to infinity [23, 15, 14, 22]. Later works have considered self-play algorithms that incorporate exploration and can find Nash equilibrium in Markov games with unknown dynamics [36, 4, 3, 37, 24]. When the algorithm is only able to control one player and the other player is potentially adversarial, Brafman and Tennenholtz [6] proposed the R-max algorithm, and showed that it is able to obtain average value close to the Nash value. Later works [36, 34, 18] obtain similar or improved results also for comparing to the Nash value."

> _[Section 2, Related Work — "Learning latent MDPs."]_

"In latent MDPs, sometimes also referred as multi-model MDPs, a latent variable is drawn from a fixed distribution at the start of each episode, and the dynamics of the MDP would be a function of this latent variable. Steimle et al. [33] has shown that finding the optimal Markov policy in the latent MDP problem is computational hard; Kwon et al. [20] considered reinforcement learning in latent MDPs, providing both statistical lower bounds for the general case and sample complexity upper bounds under further assumptions. Latent MDPs, and in fact POMDPs [32, 2, 17] in general, can be simulated using Markov games with adversarial opponents as proved in this paper; thus learning latent MDPs can be viewed as a special case of the setting considered in this paper."

> _[Section 2, Related Work — "Adversarial MDPs."]_

"Another line of work focuses on the single-agent adversarial MDP setting where the transition or the reward function is adversarially chosen for each episode. When the adversary can arbitrarily alter the transition, Abbasi Yadkori et al. [1] prove that no-regret learning is computationally at least as hard as learning parity with noise. Later work by Bai et al. [4] adapt similar hard instance for Markov games and prove that achieving sublinear regret in MGs against adversarial opponents is also computationally hard. On the other hand, if the transition is fixed and the adversary is only allowed to alter the reward function, sublinear regret can be achieved by various algorithms [16, 38, 26, 28] in competing against the best Markov policy in hindsight."

> _[Section 2, Related Work — "Matrix games and extensive form games."]_

"For matrix games, it is well known that playing EXP-style algorithms would allow one to compete with the best policy (action profile) in hindsight [see e.g., 9]. For extensive form games (EFGs), similar no-regret guarantees can be achieved via counterfactual regret minimization [39] or online convex optimization [13, 11, 10, 19]. EFGs can be viewed a special subclass of MGs where the transition admits a strict tree structure. Therefore, results for EFGs do not directly apply to MGs."

> _[Introduction — on prior work competing only against Nash equilibria when facing adversarial opponents]_

"On the other hand, addressing general MARL brings a number of new challenges such as unknown environment dynamics and sequential correlations between the player and the opponents. Consequently, all existing results [e.g., 6, 36, 34, 18] have only focused on competing against Nash equilibria when facing adversarial opponents."

### Cited references (resolved from the paper's bibliography)
- **[1]** Abbasi Yadkori, Bartlett, Kanade, Seldin, Szepesvári. *Online learning in Markov decision processes with adversarially chosen transition probability distributions.* NeurIPS 2013.
- **[2]** Azizzadenesheli, Lazaric, Anandkumar. *Reinforcement learning of POMDPs using spectral methods.* COLT 2016.
- **[3]** Bai, Jin. *Provable self-play algorithms for competitive reinforcement learning.* ICML 2020.
- **[4]** Bai, Jin, Yu. *Near-optimal reinforcement learning with self-play.* NeurIPS 2020.
- **[6]** Brafman, Tennenholtz. *R-max — a general polynomial time algorithm for near-optimal reinforcement learning.* JMLR 2002.
- **[9]** Cesa-Bianchi, Lugosi. *Prediction, Learning, and Games.* Cambridge University Press 2006.
- **[10]** Farina, Sandholm. *Model-free online learning in unknown sequential decision making problems and games.* arXiv 2021.
- **[11]** Farina, Kroer, Sandholm. *Faster game solving via predictive Blackwell approachability: connecting regret matching and mirror descent.* arXiv 2020.
- **[13]** Gordon. *No-regret algorithms for online convex programs.* NeurIPS 2007.
- **[14]** Hansen, Miltersen, Zwick. *Strategy iteration is strongly polynomial for 2-player turn-based stochastic games with a constant discount factor.* Journal of the ACM 2013.
- **[15]** Hu, Wellman. *Nash Q-learning for general-sum stochastic games.* JMLR 2003.
- **[16]** Jin, Jin, Luo, Sra, Yu. *Learning adversarial Markov decision processes with bandit feedback and unknown transition.* ICML 2019.
- **[17]** Jin, Kakade, Krishnamurthy, Liu. *Sample-efficient reinforcement learning of undercomplete POMDPs.* NeurIPS 2020.
- **[18]** Jin, Liu, Yu. *The power of exploiter: provable multi-agent RL in large state spaces.* arXiv:2106.03352, 2021.
- **[19]** Kozuno, Ménard, Munos, Valko. *Model-free learning for two-player zero-sum partially observable Markov games with perfect recall.* arXiv:2106.06279, 2021.
- **[20]** Kwon, Efroni, Caramanis, Mannor. *RL for latent MDPs: regret guarantees and a lower bound.* NeurIPS 2021.
- **[22]** Lee, Luo, Wei, Zhang. *Linear last-iterate convergence for matrix games and stochastic games.* arXiv:2006.09517, 2020.
- **[23]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994 (Elsevier).
- **[24]** Liu, Yu, Bai, Jin. *A sharp analysis of model-based reinforcement learning with self-play.* ICML 2021.
- **[26]** Rosenberg, Mansour. *Online convex optimization in adversarial Markov decision processes.* arXiv:1905.07773, 2019.
- **[28]** Shani, Efroni, Rosenberg, Mannor. *Optimistic policy optimization with bandit feedback.* ICML 2020.
- **[32]** Smallwood, Sondik. *The optimal control of partially observable Markov processes over a finite horizon.* Operations Research 1973.
- **[33]** Steimle, Kaufman, Denton. *Multi-model Markov decision processes.* IISE Transactions 2021.
- **[34]** Tian, Wang, Yu, Sra. *Online learning in unknown Markov games.* ICML 2021.
- **[36]** Wei, Hong, Lu. *Online reinforcement learning in stochastic games.* NeurIPS 2017.
- **[37]** Xie, Chen, Wang, Yang. *Learning zero-sum simultaneous-move Markov games using function approximation and correlated equilibrium.* arXiv:2002.07066, 2020.
- **[38]** Zimin, Neu. *Online learning in episodic Markovian decision processes by relative entropy policy search.* NeurIPS 2013.
- **[39]** Zinkevich, Johanson, Bowling, Piccione. *Regret minimization in games with incomplete information.* NeurIPS 2007.
