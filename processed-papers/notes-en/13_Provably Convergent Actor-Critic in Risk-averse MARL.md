# 13. Provably Convergent Actor-Critic for MARL through Risk-aversion

## Metadata
- **Title**: Provably Convergent Actor-Critic for MARL through Risk-aversion
- **Authors**: Yizhou Zhang, Eric Mazumdar
- **Affiliation**: Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, CA, USA
- **Venue**: Preprint (arXiv:2602.12386v2 [cs.MA], 29 May 2026); dated "Preprint. June 1, 2026."
- **Link/arXiv**: arXiv:2602.12386

## Taxonomy
- **Robustness / perturbation type targeted**: Strategic risk aversion (agents are risk-averse against the behaviors of other agents rather than the environment); robustness/risk-aversion modeled via an imagined adversary constrained by a divergence penalty; bounded rationality.
- **Method paradigm**: Risk-averse Quantal-Response Equilibria (RQE), behavioral game theory, convex risk measures, monotone games, contractive risk-adjusted Bellman operator, single-timescale actor-critic (faster actor / slower critic), stochastic approximation, Lyapunov drift analysis.
- **Keywords**: Risk-averse Quantal Response Equilibrium (RQE), general-sum Markov game, actor-critic, monotone games, bounded rationality, finite-sample convergence

## TL;DR
The paper proposes a single-timescale actor-critic algorithm (faster actor, slower critic) that provably converges with finite-sample guarantees to a stationary Risk-averse Quantal-Response Equilibrium (RQE) in general-sum discounted Markov games, by exploiting risk aversion and bounded rationality to regularize the game into a monotone one and make the risk-adjusted Bellman operator a contraction—claimed to be the first MARL algorithm with global convergence guarantees to stationary equilibria in general-sum discounted MGs without assuming additional game structure.

## Problem & Motivation
Learning stationary policies in infinite-horizon general-sum Markov games is a fundamental open problem in MARL: computing stationary forms of classic equilibria (Nash, even correlated/coarse correlated equilibria) is computationally intractable (PPAD-complete for Nash in general-sum normal-form games), in stark contrast to single-agent RL or zero-sum games. Recent work pivoted to non-stationary equilibria, which are tractable but require history-dependent policies whose complexity scales with the horizon and which do not reflect the stationary policies used in practice. The paper instead achieves tractability by making assumptions on agent behavior (risk aversion and bounded rationality) rather than on game structure, building on RQE, a behavioral-game-theory solution concept recently shown to be tractable in MGs.

