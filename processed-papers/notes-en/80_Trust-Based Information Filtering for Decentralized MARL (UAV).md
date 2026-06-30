# 80. Trust-Based Information Filtering for Robust Decentralized Execution of Pre-Trained MARL Policies in UAV Swarms

## Metadata
- **Title**: Trust-Based Information Filtering for Robust Decentralized Execution of Pre-Trained MARL Policies in UAV Swarms
- **Authors**: Ernests Rudzītis, Alessandro Chiumento
- **Affiliation**: Pervasive Systems Group, EEMCS Faculty, University of Twente, The Netherlands
- **Venue**: 2025 16th IFIP Wireless and Mobile Networking Conference (WMNC) 2025
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Communication robustness / unreliable inter-agent communication (stale "frozen" messages / replay, persistent offset bias from compromised agents or biased sensors, random Gaussian channel noise); message manipulation / corruption at the receiving end.
- **Method paradigm**: Post-hoc trust mechanism, anomaly/outlier detection (Local Outlier Factor), spatio-temporal feature engineering, unsupervised self-configuration, message recovery/reconstruction heuristics (layered onto a pre-trained CTDE MAPPO policy).
- **Keywords**: Trust-Based Information Filtering (TIF), communication robustness, UAV swarm, MARL, anomaly detection, post-hoc / pre-trained policy

## TL;DR
The paper introduces Trust-Based Information Filtering (TIF), a decentralized, post-hoc module that equips each agent of a pre-trained MARL UAV swarm with a self-configured anomaly detector (Local Outlier Factor over engineered spatio-temporal features) plus lightweight recovery heuristics, so message trustworthiness can be assessed and unreliable communication filtered/reconstructed at execution time without retraining or attack data.

## Problem & Motivation
MARL-based UAV swarms rely heavily on inter-agent communication (positions, velocities, formation intentions), but channels can be noisy, sensors can malfunction, and messages can be intentionally manipulated by compromised agents or external foes, causing mission failure or unsafe operation. Existing trust/robustness solutions either integrate countermeasures directly into MARL training (restricting algorithm choice, increasing training complexity, requiring costly retraining), rely on pre-configured protocols such as cryptography (heavy setup, poor in-mission adaptability), or use simple outlier filters that lack contextual understanding against subtle or previously unknown disruptions. The paper targets this gap: a decentralized, post-hoc trust mechanism that strengthens pre-trained policies against unreliable communication without retraining or requiring adversarial data.

## Robustness Setting
- **Threat model / uncertainty set**: Communication is modeled as an ideal broadcast where each drone transmits its internal state; the TIF operates at the receiving end. Received peer information may be corrupted, stale, or manipulated. Three unreliability modes are injected: (1) Message Freezing (stale last-known value, simulating a replay attack or connection discrepancy); (2) Message Offset (a consistent additive error, simulating a compromised agent or persistently biased sensor); (3) Random Noise Injection (Gaussian noise on transmitted contents, simulating channel noise or minor sensor inaccuracy). Compromise rates of 10%, 20%, 30% are evaluated. No prior attack data or threat intelligence is assumed.
- **Setting**: Cooperative; Centralized Training with Decentralized Execution (CTDE) with explicit inter-agent communication; robustness module applied post-hoc at decentralized execution (the base policy is trained offline/in simulation under ideal communication, the TIF self-configures from recorded normal operation, then operates online during execution).

