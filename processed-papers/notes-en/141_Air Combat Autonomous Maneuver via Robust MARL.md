# 141. Air combat autonomous maneuver decision for one-on-one within visual range engagement base on robust multi-agent reinforcement learning

## Metadata
- **Title**: Air combat autonomous maneuver decision for one-on-one within visual range engagement base on robust multi-agent reinforcement learning
- **Authors**: Weiren Kong, Deyun Zhou, Kai Zhang, Zhen Yang
- **Affiliation**: Northwestern Polytechnical University, Xi'an, China
- **Venue**: 2020 IEEE 16th International Conference on Control & Automation (ICCA)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to opponent policy changes / adversarial opponent perturbation (worst-case perturbation of the opponent's action in a competitive game), addressing environment non-stationarity in the multi-agent setting.
- **Method paradigm**: Robust MADDPG (minimax / worst-case perturbation via 1-step gradient adversarial training), zero-sum Markov game, actor-critic with CTDE, potential-based reward shaping.
- **Keywords**: Robust MADDPG, air combat, reinforcement learning, maneuver strategy, zero-sum Markov game, minimax

## TL;DR
The paper applies a Robust MADDPG framework (MADDPG with a minimax module that locally approximates the worst-case opponent perturbation via a 1-step gradient) to the UCAV one-on-one within-visual-range (WVR) air combat maneuver-decision problem, modeled as a two-player zero-sum Markov game, and shows it converges better and yields less fragile policies than vanilla MADDPG.

## Problem & Motivation
UCAV one-on-one WVR (dogfight) autonomous maneuver decision is a strongly competitive, real-time task. From the viewpoint of a single UCAV the environment is non-stationary, so it cannot be modeled as an MDP and single-agent RL fails to converge (experience replay becomes invalid, and policy-gradient variance grows with the number of agents). Modeling it as a zero-sum Markov game and solving with MARL avoids needing a precise/differentiable dynamics model (which is complex, has non-differentiable modules, and is unavailable for the enemy UCAV). However, MADDPG in a strongly competitive environment is prone to learning a fragile policy that targets only a specific equilibrium and can be easily broken when the opponent changes its policy; this motivates a robust variant.

## Robustness Setting
- **Threat model / uncertainty set**: The opponent is treated as an adversary; the desired worst-case opponent perturbation `bϵ = −α∇_o Q^{μa}(s,a,o)` is locally approximated by taking a small gradient step in the direction that minimizes the agent's Q-value (multi-agent adversarial learning, MAAL). `α` is a tunable perturbation-rate coefficient. The minimax objective `J^{Ma}(θa)` uses a minimax Q-function `Q^{Ma}(s,a,o)` representing the current reward plus the discounted worst-case future return.
- **Setting**: Competitive (two-player zero-sum Markov game); centralized training, decentralized execution (CTDE); offline learning (the authors note the algorithm is "only limited to offline learning").

## Method
- Model the UCAV 1-vs-1 WVR air combat as a two-player zero-sum Markov game ⟨S, T, A, O, R⟩ with state vector (positions, speeds, heading and bank angles of blue and red UCAVs), a continuous action space (thrust acceleration `ut`, bank angular rate `u_ψ̇`), and an opposite-sign reward based on antenna train angle (ATA, λ) and aspect angle (AA, ϵ) attack-zone conditions.
- Base learner is MADDPG (DDPG extended to multi-agent with centralized critics `Q^{μa}(s,a,o)`, experience replay, target networks, "centralized training, decentralized execution").
- Robust MADDPG adds a "minimax" module following M3DDPG: instead of expensive Monte-Carlo minimization of the centralized minimax Q-function, it linearizes `Q^{Ma}(s,a,o)` and solves the local minimum with a 1-step gradient descent (MAAL), yielding the perturbed opponent action `o* = o + bϵ` used in the actor and critic updates (Eq. 12, Eq. 19); requires only one extra gradient computation, end-to-end.
- Potential-based reward shaping (PBRS) accelerates training without altering Nash equilibria: a potential `Φ(s) = Φo(s) + Φd(s) + Φv(s)` combining orientation, distance, and velocity terms is used as `Rrs = R + γΦ(s) − Φ(s′)`.

## Theoretical Contributions
None / mostly empirical. The paper reuses existing results (DPG/DDPG gradients, the M3DDPG minimax objective/MAAL gradient, and the known property that potential-based reward shaping does not alter the multi-agent Nash equilibria) rather than proving new theory.

## Experiments
- **Environment/Benchmark**: Custom Python 3 air combat simulation environment with 2-DOF kinematic/dynamics models of two UCAVs (Eq. 20). Robust MADDPG built in TensorFlow; Actor and Critic are fully connected with two hidden layers of 300 and 300 units (tanh), learning rate 10⁻³, batch size 64, max episode length 15, replay buffer 10000, OU-process exploration noise. Blue UCAV given a smaller minimum turning radius (better) than red.
- **Baselines**: MADDPG; Approximate Dynamic Programming (ADP), where the hostile UAV adopts the maximum maneuver turn-right strategy.
- **Evaluation metrics**: Convergence of average (mean) reward per episode of the blue UAV (equivalent to advantage steps ratio); win ratio in head-to-head matchups (Robust MADDPG vs MADDPG, Robust vs ADP, MA vs ADP).

## Key Results
- Both MADDPG and Robust MADDPG converge to high average reward (best value 1), but the Robust MADDPG convergence curve is better than MADDPG throughout training.
- In head-to-head matches, the Robust MADDPG policy has a slight advantage over MADDPG (about a 60% winning rate is stated for the matchup).
- ADP yields the worst policy of the three methods.

## Limitations & Future Work
- The algorithm is limited to offline learning and does not keep learning while the strategy is in use, which the authors call a major limitation.
- Future work: use "lifelong learning" and similar mechanisms so UAVs can perform distributed online learning.

## Relevance to Survey
A domain application of robust MARL: it adopts the M3DDPG minimax / worst-case-perturbation adversarial-training line (Robust MADDPG) within a two-player zero-sum Markov game to obtain less fragile competitive policies in UCAV dogfight. It connects the "adversarial opponent / opponent-policy-change robustness" theme to a concrete air-combat control task, and sits alongside other minimax/adversarial-training MARL works rather than the distributionally-robust or certified-robustness lines.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work]_