## Robustness Setting
- **Threat model / uncertainty set**: Each player i imagines an adversary i that selects a distribution p_i over the opponent's action set to minimize player i's expected payoff, while being constrained by a penalty term D_i(p_i, π_{-i})/τ_i (a distance/divergence such as KL or reverse KL) that keeps p_i from being too far from the true opponent policy π_{-i}. The parameter τ_i controls the degree of risk aversion (larger τ_i = more risk-averse = less constrained adversary); ε_i is a temperature controlling bounded rationality (quantal response) via a convex regularizer ν_i (e.g., entropy or log-barrier). Risk aversion here is strategic (against other agents' behaviors), not against environment stochasticity.
- **Setting**: general-sum (and cooperative) Markov games, two-player focus (extendable to n-player); centralized actor-critic with policy/Q networks and a replay buffer; supports both on-policy and off-policy training; online learning through environment interaction.

## Method
- Reformulates each player's risk-averse, bounded-rational objective f_i as a minimax problem, then lifts the original 2-player game to a 4-player game (2 original players minimizing J_i and 2 adversaries minimizing J̄_i = −J_i), creating a partial zero-sum structure in each player-adversary pair; Nash equilibria of the 4-player game correspond to RQE of the original game.
- Introduces a generalized λ-monotonicity notion (diagonal strict concavity, after Rosen 1965) for the 4-player game; proves the game is monotone under conditions on only the regularizer Hessians (e.g., 16·ε_1·ε_2·τ_1·τ_2 > 1 for KL/log-barrier or reverse-KL/negative-entropy pairs), independent of payoff matrices.
- Defines a risk-averse quantal-response Bellman optimality operator T and evaluation operator T_z over Q-function pairs; shows T is a γ_0-contraction under (µ,λ)-strong monotonicity, so its fixed point yields the RQE.
- Proposes a coupled iteration rule on the joint policy z = (π, p) and Q: projected preconditioned gradient step on z with a larger step size β_t, followed by a soft Q-update with a smaller step size α_t (α_t ≪ β_t), i.e., a faster actor and slower critic; this avoids needing an RQE oracle.
- Converts this into a sample-based actor-critic algorithm (Algorithm 1) using stochastic Q-targets, plus a scalable deep-RL implementation (Algorithm 2) with policy/Q networks, double-Q, target networks, and a replay buffer (SAC-style); a risk-neutral variant (no adversaries) serves as the baseline.

## Theoretical Contributions
- **Generalized RQE tractability** (Theorems 3.1, 3.2): uniqueness and Lipschitz continuity of RQE w.r.t. payoff matrices under λ-monotonicity, with weaker risk-aversion/bounded-rationality requirements than prior work (Mazumdar et al., 2025; Zhang & Mazumdar, 2025); monotonicity conditions depend only on regularizer Hessians, not on the game.
- **Contraction of the Bellman operator** (Proposition 4.2): generalizes prior results to (µ,λ)-strong monotonicity and to KL/log-barrier regularizers.
- **Convergence of the coupled iteration rule** (Theorem 4.4): linear convergence to RQE under constant step sizes and sublinear O(1/t) under diminishing step sizes.
- **Finite-sample convergence of the actor-critic algorithm** (Theorem 4.7): finite-sample mean-square convergence bounds for both on- and off-policy variants, via a novel coupled Lyapunov drift analysis tailored to single-timescale (faster-actor/slower-critic) step sizes, relying on Bellman-operator contraction (not policy-gradient negative drift) for the negative drift. Claimed first MARL algorithm with global convergence guarantees to stationary equilibria in general-sum discounted MGs without extra game structure.

## Experiments
- **Environment/Benchmark**: (1) a normal-form Inspection Game (inspector vs. inspectee); (2) a 5×5 gridworld cooperation game with 2 agents (defection vs. cooperation zones); (3) MPE Simple Tag with 3 agents (1 fixed good agent, 2 adversaries), turned into a fully cooperative 2-adversary game.
- **Baselines**: risk-neutral version of the same actor-critic algorithm; MAPPO (Yu et al., 2022); MADDPG (Lowe et al., 2017).
- **Evaluation metrics**: convergence behavior of gradient-descent learning dynamics / policies for varying risk-aversion levels τ; MA100 (100-episode moving average) reward curves and their consistency across independent runs; final reward mean ± standard deviation.

## Key Results
- Inspection game: risk-neutral gradient descent fails to converge, while larger τ (more risk aversion, fixed ε = 0.2) yields faster convergence and induces more risk-averse behaviors (inspector less likely to inspect, inspectee more likely to comply, lower utility variance).
- Gridworld cooperation game: risk-averse training curves are much more consistent and converge much faster across 10 runs, whereas risk-neutral curves are inconsistent and may never converge; MAPPO and MADDPG baselines also fail to provide stable training curves.
- MPE Simple Tag: risk-averse training gives more consistent training curves with similar final performance; final reward (mean ± std over 5 runs): Risk-averse AC 36.74 ± 2.65, MAPPO 35.50 ± 4.91, MADDPG 30.20 ± 9.53 — i.e., simultaneously higher reward and lower variance.
- Authors note that even when some configurations do not satisfy the RQE monotonicity condition, adding a mild level of risk aversion already improves convergence empirically.

## Limitations & Future Work
- Theory focuses on the two-player case (claimed extendable to n-player) and tabular/direct-parameterization settings; some experiment configurations do not satisfy the monotonicity condition required by the theory.
- Future directions: improving sample efficiency; adapting results to linear function approximation and softmax policy parameterization; designing independent learning algorithms that do not explicitly require opponent policies; extending the RQE framework and tractability results to extensive-form and imperfect-information games.

## Relevance to Survey
This paper sits on the "risk-sensitive / risk-averse MARL" line of robust MARL and connects it to robustness via the established equivalence between robustness and risk aversion in RL (Zhang et al., 2024). It models robustness through an imagined, divergence-constrained adversary per player (a structural cousin of the "nature player" / adversarial minimax modeling used in robust MARL such as note 1 and M3DDPG), but emphasizes *strategic* robustness against other agents' behaviors rather than environment/model uncertainty. It contributes a game-theoretic equilibrium concept (RQE) with provable convergence and finite-sample guarantees in general-sum MGs, linking the robust/risk-averse MARL theme to the broader "learning in games", monotone-game, and actor-critic stochastic-approximation literatures.

## Related Work (verbatim excerpts from the paper)
> _[Appendix B, Related Work — overview and "MARL algorithms and approaches" subsection]_

"In this section we provide a detailed discussion on related work. Our work primarily considers the solution concept of RQE originally proposed by Mazumdar et al. (2025), where they proved that all CCEs of the 4-player game have their π components being an RQE of the original 2-player game, and provided an extension of the solution concept to finite-horizon Markov games. Working further on RQE, Zhang & Mazumdar (2025) studied the case where the 4-player game is monotone, and proved the uniqueness and Lipschitz continuity of RQE with respect to the payoff matrices. They also considered discounted Markov games and proved the contraction of Bellman operator under the same monotonicity condition. However, the condition provided in (Mazumdar et al., 2025) doesn't match that in (Zhang & Mazumdar, 2025) (and neither includes the other). To reconcile these disparate conditions, we introduce a generalized class of λ-monotone games and provide a condition that strictly includes both conditions. We additionally provide a practical algorithm that naturally fits into the Actor-Critic framework, not relying on the RQE oracle, which neither of the above works provides."

"Our work is situated at the intersection of algorithm design for MARL, learning in games, risk-aversion, robustness and bounded rationality decision-making and stochastic approximation (especially for convergence analysis of Actor-Critic algorithms). We list the related work for each field in the following paragraphs."

"MARL algorithms and approaches. Various distinctive MARL algorithms have been proposed and empirically tested, among which MAPPO (Yu et al., 2022) and QMIX (Rashid et al., 2020) are the most empirically successful for fully cooperative environments. For the environments where agents are not fully cooperative, MADDPG (Lowe et al., 2017), MAAC (Iqbal & Sha, 2019) and even Individual PPO (Schulman et al., 2017) have been tested to have good empirical performance (Rudolph et al., 2026). Focusing on the strategic side of MARL, several techniques have been proposed, including opponent shaping (learning with opponent-learning awareness) (Foerster et al., 2018; Lu et al., 2022), Theory of Mind (Sclar et al., 2022) and Rationality-preserving Policy optimization (Lauffer et al., 2026). Empirical studies of risk-averse MARL have also been extensively conducted (Eriksson et al., 2022; Ganesh et al., 2019; Qiu et al., 2021; Shen et al., 2023). While these methods perform well in practice, they generally lack theoretical convergence guarantees, especially in general-sum environments."

> _[Appendix B, Related Work — "Learning in normal-form and Markov games" subsection]_

"Learning in normal-form and Markov games. Parallel to empirical advances, the theoretical foundations of learning in games—both normal-form and Markov games (MGs)—have also seen significant development. In normal form games, although Nash equilibria are proven to be computationally intractable for general-sum games (Daskalakis et al., 2009), prior work developed learning algorithms like fictitious play (Robinson, 1951), MWU (Freund & Schapire, 1997) and OMD/OGDA (Daskalakis et al., 2018; Wei et al., 2021) that provably converge to Nash in zero-sum games, or to Coarse Correlated equilibria (CCEs) in general-sum games. In Markov games, Littman (1994) first formalized the notion of Markov games (discounted) and proposed minimax-Q learning that provably converges in 2-player zero-sum MGs. Bai & Jin (2020) provided the first provably sample-efficient self-play algorithm for finite-horizon zero-sum MGs achieving O(√T) regret. For finite-horizon general-sum MGs, Jin et al. (2024) proposed a V-learning framework that provably learns its CCE in polynomial complexity with respect to the number of agents, yet the CCE is typically not a Markov policy, and requires joint randomness to execute. Prior work has also assumed access to equilibrium oracles to solve Markov Games. Hu & Wellman (2003) established Nash Q-learning, which extends Q-learning in single-agent RL to multi-agent RL through solving the stage game at each state. Liu et al. (2021) refined the algorithm for better sample-complexity through the V-learning framework, and Zehfroosh & Tanner (2022) combined the ideas of Nash Q-learning and delayed Q-learning and built a new algorithm for PAC MARL."

"For general-sum games, in addition to learning CCEs, there are also works that try to learn Nash equilibrium for games with additional structure. Monderer & Shapley (1996) introduced potential games, where a single global function tracks the improvement of any agent's unilateral move, where Nash equilibria are learnable, and Fox et al. (2022) later generalized this idea to Markov potential games. Rosen (1965) introduced monotone games, where gradient dynamics converges to the unique Nash equilibrium, and many algorithms are designed and proven to have better rates of convergence (Cai & Zheng, 2023), or to be robust to noisy gradient steps (Mertikopoulos & Zhou, 2019). More recently, Even-dar et al. (2009) explored socially convex games where the (weighted) sum of player utilities is convex. There is also a line of works exploring the effectiveness of regularization for learning in games (Mertikopoulos & Sandholm, 2016; Giannou et al., 2021; Sokota et al., 2023; Cen et al., 2024). However, as shown by Mertikopoulos et al. (2018), regularization itself doesn't provide convergence guarantees even for zero-sum games without additional structure. Despite various attempts on learning in normal-form and Markov games, no existing algorithm provide provable guarantee for the most natural infinite-horizon general-sum Markov games, as is provided in our work."

> _[Appendix B, Related Work — "Risk-aversion, robustness and bounded-rationality in decision-making" subsection]_

"Risk-aversion, robustness and bounded-rationality in decision-making. The solution concept of RQE naturally unifies three paradigms that have gained significant traction in recent years: behavioral robustness, risk-aversion, and bounded rationality in decision-making. In behavioral economics, risk-aversion (Gollier, 2001; Goeree & Offerman, 2002; Goeree et al., 2003) and bounded rationality (McKelvey & Palfrey, 1992; 1995; 1998) in human decision-making has been extensively studied, showing that the solution concept of Nash equilibrium does not necessarily capture real-world human decision-making behaviors, where both risk-aversion and bounded rationality are important aspects. In reinforcement learning, robustness and risk-aversion (proven to be equivalent in (Zhang et al., 2024)) has also been studied to tackle stochasticity and uncertainty in the environment (Mihatsch & Neuneier, 2002; Shen et al., 2014). Several more recent works have focused on the theoretical foundations of risk-sensitive MARL (Gao et al., 2021; Slumbers et al., 2023; Wang et al., 2024; Yekkehkhany et al., 2020), yet most of their results still rely on the game to be structured itself. Recent work (Lanzetti et al., 2025) considered an equilibrium concept of strategically robust equilibrium sharing similar expression to RQE but a different motivation of robustness. Contrary to risk-aversion, risk-seeking has also been studied recently in MARL by Zhang et al. (2025). There are different formulations of risk-aversion used in the works above, among which our work mainly considers a class of convex risk measures proposed by Föllmer & Schied (2002), where they proposed a dual representation theorem connecting risk-aversion to regularization in agent behaviors."

"Among all these works regarding risk-aversion, our work differentiates itself in two aspects: (i) We mainly consider strategic risk-aversion, where agents are risk-averse against the behaviors of other agents rather than the environment; (ii) Our analysis do not rely on the payoff structure of the original game, but only on the level of risk-aversion and bounded rationality."

### Cited references (resolved from the paper's bibliography)
- **[Mazumdar et al., 2025]** Mazumdar, Panaganti, Shi. *Tractable multi-agent reinforcement learning through behavioral economics.* ICLR 2025.
- **[Zhang & Mazumdar, 2025]** Zhang, Mazumdar. *Convergent Q-learning for infinite-horizon general-sum Markov games through behavioral economics.* IEEE 64th Conference on Decision and Control (CDC) 2025.
- **[Yu et al., 2022]** Yu, Velu, Vinitsky, Gao, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative multi-agent games.* NeurIPS 2022.
- **[Rashid et al., 2020]** Rashid, Samvelyan, De Witt, Farquhar, Foerster, Whiteson. *Monotonic value function factorisation for deep multi-agent reinforcement learning (QMIX).* JMLR 2020.
- **[Lowe et al., 2017]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments (MADDPG).* NeurIPS (NIPS) 2017.
- **[Iqbal & Sha, 2019]** Iqbal, Sha. *Actor-attention-critic for multi-agent reinforcement learning (MAAC).* ICML 2019.
- **[Schulman et al., 2017]** Schulman, Wolski, Dhariwal, Radford, Klimov. *Proximal policy optimization algorithms (PPO).* arXiv 2017.
- **[Rudolph et al., 2026]** Rudolph, Lichtlé, Mohammadpour, Bayen, Kolter, Zhang, Farina, Vinitsky, Sokota. *Reevaluating policy gradient methods for imperfect-information games.* ICLR 2026.
- **[Foerster et al., 2018]** Foerster, Chen, Al-Shedivat, Whiteson, Abbeel, Mordatch. *Learning with opponent-learning awareness (LOLA).* AAMAS 2018.
- **[Lu et al., 2022]** Lu, Willi, De Witt, Foerster. *Model-free opponent shaping.* ICML 2022.
- **[Sclar et al., 2022]** Sclar, Neubig, Bisk. *Symmetric machine theory of mind.* ICML 2022.
- **[Lauffer et al., 2026]** Lauffer, Shah, Carroll, Seshia, Russell, Dennis. *Robust and diverse multi-agent learning via rational policy gradient.* NeurIPS 2026.
- **[Eriksson et al., 2022]** Eriksson, Basu, Alibeigi, Dimitrakakis. *Risk-sensitive Bayesian games for multi-agent reinforcement learning under policy uncertainty.* OptLearnMAS@AAMAS 2022.
- **[Ganesh et al., 2019]** Ganesh, Vadori, Xu, Zheng, Reddy, Veloso. *Reinforcement learning for market making in a multi-agent dealer market.* arXiv 2019.
- **[Qiu et al., 2021]** Qiu, Wang, Yu, Wang, He, An, Obraztsova, Rabinovich. *RMIX: Learning risk-sensitive policies for cooperative reinforcement learning agents.* NeurIPS 2021.
- **[Shen et al., 2023]** Shen, Ma, Li, Liu, Fu, Mei, Liu, Wang. *RiskQ: Risk-sensitive multi-agent reinforcement learning value factorization.* NeurIPS 2023.
- **[Daskalakis et al., 2009]** Daskalakis, Goldberg, Papadimitriou. *The complexity of computing a Nash equilibrium.* SIAM Journal on Computing 2009.
- **[Robinson, 1951]** Robinson. *An iterative method of solving a game.* Annals of Mathematics 1951.
- **[Freund & Schapire, 1997]** Freund, Schapire. *A decision-theoretic generalization of on-line learning and an application to boosting.* Journal of Computer and System Sciences 1997.
- **[Daskalakis et al., 2018]** Daskalakis, Ilyas, Syrgkanis, Zeng. *Training GANs with optimism.* ICLR 2018.
- **[Wei et al., 2021]** Wei, Lee, Zhang, Luo. *Last-iterate convergence of decentralized optimistic gradient descent/ascent in infinite-horizon competitive Markov games.* COLT 2021.
- **[Littman, 1994]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994.
- **[Bai & Jin, 2020]** Bai, Jin. *Provable self-play algorithms for competitive reinforcement learning.* ICML 2020.
- **[Jin et al., 2024]** Jin, Liu, Wang, Yu. *V-learning—a simple, efficient, decentralized algorithm for multiagent reinforcement learning.* Mathematics of Operations Research 2024.
- **[Hu & Wellman, 2003]** Hu, Wellman. *Nash Q-learning for general-sum stochastic games.* JMLR 2003.
- **[Liu et al., 2021]** Liu, Yu, Bai, Jin. *A sharp analysis of model-based reinforcement learning with self-play.* ICML 2021.
- **[Zehfroosh & Tanner, 2022]** Zehfroosh, Tanner. *PAC reinforcement learning algorithm for general-sum Markov games.* IEEE Transactions on Automatic Control 2022.
- **[Monderer & Shapley, 1996]** Monderer, Shapley. *Potential games.* Games and Economic Behavior 1996.
- **[Fox et al., 2022]** Fox, McAleer, Overman, Panageas. *Independent natural policy gradient always converges in Markov potential games.* AISTATS 2022.
- **[Rosen, 1965]** Rosen. *Existence and uniqueness of equilibrium points for concave n-person games.* Econometrica 1965.
- **[Cai & Zheng, 2023]** Cai, Zheng. *Doubly optimal no-regret learning in monotone games.* ICML 2023.
- **[Mertikopoulos & Zhou, 2019]** Mertikopoulos, Zhou. *Learning in games with continuous action sets and unknown payoff functions.* Mathematical Programming 2019.
- **[Even-dar et al., 2009]** Even-dar, Mansour, Nadav. *On the convergence of regret minimization dynamics in concave games.* STOC 2009.
- **[Mertikopoulos & Sandholm, 2016]** Mertikopoulos, Sandholm. *Learning in games via reinforcement and regularization.* Mathematics of Operations Research 2016.
- **[Giannou et al., 2021]** Giannou, Vlatakis-Gkaragkounis, Mertikopoulos. *The convergence rate of regularized learning in games: From bandits and uncertainty to optimism and beyond.* NeurIPS 2021.
- **[Sokota et al., 2023]** Sokota, D'Orazio, Kolter, Loizou, Lanctot, Mitliagkas, Brown, Kroer. *A unified approach to reinforcement learning, quantal response equilibria, and two-player zero-sum games.* ICLR 2023.
- **[Cen et al., 2024]** Cen, Wei, Chi. *Fast policy extragradient methods for competitive games with entropy regularization.* JMLR 2024.
- **[Mertikopoulos et al., 2018]** Mertikopoulos, Papadimitriou, Piliouras. *Cycles in adversarial regularized learning.* ACM-SIAM Symposium on Discrete Algorithms (SODA) 2018.
- **[Gollier, 2001]** Gollier. *The economics of risk and time.* MIT Press 2001.
- **[Goeree & Offerman, 2002]** Goeree, Offerman. *Efficiency in auctions with private and common values: An experimental study.* American Economic Review 2002.
- **[Goeree et al., 2003]** Goeree, Holt, Palfrey. *Risk averse behavior in generalized matching pennies games.* Games and Economic Behavior 2003.
- **[McKelvey & Palfrey, 1992]** McKelvey, Palfrey. *An experimental study of the centipede game.* Econometrica 1992.
- **[McKelvey & Palfrey, 1995]** McKelvey, Palfrey. *Quantal response equilibria for normal form games.* Games and Economic Behavior 1995.
- **[McKelvey & Palfrey, 1998]** McKelvey, Palfrey. *Quantal response equilibria for extensive form games.* Experimental Economics 1998.
- **[Zhang et al., 2024]** Zhang, Hu, Li. *Soft robust MDPs and risk-sensitive MDPs: Equivalence, policy gradient, and sample complexity.* ICLR 2024.
- **[Mihatsch & Neuneier, 2002]** Mihatsch, Neuneier. *Risk-sensitive reinforcement learning.* Machine Learning 2002.
- **[Shen et al., 2014]** Shen, Tobia, Sommer, Obermayer. *Risk-sensitive reinforcement learning.* Neural Computation 2014.
- **[Gao et al., 2021]** Gao, Lui, Hernandez-Leal. *Robust risk-sensitive reinforcement learning agents for trading markets.* arXiv 2021.
- **[Slumbers et al., 2023]** Slumbers, Mguni, Blumberg, McAleer, Yang, Wang. *A game-theoretic framework for managing risk in multi-agent systems.* ICML 2023.
- **[Wang et al., 2024]** Wang, Shen, Zavlanos, Johansson. *Learning of Nash equilibria in risk-averse games.* American Control Conference (ACC) 2024.
- **[Yekkehkhany et al., 2020]** Yekkehkhany, Murray, Nagi. *Risk-averse equilibrium for games.* arXiv 2020.
- **[Lanzetti et al., 2025]** Lanzetti, Fricker, Bolognani, Dörfler, Paccagnan. *Strategically robust game theory via optimal transport.* arXiv 2025.
- **[Zhang et al., 2025]** Zhang, Li, Ozdaglar, Shamma, Zardini. *Optimism as risk-seeking in multi-agent reinforcement learning.* IEEE Control Systems Letters 2025.
- **[Föllmer & Schied, 2002]** Föllmer, Schied. *Convex measures of risk and trading constraints.* Finance and Stochastics 2002.
