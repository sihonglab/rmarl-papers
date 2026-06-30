# 78. Fully Byzantine-Resilient Distributed Multi-Agent Q-Learning

## Metadata
- **Title**: Fully Byzantine-Resilient Distributed Multi-Agent Q-Learning
- **Authors**: Haejoon Lee, Dimitra Panagou
- **Affiliation**: Department of Robotics, University of Michigan, Ann Arbor, MI, USA
- **Venue**: Not specified (arXiv preprint, arXiv:2604.02791v1 [cs.MA], 3 Apr 2026)
- **Link/arXiv**: arXiv:2604.02791v1

## Taxonomy
- **Robustness / perturbation type targeted**: Byzantine fault tolerance / communication attacks in distributed cooperative MARL; specifically a Byzantine *edge* attack model where messages on communication links are arbitrarily altered or dropped (rather than fully compromised nodes).
- **Method paradigm**: Consensus-based distributed (QD-)Q-learning with a redundancy-based two-hop message-validation filter; almost-sure convergence analysis; graph-topological condition design ((r, r′)-redundancy).
- **Keywords**: Byzantine resilience, distributed MARL, QD-learning, two-hop redundancy filtering, (r, r′)-redundancy, optimal value-function convergence

## TL;DR
The paper proposes FRQD-learning, a fully resilient distributed Q-learning algorithm that uses two-hop redundancy-based message filtering to validate incoming Q-values, guaranteeing almost-sure convergence of all agents to the *exact* optimal value functions under F-total Byzantine edge attacks — improving over prior resilient MARL methods that only reach near-optimal solutions or require co-NP-complete robustness conditions.

## Problem & Motivation
Distributed cooperative MARL lets networked agents learn a shared global objective (e.g., the average of local rewards) by exchanging local information, but such algorithms are highly vulnerable to adversarial/Byzantine corruption of shared information during training. Existing resilient MARL methods generally only guarantee convergence to a *neighborhood* of the optimal value functions (because value-clipping/extreme-value filtering breaks the symmetry of information flow, effectively producing a directed network and biasing updates), or they require the communication network to satisfy robustness conditions such as (2F+1)-robustness whose verification is co-NP-complete and thus impractical at scale; alternatives that avoid robustness conditions require a trusted central coordinator. The paper instead targets a slightly weaker but practical adversarial model (Byzantine *edge* attacks) and asks: can every agent provably learn the *exact* optimal value functions using only local interactions, with no central coordinator and no structural assumptions on the problem?

## Robustness Setting
- **Threat model / uncertainty set**: F-total Byzantine edge attack (Definition 1). An omniscient adversary may, in each communication round, arbitrarily alter or drop the message sent over up to F edges (bidirectionally), affecting at most 2F agents per round. Unlike node-compromise Byzantine models, only communication links are unreliable; all agents are cooperative and follow the prescribed protocol (Assumption 1). The attack is point-to-point (an attacker need not broadcast the same value to all neighbors).
- **Setting**: Cooperative; fully decentralized (no central coordinator); online model-free Q-learning over a simple, undirected, time-varying communication graph; networked multi-agent MDP minimizing infinite-horizon discounted global cost (average of local costs).

## Method
- Builds on consensus-based distributed Q-learning (QD-learning) [6], where each agent updates its Q-values via a local Bellman/innovation term plus a consensus term over neighbor Q-values; the core difficulty is choosing the neighbor set P^i_N(t) so the *induced* communication stays undirected despite attacks.
- Key idea — two-hop redundancy filtering: each agent receives the same two-hop neighbor's Q-value through multiple independent one-hop paths and cross-validates these redundantly relayed copies; corrupted copies are filtered before being used.
- FRQD-learning (Algorithm 1) runs two communication rounds with six steps: (1) receive (x_t, u_t, c_i); (3) exchange (Q^i_{x_t,u_t}(t), i) tuples with one-hop neighbors; first filtering (lines 4-6) keeps only tuples whose index appears exactly once and is not the agent's own; (7) relay the filtered set K_i(t) to neighbors and collect into C_i(t); second filtering (lines 8-12) trusts a value for agent k only if it appears at least 3F+1 times; (13-14) update Q^i via (5) using the validated set P^i(t) and set V^i = min_u Q^i.
- The validated update is shown to be mathematically equivalent to running plain QD-learning on the (6F+1)-2-hop graph of G(t), so existing QD-learning convergence theory applies under the new topological condition.
- (r, r′)-redundancy (Definition 3): a topological condition on the r-2-hop graph (where an edge needs ≥ r shared neighbors). (6F+1, 0)-redundancy is the sufficient condition that guarantees symmetric validation and recovers convergence; the paper gives a systematic graph construction (Proposition 1) and an O(n^3) verification procedure (Proposition 2).

