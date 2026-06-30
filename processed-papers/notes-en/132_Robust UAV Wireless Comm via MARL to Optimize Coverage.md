# 132. Robust UAV-Oriented Wireless Communications via Multi-Agent Deep Reinforcement Learning to Optimize User Coverage

## Metadata
- **Title**: Robust UAV-Oriented Wireless Communications via Multi-Agent Deep Reinforcement Learning to Optimize User Coverage
- **Authors**: Mahfizur Rahman Khan, Gowtham Raj Veeraswamy Premkumar, Bryan Van Scoy
- **Affiliation**: Department of Electrical and Computer Engineering, Miami University, Oxford, OH, USA
- **Venue**: Drones (MDPI) 2025, Vol. 9, No. 5, Article 321
- **Link/arXiv**: https://doi.org/10.3390/drones9050321 (code: https://github.com/vanscoy/data-uav-rl/)

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/distribution uncertainty (stochastic user distributions, train/test distribution shift) and communication attacks (jamming attacks that disable a UAV and cut its inter-UAV links / agent failure recovery)
- **Method paradigm**: Multi-agent deep Q-learning (MADQL/DQN); centralized vs. decentralized (shared-network) training; stochastic-environment training for generalization; heuristic relocation algorithm for jamming recovery
- **Keywords**: UAV base stations, multi-agent deep Q-learning, user coverage, stochastic user distribution, jamming robustness

## TL;DR
The paper uses centralized and decentralized multi-agent deep Q-learning to place UAV base stations for maximum ground-user coverage, and improves robustness by training under stochastic user distributions and by adding a heuristic relocation scheme that lets unaffected UAVs reposition to recover coverage when one UAV is jammed.

## Problem & Motivation
UAVs deployed as dynamic aerial base stations can deliver wireless coverage in areas lacking fixed infrastructure (disasters, temporary events, rural regions). Placing UAVs in 3D adds a degree of freedom that makes deployment harder than for fixed terrestrial base stations, and the underlying optimization is non-convex / NP-hard. The authors identify three gaps: (1) prior work studies either centralized or decentralized approaches but rarely compares both; (2) most RL studies train and test on the same user distribution rather than deliberately using a stochastic environment to ensure generalization; (3) jamming attacks during dynamic-base-station operation have received limited attention. The paper addresses all three.

## Robustness Setting
- **Threat model / uncertainty set**: (a) Distribution uncertainty — user positions and counts are sampled stochastically per episode (Type II: random positions, fixed hotspot coordinates/counts; Type III: random positions and counts, fixed hotspots), and policies trained on one distribution are tested on others to measure transfer. (b) Jamming attack — after a UAV reaches its optimal location (jamming triggered after ~30 steps), a malicious entity jams one UAV; the jammed UAV's individual coverage drops to zero and it loses all inter-UAV communication, hovering indefinitely (an induced agent failure). Recovery must come from the remaining UAVs.
- **Setting**: Cooperative (agents share reward information to maximize global coverage); both centralized (single controller over joint state/action) and decentralized (each UAV autonomous, sharing a common neural network) are studied; online deep Q-learning with experience replay.

