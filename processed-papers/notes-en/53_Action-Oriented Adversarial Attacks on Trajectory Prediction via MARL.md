# 53. Action-Oriented Adversarial Attacks on Trajectory Prediction in Connected Autonomous Vehicles via Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Action-Oriented Adversarial Attacks on Trajectory Prediction in Connected Autonomous Vehicles via Multi-Agent Reinforcement Learning
- **Authors**: Xiaofeng Zhao, Dengfeng Sun
- **Affiliation**: School of Aeronautics and Astronautics, Purdue University, West Lafayette, IN, USA
- **Venue**: Not specified (Preprint submitted to Elsevier; not peer reviewed; available at SSRN, abstract 5348784)
- **Link/arXiv**: https://ssrn.com/abstract=5348784 ; code: https://github.com/xzhao391/Prediction-Adversarial-MARL/tree/main

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial attack on infrastructure-level trajectory prediction (perturbation injected at the prediction-output level of a V2I communication station); bounded, physically-plausible trajectory perturbations used to mislead a prediction-based safety supervisor; used as a robustness/reliability evaluation tool for trajectory planning under uncertainty.
- **Method paradigm**: Adversarial MARL; prediction-adversarial Markov decision process (PA-MDP); minimax / worst-case adversarial value function; Bellman contraction; CTDE; action-oriented (action-space-reduction) optimization to defeat the curse of dimensionality; MAPPO-based policy.
- **Keywords**: Multi-agent reinforcement learning, Connected autonomous vehicles, Trajectory prediction, Adversarial machine learning, Reliability evaluation

## TL;DR
The paper proposes AO-PA-MARL, a CTDE multi-agent reinforcement learning framework that generates bounded, coordinated black-box perturbations of infrastructure-level trajectory predictions to mislead prediction-based safety supervisors, formalizing it as a prediction-adversarial MDP (PA-MDP) with a proven optimal adversary via Bellman contraction and using action-oriented optimization to avoid the curse of dimensionality.

## Problem & Motivation
Infrastructure-assisted (V2I) trajectory prediction and centralized safety supervision are increasingly central to CAV navigation, but their centralized nature creates a critical attack surface: compromising the infrastructure-level prediction module can simultaneously endanger multiple autonomous agents. Prior adversarial work targets perception noise, planning injection, or direct state/observation manipulation, and often assumes white-box or policy-level access; the infrastructure-level trajectory-forecasting attack surface is realistic yet underexplored. The paper aims to (1) model this black-box, prediction-output threat under physically bounded perturbations, and (2) establish a systematic framework for evaluating the robustness of trajectory-planning models under realistic CAV uncertainties (multi-agent interactions, stochastic models, weather, dynamics disturbances). A key technical gap is the curse of dimensionality in continuous multi-agent trajectory action spaces, where standard methods (DDPG/TD3/MADDPG) fail to converge or yield brittle policies.

## Robustness Setting
- **Threat model / uncertainty set**: Black-box attacker that perturbs only the output of the infrastructure-level trajectory prediction module (e.g., at an RSU), with access to predicted trajectories before downstream safety logic uses them; no modification to onboard sensing/actuation and no white-box/policy-level access. Perturbations are constrained to a bounded, physically-plausible feasible set (±0.2 m position in crowd navigation; ±0.4 m position and ±0.2 rad orientation in highway merging), consistent with empirical trajectory-prediction error margins. Worst-case perturbations model real-world prediction uncertainty.
- **Setting**: Cooperative MARL for the CAVs (shared global reward, average of individual rewards) vs. an adversary whose reward is the negated CAV reward (zero-sum-like attacker objective); CTDE (centralized training, decentralized execution); partial observability (each ego vehicle observes neighbors within a 150 m longitudinal range); online RL training in simulation.

## Method
- Formalize the attack as a prediction-adversarial Markov decision process (PA-MDP), a 7-tuple over joint states, joint actions, predicted-trajectory space, feasible-perturbation set, transition dynamics, global cooperative reward, and discount factor; before the safety supervisor evaluates collisions, each adversary ν_i observes (s_i, a_i, ζ_i) and outputs perturbed predictions inside the bounded set, receiving reward = −r (negated CAV reward).
- Define an adversarial value function under the perturbed predictions and an optimal adversarial value function as the min over adversary policies; prove (Theorem 1) a Bellman operator on this value function is a γ-contraction, so by the Banach fixed-point theorem an optimal joint adversarial policy ν* exists/is unique and can be found by iterating the Bellman operator during centralized training.
- AO-PA-MARL (action-oriented): instead of searching the full continuous perturbed-trajectory space, restrict the adversary to a finite, structured set of discrete high-level action candidates; each adversary outputs action pairs (â, ă) where â is a targeted risky action and ă a set of reference safe actions; a trajectory-optimization step (Eq. 2) constructs the perturbed trajectory that maximizes the inter-agent distance for â while minimizing distances for the safe alternatives, manipulating the supervisor's safety-margin ranking.
- The adversary adapts to the coupled CAV-policy/safety-supervisor behavior: when the policy already proposes the risky action it maximizes that action's margin to suppress intervention; otherwise it inflates the risky action's margin and deflates safer alternatives; sequences of marginally-risky perturbations can accumulate over time into critical safety violations.
- Implementation builds on MAPPO with centralized critics and decentralized RNN actors; each high-level action dimension is augmented with a "no-action" option to allow variable action outputs.

