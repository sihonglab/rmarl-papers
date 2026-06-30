# 47. Camouflage Adversarial Attacks on Multiple Agent Systems

## Metadata
- **Title**: Camouflage Adversarial Attacks on Multiple Agent Systems
- **Authors**: Ziqing Lu, Guanlin Liu, Lifeng Lai, Weiyu Xu
- **Affiliation**: University of Iowa (Ziqing Lu, Weiyu Xu); University of California, Davis (Guanlin Liu, Lifeng Lai)
- **Venue**: Not specified (arXiv preprint, arXiv:2401.17405 [cs.MA], 30 Jan 2024)
- **Link/arXiv**: arXiv:2401.17405v1

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial attack on MARL — a new "camouflage" attack, a form of state-perception (observation) attack where attackers change the appearances of objects they control rather than directly manipulating each victim agent's measurements; the resulting delusional observations are correlated / identical across recipient agents.
- **Method paradigm**: Optimal adversarial attack design via between-step dynamic programming combined with within-step static constrained optimization (cost-constrained attack); theoretical bounding of the gap to state-perception attacks.
- **Keywords**: camouflage attack, MARL, state perception attack, dynamic programming, cost-constrained attack, Markov game

## TL;DR
The paper introduces the "camouflage attack," a new adversarial attack on MARL where attackers alter the appearances of objects they control (yielding the same/correlated delusional observations for all victim agents), designs a dynamic-programming algorithm for the optimal (and cost-constrained) camouflage attack, and shows both theoretically and numerically that it can rival the more powerful but harder-to-realize state-perception attack.

## Problem & Motivation
RL is increasingly used in safety/security-critical applications (autonomous driving, finance, recommendation, drones/robots), so studying adversarial attacks and worst-case performance is essential for building robust, trustworthy systems. Adversarial attacks on single-agent RL are relatively well studied, but attacks on MARL are not well understood, and the increased complexity of multi-agent settings may make them more fragile and harder to analyze. Prior MARL attacks (action poisoning, reward poisoning, state poisoning, environmental, mixed) target victim properties directly, while state-perception attacks freely confuse each victim into arbitrary delusional states — which is powerful but often hard to realize in practice. The paper proposes a more practical alternative: instead of directly manipulating each victim, the attacker camouflages the appearance of objects it controls, indirectly producing the same/correlated delusional observations across victims.

## Robustness Setting
- **Threat model / uncertainty set**: Attackers form a group M (|M| = m) opposing a recipient/victim group N (|N| = n). Both groups know the recipients' optimal policies; recipients are unaware of attackers. Within each time step there are two phases: (phase 1, from t−1 to t−0.5) attackers act so each recipient i perceives a delusional state s_{d,t−0.5,i}; (phase 2, from t−0.5 to t) each recipient moves according to its optimal policy applied to the delusional state. In a camouflage attack the appearance Y_{t−0.5} = g(X_{t−0.5}) of an object (true status X_{t−0.5}) is changed by a camouflage function g(·); each agent observes s_{d,t−0.5,i} = h_i(g(X_{t−0.5})) via observation function h_i. Crucially, the delusional states across victims are correlated or identical (they observe the same camouflaged objects), unlike state-perception attacks where victims can be fooled into different states. The attacker's goal is to minimize the recipients' total expected reward over T (finite) time steps. A cost-constrained variant gives all attackers a shared per-step budget B (refilled each step) with per-attacker spending b_j.
- **Setting**: competitive (attackers vs. recipients) over a multi-agent MDP / Markov game; finite-horizon (T steps); recipients act independently with a shared optimal policy; attack-design (planning) problem solved by backward dynamic programming.

## Method
- Formulate the optimal camouflage attack as a backward dynamic program over "dynamic programming states" (DPS) σ, which include all recipient/attacker conditions and the conditions of the camouflaged objects; initialize V*_T(σ_T) = 0 and work backward from t = T to t = 0.
- For the cost-constrained ("instant cost constrained") case, within each time step solve a within-step static constrained optimization (Eq. 1): minimize the expected continuation value Σ_k P(b, s_{a,t}, σ^k_{t+0.5}) V*_{t+0.5}(σ^k_{t+0.5}) over the attack allocation vector b, subject to Σ_j b_j ≤ B, valid probabilities, and b_j ≥ 0.
- Model the attack success probability as a function of budget; in one model the probability attacker j changes its object's appearance is max{b_j / C_t(x_j, y_j), 1}, with C_t(x_j, y_j) = d(s†_{a,j}, s†_{d,j}) + ε reflecting how hard the camouflage is (distance between the attacker's real position and the target camouflaged position).
- Between time steps, perform a static-optimization / dynamic-programming cycle: take the optimal objective of the within-step program as V*_t(σ), then update V*_{t−0.5}(σ_{t−0.5}) = Σ_{σ_t} P(σ_t | σ_{t−0.5}, a*_{t−0.5}) (V*_t(σ_t) + R(σ_{t−0.5}, σ_t)), recursing until all V*_t(·) are computed.

