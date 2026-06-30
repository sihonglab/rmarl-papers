# 138. Robust Multi-agent Federated Reinforcement Learning for Task Offloading

## Metadata
- **Title**: Robust Multi-agent Federated Reinforcement Learning for Task Offloading
- **Authors**: Dibao Yan, Yongfeng Wang, Wenjing Hou, Huanhuan Song, Hong Wen, Wendi Ma, Fan Sun
- **Affiliation**: School of Aeronautics and Astronautics, University of Electronic Science and Technology of China (UESTC), Chengdu, China; Aircraft Swarm Intelligent Sensing and Cooperative Control Key Laboratory of Sichuan Province; Sichuan Intelligent IoT Communication Technology Engineering Research Center, UESTC
- **Venue**: WCNA 2023 (Proceedings published in LNEE vol. 1361, pp. 211–218, Springer, 2025)
- **Link/arXiv**: https://doi.org/10.1007/978-981-96-2409-6_21

## Taxonomy
- **Robustness / perturbation type targeted**: Malicious/Byzantine nodes in federated aggregation; reward poisoning (reward inversion / "reward flip" attack); fault tolerance against corrupted model updates
- **Method paradigm**: Multi-agent deep RL (TD3) + federated learning (FedAvg) with statistical outlier detection (Euclidean distance + Modified Z-score / MAD) for malicious-node filtering
- **Keywords**: task offloading, malicious node detection, federated learning, multi-agent deep reinforcement learning, reward inversion attack, edge computing

## TL;DR
Proposes a federated learning strategy built on multi-agent TD3 for edge-computing task offloading that aggregates per-node policies via FedAvg while detecting and excluding malicious nodes (using Euclidean distance and a Modified Z-score test), and shows it resists reward-inversion attacks while still learning effective offloading strategies.

## Problem & Motivation
With the proliferation of lightweight IoT/mobile devices that have limited computing power and battery life, edge computing and computational offloading are needed to reduce computational delay and energy consumption. To learn task-offloading policies across diverse, complex scenarios, the paper aggregates the training strategies of multiple edge devices via federated learning, improving generalization across environments. A key open issue is that federated aggregation involves multiple data nodes whose safety/reliability is uncertain; malicious nodes can corrupt the aggregated model. The paper therefore targets both better cross-scenario offloading policies and protection against malicious participants.

## Robustness Setting
- **Threat model / uncertainty set**: Malicious nodes participate in federated aggregation and conduct a reward inversion ("reward flip") attack — they modify/invert the reward in their experience replay pool during local training so as to learn the worst task-offloading strategy, then upload these corrupted parameters to poison the FedAvg aggregate. The defense models normal nodes as training "in the same direction," so malicious nodes appear as statistical outliers in the Euclidean distance of network parameters.
- **Setting**: Cooperative/distributed multi-agent (multiple edge devices/agents across multiple offloading scenarios); federated (distributed training with central aggregation); online deep RL.