## Theoretical Contributions
- **Lemma 2**: under an F-total Byzantine edge attack, after the two communication rounds the multiset L^i_k(t) contains at most 3F corrupted values for any other agent k, so any value appearing ≥ 3F+1 times must be correct (justifying the line-11 threshold).
- **Lemma 3**: under (6F+1, 0)-redundancy, FRQD-learning's update is equivalent to QD-learning on the (6F+1)-2-hop graph (Laplacian form), with the induced graph connected and undirected.
- **Theorem 1**: under Assumptions 1-3 and a (6F+1, 0)-redundant graph under F-total Byzantine edge attack, every agent's Q_i(t) → Q* and V_i(t) → V* almost surely — exact (not near-optimal) convergence.
- **Proposition 1**: a constructive method to build (r, r′)-redundant graphs for any r > r′ ≥ 0.
- **Proposition 2**: (r, r′)-redundancy can be verified in O(n^3) (polynomial time), contrasting with the co-NP-complete r-robustness check; Remark 4 notes the constructed graph is at least ⌈(r+1)/2⌉-robust.

## Experiments
- **Environment/Benchmark**: Simulated networked multi-agent MDP — n = 10 heterogeneous robots assigning robot-pairs to six sequential tasks (state space {1,...,7}, action space U = {(i,j) | i≠j}), with state- and pair-dependent transition dynamics (12) and local costs (13), γ = 0.9. Agents communicate over a (7, 0)-redundant graph (also 4-robust) under F = 1-total Byzantine edge attack.
- **Baselines**: Oracle = vanilla QD-learning [6] with no attack (ground-truth optimal); Baseline = the resilient QD-learning method of [22], [24] (without the event-triggering mechanism).
- **Evaluation metrics**: Convergence of agents' Q-values to the optimal Q-values (e.g., for state 1 and actions (0,1), (0,2)); correctness of the recovered optimal policies across states x = 1,...,6 (Table I).

## Key Results
- Under FRQD-learning all agents converge almost surely to the true optimal Q-values despite the Byzantine edge attack, whereas the Baseline fails to converge to the optimal values.
- All agents under the proposed method recover the true optimal policies for all states (matching the Oracle), while the Baseline produces incorrect policies for states x = 1, 4, 5, 6 (Table I).
- The (6F+1, 0)-redundancy condition is verifiable in polynomial time O(n^3), unlike the co-NP-complete (2F+1)-robustness conditions required by prior robustness-based resilient MARL methods.

## Limitations & Future Work
- Communication overhead: the second relay round costs up to O(|N_i(t)|^2) per agent; reducing this while preserving Theorem 1's guarantees is left as future work (Remark 1).
- Restricted adversary: results hold for the (weaker) Byzantine *edge* attack model, not full node-compromise Byzantine agents; the analysis assumes all agents are cooperative (Assumption 1).
- Simulations use a single fixed (7,0)-redundant graph with n = 10 and F = 1 (the Baseline only supports static networks), though the method is stated to generalize to time-varying graphs.
- The precise relationship between (r, r′)-redundancy and r-robustness is left open (Remark 4).
- Future work: extend the framework to actor-critic architectures.

## Relevance to Survey
This paper sits on the **fault tolerance / Byzantine resilience** and **communication-robustness** lines of robust MARL, addressing adversarial corruption of inter-agent communication in fully decentralized cooperative learning. It connects the distributed/consensus MARL line (QD-learning, networked actor-critic) with the resilient-distributed-systems literature (Byzantine consensus, optimization, federated learning) and the graph-theoretic robustness line (r-robustness vs. the proposed (r, r′)-redundancy). Distinctively, it provides *exact* optimal-value convergence guarantees and a polynomial-time-verifiable topological condition, contrasting with the near-optimal guarantees and co-NP-complete robustness requirements typical of prior resilient MARL with function approximation.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction]_

"One of the challenges in these decentralized frameworks is that agents receive local rewards from the environment, making the computation of optimal global value functions impossible without information sharing. To this end, a variety of frameworks have been developed. A consensus-based distributed Q-learning (QD-learning) has been proposed in [6], enabling agents to asymptotically compute the average of their optimal value functions through exchanges of state-action value estimates. Subsequent work introduced distributed actor-critic frameworks using linear function approximations [3], [7]. To ensure scalability, [4], [5] studied scalable actor-critic algorithms where agents maintain state-action information only for their multi-hop neighbors."

> _[Section I, Introduction]_

