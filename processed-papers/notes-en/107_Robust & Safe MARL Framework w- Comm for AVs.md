# 107. Robust and Safe Multi-Agent Reinforcement Learning with Communication for Autonomous Vehicles: From Simulation to Hardware

## Metadata
- **Title**: Robust and Safe Multi-Agent Reinforcement Learning with Communication for Autonomous Vehicles: From Simulation to Hardware
- **Authors**: Keshawn Smith, Zhili Zhang, H M Sabbir Ahmad, Ehsan Sabouni, Mainak Mondal, Song Han, Wenchao Li, Fei Miao
- **Affiliation**: University of Connecticut (School of Computing; Dept. of ECE); Boston University (Dept. of ECE)
- **Venue**: Not specified (arXiv preprint arXiv:2506.00982v3 [cs.RO], 12 May 2026)
- **Link/arXiv**: arXiv:2506.00982v3

## Taxonomy
- **Robustness / perturbation type targeted**: Communication latency (delayed and asynchronous V2V message passing), state/observation perturbation, model uncertainties and state estimation errors, safety constraints (collision avoidance), sim-to-real (sim-to-hardware) gap.
- **Method paradigm**: Robust MARL (robust PPO with a worst-case Q network), delay-aware training, Control Barrier Function (CBF)-based safety shield (QP-filtered safe action enforcement), domain-randomization comparison, CTDE.
- **Keywords**: Robust MARL, communication delay, V2V, CBF safety shield, sim-to-real, connected autonomous vehicles

## TL;DR
The paper proposes RSR-RSMARL, a Real-Sim-Real robust and safe MARL framework that parameterizes delay-aware state sharing from hardware-measured V2V communication latency and couples a CBF-based safety shield with pluggable PID/MPC controllers, enabling zero-shot transfer of delay-robust, collision-free cooperative driving policies from CARLA to physical 1/10th-scale connected autonomous vehicles.

## Problem & Motivation
Deep MARL performs well in simulation for connected autonomous driving but most prior work assumes instantaneous, perfectly synchronized inter-agent communication, which limits reliable transfer to hardware where V2V communication is inherently delayed and asynchronous. Measurable latency and transmission variability are rarely incorporated into MARL training or validated on hardware. The sim-to-real gap is compounded for multi-agent CAV systems by safety criticality (unsafe actions can cause irreversible failures), state estimation errors, communication delays, and model uncertainties. The paper argues that MARL-for-CAV frameworks must incorporate safety guarantees not only during training but throughout real-world deployment, and addresses the absence of an open-source testbed that supports end-to-end development and evaluation of robust, safe MARL for CAVs.

## Robustness Setting
- **Threat model / uncertainty set**: Inter-agent communication delay (both fixed F-k delays and time-varying delays sampled over a range, e.g., [0, 5]), modeled from hardware-measured V2V latency statistics (controlled testbed 10–20 ms; production V2X 50–200 ms via stochastic sampling). Neighbor states are treated as bounded-delay / potentially stale observations; the worst-case Q network estimates expected return when action selection is affected by inaccurate or perturbed observations; CBF safety margins are conservatively inflated to account for state uncertainty.
- **Setting**: Cooperative multi-agent (connected autonomous vehicles); decentralized CTDE (centralized training with decentralized execution); online RL trained in simulation then deployed zero-shot on hardware (the CBF-QP safety filter is solved fully decentralized at the agent level).

## Method
- **Communication-aware state/action design**: Each ego agent i fuses its local observation o_i with delayed neighbor observations o_j^del (j ∈ N_i) into a delay-aware state s_i^del, applying the measured V2V latency model; discrete actions align with real actuation (emergency stop, lane keeping, lane change, discrete acceleration/braking). The MARL problem is a tuple G = (S, A, P, r, γ) with reward r = w1‖v_i‖² − w2‖c_i‖ + w3‖l_i‖ + r_i^safe, where r_i^safe penalizes safety-shield interventions.
- **Delay-aware robust MARL training**: Robust PPO agents are trained under fixed and time-varying delay models, each equipped with an extra worst-case Q network estimating return under perturbed/inaccurate observations; agents experience delayed states during training to emulate network latency.
- **CBF-based Safety Shield**: A quadratic program minimally modifies the reference control u_ref subject to a CBF constraint (forward invariance of the safe set h(x,t) ≥ 0) plus velocity/acceleration bounds, filtering unsafe commands before actuation; solved decentrally per agent using local ego states, communicated neighbor states (treated as bounded-delay), and static map obstacles, with conservatively inflated safety margins.
- **Pluggable controllers**: Safe actions are tracked by either a PID controller (lightweight) or an MPC controller with CBF/CLF constraints (smoother, foresighted, higher compute), making the shield controller-agnostic; if no safe action exists an emergency stop is triggered.

## Theoretical Contributions
None / mostly empirical. The CBF-QP provides formal forward-invariance safety guarantees of the safe set h(x,t) ≥ 0 during execution, but no convergence, sample-complexity, or equilibrium analysis for the MARL component is presented.

