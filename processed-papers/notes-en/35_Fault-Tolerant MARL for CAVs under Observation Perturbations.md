# 35. Fault-Tolerant MARL for CAVs under Observation Perturbations for Highway On-Ramp Merging

## Metadata
- **Title**: Fault-Tolerant MARL for CAVs under Observation Perturbations for Highway On-Ramp Merging
- **Authors**: Yuchen Shi, Huaxin Pei, Yi Zhang, Danya Yao
- **Affiliation**: Department of Automation, Tsinghua University, Beijing, China; Beijing National Research Center for Information Science and Technology (BNRist), Tsinghua University
- **Venue**: Not specified (arXiv preprint; arXiv:2511.23193v1 [cs.RO], 28 Nov 2025)
- **Link/arXiv**: arXiv:2511.23193v1

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation (communication and perception faults causing observed data to deviate from ground truth); fault tolerance for cooperative connected and automated vehicles (CAVs)
- **Method paradigm**: Adversarial training (co-trained adversarial fault injection agent), minimax-style perturbation generation within an l∞-norm ball, fault diagnosis + observation reconstruction via temporal (GRU) network, MADDPG/DDPG actor-critic
- **Keywords**: Cooperative Driving, Multi-agent Reinforcement Learning, Fault Tolerance, Perturbed Observations, On-ramp Merging

## TL;DR
The paper proposes Observational Fault-Tolerant MARL (OFT-MARL) for cooperative on-ramp merging, combining a co-trained adversarial fault injection agent that generates the most disruptive bounded observation perturbations during training with a fault-tolerant vehicle agent that uses a GRU-based temporal discrimination network to detect faults and reconstruct credible observations, achieving near-fault-free safety and efficiency under various observation fault patterns.

## Problem & Motivation
MARL is promising for cooperative driving among CAVs, but its practical deployment is hindered by insufficient fault tolerance against observational faults arising from unavoidable communication and perception faults, which cause observed data to deviate from ground truth and mislead vehicles' decision-making, propagating disruption throughout the cooperative fleet (e.g., at the merging point). Current MARL studies for cooperative driving rarely consider the impact mechanisms of potential perception or communication faults. Addressing this presents two challenges: (1) generating perturbations that effectively stress the policy during training (random or manual fault injection mostly introduces perturbations with inappropriate magnitudes), and (2) equipping vehicles with the capability to mitigate the impact of corrupted observations under the dual uncertainty where blindly trusting faulty data may lead to unsafe decisions while excessive distrust forces overly conservative, inefficient behaviors.

