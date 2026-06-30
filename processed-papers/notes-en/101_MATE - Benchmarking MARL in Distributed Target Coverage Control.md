# 101. MATE: Benchmarking Multi-Agent Reinforcement Learning in Distributed Target Coverage Control

## Metadata
- **Title**: MATE: Benchmarking Multi-Agent Reinforcement Learning in Distributed Target Coverage Control
- **Authors**: Xuehai Pan, Mickel Liu, Fangwei Zhong, Yaodong Yang, Song-Chun Zhu, Yizhou Wang
- **Affiliation**: School of Computer Science, Peking University; Center on Frontiers of Computing Studies, Peking University; School of Intelligence Science and Technology, Peking University; Institute for Artificial Intelligence, Peking University; Beijing Institute for General Artificial Intelligence (BIGAI); Department of Automation, Tsinghua University
- **Venue**: NeurIPS 2022 (36th Conference on Neural Information Processing Systems)
- **Link/arXiv**: https://github.com/UnrealTracking/mate

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to adversarial / non-stationary opponents and policy generalization (over-fitting to fixed opponents in distributed target coverage); robustness probed via variable agent populations (scalability) and trainable adversarial target agents; reduction of policy exploitability. (Benchmark environment rather than a robustness-specific algorithm.)
- **Method paradigm**: Benchmark / environment design; asymmetric two-team stochastic (cooperative-competitive zero-sum) game; self-play and population-based training (PSRO-Nash, Fictitious Self-Play, asymmetric self-play); exploitability as a robustness measure; CTDE MARL baselines
- **Keywords**: Multi-Agent Tracking Environment (MATE), target coverage control, asymmetric cooperative-competitive game, self-play / PSRO, exploitability, robustness benchmark

## TL;DR
The paper introduces MATE, an open-source, Python/Gym-compatible multi-agent benchmark simulating distributed target coverage control as an asymmetric two-team zero-sum game between "cameras" and "targets," and benchmarks MARL algorithms across cooperation, communication, scalability, robustness, and asymmetric self-play, showing that population-based / self-play co-evolution reduces policy exploitability and improves robustness.

## Problem & Motivation
The target coverage problem (actively controlling a group of directional sensors to track targets, as in wireless sensor networks, surveillance camera networks, and UAV networks) has wide real-world significance but remains an open challenge in distributed networks due to real-time-varying numbers of cameras and targets, diverse/unpredictable target trajectories, partial observability, and limited communication bandwidth. Popular MARL algorithms (MADDPG, QMIX, MAPPO, HAPPO) perform poorly on the target coverage problem despite their success on other benchmarks, and existing benchmarks (mostly video games or simplified scenarios) neglect features that real-world multi-agent applications demand: heterogeneous agents, asymmetric games, variable agent populations, partial observation, and peer-to-peer communication. There is no open-source, standardized environment benchmarking MARL under such practical settings in the target coverage context, which motivates building MATE.

## Robustness Setting
- **Threat model / uncertainty set**: Targets are controlled by adversaries (trainable adversarial target agents) that relentlessly challenge the camera policy with new strategies to improve the robustness and generalizability of the trackers. Robustness is also stressed by varying the number of agents on both sides (scalability) and by switching observability modes (full vs. partial). Robustness is quantified via exploitability — the average performance difference between best-response and current policies; low exploitability indicates proximity to a Nash equilibrium.
- **Setting**: Asymmetric two-team stochastic game supporting fully-cooperative, fully-competitive (zero-sum, r(C) = −r(T)), and general mixed-motive configurations; heterogeneous agents (inter-team and intra-team); partially observable by default; CTDE and decentralized MARL baselines; online training; intra-team broadcast and peer-to-peer communication.

