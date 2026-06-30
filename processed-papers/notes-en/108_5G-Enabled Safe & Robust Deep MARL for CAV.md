# 108. 5G-enabled Safe and Robust Deep Multi-agent Reinforcement Learning Framework for CAV Coordination

## Metadata
- **Title**: 5G-enabled Safe and Robust Deep Multi-agent Reinforcement Learning Framework for CAV Coordination
- **Authors**: Fei Miao, Song Han
- **Affiliation**: University of Connecticut (in cooperation with U.S. Department of Transportation, OST-R; New England University Transportation Center)
- **Venue**: NEUTC / USDOT Final Research Report, June 2025
- **Link/arXiv**: Not specified (report at www.umass.edu/neutc; associated papers at https://arxiv.org/abs/2309.11057 and https://arxiv.org/abs/2506.00982)

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation uncertainty (noisy sensor measurements, state estimation, communication medium); perturbed observations of other vehicles; sim-to-real gap; safety constraints (collision avoidance)
- **Method paradigm**: Robust MARL (worst-case Q network), MAPPO, CTDE, hierarchical control, model predictive control (MPC) with robust Control Barrier Functions (CBFs)
- **Keywords**: Connected and Automated Vehicles (CAV), Robust MARL, Safe RL, Control Barrier Functions, MPC, state uncertainty

## TL;DR
Proposes Safe-RMM, a hierarchical coordination-and-control scheme for connected and automated vehicles (CAVs) under imperfect observations: a high-level Robust Multi-Agent PPO (RMAPPO) policy augmented with a worst-case Q network for robustness to state uncertainty, combined with a low-level MPC controller using robust Control Barrier Functions for hard safety guarantees.

## Problem & Motivation
Coordinating and controlling CAVs in mixed traffic (with human-driven vehicles, HDVs) typically uses learning-based decision-making such as RL/MARL, but most existing safe RL methods (i) assume accurate state information and (ii) define safety only over the expectation of trajectories. Real CAVs face state uncertainties from noisy sensors, state estimation, and communication, where safety is highly correlated with the correctness of state information, especially around HDVs/unconnected vehicles. It remains challenging to design optimal multi-agent coordination while ensuring hard safety constraints under per-time-step state uncertainty, and there has been no hardware demonstration (small or full scale) of MARL for CAVs. The paper jointly addresses safety and robustness to state uncertainty in a unified multi-agent decision-making framework.

## Robustness Setting
- **Threat model / uncertainty set**: Each CAV agent i has accurate self-observation of its own driving state but potentially perturbed observations of other vehicles (state uncertainty arising from noisy sensor measurements, state estimation algorithms, or the communication medium). A worst-case Q network estimates the impact of state perturbations on action selection / expected return. Evaluation uses four uncertainty configurations: None (uncertainty-free), random error e_rand, and two targeting errors ETU and ETT.
- **Setting**: cooperative (mixed traffic with non-communicating HDVs); centralized training, decentralized execution (CTDE); online (trained without uncertainty, robust at test time via worst-case Q).

## Method
- Formulates Multi-Agent RL with State Uncertainty for CAVs as a tuple G = (S, A, P, r_i, õ, G, γ), where G = (N, E) is the communication network; each agent's state combines self-observation o_i, communicated neighbor observations o_{N_i}, and observations of unconnected vehicles o_{N_i}^{UN}.
- Safe-RMM is a hierarchical design with two parts: (1) Robust MAPPO (high-level coordination policy) and (2) Robust CBF-based Model Predictive Control (low-level execution).
- Robust MAPPO augments MAPPO (Yu et al., 2022) so each PPO agent has a policy network ("actor") π_i(s_i), a value network ("critic") V(s), and a second critic Q_i(s_i, a_i) approximating worst-case action values; inspired by the Worst-case-aware Robust RL framework (Liang, Sun, Zheng, & Huang, 2022). Incorporating the worst-case Q into the training objective enhances robustness to state perturbations. The MARL interacts with the MPC controller during training rollout.
- Robust MPC uses receding horizon control to map high-level actions a_i ~ π_i into primitive control inputs u_i; a path-planning function produces state/action references, and CBFs are incorporated as safety constraints to prevent collisions between agents (forward invariance property guarantees safety).
- A companion hardware framework, RSR-RSMARL, supports Real-Sim-Real (RSR) policy adaptation with V2V communication; the MARL policy is trained with a robust MARL algorithm for zero-shot transfer to hardware, with a CBF safety-shield module for per-agent safety.

## Theoretical Contributions
None / mostly empirical (the report describes the problem formulation, algorithm design, and safety via CBF forward invariance, but presents no formal convergence, sample-complexity, or equilibrium-existence proofs in the extracted text).

## Experiments
- **Environment/Benchmark**: CARLA simulator (Dosovitskiy et al., 2017) with onboard GPS, IMU, and collision sensors; two scenarios — multi-lane Intersection and Highway (with stop-and-go HDV). Hardware demonstration on F1/10th-scale autonomous vehicles with V2V communication.
- **Baselines**: Safe-MM ("non-robust" version of the same framework), MCP (MARL-PID controller with CBF safety shield, from Zhang, Han, Wang, & Miao, 2023), MP (MARL with PID controller, no safety shielding), and RULE (rule-based planner with robust MPC, based on Sabouni, Ahmad, Cassandras, & Li, 2023).
- **Evaluation metrics**: Number of collisions during evaluation (over 50 episodes) and agents' mean discounted return (rewards related to velocity and goal-achievement), reported under four uncertainty configurations (None, random error e_rand, and two targeting errors ETU and ETT).

## Key Results
- The proposed method provides the best evaluated safety and efficiency in challenging mixed-traffic environments with uncertainties (least collisions and highest efficiency return highlighted as top performance).
- Models were trained on the two scenarios for 200 episodes each and evaluated over 50 episodes per scenario across the four uncertainty configurations.
- Hardware experiments on F1/10th-scale autonomous vehicles with V2V communication demonstrate that the RSR-RSMARL framework enhances driving safety and coordination across multiple configurations.

## Limitations & Future Work
- Tube-based MPC approaches require a feedback controller keeping the actual trajectory close to the nominal one, which is non-trivial in multi-agent systems with nonlinear dynamics; Min-Max MPC is hard to solve and its approximations can be overly conservative.
- Future work: refine the methodology and deploy on electric autonomous buses on the UConn Depot campus; demonstrate hardware performance to CT DOT; develop a real-time 5G V2X resource-management/flow-scheduling solution (with Verizon) and integrate with Nvidia/Qualcomm; plan demonstration on full-scale CAV testbeds.

## Relevance to Survey
Sits at the intersection of robust MARL and safe MARL for a concrete autonomous-driving application: it targets state/observation uncertainty (rather than model/transition uncertainty) using a worst-case-Q robust-RL approach layered on MAPPO, and adds hard safety guarantees via CBF-based MPC. It connects the "state/observation-perturbation robustness" line (worst-case-aware robust RL) with the "safety constraints / shielding" line and the "sim-to-real / real-sim-real transfer" theme, and provides one of the few hardware demonstrations of robust MARL for CAVs.

## Related Work (verbatim excerpts from the paper)
> _[Motivation — "Safe RL and Robust RL" paragraph]_

"Safe RL and Robust RL: Different approaches have been proposed to guarantee or improve safety of the system, such as defining a safety shield or barrier assisting RL or MARL algorithm in either training or execution stage (Brunke, et al., 2022; Cai, Cao, Lu, Zhang, & Xiong, 2021), constrained RL/MARL that learns a risk network (Wen, Duan, Li, Xu, & Peng, 2020), an expected cost function (Lu, Zhang, Chen, Başar, & Horesh, 2021), or cost constraints from language (Wang, Fang, Tomilin, Fang, & Du, 2024) that define the safety requirements. For MARL of CAV, safety-checking module with CBF-PID controller for each individual vehicle has been designed (Wang, et al., 2023; Zhang, Han, Wang, & Miao, 2023). However, the above works assume accurate state inputs to RL or MARL algorithm from the driving environment and cannot tolerate noisy or inaccurate state input. Meanwhile, robust RL and robust MARL that only considers to train a policy under state uncertainty or model uncertainty (Liang, Sun, Zheng, & Huang, 2022; Han, Wang, Su, Shi, & Miao, 2022; Salvato, Fenu, Medvet, & Pellegrino, 2021; Pinto, Davidson, Sukthankar, & Gupta, 2017) without explicitly considering the safety requirements have been proposed recently. However, in the multi-agent settings with imperfect observations, considering both safety requirements and robustness in a unified decision-making framework for CAVs still remains challenging."

> _[Motivation — "Rule-Based Approaches" paragraph]_

"Rule-Based Approaches: Unified optimization framework poses challenges that can be addressed by decomposing the problem into hierarchical structures. Specifically, the higher-level control is responsible for decision making and the lower-level control is responsible for safe execution. For the higher-level planner, heuristic rule-based methods can be employed in which a set of rules govern the behavior of each agent within the system. For instance, existing driving behavior models in mixed traffic can be found in (Treiber, Hennecke, & Helbing, 2000; Kesting, Treiber, & Helbing, 2007; Munigety, 2018). However, these models often lack robustness and make various assumptions about HDVs, which prevents generalization to all scenarios. MPC can be used for the lower-level controller due to its ability in reference tracking and handling hard constraints in real time. In situations where imperfect observations are present, robust MPC approaches may be used, such as tube MPC (Lopez, Slotine, & How, 2019; Mayne & Kerrigan, 2007; Sinha, Harrison, Richards, & Pavone, 2022). Nevertheless, tube-based MPC approaches require a feedback controller that can keep the actual system trajectory close to the nominal one. The calculation of such feedback controller is not trivial in multi-agent systems with nonlinear dynamics. Min-Max MPC (Raimondo, Limon, Lazar, Magni, & ndez Camacho, 2009) can also be adopted but it is often difficult to solve, and when it is approximated, the approximation can result in an overly conservative solution."

### Cited references (resolved from the paper's bibliography)
- **(Brunke, et al., 2022)** Brunke, Greeff, Hall, Yuan, Zhou, Panerati, Schoellig. *Safe learning in robotics: From learning-based control to safe reinforcement learning.* Annual Review of Control, Robotics, and Autonomous Systems, 2022.
- **(Cai, Cao, Lu, Zhang, & Xiong, 2021)** Cai, Cao, Lu, Zhang, Xiong. *Safe Multi-Agent Reinforcement Learning through Decentralized Multiple Control Barrier Functions.* 2021.
- **(Wen, Duan, Li, Xu, & Peng, 2020)** Wen, Duan, Li, Xu, Peng. *Safe reinforcement learning for autonomous vehicles through parallel constrained policy optimization.* 2020.
- **(Lu, Zhang, Chen, Başar, & Horesh, 2021)** Lu, Zhang, Chen, Başar, Horesh. *Decentralized policy gradient descent ascent for safe multi-agent reinforcement learning.* 2021.
- **(Wang, Fang, Tomilin, Fang, & Du, 2024)** Wang, Fang, Tomilin, Fang, Du. *Safe Multi-agent Reinforcement Learning with Natural Language Constraints.* 2024 (arXiv:2405.20018).
- **(Wang, et al., 2023)** Wang, Yang, An, Han, Zhang, Mangharam, ... Miao. *Multi-Agent Reinforcement Learning Guided by Signal Temporal Logic Specifications.* arXiv:2306.06808, 2023.
- **(Zhang, Han, Wang, & Miao, 2023)** Zhang, Han, Wang, Miao. *Spatial-temporal-aware safe multi-agent reinforcement learning of connected autonomous vehicles in challenging scenarios.* 2023.
- **(Liang, Sun, Zheng, & Huang, 2022)** Liang, Sun, Zheng, Huang. *Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning.* NeurIPS 2022.
- **(Han, Wang, Su, Shi, & Miao, 2022)** Han, Wang, Su, Shi, Miao. *Stable and Efficient Shapley Value-Based Reward Reallocation for Multi-Agent Reinforcement Learning of Autonomous Vehicles.* 2022.
- **(Salvato, Fenu, Medvet, & Pellegrino, 2021)** Salvato, Fenu, Medvet, Pellegrino. *Crossing the reality gap: A survey on sim-to-real transferability of robot controllers in reinforcement learning.* IEEE Access, 2021.
- **(Pinto, Davidson, Sukthankar, & Gupta, 2017)** Pinto, Davidson, Sukthankar, Gupta. *Robust Adversarial Reinforcement Learning.* ICML 2017 (PMLR 70).
- **(Treiber, Hennecke, & Helbing, 2000)** Treiber, Hennecke, Helbing. *Congested Traffic States in Empirical Observations and Microscopic Simulations.* Physical Review E, 2000.
- **(Kesting, Treiber, & Helbing, 2007)** Kesting, Treiber, Helbing. *General Lane-Changing Model MOBIL for Car-Following Models.* Transportation Research Record, 2007.
- **(Munigety, 2018)** Munigety. *Modelling behavioural interactions of drivers' in mixed traffic conditions.* Journal of Traffic and Transportation Engineering (English Edition), 2018.
- **(Lopez, Slotine, & How, 2019)** Lopez, Slotine, How. *Dynamic tube MPC for nonlinear systems.* American Control Conference (ACC), 2019.
- **(Mayne & Kerrigan, 2007)** Mayne, Kerrigan. *Tube-based robust nonlinear model predictive control.* IFAC Proceedings Volumes, 2007.
- **(Sinha, Harrison, Richards, & Pavone, 2022)** Sinha, Harrison, Richards, Pavone. *Adaptive Robust Model Predictive Control with Matched and Unmatched Uncertainty.* American Control Conference, 2022 (arXiv:2104.08261).
- **(Raimondo, Limon, Lazar, Magni, & ndez Camacho, 2009)** Raimondo, Limon, Lazar, Magni, Fernández Camacho. *Min-max Model Predictive Control of Nonlinear Systems: A Unifying Overview on Stability.* European Journal of Control, 2009.
