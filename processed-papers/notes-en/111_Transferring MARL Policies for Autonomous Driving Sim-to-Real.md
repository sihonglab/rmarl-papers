# 111. Transferring Multi-Agent Reinforcement Learning Policies for Autonomous Driving using Sim-to-Real

## Metadata
- **Title**: Transferring Multi-Agent Reinforcement Learning Policies for Autonomous Driving using Sim-to-Real
- **Authors**: Eduardo Candela, Leandro Parada, Luis Marques, Tiberiu-Andrei Georgescu, Yiannis Demiris, Panagiotis Angeloudis
- **Affiliation**: Centre for Transport Studies, Department of Civil and Environmental Engineering, Imperial College London, UK; Personal Robotics Laboratory, Department of Electrical and Electronic Engineering, Imperial College London, UK
- **Venue**: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2022
- **Link/arXiv**: DOI: 10.1109/IROS47612.2022.9981319

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty and the sim-to-real (reality) gap in multi-agent autonomous driving (dynamics/model mismatch, asynchronous agent stepping, measurement noise, hardware variability between robots)
- **Method paradigm**: Domain randomization during MARL training; CTDE on-policy actor-critic (MAPPO); empirical sim-to-real transfer
- **Keywords**: Sim-to-Real, domain randomization, MARL, MAPPO, autonomous driving, reality gap, Duckietown

## TL;DR
The paper proposes transferring multi-agent autonomous driving policies trained in a Duckietown-imitating simulator (Duckie-MAAD) to a real Duckiebot fleet by training with MAPPO under different levels of domain randomization, showing that domain randomization can reduce the reality gap by ~90% and outperform a rule-based benchmark.

## Problem & Motivation
Coordinating autonomous vehicles (AVs) in traffic is a hard problem; rule-based policies cannot cover all real-world scenarios, require manual rule crafting, and cannot achieve effective agent-agent coordination. MARL is a powerful, scalable framework for AV control but cannot be trained on live systems due to safety concerns and the need for millions of training steps, so it must be trained in simulation and transferred. However, simulation-trained policies overfit to simulator characteristics and suffer from the reality gap. This gap is even larger for multi-agent systems, which add complexities such as agent collaboration, environment synchronization, and limited agent perception. Little work has addressed bridging the sim-to-real gap in multi-AV systems, and to the authors' knowledge this is the first study using MARL and domain randomization for training real-life AV controllers.

## Robustness Setting
- **Threat model / uncertainty set**: The reality gap is treated as model/environment uncertainty arising from (1) a dynamical model based on assumptions (symmetric mass distribution, steady-state motors), (2) sequential simulated stepping vs. asynchronous real stepping, (3) inaccuracies in the OptiTrack positioning system, and (4) hardware variability between physically identical Duckiebots. Domain randomization injects this uncertainty by randomizing Inverse Kinematics parameters (steering factor, motor constant K, gain, trim) and steering error during training, sampled from Normal or Uniform distributions at none/medium/high levels.
- **Setting**: Cooperative/mixed multi-agent autonomous driving; CTDE (centralized critic, decentralized actors via MAPPO); online training in simulation, then transfer/evaluation in the real world.

## Method
- Model the multi-agent driving problem as a Decentralized Partially Observable MDP (Dec-POMDP) defined by ⟨N, S, Ai, T, R, Ωi, O⟩, aiming to find the joint optimal policy that maximizes expected return.
- Train cooperative multi-agent policies with MAPPO (an on-policy CTDE extension of PPO using RNNs for actor and critic); all agents share both networks for simplicity.
- Build Duckie-MAAD, a new multi-agent gym environment extending Gym-Duckietown, where Duckiebots follow waypoint-defined lane paths and take discrete high-level actions (accelerate, brake, change lane, keep velocity). A Path Following logic computes target waypoints and required linear/angular velocities, which differential-drive Inverse Kinematics converts to wheel velocities; poses are updated either by a Nonlinear Dynamics model (simulation) or by the OptiTrack MoCap system (reality).
- Apply domain randomization at training time to the Inverse Kinematics parameters that showed the most variance across physical cars (steering factor, K, gain, trim) plus steering error, training a model that can adapt to the real environment viewed as a sample of the randomized environment space.
- Reward function: v − 5c − 5t − 0.5l, where v is measured velocity and c (collision), t (off-track), l (lane change) are binary penalties.

## Theoretical Contributions
None / mostly empirical.

## Experiments
- **Environment/Benchmark**: Duckie-MAAD simulated environment and the real Duckietown testbed (Duckiebot fleet with NaturalPoint OptiTrack MoCap, 8 PrimeX13 cameras at 120 Hz); case study with 3 moving agents and 3 randomly spawned parked cars as obstacles on a test track; 10 Hz control frame rate; 30 runs in simulation and 30 in real life per policy, 400 steps per run.
- **Baselines**: Rule-based benchmark — Gipps' lane changing model with safe following distances set per the RSS model; three MAPPO-trained policies with no / medium / high domain randomization.
- **Evaluation metrics**: Average reward (over scenarios and cars) in simulation and reality; reality gap measured as the difference between reward of the no-domain-randomization policy in simulation vs. its reward in real life; component metrics — measured speed, number of times leaving the track, number of collisions, number of lane changes.