"Various studies on autonomous aerial combat have been per- formed since early 1960s. Several remarkable works have been published in literature. At present, many modeling and solving methods for autonomous decision-making of air combat maneuvers have been formed, which can be roughly divided into three categories:
(1) Based on basic ﬁghter maneuvers(BFM) library. In [3], the ﬁrst systematic study and summary on the establishment of BFM expert system is proposed. The design of the maneuver library, the control application and the maneuver recognition based on the BFM expert system was proposed, and the various problems in the maneuver decision based on the action library is elaborated in [4], [5], Based on the combination of BFM library, target prediction and impact point's calculation, an autonomous aerial combat framework for two-on-two engagements. is proposed [6].
(2) Based on optimization method. In [1], Using Approximate Dynamic Programming(ADP), a real time autonomous one-to-one air combat method is studied and the results are tested in Real-time indoor autonomous vehicle test environment (RAVEN) . In [8], Particle swarm optimization, ant colony optimization and game theory are applied on a cooperative air combat framework and the results are compared.
(3) Based on artiﬁcial intelligence method. Using genetic based machine learning, these algorithms demonstrated the ability to discover model-free tactics in an air combat environment [9], [7]. The Q-learning method generates novel actions with a designed action value function and enables a successful outmaneuvering of the target [10]."

> _[Section III.C.3, Robust MADDPG — verbatim discussion of robust MARL / minimax / adversarial training]_

"In MARL, agent's policy is very sensitive to other agents' polices in the same environment. Particularly in competitive environments, the learned policies can be easily broken when the opponents change their policies. In [18], minimax mulit-agent deep deterministic policy gradient (M3DDPG) algorithm is proposed. For robust multi-agent reinforcement learning, which leverages the minimax concept and introduces a minimax learning objective."

"Since QMa(s, a, o) is approximated by a deep learning network, solving min_o QMa(s, a, o) is very intractable. The computational cost will be very large by Monte-Carlo simulation. In [1], the paper introduce an efﬁcient and end-to-end solution, multi-agent adversarial learning (MAAL). MAAL's main idea is to treat QMa(s, a, o) as a linearized function, and then solve the local minimum of QMa(s, a, o) with a 1-step gradient descent. This idea is similar to adversarial training technique originally developed for supervised learning."

> _[Section III.C.2, MADDPG]_

"In order to solve the problem of reinforcement learning in a multi-agent environment, Lowe et al proposed the MADDPG algorithm [15], which applies the DDPG algorithm to a multi-agent environment. MADDPG algorithm puts forward the idea of "centralized training, decentralized execution, which learns a centralized Q function for each agent. MADDPG algorithm can alleviate non-stationary problems and stabilize training based on global information."

### Cited references (resolved from the paper's bibliography)
- **[1]** McGrew, How, Williams, et al. *Air-combat strategy using approximate dynamic programming.* Journal of Guidance, Control, and Dynamics, 2010, 33(5):1641-1654.
- **[3]** Gongzhang et al. *Recognition method for tactical maneuver of target in autonomous close-in air combat.* Journal of Beijing University of Aeronautics and Astronautics, 2007.
- **[4]** Shin, Lee, Kim, et al. *An autonomous aerial combat framework for two-on-two engagements based on basic fighter maneuvers.* Aerospace Science and Technology, 2018, 72:305-315.
- **[5]** Duan, Wei, Dong. *Multiple UCAVs cooperative air combat simulation platform based on PSO, ACO, and game theory.* IEEE Aerospace and Electronic Systems Magazine, 2013, 28(11):12-19.
- **[6]** Smith, Dike, Mehra, et al. *Classifier systems in combat: two-sided learning of maneuvers for advanced fighter aircraft.* Computer Methods in Applied Mechanics and Engineering, 2000, 186(2-4):421-437.
- **[7]** Ernest, Car, Schumacher, et al. *Genetic fuzzy based artificial intelligence for unmanned combat aerial vehicle control in simulated air combat missions.* Journal of Defense Management, 2016, 6(1).
- **[8]** Duan, Li, Yu. *A predator-prey particle swarm optimization approach to multiple UCAV air combat modeled by dynamic game theory.* IEEE/CAA Journal of Automatica Sinica, 2015, 2(1):11-18.
- **[9]** Luo, Shen, Wang, et al. *Air combat decision-making for cooperative multiple target attack using heuristic adaptive genetic algorithm.* 2005 International Conference on Machine Learning and Cybernetics, IEEE, 2005.
- **[10]** Liu, Ma. *A deep reinforcement learning based intelligent decision method for UCAV air combat.* Asian Simulation Conference, Springer, 2017:274-286.
- **[15]** Lowe, Wu, Tamar, et al. *Multi-agent actor-critic for mixed cooperative-competitive environments.* Advances in Neural Information Processing Systems (NeurIPS), 2017:6379-6390.
- **[18]** Li, Wu, Cui, et al. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* Proceedings of the AAAI Conference on Artificial Intelligence, 2019, 33:4213-4220.
