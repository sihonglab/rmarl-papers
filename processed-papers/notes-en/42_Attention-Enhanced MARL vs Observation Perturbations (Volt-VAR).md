# 42. Attention-Enhanced Multi-Agent Reinforcement Learning Against Observation Perturbations for Distributed Volt-VAR Control

## Metadata
- **Title**: Attention-Enhanced Multi-Agent Reinforcement Learning Against Observation Perturbations for Distributed Volt-VAR Control
- **Authors**: Xu Yang, Haotian Liu, Wenchuan Wu
- **Affiliation**: State Key Laboratory of Power Systems, Department of Electrical Engineering, Tsinghua University, Beijing, China
- **Venue**: IEEE Transactions on Smart Grid, Vol. 15, No. 6, November 2024
- **Link/arXiv**: https://doi.org/10.1109/TSG.2024.3423700 (DOI 10.1109/TSG.2024.3423700)

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation (measurement noise, communication errors, and cyber-attacks on the agents' observations) in distributed Volt-VAR control
- **Method paradigm**: CTDE multi-agent RL with value network factorization, agent-level (multi-head) attention mix network, robust regularizer (KL-divergence smoothing of the policy under bounded observation perturbations), soft actor-critic
- **Keywords**: Voltage control, cloud-edge collaboration, CTDE, multi-agent reinforcement learning, attention mechanism, robust regularizer

## TL;DR
The paper proposes RASAC, a CTDE multi-agent soft-actor-critic method for distributed Volt-VAR control that combines an agent-level attention mix network (for scalable coordination via value factorization) with a novel KL-divergence robust regularizer that hardens decentralized policies against bounded observation perturbations without the cost of adversarial training.

## Problem & Motivation
Distributed Volt-VAR control (VVC) in active distribution networks (ADNs) increasingly relies on CTDE-based multi-agent RL to offload computation from edge inverters to the cloud, but performance hinges on two fragile elements: the agents' coordination mechanism and the accuracy of their observations. Existing "central value network" approaches suffer from the curse of dimensionality, while existing value-factorization mix networks (VDN, QMIX, an MLP-based FMASAC) are too simple or unstructured to coordinate large numbers of agents. Moreover, real-world ADN observations are subject to measurement noise, communication errors, and cyber-attacks; because RL policy networks are sensitive to input, even small perturbations can produce severely distorted control actions, yet existing distributed-VVC MARL methods do not consider such perturbations, hindering real-world deployment.

## Robustness Setting
- **Threat model / uncertainty set**: The true observation of agent In is on, but the received observation may be any õn in the neighborhood B(on, ϵ) bounded by ‖õn − on‖∞ ≤ ϵ (ϵ rescaled by each observation element's standard deviation). Perturbations include measurement noise, communication errors, and deliberate cyber-attacks. In the cyber-attack scenario, the attacker is assumed to have leaked policy networks and uses SGLD to craft worst-case perturbations within the ϵ-ball to maximize action distortion (overvoltage or undervoltage).
- **Setting**: Cooperative (cooperative Markov game with a shared global reward); CTDE (centralized training on the cloud, decentralized execution on edge PV inverters); online (replay-buffer-based off-policy training).

## Method
- Formulate distributed VVC as a cooperative Markov game where each PV inverter is an RL agent; under CTDE, maintain only local value networks and a mix network on the cloud (value network factorization) to avoid the curse of dimensionality.
- Replace the simple VDN/QMIX/MLP mix network with an attention-enhanced mix network: each agent's local value Qφn(on, an) is a value vector, the embedded global state s is the query vector, and the embedded local features (local observation on plus one-hot agent id) form the key vector; multi-head attention computes per-agent importance χⁿₕ via a scaled softmax, aggregates value vectors per head (Qh), then combines heads with state-dependent positive weights wh(s) and bias b(s) (ELU-activated, QMIX-style) to approximate the global return fϕ.
- Add a robust regularizer to the policy loss: Rθn(on, ϵ) = max over õ∈B(on,ϵ) of DKL(πθn(on) ‖ πθn(õn)), the maximum KL divergence between the nominal and perturbed (stochastic Gaussian) action distributions; the policy loss becomes the SAC objective plus δ·Σn Rθn(on,t, ϵ), constructing a game between the agent and the observation perturbation that automatically embeds robustness with only ϵ and δ to tune.
- Solve the inner max (a high-dimensional non-convex problem over õn) approximately with Stochastic Gradient Langevin Dynamics (SGLD): initialize õn near on, iterate K steps of noisy gradient ascent on the KL term, clipping back into B(on, ϵ).
- Train end-to-end (Algorithm 1 RASAC) with target networks for the mix and local value networks; at execution only the local policy networks run on edge inverters (millisecond-level forward pass).

## Theoretical Contributions
None / mostly empirical. The work is methodological/empirical; it adapts a KL-smoothing robustness argument (citing that minimizing the distance between πθn(on) and πθn(õn) suffices to improve robustness) but provides no formal convergence, equilibrium, or certified-radius guarantees.

## Experiments
- **Environment/Benchmark**: IEEE 33-bus and 141-bus distribution networks; 33-bus partitioned into 4 regions with 6 PVs, 141-bus into 9 regions with 22 PVs. Load and PV profiles from 3-year Portuguese electricity load data and Elia group PV generation data; 3-minute control period, episodes of 240 timesteps (half a day); voltage limits [0.95, 1.05] p.u., Vref = 1.0 p.u.; 3 random seeds.
- **Baselines**: QMIXSAC, VDNSAC (QMIX/VDN combined with SAC), FMASAC (authors' previous MLP-mix-network method), ASAC (attention-enhanced SAC without the robust regularizer — ablation), and CSAC (centralized single-agent SAC); also a "No Control" reference.
- **Evaluation metrics**: Centralized training reward curves; execution-stage voltage deviation and network loss over 36 typical days (17,280 timesteps); total rewards under increasing observation noise (ϵ′ from 0.0 to 2.5, 30 test episodes each); control actions and voltage profiles under two types of cyber-attacks; online per-agent per-step computational time.

## Key Results
- RASAC achieves the highest final training reward and stable convergence on both systems; on the larger 141-bus system VDNSAC fails to coordinate and is unstable, QMIXSAC's reward does not grow, and FMASAC degrades, whereas RASAC maintains steady convergence — demonstrating the agent-level attention mechanism's scalability.
- The robust regularizer is "free" under nominal conditions: RASAC and ASAC have almost identical VVC performance without perturbations, so robustness does not sacrifice normal performance.
- Under noise on the 33-bus system, ASAC's total reward drops by almost 75% at ϵ′ = 2.5 while RASAC keeps similar rewards; under crafted cyber-attacks on the 141-bus system, ASAC's actions are heavily distorted (voltage driven to ~0.85 p.u. in the undervoltage attack) whereas RASAC's actions stay much less distorted and voltages remain mostly within the safe range.
- RASAC matches the centralized CSAC's performance using only local measurements, and online execution takes only milliseconds per agent per step — well within the minute-level VVC requirement.

## Limitations & Future Work
- The robust regularizer requires tuning ϵ and δ, and the inner maximization is solved only approximately via a K-step SGLD heuristic (no global-optimum guarantee).
- The approach mitigates but does not fully eliminate action distortion under severe attacks (some voltages can still leave the safe range), and it provides no formal robustness certificate.
- Future work: a new RL method to detect cyber-attacks is identified as an interesting research direction.

## Relevance to Survey
This paper sits on the "state/observation-perturbation robustness" line of robust MARL, applied to a cooperative power-systems control domain. It connects the SA-MDP / observation-attack robustness literature (Zhang et al. 2020 robust DRL against adversarial state perturbations; smooth-policy regularization) to cooperative CTDE MARL, and contrasts with adversarial-training paradigms (Pinto et al. robust adversarial RL) by adopting a lightweight regularization alternative. It also illustrates the value-factorization + attention coordination theme and the practical communication/cyber-attack robustness theme relevant to a robust MARL survey.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"In the CTDE framework, the cloud platform carries out the centralized training process, which shoulders the majority of the computation burden. The edge controllers, on the other hand, execute the trained policies with local measurements. After centralized training, the only computation burden for inverters in execution stage is the forward propagation of the local policy networks, which is fast enough to realize real-time VVC. Several multi-agent RL methods for distributed VVC have been investigated under this framework, such as multi-agent deep deterministic policy gradient (MADDPG) [9], [10], [11], [12], multi-agent soft actor-critic (MASAC) [13], [14], [15], and multi-agent twin delayed deep deterministic policy gradient (MATD3) [16]."

> _[Introduction]_

"The above CTDE based multi-agent RL methods have one thing in common: they all maintain a "central value network" on the cloud platform to approximate the global reward of the system, whose input concatenates observations and actions of all RL agents to optimize policies and achieve coordination. But the curse of dimensionality and training burden caused by the "central value network" limit their performance on large-scale distribution systems. Unlike the aforementioned approaches, value network factorization, exemplified by VDN [17] and QMIX [18] only maintains a relatively small-scale mix network on the cloud platform, reducing training difficulty and burden. These methods have also been applied in distributed VVC recently [19]. However, the critical mix network in existing works is relatively simple, whose performance may not be assured as the number of edge controllers increases. Therefore, a more effective mix network structure is needed for large-scale multi-agent systems."

> _[Introduction]_

"This paper is inspired by the success of attention mechanism in the field of natural language processing. Attention mechanism aggregates scattered information based on the calculated attention distribution, which has a strong ability to extract the most important information for learning. Some pioneering works also combine attention mechanism and RL to address dispatch problems in power systems. For example, researchers in [20], [21], [22] utilize attention mechanism to process global information so that the most relevant information is fed into the RL agents for better training. And researchers in [23], [24] leverage graph attention networks to explicitly embed the topology and features of distribution networks or transportation networks so that RL agents can better perceive the system states. As can be seen, most of the existing works use attention mechanism to extract significant information. But attention mechanism is rarely used to achieve coordination under the scheme of value network factorization, which is one of the innovations of this paper."

> _[Introduction]_

"On the other hand, since RL is data-driven, the performance of multi-agent RL methods for distributed VVC relies heavily on the observations' accuracy. Due to the sensitivity of the policy networks in RL agents, once there exists a small perturbation in the observations, the generated control actions can be very distorted. In reality, perturbations in observations, such as measurement noises, communication errors, and even cyber-attacks are unavoidable in the edge controllers. The existing multi-agent RL methods for distributed VVC lack consideration of these perturbations, which hinders their application to real-world ADNs."

> _[Section III-C, Robust Regularizer]_

"In order to tackle the above problem, we consider robust reinforcement learning [30] whose objective is to maintain the performance of RL agents under adversarial perturbations. In order to improve the RL agents' robustness, traditional robust reinforcement learning methods usually concurrently train an adversarial agent. During training, the adversarial agent attacks the observation of RL agents to make their performance deteriorate. Then the RL agents' robustness is gained through the adversarial training process. However, this adversarial training requires massive computation and exhaustive tuning, and may result in an unstable training performance [31]. Instead of burdensome adversarial training, recent studies show that minimizing the distance between πθn(on) and πθn(õn) during training is enough to improve the robustness of the policy network [32], [33]. Based on this idea, we propose a novel robust regularizer to be added into the loss function of the policy networks, so that policy networks can minimize the distance between πθn(on) and πθn(õn) while maximizing the reward."

### Cited references (resolved from the paper's bibliography)
- **[9]** S. Wang et al. *A data-driven multi-agent autonomous voltage control framework using deep reinforcement learning.* IEEE Trans. Power Syst. 2020.
- **[10]** X. Sun, J. Qiu. *Two-stage volt/var control in active distribution networks with multi-agent deep reinforcement learning method.* IEEE Trans. Smart Grid 2021.
- **[11]** H. Liu, C. Zhang, Q. Chai, K. Meng, Q. Guo, Z. Y. Dong. *Robust regional coordination of inverter-based volt/var control via multi-agent deep reinforcement learning.* IEEE Trans. Smart Grid 2021.
- **[12]** D. Cao, W. Hu, J. Zhao, Q. Huang, Z. Chen, F. Blaabjerg. *A multi-agent deep reinforcement learning based voltage regulation using coordinated PV inverters.* IEEE Trans. Power Syst. 2020.
- **[13]** H. Liu, W. Wu. *Online multi-agent reinforcement learning for decentralized inverter-based volt-VAR control.* IEEE Trans. Smart Grid 2021.
- **[14]** D. Cao et al. *Data-driven multi-agent deep reinforcement learning for distribution system decentralized voltage control with high penetration of PVs.* IEEE Trans. Smart Grid 2021.
- **[15]** D. Cao et al. *Deep reinforcement learning enabled physical-model-free two-timescale voltage control method for active distribution systems.* IEEE Trans. Smart Grid 2022.
- **[16]** P. Chen, S. Liu, X. Wang, I. Kamwa. *Physics-shielded multi-agent deep reinforcement learning for safe active voltage control with photovoltaic/battery energy storage systems.* IEEE Trans. Smart Grid 2023.
- **[17]** P. Sunehag et al. *Value-decomposition networks for cooperative multi-agent learning.* arXiv:1706.05296, 2017.
- **[18]** T. Rashid, M. Samvelyan, C. Schroeder, G. Farquhar, J. Foerster, S. Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[19]** H. Liu, W. Wu. *Federated reinforcement learning for decentralized voltage control in distribution networks.* IEEE Trans. Smart Grid 2022.
- **[20]** D. Cao, J. Zhao, W. Hu, F. Ding, Q. Huang, Z. Chen. *Attention enabled multi-agent DRL for decentralized volt-VAR control of active distribution system using PV inverters and SVCs.* IEEE Trans. Sustain. Energy 2021.
- **[21]** L. Yu et al. *Multi-agent deep reinforcement learning for HVAC control in commercial buildings.* IEEE Trans. Smart Grid 2021.
- **[22]** D. Hu, Z. Ye, Y. Gao, Z. Ye, Y. Peng, N. Yu. *Multi-agent deep reinforcement learning for voltage control with coordinated active and reactive power optimization.* IEEE Trans. Smart Grid 2022.
- **[23]** D. Cao et al. *Physics-informed graphical representation-enabled deep reinforcement learning for robust distribution system voltage control.* IEEE Trans. Smart Grid 2024.
- **[24]** Q. Xing, Y. Xu, Z. Chen. *A bilevel graph reinforcement learning method for electric vehicle fleet charging guidance.* IEEE Trans. Smart Grid 2023.
- **[30]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[31]** H. Liu, W. Wu. *Two-stage deep reinforcement learning for inverter-based volt-VAR control in active distribution networks.* IEEE Trans. Smart Grid 2021.
- **[32]** H. Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[33]** Q. Shen, Y. Li, H. Jiang, Z. Wang, T. Zhao. *Deep reinforcement learning with robust and smooth policy.* ICML 2020.
