# 1. Robust Multi-Agent Reinforcement Learning with Model Uncertainty

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning with Model Uncertainty
- **Authors**: Kaiqing Zhang, Tao Sun, Yunzhe Tao, Sahika Genc, Sunil Mallya, Tamer Başar
- **Affiliation**: University of Illinois at Urbana-Champaign (ECE & CSL); Amazon Web Services
- **Venue**: NeurIPS 2020
- **Link/arXiv**: Not specified (NeurIPS 2020 paper)

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty (distribution-free uncertainty in the reward function and transition probabilities; sim-to-real gap)
- **Method paradigm**: Robust Markov game (robust stochastic game), minimax / worst-case, nature player, Q-learning, actor-critic with function approximation, game-theoretic equilibrium
- **Keywords**: Robust Markov Game, Robust Nash Equilibrium, model uncertainty, MADDPG, nature player

## TL;DR
First to formalize MARL with model uncertainty as a robust Markov game, introducing a "nature" adversarial player to model the worst case, proposing the robust Markov perfect Nash equilibrium solution concept, and giving a Q-learning algorithm with convergence guarantees plus a scalable Robust-MADDPG actor-critic algorithm.

## Problem & Motivation
In real-world multi-agent applications, agents (especially those trained in simulation) often lack perfectly accurate knowledge of the model (other agents' rewards, the joint transition), causing a sim-to-real gap where simulation-derived policies perform poorly in practice. Single-agent RL has handled such uncertainty via robust MDPs / robust (adversarial) RL, but MARL has scarcely accounted for model uncertainty in either problem formulation or algorithm design. Adding an extra adversary makes the game no longer two-agent zero-sum but general-sum, which is much harder to solve.

## Robustness Setting
- **Threat model / uncertainty set**: At each state s, compact uncertainty sets are defined for the reward (and optionally the transition): R̄ⁱ_s, P̄_s. Uncertainty is treated as the decision of an implicit "nature" player that selects worst-case model data at every state for each agent. Distribution-free (no prior probabilistic information required). For simplicity the paper mainly focuses on reward uncertainty.
- **Setting**: cooperative and competitive mixed (general-sum Markov game); centralized-training-decentralized-execution (CTDE); online (model-free Q-learning / actor-critic).

## Method
- Models the problem as a robust Markov game and gives a Bellman-type fixed-point equation: each agent maximizes its own policy while minimizing over the uncertainty set (nature); defines robust Markov perfect Nash equilibrium (RMPNE) and an equivalent form with an explicit nature player (NRMPNE).
- Proves existence of RMPNE under finite state-action spaces and compact uncertainty sets, and that nature's optimal policy can be taken to be deterministic.
- Provides value iteration when the model is known; for model-free settings gives a tabular Q-learning update (maintaining all agents' Q-values and solving a general-sum equilibrium each step), with convergence guarantees under certain conditions.
- Derives the policy gradient theorem for robust MARL (standard-PG-like for agent policies, deterministic-PG-like for nature's deterministic policy), and designs a two-timescale actor-critic (Robust-MADDPG) supporting function approximation and mini-batch updates.

## Theoretical Contributions
- Existence proof for RMPNE (Proposition 2.2).
- Convergence guarantee for Q-learning under certain conditions (following Nash-Q assumptions).
- Policy gradient theorem for robust MARL (Lemma 3.1, with gradients w.r.t. agent, nature, and transition parameters).

## Experiments
- **Environment/Benchmark**: Multi-agent particle environments: cooperative navigation, keep-away, physical deception, predator-prey.
- **Baselines**: MADDPG (no robustness), M3DDPG (robust to opponent policy changes).
- **Evaluation metrics**: Accumulated reward, success rate, number of occupied landmarks / minimum distance, average steps occupying a target, number of prey touches, etc., evaluated across cross-combinations under different reward uncertainty levels λ (truncated Gaussian noise).

## Key Results
- With no uncertainty the three methods perform similarly; as λ increases, R-MADDPG significantly outperforms MADDPG and M3DDPG across environments.
- In cooperative navigation R-MADDPG still occupies most landmarks with higher success rate.
- In keep-away / physical deception / predator-prey, fixing one side as R-MADDPG consistently yields better robustness.

## Limitations & Future Work
- Q-learning convergence for general general-sum robust Markov games holds only under restrictive conditions; solving an equilibrium each step is computationally expensive and requires maintaining all agents' Q-values.
- Mainly focuses on reward uncertainty; transition uncertainty is only addressed theoretically.
- Future: apply to more MARL scenarios and evaluate sim-to-real performance on real robots (e.g., a multi-car racing platform).

## Relevance to Survey
One of the foundational works of robust MARL, establishing the robust Markov game / robust Nash equilibrium theoretical framework and the nature-player modeling paradigm; a base reference for later distributionally robust MARL and minimax adversarial training lines. Sits on the "model/environment uncertainty" main line and the "game-theoretic equilibrium + adversarial training" method line.

## Related Work (verbatim excerpts from the paper)
> _[Introduction — "Related Work." paragraph]_

"Our work falls into the regime of MARL that originates from the seminal work [16], under the framework of Markov games [24]. Going beyond the zero-sum setting in [16], [25, 26, 27] have considered general-sum Markov games. Most of the later MARL works, either empirical or theoretical, have been built upon this Markov game model, e.g., [14, 13, 28, 29, 30, 31]. Despite the numerous advances in MARL recently, however, few of them based on Markov games have handled the uncertainty in the model, which is the focus of our work. The closest setting to ours is the recent work [32], which also considered robustness in MARL problems. Nonetheless, we highlight that the robustness there is with respect to the changes of the opponents' policies, between the training and testing phases, instead of the robustness to the model uncertainty that we consider here."

"Model uncertainty has been nicely handled in single-agent RL. Notably, one classical and rigorous formulation of robust RL is the robust MDP framework [18, 19, 20], where the model uncertainty is treated as an adversary that plays against the agent, leading to a two-agent zero-sum game. Robust RL algorithms were then developed for this setting in [21, 33, 34, 35]. Such a zero-sum game/minimax formulation has also been adopted in other works [36, 22, 37, 38], in order to handle the sim-to-real gap. Besides this worst-case modeling, [39] also considered a distributional framework to model uncertainty in MDPs, and [40] recently proposed distributionally robust RL algorithms. However, it is not yet clear how these approaches can be generalized to multi-agent settings. In fact, with an additional adversary in MARL, the underlying model is no longer two-agent zero-sum, but falls into the general-sum regime, which is much harder to solve in general [41], or develop RL algorithms for [25, 26, 27]. Motivated by the robust Markov game model in operations research [23], we attempt to make an initial step toward this direction for robust MARL."

> _[Introduction — motivation paragraph, on single-agent robust RL background]_

"In single-agent RL, such an uncertainty has been nicely handled through the lens of robust Markov decision processes (MDPs) [18, 19, 20] and robust (adversarial) RL [21, 22]. In comparison, such an uncertainty has not been fully explored in the multi-agent RL regime."

### Cited references (resolved from the paper's bibliography)
- **[13]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[14]** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[16]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* ICML 1994.
- **[17]** Balaji et al. *DeepRacer: Autonomous racing platform for experimentation with sim2real reinforcement learning.* ICRA 2020.
- **[18]** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **[19]** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 2005.
- **[20]** Wiesemann, Kuhn, Rustem. *Robust Markov decision processes.* Mathematics of Operations Research, 2013.
- **[21]** Lim, Xu, Mannor. *Reinforcement learning in robust Markov decision processes.* NeurIPS 2013.
- **[22]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[23]** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **[24]** Shapley. *Stochastic games.* PNAS 1953.
- **[25]** Hu, Wellman. *Nash Q-learning for general-sum stochastic games.* JMLR 2003.
- **[26]** Littman. *Friend-or-foe Q-learning in general-sum games.* ICML 2001.
- **[27]** Greenwald, Hall, Serrano. *Correlated Q-learning.* ICML 2003.
- **[28]** Hansen, Miltersen, Zwick. *Strategy iteration is strongly polynomial for 2-player turn-based stochastic games with a constant discount factor.* Journal of the ACM, 2013.
- **[29]** Sidford, Wang, Yang, Ye. *Solving discounted stochastic two-player games with near-optimal time and sample complexity.* AISTATS 2020.
- **[30]** Zhang, Kakade, Başar, Yang. *Model-based multi-agent RL in zero-sum Markov games with near-optimal sample complexity.* arXiv 2020.
- **[31]** Zhang, Yang, Başar. *Policy optimization provably converges to Nash equilibria in zero-sum linear quadratic games.* NeurIPS 2019.
- **[32]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[33]** Mankowitz, Mann, Bacon, Precup, Mannor. *Learning robust options.* AAAI 2018.
- **[34]** Derman, Mankowitz, Mann, Mannor. *Soft-robust actor-critic policy-gradient.* arXiv 2018.
- **[35]** Mankowitz, Levine, Jeong, Abdolmaleki, Springenberg, Mann, Hester, Riedmiller. *Robust reinforcement learning for continuous control with model misspecification.* arXiv 2019.
- **[36]** Morimoto, Doya. *Robust reinforcement learning.* Neural Computation, 2005.
- **[37]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* arXiv 2019.
- **[38]** Abdullah, Ren, Bou Ammar, Milenkovic, Luo, Zhang, Wang. *Wasserstein robust reinforcement learning.* arXiv 2019.
- **[39]** Xu, Mannor. *Distributionally robust Markov decision processes.* NeurIPS 2010.
- **[40]** Smirnova, Dohmatob, Mary. *Distributionally robust reinforcement learning.* arXiv 2019.
- **[41]** Daskalakis, Goldberg, Papadimitriou. *The complexity of computing a Nash equilibrium.* SIAM Journal on Computing, 2009.