## Robustness Setting
- **Threat model / uncertainty set**: A global adversarial fault injection agent adaptively perturbs a randomly selected fault-recipient vehicle's observation of a randomly selected target neighbor. Perturbation b is applied via an add function f(o_ij, b) = o_ij + clip(b, −ϵ, ϵ), constrained to lie within an l-norm (∞-norm) ball B(o) of perturbation budget ϵ. Only the relative position and velocity dimensions can be perturbed (d0 = 2; existence and lane features are unperturbable). The fault injection agent's objective maximizes policy disruption by minimizing collective rewards (r' = −Σ r_i).
- **Setting**: Cooperative (cooperative driving fleet) with an adversarial fault injection agent (offensive-defensive synergy); CTDE (centralized critics with decentralized policies, MADDPG); online RL with replay buffers. Modeled as Dec-POMDPs.

## Method
- Models the N-vehicle system as a Dec-POMDP; vehicle i observes only its own state and m surrounding vehicles (front/rear/side-front/side-rear). True observation o_i and perturbed observation ô_i are formally defined; perturbations are bounded within an ∞-norm ball.
- **Adversarial fault injection agent**: a global agent aggregates all vehicles' observations plus one-hot fault recipient (e_rec) and target (e_tgt) indicators into input x, processes x through the fault generation network ρ_ω to output perturbation magnitude b = ρ_ω(x), then applies b via the fault-affected (add + clip) function. Trained with DDPG as a single-agent adversarial policy.
- **Fault-tolerant vehicle agent**: a temporal discrimination network G_g implemented as a GRU leverages spatio-temporal correlations in vehicle data; from the hidden state it outputs a per-neighbor fault probability p̃_i = sigmoid(W_p h'_i + b_p) and a reconstructed observation estimate õ_i = W_o h'_i + b_o. The temporal network is trained via supervised learning with a composite MSE loss against ground-truth fault indicators and observations.
- **Policy**: the action network produces the acceleration action a_i = µ_θ(ô_i, p̃_i, õ_i), augmenting the (possibly corrupted) observation with the fault diagnosis and reconstruction outputs; policy parameters θ are shared across vehicles and trained via MADDPG (centralized critics Q_ψi receive ground-truth global states).
- **Joint training**: a co-evolutionary, offensive-defensive synergy between the two agents, with three network components optimized via distinct paradigms (G_g via supervised learning, {Q_ψi, µ_θ} via MADDPG, {Q_ϕ, ρ_ω} via DDPG), per Algorithm 1.

## Theoretical Contributions
None / mostly empirical. (The method defines a bounded ∞-norm-ball perturbation constraint and provides loss/policy-gradient formulations, but no convergence, sample-complexity, or equilibrium-existence proofs are given.)

## Experiments
- **Environment/Benchmark**: A highway on-ramp merging scenario modified from the Highway Environment [35], with single-lane main road and on-ramp, N = 4 vehicles, each observing m = 4 neighbors; state dimension d = 4 (existence Boolean, longitudinal position, velocity, lane ID), perturbable dimensions d0 = 2 (relative position and velocity). Increased randomness in initial velocities, strict headway, and heterogeneous acceleration characteristics.
- **Baselines / configurations**: Fault injection dimension — Fault-free (b = 0), Random fault (b ∼ U(−ϵ, ϵ)), Adversarial fault (b = ρ_ω(x)). Policy training dimension — Vanilla MADDPG (baseline without fault tolerance), OFT-MARL w/o GRU (ablation), OFT-MARL (full method); MADDPG (fault-free) reference.
- **Evaluation metrics**: Reward (episode reward), Collision Rate, Timesteps (task completion timesteps); for the temporal network: fault-detection accuracy/precision/recall (confusion matrix) and observation prediction recovery (MAE/MSE for position and velocity).

## Key Results
- Training vanilla MADDPG without faults degrades significantly under random faults: reward drops from 0.30 (fault-free) to −2.07 and collision rate rises from 11.3% to 22.9%, demonstrating the necessity of fault tolerance.
- The adversarial fault injection agent is more disruptive than random faults: against fixed policies, reward declines markedly (e.g., Vanilla MADDPG reward −1.26 → −4.91; OFT-MARL −0.14 → −5.72), confirming it strategically compromises safety or efficiency, whereas policies trained only with random faults have inadequate fault tolerance.
- When trained with adversarial faults, OFT-MARL outperforms all baselines across metrics (reward −0.38, collision rate 12.5%, timesteps 17.60), approaching MADDPG (fault-free) levels (reward 0.30, 11.3%), and generalizes across diverse fault patterns including retrained fault injection policies (Table V).
- The GRU temporal network achieves 99.3% fault-detection accuracy, 99.6% precision, 95.8% recall (over 69456 judgments / 1000 episodes), and corrects observation errors substantially: position MAE reduced from 9.10 m to 3.36 m (63.1% correction) and velocity MAE from 3.46 to 1.45 m/s (58.1% correction).

## Limitations & Future Work
- Validated only in a single simulated highway on-ramp merging scenario with N = 4 vehicles; broader applicability across diverse scenarios remains to be investigated.
- The method provides no formal/theoretical guarantees (empirical only).
- Future work: investigate applicability across diverse scenarios; integrate with safety verification modules to ensure security of vehicle policies; fuse more data credibility assessment methods (e.g., driving-habit factors) into the vehicle agent to enhance fault detection and observation prediction for heterogeneous vehicles.

## Relevance to Survey
This paper sits in the "state/observation perturbation" robustness line of robust MARL, applied to cooperative driving for CAVs. It connects the adversarial-training paradigm (a co-trained adversarial perturbation/fault-injection agent generating worst-case bounded perturbations within an l∞-norm ball, echoing SA-MDP-style state-observation robustness) with a defensive denoising/reconstruction mechanism (GRU-based fault diagnosis and observation reconstruction). It is closely related to robust RL against state-observation perturbations [33] and robust MARL with state uncertainty [34], and represents the fault-tolerance / safety subtheme for multi-agent cooperative systems.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Works — A. Cooperative Driving]_

"Traditional cooperative driving methods are typically achieved by establishing explicit optimization objectives, designing right-of-way allocation rules, and implementing trajectory planning [15], [16], [17], [18]. However, traditional methods can be limited in scalability and adaptability in highly dynamic and complex scenarios. This has motivated the adoption of MARL, which excels at learning cooperative strategies directly from interaction data.

To tackle various practical challenges in traffic, researchers have developed solutions built upon foundational frameworks. Ramp merging scenario is one of the typical scenario for algorithm verification. For instance, Chen et al. [19] incorporated a priority-based safety supervisor into MA2C to enhance safety considerations. Pan et al. [20] proposed Trust-MARL based on MASAC to control mixed traffic flows on ramps. Chen et al. [21] integrated graph neural networks with MADQN to handle dynamic vehicle numbers and rapidly expanding joint action spaces for cooperative lane change control during merging. In this work, to achieve precise velocity control, we enhance the fault tolerance of the MADDPG [22] algorithm, which is suitable for continuous action control, and validate it in ramp scenarios."

> _[Section II, Related Works — B. Fault Tolerance for Cooperative Driving]_

"Classical fault-tolerant methods for cooperative driving are typically implemented through scheduling rule design or game-theoretic optimization. Pei et al. [23] constructs a rule-based fault-tolerant cooperative driving strategy. He et al. [24] proposed a global planning and local gaming framework. Liu et al. [25] introduced a method for real-time decision adjustments, where faulty and normal vehicles can execute distinct decision models in a distributed manner. Ma et al. [26] transformed robust autonomous intersection control into a weighted maximal clique problem with restrictions and employed a heuristic algorithm to explore the solution space. Such traditional methods possess certain advantages in fault handling, for their relatively fixed and predictable decision rules. To address potential input biases in RL-based vehicle policy networks, He et al. utilized Bayesian optimization to approximate input perturbations for black-box vehicle policies [27], while applied gradient descent for white-box scenarios with known policy gradients [28]. However, most studies about robust RL-based vehicle policies focus on single-vehicle settings, with limited research on multi-vehicle interactions."

> _[Section IV-B, Observation Modeling under Faults — perturbation constraint]_

"To bound fault magnitudes, we define an l-norm ball B(o) [33], [34]. The perturbed observation f(o, b) should lie within the ball centered at o:
B(o) := { f(o, b) ∈ Rd : ∥f(o, b) − o∥l ≤ ϵ },
where ϵ > 0 is the perturbation budget. This constraint ensures the problem remains well-posed, as excessive perturbations provide limited practical utility for policy decisions and are readily detectable in real-world scenarios."

### Cited references (resolved from the paper's bibliography)
- **[15]** H. Pei, S. Feng, Y. Zhang, D. Yao. *A cooperative driving strategy for merging at on-ramps based on dynamic programming.* IEEE Transactions on Vehicular Technology, 2019.
- **[16]** K. Long, Z. Gao, Z. Jiang, C. Ma, J. Hu, X. Yang. *Optimization based trajectory planner for multilane roundabouts with connected automation.* Journal of Intelligent Transportation Systems, 2023.
- **[17]** M. Zhang, C. Wang, W. Zhao, J. Liu, Z. Zhang. *A multi-vehicle self-organized cooperative control strategy for platoon formation in connected environment.* IEEE Transactions on Intelligent Transportation Systems, 2025.
- **[18]** Q. Wang, D. Tian, X. Duan, G. Qi, J. Zhou, D. Zhao. *Efficient and energy-saving cooperative motion planning for multiple connected and autonomous vehicles at unsignalized intersections.* IEEE Transactions on Intelligent Transportation Systems, 2025.
- **[19]** D. Chen, M. R. Hajidavalloo, Z. Li, K. Chen, Y. Wang, L. Jiang, Y. Wang. *Deep multi-agent reinforcement learning for highway on-ramp merging in mixed traffic.* IEEE Transactions on Intelligent Transportation Systems, 2023.
- **[20]** J. Pan, T. Wang, C. Claudel, J. Shi. *Trust-MARL: Trust-based multi-agent reinforcement learning framework for cooperative on-ramp merging control in heterogeneous traffic flow.* arXiv preprint arXiv:2506.12600, 2025.
- **[21]** S. Chen, J. Dong, P. Ha, Y. Li, S. Labi. *Graph neural network and reinforcement learning for multi-agent cooperative control of connected autonomous vehicles.* Computer-Aided Civil and Infrastructure Engineering, 2021.
- **[22]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS (NIPS'17), 2017.
- **[23]** H. Pei, J. Zhang, Y. Zhang, X. Pei, S. Feng, L. Li. *Fault-tolerant cooperative driving at signal-free intersections.* IEEE Transactions on Intelligent Vehicles, 2023.
- **[24]** Z. He, J. Zhang, H. Pei, L. Feng, D. Yao. *Communication fault-tolerant cooperative driving at on-ramps: A global planning and local gaming strategy.* IEEE Intelligent Vehicles Symposium (IV), 2024.
- **[25]** Q. Liu, J. Zhang, W. Zhong, Z. Li, X. J. Ban, S. Li, L. Li. *Fault-tolerant cooperative driving at highway on-ramps considering communication failure.* Transportation Research Part C: Emerging Technologies, 2023.
- **[26]** M. Ma, Z. Li. *A time-independent trajectory optimization approach for connected and autonomous vehicles under reservation-based intersection control.* Transportation Research Interdisciplinary Perspectives, 2021.
- **[27]** X. He, H. Yang, Z. Hu, C. Lv. *Robust lane change decision making for autonomous vehicles: An observation adversarial reinforcement learning approach.* IEEE Transactions on Intelligent Vehicles, 2023.
- **[28]** X. He, B. Lou, H. Yang, C. Lv. *Robust decision making for autonomous vehicles at highway on-ramps: A constrained adversarial reinforcement learning approach.* IEEE Transactions on Intelligent Transportation Systems, 2023.
- **[33]** H. Zhang, H. Chen, C. Xiao, B. Li, M. Liu, D. Boning, C.-J. Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[34]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research (TMLR), 2023.