## Method
- Designs MATE, a 2D mini-world with four entity kinds — proactive directional "camera" sensors (in-place, zoomable, pie-shaped field of view with rotation and zoom continuous actions), mobile "targets" (omnidirectional sensing, move freely via displacement vectors, two vehicle types differing in speed/carrying capacity), static obstacles (with a transmittance attribute for partial detection through them), and warehouses storing cargo.
- Reward structure mirrors the "min-max" nature of a cooperative-competitive game: cameras maximize Mean Coverage Rate (fraction of detected targets, averaged over the episode) while minimizing repeated detection; targets get a transport reward r(T) = F + B ("freight" F, a fixed sparse delivery reward, plus "bounty" B that depreciates over time and further drops when detected). Switchable between three game types; fully-competitive sets r(C) = −r(T) for a zero-sum game; wrappers allow custom mixed-motive rewards.
- Supports intra-team multi-round broadcast and peer-to-peer communication channels, with messages explicitly isolated from observations; wrappers can simulate signal noise, distance-based delays, restricted ranges, and limited bandwidth.
- Provides configurable population, observability, action space, and scene layouts; pure-Python numerical simulation integrated with OpenAI Gym API (compatible with RLlib, Tianshou, Stable-Baselines-3) and amenable to large-scale parallelism (Ape-X, IMPALA).
- For robustness, trains cameras and targets in co-evolution under a zero-sum payoff structure using population-based methods (PSRO-Nash, Fictitious Self-Play, asymmetric self-play) to reduce exploitability versus training against fixed-policy opponents.

## Theoretical Contributions
None / mostly empirical (benchmark/environment paper; the NeurIPS checklist marks theoretical results as N/A). It does formally define a Mean Coverage Rate metric (Eq. 1) and an exploitability measure (Eq. 2) for the environment.

## Experiments
- **Environment/Benchmark**: MATE itself, evaluated on multiple configurations (e.g., 4C vs. 8T (9O), 2C vs. 4T (0O), 4C vs. 8T (0O)), where C = camera, T = target, O = obstacle; cooperative training of one team against rule-based (random/greedy) opponents, communication-augmented cooperation, and zero-sum fully-competitive co-evolution.
- **Baselines**: MARL algorithms MAPPO, IPPO, MADDPG, QMIX (implemented/extended via RLlib); communication add-ons TarMAC and I2C; self-play / population-based methods PSRO-Nash, Fictitious Self-Play (FSP), and (asymmetric) self-play; rule-based (random and greedy) controllers. A hierarchical RL (HRL) model with a rule-based low-level executor is also used for camera agents.
- **Evaluation metrics**: Mean Coverage Rate, normalized episode reward, and exploitability (and meta-strategy distributions over PSRO iterations); curves averaged over three random seeds (shaded one-standard-deviation intervals); 10 million environment steps per cooperative experiment.

## Key Results
- In the cooperative camera task (4C vs. 8T (9O)), HRL methods show superior performance and PPO-based methods converge steadily; adding communication to MAPPO with the hierarchical structure barely improves convergence (attributed to the strong inductive bias of the HRL low-level rule-based executors).
- For target agents, communication brings more conclusive gains than for cameras; MAPPO+I2C attains the best convergence, and IPPO+TarMAC can match MAPPO+TarMAC. Observability matters: in 2C vs. 4T (0O), partial observability causes roughly a 0.35 drop in normalized episode reward for IPPO (little effect on MAPPO); in 4C vs. 8T (0O), IPPO fails in both observability modes while MAPPO drops about 0.1 under partial observability.
- In the zero-sum fully-competitive game, PSRO-Nash and self-play converge to policy populations that are less exploitable than those trained against non-evolving fixed-policy opponents, improving robustness; FSP decreases exploitability slowly because it uniformly samples (including the random policy) from the policy memory. Different roles (e.g., "distractors" and "running backs") emerge when training target agents with communication.

## Limitations & Future Work
- The first-stage focus of MATE is an all-in-one benchmark for MARL algorithms and a platform for distributed target coverage with trainable adversaries; it places lesser focus on visual perception (e.g., evaluation in three-dimensional space).
- Future work: extend MATE into a high-quality 3D game engine, e.g., realistic environments on Unreal Engine 4 (UE4) with UnrealCV.
- Ethical/societal concern noted regarding potential misuse of multi-agent tracking technologies in repressive surveillance; the authors advocate responsible use.

