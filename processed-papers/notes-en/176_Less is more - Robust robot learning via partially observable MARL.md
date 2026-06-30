# 176. Less Is More: Robust Robot Learning via Partially Observable Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Less Is More: Robust Robot Learning via Partially Observable Multi-Agent Reinforcement Learning
- **Authors**: Wenshuai Zhao, Eetu-Aleksi Rantala, Sahar Salimpour, Joni Pajarinen, Jorge Peña-Queralta
- **Affiliation**: Aalto University (Dept. of Electrical Engineering and Automation), Finland; Turku Intelligent Embedded and Robotic Systems (TIERS) Lab, University of Turku, Finland; Institute of Robotics and Intelligent Systems, ETH Zurich, Switzerland
- **Venue**: Not specified (arXiv:2309.14792v2 [cs.RO], 28 Feb 2025)
- **Link/arXiv**: arXiv:2309.14792v2; Code: https://github.com/TIERS/partially-observable-marl and https://github.com/TIERS/isaac-marl-mobile-manipulation

## Taxonomy
- **Robustness / perturbation type targeted**: Agent failure / component failure (manipulator agent disablement), perturbation of an agent's initial state, system disturbances in interconnected control; robustness arising from partial (local) observability
- **Method paradigm**: MARL vs. SARL comparison; policy-gradient equivalence analysis; Dec-MDP / Dec-POMDP; decentralized control with local observations; MAPPO/PPO; illustrative decentralized PI control
- **Keywords**: Robot learning, Robust learning, Multi-agent reinforcement learning, Dec-POMDP, Mobile manipulation, partial observability, decentralized control

## TL;DR
The paper shows that splitting an inherently single-agent robot control task into multiple agents with only partial (local) observations — rather than a single centralized full-state controller — improves robustness to component failures and perturbations, after first proving that policy-gradient SARL and MARL are equivalent under full-state observation.

## Problem & Motivation
Many high-dimensional robotic tasks can be controlled either centrally (single-agent RL, SARL) or in a decentralized manner (MARL), but the relationship between the two paradigms and the criteria for choosing between them are not well-studied. Centralized controllers with global information can be brittle: when part of the system fails or is perturbed, a controller that depends on full-state information may diverge. Prior decentralized-control literature mostly tries to mitigate the limitations of local information rather than leverage its structural advantages. The authors argue that, for inherently single-agent-like tasks, deliberately giving each agent only local observations ("less is more") can yield additional robustness to perturbations and agent failures.

## Robustness Setting
- **Threat model / uncertainty set**: Robustness is tested against (1) disablement of one agent (the manipulation agent fails to move), (2) disablement plus additional perturbation of that agent's initial state (out-of-distribution from training), and (3) system disturbances (a step-function disturbance applied to one area of a two-area interconnected power system in the illustrative PI-control example). No explicit adversary or formal uncertainty set is defined; robustness is empirical and structural, arising from decentralized local observations.
- **Setting**: Fully cooperative (shared reward); Dec-MDP / Dec-POMDP; decentralized execution with local observations (centralized critic via MAPPO for training, local observations at execution); online; evaluated Sim-to-Real and Sim-to-Sim without fine-tuning.

## Method
- Analytically establishes that independent Gaussian (diagonal-covariance) policies optimized by policy-gradient SARL and MARL are equivalent under full-state observation: the joint action probability factorizes across action dimensions/agents, value and advantage estimates coincide (V(sⁱ)=V(s), A(sⁱ,aⁱ)=A(s,a)), so the SARL policy gradient equals the sum of per-agent MARL gradients (Assumption 1).
- Empirically shows that on standard cooperative MARL toy tasks (MPE Simple-Spread, Pursuit), agents achieve near-optimal performance across a wide range of limited local observation ranges, motivating deliberate use of partial observability.
- Provides an illustrative decentralized vs. centralized proportional-integral (PI) control analysis on a two-area interconnected power system, showing decentralized controllers with local observations naturally disregard disturbances in non-local observations, reducing frequency deviation.
- For the real-robot task, trains three policies in NVIDIA Isaac Sim with PPO (RLGames library): SARL and global MARL use a single MLP with separate heads (full state); partial MARL uses two separate MLPs where the base agent observes (sbase, see, starget) and the manipulator agent observes (sarm, see, starget). The reward minimizes end-effector-to-target distance with penalties for joint-limit configurations and large actions.

## Theoretical Contributions
- Proof of equivalence between SARL and MARL policy gradients under full-state observation and independent Gaussian/categorical policies (Section IV, Eqs. 1–4). Otherwise the work is mostly empirical / illustrative (the PI-control robustness result is analytical/illustrative rather than a general theorem).