## Method
- Formulate UAV placement as a grid-discretized MARL problem: state = UAV 2D coordinates plus individual/overall coverage rates; action space = {left, right, forward, backward, stand-still}; reward = number of covered users with bonus/penalty terms for crossing the threshold coverage rate and a penalty for leaving the grid (agents share an average reward).
- User association uses a two-sweep algorithm (Algorithm 1): each user requests its closest UAV, UAVs admit users within coverage radius r = H·tan(θ/2) in order of distance up to capacity; a second sweep covers any unassigned users.
- Train with Deep Q-Learning (target network, replay buffer, epsilon-greedy, MSE loss, Adam): a decentralized variant where all UAVs share one network (two 400-neuron hidden layers, ReLU), and a centralized variant where one network outputs Q-values over the joint action space (size kᴺ, e.g. 5⁵ = 3125). The centralized model can be warm-started by averaging the hidden-layer weights of the trained decentralized models.
- Robustness mechanisms: (1) inject stochastic user distributions across episodes during training so the policy generalizes to varied user situations; (2) a heuristic jamming-recovery scheme (Algorithm 3): when a UAV is jammed, the remaining UAV with the lowest coverage rate (if below the jammed UAV's prior coverage) moves step-by-step via vector calculation toward the jammed UAV's location to restore coverage.

## Theoretical Contributions
None / mostly empirical (the paper is an applied deep-RL system study; no convergence, sample-complexity, or certified-robustness theorems).

## Experiments
- **Environment/Benchmark**: Custom simulator (Python 3.11, Gym, PyTorch) of a 1000×1000 m target area discretized into a 10×10 grid, N = 5 UAVs at height H = 350 m, aperture 60°, M = 100 users (90 in four hotspots, rest uniform), UAV capacities [10,15,20,25,30]; smaller-scale variant with 3 UAVs / 60 users.
- **Baselines**: No external learned baselines; the paper compares its own centralized vs. decentralized MADQL, the three user-distribution regimes (Type I/II/III), grid-resolution variants (100 m vs. 50 m steps), and pre/post-jamming coverage. Table 1 qualitatively contrasts optimization, single-agent DQL, and distributed Q-learning (MARL).
- **Evaluation metrics**: Number of connected (covered) users per episode, mean connectivity across test distributions, convergence curves, coverage recovery after jamming, and simulation runtime.

## Key Results
- Baseline decentralized MADQL covers up to 93 users (100 m grid); refining the grid to 50 m steps near the optimum raises coverage to 95 users but increases runtime from ~200 to ~300 min.
- Cross-distribution testing: policies covered about 80% of users regardless of which distribution they were trained or tested on (e.g., Type-I-trained policy reaches ~86 users on Type I, ~82 on Type II, ~76 on Type III), demonstrating robustness/transferability to distribution shift.
- Jamming recovery: when a UAV is jammed, coverage drops sharply (e.g., 86 → 45 users) but the relocation heuristic restores it to a new, somewhat lower equilibrium (e.g., ~68 users); recovery is shown across each of the five UAVs being jammed independently.
- Centralized vs. decentralized trade-off: centralized DQL achieves smoother learning and better coverage on small problems (54/60 vs. 48/60 users with 3 UAVs) but scales poorly (joint action space grows as kᴺ); weight-initialization from decentralized models cut centralized runtime (e.g., 157 → 63 min).

## Limitations & Future Work
- Centralized approach scales poorly due to exponential joint state/action growth; decentralized approach faces inter-agent coordination challenges as network size grows.
- Robustness to jamming is handled by a hand-crafted heuristic (not learned), and only single-UAV-at-a-time jamming is modeled with jamming triggered at a fixed step.
- Limited UAV flight time / battery, memory, and computational constraints are not modeled; energy management and trajectory optimization are left to future work; real-world (sim-to-real) deployment challenges remain open.

## Relevance to Survey
This is an applied MARL systems paper whose "robustness" is empirical rather than formally adversarial: robustness to environment/distribution shift via stochastic-environment training, and robustness to a communication/jamming attack that induces an agent failure, mitigated by a relocation heuristic. It connects the survey's themes of communication-attack robustness, agent-failure/fault tolerance, and distributional generalization in cooperative MARL, while sitting outside the robust-MDP / minimax / distributionally-robust theory line. Useful as a domain (UAV networking) example of jamming/fault-tolerant cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 2.4, Jamming]_

"Due to the broadcasting nature of wireless communications, UAV-assisted wireless communication networks are particularly vulnerable to spectrum jamming assaults, which pose a serious threat to network operation. Malicious users exploit this vulnerability by launching three forms of jammer attacks: constant, intermittent, and reactive. Constant jamming occurs when jamming signals are continuously sent, intermittent jamming involves sending signals periodically, and reactive jamming occurs when jamming signals target the region of the spectrum inhabited by legitimate users while monitoring their transmission [38]. In this study [39], a hidden Markov model (HMM)-based jamming detection technique is suggested, with the goal of detecting reactive short-period jamming for UAV-assisted wireless communications without requiring prior knowledge of the signal or channel characteristics."

> _[Section 3.3, Multi-Agent Reinforcement Learning]_

"In recent years, a wide range of strategies have been put out to take advantage of the benefits and overcome the obstacles presented by the fast-growing field of MARL. For example, agents can communicate with one another to exchange information [57], competent agents can act as teachers for learners [58], or learners can observe and mimic skilled agents [59]. In a multi-agent system, the surviving agents can assume some of the responsibilities of the failing agent or agents. This suggests that MARL is resilient by nature. Additionally, most multi-agent systems are highly scalable due to their design, which makes it simple to add new agents to the system. Stability, scalability, and communication are a few issues that MARL must deal with, which are contingent upon the structure of the learning process."

> _[Section 3.3.2, Decentralized]_

"Another method in MARL is decentralized learning, in which each agent independently learns and modifies its own policy or value function depending on its local observations and actions. The benefits of this strategy include scalability, privacy, and robustness, as it can manage dynamic and heterogeneous agents without relying on a global state or central authority. Nevertheless, because decentralized learning necessitates greater agent cooperation and communication and may face non-stationarity and partial observability, it also has several drawbacks, including complexity, inconsistency, and inefficiency [61]."

> _[Section 6, Robustness Against Jamming Attacks]_

"Unmanned aerial vehicles (UAVs) have shown great promise in addressing a variety of communication network difficulties [62]. Jamming attacks remain one of the main problems in wireless networks, despite the significant technological advancements in this field. The widespread occurrence of wireless networks based on UAVs has made jamming assaults a significant obstacle to the effective implementation of these technologies [63]. The term “jamming attack” describes the illegal creation of interference to an ongoing communication in order to cause disruptions or deceive users of wireless networks. In order to interfere with the wireless networks’ regular operation, the jammer sends out jamming signals. Wireless networks are therefore still susceptible to a variety of jamming attack methods. Because of the UAV’s great degree of adaptability, it is possible to mitigate the jamming attack or perhaps completely prevent its detrimental effects. Nonetheless, the jammer may target the UAV itself in an attempt to impede the regular operation of UAV-based communication networks [64]."

"The authors of [65] presented a UAV-aided anti-jamming system for cellular networks. Reinforcement learning algorithms are used by the UAV to select relay policies for users in cellular networks. To counteract the jamming attack, the UAV routes traffic from the jammed base station to a backup base station. In [66], the authors examined an anti-jamming communication within a UAV swarm when jamming was present. The UAV maximizes its data reception by taking use of the degree of freedom in frequency, velocity, antenna, and regional domain while a jammer targets the network. In [67,68] suggested a combined optimization for the UAV trajectory and transmission power in anti-jamming communication networks. The optimization problems are solved using a Q-learning-based anti-jamming approach and a stackelberg framework."

### Cited references (resolved from the paper's bibliography)
- **[38]** Pelechrinis, Iliofotou, Krishnamurthy. *Denial of service attacks in wireless networks: The case of jammers.* IEEE Commun. Surv. Tutorials 2010.
- **[39]** Zhang, Zhang, Mao, Xiao, Han, Xia. *Detection of Stealthy Jamming for UAV-Assisted Wireless Communications: An HMM-Based Method.* IEEE Trans. Cogn. Commun. Netw. 2023.
- **[57]** Tan. *Multi-agent reinforcement learning: Independent vs. cooperative agents.* ICML 1993.
- **[58]** Clouse. *Learning from an automated training agent.* In Adaptation and Learning in Multiagent Systems, Springer 1996.
- **[59]** Price, Boutilier. *Accelerating reinforcement learning through implicit imitation.* J. Artif. Intell. Res. 2003.
- **[61]** Zhang, Yang, Liu, Zhang, Basar. *Fully decentralized multi-agent reinforcement learning with networked agents.* ICML (PMLR) 2018.
- **[62]** Khan. *Distributed UAV-Based Wireless Communications Using Multi-Agent Deep Reinforcement Learning.* Master's Thesis, Miami University 2024.
- **[63]** Almasoud. *Jamming-aware optimization for UAV trajectory design and internet of things devices clustering.* Complex Intell. Syst. 2023.
- **[64]** Pirayesh, Zeng. *Jamming attacks and anti-jamming strategies in wireless networks: A comprehensive survey.* IEEE Commun. Surv. Tutorials 2022.
- **[65]** Lu, Xiao, Dai, Dai. *UAV-aided cellular communications with deep reinforcement learning against jamming.* IEEE Wirel. Commun. 2020.
- **[66]** Peng, Zhang, Wu, Zhang. *Anti-jamming communications in UAV swarms: A reinforcement learning approach.* IEEE Access 2019.
- **[67]** Xu, Ren, Chen, Zhang, Jia, Feng, Xu. *Joint power and trajectory optimization in UAV anti-jamming communication networks.* IEEE ICC 2019.
- **[68]** Lv, Xiao, Hu, Wang, Hu, Sun. *Anti-jamming power control game in unmanned aerial vehicle networks.* IEEE GLOBECOM 2017.
