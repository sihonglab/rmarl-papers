# 79. Decentralized Byzantine-Resilient Multi-Agent Reinforcement Learning with Reward Machines in Temporally Extended Tasks

## Metadata
- **Title**: Decentralized Byzantine-Resilient Multi-Agent Reinforcement Learning with Reward Machines in Temporally Extended Tasks
- **Authors**: Anonymous authors (paper under double-blind review)
- **Affiliation**: Not specified
- **Venue**: ICLR 2026 (under review)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Byzantine/fault tolerance in cooperative MARL (a fraction of agents act arbitrarily/maliciously, sending fabricated or adversarially crafted actions/information); action perturbation; worst-case adversary
- **Method paradigm**: Belief-based Byzantine detection (probabilistic suspicion over peers), reward machines (RMs) for temporally extended / non-Markovian tasks, tabular Q-learning, two-timescale actor-critic, decentralized consensus, convergence analysis
- **Keywords**: Byzantine resilience, reward machines, cooperative MARL, belief-based detection, decentralized learning, temporally extended tasks

## TL;DR
The paper proposes a fully decentralized, central-controller-free Byzantine-resilient cooperative MARL framework that combines reward machines (to encode temporally extended task structure) with a belief-based Byzantine-detection mechanism, instantiated as two algorithms (BQL-RM and BAC-RM) with provable convergence to optimal policies / stationary points.

## Problem & Motivation
In cooperative MARL deployed on distributed systems (e.g., autonomous vehicle networks, distributed sensor arrays) agents communicate locally and a fraction may exhibit Byzantine behavior, transmitting corrupted data to undermine collective learning. Existing approaches often rely on a central controller/server (a single point of failure), impose stringent behavior requirements on agents, require episodic synchronization with high communication cost, or assume fixed adversary budgets and fail against adaptive adversaries. Standard RL frameworks assume benign agents or centralized coordination, leaving them vulnerable. Moreover, many tasks have temporal dependencies / long-term structure that standard Markovian reward functions cannot capture. The paper targets Byzantine-robust MARL in a fully decentralized setting over a time-varying network without a central coordinator, while handling temporally extended tasks.

## Robustness Setting
- **Threat model / uncertainty set**: A fraction of agents are Byzantine (type θⁱ = 1) versus defenders (θⁱ = 0); types are determined by nature, fixed within an episode, and unknown to defenders. Byzantine agents send fabricated or adversarially crafted information, modeled by sampling an action from the Byzantine policy π̂ⁱ(· | sⁱ, uⁱ, bⁱ) and replacing the defender's action. Assumption 1 bounds the number of Byzantine agents: |N| − |N_B| ≥ M|N_B| + 1 (defenders at least M times Byzantine agents). Defenders must learn a robust policy against the worst-case adversary. The method also leverages a state-adversarial MDP view.
- **Setting**: cooperative (c-MARL); fully decentralized (local agent-to-agent communication, no central coordinator); online; tabular. Defenders observe only their own and neighbors' actions/rewards, only labels associated with their own actions, and do not know other agents' types.

## Method
- Models the environment as a multi-agent labeled MDP M = (S, N, sI, A, p, γ, P, L); the reward function is replaced by a per-agent reward machine (Mealy machine) Aⁱ = ⟨U, uI, 2^P, M, δ, σ⟩ that processes label sequences to emit rewards, making temporal dependencies explicit and learnable.
- Augments each agent's state with RM state uⁱ and belief state bⁱ; each agent maintains a probabilistic belief ζⁱ_j about whether each neighbor j is Byzantine.
- Belief-based Byzantine detection (Algorithm 1): beliefs are initialized to a prior p ∈ (0,1) and updated each step by comparing a neighbor's observed action to its inferred optimal action — suspicion increases by γ⁺α(1 − ζ) when the action is non-optimal and decreases by γ⁻αζ when optimal; the belief is then discretized into defender (Bⁱ_j = 0), suspicious (1), or Byzantine (2) via thresholds β_l < β_u.
- BQL-RM (Algorithm 2): tabular Q-learning over the augmented state Qⁱ(sⁱ, uⁱ, bⁱ, aⁱ) with ε-greedy action selection, RM transitions for reward, periodic belief updates (every m steps) to isolate Byzantine agents, and Bellman updates (Eq. 3).
- BAC-RM: a two-timescale actor-critic variant (critic faster than actor) where belief-based detection ensures unbiased gradient estimates despite adversarial agents.

## Theoretical Contributions
- Theorem 1 (Belief Update Convergence): the belief update mechanism converges to the ground-truth belief state.
- Theorem 2 (Convergence of BQL-RM): the learned Q-function converges almost surely to the optimal Q-function, via the contraction property of the Bellman operator over the augmented state space and Markov-property preservation when beliefs are included as state (under finite S, U, B; infinite visitation Assumption 4; Robbins-Monro learning rates; asymptotically correct belief estimates).
- Theorem 3 (Convergence of BAC-RM): parameters converge almost surely to a stationary point of the objective under two-timescale stochastic approximation and Lipschitz continuity of policy and Q-function.