## Experiments
- **Environment/Benchmark**: CARLA simulator (highway scenario; CARLA 0.9.15, Python 3.10, PyTorch 2.6, CUDA 12.2) for robust training/evaluation and ablations; physical hardware testbed of 1/10th-scale F1TENTH CAVs (2D LiDAR Hokuyo UST-10LX, Intel RealSense D435i, onboard IMU; V2V over Wi-Fi at 5 Hz, latency 10–20 ms; NVIDIA Jetson Orin Nano, ROS Noetic; policy/safety at 10 Hz, control at 50 Hz) on a 3-lane miniature highway and a 2-lane circular/oval highway, each at three obstacle-density levels.
- **Baselines**: Safe-RMM (excludes delay modeling); RSR-MARL (removes the Safety Shield); No-Comm RSR-RSMARL (disables V2V); MARL-DR (domain randomization); Non-Robust RSR-MARL; comparisons of MPC vs. PID backends and fixed vs. time-varying delay.
- **Evaluation metrics**: Number of collisions, completion time, discounted episode return, CBF intervention frequency; ablations over no-delay / fixed (F-1–F-5) / time-varying (TV) latency under matched and mismatched settings (results averaged over 50 test episodes in the delay-modeling table).

## Key Results
- On both the 3-lane and 2-lane oval highway hardware tracks, both delay-aware RSR-RSMARL variants (time-varying TV and fixed-delay F-2) achieve zero collisions across all obstacle levels, with the TV model giving the lowest completion times; RSR-MARL (no Safety Shield) accumulates growing collisions and MARL-DR degrades most as obstacle density increases.
- Under communication-delay modeling (Table 2), TV training achieves zero collisions with competitive efficiency (return 139.71 MPC, 124.18 PID); fixed-delay F-5 attains the highest peak return (161.90) at near-zero collisions but is tuned to one latency regime. Removing the Safety Shield sharply increases collisions (RSR-MARL 42, Non-Robust RSR-MARL 45 at F-2), and MARL-DR / Safe-RMM show higher collisions and lower returns than RSR-RSMARL.
- V2V communication lowers the average CBF intervention rate from 18.7% (no communication) to 11.4% (with communication), and delay-trained policies remain stable even when deployment delays differ from simulation; MPC further improves trajectory smoothness and robustness at modest extra compute.

## Limitations & Future Work
- Not explicitly enumerated by the authors. Implicitly: the controlled testbed achieves only 10–20 ms latency whereas production V2X networks exhibit higher variability (50–200 ms), so real-deployment latency is approximated by stochastic sampling rather than directly measured; MPC adds computational load relative to PID; fixed-delay policies are optimized for a single stationary latency regime and are less robust than TV under jitter. No future-work section is provided in the text.

## Relevance to Survey
This paper sits on the communication-robustness and safety branches of robust MARL, intersecting with state/observation-perturbation robustness and the sim-to-real line. It combines a worst-case-aware robust RL component (worst-case Q network, related to state-adversarial MARL) with formal CBF-based safety shielding, and is one of the few works validating robust, safe, communication-aware MARL on physical multi-vehicle hardware rather than simulation alone. It connects the "communication attacks/latency robustness", "safety/shielding", and "robust RL under uncertain observations" themes, and builds directly on prior safe/robust MARL for CAVs (e.g., Safe-RMM and state-adversarial MARL).

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Deep Reinforcement Learning in Robotics"]_

"Deep Reinforcement Learning in Robotics Training RL or MARL policies in simulation ensures safety and efficiency by mitigating risks to hardware and its surroundings. While imitation learning is commonly used for policy transfer [16, 17], its reliance on real-world data often incurs significant costs. Our approach focuses on simulator-based training to reduce this dependency while maintaining robust real-world performance. Addressing the challenges of sim-to-real transfer, prior studies have introduced techniques such as domain randomization, state normalization, and noise injection to bridge the sim-to-real gap [18, 19, 20]. Building on these advancements, our proposed RSR-RSMARL framework aligns simulator and real-world environments by designing state and action spaces based on hardware capabilities, enabling efficient policy deployment for execution."

> _[Section 2, Related Work — "Multi-Agent Systems and CAV Testbeds"]_

"Multi-Agent Systems and CAV Testbeds Existing multi-agent system and CAV vehicular testbeds [9, 3, 10, 11, 21] address diverse research areas such as planning and control, computer vision, collective behavior, autonomous racing, and human-computer interaction. For instance, Blumenkamp et al. [21] introduced the Cambridge RoboMaster platform, which leverages customized DJI RoboMaster S1 robots with a tightly integrated hardware, control, and simulation stack. While effective, their approach requires a bespoke simulation environment tailored specifically to their robot platform in order to train MARL policies, limiting portability to other systems. Moreover, their framework does not incorporate explicit safety filtering during policy execution, whereas our work introduces a CBF-based Safety Shield (via QP formulations) and CBF/CLF-constrained MPC backend to enforce real-time safety guarantees. By contrast, our proposed testbed provides a fully open-source and extensible framework, supports Real-Sim-Real transfer without reliance on robot-specific simulators, and integrates robust MARL with modular safety mechanisms to ensure reliable multi-agent autonomy across diverse scenarios."

