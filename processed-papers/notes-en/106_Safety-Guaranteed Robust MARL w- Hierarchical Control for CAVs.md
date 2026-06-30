# 106. Safety Guaranteed Robust Multi-Agent Reinforcement Learning with Hierarchical Control for Connected and Automated Vehicles

## Metadata
- **Title**: Safety Guaranteed Robust Multi-Agent Reinforcement Learning with Hierarchical Control for Connected and Automated Vehicles
- **Authors**: Zhili Zhang, H. M. Sabbir Ahmad, Ehsan Sabouni, Yanchao Sun, Furong Huang, Wenchao Li, Fei Miao
- **Affiliation**: University of Connecticut (CSE); Boston University (Systems Engineering & ECE); University of Maryland, College Park (CS)
- **Venue**: Not specified (arXiv:2309.11057v2 [cs.RO], 23 Sep 2024)
- **Link/arXiv**: arXiv:2309.11057v2

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation uncertainty (noisy sensor measurements, state estimation, V2X communication) for the observed locations/velocities of other vehicles, plus hard safety (collision-free) constraints under such uncertainty.
- **Method paradigm**: Hierarchical control; robust MARL via worst-case Q network augmenting MAPPO (RMAPPO); model predictive control (MPC) with robust Control Barrier Functions (CBFs); CTDE.
- **Keywords**: Connected and Automated Vehicles (CAVs), Robust MARL, worst-case Q network, Control Barrier Functions, Model Predictive Control, safety guarantees

## TL;DR
The paper proposes Safe-RMM, a hierarchical scheme where a robust MAPPO (RMAPPO) high-level policy—trained with a worst-case Q critic but no injected perturbations—coordinates CAVs, while a low-level MPC controller with robust CBFs guarantees collision-free safety under state uncertainties, achieving best evaluated safety and efficiency in CARLA mixed-traffic scenarios.

## Problem & Motivation
Coordinating and controlling Connected and Automated Vehicles (CAVs) in mixed traffic with human-driven vehicles (HDVs) is challenging because real-world state uncertainties (noisy sensors, state estimation, communication medium) can mislead learning-based decision-making and cause collisions. Most existing safe RL methods (i) assume accurate state information and (ii) define safety only in expectation over trajectories, so they cannot guarantee hard, per-time-step safety under state uncertainty. The paper aims to design optimal multi-agent coordination while ensuring hard safety constraints in the presence of imperfect observations.

## Robustness Setting
- **Threat model / uncertainty set**: Each CAV agent i has accurate self-observation but potentially perturbed observations of other vehicles (neighbors and unconnected vehicles). Uncertainty is modeled as bounded errors on observed locations and velocities, (el, ev) with ˜l = l + el, ˜v = v + ev; for the controller, measurement/process noise w(t) is bounded by ‖w(t)‖∞ ≤ ε. No prior knowledge of uncertainty distribution is required, and no perturbation is injected during training; uncertainties are applied only at test time (random error, ERRT over time, ERRV over target vehicles).
- **Setting**: Cooperative (CAVs coordinate; HDVs do not communicate/coordinate); centralized training, decentralized execution (CTDE); online RL combined with online MPC.

## Method
- **Hierarchical Safe-RMM framework**: A high-level Robust MARL policy outputs discrete planning actions per CAV (KEEP-LANE-MAX, CHANGE-LANE-LEFT/RIGHT, and k lane-keeping actions with different reference throttles), conditioned on behaviors of other CAVs and HDVs; a low-level MPC controller with CBFs executes the plan safely.
- **Robust MAPPO (RMAPPO)**: Augments MAPPO so each PPO agent keeps an actor πθi, a PPO value critic V(s), and a second worst-case Q critic Qωi(si, ai). The worst-case Q estimates the impact of state perturbations on action selection and return; it is folded into the policy objective Li(θi) (Eq. 2) together with the advantage Âi and a value-based state-regularization term Lreg, so the policy becomes robust at "vulnerable" states without simulating uncertainty during training.
- **Robust CBF-based MPC**: A path-planning map z converts high-level actions into state/action references; CBFs define a speed-dependent ellipsoidal safe region between vehicles and CLFs track references (soft constraint). Under bounded noise the robust CBF constraint (Eq. 8) takes a worst-case (min over w) form shown to keep the safe set C forward invariant, ensuring per-step collision-free control.
- **Training loop (Algorithm 1)**: During rollout the MARL action is passed to the MPC-CBF controller, which returns a safe control and an MPC-infeasibility penalty pMPC that feeds the safety reward; both critics update the actor; safety reward = collision penalty + MPC-infeasibility penalty.

