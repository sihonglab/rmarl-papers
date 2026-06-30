# 90. Collaborative Communication for Edge LLM Servicing in Adversarial Networks: An MARL-Empowered Stackelberg Game Approach

## Metadata
- **Title**: Collaborative Communication for Edge LLM Servicing in Adversarial Networks: An MARL-Empowered Stackelberg Game Approach
- **Authors**: Liqi Hong, Shengli Pan, Fan Feng, Chengbo Jiao
- **Affiliation**: School of Cyberspace Security, Beijing University of Posts and Telecommunications, Beijing, China; Guangxi Key Laboratory of Digital Infrastructure, Guangxi Zhuang Autonomous Region Information Center, Nanning, China
- **Venue**: IEEE Internet of Things Journal 2025 (Vol. 12, No. 20, 15 October 2025)
- **Link/arXiv**: Digital Object Identifier 10.1109/JIOT.2025.3583280

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks — malicious relay nodes performing communication delay injection attacks in edge networks; adversarial nodes degrading channel quality
- **Method paradigm**: Stackelberg game (leader–follower), multiagent reinforcement learning (MARL), decentralized actor–critic / DDPG, game-theoretic equilibrium
- **Keywords**: Collaborative communication, edge large language model (LLM) servicing, multiagent reinforcement learning (MARL), Stackelberg Game

## TL;DR
The paper proposes a framework combining Stackelberg Game theory with MARL to mitigate communication delay injection attacks in edge LLM-servicing networks, modeling malicious relay nodes as leaders and edge devices as followers so that distributed edge agents can cooperatively identify and avoid malicious relays.

## Problem & Motivation
With the expansion of IoT and the 6G era, edge LLM servicing (collaborative resource sharing of computational power, Mixture-of-Expert modules, and intermediate inference results among edge devices) reduces cloud dependency but is hindered by edge heterogeneity and by vulnerable edge networks facing security threats from malicious relay nodes. Malicious relay nodes injecting delays pose a significant threat to network performance and security, disrupting latency-sensitive inference. Existing approaches focus mostly on resource allocation/task scheduling or on security in isolation; RL-based methods often treat edge devices as competing entities rather than collaborative agents in adversarial environments, rely on centralized control, and fail to model the complex strategic interactions between edge devices and malicious nodes in dynamic environments while providing decentralized decision-making without excessive communication overhead.

## Robustness Setting
- **Threat model / uncertainty set**: Delay injection attacks targeting relay nodes that reduce channel gain. The injected delay term D = 0.1 · σ²_noise is added to the relay channel gain model; when an attack occurs the interference channel gain switches from G_int to G_attack_int (with σ²_D reflecting the impact of delay injection, deteriorating channel gain as it increases). Attacks are assumed to randomly target relay nodes. The attacker (malicious relay alliance) acts as a strategic leader setting defensive/disruptive pricing.
- **Setting**: cooperative (edge devices implicitly collaborate) within an adversarial/competitive game (devices vs. malicious nodes); decentralized/distributed training (each edge device learns its strategy independently, no centralized coordination); online learning. Modeled as a Stackelberg leader–follower game solved via MARL.

## Method
- Models the interaction between edge devices and malicious relay nodes as a Stackelberg Game: the relay alliance acts as the leader (setting energy price/power), and the source/edge device acts as the follower (selecting relay nodes and determining energy purchase). Relay nodes lead due to attack risks, setting defensive pricing; the source node adapts energy purchases to minimize losses.
- Defines utility functions: relay utility U_r = β·C_r·P_r − Penalty_r, with an attack-induced penalty Penalty_r capturing resource-risk tradeoffs; source utility U_s = R_s − C_s − Penalty_s, with a coupling constraint P_r ≤ η·P_k (η ∈ (0,1]) ensuring a relay cannot forward more power than provisioned and discouraging arbitrary price inflation. The relay maximizes U_r and the source then adjusts to maximize U_s for an equilibrium; a sequential Stackelberg model can use backward induction.
- Formulates the multiagent decision process as an MDP (E, S, A, P, R, γ) with leader/follower state spaces (observations of CSI from the previous time slot, plus relay pricing/selection status for the follower), action spaces (relay power and pricing for the leader, relay selection/power for the follower), and reward functions r_leader,t = βU_r and r_follow,t = U_s.
- Uses a distributed MARL framework with decentralized actor–critic (DDPG-style) learning: the leader shares knowledge to speed up learning; critic loss minimizes weighted mean-square TD error, the actor is updated by maximizing the critic Q-value, and target networks are updated via soft updates (rate τ). A MoE service lets each edge agent preload different expert models and switch functions (e.g., fast response vs. high security) according to the environment.