## Experiments
- **Environment/Benchmark**: MPE Simple-Spread (8 agents covering 8 landmarks) and Pursuit toy MARL tasks; an illustrative two-area interconnected power system (decentralized vs. centralized PI control); a real-world modular mobile manipulator (Clearpath Husky base + Franka Emika Panda 6-DoF arm) trained in NVIDIA Isaac Sim, deployed Sim-to-Real and Sim-to-Sim in Gazebo.
- **Baselines**: SARL (centralized, full state) and MARL (global) — decentralized policies that still use global/full-state observations — compared against the proposed MARL (partial) with local observations.
- **Evaluation metrics**: Episode return / training return; for toy tasks, average return over 5 seeds with 95% CIs across observation ranges k∈{2,4,6,8} (Simple-Spread) and k∈{7,10,14} (Pursuit); for the robot, distance from end effector to target over time across three target points under three conditions (nominal, manipulator disabled, manipulator disabled + initial-state perturbation); Gazebo runs repeated 10 times per target with randomized targets in a 0.5×0.5×0.5 m³ box; frequency deviation for the PI-control example.

## Key Results
- Toy MARL tasks: performance is comparable across a relatively large range of observation ranges, indicating limited partial observation is sufficient for near-optimal decision-making.
- Real robot, nominal conditions: all three methods complete the task; SARL performs best and MARL (global)'s margin is minimal, while MARL (partial) still reaches near-optimal performance.
- Real robot, manipulator disabled: MARL (partial) outperforms the baselines and reaches the closest distances; MARL (global) diverges in all three trials (hypothesized to need more data for its two full-state policy networks), while SARL shows superior performance to MARL (global).
- Real robot, manipulator disabled + initial-state perturbation: MARL (partial) consistently outperforms the others; SARL does not always converge. Gazebo Sim-to-Sim results mirror the real-world results (MARL global consistently diverges when manipulator is disabled; only MARL partial consistently succeeds under the additional perturbation). The decentralized PI controller substantially reduces frequency deviation while the centralized controller introduces disturbance in the undisturbed area.

## Limitations & Future Work
- Real-world experiments are limited in scope and could be extended to more complex tasks with critical robustness requirements.
- It would be beneficial to formally identify the specific robot systems to which the empirical findings apply.
- A principled approach to designing observation spaces for decentralized controllers is still needed (robustness via partial observation is demonstrated only empirically).

## Relevance to Survey
This paper sits on the robust MARL landscape's "fault tolerance / agent-failure robustness" line and the "decentralized control with partial observability" theme, connecting Dec-POMDP cooperative MARL to robust robot learning. Rather than modeling an adversary or uncertainty set, it argues that structural design choices — distributing control across agents with deliberately restricted local observations — yield robustness to component failures and out-of-distribution perturbations. It is relevant to themes of robustness-via-decentralization, sim-to-real robustness, and the SARL-vs-MARL equivalence/divergence boundary, complementing adversarial and distributionally robust MARL approaches with an architectural/observation-design perspective.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — A. Multi-Agent Reinforcement Learning]_

"Deep multi-agent reinforcement learning (MARL) has exhibited success in various game tasks [11], such as StarCraft II [2] and Stratego [12]. Value decomposition methods [13], [14] and recent multi-agent policy gradient (MAPG) methods [15], [16], [1] have demonstrated significant performance across various benchmarks [3], [5], [2]. One notable example is the Multi-agent Mujoco (Ma-MuJoCo) [5] domain which splits the joints of Mujoco robot tasks [17] into different agents and formulates it as a multi-agent cooperative task. Although such Mujoco tasks were traditionally used to benchmark single-agent RL methods, MARL approaches also show competitive performance. Therefore, it motivates us to investigate the connection between MARL and SARL paradigms and their applicability to complex robotic systems."

> _[Section II, Related Work — B. Partially Observable MARL]_

"Similar to studies in classical decentralized control theory [7], the existing literature on the partial observation problem in MARL primarily focuses on mitigating the impact of partial observation. This is typically achieved by sharing more information [18] or approximating the underlying full-state belief through various methods, such as the mean-field method [19] and agent modeling [20]. In contrast, inspired by the finding that many multi-agent learning problems can be locally independent and require only local information for near-optimal performance [6], [21], we propose leveraging the inherent structure of complex robot tasks to harness the potential of partial observation."

> _[Section II, Related Work — C. MARL for Robotics]_

"MARL methods have been naturally used in multi-robot control tasks [22], [23], [24] due to their intrinsic decentralized control mechanism. However, some robot tasks can adopt either SARL or MARL methods to learn controllers. For example, in bi-arm manipulation, studies such as [25] and [26] employ MARL methods to learn decentralized controllers, whereas works like [27] and recent imitation learning studies [28], [29] develop a centralized controller for all arms. Most existing works predominantly use centralized controllers for mobile manipulation [30], [31], and few studies have explored the comparative advantages of MARL over SARL when both approaches are applicable. The closest work to ours [9] compares SARL and MARL methods for in-hand manipulation. However, unlike our approach, they allow the decentralized controllers to observe the neighbor agents' actions, which provides critical information for the agents to adapt to malfunctions compared to SARL baselines. In this paper, we instead seek the benefits of using less state information with MARL and comprehensively investigate the connection between SARL and MARL."

> _[Section I, Introduction — decentralized control background]_

"Decentralized control has been extensively studied to achieve performance comparable to centralized control in large-scale systems [6], [7]. However, these studies often focus on mitigating the limitations of local information in decentralized controllers rather than leveraging this structure. Recent research has demonstrated that decentralized controllers for complex robotic systems can achieve similar or even superior performance and robustness compared to centralized controllers [8], [9], [10]. Nonetheless, these studies are typically confined to specific simulated tasks and do not provide a general investigation of design choices."