## Theoretical Contributions
- Uses the robust CBF constraint (Eq. 8) whose forward-invariance of the safe set C under bounded noise is established in prior work [33], providing the per-step safety (collision-free) guarantee for the low-level controller. No new convergence/sample-complexity proofs for the MARL component; the robustness of RMAPPO is mostly empirical, building on the worst-case-aware framework of [9]. (Mostly empirical aside from the borrowed CBF forward-invariance guarantee.)

## Experiments
- **Environment/Benchmark**: CARLA simulator; two mixed-traffic scenarios—Intersection (3 CAVs, 2 HDVs running the red light) and Highway (3 CAVs, 3 HDVs, one HDV simulating stop-and-go). Vehicles equipped with GPS, IMU, and collision sensors. Three test-time uncertainty types: random error e_rand ∼ U(−3,3), ERRT (errors over time T), ERRV (errors on target vehicles V).
- **Baselines**: Safe-MM (same framework, "non-robust", trained without the worst-case Q); MCP (MARL-PID controller with CBF safety shield, from [8]); MP (MARL-PID without shielding); RULE (rule-based planner with robust MPC controller, based on [35]).
- **Evaluation metrics**: Number of collisions over 50 evaluation episodes; mean discounted efficiency return (velocity- and goal-related rewards); evaluated under four uncertainty configurations (None, e_rand, ERRV, ERRT).

## Key Results
- Both Safe-RMM and Safe-MM achieve zero collisions across all evaluation scenarios and uncertainty settings, and rank top-two in efficiency; Safe-RMM attains comprehensively best safety and efficiency.
- MP (no safety shield) collides in 60%–80% of episodes; MCP (CBF shield) reduces collisions to ~3% on average but is conservative, with a 54% efficiency drop in Intersection and 23% drop in Highway vs. MP.
- In Intersection, Safe-RMM outperforms the non-robust Safe-MM by ~4% in efficiency across all settings; the rule-based RULE benchmark shows a 6%–13% efficiency drop with vs. without uncertainty, supporting the claim that rule-based planners lack the robustness of learning-based ones. The robustness advantage does not extend to the (less safety-critical) Highway scenario, where worst-case awareness can cause sub-optimality.

## Limitations & Future Work
- The worst-case awareness of Safe-RMM can lead to sub-optimal (overly cautious) behavior in less safety-critical scenarios such as Highway, where the robustness advantage over Safe-MM does not hold.
- Uncertainty in evaluation arises not only from injected test errors but also from initial randomization of HDV location/speed, complicating analysis.
- Future work: optimize the control policy in mixed-traffic scenarios with both RL-based and rule-based intelligent agents.

## Relevance to Survey
This paper sits on the "state/observation-uncertainty robust MARL" line applied to safety-critical autonomous driving, combining a worst-case Q (worst-case-aware robust RL) high-level policy with a CBF/MPC safety layer. It connects the robust MARL theme to the safe MARL and certified/forward-invariant safety (CBF) themes, and to communication-aware CAV coordination. It is a useful applied datapoint showing how worst-case-aware robustness ([9]) and state-adversarial robust MARL ([20], [21], [32]) integrate with hard safety guarantees in multi-agent control.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — a) Safe RL and Robust RL]_

"Different approaches have been proposed to guarantee or improve safety of the system, such as defining a safety shield or barrier assisting RL or MARL algorithm in either training or execution stage [11], [12], [13], constrained RL/MARL that learns a risk network [14], an expected cost function [15], [16], or cost constraints from language [17] that define the safety requirements. For MARL of CAV, safety-checking module with CBF-PID controller for each individual vehicle has been designed [8], [18], [19]. However, the above works assume accurate state inputs to RL or MARL algorithm from the driving environment and cannot tolerate noisy or inaccurate state input. Meanwhile, robust RL and robust MARL that only considers to train a policy under state uncertainty or model uncertainty [9], [20], [21], [22], [23] without explicitly considering the safety requirements have been proposed recently. However, in the multi-agent settings with imperfect observations, considering both safety requirements and robustness in an unified decision-making framework for CAVs still remains challenging."

> _[Section II, Related Work — b) Rule-Based Approaches]_

