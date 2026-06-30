# 127. Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for MANETs

## Metadata
- **Title**: Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for MANETs
- **Authors**: Saeed Kaviani, Bo Ryu, Ejaz Ahmed, Kevin Larson, Anh Le, Alex Yahja, Jae H. Kim
- **Affiliation**: EpiSys Science, Inc.; Boeing Research and Technology
- **Venue**: Not specified (arXiv preprint arXiv:2101.03273v2 [cs.NI], 29 Mar 2021)
- **Link/arXiv**: arXiv:2101.03273v2

## Taxonomy
- **Robustness / perturbation type targeted**: Environment dynamics / distribution shift in network conditions (network size, mobility/dynamic level, traffic dynamics, topology change); robustness/scalability to scenarios outside the trained range (out-of-distribution generalization). Domain context is highly dynamic / tactical MANETs with link outages, jamming, and unpredictable mobility.
- **Method paradigm**: Multi-agent deep reinforcement learning (MADRL); hybrid of MADRL with classical Q-learning-based routing (CQ+/SRR); CTDE with parameter sharing; PPO policy optimization; Dec-POMDP formulation
- **Keywords**: MANET routing, MADRL, CQ+/Q-routing, robustness, scalability, parameter sharing, PPO, CTDE

## TL;DR
The paper proposes DeepCQ+, a hybrid routing approach that integrates multi-agent deep reinforcement learning (PPO with parameter sharing under CTDE) into the Q-learning-based CQ+/SRR routing protocol, achieving 10–15% lower normalized overhead at comparable goodput and—most importantly—maintaining its performance gains on network sizes, mobility levels, and traffic dynamics far outside the limited range it was trained on.

## Problem & Motivation
Routing in highly dynamic, heterogeneous MANETs (especially tactical networks with mobility, interference, and jamming) is extremely challenging: traditional link-state/distance-vector protocols become stale and unreliable, and Q-learning-based routing (Q-routing, CQ-routing, CQ+/SRR) either becomes inefficient in rapidly changing networks or relies on a single hand-crafted parameter (best-path confidence) that gives only a local perspective. Prior MADRL routing approaches train per-agent policies that scale poorly and whose generalization to network sizes outside the trained range is unclear, while suffering from non-stationarity. The paper targets a scalable and robust routing policy that can be trained on a limited range of parameters yet executed across a much wider range of configurations, avoiding the curse of dimensionality of training over all network sizes.

## Robustness Setting
- **Threat model / uncertainty set**: No explicit adversary. Uncertainty arises from highly dynamic network conditions—variable network sizes (5 ≤ N ≤ 50), variable mobility/dynamic levels (node velocities, Gauss-Markov / random waypoint mobility), variable data flows and topology change. The robustness goal is that a policy trained on a narrow range (e.g., single network size N = 12, single data flow, small dynamic-level range) maintains performance when tested far outside that range (larger/smaller networks, multiple flows, higher dynamics).
- **Setting**: Cooperative multi-agent; Dec-POMDP; CTDE (centralized training, decentralized execution) with homogeneous-agent parameter sharing; trained offline in simulation, executed online with real-time C/H path-parameter updates via ACK messages.

## Method
- **Hybrid design**: Preserve the CQ+/SRR routing protocol's reception/ACK procedure (C- and H-value tracking, loop/duplicate checking, queueing) and replace only the transmission-time broadcast-vs-unicast decision (the CQ+ routing policy) with a learned DNN policy (DeepCQ+ routing).
- **Dec-POMDP + CTDE with parameter sharing**: Each node is a homogeneous agent using one shared parameterized policy πθ; decentralized execution relies only on local action-observation history, while centralized training accesses other agents' hidden state, enabling scalability to any network size without re-training.
- **Scalable input features**: Pre-process state by selecting the best K neighbors (e.g., K = 4) ordered by ascending h_j(1 − c_j), giving a fixed-size input regardless of N; observations include current C/H levels, their temporal changes (Δc, Δh), and the previous action, fed to a fully connected network (FCNN).
- **Reward design**: Reward type 1 reproduces the CQ+ policy as the optimal zero-horizon policy (rewards proportional to next-hop confidence/uncertainty); reward type 2 adds explicit overhead minimization via a weighted combination of delivery reward, a no-ACK penalty indicator, and normalized number of ACKs received (N_ack/N) as a proxy for added transmissions, formalized as minimizing N_TX subject to maintaining goodput ρ ≥ ρ0.
- **Optimization**: Use PPO (clipped objective) to optimize the shared routing policy.

