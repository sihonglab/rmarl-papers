# 38. Tackling Uncertainties in Multi-Agent Reinforcement Learning through Integration of Agent Termination Dynamics

## Metadata
- **Title**: Tackling Uncertainties in Multi-Agent Reinforcement Learning through Integration of Agent Termination Dynamics
- **Authors**: Somnath Hazra, Pallab Dasgupta, Soumyajit Dey
- **Affiliation**: IIT Kharagpur, India (Hazra, Dey); Synopsys, Santa Clara, USA (Dasgupta)
- **Venue**: AAMAS 2025 (24th International Conference on Autonomous Agents and Multiagent Systems)
- **Link/arXiv**: arXiv:2501.12061v1 [cs.LG] 21 Jan 2025

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental stochasticity and return-distribution uncertainty (especially early-training prediction errors); safety constraints / fault tolerance derived from agent terminations (agent deaths / casualties); risk-sensitive learning.
- **Method paradigm**: Distributional RL + value factorization (DIGM), Control Barrier Function (CBF) based safety loss, multi-task gradient manipulation (PCGrad), chance-constrained / scenario-optimization safety verification.
- **Keywords**: Multi-Agent Reinforcement Learning, Distributional RL, Barrier Function, safety, agent termination, CTDE

## TL;DR
The paper proposes DBF/QBF, a cooperative MARL method that augments distributional value-factorization learning with a Control-Barrier-Function loss derived from agent terminations (casualties), using PCGrad gradient manipulation to combine it with the Huber-quantile loss, improving convergence, safety, and task completion on StarCraft II and MetaDrive.

## Problem & Motivation
Cooperative MARL suffers from inherent environmental stochasticity and collective uncertainty from many concurrently-learning agents, producing uncertain reward outcomes. Distributional RL gives a richer view of return variability, but its predicted distributions are inaccurate in early training (insufficient exploration, partial observability), and in MARL these prediction errors compound across agents. Most CTDE algorithms maximize returns and overlook this uncertainty and the additional safety constraints stochasticity induces. The authors observe an inherent fault-tolerant structure in many MAS (e.g., a team game cannot be won if too many agents are eliminated), so casualties/agent-deaths are a safety-critical signal that prior Distributional-MARL work, focused on algorithmic modifications, has not exploited to optimize the learning process.

## Robustness Setting
- **Threat model / uncertainty set**: Uncertainty from environmental stochasticity and from untrained policy parameters (epistemic uncertainty, especially early in training), captured via the learned return distribution. Safety is modeled through a barrier certificate over a "safe" region of the state space, with the unsafe condition defined by the number of agent terminations exceeding a threshold ω (e.g., ω = n−1). No explicit adversary; "robustness" here is risk-sensitivity and fault tolerance rather than worst-case model perturbation.
- **Setting**: Cooperative; CTDE (Centralized Training, Decentralized Execution); Dec-POMDP; online value-based learning with replay buffer; barrier loss computed on on-policy samples.

## Method
- **Barrier Function loss**: Defines a barrier certificate B_π(s) capturing the discounted number of agents dead at state s (B_π(s) = (agents dead at s) + γ_B B_π(s′)), interpreted as collective "vulnerability." Enforces the invariant/decrease condition via a loss L_B(π) = (1/|S|) Σ max(B_π(s′) − (1−λ_B) B_π(s), 0). A global (trajectory-level) barrier is used rather than per-agent barriers, because per-agent gradients are too weak and credit for a death cannot be attributed to a single local policy in cooperative settings.
- **Distributional return optimization**: Uses Huber-quantile regression loss with IQN to model the return distribution Z(s,u); adopts a distributional QPLEX-style factorization with a dueling-network architecture and Mean-Shape decomposition (Z = Z_mean + Z_shape) to satisfy Distributional IGM (DIGM).
- **Gradient manipulation (PCGrad)**: Combines the Huber-quantile gradient g_Q and barrier gradient g_B. When they conflict (angle θ > 90°) each is projected onto the normal plane of the other (g_Q^+, g_B^+) and combined with equal weights; when θ ≤ 90° the raw gradients are combined; equal weights β_Q = β_B = 0.5 are shown best by ablation.
- **Local policy network**: Uses IQN for sampling action distributions and a recurrent network (GRU) for partial observability; designs the input layer as a hyper-network that predicts input-layer weights from the previous step's return distribution, with ReLU enforcing non-negative (optimistic) weights to prioritize important observation components.
- Instantiated two ways: **DBF** (barrier loss integrated with distributional DMIX) and **QBF** (barrier loss integrated with non-distributional QMIX).

