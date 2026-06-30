# 98. Robustness Testing for Multi-Agent Reinforcement Learning: State Perturbations on Critical Agents

## Metadata
- **Title**: Robustness Testing for Multi-Agent Reinforcement Learning: State Perturbations on Critical Agents
- **Authors**: Ziyuan Zhou, Guanjun Liu
- **Affiliation**: Department of Computer Science, Tongji University, Shanghai, China
- **Venue**: Not specified (marked "Under review"; arXiv preprint, 2023)
- **Link/arXiv**: arXiv:2306.06136v1 [cs.LG], 9 Jun 2023

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation via adversarial attacks; robustness testing of trained cooperative MARL models; targeted attacks on the states of a variable set of "critical" victim agents.
- **Method paradigm**: Adversarial attack / robustness testing; Differential Evolution (DE) based black-box selection of victims and worst-case joint actions; Sarsa-based joint action-value function for team policy evaluation; FGSM-based targeted observation perturbation.
- **Keywords**: Robustness testing, MARL, state perturbation, critical agents, Differential Evolution, adversarial attack, CTDE, SMAC

## TL;DR
The paper proposes RTCA, the first MARL robustness-testing framework with a varying set of victim agents, which uses Differential Evolution to select critical agents and advise their worst-case joint actions (scored by a Sarsa-learned joint action-value function) and then generates adversarial state perturbations on those critical agents via FGSM-style targeted attacks.

## Problem & Motivation
MARL is widely used in multi-agent systems (smart traffic, UAVs), but classical CTDE methods such as VDN and QMIX are shown to be sensitive to state perturbations caused by sensor noise or malicious attacks. Robustness testing of a trained model is essential for confirming the trustworthiness of MAS, and since the space of possible perturbations cannot be exhaustively covered, it is important to generate the most disruptive (stealthy yet damaging) adversarial states. Prior MARL attack work fixes the victim set, formulates the attack as a Stochastic Game solvable by (MA)RL, and must retrain the adversary whenever the victim changes; it also often ignores the effect of an individual agent's action on the team. Multi-agent testing faces three challenges: (1) victims are uncertain, so the testing process cannot be formulated as an SG; (2) a sub-optimal action by one agent does not necessarily cause team failure; (3) the centralized training process is usually unavailable at test time and assumes all agents act optimally, so it may not accurately evaluate team reward when agents take sub-optimal actions.

## Robustness Setting
- **Threat model / uncertainty set**: The adversary perturbs only the observations (= states, since the environment is partially observed) of a subset of victim agents to minimize the team's expected cumulative discounted reward. Perturbations are bounded as ℓ∞ with range 0.1. The adversary needs only the inputs/outputs of the joint action-value function (treated as black-box / non-differentiable), and the victim set M (number and indices) can change at every time step without retraining.
- **Setting**: Cooperative; Dec-POMDP / CTDE-trained victim models (VDN, QMIX); test-time / execution-phase attack (no adversary training required for RTCA). Formalized as State Adversarial Dec-POMDPs (SA-Dec-POMDPs).

