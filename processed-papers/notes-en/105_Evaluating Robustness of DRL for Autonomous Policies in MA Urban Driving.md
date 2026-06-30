# 105. Evaluating the Robustness of Deep Reinforcement Learning for Autonomous Policies in a Multi-Agent Urban Driving Environment

## Metadata
- **Title**: Evaluating the Robustness of Deep Reinforcement Learning for Autonomous Policies in a Multi-Agent Urban Driving Environment
- **Authors**: Aizaz Sharif, Dusica Marijan
- **Affiliation**: Simula Research Laboratory, Oslo, Norway
- **Venue**: 2022 IEEE 22nd International Conference on Software Quality, Reliability and Security (QRS) 2022
- **Link/arXiv**: Code: https://github.com/AizazSharif/Benchmarking-QRS-2022 (DOI: 10.1109/QRS57517.2022.00084)

## Taxonomy
- **Robustness / perturbation type targeted**: Non-stationarity from multi-agent interaction (other autonomous cars and pedestrians changing the environment); robustness/generalization of trained single-agent-style policies when deployed in single- vs. multi-agent urban driving scenarios. No explicit adversarial/uncertainty-set threat model.
- **Method paradigm**: Empirical benchmarking / comparative evaluation of model-free DRL algorithms; multi-objective reward design; no new robust-learning algorithm proposed.
- **Keywords**: deep reinforcement learning, multi-agent systems, autonomous cars, autonomous driving, testing autonomous driving, benchmarking, CARLA

## TL;DR
The paper provides an open, reusable end-to-end benchmarking framework (built on CARLA/RLlib/Macad-gym) plus a multi-objective reward function to systematically compare the robustness of six model-free DRL algorithms (PPO, A3C, IMPALA, DQN, DDPG, TD3) for autonomous-car policies trained in multi-agent urban driving and tested in both single- and multi-agent scenarios, finding A3C and TD3 most robust.

## Problem & Motivation
Deep RL is widely used to train autonomous-car (AC) policies in simulation, but there is (i) a lack of systematic comparison among DRL algorithms for vision-based urban driving, (ii) almost no study of which DRL models work best for AD in multi-agent (rather than single-agent) environments where non-stationarity arises from interacting cars, and (iii) a lack of a detailed multi-objective reward function used within independent multi-agent DRL agents to enable a fair robustness comparison. The paper addresses these three gaps with a benchmarking framework and a comparative study.

## Robustness Setting
- **Threat model / uncertainty set**: No explicit adversarial perturbation or uncertainty set. "Robustness" is operationalized as driving performance stability (low collision, low offroad-steering, adequate speed/distance) when policies trained in a multi-agent environment are evaluated across single-agent (Scenario 2) and competitive multi-agent (Scenario 1) settings and across five driving environments (Straight, Three-Way, Four-Way, Roundabout, Merge). Multi-agent non-stationarity (each agent's transition probability and reward depend on all agents' actions) is identified as the key threat.
- **Setting**: Mixed/competitive multi-agent (independent, non-communicating competitive driving agents plus auto-controlled cars); decentralized execution; modeled as POMDP / Partially Observable Stochastic Game (POSG) via Markov Games; online training, then offline-style testing over 50 episodes; vision-only input (84x84x3 front-camera images).

## Method
- Build an end-to-end DRL benchmarking framework on CARLA (Town03, v0.9.4), RLlib, Macad-gym (modified to add competitive multi-agent driving), and TensorFlow; each AC takes 84x84x3 camera images and outputs Steer/Throttle/Brake (9 discrete actions or 2 continuous Box values; reverse disabled).
- Benchmark six model-free DRL algorithms across discrete (PPO, A3C, IMPALA, DQN) and continuous (DDPG, TD3) action spaces, tuned with Population Based Training (PBT).
- Propose a multi-objective reward function RAC combining Safety (−50 penalty for collisions with vehicles/objects/pedestrians), Efficiency (+10 for distance-to-goal reduction and speed), Lane Keeping (−0.5 for offroad steering), and a penalty constant ϕ to encourage exploration.
- Train policies in a multi-agent environment (Scenario 1), then test in both competitive multi-agent (Scenario 1) and single-agent (Scenario 2) settings; evaluate via two research questions (RQ1: per-metric driving performance; RQ2: success rate on Safety/Efficiency/Lane Keeping).

