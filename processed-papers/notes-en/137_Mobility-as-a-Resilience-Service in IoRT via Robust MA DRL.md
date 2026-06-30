# 137. Mobility-as-a-Resilience Service in Internet of Robotic Things Through Robust Multiagent Deep Reinforcement Learning

## Metadata
- **Title**: Mobility-as-a-Resilience Service in Internet of Robotic Things Through Robust Multiagent Deep Reinforcement Learning
- **Authors**: Shi Li, Jiong Jin, Mahbuba Afrin, Xiaohua Ge, Jing Fu, Yu-Chu Tian
- **Affiliation**: Swinburne University of Technology (School of Science, Computing and Engineering Technologies), Melbourne, Australia; Curtin University; RMIT University; Queensland University of Technology
- **Venue**: IEEE Internet of Things Journal 2025 (Vol. 12, No. 23, 1 December 2025)
- **Link/arXiv**: Digital Object Identifier 10.1109/JIOT.2025.3535148

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty (unknown reward functions of other robots and system transition dynamics), observation/communication noise, reward uncertainty; UAV/hardware failures and network instability (system resilience)
- **Method paradigm**: Robust MADDPG (RMADDPG) — MADDPG with an adversarial "nature player"; domain randomization; partially observable Markov game (POMG) / Nash equilibrium; CTDE actor-critic
- **Keywords**: Internet of Robotic Things (IoRT), multiagent deep reinforcement learning (MADRL), smart farm, task allocation, robustness, nature player

## TL;DR
The paper proposes Mobility-as-a-Resilience Service (MaaRS), which relocates active UAVs to failure points for system recovery in IoRT smart-farm deployments, and devises a Robust MADDPG (RMADDPG) method — MADDPG augmented with an adversarial "nature player" — to perform dynamic task allocation that remains effective under model uncertainty, observation noise, and reward uncertainty.

## Problem & Motivation
Deploying IoRT systems for sustainable agriculture (e.g., livestock monitoring) faces network instability and hardware/UAV failures that cause data collection failures and "buffer overflow deadlines" where critical data may be lost. Standard MADRL methods such as MADDPG assume robots have accurate knowledge of the system model, but in reality robots lack full knowledge of other robots' reward functions and system transition dynamics (model uncertainty), and agricultural environments introduce disturbances and observation noise that degrade convergence. Prior work has not fully explored the resilience and consistency of MADRL in noisy, real-world agricultural scenarios, leaving a gap in integrating robust MADRL to address practical multiagent resilience challenges.

## Robustness Setting
- **Threat model / uncertainty set**: Uncertainty is introduced via a virtual "nature player/agent" that acts adversarially to all other agents by generating domain randomization parameters that modify the state transition function and reward functions. The formulation uses simple uncertainty sets without requiring prior probabilistic information; agents maximize outcomes under worst-case scenarios. Observation noise is modeled as multiplicative zero-mean Gaussian noise on the true observation vector (ō_r = o_r·(1 + N(0, σ²))), and reward uncertainty is modeled as truncated Gaussian noise on the reward controlled by a level λ.
- **Setting**: Cooperative (shared team reward) multiagent; modeled as a partially observable Markov game (POMG); centralized-training-decentralized-execution (CTDE); online learning.

## Method
- Models dynamic task allocation under uncertain UAV failures as a partially observable Markov game (POMG) ⟨R, S̄, {A_r}, {Ō_r}, {W_r}, P, U, γ⟩, where the set U of domain randomization parameters influences both transitions P and rewards W_r; states summarize observations of all active UAVs (accessible at the edge server), actions are {movement, task assignment}, and the reward is a shared team reward w_t = −(ατ′_x + βe′_x) minimizing recovery time and energy.
- Solves the game with RMADDPG under CTDE: each UAV agent has actor, target actor, critic, target critic networks and a separate replay buffer; centralized critics access all agents' observations/actions during training, while decentralized actors use only local observations at execution; target networks stabilize TD updates.
- Adds a "nature player/agent" trained simultaneously with the main agents as an adversarial environment generator: it observes the current state s and outputs a domain randomization parameter ξ for the next episode, with loss Loss_np = α_np·w̄ + β_np·MSE(o_ξ, ξ) (w̄ is average agent reward), balancing environment difficulty against parameter randomness, progressively generating harder scenarios.
- Introduces an observation noise model (multiplicative Gaussian) to simulate communication/sensor uncertainty in smart farms; complexity analysis gives space O(|R|×B) and overall training time O(KT|R|I²_max), roughly |R| times the MDQN baseline.