"Despite these merits, distributed MARL algorithms, just like other distributed algorithms, are highly vulnerable to adversarial attacks that corrupt or share faulty information during their training. In the distributed systems literature, the Byzantine model defines an omniscient adversary capable of injecting arbitrary errors or disruptions via hardware, software, and communication compromises [8], [9]. Thus, many resilient algorithms have been studied to counter or contain the impacts of Byzantine agents in distributed consensus [9]–[13], optimization [8], [14]–[16], and learning frameworks [17]–[20]. Similarly, Byzantine-resilient distributed MARL has been studied in recent years. Early studies showed that even a single adversarial agent can severely disrupt the learning process in cooperative MARL algorithms [21], [22]. It has been established in [23] that exact evaluation of the honest agents' average reward is generally impossible under Byzantine attacks."

> _[Section I, Introduction]_

"To address this vulnerability, several resilient MARL algorithms have been proposed. The QD-learning algorithm from [6] was adapted in [22], [24] to ensure convergence despite Byzantine agents. Other works have utilized linear function approximation to learn Q-values with adversarial attacks [25]–[27]. However, these methods generally only guarantee convergence to near-optimal value functions, and therefore cannot guarantee learning of the true optimal policies. Furthermore, many of these approaches require the communication network to satisfy robustness conditions (e.g., (2F +1)-robustness). Since verifying such properties is a co-NP-complete problem [28], the application of these approaches to large-scale networks is limited. While [29]–[31] proposed an alternative algorithm that avoids such robustness conditions, they require a trusted central coordinator."

> _[Section I, Introduction]_

"In this work, we propose a fully resilient distributed Q-learning algorithm under which agents achieve almost sure convergence to optimal value functions in the presence of Byzantine edge attack, a restricted variant of the Byzantine model, in a decentralized network. By focusing on edge-level adversaries only, we provide stronger learning guarantees than prior work [16], [22], [24], which achieves only near-optimal convergence or requires additional structural assumptions on Q-values or local objectives. The key feature of our method is that it relies on redundant two-hop information to verify incoming messages and filter adversarial injections. We prove that under a novel topological condition, this approach ensures almost sure convergence to the optimal solution without any structural assumptions on the problem."

> _[Section III, Fully Resilient QD-Learning]_

"While Byzantine resilient variants of QD-learning have been proposed [24], [25], [27], these methods in general only guarantee convergence to the neighborhood of the optimal value functions. This is because the methods rely on each agent i modifying Pi N(t) in (5) by filtering extreme neighbor values. Such filtering can induce asymmetric information exchange, effectively resulting in a directed communication network and introducing biases into the update. Under such situation, convergence to the optimal value functions is generally not guaranteed (cf. [22, Remark 3])."

> _[Section III, Remark 2]_

"Our algorithm uses multi-path redundancy for validation and directly incorporates validated two-hop messages into the update. This differs from works such as [11], [34], which use two-hop messages only to detect and isolate malicious agents from updates. Moreover, our approach provides resilience against point-to-point Byzantine communication attacks, whereas these works consider adversaries that only broadcast the same values to all neighbors."

> _[Section IV, Construction of Redundant Network Graph]_

"While (2F + 1)-robustness provides a sufficient condition for Byzantine-resilient QD-learning in other MARL frameworks [25], [26], [29], determining whether a graph satisfies this property is co-NP-complete and thus computationally expensive [28], [36]. This computational bottleneck renders robustness-based design impractical for large-scale and dynamic networks. In contrast, (r, r′)-redundancy offers a tractable alternative, making our approach more suitable."