## Theoretical Contributions
None / mostly empirical.

## Experiments
- **Environment/Benchmark**: CARLA Town03 urban driving, five environments — env_1 Straight, env_2 Three-Way intersection, env_3 Four-Way intersection, env_4 Roundabout, env_5 Merge (env_2 and env_3 include pedestrians). 50 testing episodes, 5000 simulation steps per episode.
- **Baselines**: The six DRL algorithms compared against each other — PPO, A3C, IMPALA, DQN (discrete); DDPG, TD3 (continuous). No external robust-MARL baseline.
- **Evaluation metrics**: Six Driving Performance Metrics — CV (collision with vehicles), CO (collision with road objects), CP (collision with pedestrians), OS (offroad steering %), TTFC (time to first collision), SPEED; plus DISTANCE; aggregated into Safety, Efficiency, and Lane Keeping success rates.

## Key Results
- A3C and TD3 are the most robust: A3C performs best overall (no vehicle collision in four of five environments, minimal road collisions and offroad-steering errors, consistent speed) and TD3 is the best continuous-action policy (avoids vehicle/pedestrian collisions, best lane keeping, though it trades off lower speed for safer driving).
- IMPALA is the weakest discrete-action algorithm and DDPG the weakest continuous-action algorithm (frequent collisions, high offroad-steering, early first collisions); DQN is second-best discrete and improves substantially in single-agent testing.
- Driving performance degrades notably when agents move from single-agent to competitive multi-agent settings, demonstrating the impact of multi-agent non-stationarity; different DRL algorithms exhibit different driving/testing performance across scenarios, motivating systematic comparison.

## Limitations & Future Work
- Threats to validity: multi-agent non-stationarity strongly affects driving behavior; choice of only six DRL algorithms (constrained by Ray RLlib / TensorFlow / CARLA compatibility); hyperparameter tuning sensitivity (mitigated via literature-reported settings plus PBT).
- Future directions: investigate higher-speed A3C policies; further tune IMPALA for complex urban scenarios; explore continuous-action extensions of DQN (e.g., DDPG); further analyze TD3 at higher speed while balancing safety and lane keeping; more hyperparameter-tuning experimentation.

## Relevance to Survey
This is an empirical robustness-evaluation/benchmarking paper rather than a robust-MARL algorithm paper. It connects to the survey's "evaluation / benchmarking of robustness" and "multi-agent non-stationarity" themes for autonomous-driving applications: it frames multi-agent driving as a POSG/Markov Game with partial observability and quantifies how single-agent-trained-style policies generalize (or fail) under multi-agent interaction. It is a useful application-domain and benchmarking reference, but contributes no robust-learning method, uncertainty set, or adversarial training; the related-work discussion is on AD benchmarks rather than robust RL/MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work]_

"In AD research, there are only a few benchmarks for evaluating the performance of RL-based AD models. Vinitsky [15] proposes a benchmark for DRL in mixed-autonomy traffic. While the benchmark involves four scenarios: the figure eight network, the merge network, the grid, and the bottleneck, it evaluates a limited number of reinforcement learning (RL) algorithms (two gradient-based and two gradient-free). In addition, the proposed benchmark is specific to connected AD research. Stang [14] proposes another benchmark for RL algorithms in a simulated AD environment. As a limitation, this benchmark focuses on a simple lane-tracking task, and furthermore, evaluates only off-policy RL algorithms. In contrast, our work evaluates both on-policy and off-policy algorithms and further allows for comparing the performance of DRL algorithms in a complex urban environment. As another limitation, both [15] and [14] only support DRL benchmarking for single-agent AD environments."