## Theoretical Contributions
None / mostly empirical. The paper states (citing [11]) that a Nash equilibrium exists in the POMG and writes the corresponding Bellman / NE equations, but provides no new convergence, sample-complexity, or certified-robustness proofs; contributions are primarily modeling and empirical.

## Experiments
- **Environment/Benchmark**: Simulated multi-UAV livestock-monitoring smart farm built in Python 3.8 / PyTorch 2.0 on modified Multiagent Particle Environments (MPEs); synthetic workloads with parameter configurations based on prior work; trained for 5×10⁴ episodes, 25 time steps per episode, replay buffer 10⁶, mini-batch 1024.
- **Baselines**: Decentralized DDPG; MADDPG; and a heuristic algorithm that assigns tasks to the closest UAV. (Complexity also compared against the MDQN algorithm from [7].)
- **Evaluation metrics**: Running average / accumulated reward (with 95% confidence intervals over five runs), convergence under hyperparameter sweeps (learning rate, hidden units, batch size, discount factor), average time consumption, average energy consumption, and performance under varying numbers of UAVs and tasks.

## Key Results
- Under observation noise (1%, 3%, 5%), RMADDPG achieves higher rewards with less performance degradation than DDPG and MADDPG; overall time and energy consumption can be reduced by about 28% at 3% uncertainty.
- Under reward uncertainty (3%, 6%, 9%), with no uncertainty MADDPG outperforms RMADDPG, but with uncertainty RMADDPG begins to outperform others after ~10K episodes (about 10% time/energy reduction at 6% uncertainty); at very high uncertainty (9%) RMADDPG's robustness reaches a limit.
- RMADDPG shows the lowest average time and energy consumption, especially under noise/uncertainty; performance improves with more UAVs (fixed 20 tasks) and with fewer tasks (fixed 4 UAVs).

## Limitations & Future Work
- RMADDPG's ability to cope with uncertainty has a limit: excessive uncertainty beyond a certain threshold hinders effective learning and reduces performance; in noise-free settings RMADDPG converges to a lower reward than MADDPG.
- Training cost is roughly |R| times that of single-agent MDQN.
- Future work: improving MADRL robustness; extending MaaRS to more complex agricultural tasks; integrating heterogeneous agents (e.g., ground robots with UAVs); real-world deployment validation under varying weather and communication delays; optimizing energy-efficient task allocation strategies.

## Relevance to Survey
An applied robust-MARL paper that directly adopts the "nature player" model-uncertainty paradigm from the foundational Robust MARL with Model Uncertainty work (Zhang et al., NeurIPS 2020 — its [11]) and instantiates it as RMADDPG for a real-world IoRT/UAV smart-farm task-allocation problem. It sits on the "model/environment uncertainty + adversarial nature player" main line, connects to domain-randomization-based robust MARL and to robustness against observation/communication noise, and exemplifies how the robust Markov game framework transfers to systems/resilience applications.

## Related Work (verbatim excerpts from the paper)

> _[Section II.C, Related Work — MADRL and Robustness]_

"MADRL algorithms like MADDPG consider the strategies of other agents during training to promote cooperative learning [8]. Recent studies have applied MADRL to address multiagent IoRT challenges. For instance, Seid et al. [13] proposed a MADRL-based scheme to reduce computation costs while maintaining QoS in a multi-UAV IoT edge network. A scalable MADRL algorithm for improving optimality, robustness, and sample efficiency was introduced in [25] for adaptive traffic control. Despite these advancements, ensuring the robustness of MADRL in practical applications remains a challenge, often overlooked in theoretical studies [11], [26]. Uncertainties in state transitions were considered in [17] and an attempt was made to bridge the sim-to-real gap in autonomous driving. However, the use of robust MADRL in precision agriculture, especially under real-world variability and model uncertainty, has not been fully explored, presenting an opportunity to enhance resilience and reliability in agricultural IoRT systems."

> _[Section II.B, Related Work — IoRT System Resilience]_