## Theoretical Contributions
None / mostly empirical. The paper provides a derivation showing the CQ+ routing policy is the optimal zero-horizon policy under reward type 1, and a reformulation of overhead minimization as a constrained optimization, but offers no convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: A custom Python CQ+ routing network simulator interfaced with Ray and RLlib; random dynamic MANETs with configurable nodes, data flows, dynamic levels, area size, data rates, link quality. Benchmark topology based on adaptive routing [13] and CQ+ routing [19] (e.g., 800 m × 300 m area, 150 m radio range, Gauss-Markov / random waypoint mobility, flows up to 20 packets/s, up to 160 Kbps). Training on a single network size (e.g., N = 12), single flow, narrow dynamic range; testing on N = 5–50, multiple flows (1–4), and higher dynamic/region scales.
- **Baselines**: Q-routing, CQ-routing [18], and CQ+ routing (SRR) [19] (the generic non-DRL CQ+ routing policy is the primary comparison).
- **Evaluation metrics**: End-to-end throughput / goodput (delivery) rate, normalized overhead (N_TX/N_D divided by network size), broadcast rate, average number of hops; tracked over training (>50M steps, >15000 episodes) and across network sizes.

## Key Results
- DeepCQ+ with reward type 2 achieves at least ~15% lower normalized overhead than non-DRL CQ+ routing while maintaining approximately the same goodput rate (overall efficiency gain stated as 10–15%).
- The policy trained on a single network size (N = 12) scales "perfectly" across tested network sizes (10–30, and tested up to 50), with lower overhead and lower broadcast rate than CQ+.
- Training over a wide range of network sizes (10–30 variable) yields little to no additional gain over training on a single size, indicating the MADRL approach is not overfit and the parameter-sharing design generalizes (robustness/scalability) to untrained scenarios.

## Limitations & Future Work
- Action space is limited to broadcast/unicast (mode) selection; next-hop selection for unicast is currently fixed by CQ+ and not learned. Future work plans to expand the action space to include next-hop selection for unicast mode.
- Assumes no interference between transmissions to focus on the routing layer; uses simplified FIFO scheduling.
- End-to-end delay is not optimized in either reward type (only shown for behavior). Future work: accommodate additional metrics (end-to-end delay minimization), extend ACK-based information sharing with more context, and support heterogeneous wireless networks (multiple radio interfaces), tuning policies to balance metrics for arbitrary MANET environments.

## Relevance to Survey
This paper represents the "robustness as out-of-distribution generalization / scalability" line within (cooperative) MARL applied to a real systems domain (MANET routing), rather than adversarial or distributionally robust formulations. Its robustness claim is empirical: a CTDE + parameter-sharing MADRL policy trained on a narrow parameter range that retains performance across untrained network sizes, mobility, and traffic. It connects to the broader robust-MARL theme of generalization/transfer under environment/dynamics shift and to the practical-deployment (sim-to-real-like, train-narrow/test-wide) motivation, while contrasting with model-uncertainty and adversarial-agent lines that use explicit worst-case or minimax modeling.

## Related Work (verbatim excerpts from the paper)
> _[Introduction — broadcast/adaptive routing background]_

"To improve packet delivery and rapid exploration in these highly dynamic networks, broadcasting (i.e. transmission of a packet to all neighbors) has become a popular technique [8]–[12]. Traditional network routing protocols (e.g. DSDV [9], OSPF [12], OLSR [11], and AODV [10]) are used when the network is in a stable state. When link outages and node mobility become too frequent, these algorithms require alternative strategies to sustain performance. Danilov et al. [13] discussed the poor performance of these link-state routing protocols in tactical environments and attempted to reduce loss during transitions by flooding."

> _[Introduction — adaptive MANET routing]_

