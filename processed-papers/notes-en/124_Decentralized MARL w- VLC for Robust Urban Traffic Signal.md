# 124. Decentralized Multi-Agent Reinforcement Learning with Visible Light Communication for Robust Urban Traffic Signal Control

## Metadata
- **Title**: Decentralized Multi-Agent Reinforcement Learning with Visible Light Communication for Robust Urban Traffic Signal Control
- **Authors**: Manuel Augusto Vieira, Gonçalo Galvão, Manuela Vieira, Mário Véstias, Paula Louro, Pedro Vieira
- **Affiliation**: DEETC-ISEL/IPL, Lisboa, Portugal; UNINOVA-CTS and LASI, Caparica; NOVA School of Science and Technology; INESC INOV; Instituto de Telecomunicações, Instituto Superior Técnico
- **Venue**: Sustainability 2025, 17, 10056 (MDPI)
- **Link/arXiv**: https://doi.org/10.3390/su172210056

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness under partial observability / incomplete and noisy data; partial communication failures and partial network visibility; resilience to congestion spillback. (Not adversarial/worst-case robustness in the robust-MDP sense.)
- **Method paradigm**: Decentralized MARL with shared replay/global Deep Q-Network (DQN); neighbor-influenced Q-value updates; rule-based adaptive phase-duration mechanism (SAPA); Visible Light Communication (VLC) as the communication layer
- **Keywords**: MARL, DQN, traffic signal control, Visible Light Communication (VLC), decentralized control, pedestrian safety

## TL;DR
The paper proposes a decentralized MARL framework for urban traffic signal control in which a DQN agent at each intersection is fed high-fidelity, low-latency Visible Light Communication (VLC) data and incorporates neighboring-intersection Q-values, augmented by a Strategic Anti-Blocking Phase Adjustment (SAPA) mechanism, to remain robust under partial network visibility while reducing waiting times, queue lengths, and improving pedestrian safety and energy efficiency.

## Problem & Motivation
Urban congestion increases travel times, energy consumption, emissions, and pedestrian safety risks, while conventional centralized and rule-based traffic-signal control scales poorly and adapts poorly to dynamic, heterogeneous, multi-modal traffic. Existing MARL-based traffic signal control approaches often (i) do not fully capture simultaneous interactions among all agents, (ii) neglect pedestrian flows, and (iii) assume generic wireless links (DSRC, C-V2X) without exploring optical communication; many frameworks also rely on incomplete or noisy data, which can compromise robustness in real-world deployments. The paper's stated gap is that current approaches "do not fully integrate MARL with real-time, high-fidelity communication to optimize both traffic efficiency and urban sustainability," motivating a native MARL–VLC integration.

## Robustness Setting
- **Threat model / uncertainty set**: Not a formal adversarial/worst-case model. Robustness is operational: maintaining performance under partial visibility of the traffic network, partial/intermittent/heterogeneous traffic conditions, and partial communication failures. VLC provides high-fidelity, low-latency, interference-immune state exchange so agents can act on neighbor state despite limited local observations; the SAPA module guards against link saturation/spillback. The paper notes its evaluation "assumes ideal communication conditions without fully considering uncertainties in sensors or environmental factors."
- **Setting**: cooperative (decentralized agents sharing limited information and trained via a shared/global DQN); decentralized execution with neighbor-influenced coordination; online learning in simulation (SUMO) plus preliminary real-world experiments.

## Method
- Deploy one DRL agent (Intersection Manager) per intersection; each performs local observation and selects signal phases. Experiences are stored in a centralized replay memory and used to train a unified/global DQN, feasible because intersections are homogeneous; five strategy-specific networks are trained.
- State is encoded as 4×2×10 position cells + 4×2×10 velocity cells + 4 waiting cells (164 input neurons); the network is a fully connected net with five hidden layers of 400 neurons (ReLU), and 9 output neurons (one Q-value per action/phase). A separate Q-target network is used.
- Neighbor coordination: the Q-target adds a weighted aggregate of neighbors' predicted Q-values, Q_target = r_t + γ·max Q_pred(s_{t+1}, a′) + β·(1/N)·Σ_n Q_pred(n_{t+1}, a′), with neighbor-influence factor β = 0.3 (calibrated). The reward r_t rewards reductions in accumulated waiting time of both vehicles and pedestrians (atwt), weighted by p_veh and p_ped.
- VLC layer: LED transmitters (tetra-chromatic WLEDs, OOK modulation) and PIN–PIN photodiode receivers form a mesh–cellular V-VLC architecture (streetlights as geo-transmitters, traffic signals as edge nodes), supporting V2I/I2V, V2V, P2I/I2P links and a queue–request–response mechanism for conflict resolution and pedestrian-crossing prioritization.
- SAPA (Strategic Anti-Blocking Phase Adjustment): dynamic phase duration based on VLC-derived queue length Q and downstream link occupancy ρ. Green time is extended proportionally to Q when ρ is below a threshold (40% for a 400 m link, 35% when feeding a 200 m link), otherwise constrained to a minimum T_base = 8 s, preventing spillback. Five traffic-control strategies (balanced vs. circular/radial, inbound/outbound priorities) are implemented by biasing vehicle generation.