## Theoretical Contributions
None / mostly empirical. The paper references existing methods for computing Stackelberg equilibria (directed acyclic graph algorithms, sequence-form approach, PPAD-completeness, backward induction) but provides no new convergence, sample-complexity, or equilibrium-existence proofs of its own.

## Experiments
- **Environment/Benchmark**: Simulated edge intelligent communication network with multiple source nodes, relay nodes, and destination nodes. Relay max power 2.2 W (cost limit 7.0/W), source power up to 1.0 W, source–destination distance 150 units, source-to-relay distances [85, 80, 75, 90, 85], relay-to-destination distances [90, 110, 95, 100, 95]. Hyperparameters: τ = 0.001, γ = 0.95, actor/critic learning rates 0.001/0.005, α = 0.15, β = 0.0935, λ = 0.235, γ = 0.3, attack strength a = 0.3, memory capacity 10000, batch size 128.
- **Baselines**: Random (random relay/energy-price selection ignoring attacks); DQN (value-based Deep Q-Learning with discretized continuous aspects); Adaptive Greedy (constrained-optimization scheme solving a per-step utility maximization and scoring relays by |H_sr|²/C_r).
- **Evaluation metrics**: Utility/reward values for edge and relay agents, convergence speed (training episodes), reward variance (stability), performance drop under increasing attack intensity and traffic load, resource utilization, latency reduction, system vulnerability reduction, stability improvement, energy consumption.

## Key Results
- Convergence: the scheme stabilizes at ~50 rounds for edge nodes (utility ~0.55) and ~85 rounds for relay nodes (utility ~0.35), converging faster and to higher utility than Random and DQN; it also achieves higher and more stable utility for both agent types than Adaptive Greedy.
- Robustness under delay injection: smaller performance drops than baselines as attack intensity rises 0.0→1.0 (48.1% drop at power_r=0.1 and 53.3% at power_r=1.0); lowest reward variance (0.0114 at power_r=0.1 vs Random 0.0192, DQN 0.0163, Adaptive Greedy 0.0182), and smallest variance even in high-power settings.
- Aggregate gains over baselines: 27.5% improvement in resource utilization, 21% lower delay, 35.6% lower system vulnerability, 27.3% higher stability, 18.6% lower energy consumption, and 35.7% higher overall throughput; under varying request loads the scheme shows the smallest degradation (e.g., 48.6% drop at power_r=0.1 vs Random 67.9%, DQN 55.6%, greedy 61.0%).

## Limitations & Future Work
- Evaluation is purely simulation-based; the framework is not yet scaled to large-scale deployments.
- No formal theoretical guarantees for the learned Stackelberg equilibrium under the adversarial setting.
- Future work: scaling the framework to large-scale deployments and exploring integration of federated learning (FL) to further enhance privacy and security.

## Relevance to Survey
This paper sits on the "communication robustness / adversarial networks" line of robust MARL, where the adversary acts on the communication channel (delay injection by malicious relay nodes) rather than on the environment model or agent observations directly. It connects the game-theoretic equilibrium method line (Stackelberg leader–follower games) with distributed MARL (decentralized actor–critic / DDPG) for cooperative robustness against adversarial nodes, and is an applied (edge LLM / 6G IoT) instance of using game structure plus MARL to achieve resilience under adversarial behaviors and incomplete information.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work]_

"The rapid development of edge LLM servicing has underscored the critical role of communication quality in adversarial edge networks. Recent surveys, such as [1], have identiﬁed key challenges in resource constraints, latency, and privacy when deploying LLMs at the edge. Research has focused on two main approaches: 1) optimizing bandwidth and 2) resource allocation under constraints, and enhancing security against threats like delay injection attacks. For bandwidth optimization, RL techniques have been widely adopted. Reference [7] integrated deep neural networks with traditional algorithms to address high-dimensional scheduling problems [8], while [9] applied deep Q-networks for resource allocation in federated and vehicular networks. However, these methods rely on centralized control and struggle in multi-controller scenarios with partial observability or conﬂicting objectives."

"To tackle distributed challenges, multiagent game theory and efﬁcient LLM deployment techniques have been introduced. References [10] and [11] employed cooperative learning to optimize throughput and relay selection. Meanwhile, sparse LLM architectures like MoE models have gained traction for edge deployment due to their parameter efﬁciency. For instance, [12] proposed an on-device inference engine that dynamically manages expert weights in MoE LLMs through storage hierarchy partitioning and adaptive preloading. Similarly, [13] introduced a framework for customizing on-device LLM serving via proxy submodel tuning, enabling resource-efﬁcient ﬁne-tuning of adapters."

