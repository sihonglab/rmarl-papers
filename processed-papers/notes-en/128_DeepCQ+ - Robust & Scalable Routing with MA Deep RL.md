# 128. DeepCQ+: Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for Highly Dynamic Networks

## Metadata
- **Title**: DeepCQ+: Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for Highly Dynamic Networks
- **Authors**: Saeed Kaviani, Bo Ryu, Ejaz Ahmed, Kevin Larson, Anh Le, Alex Yahja, Jae H. Kim
- **Affiliation**: EpiSys Science, Inc.; Boeing Research and Technology
- **Venue**: MILCOM 2021 (2021 IEEE Military Communications Conference)
- **Link/arXiv**: DOI 10.1109/MILCOM52596.2021.9652948

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/distribution shift robustness and scalability — robustness to changes in network size, mobility/topology dynamics, and traffic load (deployment in scenarios outside the trained range); sim-to-deploy generalization for MANET routing. (Not an adversarial/attack threat model.)
- **Method paradigm**: Cooperative MADRL; Dec-POMDP; centralized training with decentralized execution (CTDE); parameter sharing; policy-gradient / PPO; inverse-RL-inspired reward design; learned control layer on top of a Q-learning-based routing protocol.
- **Keywords**: MANET routing, MADRL, robustness, scalability, CTDE, PPO

## TL;DR
DeepCQ+ replaces the hand-tuned thresholds and rules of a Q-learning-based robust routing protocol (CQ+/SRR) with shared-parameter cooperative MADRL agents that decide when to broadcast vs. unicast, achieving higher throughput with lower overhead and—crucially—maintaining its performance gains on network sizes, mobility, and traffic conditions it was never trained on.

## Problem & Motivation
Designing robust, efficient, scalable routing for highly dynamic tactical MANETs is hard because the network is unpredictable in mobility, topology, interference, and possible jamming, forcing frequent route re-computations and throughput loss. Traditional protocols (OSPF, OLSR) work well in stable networks but degrade in highly dynamic ones, and existing RL/MADRL routing approaches scale poorly: they often learn node-specific policies that require re-training whenever a new node joins the network. The paper argues that no prior study had simultaneously achieved both scalability and robust performance using MADRL in dynamic MANETs, and aims to fill that gap while preserving the structure of the established CQ+ routing protocol so that the learned policy generalizes outside the trained range without the curse of dimensionality or catastrophic forgetting.

## Robustness Setting
- **Threat model / uncertainty set**: No explicit adversary. "Robustness" means consistent performance under non-adversarial environment variation: variable network sizes (5 ≤ N ≤ 50), high-rate topology/mobility changes (Gauss-Markov and random-waypoint models, region-dependent speed variance), and multiple data flows—including deployment configurations far outside the training distribution (trained on a single network size N=12, single flow, narrow dynamic range; tested on larger sizes, higher dynamics, and 1–4 flows).
- **Setting**: cooperative (team of agents/nodes); modeled as a Dec-POMDP; centralized training with decentralized execution (CTDE) with parameter sharing across homogeneous agents; trained/evaluated in simulation (online RL via PPO).

## Method
- Keeps the CQ+ (SRR) routing protocol "structure": next-hop selection still uses the CQ+ rule j* = arg min_j h(i,j,d)(1 − c(i,j,d)) based on confidence (C) and hop (H) values exchanged via per-hop ACKs; only the broadcast-vs-unicast decision is replaced by a learned policy.
- Each node is an agent in a Dec-POMDP; observations are the best-K (e.g., K=4) neighbors' C and H values plus their change rates and the previous action/packet-source indicator: o_t(i) = [c_t(i), h_t(i), Δc_t(i), Δh_t(i), a_{t-1}(i), p_{t-1}(i)].
- A single shared FCNN policy π_θ (one policy for all nodes) outputs the probability of broadcast vs. unicast; trained with Proximal Policy Optimization (PPO) under CTDE, which enables scalability and avoids the exponentially growing joint action space.
- Reward design uses an inverse-RL-inspired step: first a reward mimicking CQ+'s broadcast probabilities (DNN-based CQ+), then a tuned overhead-aware reward r_t = w1·1_D − w2·1_Z − w3·(N_ack/N) that rewards successful delivery, penalizes missing ACKs, and penalizes the normalized ACK count (a proxy for packet copies / overhead).
- Overhead is defined as normalized transmissions per delivered packet (OH = (1/N)·N_TX/N_D), with two additional bit-level overhead definitions; the learned policy minimizes overhead while preserving goodput.

## Theoretical Contributions
None / mostly empirical. The work is an applied MADRL system; it provides protocol/algorithm design (Algorithm 1) and reward formulations but no convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: Custom OpenAI Gym environment in Python simulating the CQ+ protocol (C/H value tracking, duplicate checking, mobility), interfaced with Ray and RLlib. MANET mobility via Gauss-Markov and random-waypoint models with region-dependent speed variance. Training: single network size N=12, single data flow, episode length 3000, γ=0.99, ~50M steps (>15000 episodes), policy FCNN(16,8,8,4). Testing: network sizes 5–50 (results shown for 10–30), region/dynamic-level scaling up to 2×/5×, 1–4 data flows.
- **Baselines**: CQ+ routing / SRR (also known as R2DN), the Q-learning-based protocol with hand-written broadcast rules; related lineage CQ-routing and Q-routing. (Comparison table positions DeepCQ+ as adding MADRL on top of C/Q-values + broadcast.)
- **Evaluation metrics**: Goodput / delivery ratio (delivered packets ÷ total incoming packets, excluding duplicates), normalized overhead (types 1 and 2), broadcast rate, and end-to-end delay (hop counts).