"Li [18] introduces a driving simulation framework called MetaDrive and performs a benchmarking of RL algorithms for AD. While the authors use five different driving scenarios, they only evaluate two RL algorithms (PPO and SAC). The work could also benefit from using realistic visual rendering as provided by the CARLA framework in our work. Palanisamy [19] proposes a multi-agent urban driving framework in which one can train more than one AC. Using IMPALA, a connected AC policy is trained within the CARLA simulator. However, as a limitation, the work is restricted to connected AD problems only."

"Furthermore, there are frameworks proposed for training and testing autonomous vehicles. For example, F1TENTH framework [20] with three racing scenarios and baselines for testing and evaluating autonomous vehicles. However, the framework does not support dealing with ARL. Han [21] proposes an off-road simulated environment for AD with realistic off-road scenes, such as mountains, deserts, snowy fields, and highlands. While realistic environments are useful for evaluating the generalization abilities of AD models, the work is limited to single-agent AD environments."

> _[Section III-B, Multi-agent Autonomous Driving]_

"While introducing multi-agent AD agents, we need to consider an environment where agents do not have access to all the states at each time step. Such types of environments are found in the field of robotics and ACs where an agent is limited to the sensory information gathered by its hardware. Therefore, the existing MDP can be termed as a Partially Observable Markov decision process (POMDP) [40]. Furthermore, the current formulation of POMDP can be reformulated as Partially Observable Stochastic Games (POSG) [41] by defining a DRL control problem as a tuple (I, S, A, O, P, R). In POSG, we can incorporate multi-agent scenarios using Markov Games [42] where multiple agents are interacting with the environment. An actor i ϵ I receives its partial observations from a joint observation state oi ϵ Oi at each time step t. Following the traditional MDP approach, each actor uses its learned policy function πi : Oi 7→Ai to perform actions ai ϵ Ai. As a return, each actor gets a desired reward value ri ϵ Ri."

> _[Section VIII, Threats to Validity — Non stationary multi-agent driving environments]_

"In multi-agent non-stationary environments, each agent's transition probability and reward function depends on the actions of all the agents since they change every time with the actions performed by the agents. DRL research for AD is mainly focused on driving in a single-agent stationary MDP environment. Driving behavior is affected a lot when tested in a multi-agent scenario due to the non-stationary driving environment [50]. This is one of the key threats to the existing DRL-based AD research that is performed only in a single-agent scenario."

### Cited references (resolved from the paper's bibliography)
- **[14]** Stang, Grimm, Gaiser, Sax. *Evaluation of deep reinforcement learning algorithms for autonomous driving.* IEEE Intelligent Vehicles Symposium (IV) 2020.
- **[15]** Vinitsky, Kreidieh, Le Flem, Kheterpal, Jang, Wu, Liaw, Liang, Bayen. *Benchmarks for reinforcement learning in mixed-autonomy traffic.* CoRL 2018.
- **[18]** Li, Peng, Feng, Zhang, Xue, Zhou. *MetaDrive: Composing diverse driving scenarios for generalizable reinforcement learning.* arXiv 2021.
- **[19]** Palanisamy. *Multi-agent connected autonomous driving using deep reinforcement learning.* IJCNN 2020.
- **[20]** O'Kelly, Zheng, Karthik, Mangharam. *F1TENTH: An open-source evaluation environment for continuous control and reinforcement learning.* NeurIPS 2019 Competition and Demonstration Track (PMLR vol. 123) 2020.
- **[21]** Han, Park, Kim. *A new open-source off-road environment for benchmark generalization of autonomous driving.* IEEE Access 2021.
- **[40]** Oliehoek. *Decentralized POMDPs.* Springer Berlin Heidelberg 2012.
- **[41]** Emery-Montemerlo, Thrun, Gordon, Schneider. *Approximate solutions for partially observable stochastic games with common payoffs.* AAMAS (IEEE Computer Society) 2004.
- **[42]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* ICML 1994.
- **[50]** Papoudakis, Christianos, Rahman, Albrecht. *Dealing with non-stationarity in multi-agent deep reinforcement learning.* 2019.