## Method
- **Post-hoc trust layer**: TIF sits between incoming communication and each agent's pre-trained MARL policy (MAPPO, CTDE). It is decoupled from training, operates only on features of the policy's inputs, and requires no policy modification or retraining (Modularity, Self-Configuring, Generality principles).
- **Spatio-temporal feature engineering**: Features are extracted from incoming observation data and organized into five groups capturing spatio-temporal consistency: Temporal Consistency (generic; magnitude/component-wise change between current and previous observations), Inter-Agent Consistency (generic; pairwise differences and summary statistics across agents), Motion Consistency (specific; velocity magnitude, position-vs-predicted-position), Formation-Aware (specific; distance from centroid, velocity alignment), and Anomaly Pattern (mixed; observation variance, extreme-value ratios). Inter-agent features scale O(N) with swarm size; intra-agent features are O(1).
- **Trust assessment (anomaly detection)**: A Local Outlier Factor (LOF) model, a density-based outlier detector measuring local deviation relative to neighbours, is fit on the normal-operation feature dataset and outputs a binary trust assessment per incoming message (n_neighbors = 20).
- **Information Filtering Logic (IFL)**: Trusted messages pass unaltered; untrustworthy messages are not discarded but reconstructed via one of two lightweight recovery heuristics — Historical Average Recovery (component-wise average over a recent history window; smoothing) or Trend Extrapolation Recovery (linear trend from the last two trusted observations extrapolated one step; projection).
- **Data-driven self-configuration**: A baseline of ~60,000 feature vectors is collected from 100 episodes (max 200 steps each) of normal swarm operation under ideal communication; a unified thresholding strategy uses a contamination parameter of 0.05 (flag the 5% most unusual samples), passed directly to LOF during fitting — no complex hyperparameter search or labeled attack data needed.

## Theoretical Contributions
None / mostly empirical. The contribution is a system design and empirical validation; no convergence, sample-complexity, or certified-robustness guarantees are provided.

## Experiments
- **Environment/Benchmark**: A custom 2D drone simulation environment adhering to the PettingZoo API; task is a swarm of three UAVs achieving and maintaining a V-shaped formation. Base policy: MAPPO under CTDE (each agent with its own critic having full global state at training), trained for 2 million environment steps (episodes up to 200 steps) under ideal communication.
- **Baselines**: The baseline pre-trained MARL policy without TIF (compared against the same policy enhanced with TIF). Internal comparisons across feature-group configurations (Table II), anomaly recovery strategies (Historical Average vs. Trend Extrapolation), and the LOF anomaly detector.
- **Evaluation metrics**: F1-score and accuracy for trust/anomaly discrimination across feature configurations and compromise types; mean formation error (and percentage improvement) of the swarm under noise/offset/freeze compromise types and varying compromise rates.

## Key Results
- Feature discrimination: the comprehensive group (T, M, I, F) reached near-perfect F1 0.999 (±0.002) / accuracy 0.999 (±0.001); temporal_only alone reached F1 0.997 (±0.003), showing a single well-chosen temporal feature is highly effective; noise and offset were generally easier to detect (F1 near 1.000) while freezing was the most challenging.
- Robustness enhancement: TIF achieved an overall 6.8% reduction in mean formation error; most effective against sensor noise (9.5% improvement), 6.8% against offset, and least effective against message freezing (3.8%, since slowly changing stale data evades consistency checks).
- Recovery strategy: Historical Average Recovery outperformed Trend Extrapolation by ~13% on average at reducing formation error; under its optimal configuration TIF reached a maximum 33.6% improvement over the baseline in specific scenarios.
- Degradation with compromise rate: improvement was 8.3% at 10% compromise rate, diminishing to 6.1% and 6.0% at 20% and 30% rates respectively, indicating continued (but reduced) benefit as communication quality degrades.

## Limitations & Future Work
- Evaluation was in a custom 2D simulation; future work should validate in high-fidelity 3D environments and ultimately on physical UAV hardware with real-world physics and communication latencies.
- The baseline of "normal" behaviour is static and configured once; long-duration or dynamically changing missions may shift normal patterns, motivating online/adaptive learning of the trust model.
- Only relatively simple communication issues (freeze, offset, Gaussian noise) were tested; a key next step is resilience against more sophisticated, adaptive adversaries that strategically mimic normal behaviour.
- Recovery relies on simple heuristics; future iterations could use advanced generative reconstruction (e.g., VAEs, GANs). Scalability and performance in larger, more complex swarms also remain to be explored.

## Relevance to Survey
This paper sits on the communication-robustness branch of robust MARL: rather than adversarial training or robust-MDP formulations, it proposes a lightweight, post-hoc, anomaly-detection-based trust filter layered onto an already-trained cooperative CTDE policy (MAPPO). It connects to the communication-attack / message-perturbation defense line (e.g., AME certified-robust communication, message detection-and-reconstruction, Gaussian-process message filtering, and trust/consensus-based MARL), and to fault-tolerance and safety themes for multi-agent systems. Its distinctive angle for the survey is the "robustness without retraining" / plug-and-play execution-time defense paradigm.

