# 21. Minimax-Optimal Multi-Agent RL in Markov Games With a Generative Model

## Metadata
- **Title**: Minimax-Optimal Multi-Agent RL in Markov Games With a Generative Model
- **Authors**: Gen Li, Yuejie Chi, Yuting Wei, Yuxin Chen
- **Affiliation**: University of Pennsylvania (UPenn); Carnegie Mellon University (CMU)
- **Venue**: NeurIPS 2022 (36th Conference on Neural Information Processing Systems)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Not a robustness/perturbation paper in the adversarial sense; "minimax" here refers to minimax-optimal sample complexity. The work draws on online adversarial learning (Follow-the-Regularized-Leader) as an algorithmic subroutine to break the curse of multiple agents.
- **Method paradigm**: Sample-complexity / minimax theory for Markov games; model-free Q-learning with FTRL (online adversarial learning), optimism in the face of uncertainty (Bernstein-style/UCB bonuses), generative-model (simulator) sampling, game-theoretic equilibria (Nash equilibrium / coarse correlated equilibrium).
- **Keywords**: Markov games, Nash equilibrium, coarse correlated equilibrium (CCE), sample complexity, generative model, Follow-the-Regularized-Leader (FTRL)

## TL;DR
The paper develops Q-FTRL, a model-free algorithm with an adaptive generative-model sampling scheme that learns an ε-approximate CCE in general-sum Markov games (and an ε-NE in two-player zero-sum games) using Õ(H⁴S Σᵢ Aᵢ / ε²) samples, which is minimax-optimal up to log factors for a fixed number of players — simultaneously overcoming the curse of multiple agents and the long-horizon barrier.

## Problem & Motivation
Learning equilibria (Nash equilibria or coarse correlated equilibria) in Markov games sample-efficiently remains unsettled even in the most basic two-player zero-sum case. All prior results suffer from at least one of two obstacles regardless of the sampling protocol: (i) the curse of multiple agents (sample size scales with the product of joint actions, e.g., A₁A₂, which blows up exponentially with the number of players), and (ii) the barrier of long horizon (sub-optimal dependence on the horizon H, e.g., V-learning is a factor of H² above the minimax lower bound). The paper asks whether one can learn an NE (resp. CCE) in a sample-optimal and computation-efficient fashion that crosses both hurdles simultaneously.