## Experiments
- **Environment/Benchmark**: Cooperative grid-world tasks with Byzantine agents — a Foraging task (6×4 grid-world, a variation of level-based foraging (LBF), three agents cooperating while one provides fabricated information) and a Search and Rescue task (presented in the Appendix).
- **Baselines**: PPO-QMIX, COMA, M3DDPG (and, more broadly, methods without reward machines).
- **Evaluation metrics**: Cumulative rewards and convergence speed.

## Key Results
- Both BQL-RM and BAC-RM outperform baselines that lack reward machines on the foraging task.
- BQL-RM achieves higher cumulative rewards and converges faster than baselines, showing the effectiveness of reward machines plus belief states for Byzantine-robust c-MARL; BAC-RM also performs well but converges more slowly.
- PPO-QMIX achieves the highest baseline performance, while COMA and M3DDPG show limited effectiveness due to inability to capture temporal dependencies.

## Limitations & Future Work
- Algorithms perform well in the tabular setting but may not scale to large state/action spaces; extending BQL-RM with function approximation is needed.
- The current belief-update mechanism compactly models agent types from observed actions; richer inference could improve detection under noisy/ambiguous observations.
- As agent numbers grow, network constraints become more central, motivating communication-efficient designs.
- Empirical performance can be sensitive to hyperparameter choices and environment dynamics.
- Future work: scaling with function approximation, learning reward-machine structure from data, and transferring the decentralized resilient framework to real multi-robot and networked systems.

## Relevance to Survey
This paper sits on the Byzantine/fault-tolerance line of robust MARL, distinguished by being fully decentralized (no central controller) and by integrating reward machines for temporally extended / non-Markovian tasks. It connects the belief-based / Bayesian-game detection theme (treating adversarial agents as uncertain types) with robust-aggregation and adversarial-MARL lines (M3DDPG, ROMAX, RADAR), and bridges to state-adversarial MDP and action-perturbation threat models. As a robustness-with-convergence-guarantee work in cooperative MARL, it complements model-uncertainty and state-uncertainty robust MARL papers in the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 1, Introduction — "Related Work." paragraph]_

"In resilient RL, there are several main approaches to handle adversarial agents. One is to use robust aggregation Huang et al. (2024); Blanchard et al. (2017), another is to use a belief mechanism for Byzantine detection Li et al. (2023) or considering adversarial agents as uncertainty in the environment He et al. (2023). Our approach combines decentralized belief updates with RMs to handle temporally extended tasks without a central coordinator."

> _[Section 1, Introduction — "Byzantine-Robust Distributed RL" sub-group]_

"Byzantine-Robust Distributed RL: Byzantine resilience in distributed systems traces to Lamport's seminal work on fault-tolerant consensus Lamport & Fischer (1982). Recent RL adaptations, such as Byzan-UCBVI Zhang et al. (2021) requires episodic synchronization, incurring high communication costs. On the other hand, clique-overweight (COW) Chen et al. (2023), proposes robust mean estimators for aggregating gradients from untrusted batches. While COW handles arbitrary batch sizes, it focuses on supervised settings and assumes a central server; a single point of failure in decentralized MARL. In contrast, our belief mechanism operates fully decentralized."

> _[Section 1, Introduction — "Adversarial MARL" sub-group]_

"Adversarial MARL: Adversarial methods like RADAR Phan et al. (2021) co-train the protagonist and antagonist agents, but require exhaustive adversary sampling, becoming intractable for large systems. M3DDPG Li et al. (2019) uses minimax optimization for worst-case perturbations but assumes fixed budgets, failing against adaptive adversaries. BARDec-POMDP Li et al. (2023) frames adversaries as Bayesian types but lacks convergence guarantees. COMA Foerster et al. (2018) and PPO-QMIX Rashid et al. (2020) excel in cooperation but require fixed agent numbers. Our work eliminates ratio assumptions and provides rigorous discrete-time analysis with convergence guarantees."

> _[Section 1, Introduction — "Belief-Based Coordination" sub-group]_

"Belief-Based Coordination: Belief systems in ad hoc teamwork Stone et al. (2010); Albrecht & Ramamoorthy (2015) enable agents to adapt to unknown teammate types. However, these methods presume cooperative agents with shared objectives, unlike our adversarial setting. Recent extensions Rahman et al. (2021) handle open teams (agents can enter and leave the team), but do not address Byzantine failures. Closest to our work is Tessler et al. (2018), which uses reward shaping for robustness, but their mechanism lacks theoretical grounding."