## Method
- Defines SA-Dec-POMDPs, generalizing State-Adversarial Stochastic Games (SASG) to a setting where the victim set M is variable; shows that solving the adversary's optimal joint policy is equivalent to solving the agents' optimal joint policy where the agent action space is the adversary's adversarial-observation space.
- Step 1 (DE-based selection): Encodes the critical-agent indices and their worst joint actions as a candidate solution (a 2M-element tuple) and runs Differential Evolution (population 400, scaling factor F=0.5, crossover rate CR) to minimize the joint action-value function Qjt(τ, aM, a−M) over which agents are victims and what worst actions they take. DE is chosen because it needs only inputs/outputs (works on non-differentiable Qjt such as QMIX's mixing network) and allows M to change without retraining.
- Step 2 (Sarsa-based team evaluation): Since the true CTDE Qjt is unavailable at execution and is trained assuming all agents act optimally, the paper trains a separate joint action-value network ˜Qjt (input: environment state s and joint action a) with Sarsa during execution, using ε-greedy exploration over a fixed policy π and minimizing a Sarsa TD loss over sampled mini-batches; ˜Qjt serves as the DE objective function.
- Step 3 (targeted perturbation): Given the chosen victim indices and target (worst) actions, generates the adversarial observation with a targeted-attack loss that pushes the victim policy toward the target action and away from its clean action, solved by one-step FGSM with step size α and clipping to the valid observation range [m, n].

## Theoretical Contributions
None / mostly empirical. The paper introduces the SA-Dec-POMDP formulation (Definition 1) and argues equivalences (e.g., solving the adversary's optimal policy equals solving the Dec-POMDP agents' optimal policy), but provides no convergence, sample-complexity, or certified-robustness proofs of its own; existence/contraction properties are cited from prior SASG work [10].

## Experiments
- **Environment/Benchmark**: StarCraft Multi-Agent Challenge (SMAC) [26] on four maps: 8 Marines (8m), 2 Stalkers & 3 Zealots (2s3z), 3 Stalkers & 5 Zealots (3s5z), and 3 Stalkers & 6 Zealots (3s6z). Victim agents trained via VDN and QMIX for two million steps.
- **Baselines**: Random noise (uniform), FGSM [23], ATLA [13] (adversary trained via PPO/MAPPO), PAAD [29] (director + actor two-step adversary). Perturbation ℓ∞ range 0.1; 32 episodes per evaluation; in RTCA the victim set changes each time step, while in baselines it is randomly changed for fairness.
- **Evaluation metrics**: Winning rate (WR) and average team cumulative reward (max 20 per episode); evaluated for victim counts |M| = 0, 1, 2. Lower WR and reward indicate a stronger (better) attack.

## Key Results
- RTCA generally achieves the best (lowest) WR and reward when attacking a small number of agents, especially in heterogeneous-agent maps; e.g., on 3s5z QMIX with M=2, RTCA drives WR to 0.00 (reward 12.70±1.50) vs PAAD 0.10, FGSM 0.13, ATLA 0.81; on 3s5z VDN M=2 RTCA reaches WR 0.00 (reward 9.71±1.51).
- Random noise is a weak attack (sometimes even raising the victim's WR), and ATLA performs poorly because the joint adversarial-observation action space grows exponentially with the number of agents, making it hard for MAPPO to learn; FGSM only disrupts individual policy and ignores team cooperation; PAAD considers team effect but requires a certain victim set.
- Ablation shows QMIX's Qjt represents joint-policy quality better than VDN's; the Sarsa-learned ˜Qjt matches QMIX's Qjt and is even better in complex maps (3s5z, 3s6z), whereas VDN's Qjt is unsuitable as the DE objective. ˜Qjt also transfers across algorithms (a ˜Qjt sampled with QMIX can attack VDN agents and vice versa), suggesting use as a black-box attack.

## Limitations & Future Work
- RTCA performs relatively poorly on the 2s3z scenario for VDN because the VDN-trained model is weak there, causing the learned ˜Qjt to be worse and the worst-joint-action computation to be inaccurate. On homogeneous maps (8m) a randomly chosen agent may happen to be critical, so PAAD can outperform RTCA when attacking only one agent under QMIX.
- The framework is evaluated only on discrete-action SMAC. Future work aims to apply RTCA to continuous action spaces such as MADDPG [34] and MAAC [35] to test their robustness against observation perturbations of critical agents.

## Relevance to Survey
This paper sits on the state/observation-perturbation and adversarial-attack line of robust MARL, specifically on the testing/evaluation side rather than the defense/training side. It connects the State-Adversarial Markov Decision Process (SA-MDP) and State-Adversarial Stochastic Game (SASG) formulations to a new SA-Dec-POMDP with a variable victim set, and relates to robustness-testing frameworks (MARLSafe), optimal-adversary attacks (PAAD), and learned-adversary methods (ATLA). It is a useful reference for how adversarial state perturbations are constructed and how cooperative MARL robustness is measured, complementing defense-oriented robust MARL works.

## Related Work (verbatim excerpts from the paper)
> _[Section V, Related Work — A. Adversarial attacks on SARL]_

"An extensive body of research has been conducted on methods related to generating adversarial examples in classification tasks. Furthermore, recent studies have emerged that explore adversarial attacks in the context of SARL. Based on a survey [30], adversarial attacks on SARL can be classified into four distinct categories including perturbations to the state space, the reward function, the action space, and the model space. Huang et al. [11] utilize FGSM for creating adversarial examples of agent input states. Their findings illustrate the efficacy of adversarial attacks for the model trained by RL. Pattanaik et al. [31] propose three types of methods containing random noise, gradient-based, and stochastic gradient decrease. The sample efficient model-based adversarial attack is introduced by Weng et al. [32]. To achieve this, they propose a two-step attack framework including the learning for the dynamic environment model and the generation of the adversarial state based on the environment model. Huang et al [12] propose the State-Adversarial Markov Decision Process (SA-MDP) which indicates the optimal adversary exists. Besides, they improve the gradient-based attack in [31] and propose a robust Sarsa attack. They use Sarsa to learn the critic network in continuous action space while we use Sarsa to train the joint action-value network in a discrete one. [13] and [29] are introduced in Section 4."

> _[Section V, Related Work — B. Adversarial attacks on MARL]_

"There are few studies on adversarial attacks in MARL. Lin et al. [9] propose the method of generating adversarial states for MARL, they use a two-step attack similar to [29] which reduces the team reward by perturbing the state of only a fixed agent. Pham et al. [33] extend [32] to multi-agent setting. Guo et al. [7] propose a comprehensive robustness testing framework named MARLSafe from three aspects: state, action, and reward. In these methods, the set of victim agents is fixed, while in RTCA, the set of victim agents is variable."

> _[Introduction — prior work on robustness testing for SARL and MARL]_

"There has been a lot of robustness testing technique on Single-Agent Reinforcement Learning (SARL), such as using the adversarial attack based on the gradient of the neural network [11], [12] or constructing an adversary as an RL agent [13] to generate the adversarial observation. However, there have been a few related research to test the robustness of MARL against state perturbation of agents. Zhou et al. [10] demonstrate that the adversary for MARL can be formulated as the Stochastic Game (SG) and there exists the joint optimal adversarial state. But the influence of individual policy on teams is not considered during the attack in [7], [10]. They only generate adversarial observation misleading the victim to take actions that are not within expectations, which may not lead to the failure of team tasks. The methods in [14], [15], [9] consider the effect of individual actions on teams by constructing the adversary as SARL or MARL agent. However, the adversary is trained at the assumption that the victim is determined. When the victim changes, it needs to be retrained."

> _[Section II.B, State-Adversarial Stochastic Game]_

"In [10], the properties of SASG are discussed, including the existence and contraction of the joint optimal adversarial perturbation. And they point out that solving the joint optimal adversarial perturbation is equal to solving an SG which can be solved by MARL. Therefore, there is some research to solve this one via MARL [14], [15], [9]. However, the victim agents are certain in the training process. If the victims are changing, MARL models have to retrain. We solve this problem in the next section."

### Cited references (resolved from the paper's bibliography)
- **[7]** Guo, Chen, Hao, Yin, Yu, Li. *Towards comprehensive testing on the robustness of cooperative multi-agent reinforcement learning.* IEEE/CVF CVPR Workshops 2022.
- **[9]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[10]** Zhou, Liu. *RomFAC: A robust mean-field actor-critic reinforcement learning against adversarial perturbations on states.* arXiv preprint arXiv:2205.07229, 2022.
- **[11]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv preprint arXiv:1702.02284, 2017.
- **[12]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[13]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[14]** Han, Su, He, Han, Yang, Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv preprint arXiv:2212.02705, 2022.
- **[15]** Li, Guo, Xiu, Feng, Yu, Wang, Liu, Wu, Liu. *Attacking cooperative multi-agent reinforcement learning by adversarial minority influence.* arXiv preprint arXiv:2302.03322, 2023.
- **[29]** Sun, Zheng, Liang, Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL.* ICLR 2022.
- **[30]** Ilahi, Usama, Qadir, Janjua, Al-Fuqaha, Hoang, Niyato. *Challenges and countermeasures for adversarial attacks on deep reinforcement learning.* IEEE Transactions on Artificial Intelligence, 2022.
- **[31]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* AAMAS 2018.
- **[32]** Weng, Dvijotham, Uesato, Xiao, Gowal, Stanforth, Kohli. *Toward evaluating robustness of deep reinforcement learning with continuous control.* ICLR 2020.
- **[33]** Pham, Nguyen, Chen, Lam, Das, Weng. *Evaluating robustness of cooperative MARL: A model-based approach.* arXiv preprint arXiv:2202.03558, 2022.