## Theoretical Contributions
- Theorem 1 (Bellman contraction for the optimal adversary): the adversarial Bellman operator is a γ-contraction (0 < γ < 1), guaranteeing existence and uniqueness of the optimal adversarial value function and hence an optimal joint adversarial policy obtainable by iterative application of the operator. Otherwise mostly empirical.

## Experiments
- **Environment/Benchmark**: Two simulated environments — (1) crowd navigation: 3 autonomous vehicles among 3 human pedestrians (motion via ORCA), with a stochastic second-order linear motion model + Gaussian process noise as ground-truth predictor; (2) highway on-ramp merging (built on highway-env / OpenAI Gym): 3 CAVs merging among 3 cyclists, using MOBIL lane-change + kinematic bicycle model for CAV predictions and an MLE-trained neural network for cyclist prediction. Both are non-compliant settings (humans act independently).
- **Baselines**: Continuous-action PA-MARL variants — PA-MAPPO (MAPPO) and PA-MASAC (multi-agent soft actor-critic). Discrete-action PA-MARL is not considered due to prohibitive cost of optimizing extremely large discrete action spaces.
- **Evaluation metrics**: Training/evaluation reward curves (adversary degrades the CAV reward comprising lane-following, collision avoidance, speed) and collision rate; qualitative trajectory case studies.

## Key Results
- AO-PA-MARL consistently outperforms PA-MAPPO and PA-MASAC across both environments, achieving higher evaluation rewards, faster convergence, and better training stability while reaching high-reward policies in fewer epochs.
- AO-PA-MARL induces significantly higher collision rates than the baselines: an order-of-magnitude increase in crowd navigation and a smaller but still substantial increase in highway merging, indicating it is especially effective in densely interactive environments.
- Qualitative case studies show bounded perturbations can make a pedestrian appear to yield (deactivating the supervisor until it is too late) and can coordinate two cyclists' perturbed forecasts into a coherent strategy that deceives the supervisor into unsafe lane changes, both ending in collisions.

## Limitations & Future Work
- A current architectural limitation is potential inconsistency when multiple adversarial agents generate perturbations for the same target; a consistent perturbation-generation scheme (e.g., priority-based or consensus-driven) is identified as important future work.
- Results are in simulation only; the framework is an adversarial/robustness-evaluation (stress-test) tool rather than a defense.

## Relevance to Survey
This work sits on the adversarial-attack / robustness-evaluation line of robust MARL applied to safety-critical CAV systems. It contributes a worst-case adversarial MDP formulation (PA-MDP) with a Bellman-contraction existence proof — connecting to the robust-MDP / minimax adversarial-RL theoretical tradition — but uniquely targets the infrastructure-level prediction output rather than agent observations or actions, complementing observation-robust RL methods. It is relevant as an example of using MARL itself to expose systemic vulnerabilities in prediction-dependent cooperative coordination, and to the broader theme of evaluating/enhancing resilience of multi-agent systems under realistic uncertainty and adversarial perturbation.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"However, the centralization of prediction and control logic introduces new cybersecurity vulnerabilities. Infrastructure-level components possess privileged access to aggregated trajectory information and planning interfaces, making them attractive and impactful targets for attackers. Prior studies have shown that attacks on V2V or V2I communication channels can destabilize platoons, induce unsafe spacing, or mislead cooperative behaviors (Comert et al., 2022; Khattak et al., 2020; Li et al., 2024). We adopt a threat model grounded in these observations: the attacker compromises the infrastructure-level trajectory prediction module (e.g., at an RSU), gaining access to predicted trajectories before they are used by downstream safety logic. This scenario is consistent with real-world cyber-physical vulnerabilities observed in vehicular networks, where RSUs and cloud services are exposed to risks such as outdated firmware, weak authentication, and remote code execution (Rathore et al., 2022; Tanaji and Roychowdhury, 2024)."

> _[Introduction]_

"Our framework differs from previous adversarial frameworks by focusing on a black-box attacker who perturbs only the output of the prediction model. This access level mirrors known attack surfaces, such as falsified V2X messages or corrupted state estimates, without requiring any modification to onboard sensing or actuation (Khattak et al., 2021; Sun et al., 2023). While prior adversarial approaches target perception noise, planning injection, or direct state manipulation, our work focuses specifically on infrastructure-level trajectory forecasting—a relatively underexplored but realistic attack surface in connected autonomous vehicles."

> _[Introduction]_