## Theoretical Contributions
- **Convergence (Theorem 5.1)**: In a tabular setting with direct policy parameterization and NPG step size α = (1−γ)^1.5 / sqrt(|S||U|T), assuming convergence of the underlying TD update, the optimality gap V^{π*}(s0) − E[V^{π_{m_T}}(s0)] is bounded by Θ( sqrt( |S||U| / ((1−γ)^3 T) ) ). Proof builds on the performance difference lemma and CRPO-style analysis (Supplementary Material, Section C); convergence of the underlying value decomposition is assumed (not re-proved).
- **Safety verification (Theorem 5.2)**: Frames safety as a chance-constrained program P(V^B_π(τ) ≤ ω) ≥ (1−ε) and solves it via a sampling-and-discarding scenario-optimization approach (remove k of N i.i.d. sample constraints), giving a probabilistic confidence bound relating ε, β, N, k, and the number of policy parameters m; argues ε (upper bound on probability of unsafe trajectories) is very small for finite m ≪ N and small β, k.

## Experiments
- **Environment/Benchmark**: StarCraft II Multi-Agent Challenge (SMAC) — easy scenarios (2s3z, 3s5z, 3m, 1c3s5z) and hard/super-hard scenarios (5m_vs_6m, 8m_vs_9m, 10m_vs_11m, so_many_baneling, 3s_vs_4z, 3s_vs_5z, MMM, MMM2); MetaDrive multi-agent driving (Bottleneck, Intersection, ParkingLot, Tollgate), 10 agents per environment, no respawn. PyMARL framework.
- **Baselines**: Distributional MARL — RMIX, DMIX, QDIST, CBF, RESQ (RESZ), RISKQ; traditional value-factorization MARL — VDN, QMIX, QTRAN.
- **Evaluation metrics**: Test battle win rate mean (and fraction of runs with win rate ≥ 0.6, ≥ 0.8, ≥ 0.9) for StarCraft; average return for MetaDrive.

## Key Results
- On StarCraft hard/super-hard scenarios, DBF achieves a higher fraction of test wins across thresholds (≥0.6, ≥0.8, ≥0.9) than distributional baselines; e.g., for the ≥0.6 band DBF reaches 33.83% average win rate vs. next-best RISKQ 24.50% (RMIX lowest at 9.00%).
- On StarCraft easy scenarios, integrating the barrier loss with QMIX (QBF) improves over baselines, albeit marginally (e.g., QBF 86.67% vs. QMIX 82.67% in the ≥0.8 band), also highlighting the contribution of the local-policy hyper-network.
- On MetaDrive environments, the approach (DBF) shows strong average-return performance versus DMIX, QDIST, and RISKQ baselines across the four scenarios.
- Ablations: γ_B = 0.5 performs best (tested 0.4/0.5/0.7/0.9/0.99); equal gradient weights β_Q = β_B = 0.5 outperform skewed weightings on most scenarios.

## Limitations & Future Work
- The stated objective is not to introduce a novel constrained-MARL algorithm but to evaluate incorporating agent casualties as an implicit constraint; gains on easy scenarios are only marginal.
- Convergence proof is in a tabular setting with direct policy parameterization and assumes convergence of the underlying value-decomposition/TD method rather than proving it.
- The barrier function is tied to environments where agent terminations/casualties are a meaningful, available signal; ω must be tuned (e.g., ω = n−1) and setting ω = 0 can harm returns.
- Future work: integrate the approach with other constrained-MARL methods and test robustness in environments with extrinsic (rather than intrinsic) safety constraints.