## Theoretical Contributions
None / mostly empirical. The paper provides reward and Q-target equations and a rule-based SAPA formulation but no convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: Microscopic SUMO simulation of a downtown Lisbon scenario; a "cell" of 5 homogeneous four-arm intersections (C0–C4 with central hub C1); ~1800 veh/h and 2000 pedestrians/h; episodes of 3600 s (training 200/300 episodes per text; 500 training epochs). Preliminary real-world VLC experiments are also reported.
- **Baselines**: Fixed-time (fixed-duration) control vs. SAPA-enabled adaptive MARL–VLC control; ablations across neighbor-influence factor β ∈ {0, 0.1, 0.2, 0.3, 0.4}; comparison across five traffic-control strategies (Balanced, Circular+Outbound/Inbound Radial, Radial+Outbound/Inbound). No external MARL-TSC baseline algorithm is quantitatively compared.
- **Evaluation metrics**: Cumulative (negative) reward, vehicle and pedestrian halting counts over time, average waiting time, queue length, average vehicle speed, throughput, and green-time/phase activation distribution.

## Key Results
- All five strategy-specific networks converged; prioritization strategies (e.g., Network 4, Radial+Outbound) achieved higher cumulative rewards than the balanced strategy (Network 1), which amplified congestion at the critical central intersection C1.
- Including neighbor influence (β = 0.3) versus β = 0 markedly reduced halted vehicles and pedestrian waiting times—most pronounced at C1—and left fewer vehicles/pedestrians in the environment, evidencing improved throughput and reduced delay.
- SAPA-enabled control substantially outperformed fixed-time control at C1: average queue ~20 vehicles (brief peaks to 40) versus the fixed network frequently exceeding 40 and accumulating over time; pedestrian-phase activation rose by over 20% in the SAPA network while keeping P1/P5 balanced.
- Pedestrian halting remained low and balanced across strategies; the framework maintained queues, mitigated congestion, and preserved throughput under partial/intermittent/heterogeneous conditions, with sustainability benefits (lower idling, fuel use, CO2).

## Limitations & Future Work
- Evaluation relies mainly on simulation, which may not capture all real-world complexities, and assumes ideal communication conditions without fully modeling sensor/environmental uncertainties.
- Highly non-standard intersections or networks with highly dynamic demand require scenario-specific tuning.
- VLC degrades under adverse weather (fog, rain, snow), strong ambient/direct sunlight (receiver saturation); it is positioned as a complement to, not replacement for, RF.
- Future work: real urban deployment, larger heterogeneous/multimodal networks, more complex layouts (e.g., roundabouts), advanced RL techniques, and further VLC/ITS integration toward fully autonomous self-optimizing systems.

## Relevance to Survey
This is an applied, communication-centric MARL work rather than a robust-MARL theory paper. Its notion of "robust" maps to the survey's themes of robustness under partial observability, communication robustness/failure tolerance, and resilience to incomplete or noisy data—achieved here through a high-fidelity VLC communication layer and a neighbor-aware, anti-blocking adaptive control rule. It is a useful data point for the "communication robustness / decentralized cooperative MARL under partial information" line and for application-domain (intelligent transportation) coverage, but it does not engage with robust MDP, adversarial RL, distributionally robust, or minimax formulations.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — 2.2 Reinforcement Learning Approaches: MARL-Based Traffic Signal Control (TSC)]_

"Reinforcement Learning (RL) has emerged as a promising paradigm for traffic signal control, enabling agents to learn optimal policies through interaction with the environment. Early studies focused on single-agent RL, demonstrating improvements in local intersection performance. However, centralized RL approaches typically struggle to scale to city-wide networks due to computational complexity and communication overhead.

MARL has therefore gained traction, allowing distributed agents to coordinate locally while addressing scalability challenges. MARL extends single-intersection reinforcement learning control to a stochastic game environment, where multiple agents (intersections) interact simultaneously across arterial or regional traffic networks [13]. Communication plays a critical role in decentralized MARL, as agents must learn to exchange information using messages to better understand the system and achieve effective coordination. Deep MARL has been used to enable inter-agent communication by learning communication protocols in a differentiable manner [14]. The objective is to achieve a global equilibrium strategy that optimizes overall traffic flow. However, because agents learn and adapt their strategies at the same time, each one faces the challenge of pursuing a moving target [15]. This means that the optimal local strategy of one intersection is constantly influenced by the evolving strategies of its neighbors. Recent works have reported reductions in delays and queue lengths, yet many frameworks ne incomplete or noisy data, which can compromise robustness in real-world deployments."