"Recent studies have integrated federated learning (FL) and encryption to mitigate security risks while balancing efﬁciency. References [14] and [15] leveraged FL to protect raw data, while [16] applied differential privacy to enhance model conﬁdentiality. Others like [17] achieved to improve transmission security through risk-aware task allocation and lightweight protocols. However, these approaches either sacriﬁce efﬁciency for security or fail to address dynamic adversarial conditions, such as malicious relay nodes. For example, delay injection attacks can disrupt LLM inference timing, degrading service quality despite resource optimization efforts."

"Current approaches lack a holistic solution for edge LLM Servicing that balances bandwidth optimization, adversarial resilience, and computational efﬁciency. Most RL-based methods assume benign environments, while security-focused work neglects communication efﬁciency [18], [19]. Moreover, while sparse LLMs (e.g., [12] and [13]) reduce on-device costs, their interaction with adversarial networks remains unexplored. Moreover, unlike most of exiting approaches that operates in benign or partially cooperative environments, our MARL directly addresses the strategic complexity inherent in game-theoretic settings. By allowing distributed agents to iteratively learn and adapt their strategies based on observed outcomes and the explicit leader–follower structure of the Stackelberg game, our MARL framework is able to ﬁnd the equilibrium even under incomplete information and adversarial behaviors, and therefore, it can enable a more robust and adaptive solution to game-theoretic problems than exiting static or single-agent RL approaches."

### Cited references (resolved from the paper's bibliography)
- **[1]** G. Qu, Q. Chen, W. Wei, Z. Lin, X. Chen, K. Huang. *Mobile edge intelligence for large language models: A contemporary survey.* IEEE Commun. Surveys Tuts. (early access) 2025.
- **[7]** X. Wang et al. *Deep reinforcement learning: A survey.* IEEE Trans. Neural Netw. Learn. Syst. 2024.
- **[8]** Y. Wen et al. *VSP upgoing and downgoing wavefield separation: A hybrid model-data-driven approach.* IEEE Trans. Geosci. Remote Sens. 2025.
- **[9]** A. D. Mafuta, B. T. Maharaj, A. S. Alfa. *Decentralized resource allocation-based multiagent deep learning in vehicular network.* IEEE Syst. J. 2023.
- **[10]** A. Ortiz, T. Weber, A. Klein. *Multi-agent reinforcement learning for energy harvesting two-hop communications with a partially observable system state.* IEEE Trans. Green Commun. Netw. 2021.
- **[11]** A. Gao, Q. Wang, W. Liang, Z. Ding. *Game combined multi-agent reinforcement learning approach for UAV assisted offloading.* IEEE Trans. Veh. Technol. 2021.
- **[12]** R. Yi, L. Guo, S. Wei, A. Zhou, S. Wang, M. Xu. *EdgeMoE: Empowering sparse large language models on mobile devices.* IEEE Trans. Mobile Comput. 2025.
- **[13]** Y. Zhuang, Z. Zheng, F. Wu, G. Chen. *LiteMoE: Customizing on-device LLM serving via proxy submodel tuning.* Proc. 22nd ACM Conf. Embed. Netw. Sensor Syst. 2024.
- **[14]** H. Sharma, N. Kumar, R. Tekchandani. *Mitigating jamming attack in 5G heterogeneous networks: A federated deep reinforcement learning approach.* IEEE Trans. Veh. Technol. 2023.
- **[15]** H. Zhou, G. Yang, H. Dai, G. Liu. *PFLF: Privacy-preserving federated learning framework for edge computing.* IEEE Trans. Inf. Forensics Security 2022.
- **[16]** K. Wei et al. *Federated learning with differential privacy: Algorithms and performance analysis.* IEEE Trans. Inf. Forensics Security 2020.
- **[17]** X. Liu, M. Derakhshani, L. Mihaylova, S. Lambotharan. *Risk-aware contextual learning for edge-assisted crowdsourced live streaming.* IEEE J. Sel. Areas Commun. 2023.
- **[18]** H. Guo et al. *Achieving multi-attribute superiority and Sybil attack detection in IoV: A heuristic-based dynamic RSU deployment scheme.* IEEE Trans. Intell. Transp. Syst. 2025.
- **[19]** Y. Xun, H. Dong, X. Ma, B. Mao, H. Guo. *EVP-LCO: LiDAR-camera odometry enhancing vehicle positioning for autonomous vehicles.* IEEE Internet Things J. 2025.