"Our approach is model-agnostic and operates entirely at the prediction output level, making it broadly compatible with diverse trajectory forecasting modules. Unlike gradient-based adversarial attacks (Cao et al., 2022), which require white-box access or direct policy injection, AO-PA-MARL perturbs only the trajectory predictions used in planning—making it suitable for both generative and rule-based predictors (Bautista-Montesano and Others, 2022). In contrast to trajectory generation models like Social-GAN (Gupta et al., 2018) or CoverNet (Phan-Minh et al., 2020), which focus on behavioral realism, our approach explicitly targets vulnerabilities in safety-aware control systems. Additionally, while robust RL methods aim to withstand observation-level disturbances (Tessler et al., 2019; Wang et al., 2025), AO-PA-MARL exposes systemic weaknesses in prediction-dependent coordination under adversarial inputs. To the best of our knowledge, AO-PA-MARL is the first framework to apply multi-agent reinforcement learning for coordinated black-box perturbation of infrastructure-generated trajectory predictions. This enables systematic robustness evaluation in prediction-driven CAV systems without assuming white-box access or policy-level interference."

> _[Section 2.3, Cooperative MARL with Prediction-Based Safety Supervisor]_

"Several recent works have addressed safety issues in MARL problems (Chen et al., 2023; Elsayed-Aly et al., 2021). Our adversarial architecture builds upon the widely studied MARL with prediction-based safety supervisor, which is designed to replace unsafe actions with safer alternatives (Chen et al., 2023). To enhance safety in connected autonomous systems, a central communication station aggregates the joint state s̄ and joint action ā from all agents via vehicle-to-infrastructure (V2I) communication. A prediction-based safety supervisor, denoted by , utilizes this information to evaluate planned actions and intervene if they pose safety risks."

### Cited references (resolved from the paper's bibliography)
- **(Comert et al., 2022)** Comert, Rahman, Islam, Chowdhury. *Change point models for real-time cyber attack detection in connected vehicle environment.* IEEE Transactions on Intelligent Transportation Systems 2022.
- **(Khattak et al., 2020)** Khattak, Nair, Comert, Wang, Hou, et al. *Modeling and analyzing cyberattack effects on connected automated vehicular platoons.* Transportation Research Part C: Emerging Technologies 2020.
- **(Li et al., 2024)** Li, Zhou, Zhang, et al. *Enhancing vehicular platoon stability in the presence of communication cyberattacks: A reliable longitudinal cooperative control strategy.* Transportation Research Part C: Emerging Technologies 2024.
- **(Rathore et al., 2022)** Rathore, Hewage, Kaiwartya, Lloret. *In-vehicle communication cyber security: Challenges and solutions.* Sensors 2022.
- **(Tanaji and Roychowdhury, 2024)** Tanaji, Roychowdhury. *A survey of cybersecurity challenges and mitigation techniques for connected and autonomous vehicles.* IEEE Transactions on Intelligent Vehicles 2024.
- **(Khattak et al., 2021)** Khattak, Smith, Fontaine. *Impact of cyberattacks on safety and stability of connected and automated vehicle platoons under lane changes.* Accident Analysis & Prevention 2021.
- **(Sun et al., 2023)** Sun, Luo, Chen. *Online transportation network cyber-attack detection based on stationary sensor data.* Transportation Research Part C: Emerging Technologies 2023.
- **(Cao et al., 2022)** Cao, Xiao, Anandkumar, Xu, Pavone. *AdvDO: Realistic adversarial attacks for trajectory prediction.* ECCV 2022.
- **(Bautista-Montesano and Others, 2022)** Bautista-Montesano, et al. *Autonomous navigation at unsignalized intersections: A coupled reinforcement learning and model predictive control approach.* Transportation Research Part C: Emerging Technologies 2022.
- **(Gupta et al., 2018)** Gupta, Johnson, Fei-Fei, Savarese, Alahi. *Social GAN: Socially acceptable trajectories with generative adversarial networks.* CVPR 2018.
- **(Phan-Minh et al., 2020)** Phan-Minh, Grigore, Boulton, Beijbom, Wolff. *CoverNet: Multimodal behavior prediction using trajectory sets.* CVPR 2020.
- **(Tessler et al., 2019)** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **(Wang et al., 2025)** Wang, Ma, Liang, Yang, Wang. *Robust lane change decision for autonomous vehicles in mixed traffic: A safety-aware multi-agent adversarial reinforcement learning approach.* Transportation Research Part C: Emerging Technologies 2025.
- **(Chen et al., 2023)** Chen, Hajidavalloo, Li, Chen, Wang, Jiang, Wang. *Deep multi-agent reinforcement learning for highway on-ramp merging in mixed traffic.* IEEE Transactions on Intelligent Transportation Systems 2023.
- **(Elsayed-Aly et al., 2021)** Elsayed-Aly, Bharadwaj, Amato, Ehlers, Topcu, Feng. *Safe multi-agent reinforcement learning via shielding.* arXiv preprint arXiv:2101.11196, 2021.