## Relevance to Survey
MATE provides a standardized, practical testbed for studying robustness in MARL through asymmetric cooperative-competitive games, trainable adversarial agents, variable agent populations, and exploitability-based robustness evaluation. It connects the robust MARL theme to the self-play / population-based training (PSRO, FSP) and game-theoretic equilibrium lines, and to robustness-via-adversarial-opponents and generalization-against-non-stationary-opponents themes. As a benchmark rather than a robustness algorithm, it is most relevant to the survey's discussion of evaluation environments, adversarial co-evolution for less exploitable (more robust) policies, and communication robustness (configurable noise/delay/bandwidth wrappers).

## Related Work (verbatim excerpts from the paper)

> _[Section 2, Related Work — "Target Coverage Problem"]_

"The target coverage problem is to find an optimal control strategy for sensors such that the time to monitor every interested target can be as long as possible [47]. It is a long-standing problem in directional sensor networks [48, 49], robotics [50, 51, 52, 53], and computer vision [3, 54]. Most previous algorithms are heuristically designed for a specific setting or application, lacking a general solution for this problem. Recently, Xu et al. [28] built a 2D environment, formulated the problem as a multi-agent cooperative game, and introduced a hierarchical multi-agent reinforcement learning approach to solve this game. However, compared with the real-world scenarios, the environment is over-simplified due to random-walking targets and a lack of obstacles. In MATE, we aim to build a more realistic simulator for benchmarking the off-the-shelf learning algorithms, e.g., account for occlusion caused by obstacles, the limited observing area of sensors, and controllable Field-of-View (FoV) of the Pan-Tilt-Zoom (PTZ) cameras. Besides, we reformulate the problem as a cooperative-competitive game and provide an interface to control the targets, i.e., the targets are controlled by adversaries to relentlessly challenge the camera policy with new strategies for the purpose of improving the robustness and generalizability of the trackers."

> _[Section 2, Related Work — "Self-Play and Population-Based Training Regime"]_

"MATE experimented with three training principles to promote camera-target competition in zero-sum games. Solving zero-sum games can be highly non-trivial due to the non-transitivity (e.g., Rock-Paper-Scissor) in the policy space [65]. Conventional self-play makes the agent continuously play against the latest copy of itself. Since the agents in MATE are heterogeneous, we adopt the asymmetric version [66, 67, 68] of the self-play training method. However, self-play may fail to converge due to the lack of policy diversity [69, 70], thereby trapped by the non-transitivity. Fictitious Self-Play (FSP) [40] is a population-based method that maintains a policy memory storing past versions of the policy and uniformly samples a policy from memory as the response against the opponent. Policy Space Response Oracle [39] with Nash Equilibrium solver (PSRO-Nash) is also a population-based method that computes a meta-strategy distribution. Instead of a uniform distribution, the distribution computed by PSRO-Nash resembles that of a mixed-strategy Nash Equilibrium. Recently, many efforts have been spent on extending PSRO methods to diverse PSRO methods [71, 72], no-regret PSRO methods [70], and PSRO with meta-learning [73, 74]. In this paper, we conduct experiments to demonstrate the effectiveness of these training regimes for improving and evaluating the robustness of the tracking agents."

> _[Section 5.3, Zero-sum Fully-competitive Game]_

"In Section 5.1 and 5.2, we present the results of training camera or target agents against fixed-policy opponents. However as these models implicitly treat their opponents as integrated parts of the non-stationary environment, this would often result in over-fitting or failure to generalize against new opponents [39]. In realistic deployment, a stable and robust solution is often preferred over a better-performing but brittle solution. Therefore to improve the robustness of the camera policy, we proposed to train camera and target agents in co-evolution with a zero-sum payoff structure."