"To meet the demands of highly dynamic MANET, many solutions have adapted routing protocols to variations in the network conditions, e.g. fish-eye state routing protocol (FSR) [14] use adaptive link-state update rates, and the adaptive distance vector (ADV) routing protocol [15] use a threshold-based adjustment of the routing update rates based on the network dynamics. While these protocols outperform traditional routing schemes with lower overhead and topology information sharing, they are not responsive enough in highly dynamic MANETs where the routing recalculations happens at slower paste than link changes."

> _[Introduction — Q-routing / CQ-routing / CQ+ (SRR) prior work]_

"The seminal work in [16] proposed Q-routing, which uses a reinforcement learning (RL) module (i.e. Q-Learning [17]) to route packets and minimize delivery time. Each node uses Q-values based on locally acquired statistics to determine the next hop. Each Q-value represents the quality of each next-hop (or route) as an estimation of the delay for each path. The Q data is shared only via ACK messages, and each node maintains a table of values for every neighbor and destination pair. After any transmission, a node may receive an ACK message containing values to update the Q table. The Q-routing protocol selects the next hop with the best Q-value. Q-routing is efficient in static and minimally dynamic networks. In dynamic networks, Q-values quickly become stale as links break."

> "Kumar et al. [18] improved Q-routing for dynamic networks with the addition of confidence values (i.e. C-values) in their CQ-routing protocol. C-values are incremented when Q-value is updated and decremented as it becomes stale; however, CQ-routing becomes inefficient in highly dynamic networks as it is based on only uni-casting to a single node. With only unicast transmissions, network exploration (Q-value updates) is too slow when the network changes rapidly. The rate at which information is shared is simply too slow to keep up with highly dynamic networks."

> "AR [13] and smart robust routing (SRR) algorithms [19] have attempted to supplement unicast transmission with broadcast to improve robustness in highly dynamic networks. Both of these algorithms revert to unicast transmission in order to reduce the overhead of the flooding. Johnston et al [19] use techniques from the CQ-routing protocol (i.e. C and Q-values) but extends it by adding broadcast procedure for high reliability, robustness, and rapid network exploration as needed in the tactical and highly dynamic MANETs. To simplify the convention when listed with the other protocols, we will refer to it as the CQ+ routing protocol. Although CQ+ routing uses a simple but efficient switching policy to choose between unicast and broadcast, its decisions depend on a single network parameter (best path confidence level). It has a limited perspective of the entire network and can settle on a locally optimal solution. CQ+ routing also does not account for the change rate of network parameters and congestion in forwarding paths. We build more perspective into traffic and queuing and leverage this information to further improve performance. Among the various routing algorithms for MANET networks, Q-routing, CQ-routing, and CQ+ routing approaches are considered as benchmarks for this work."

> _[Introduction — RL/MADRL for routing prior work and its scalability/robustness gaps]_

"Routing decisions, such as next-hop selection, are opportune targets of reinforcement learning (RL). The work in this area was initiated by Boyan's Q-routing protocol[16]. Following the Q-routing approach, many other techniques and algorithms from the RL community have been applied to packet routing and scheduling [20]–[27]. [20] uses MADRL to design independent deep routing policies for each agent based on an off-policy deep Q-learning RL algorithm. Deep Q-learning approaches are based on value estimation, an estimation of the expected reward of the actions at certain states. Consequently, deep Q-learning and value estimation policies scale poorly, as the expected reward is dependent on many network parameters and conditions that are not known prior to decisions. Moreover, in MADRL-based approaches in the literature like [20], training unique policies for each agent further limits scalability. It is unclear how policies trained for specific network sizes perform when the network is extended or shrunk. A similar deep Q-learning RL-based approach is used in [21], where it creates cluster abstractions in the network and accounts for inter-cluster routing performance. They also assume a feedback link is available from the source node to the cluster lead agents. Although it is claimed that their approach is expected to be scalable to larger networks and dynamics but it is not clear how this would scale and perform if only trained on smaller networks and limited network settings. Deep neural network (DNN)-based routing policies tend to struggle with high dynamics, as the complexity of multi-agent environment struggles with the rapid rate of change. Optimization of the policy for one agent is dependent on the policy and actions of other agents and therefore suffers from non-stationarity. This is particularly difficult in dynamic networks as many network parameters and topology are rapidly changing."