## Key Results
- DeepCQ+ achieves goodput (delivery ratio) roughly equal to or slightly higher (1–5%) than CQ+ while requiring 10–25% less overhead, with a lower percentage of broadcast transmissions.
- The policy trained only on a 12-node network scales to networks as large as 30 (and reportedly well beyond 50) without retraining, maintaining gains under network sizes, mobility, and traffic dynamics it was not trained for—demonstrating the targeted scalability and robustness.
- No apparent degradation in end-to-end delay (hop counts); the MADRL framework can be tuned to trade off goodput, broadcast rate, and delay, a flexibility not available in CQ+.

## Limitations & Future Work
- Action space is limited to broadcast-vs-unicast selection; next-hop is still chosen by the fixed CQ+ rule. Authors are working to expand the action space to include next-hop selection for unicast mode.
- Evaluation is simulation-only (OpenAI Gym / Ray / RLlib); no real-world tactical deployment reported.
- Plan to incorporate recurrent neural network (RNN) policy units to better capture temporal/network dynamics and obtain higher gains, and to explore other MADRL techniques.

## Relevance to Survey
This paper represents the "applied/empirical robustness via generalization and scalability" line of MARL rather than adversarial or distributionally-robust formulations: robustness is operationalized as out-of-distribution generalization (train narrow, deploy broad) using cooperative MADRL with CTDE and parameter sharing. It is a useful contrast case for the survey—showing how robustness is framed in a real cooperative-networking application (MANET routing) and how protocol-structure preservation plus shared policies yields zero-shot scalability—complementing the theory-driven robust-MARL / robust-MDP works that model explicit uncertainty sets or adversaries.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"In this paper, we consider a class of distributed routing algorithms that only share limited information (i.e. two single ﬂoating value) through per-hop acknowledgment (ACK) packets. This method of cooperation is efﬁcient as ACKs are inherently present in the networking protocols (such as MAC-layer acknowledgement) and do not require any extra implementation in the system. The seminal work [5] proposed Q-routing, which used a reinforcement learning (RL) module (i.e. Q-Learning [6]) to route packets and minimize delivery time. Each node uses Q-values representing quality of paths which are acquired locally to determine the next hop and shared via ACK messages. Kumar et al. [7] improved Q-routing for dynamic networks with the addition of conﬁdence values (i.e. C-values) in their CQ routing protocol. To improve reliability and exploration speed of the CQ-routing, smart robust routing (SRR) algorithm [8] was proposed to add selective broadcasting actions. SRR utilizes heuristic rules on when to broadcast in order to improve robustness but keep the overall overhead under control. We refer to this technique as CQ+ routing (also known as Robust Routing for Dynamic Networks, or R2DN) as it is an extension of CQ routing for balancing between reliability and overhead. Although CQ+ routing uses a simple but efﬁcient switching policy to choose between unicast and broadcast, its decisions depend on a single network parameter: best-path conﬁdence level. Consequently, it has a limited perspective of the entire network that often leads to a locally optimal solution, since it does not fully account for the high rate changes in topology and degree of congestion in likely forwarding paths. Nevertheless, its performance has been consistent across many scenarios used in our study, and as a result, it serves as a baseline design for our MADRL framework."

> _[Introduction]_

"Routing decisions such as next-hop selection are opportune targets for employing RL-based techniques, originally introduced and initiated by Boyan's Q-routing protocol [5]. Following the Q-routing approach, a ﬂurry of new techniques and algorithms from the RL community have been developed and applied to packet routing and scheduling [9]–[13]. These techniques are often scale poorly when network sizes increase and system parameters change. To address these shortcomings, new MADRL-based approaches such as [13] and [9] have been proposed, but they suffer from limited scalability due to node-speciﬁc policy generated from the training, requiring a re-training every time a new node needs to be introduced to the network."

> _[Introduction]_

"To the best of our knowledge, no study has been reported on successfully achieving both scalability and robust performance simultaneously using MADRL in dynamic networks such as MANET. Our DeepCQ+ is both scalable and robust by allowing MADRL to control the next-hop adaptive ﬂooding decisions while maintaining the CQ+ routing protocol "structure"."

### Cited references (resolved from the paper's bibliography)
- **[5]** J. A. Boyan, M. L. Littman. *Packet routing in dynamically changing networks: A reinforcement learning approach.* NeurIPS 1994.
- **[6]** R. S. Sutton, A. G. Barto. *Reinforcement learning: An introduction.* MIT Press 2018.
- **[7]** S. Kumar, R. Miikkulainen. *Confidence-based Q-routing: An online adaptive network routing algorithm.* Proc. Artificial Neural Networks in Engineering 1998.
- **[8]** M. Johnston, C. Danilov, K. Larson. *A reinforcement learning approach to adaptive redundancy for routing in tactical networks.* MILCOM 2018.
- **[9]** R. E. Ali, B. Erman, E. Baştuğ, B. Cilli. *Hierarchical deep double Q-routing.* ICC 2020.
- **[10]** C. Yu, J. Lan, Z. Guo, Y. Hu. *DROM: Optimizing the routing in software-defined networks with deep reinforcement learning.* IEEE Access 2018.
- **[11]** G. Stampa, M. Arias, D. Sánchez-Charles, V. Muntés-Mulero, A. Cabellos. *A deep-reinforcement learning approach for software-defined networking routing optimization.* arXiv:1709.07080 2017.
- **[12]** H. Ye, G. Y. Li, B.-H. F. Juang. *Deep reinforcement learning based resource allocation for V2V communications.* IEEE Transactions on Vehicular Technology 2019.
- **[13]** X. You, X. Li, Y. Xu, H. Feng, J. Zhao, H. Yan. *Toward packet routing with fully distributed multiagent deep reinforcement learning.* IEEE Transactions on Systems, Man, and Cybernetics: Systems 2020.