### Cited references (resolved from the paper's bibliography)
- **[3]** Li, Xu, Zhong, Kong, Qiao, Wang. *Pose-assisted multi-camera collaboration for active object tracking.* AAAI 2020.
- **[28]** Xu, Zhong, Wang. *Learning multi-agent coordination for enhancing target coverage in directional sensor networks.* NeurIPS 2020.
- **[39]** Lanctot, Zambaldi, Gruslys, Lazaridou, Tuyls, Pérolat, Silver, Graepel. *A unified game-theoretic approach to multiagent reinforcement learning.* NeurIPS 2017.
- **[40]** Heinrich, Lanctot, Silver. *Fictitious self-play in extensive-form games.* ICML 2015.
- **[47]** Mini, Udgata, Sabat. *Sensor deployment and scheduling for target coverage problem in wireless sensor networks.* IEEE Sensors Journal 2013.
- **[48]** Ma, Liu. *Some problems of directional sensor networks.* International Journal of Sensor Networks 2007.
- **[49]** Guvensan, Yavuz. *On coverage issues in directional sensor networks: A survey.* Ad Hoc Networks 2011.
- **[50]** Zorbas, Di Puglia Pugliese, Razafindralambo, Guerriero. *Optimal drone placement and cost-efficient target coverage.* Journal of Network and Computer Applications 2016.
- **[51]** Saeed, Abdelkader, Khan, Neishaboori, Harras, Mohamed. *Argus: realistic target coverage by drones.* ACM/IEEE IPSN 2017.
- **[52]** Khan, Heurtefeux, Mohamed, Harras, Hassan. *Mobile target coverage and tracking on drone-be-gone UAV cyber-physical testbed.* IEEE Systems Journal 2017.
- **[53]** Tuba, Capor-Hrosik, Alihodzic, Tuba. *Drone placement for optimal coverage by brain storm optimization algorithm.* International Conference on Hybrid Intelligent Systems (Springer) 2017.
- **[54]** Ristani, Solera, Zou, Cucchiara, Tomasi. *Performance measures and a data set for multi-target, multi-camera tracking.* ECCV (Springer) 2016.
- **[65]** Sanjaya, Wang, Yang. *Measuring the non-transitivity in chess.* Algorithms 2022.
- **[66]** Zhong, Sun, Luo, Yan, Wang. *AD-VAT: An asymmetric dueling mechanism for learning visual active tracking.* ICLR 2019.
- **[67]** Zhong, Sun, Luo, Yan, Wang. *AD-VAT+: An asymmetric dueling mechanism for learning and understanding visual active tracking.* IEEE TPAMI 2021.
- **[68]** Zhong, Sun, Luo, Yan, Wang. *Towards distraction-robust active visual tracking.* ICML 2021.
- **[69]** Yang, Luo, Wen, Slumbers, Graves, Bou Ammar, Wang, Taylor. *Diverse auto-curriculum is critical for successful real-world multiagent learning systems.* AAMAS 2021.
- **[70]** Dinh, McAleer, Tian, Perez-Nieves, Slumbers, Mguni, Wang, Bou Ammar, Yang. *Online double oracle.* TMLR 2022.
- **[71]** Perez-Nieves, Yang, Slumbers, Mguni, Wen, Wang. *Modelling behavioural diversity for learning in open-ended games.* ICML 2021.
- **[72]** Liu, Jia, Wen, Hu, Chen, Fan, Hu, Yang. *Towards unifying behavioral and response diversity for open-ended learning in zero-sum games.* NeurIPS 2021.
- **[73]** Feng, Slumbers, Wan, Liu, McAleer, Wen, Wang, Yang. *Neural auto-curricula in two-player zero-sum games.* NeurIPS 2021.
- **[74]** Liu, Feng, Zhang, Wang, Yang. *Settling the bias and variance of meta-gradient estimation for meta-reinforcement learning.* arXiv 2021.