> "To the best of our knowledge, there have not been works on a scalable and robust routing policy design framework using MADRL in MANET. To provide robustness and reliability, we use a similar approach to CQ+ routing, where CQ-routing is combined with adaptive flooding."

### Cited references (resolved from the paper's bibliography)
- **[8]** S. Taneja, A. Kush. *A survey of routing protocols in mobile ad hoc networks.* International Journal of Innovation, Management and Technology, 2010.
- **[9]** C. E. Perkins, P. Bhagwat. *Highly dynamic destination-sequenced distance-vector routing (DSDV) for mobile computers.* ACM SIGCOMM Computer Communication Review, 1994.
- **[10]** C. E. Perkins, E. M. Royer. *Ad-hoc on-demand distance vector routing (AODV).* Proceedings WMCSA'99 (2nd IEEE Workshop on Mobile Computing Systems and Applications), 1999.
- **[11]** T. Clausen, P. Jacquet, et al. *Optimized link state routing protocol (OLSR).* 2003.
- **[12]** J. Moy et al. *OSPF version 2.* 1998.
- **[13]** C. Danilov, T. R. Henderson, T. Goff, O. Brewer, J. H. Kim, J. Macker, B. Adamson. *Adaptive routing for tactical communications.* MILCOM 2012 (IEEE Military Communications Conference), 2012.
- **[14]** G. Pei, M. Gerla, T.-W. Chen. *Fisheye state routing: A routing scheme for ad hoc wireless networks.* IEEE ICC 2000.
- **[15]** R. V. Boppana, S. P. Konduru. *An adaptive distance vector routing algorithm for mobile, ad hoc networks.* IEEE INFOCOM 2001.
- **[16]** J. A. Boyan, M. L. Littman. *Packet routing in dynamically changing networks: A reinforcement learning approach.* NeurIPS (Advances in Neural Information Processing Systems) 1994.
- **[17]** R. S. Sutton, A. G. Barto. *Reinforcement learning: An introduction.* MIT Press, 2018.
- **[18]** S. Kumar, R. Miikkulainen. *Confidence-based Q-routing: An online adaptive network routing algorithm.* Proceedings of Artificial Neural Networks in Engineering, 1998.
- **[19]** M. Johnston, C. Danilov, K. Larson. *A reinforcement learning approach to adaptive redundancy for routing in tactical networks.* MILCOM 2018 (IEEE Military Communications Conference), 2018.
- **[20]** X. You, X. Li, Y. Xu, H. Feng, J. Zhao, H. Yan. *Toward packet routing with fully distributed multiagent deep reinforcement learning.* IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2020.
- **[21]** R. E. Ali, B. Erman, E. Baştuğ, B. Cilli. *Hierarchical deep double Q-routing.* IEEE ICC 2020.
- **[22]** Z. Mammeri. *Reinforcement learning based routing in networks: Review and classification of approaches.* IEEE Access, 2019.
- **[23]** C. Yu, J. Lan, Z. Guo, Y. Hu. *DROM: Optimizing the routing in software-defined networks with deep reinforcement learning.* IEEE Access, 2018.
- **[24]** G. Stampa, M. Arias, D. Sánchez-Charles, V. Muntés-Mulero, A. Cabellos. *A deep-reinforcement learning approach for software-defined networking routing optimization.* arXiv:1709.07080, 2017.
- **[25]** H. Ye, G. Y. Li, B.-H. F. Juang. *Deep reinforcement learning based resource allocation for V2V communications.* IEEE Transactions on Vehicular Technology, 2019.
- **[26]** S.-C. Lin, I. F. Akyildiz, P. Wang, M. Luo. *QoS-aware adaptive routing in multi-layer hierarchical software defined networks: A reinforcement learning approach.* IEEE SCC 2016.
- **[27]** A. Valadarsky, M. Schapira, D. Shahaf, A. Tamar. *Learning to route.* HotNets-XVI, ACM 2017.