### Cited references (resolved from the paper's bibliography)
- **[1]** Yu, Velu, Vinitsky, Gao, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative multi-agent games.* NeurIPS 2022.
- **[2]** Vinyals, Babuschkin, Czarnecki, et al. *Grandmaster level in StarCraft II using multi-agent reinforcement learning.* Nature 2019.
- **[3]** Terry, Black, Grammel, et al. *PettingZoo: Gym for multi-agent reinforcement learning.* NeurIPS 2021.
- **[5]** Peng, Rashid, Schroeder de Witt, Kamienny, Torr, Böhmer, Whiteson. *FACMAC: Factored multi-agent centralised policy gradients.* NeurIPS 2021.
- **[6]** Lavaei. *Decentralized implementation of centralized controllers for interconnected systems.* IEEE Transactions on Automatic Control, 2011.
- **[7]** Davison, Aghdam, Miller. *Decentralized control of large-scale systems.* Springer 2020.
- **[8]** Schilling, Konen, Ohl, Korthals. *Decentralized deep reinforcement learning for a distributed and adaptive locomotion controller of a hexapod robot.* IROS 2020.
- **[9]** Tao, Zhang, Bowman, Zhang. *A multi-agent approach for adaptive finger cooperation in learning-based in-hand manipulation.* ICRA 2023.
- **[10]** Guo, Jiang, Wang, Gao, Chen. *Decentralized motor skill learning for complex robotic systems.* IEEE Robotics and Automation Letters, 2023.
- **[11]** Gronauer, Diepold. *Multi-agent deep reinforcement learning: a survey.* Artificial Intelligence Review, 2022.
- **[12]** Perolat, De Vylder, Hennes, et al. *Mastering the game of Stratego with model-free multiagent reinforcement learning.* Science 2022.
- **[13]** Sunehag, Lever, Gruslys, et al. *Value-decomposition networks for cooperative multi-agent learning.* arXiv:1706.05296, 2017.
- **[14]** Rashid, Samvelyan, De Witt, Farquhar, Foerster, Whiteson. *Monotonic value function factorisation for deep multi-agent reinforcement learning (QMIX).* JMLR 2020.
- **[15]** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[16]** de Witt, Gupta, Makoviichuk, Makoviychuk, Torr, Sun, Whiteson. *Is independent learning all you need in the StarCraft multi-agent challenge?* arXiv:2011.09533, 2020.
- **[17]** Brockman, Cheung, Pettersson, Schneider, Schulman, Tang, Zaremba. *OpenAI Gym.* arXiv:1606.01540, 2016.
- **[18]** Liu, Zhang. *Partially observable multi-agent RL with (quasi-)efficiency: the blessing of information sharing.* ICML 2023.
- **[19]** He, Doshi, Banerjee. *Many agent reinforcement learning under partial observability.* arXiv:2106.09825, 2021.
- **[20]** Papoudakis, Christianos, Albrecht. *Agent modelling under partial observability for deep reinforcement learning.* NeurIPS 2021.
- **[21]** DeWeese, Qu. *Locally interdependent multi-agent MDP: theoretical framework for decentralized agents with dynamic dependencies.* arXiv:2406.06823, 2024.
- **[22]** Jana, Vachhani, Sinha. *A deep reinforcement learning approach for multi-agent mobile robot patrolling.* International Journal of Intelligent Robotics and Applications, 2022.
- **[23]** Leottau, Ruiz-del-Solar, Babuška. *Decentralized reinforcement learning of robot behaviors.* Artificial Intelligence, 2018.
- **[24]** Zhao, Queralta, Westerlund. *Sim-to-real transfer in deep reinforcement learning for robotics: a survey.* IEEE SSCI 2020.
- **[25]** Liu, Liu, Song, Pang, Yuan, Xu. *A collaborative control method of dual-arm robots based on deep reinforcement learning.* Applied Sciences, 2021.
- **[26]** Ding, Koh, Merckaert, Vanderborght, Nicotra, Heckman, Roncone, Chen. *Distributed reinforcement learning for cooperative multi-robot object manipulation.* arXiv:2003.09540, 2020.
- **[27]** Chitnis, Tulsiani, Gupta, Gupta. *Efficient bimanual manipulation using learned task schemas.* ICRA 2020.
- **[28]** Zhao, Kumar, Levine, Finn. *Learning fine-grained bimanual manipulation with low-cost hardware.* arXiv:2304.13705, 2023.
- **[29]** Shi, Sharma, Zhao, Finn. *Waypoint-based imitation learning for robotic manipulation.* arXiv:2307.14326, 2023.
- **[30]** Yokoyama, Clegg, Undersander, Ha, Batra, Rai. *Adaptive skill coordination for robotic mobile manipulation.* arXiv:2304.00410, 2023.
- **[31]** Wang, Zhang, Tian, Li, Wang, Lane, Petillot, Wang. *Learning mobile manipulation through deep reinforcement learning.* Sensors 2020.