## Key Results
- The policy with medium domain randomization bridges the reality gap the best, reducing it by almost 90%.
- All MARL policies clearly outperform the rule-based baseline in both simulation and real life; the rule-based policy performed worst because it cannot adapt to agents not precisely following lanes.
- Adding domain randomization slightly decreases simulated performance but improves real-life rewards; the no-D.R. policy was best in simulation but worst in real life among MARL policies.
- High domain randomization yields an overly conservative policy (slowest speed, fewest track exits), while domain-randomization policies change lanes more often in reality (to avoid crashes) and have lower collisions; the medium-D.R. policy achieves the fewest collisions in real life.

## Limitations & Future Work
- Domain randomization shows diminishing returns (the high-D.R. policy becomes overly conservative) and cannot fully close the reality gap without increasing simulator fidelity.
- The amount of domain randomization is case-specific; a theory for selecting domain randomization remains an open question.
- The quantification and description of reality gaps is identified as an opportunity for future research.

## Relevance to Survey
This paper sits on the "environment/model uncertainty and sim-to-real gap" line of the robust MARL landscape, approaching robustness empirically via domain randomization rather than formal worst-case/adversarial optimization. It connects robust MARL to real-world multi-agent autonomous driving deployment, explicitly citing robust MARL work (Zhang et al.'s "Robust multi-agent reinforcement learning with model uncertainty") and the multi-agent reality-gap taxonomy (control architecture, observation, and communication gaps), making it a useful bridge between the theory-oriented robust MARL literature and physical multi-agent transfer.

## Related Work (verbatim excerpts from the paper)

> _[Introduction]_

"Several approaches have been proposed for bridging the reality gap in single-agent tasks, particularly in robotic manipulation [5], [6]. Among others, the methods include System Identification [7], Domain Randomisation [8] and Domain Adaptation [9]. Despite the increasing efforts in this direction, bridging the reality gap in single-agent applications remains to be a challenging task."

"The reality gap can become even larger for multi-agent systems, such as those involving AVs. These systems introduce additional complexities to the Sim-to-Real problem, such as agent collaboration, environment synchronization and limited agent perception. Little work has been done on bridging the gap between simulation and reality in multi-AV systems. Attempts have been made to make MARL more robust to uncertainty [10], [11], although these methods have not been tested in the real world."

> _[Section II, Related Work — A. Multi-Agent Learning for Autonomous Vehicles]_

"A taxonomy for multi-agent learning in Autonomous Driving was presented in [3], consisting of five levels. The first level M0 represents rule-based planning with no learning, and the last level M5 represents agents with a high degree of forward-planning, working to optimize the Price of Anarchy of the overall traffic scenario [13], [14]. Most multi-agent learning paradigms find it difficult to reach level M5, as most traffic scenarios are massive multi-agent games. Fortunately, a significant amount of algorithms fit either in M3, allowing agents to behave and expect in return partially cooperative behavior [15], and M4, where a local Nash equilibrium is achieved through the grouping of agents [16]."

"A few studies have addressed multi-AV problems using MARL. [3] proposed an open-source MARL simulation platform, that includes several traffic scenarios with the possibility of choosing different AV controllers, environment configurations and MARL algorithms. Similarly, [2] presented MACAD-gym, an Autonomous Driving multi-agent platform based on the CARLA [17] simulator. [18] modeled the multi-agent problem as a graph and used Graph Neural Networks in combination with Deep Q Network to control lane-changing decisions in environments with multiple Connected Autonomous Vehicles (CAVs)."

> _[Section II, Related Work — B. Sim-to-Real]_

"To bridge the gap between simulation and reality, known as reality gap, various domain-adaptation approaches have been developed [5]. To this date, the area with the highest amount of contributions in Sim-to-real is robotic manipulation. The methods that have been used include imitation learning, data augmentation and real world reinforcement learning. The latter case is the most difficult one to replicate due to lack of resources, safety concerns and difficulty in resetting training runs. There are simple ways of automating the reset in real world robotic manipulation [6], or to continue training efficiently without resetting [19], [20]. However, in the case of AVs, human interference is needed in order to reset the environment or to prevent catastrophic events. Therefore, most of the techniques used in robotic manipulation cannot be adapted to environments with AVs."

"For AV scenarios, [21] proposed ModEL, a modular infrastructure which considered perception, planning and control, each being trained using reinforcement learning. They used vision as the agent's main sensorial perception, and the CARLA simulator [17] during training for data augmentation and domain generalization, in order to improve overall agent robustness."

"Furthermore, in the case of multi-agent systems, there are more reality gaps compared to single-agent settings. Three significant gaps have been reported in [10]: the control architecture gap, which relates to the tendency of simulators to synchronize the actions of all agents at each time step; the observation gap, which relates to the limited perception of agents in scaled-out environments; and the communication gap which, similar to the previous one, relates to the highly limited and inconsistent communication which in multi-agent systems. Given traditional methods of software simulation, the aforementioned gaps are non-trivial to overcome, even with a redesign of the simulation itself. The study suggests that more robust modeling of the interaction between agents would be more beneficial. [10] proposed a method called Agent Decentralized Organization (ADO), which encourages agents to share a board of information provided at certain time frames, without the necessity for the information to be complete or up to date."

"Although research in Sim-to-Real for AV learning is extensive, the main focus of the literature is generalizability over diverse environments, not different actors. This can make progress in the literature slower, since the hardware is usually significantly different and not open source. Thankfully, there are attempts to standardize the research hardware, with open source sets like Duckietown [12] and DeepRacer [22], which ensure that more prior research becomes easier to reproduce consistently. However, no study has focused on transferring multi-agent policies for autonomous driving to the real world."

### Cited references (resolved from the paper's bibliography)
- **[2]** P. Palanisamy. *Multi-agent connected autonomous driving using deep reinforcement learning.* IJCNN 2020.
- **[3]** M. Zhou, J. Luo, J. Villella, Y. Yang, D. Rusu, J. Miao, W. Zhang, M. Alban, I. Fadakar, Z. Chen et al. *SMARTS: Scalable multi-agent reinforcement learning training school for autonomous driving.* arXiv preprint arXiv:2010.09776, 2020.
- **[5]** W. Zhao, J. P. Queralta, T. Westerlund. *Sim-to-real transfer in deep reinforcement learning for robotics: a survey.* IEEE SSCI 2020.
- **[6]** B. Eysenbach, S. Gu, J. Ibarz, S. Levine. *Leave no trace: Learning to reset for safe and autonomous reinforcement learning.* arXiv preprint arXiv:1711.06782, 2017.
- **[7]** M. Kaspar, J. D. M. Osorio, J. Bock. *Sim2Real Transfer for Reinforcement Learning without Dynamics Randomization.* arXiv:2002.11635, 2020.
- **[8]** J. Matas, S. James, A. J. Davison. *Sim-to-Real Reinforcement Learning for Deformable Object Manipulation.* arXiv:1806.07851, 2018.
- **[9]** H. F. Bassani, R. A. Delgado, J. N. d. O. L. Junior, H. R. Medeiros, P. H. M. Braga, A. Tapp. *Learning to Play Soccer by Reinforcement and Applying Sim-to-Real to Compete in the Real World.* arXiv:2003.11102, 2020.
- **[10]** Y.-H. Suh, S.-P. Woo, H. Kim, D.-H. Park. *A sim2real framework enabling decentralized agents to execute maddpg tasks.* Proceedings of the Workshop on Distributed Infrastructures for Deep Learning, 2019.
- **[11]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[12]** L. Paull, J. Tani, H. Ahn, J. Alonso-Mora, L. Carlone, M. Cap, Y. F. Chen, C. Choi, J. Dusek, Y. Fang et al. *Duckietown: an open, inexpensive and flexible platform for autonomy education and research.* IEEE ICRA 2017.
- **[13]** E. Koutsoupias, C. Papadimitriou. *Worst-case equilibria.* Annual Symposium on Theoretical Aspects of Computer Science (Springer) 1999.
- **[14]** T. Roughgarden. *Selfish routing and the price of anarchy.* MIT Press 2005.
- **[15]** R. E. Wang, M. Everett, J. P. How. *R-MADDPG for partially observable environments and limited communication.* arXiv preprint arXiv:2002.06684, 2020.
- **[16]** H. Zhang, W. Chen, Z. Huang, M. Li, Y. Yang, W. Zhang, J. Wang. *Bi-level actor-critic for multi-agent coordination.* AAAI 2020.
- **[17]** A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, V. Koltun. *CARLA: An open urban driving simulator.* Conference on Robot Learning (PMLR) 2017.
- **[18]** S. Chen, J. Dong, P. Ha, Y. Li, S. Labi. *Graph neural network and reinforcement learning for multi-agent cooperative control of connected autonomous vehicles.* Computer-Aided Civil and Infrastructure Engineering, 2021.
- **[19]** H. Zhu, J. Yu, A. Gupta, D. Shah, K. Hartikainen, A. Singh, V. Kumar, S. Levine. *The ingredients of real-world robotic reinforcement learning.* arXiv preprint arXiv:2004.12570, 2020.
- **[20]** A. Gupta, J. Yu, T. Z. Zhao, V. Kumar, A. Rovinsky, K. Xu, T. Devlin, S. Levine. *Reset-free reinforcement learning via multi-task learning: Learning dexterous manipulation behaviors without human intervention.* IEEE ICRA 2021.
- **[21]** G. Wang, H. Niu, D. Zhu, J. Hu, X. Zhan, G. Zhou. *ModEL: A modularized end-to-end reinforcement learning framework for autonomous driving.* arXiv preprint arXiv:2110.11573, 2021.
- **[22]** B. Balaji, S. Mallya, S. Genc, S. Gupta, L. Dirac, V. Khare, G. Roy, T. Sun, Y. Tao, B. Townsend et al. *DeepRacer: Educational autonomous racing platform for experimentation with sim2real reinforcement learning.* arXiv preprint arXiv:1911.01562, 2019.