## Relevance to Survey
This paper sits at the intersection of the distributional / risk-sensitive MARL line and the safety / fault-tolerance line within robust MARL. Rather than worst-case adversarial robustness, it targets robustness to environmental stochasticity and early-training uncertainty by injecting a safety (barrier) signal derived from intrinsic system dynamics (agent deaths). It connects value-factorization MARL (VDN/QMIX/QTRAN/QPLEX), distributional MARL (C51/IQN, DFAC/DMIX, RMIX, RISKQ, ResQ), shielding-based safe MARL, and Control-Barrier-Function safety, and contributes a probabilistic (scenario-optimization) safety-verification perspective for MARL policies.

## Related Work (verbatim excerpts from the paper)
> _[Section 3, Related Work]_

"Efficiency and scalability have been central challenges in the MARL literature, particularly when estimating the global expected return (for using the reward, 𝑟 as a reference during training) from local policies (in decentralized execution). Value factorization methods have been widely adopted to address this, adhere to the IGM principle. Initial approaches like VDN [38] directly sum local value functions; while QMIX [26] uses a monotonic mixing function to ensure compatibility with the global return. QTRAN [32] introduced linear constraints to factorize the global return without the monotonicity assumption. Transformer-based architectures, such as Qatten [44], have also been explored in MARL. QPLEX [40] leverages the dueling network architecture [41] to improve learning generalization across actions, which we have used in a distributional setting in this work. Despite these advancements, the stochasticity inherent in multi-agent systems complicates the use of expected returns, often hindering training efficiency."

> _[Section 3, Related Work]_

"In parallel, distributional RL has made significant strides in the single-agent domain, introducing algorithms such as C51 [5], implicit quantile networks (IQN) [9], and others [10, 27]. More recently, there have been increasing interest in unifying distributional RL with MARL to improve risk-sensitivity and robustness. Notable works include restructuring the IGM principle to a distributional Q-learning standpoint [29, 35]; or exploring the methods for aggregating reward distributions for each action, considering the sources of risk [22, 34]. Works such as RMIX [25] integrate risk-aware metrics like Conditional Value at Risk (CVaR) into the QMIX framework, while DFAC [35] introduces the Distributional IGM (DIGM) principle, extending value factorization methods like VDN and QMIX to the distributional setting. DIGM was further refined in subsequent work [37]. ResQ [30] builds upon DMIX by introducing residual Q-functions for more accurate return estimation, while other studies have explored risk-sensitive aggregation of reward distributions [22, 34], uncertainty-aware exploration strategies [21], and modelling uncertainties related to reward [14]."

> _[Section 3, Related Work]_

"Action shielding has been another widely explored venue in RL and MARL to prevent unsafe actions during training and execution. Alshiekh et al. [3] introduced a shielding mechanism to enforce safety constraints by overriding unsafe actions based on a safety specification. Building on this, Bharadwaj et al. [6] proposed minimum-cost shields for multi-agent systems to ensure safe coordination. Factored shields curated on linear temporal logic properties [11] is another venue that has been explored for MARL. For environments with nonlinear dynamics, model predictive shielding [4] provides an efficient approach to maintaining safety. Zhang et al. proposed a multi-agent version [47], where only a subset of agents, determined by a greedy algorithm, need to use a backup policy. While these methods focus on action-level intervention, our approach incorporates safety directly into the policy learning process via the barrier function, complementing action shielding techniques by prioritizing long-term safety considerations during training."

> _[Section 3, Related Work]_

"Our work builds on these existing distributional MARL approaches by incorporating agent-specific information to enhance policy learning; unlike previous studies that focus primarily on algorithmic adaptations of MARL to the distributional context. This enables more effective training in stochastic multi-agent environments."

> _[Introduction]_

"Motivated by the gap in current research, our work addresses the uncertainties of the system via integration of safety considerations from the inherent faults in the MAS. While previous efforts have successfully combined Distributional RL with MARL to improve risk sensitivity [25, 35], these approaches largely focus on algorithmic modifications rather than optimizing the learning process by using the available information regarding the safety-critical objectives."