> _[Section 3, Methodology — Byzantine attack model background]_

"Across the current literature, some methods assume that the Byzantine agents can only send adversarial information to the defender agents, such as M3DDPG Li et al. (2019) and ROMAX Sun et al. (2022). Our method also uses state-adversarial MDP Zhang et al. (2020) since it considers the adversary during the decision-making process."

> _[Section 3.1, Adversarial Attack Model]_

"There have been studies for single-agent and multi-agent reinforcement learning where adversarial attacks are in the form of action perturbations Tessler et al. (2019); Li et al. (2019). Moreover, authors in Li et al. (2019) extend the action perturbation model to multi-agent reinforcement learning by offering a more dynamic and a less conservative alternative to existing methods by treating agent types as uncertain and using belief updates while remaining robust against adversarial attacks. Action uncertainties, often modeled as adversarial attacks like adversarial policies Gleave et al. (2019); Wu et al. (2021); Guo et al. (2021) or non-oblivious adversaries Dinh et al. (2023), represent a practical and disruptive form of attack that is difficult to mitigate. Building upon these works, we propose a realistic threat model with specific assumptions regarding attackers and defenders."

> _[Section 3.1, Adversarial Attack Model — after Assumption 2]_

"In our work, there can be more than one Byzantine agent as long as Assumption 1 holds. Despite similar methods such as Li et al. (2019), we assume that in each episode, more than one agent could be Byzantine. Additionally, the type space may be more complex, having a non-binary type space Xie et al. (2022), perturbing actions irregularly Lin et al. (2017). In a resilient cooperative multi-agent reinforcement learning setting with fixed policies, there exists a worst-case adversary that can cause the most harm to the defender agents Li et al. (2023)."

### Cited references (resolved from the paper's bibliography)
- **[Huang et al. (2024)]** Huang, Shi, Ye, Li, Du. *Self-driven entropy aggregation for byzantine-robust heterogeneous federated learning.* ICML 2024.
- **[Blanchard et al. (2017)]** Blanchard, El Mhamdi, Guerraoui, Stainer. *Machine learning with adversaries: Byzantine tolerant gradient descent.* NeurIPS 2017.
- **[Li et al. (2023)]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a bayesian game.* arXiv:2305.12872, 2023.
- **[He et al. (2023)]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research, 2023.
- **[Lamport & Fischer (1982)]** Lamport, Fischer. *Byzantine generals and transaction commit protocols.* 1982.
- **[Zhang et al. (2021)]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, 2021.
- **[Chen et al. (2023)]** Chen, Zhang, Zhang, Wang, Zhu. *Byzantine-robust online and offline distributed reinforcement learning.* AISTATS (PMLR) 2023.
- **[Phan et al. (2021)]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Li et al. (2019)]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[Foerster et al. (2018)]** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual multi-agent policy gradients (COMA).* AAAI 2018.
- **[Rashid et al. (2020)]** Rashid, Samvelyan, Schroeder de Witt, Farquhar, Foerster, Whiteson. *Monotonic value function factorisation for deep multi-agent reinforcement learning (QMIX).* JMLR 2020.
- **[Stone et al. (2010)]** Stone, Kaminka, Kraus, Rosenschein. *Ad hoc autonomous agent teams: Collaboration without pre-coordination.* AAAI 2010.
- **[Albrecht & Ramamoorthy (2015)]** Albrecht, Ramamoorthy. *A game-theoretic model and best-response learning method for ad hoc coordination in multiagent systems.* arXiv:1506.01170, 2015.
- **[Rahman et al. (2021)]** Rahman, Hopner, Christianos, Albrecht. *Towards open ad hoc teamwork using graph-based policy learning.* ICML 2021.
- **[Tessler et al. (2018)]** Tessler, Mankowitz, Mannor. *Reward constrained policy optimization.* arXiv:1805.11074, 2018.
- **[Sun et al. (2022)]** Sun, Kim, How. *ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* ICRA 2022.
- **[Zhang et al. (2020)]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Tessler et al. (2019)]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Gleave et al. (2019)]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[Wu et al. (2021)]** Wu, Guo, Wei, Xing. *Adversarial policy training against deep reinforcement learning.* USENIX Security 2021.
- **[Guo et al. (2021)]** Guo, Wu, Huang, Xing. *Adversarial policy learning in two-player competitive games.* ICML 2021.
- **[Dinh et al. (2023)]** Dinh, Mguni, Tran-Thanh, Wang, Yang. *Online markov decision processes with non-oblivious strategic adversary.* Autonomous Agents and Multi-Agent Systems, 2023.
- **[Xie et al. (2022)]** Xie, Sodhani, Finn, Pineau, Zhang. *Robust policy learning over multiple uncertainty sets.* ICML 2022.
- **[Lin et al. (2017)]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* arXiv:1703.06748, 2017.