### Cited references (resolved from the paper's bibliography)
- **[3]** K. Zhang, Z. Yang, H. Liu, T. Zhang, T. Başar. *Fully decentralized multi-agent reinforcement learning with networked agents.* ICML 2018.
- **[4]** Y. Lin, G. Qu, L. Huang, A. Wierman. *Multi-agent reinforcement learning in stochastic networked systems.* NeurIPS 2021.
- **[5]** G. Qu, A. Wierman, N. Li. *Scalable reinforcement learning of localized policies for multi-agent networked systems.* L4DC 2020.
- **[6]** S. Kar, J. M. F. Moura, H. V. Poor. *QD-learning: A collaborative distributed strategy for multi-agent reinforcement learning through consensus+innovations.* IEEE Transactions on Signal Processing, 2013.
- **[7]** S. Zeng, T. Chen, A. Garcia, M. Hong. *Learning to coordinate in multi-agent systems: A coordinated actor-critic algorithm and finite-time guarantees.* L4DC 2022.
- **[8]** L. Su, N. H. Vaidya. *Byzantine-resilient multiagent optimization.* IEEE Transactions on Automatic Control, 2021.
- **[9]** H. J. LeBlanc, H. Zhang, X. Koutsoukos, S. Sundaram. *Resilient asymptotic consensus in robust networks.* IEEE Journal on Selected Areas in Communications, 2013.
- **[10]** S. M. Dibaji, M. Safi, H. Ishii. *Resilient distributed averaging.* American Control Conference (ACC) 2019.
- **[11]** L. Yuan, H. Ishii. *Resilient average consensus with adversaries via distributed detection and recovery.* IEEE Transactions on Automatic Control, 2025.
- **[12]** H. Lee, D. Panagou. *Partial resilient leader-follower consensus in time-varying graphs.* American Control Conference (ACC) 2026.
- **[13]** H. Lee, D. Panagou. *Distributed resilience-aware control in multi-robot networks.* IEEE Conference on Decision and Control (CDC) 2025.
- **[14]** S. Sundaram, B. Gharesifard. *Distributed optimization under adversarial nodes.* IEEE Transactions on Automatic Control, 2019.
- **[15]** M. Yemini, A. Nedić, A. J. Goldsmith, S. Gil. *Resilient distributed optimization for multiagent cyberphysical systems.* IEEE Transactions on Automatic Control, 2025.
- **[16]** Y. Zhai, Z.-W. Liu, D. Yue, S. Hu, C. Deng, L. Ye. *Byzantine-resilient multiagent distributed optimization under redundancy.* IEEE Transactions on Control of Network Systems, 2025.
- **[17]** C. Fang, Z. Yang, W. U. Bajwa. *Bridge: Byzantine-resilient decentralized gradient descent.* IEEE Transactions on Signal and Information Processing over Networks, 2022.
- **[18]** Y. Chen, L. Su, J. Xu. *Distributed statistical machine learning in adversarial settings: Byzantine gradient descent.* 2017.
- **[19]** X. Lin, Y. Li, X. Xie, Y. Ding, X. Wu, C. Ge. *Sf-cabd: Secure byzantine fault tolerance federated learning on non-iid data.* Knowledge-Based Systems, 2024.
- **[20]** P. Blanchard, E. M. El Mhamdi, R. Guerraoui, J. Stainer. *Machine learning with adversaries: Byzantine tolerant gradient descent.* NeurIPS 2017.
- **[21]** M. Figura, K. C. Kosaraju, V. Gupta. *Adversarial attacks in consensus-based multi-agent reinforcement learning.* American Control Conference (ACC) 2021.
- **[22]** Y. Xie, S. Mou, S. Sundaram. *Towards resilience for multi-agent QD-learning.* IEEE Conference on Decision and Control (CDC) 2021.
- **[23]** Hairi, M. Fang, Z. Zhang, A. Velasquez, J. Liu. *On the hardness of decentralized multi-agent policy evaluation under byzantine attacks.* WiOpt 2024.
- **[24]** Y. Xie, S. Mou, S. Sundaram. *Communication-efficient and resilient distributed q-learning.* IEEE Transactions on Neural Networks and Learning Systems, 2023.
- **[25]** Z. Wu, H. Shen, T. Chen, Q. Ling. *Byzantine-resilient decentralized policy evaluation with linear function approximation.* IEEE Transactions on Signal Processing, 2021.
- **[26]** J. Yao, X. Gong. *Communication-efficient and resilient distributed deep reinforcement learning for multi-agent systems.* IEEE International Conference on Unmanned Systems (ICUS) 2024.
- **[27]** L. Ye, M. Figura, Y. Lin, M. Pal, P. Das, J. Liu, V. Gupta. *Resilient multiagent reinforcement learning with function approximation.* IEEE Transactions on Automatic Control, 2024.
- **[28]** H. Zhang, E. Fata, S. Sundaram. *A notion of robustness in complex networks.* IEEE Transactions on Control of Network Systems, 2015.
- **[29]** Y. Lin, S. Gade, R. Sandhu, J. Liu. *Toward resilient multi-agent actor-critic algorithms for distributed reinforcement learning.* American Control Conference (ACC) 2020.
- **[30]** Q. Lin, Q. Ling. *Robust reward-free actor–critic for cooperative multiagent reinforcement learning.* IEEE Transactions on Neural Networks and Learning Systems, 2024.
- **[31]** M. Fang, X. Wang, N. Z. Gong. *Provably robust federated reinforcement learning.* ACM Web Conference (WWW) 2025.
- **[34]** C. N. Hadjicostis, A. D. Domínguez-García. *Trustworthy distributed average consensus based on locally assessed trust evaluations.* IEEE Transactions on Automatic Control, 2025.
- **[36]** H. Lee, D. Panagou. *Minimal construction of graphs with maximum robustness.* arXiv preprint arXiv:2507.00415, 2025.