> _[Section 2, Related Work — "Safe and Robust RL and MARL"]_

"Safe and Robust RL and MARL Safety has become a critical focus in RL and MARL, with prior work exploring safety shields, barrier functions, and CBF-PID controllers [22, 23, 24, 2, 25, 8], as well as robust RL methods for uncertain observations [15, 14, 26]. However, these approaches often overlook the combined challenges of communication latency, sensing uncertainty, and explicit safety guarantees in multi-agent deployment. Our work advances this area by introducing RSR-RSMARL, a Real-Sim-Real framework that aligns simulator states and actions with hardware, incorporates V2V delays during training, and enforces safety through a CBF-based Safety Shield with pluggable PID or MPC controllers. Experiments in both CARLA and on 1/10th-scale vehicles demonstrate how this integration supports safer and more generalizable MARL-based coordination compared to existing approaches."

### Cited references (resolved from the paper's bibliography)
- **[2]** Z. Zhang, S. Han, J. Wang, F. Miao. *Spatial-temporal-aware safe multi-agent reinforcement learning of connected autonomous vehicles in challenging scenarios.* 2023 (pp. 5574–5580).
- **[3]** N. Hyldmar, Y. He, A. Prorok. *A fleet of miniature cars for experiments in cooperative driving.* IEEE ICRA 2019.
- **[8]** S. Han, S. Zhou, J. Wang, L. Pepin, C. Ding, J. Fu, F. Miao. *A multi-agent reinforcement learning approach for safe and efficient behavior planning of connected autonomous vehicles.* IEEE Transactions on Intelligent Transportation Systems 2024.
- **[9]** A. Mokhtarian, P. Scheffe, M. Kloock, S. Schäfer, H. Bang, V.-A. Le, S. Ulhas, J. Betz, S. Wilson, S. Berman, A. Prorok, B. Alrifaee. *A survey on small-scale testbeds for connected and automated vehicles and robot swarms.* 2024.
- **[10]** Y. Shao, M. A. M. Zulkefli, Z. Sun, P. Huang. *Evaluating connected and autonomous vehicles using a hardware-in-the-loop testbed and a living lab.* Transportation Research Part C: Emerging Technologies, 2019.
- **[11]** C. Tang, B. Abbatematteo, J. Hu, R. Chandra, R. Martín-Martín, P. Stone. *Deep reinforcement learning for robotics: A survey of real-world successes.* arXiv 2024.
- **[14]** S. Han, S. Su, S. He, S. Han, H. Yang, F. Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv preprint arXiv:2212.02705, 2022.
- **[15]** Y. Liang, Y. Sun, R. Zheng, F. Huang. *Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning.* NeurIPS 2022.
- **[16]** M. Torne, A. Simeonov, Z. Li, A. Chan, T. Chen, A. Gupta, P. Agrawal. *Reconciling reality through simulation: A real-to-sim-to-real approach for robust manipulation.* arXiv 2024.
- **[17]** M. T. Villasevil, A. Jain, V. Macha, J. Yuan, L. L. Ankile, A. Simeonov, P. Agrawal, A. Gupta. *Scaling robot-learning by crowdsourcing simulation environments.* (year not specified).
- **[18]** W. Zhao, J. P. Queralta, T. Westerlund. *Sim-to-real transfer in deep reinforcement learning for robotics: A survey.* IEEE SSCI 2020.
- **[19]** Y. Jiang, C. Wang, R. Zhang, J. Wu, L. Fei-Fei. *TRANSIC: Sim-to-real policy transfer by learning from online correction.* Conference on Robot Learning (CoRL) 2024.
- **[20]** S. S. Sandha, L. Garcia, B. Balaji, F. Anwar, M. Srivastava. *Sim2real transfer for deep reinforcement learning with stochastic state transition delays.* CoRL 2020 (PMLR vol. 155).
- **[21]** J. Blumenkamp, A. Shankar, M. Bettini, J. Bird, A. Prorok. *The Cambridge RoboMaster: An agile multi-robot research platform.* arXiv 2024.
- **[22]** L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, A. P. Schoellig. *Safe learning in robotics: From learning-based control to safe reinforcement learning.* Annual Review of Control, Robotics, and Autonomous Systems, 2022.
- **[23]** I. ElSayed-Aly, S. Bharadwaj, C. Amato, R. Ehlers, U. Topcu, L. Feng. *Safe multi-agent reinforcement learning via shielding.* AAMAS 2021.
- **[24]** Z. Cai, H. Cao, W. Lu, L. Zhang, H. Xiong. *Safe multi-agent reinforcement learning through decentralized multiple control barrier functions.* 2021.
- **[25]** J. Wang, S. Yang, Z. An, S. Han, Z. Zhang, R. Mangharam, M. Ma, F. Miao. *Multi-agent reinforcement learning guided by signal temporal logic specifications.* arXiv preprint arXiv:2306.06808, 2023.
- **[26]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research (TMLR), 2023.