"Unified optimization framework poses challenges that can be addressed by decomposing the problem into hierarchical structures. Specifically, the higher level control is responsible for decision making and the lower level control is responsible for safe execution. For the higher level planner, heuristic rule based methods can be employed in which a set of rules govern the behavior of each agent within the system. For instance existing driving behavior models in mixed traffic can be found in [24], [25], [26], [27]. However, these models often lack robustness and make various assumptions about HDVs, which prevents generalization to all scenarios. MPC can be used for the lower level controller due to its ability in reference tracking and handling hard constraints in real time. In situations where imperfect observations are present, robust MPC approaches may be used, such as tube MPC [28], [29]. Nevertheless, tube-based MPC approaches require a feedback controller that can keep the actual system trajectory close to the nominal one. The calculation of such feedback controller is not trivial in multi-agent systems with nonlinear dynamics. Min-Max MPC [30] can also be adopted but it is often difficult to solve, and when it is approximated, the approximation can result in an overly conservative solution."

### Cited references (resolved from the paper's bibliography)
- **[8]** Z. Zhang, S. Han, J. Wang, F. Miao. *Spatial-temporal-aware safe multi-agent reinforcement learning of connected autonomous vehicles in challenging scenarios.* 2023 (pp. 5574–5580).
- **[9]** Y. Liang, Y. Sun, R. Zheng, F. Huang. *Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning.* NeurIPS 2022.
- **[11]** L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, A. P. Schoellig. *Safe learning in robotics: From learning-based control to safe reinforcement learning.* Annual Review of Control, Robotics, and Autonomous Systems, 2022.
- **[12]** I. ElSayed-Aly, S. Bharadwaj, C. Amato, R. Ehlers, U. Topcu, L. Feng. *Safe multi-agent reinforcement learning via shielding.* AAMAS 2021.
- **[13]** Z. Cai, H. Cao, W. Lu, L. Zhang, H. Xiong. *Safe multi-agent reinforcement learning through decentralized multiple control barrier functions.* 2021.
- **[14]** L. Wen, J. Duan, S. E. Li, S. Xu, H. Peng. *Safe reinforcement learning for autonomous vehicles through parallel constrained policy optimization.* 2020 (pp. 1–7).
- **[15]** S. Lu, K. Zhang, T. Chen, T. Başar, L. Horesh. *Decentralized policy gradient descent ascent for safe multi-agent reinforcement learning.* 2021 (vol. 35, no. 10, pp. 8767–8775).
- **[16]** S. Gu, J. Grudzien Kuba, Y. Chen, Y. Du, L. Yang, A. Knoll, Y. Yang. *Safe multi-agent reinforcement learning for multi-robot control.* Artificial Intelligence, vol. 319, 103905, 2023.
- **[17]** Z. Wang, M. Fang, T. Tomilin, F. Fang, Y. Du. *Safe multi-agent reinforcement learning with natural language constraints.* 2024 (arXiv:2405.20018).
- **[18]** J. Wang, S. Yang, Z. An, S. Han, Z. Zhang, R. Mangharam, M. Ma, F. Miao. *Multi-agent reinforcement learning guided by signal temporal logic specifications.* arXiv:2306.06808, 2023.
- **[19]** S. Han, S. Zhou, J. Wang, L. Pepin, C. Ding, J. Fu, F. Miao. *A multi-agent reinforcement learning approach for safe and efficient behavior planning of connected autonomous vehicles.* arXiv:2003.04371, 2022.
- **[20]** S. Han, S. Su, S. He, S. Han, H. Yang, F. Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **[21]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research, 2023.
- **[22]** E. Salvato, G. Fenu, E. Medvet, F. A. Pellegrino. *Crossing the reality gap: A survey on sim-to-real transferability of robot controllers in reinforcement learning.* IEEE Access, vol. 9, 2021.
- **[23]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[24]** M. Treiber, A. Hennecke, D. Helbing. *Congested traffic states in empirical observations and microscopic simulations.* Physical Review E, vol. 62, 2000.
- **[25]** A. Kesting, M. Treiber, D. Helbing. *General lane-changing model MOBIL for car-following models.* Transportation Research Record, vol. 1999, 2007.
- **[26]** C. R. Munigety. *Modelling behavioural interactions of drivers' in mixed traffic conditions.* Journal of Traffic and Transportation Engineering (English Edition), vol. 5, no. 4, 2018.
- **[27]** J. J. Olstam, A. Tapani. *Comparison of car-following models.* 2004.
- **[28]** B. T. Lopez, J.-J. E. Slotine, J. P. How. *Dynamic tube MPC for nonlinear systems.* American Control Conference (ACC) 2019.
- **[29]** D. Q. Mayne, E. C. Kerrigan. *Tube-based robust nonlinear model predictive control.* IFAC Proceedings Volumes, vol. 40, no. 12, 2007.
- **[30]** D. M. Raimondo, D. Limon, M. Lazar, L. Magni, E. F. Camacho. *Min-max model predictive control of nonlinear systems: A unifying overview on stability.* European Journal of Control, vol. 15, no. 1, 2009.