"Resilience is crucial for IoRT systems, especially in maintaining functionality under adverse conditions [6]. The impact of wireless network instability on IoRT resilience for disaster management was studied in [21]. Recent studies emphasize the need for robust systems to handle communication constraints, hardware failures, and adverse weather, which are frequent in agriculture and can reduce IoRT system efficiency [18], [22]. Task allocation in IoRT was explored in contexts like precision agriculture [23], [24]. Our work builds on these by introducing MaaRS, a novel model for dynamic task allocation among UAVs to handle uncertain failures. By leveraging UAV mobility, MaaRS improves system responsiveness and efficiency, reducing recovery times and energy use, which is critical for flexible and resilient smart farming."

> _[Section I, Introduction — on model uncertainty and the nature player]_

"Although MADDPG has proven effective, practical challenges persist. In reality, robots often lack full knowledge of the system model—such as the reward functions of other robots and the system transition dynamics—leading to model uncertainty [11]. Additionally, agricultural environments introduce disturbances and noise, affecting the convergence of DRL algorithms, including MADDPG. Previous research has not fully explored the resilience and consistency of MADRL in noisy, real-world agricultural scenarios. Consequently, there exists a significant gap in integrating robust MADRL algorithms to address practical multiagent resilience challenges. This article fills this gap by proposing a novel robust RMADDPG-based MaaRS approach for livestock monitoring in precision agriculture. ... Model uncertainty is simulated through a virtual player referred to as the nature player [11], which interacts with agents to introduce a layer of complexity and unpredictability into the learning process."

> _[Section IV.B, RMADDPG Algorithm — on the nature agent]_

"A key challenge is the limited accuracy of each agent's understanding of the true reward functions and transition models governing the environment, leading to a significant performance gap between simulation results and real-world applications. To address this and account for the uncertainty inherent in MADRL scenarios, a virtual agent known as the \"nature agent\" is introduced, acting adversarially to all other agents [11]. The nature agent introduces a layer of complexity and unpredictability into the learning process, simulating the real-world uncertainties that agents encounter during their interactions. We refer to the MADDPG algorithm combined with the \"nature agent\" as RMADDPG algorithm, making the system more robust to dynamic changes."

### Cited references (resolved from the paper's bibliography)
- **[6]** A. Prorok, V. Kumar, B. Sadler, G. Sukhatme. *Introduction to the special section on resilience in networked robotic systems.* IEEE Trans. Robot. 2022.
- **[8]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[11]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[13]** A. M. Seid, G. O. Boateng, B. Mareri, G. Sun, W. Jiang. *Multi-agent DRL for task offloading and resource allocation in multi-UAV enabled IoT edge network.* IEEE Trans. Netw. Service Manag. 2021.
- **[17]** E. Candela, L. Parada, L. Marques, T.-A. Georgescu, Y. Demiris, P. Angeloudis. *Transferring multi-agent reinforcement learning policies for autonomous driving using sim-to-real.* IROS 2022.
- **[18]** S. Sarker et al. *FOLD: Fog-dew infrastructure-aided optimal workload distribution for cloud robotic operations.* Internet Things 2024.
- **[21]** X. Guan et al. *ROG: A high performance and robust distributed training system for robotic IoT.* MICRO (IEEE/ACM Int. Symp. Microarchit.) 2022.
- **[22]** X. Tian, M. Afrin, S. Mistry, R. Mahmud, A. Krishna, Y. Li. *MURE: Multi-layer real-time livestock management architecture with unmanned aerial vehicles using deep reinforcement learning.* Future Gener. Comput. Syst. 2024.
- **[23]** N. Seenu, R. M. K. Chetty, M. Ramya, M. N. Janardhanan. *Review on state-of-the-art dynamic task allocation strategies for multiple-robot systems.* Ind. Robot, Int. J. Robot. Res. Appl. 2020.
- **[24]** M. Santilli, R. F. Carpio, A. Gasparri. *A framework for tasks allocation and scheduling in precision agriculture settings.* ICAR 2021.
- **[25]** T. Chu, J. Wang, L. Codecà, Z. Li. *Multi-agent deep reinforcement learning for large-scale traffic signal control.* IEEE Trans. Intell. Transp. Syst. 2020.
- **[26]** Y. Wang, S. Zou. *Online robust reinforcement learning with model uncertainty.* NeurIPS 2021.