## Related Work (verbatim excerpts from the paper)
> _[Section I.A, Background and Context / Introduction]_

"Mission success for MARL-based UAV swarms depends heavily on inter-agent communication quality and reliability. Cooperative MARL policies often rely on exchanged messages (e.g., positions, velocities, formation intentions) to communicate and achieve coherent group behaviour. In practice, communication channels can be noisy, sensors that provide data readings can malfunction, and in adversarial scenarios, communication can be intentionally manipulated by compromised agents or extrinsic foes [5]. This reliance introduces a significant vulnerability, potentially causing mission failure or unsafe operations [6]."

"Using trust mechanisms to improve robustness is crucial but underexplored, particularly for pre-trained policies. Existing approaches often integrate countermeasures directly into the MARL training process itself [7]. While effective, this can restrict algorithm choice, increase training complexity, and require costly retraining. Other strategies involve pre-configured protocols like cryptographic methods [8], which require considerable setup effort and may not adapt to unreliability during a mission. Conversely, simple post-hoc outlier detection filters lack the contextual understanding to be effective against subtle or prior unknown disruptions."

> _[Section II, Problem Statement and Existing Works]_

"There are several research works that aim to integrate trust or robustness into MARL systems. These works fall into two categories. The first category involves integrating these mechanisms directly in the MARL training process. The research work by Fung et al. [7] proposes Reinforcement Learning-based Trusted Consensus (RLTC), a reinforcement learning approach where agents explicitly learn trust scores for neighbor agents by means of Q-learning during training phase."

"The second category relates to filtering or modification of communication. Xue et al. [9] propose a two-stage protocol to detect and reconstruct malicious messages. This method focuses on correcting perturbations using a model trained to reverse specific, anticipated manipulations from an adversary. The research work by Sun et al. [10] introduces the Ablated Message Ensemble (AME) defensive mechanism, which guarantees the performance of agents when a fraction of communication messages are perturbed; robustness was assured post-hoc by making decisions based on the majority vote from multiple base actions, each generated using a randomly chosen subset of the incoming messages. Mitchell et al. [11] proposed a different approach using Gaussian Processes to model expected message correlations based on agent proximity, allowing inconsistent messages to be identified and down-weighted."

"Finally, concepts from adjacent fields like distributed consensus and security are also relevant. The research work by Han et al. [8] on trust for UAV swarms specifically, focuses on achieving secure agreement on specific values using cryptographic protocols."

"In summary, existing research addresses MARL robustness via integrated learning methods, post-hoc filtering, and security protocols. This review highlights an opportunity for a prototype focused on dynamically learned trust from observed normal behaviour. Such a mechanism, adaptable to pre-trained policies without retraining or threat intelligence, could enhance resilience against general communication unreliability. This paper proposes and investigates such a system."

### Cited references (resolved from the paper's bibliography)
- **[5]** X. Zheng, X. Ma, S. Wang, X. Wang, C. Shen, C. Wang. *Toward evaluating robustness of reinforcement learning with adversarial policy.* 2024 54th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN) 2024.
- **[6]** B. Xu, G. Bai, Y. Zhang, Y. Fang, J. Tao. *Failure analysis of unmanned autonomous swarm considering cascading effects.* Journal of Systems Engineering and Electronics, 2022.
- **[7]** H. L. Fung, V.-A. Darvariu, S. Hailes, M. Musolesi. *Trust-based consensus in multi-agent reinforcement learning systems.* 2024.
- **[8]** P. Han, X. Wu, A. Sui. *DTPBFT: a dynamic and highly trusted blockchain consensus algorithm for UAV swarm.* Computer Networks, 2024.
- **[9]** W. Xue, W. Qiu, B. An, Z. Rabinovich, S. Obraztsova, C. K. Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* 2022.
- **[10]** Y. Sun, R. Zheng, P. Hassanzadeh, Y. Liang, S. Feizi, S. Ganesh, F. Huang. *Certifiably robust policy learning against adversarial communication in multi-agent systems.* 2022.
- **[11]** R. Mitchell, J. Blumenkamp, A. Prorok. *Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication.* 2020.