## Robustness Setting
- **Threat model / uncertainty set**: Not specified — there is no adversarial perturbation, uncertainty set, or robustness threat model. The only "uncertainty" addressed is statistical estimation uncertainty from finite samples, compensated for via data-driven UCB (Bernstein-style variance-aware) bonus terms.
- **Setting**: Competitive MARL; multi-player general-sum and two-player zero-sum Markov games (non-stationary finite-horizon). Sampling protocol is the generative model / simulator (the most flexible protocol), with an adaptive sampling scheme. The algorithm can be run in a decentralized manner (each player acts independently without observing opponents' actions; only the final policy estimate aggregates iterates across players); output policy is Markovian.

## Method
- Backward dynamic-programming recursion from step h = H to h = 1: the sampling and learning for step h are finished before moving to step h−1, which enables a Markovian output policy.
- For each step h, each player calls the generative model for K rounds; per round it draws SAᵢ independent samples (opponents' actions drawn from current policy iterates), and builds an empirical reward vector and empirical transition kernel of single-agent (per-player) size — so storage/updates scale with the aggregate individual action size Σᵢ Aᵢ, not the product action space.
- Q-function estimation: compute a one-step-look-ahead estimate qᵏ = rᵏ + Pᵏ V̂(h+1), then apply the rescaled-linear-learning-rate Q-learning update Qᵏ = (1−αₖ)Qᵏ⁻¹ + αₖqᵏ.
- Policy update via exponential weights, which implements Follow-the-Regularized-Leader (FTRL) with negative-entropy regularizer; this online-adversarial-learning subroutine is what breaks the curse of multiple agents.
- Bonus terms βᵢ,ₕ are Bernstein-style variance estimates (data-driven UCBs) chosen to mimic the variance-type quantities in a refined FTRL regret bound and to ensure decomposability over steps, which is key to optimizing the horizon dependence.
- Output: a mixture of product policies (CCE for general-sum) or a product policy b̂π₁ × b̂π₂ (NE for two-player zero-sum).

## Theoretical Contributions
- **Theorem 1 (NE, two-player zero-sum)**: with K ≳ H³ log⁴(·)/ε², with probability ≥ 1−δ the output product policy is an ε-approximate Nash equilibrium; total samples Õ(H⁴S(A₁+A₂)/ε²).
- **Theorem 2 (CCE, multi-player general-sum)**: with K ≳ H³ log⁴(·)/ε², with probability ≥ 1−δ the output joint policy is an ε-approximate CCE; total samples Õ(H⁴S Σᵢ Aᵢ / ε²).
- **Minimax optimality**: matches the information-theoretic lower bound Õ(H⁴S max₁≤i≤m Aᵢ / ε²) up to log factors when m is fixed (or grows only logarithmically), the first result to simultaneously overcome the long-horizon barrier and the curse of multiple agents.
- **No burn-in / full ε-range**: validity holds for any ε ∈ (0, H], so no burn-in sample size is needed.
- **Refined FTRL regret bound**: a new regret bound for FTRL that makes explicit the role of variance-type quantities, stated as being of independent interest.

## Experiments
- **Environment/Benchmark**: None — this is a purely theoretical paper (the NeurIPS checklist marks all experiment items as N/A).
- **Baselines**: None empirically; theoretically compared against prior sample-complexity results — Zhang et al. [79] (model-based, generative model), Liu et al. [43] (model-based, online exploration), Bai et al. [5] / Jin et al. [31] (V-learning, online exploration), and Daskalakis et al. [23].
- **Evaluation metrics**: Sample complexity (number of generative-model calls / episodes) to reach an ε-approximate NE or CCE; sub-optimality gap gap(π) ≤ ε.

## Key Results
- Learns an ε-NE in two-player zero-sum MGs with Õ(H⁴S(A₁+A₂)/ε²) samples — replacing the joint-action factor A₁A₂ (of Zhang et al. [79]) with the sum A₁+A₂, and improving the horizon dependence by a factor of H² over V-learning (Bai et al. [5], Jin et al. [31]).
- Learns an ε-CCE in multi-player general-sum MGs with Õ(H⁴S Σᵢ Aᵢ / ε²) samples; for fixed m this is minimax-optimal up to log factors, improving over the model-based bound of Liu et al. [43] (sub-optimal in H and S, suffering the curse of multiple agents) and over the V-learning bound Õ(H⁶S max Aᵢ/ε²) (sub-optimal in H).
- The returned policy is Markovian and the algorithm is "rational" (converges to a player's best response if all others freeze their policies); it can be executed in a decentralized fashion.

## Limitations & Future Work
- Requires access to a generative model / simulator (the most flexible sampling protocol); the result does not transfer to the online exploration setting, which is more restrictive.
- Minimax optimality holds only when the number of players m is fixed or grows logarithmically in the problem parameters; the dependence is not optimal for an arbitrarily growing m.
- Learns CCE rather than NE in the general-sum case, due to the general intractability of computing NE.
- Purely theoretical; no empirical validation (no experiments). The paper does not list explicit open problems beyond these, so further directions are Not specified.

## Relevance to Survey
This is a foundational theoretical reference on the sample complexity of learning equilibria in competitive (general-sum and zero-sum) Markov games. It is relevant to the robust MARL survey indirectly: (i) "minimax-optimal" sample-complexity analysis underpins much of the robust/distributionally-robust MARL theory line; and (ii) the use of online adversarial learning (FTRL / no-regret) as a subroutine to break the curse of multiple agents is a technique shared with adversarial-training and game-theoretic-equilibrium method lines in robust MARL. It sits on the "game-theoretic equilibrium / minimax theory" methodological axis rather than the perturbation-robustness axis.

## Related Work (verbatim excerpts from the paper)
> _[Introduction — opening, on MARL and Markov games]_

"The thriving ﬁeld of multi-agent reinforcement learning (MARL) studies how a group of interacting agents make decisions autonomously in a shared dynamic environment [80]. The recent developments in game playing [66, 9], self-driving vehicles [58], and multi-robot control [45] are prime examples of MARL in action. In practice, there is no shortage of situations where the agents involved have conﬂict of interest, and they have to act competitively in order to promote their own beneﬁts (possibly at the expense of one another). Scenarios of this kind are frequently modeled via Markov games (MGs) [59, 42], a framework that has been a fruitful playground to formalize and stimulate the studies of competitive MARL."

> _[Introduction — on Nash equilibrium and CCE]_

"In view of the irreconcilable competition between individual players, solutions of competitive MARL normally take the form of certain equilibrium strategy proﬁles, which are perhaps best epitomized by the concept of Nash equilibrium (NE) [49]. In a Nash equilibrium, no gain can be realized through a unilateral change — assuming no coordination between players — and hence no player has incentives to deviate from her current strategy/policy. A myriad of research has been conducted surrounding NE, which spans various aspects like existence, learnability, computational hardness, and algorithm design, among others [59, 20, 12, 53, 52, 22, 42, 28, 50, 33]. Given that ﬁnding NE is notoriously expensive in general (except for special cases like two-player zero-sum MGs) [20, 21], several more tractable solution concepts have emerged in the studies of game theory and MARL, a prominent example being the coarse correlated equilibrium (CCE) [47]. A key compromise made in the CCE is that it permits the players to act in an coordinated fashion, which contrasts sharply with the absence of coordination in the deﬁnition of NE."

> _[Introduction — "Example: inadequacy in learning two-player zero-sum Markov games", model-based methods]_

"Model-based methods under either a generative model or online exploration. Assuming access to a generative model (so that one can sample arbitrary state-action tuples), Zhang et al. [79] investigated a natural model-based algorithm, which performs planning (e.g., value iteration) on an empirical MG derived from samples produced non-adaptively by the generative model. Focusing on stationary discounted inﬁnite-horizon MGs, their algorithm ﬁnds an ε-approximate NE with eO(H3SA1A2 / ε2) samples. In parallel, Liu et al. [43] studied non-stationary ﬁnite-horizon MGs with online exploration, and obtained similar sample complexity bounds, i.e., eO(H4SA1A2 / ε2) samples or eO(H3SA1A2 / ε2) episodes for learning an ε-approximate NE. While these bounds achieve minimax-optimal dependency on the horizon H, a major drawback emerges — commonly referred to as the curse of multiple agents; namely, these results scale proportionally with the total number of joint actions (i.e., Q 1≤i≤2 Ai), a quantity that blows up exponentially with the number of players."

> _[Introduction — "Example: inadequacy ...", V-learning]_

"V-learning for online exploration settings. Focusing on online exploration settings, Bai et al. [5], Jin et al. [31] proposed an algorithm called V-learning that leverages the advances in online adversarial learning (e.g., adversarial bandits) to circumvent the curse of multiple agents. This algorithm provably yields an ε-approximate NE in non-stationary ﬁnite-horizon MGs using eO(H6S(A1 + A2) / ε2) samples or eO(H5S(A1 + A2) / ε2) episodes, which effectively brings down the sample size scaling (2) from A1A2 (i.e., the number of joint actions) to A1 + A2 (i.e., the sum of individual actions). It is worth pointing out, however, that this theory appears sub-optimal in terms of the horizon dependency, as it is a factor of H2 above the minimax lower bound."

> _[Introduction — key issues / main contributions]_

"While the above summary focuses on two-player zero-sum MGs, it unveils a fundamental issue surrounding the sample efﬁciency of learning equilibria; that is, all existing results in this front — irrespective of the sampling mechanism in use — fall short of overcoming at least one of the two major hurdles: (i) the curse of multiple agents, and (ii) the barrier of long horizon."

> _[Introduction — on algorithmic ideas]_

"The proposed algorithm is inspired by two key algorithmic ideas in RL and bandit literature: (i) optimism in the face of uncertainty (by leveraging upper conﬁdence bounds (UCBs) in value estimation), and (ii) online and adversarial learning (particularly the Follow-the-Regularized-Leader (FTRL) algorithm). ... The efﬁcacy of FTRL in breaking the curse of multiple agents has been illustrated in Jin et al. [31], Song et al. [63], Mao and Ba¸sar [44]. To improve horizon dependency, one needs to exploit connections between the performance of FTRL and certain variances."

> _[Section 3.2 — Sample complexity comparison with prior art, CCE in multi-player general-sum MGs]_

"Liu et al. [43] provided the ﬁrst non-asymptotic result on learning CCE in the exploration setting; the model-based algorithm studied therein learns an ε-CCE using eO(H5S2 Qm i=1 Ai / ε2) samples or eO(H4S2 Qm i=1 Ai / ε2) episodes which is sub-optimal in terms of the dependency on both H and S and suffers from the curse of multiple agents. A more recent strand of works focused on a type of online RL algorithms called V-learning, which exploited the effectiveness of adversarial learning subroutines in overcoming the curse of multi-agents [44, 63, 31]; along this line, the state-of-the-art sample complexity bound is [31]: eO(H6S max1≤i≤m Ai / ε2) samples or eO(H5S max1≤i≤m Ai / ε2) episodes, which remains suboptimal in terms of the horizon dependency. As a drawback of these works, the policy returned by V-learning is non-Markovian, an issue that has been recently addressed by Daskalakis et al. [23] at the price of a much higher sample complexity."

### Cited references (resolved from the paper's bibliography)
- **[5]** Y. Bai, C. Jin, T. Yu. *Near-optimal reinforcement learning with self-play.* NeurIPS 2020.
- **[9]** N. Brown, T. Sandholm. *Superhuman AI for multiplayer poker.* Science 2019.
- **[12]** X. Chen, Y. Cheng, B. Tang. *Well-supported versus approximate Nash equilibria: Query complexity of large games.* arXiv 2015.
- **[20]** C. Daskalakis. *On the complexity of approximating a nash equilibrium.* ACM Transactions on Algorithms (TALG) 2013.
- **[21]** C. Daskalakis, P. W. Goldberg, C. H. Papadimitriou. *The complexity of computing a Nash equilibrium.* SIAM Journal on Computing 2009.
- **[22]** C. Daskalakis, D. J. Foster, N. Golowich. *Independent policy gradient methods for competitive reinforcement learning.* NeurIPS 2020.
- **[23]** C. Daskalakis, N. Golowich, K. Zhang. *The complexity of markov equilibrium in stochastic games.* arXiv 2022.
- **[28]** T. D. Hansen, P. B. Miltersen, U. Zwick. *Strategy iteration is strongly polynomial for 2-player turn-based stochastic games with a constant discount factor.* Journal of the ACM 2013.
- **[31]** C. Jin, Q. Liu, Y. Wang, T. Yu. *V-learning – a simple, efficient, decentralized algorithm for multiagent RL.* arXiv 2021.
- **[33]** Y. Jin, V. Muthukumar, A. Sidford. *The complexity of infinite-horizon general-sum stochastic games.* arXiv 2022.
- **[42]** M. L. Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994 (Elsevier).
- **[43]** Q. Liu, T. Yu, Y. Bai, C. Jin. *A sharp analysis of model-based reinforcement learning with self-play.* ICML 2021.
- **[44]** W. Mao, T. Başar. *Provably efficient reinforcement learning in decentralized general-sum Markov games.* Dynamic Games and Applications 2022.
- **[45]** L. Matignon, L. Jeanpierre, A.-I. Mouaddib. *Coordinated multi-robot exploration under communication constraints using decentralized Markov decision processes.* AAAI 2012.
- **[47]** H. Moulin, J.-P. Vial. *Strategically zero-sum games: the class of games whose completely mixed equilibria cannot be improved upon.* International Journal of Game Theory 1978.
- **[49]** J. F. Nash Jr. *Equilibrium points in n-person games.* Proceedings of the National Academy of Sciences 1950.
- **[50]** A. Ozdaglar, M. O. Sayin, K. Zhang. *Independent learning in stochastic games.* arXiv 2021.
- **[52]** J. Perolat, B. Scherrer, B. Piot, O. Pietquin. *Approximate dynamic programming for two-player zero-sum Markov games.* ICML 2015.
- **[53]** A. Rubinstein. *Settling the complexity of computing approximate two-player nash equilibria.* FOCS 2016.
- **[58]** S. Shalev-Shwartz, S. Shammah, A. Shashua. *Safe, multi-agent, reinforcement learning for autonomous driving.* arXiv 2016.
- **[59]** L. S. Shapley. *Stochastic games.* Proceedings of the National Academy of Sciences 1953.
- **[63]** Z. Song, S. Mei, Y. Bai. *When can we learn general-sum Markov games with a large number of players sample-efficiently?* arXiv 2021.
- **[66]** O. Vinyals, I. Babuschkin, W. M. Czarnecki, M. Mathieu, et al. *Grandmaster level in Starcraft II using multi-agent reinforcement learning.* Nature 2019.
- **[79]** K. Zhang, S. Kakade, T. Basar, L. Yang. *Model-based multi-agent RL in zero-sum Markov games with near-optimal sample complexity.* NeurIPS 2020.
- **[80]** K. Zhang, Z. Yang, T. Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control 2021.