> _[Section 2, Related Work — 2.2, discussion following Table 1]_

"Several challenges remain in the application of MARL to traffic signal control. Independent MARL approaches are simple to implement but ignore coordination among intersections, which often limits their effectiveness at the network level. Partially cooperative MARL introduces some degree of local cooperation, yet it struggles to achieve system-wide equilibrium. Joint action MARL, on the other hand, enables strong coordination but faces severe scalability and computational challenges, making it less practical for large urban networks. Moreover, most MARL-based studies on traffic signal control focus predominantly on efficiency metrics, such as travel time and waiting time, while critical aspects such as safety and multi-objective fairness remain underexplored. To overcome these limitations, recent research has begun to explore hybrid or hierarchical MARL models. In these frameworks, a central agent is responsible for learning global policies, while local agents execute optimized actions based on multiple reward functions that account for both efficiency and safety. Such designs offer a promising balance, improving scalability, coordination, and robustness in complex urban environments."

> _[Introduction]_

"Decentralized Multi-Agent Reinforcement Learning (MARL) approaches have been explored to overcome these limitations. Partially cooperative MARL agents share limited information with neighboring intersections [3], incorporating local and adjacent states into partially shared Q-value functions, enabling improved adaptability, reduced congestion spillover, and multi-objective control for efficiency and fairness. This introduces a level of cooperation without requiring global coordination, feedback-based timing optimization [4] and RL for multi-objective decentralized control. It improves adaptability compared to independent MARL, reduces local congestion spillover effect and enables multi-objective control (e.g., efficiency and fairness) [5]. However, it does not fully account for simultaneous actions of all agents.

However, most existing approaches do not fully capture simultaneous interactions among all agents, and pedestrian flows are often neglected.

Although recent works have begun to explore Multi-Agent Reinforcement Learning (MARL) for decentralized traffic signal control [6] and comprehensive surveys on MARL-based traffic signal control exist [7], the communication layer in these studies is often assumed to rely on generic wireless links (e.g., DSRC, C-V2X) without detailed exploration of optical communication technologies. On the other hand, Visible Light Communication (VLC) has been used in Intelligent Transportation Systems (ITS) to support vehicle-to-infrastructure communication [8] and recent reviews discuss hybrid VLC/RF systems and their challenges [9], but these works do not address integration with MARL. Our work differentiates itself by proposing a native integration of VLC with MARL, where distributed agents utilize VLC for low-latency, high-reliability local information exchange, overcoming limitations related to latency, interference, and dependence on RF networks. Furthermore, unlike VLC relaying approaches for ITS [10], our method incorporates adaptive control mechanisms and prioritization between vehicular and pedestrian flows within a decentralized MARL context."

### Cited references (resolved from the paper's bibliography)
- **[3]** Richter, Aberdeen, Yu. *Natural actor-critic for road traffic optimisation.* NeurIPS (Twentieth Annual Conference on Neural Information Processing Systems) 2006.
- **[4]** Cunningham, Garg, Cahill. *A collaborative reinforcement learning approach to urban traffic control optimization.* IEEE/WIC/ACM Int. Conf. on Web Intelligence and Intelligent Agent Technology 2008.
- **[5]** Aziz, Feng, Ukkusuri. *Reinforcement learning-based signal control using R-Markov average reward technique (RMART) accounting for neighborhood congestion information sharing.* Transportation Research Board 92nd Annual Meeting 2013.
- **[6]** Chu, Wang, Codecà, Li. *Multi-agent deep reinforcement learning for large-scale traffic signal control.* arXiv 2019 (arXiv:1903.04527).
- **[7]** Shi, Wang, Zhang, Li. *A survey on traffic signal control problems with MARL.* ACM Computing Surveys 2023.
- **[8]** Vieira, Silva, Santos. *Visible light communication and learning-based control for urban intersections.* Symmetry 2024.
- **[9]** Sikder, Rahman, Bakibillah. *Advancements and challenges of visible light communication in intelligent transportation systems: A comprehensive review.* Photonics 2025.
- **[10]** Nawaz, Seminara, Caputo, Mucchi, Cataliotti, Catani. *IEEE 802.15.7-compliant ultra-low latency relaying VLC system for safety-critical ITS.* arXiv 2019 (arXiv:1906.08773).
- **[13]** Zhu, Dastani, Wang. *A survey of multi-agent deep reinforcement learning with communication.* Autonomous Agents and Multi-Agent Systems 2024.
- **[14]** Bokade, Jin, Amato. *Multi-agent reinforcement learning based on representational communication for large-scale traffic signal control.* IEEE Access 2023.
- **[15]** He, Wang, Yu, Lin, Li, Leung. *Efficient resource allocation for multi-beam satellite-terrestrial vehicular networks: A multi-agent actor critic method with attention mechanism.* IEEE Trans. Intelligent Transportation Systems 2022.