## Method
- Formulates task offloading as minimizing a combined energy-efficiency objective A(x) (weighted sum of energy consumption and latency for local vs. edge execution with a binary offloading decision x_n(t)); since the objective is hard to solve directly, deep RL is used and the energy-efficiency function is inverted into a maximization (reward).
- Each agent is trained with Twin Delayed Deep Deterministic Policy Gradient (TD3): two critic networks Q_θ1, Q_θ2 with target networks, an actor μ_φ with target actor, experience replay over tuples (s, a, r, s', d), clipped/double-Q target value estimation, delayed policy updates, target policy smoothing, and soft target updates.
- After each round, nodes upload model parameters to an aggregation node; pairwise Euclidean distances of the neural-network parameters are computed and the Modified Z-score method (using the median and Median Absolute Deviation, MAD) flags outliers as potential malicious nodes when |z_i| > threshold.
- Outlier (malicious) model data are excluded; the remaining reliable model parameters are aggregated via FedAvg and redistributed to all nodes; the train–detect–aggregate cycle repeats.

## Theoretical Contributions
None / mostly empirical. The paper provides only definitions (energy/latency model, Z-score and Modified Z-score formulas, MAD) and an algorithmic procedure; no convergence, sample-complexity, or robustness-certification proofs are given.

## Experiments
- **Environment/Benchmark**: Simulated edge-computing task-offloading environment with five task-offloading scenarios and five offloading decision-making agents; 10,000 aggregation rounds total, 10 model updates per node after each aggregation, batch size 128. Malicious participation is induced by modifying the training set during local model training (reward inversion).
- **Baselines**: FedAvg aggregation without malicious-node detection (no-attack baseline and attacked-without-defense case), compared against the proposed method that adds Modified Z-score malicious-node filtering. (No external algorithm baselines reported.)
- **Evaluation metrics**: Reward (convergence) curves over aggregation rounds, compared across no-attack, attack-without-defense, and attack-with-defense settings.

## Key Results
- Without attack, FedAvg aggregation converges to a reward of around −230 after about 3700 aggregation rounds.
- With a malicious node performing reward inversion and no defense, the aggregated reward fluctuates within roughly [−350, 350] and shows no convergence trend.
- Applying the Modified Z-score detection under attack restores convergence at about 3800 rounds, with the curve closely resembling the no-attack case — demonstrating that the TD3-based federated strategy can match no-attack performance while resisting the attack.
- A single malicious node consistently drives toward the worst task-offloading strategy (its reward converges to the worst value), confirming the attack's effect when undetected.

## Limitations & Future Work
Not specified. (The paper studies a single attack type — reward inversion — with a small-scale simulation of five agents/scenarios and a single aggregation node, and does not discuss limitations, broader threat models, or future directions.)

## Relevance to Survey
This paper sits on the fault-tolerance / Byzantine-robustness and reward-poisoning lines of robust MARL, specialized to the federated multi-agent RL setting for edge-computing task offloading. Rather than the robust-MDP/minimax or distributionally robust theory lines, it represents a practical defense approach: statistical anomaly detection (Euclidean distance + Modified Z-score/MAD) to filter malicious model updates before aggregation. It connects robust MARL to federated RL, malicious-node/Byzantine-resilient aggregation, and reward-poisoning attack-defense themes.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Edge computing positions resources at the edge of the network closer to users to provide IT service environment and cloud computing capabilities for mobile networks, thus providing users with ultra-low latency and high-efficiency network service solutions [3, 4]. As one of the key technologies in edge computing, computing offloading refers to the technology in which terminal devices transfer part or all computing tasks to the cloud computing environment to solve the shortcomings of mobile devices in resource storage, computing performance and energy efficiency."

"The task offloading process always affected by many aspects, such as the external environment and the offloading system. Therefore, in order to enable edge computing devices to learn task offloading policies in a variety of complex task offloading scenarios, the training strategies of multiple edge computing devices are aggregated in combination with the characteristics of distributed security data sharing based on federated learning [5]. Learn better task offloading strategies to adapt to more diverse scenarios. At the same time, there are often multiple data nodes in federated learning, and whether each data node is safe and reliable is another key issue."

> _[Section 2.2, Multi-agent Deep Reinforcement Learning Algorithm]_

"The core concept of Twin Delayed Deep Deterministic Policy Gradient (TD3) [7] is to utilize two independent Q-networks and a delayed policy update mechanism to mitigate estimation bias and prevent excessive policy updates. Specifically, TD3 maintains two value function networks (Critic) and a policy function network (Actor). During the value update process, TD3 employs the minimum estimates from the two critic networks for updates, which helps to reduce bias in the estimates. Additionally, TD3 adopts a delayed update strategy, where the policy function is updated only after several value function updates, enhancing the algorithm's stability. The TD3 algorithm also introduces target policy smoothing, which involves adding limited-amplitude noise to the target policy during updates, further improving the stability of the learning process."

### Cited references (resolved from the paper's bibliography)
- **[3]** Chen, X., et al. *Information freshness-aware task offloading in air-ground integrated edge computing systems.* IEEE J. Sel. Areas Commun. 40(1), 243–258, 2022.
- **[4]** Lai, X., Fan, L., Lei, X., Deng, Y., Karagiannidis, G.K., Nallanathan, A. *Secure mobile edge computing networks in the presence of multiple eavesdroppers.* IEEE Trans. Commun. 70(1), 500–513, 2022.
- **[5]** Qiao, D., Liu, G., Guo, S., He, J. *Adaptive federated learning for non-convex optimization problems in edge computing environment.* IEEE Trans. Netw. Sci. Eng. 9(5), 3478–3491, 2022.
- **[7]** Kang, C., et al. *TD3 algorithm based on dynamic delay policy update.* J. Jilin Univ. (Inf. Sci. Ed.) 38(4), 474–481, 2020.