## Theoretical Contributions
- **Lemma IV.1**: For n separable functions, comparing the minimization with an equality constraint (x_1 = … = x_n) versus the unconstrained minimization, the optimal values satisfy o2 ≤ o1 ≤ o2 + min_j {C_j}, given bounding constants C_j.
- **Theorem IV.2**: Bounds the gap between the optimal camouflage attack and the optimal (free) state-perception attack within a single time step: TR^{spa}_t ≤ TR^{ca}_t ≤ TR^{spa}_t + min_j Σ_{i≠j} {C_{ij}}, under shared state/action spaces, transition matrix, reward function, identical observation functions, and a shared optimal policy. This formally shows the camouflage attack can achieve a similar effect to the state-perception attack under certain conditions.

## Experiments
- **Environment/Benchmark**: Synthetic Markov-game settings with horizon T = 5: (A) a ring with 3 states (0,1,2) and actions {left, right, stay} with stochastic transitions (2 recipients, 2 attackers; camouflage rotates the ring orientation); (B) a q×q chessboard with fixed-position attackers — a 3×3 board with 3 recipients and 2 attackers, and a 2×2 board with 2 recipients and 1 attacker; (C) cost-constrained camouflage on the 3×3 chessboard.
- **Baselines**: No attack; free state perception attack (attackers can fool each recipient into arbitrary delusional states). For the cost-constrained study, comparison across fixed per-step budgets {1, 2, 3, 4, 6, 12}.
- **Evaluation metrics**: Total expected global reward gained by all recipients over time indices 0 to 5, reported as a percentage of the no-attack reward.

## Key Results
- Ring topology: camouflage attack reduces recipients' reward to 34.4% of the no-attack reward; the free state-perception attack reaches about 33.1% — only marginally smaller than the more practical camouflage attack.
- 3×3 chessboard (attackers fixed at (1,1) and (2,1)): camouflage attack gives 39.0% of the no-attack reward vs. roughly 16.7% for the state-perception attack. On the 2×2 board: 47.3% (camouflage) vs. 43.6% (state perception).
- Cost-constrained camouflage: higher budgets yield fewer reward gains for recipients; at budget = 6 the cost-constrained camouflage attack matches the (unconstrained) optimal camouflage attack.

## Limitations & Future Work
- Not specified (no explicit limitations or future-work section in the text). The framework assumes both groups know the recipients' optimal policies, recipients share the same state/action spaces and optimal policy, and experiments use small synthetic settings (rings and small chessboards) with horizon T = 5.

## Relevance to Survey
The paper sits on the adversarial-attack-on-MARL line (specifically observation/state-perception attacks) of the robust-MARL landscape, motivating defense and worst-case evaluation. By introducing a constrained, practically realizable variant (camouflage) of state-perception attacks whose delusional observations are necessarily correlated across victims, and by theoretically bounding its gap to the more powerful free state-perception attack, it connects the threat-modeling side of robust MARL (how attackers can perturb observations) and informs what defenses must be robust against. It complements the worst-case / minimax perspective common in robust MARL by characterizing the attacker's optimal strategy via dynamic programming and cost-constrained optimization.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction]_

"Adversarial attacks and defenses against these attacks for single-agent RL systems have been relatively well studied so far [5]–[13], but adversarial attacks on multi-agent learning are still not well understood. In MARL, the model can still be based on the Markov Decision Process (MDP), but multiple players are playing in the Markov game (MG), interacting with the environment, and the environment dynamics change by the joint action of all agents. The increasing complexity of settings potentially makes MARL systems more fragile or makes it harder to analyze their robustness. New methods are introduced especially for improving/evaluating the performance of MARL systems, and evaluating worst-case adversarial attacks on MARL systems [14]–[16]. For example, [14] proposed a decentralized algorithm: V-learning that only scales with the maximum number of actions of one agent. In [15], the authors used reward loss and cost functions to evaluate the efficacy of adversarial attacks on MARL systems."