### Cited references (resolved from the paper's bibliography)
- **[3]** Alshiekh, Bloem, Ehlers, Könighofer, Niekum, Topcu. *Safe reinforcement learning via shielding.* AAAI 2018.
- **[4]** Bastani. *Safe reinforcement learning with nonlinear dynamics via model predictive shielding.* ACC 2021.
- **[5]** Bellemare, Dabney, Munos. *A distributional perspective on reinforcement learning.* ICML 2017.
- **[6]** Bharadwaj, Bloem, Dimitrova, Könighofer, Topcu. *Synthesis of minimum-cost shields for multi-agent systems.* ACC 2019.
- **[9]** Dabney, Ostrovski, Silver, Munos. *Implicit quantile networks for distributional reinforcement learning.* ICML 2018.
- **[10]** Dabney, Rowland, Bellemare, Munos. *Distributional reinforcement learning with quantile regression.* AAAI 2018.
- **[11]** ElSayed-Aly, Bharadwaj, Amato, Ehlers, Topcu, Feng. *Safe multi-agent reinforcement learning via shielding.* arXiv:2101.11196, 2021.
- **[14]** Hu, Sun, Chen, Huang, Chang, Sun, et al. *Distributional reward estimation for effective multi-agent deep reinforcement learning.* NeurIPS 2022.
- **[21]** Oh, Kim, Jeong, Yun. *Toward risk-based optimistic exploration for cooperative multi-agent reinforcement learning.* arXiv:2303.01768, 2023.
- **[22]** Oh, Kim, Yun. *Risk perspective exploration in distributional reinforcement learning.* arXiv:2206.14170, 2022.
- **[25]** Qiu, Wang, Yu, He, Wang, An, Obraztsova, Rabinovich. *RMIX: Risk-sensitive multi-agent reinforcement learning.* 2020.
- **[26]** Rashid, Samvelyan, Schroeder de Witt, Farquhar, Foerster, Whiteson. *Monotonic value function factorisation for deep multi-agent reinforcement learning (QMIX).* JMLR 2020.
- **[27]** Rowland, Dadashi, Kumar, Munos, Bellemare, Dabney. *Statistics and samples in distributional reinforcement learning.* ICML 2019.
- **[29]** Shen, Ma, Li, Liu, Fu, Mei, Liu, Wang. *RiskQ: Risk-sensitive multi-agent reinforcement learning value factorization.* NeurIPS 2024.
- **[30]** Shen, Qiu, Liu, Liu, Fu, Liu, Wang. *ResQ: A residual Q function-based approach for multi-agent reinforcement learning value factorization.* NeurIPS 2022.
- **[32]** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning.* ICML 2019.
- **[34]** Son, Kim, Yi, Shin. *Disentangling sources of risk for distributional multi-agent reinforcement learning.* 2021.
- **[35]** Sun, Lee, Lee. *DFAC framework: Factorizing the value function via quantile mixture for multi-agent distributional Q-learning.* ICML 2021.
- **[37]** Sun, Lee, See, Lee. *A unified framework for factorizing distributional value functions for multi-agent reinforcement learning.* JMLR 2023.
- **[38]** Sunehag, Lever, Gruslys, Czarnecki, Zambaldi, Jaderberg, Lanctot, Sonnerat, Leibo, Tuyls, et al. *Value-decomposition networks for cooperative multi-agent learning (VDN).* arXiv:1706.05296, 2017.
- **[40]** Wang, Ren, Liu, Yu, Zhang. *QPLEX: Duplex dueling multi-agent Q-learning.* arXiv:2008.01062, 2020.
- **[41]** Wang, Schaul, Hessel, van Hasselt, Lanctot, de Freitas. *Dueling network architectures for deep reinforcement learning.* ICML 2016.
- **[44]** Yang, Hao, Liao, Shao, Chen, Liu, Tang. *Qatten: A general framework for cooperative multiagent reinforcement learning.* arXiv:2002.03939, 2020.
- **[47]** Zhang, Bastani, Kumar. *MAMPS: Safe multi-agent reinforcement learning via model predictive shielding.* arXiv:1910.12639, 2019.