> _[Section I, Introduction]_

"In terms of the types of adversarial attacks on MARL, most proposed adversarial attacks only consider recipient (victim) agents' properties to attack, for example, the action poisoning attacks, the reward poisoning attacks, the state poisoning attacks, the environmental attacks, or the mixed attacks [5], [15], [17]–[23]. These attacks either directly change the features of agents, i.e., actions, rewards, or states of the MDP, or perturb the interactions between the agents' actions and the environments. In [24], [25], the authors proposed a form of state perception (observation) attack in deep reinforcement learning, in which attackers confuse agents with delusional states instead of changing their actual states during the game. In [26], the authors addressed the state perception attacks with cost constraints in a multi-agent system."

> _[Section I, Introduction]_

"There have been only very limited ideas of camouflage attacks studied from the perspective of dynamic systems, except for [27] which discussed essentially state perception attack for single-victim-agent dynamic systems even though the terminology "camouflage" is used. For non-dynamic systems, some works discussed improving the detection of camouflaged attacks in deep learning models [28], [29]."

### Cited references (resolved from the paper's bibliography)
- **[5]** Liu, Lai. *Provably efficient black-box action poisoning attacks against reinforcement learning.* NeurIPS 2021.
- **[6]** Sun, Zheng, Liang, Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL.* ICLR 2022.
- **[7]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* IJCAI 2017.
- **[8]** Rakhsha, Zhang, Zhu, Singla. *Reward poisoning in reinforcement learning: attacks against unknown learners in unknown environments.* arXiv 2021.
- **[9]** Sun, Huo, Huang. *Vulnerability-aware poisoning mechanism for online RL with unknown dynamics.* ICLR 2021.
- **[10]** Banihashem, Singla, Radanovic. *Defense against reward poisoning attacks in reinforcement learning.* arXiv 2021.
- **[11]** Zhang, Chen, Zhu, Sun. *Robust policy gradient against strong data corruption.* ICML 2021.
- **[12]** Chen, Du, Jamieson. *Improved corruption robust algorithms for episodic reinforcement learning.* ICML 2021.
- **[13]** Lykouris, Simchowitz, Slivkins, Sun. *Corruption-robust exploration in episodic reinforcement learning.* COLT 2021.
- **[14]** Jin, Liu, Wang, Yu. *V-learning — a simple, efficient, decentralized algorithm for multiagent reinforcement learning.* Mathematics of Operations Research, 2021.
- **[15]** Liu, Lai. *Efficient adversarial attacks on online multi-agent reinforcement learning.* arXiv:2307.07670, 2023.
- **[16]** Zhang, Ye, Bian, Xie, Liu. *Mfvfd: A multi-agent q-learning approach to cooperative and non-cooperative tasks.* Thirtieth International Joint Conference on Artificial Intelligence, 2021.
- **[17]** Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* International Conference on Decision and Game Theory for Security (Springer), 2019.
- **[18]** Zhang, Ma, Singla, Zhu. *Adaptive reward-poisoning attacks against reinforcement learning.* ICML 2020.
- **[19]** Behzadan, Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* International Conference on Machine Learning and Data Mining in Pattern Recognition (Springer), 2017.
- **[20]** Ma, Zhang, Sun, Zhu. *Policy poisoning in batch reinforcement learning and control.* NeurIPS 2019.
- **[21]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Proceedings of the Eleventh International Conference, 1994.
- **[22]** Xu, Qu, Rabinovich. *Policy resilience to environment poisoning attacks on reinforcement learning.* arXiv:2304.12151, 2023.
- **[23]** Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* International Conference on Decision and Game Theory for Security, 2019.
- **[24]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* (listed as) International Conference on Decision and Game Theory for Security, 2020.
- **[25]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[26]** Lu, Liu, Lai, Xu. *Optimal cost constrained adversarial attacks for multiple agent systems.* arXiv:2311.00859, 2023.
- **[27]** Mukherjee, Adetola. *A secure learning control strategy via dynamic camouflaging for unknown dynamical systems under attacks.* 2021 Control Technology and Applications (CCTA), 2021.
- **[28]** Zhang, Zhou, Li, Niu. *Research on camouflaged human target detection based on deep learning.* Computational Intelligence and Neuroscience, vol. 2022, 2022.
- **[29]** Tang, He. *Malicious code dynamic traffic camouflage detection based on deep reinforcement learning in power system.* 2021 International Conference on New Energy and Power Engineering (ICNEPE 2021), 2021.
