# 136. Robust Multi-Agent Coverage Path Planning for Unmanned Aerial Vehicles (UAVs) in Complex 3D Environments with Deep Reinforcement Learning

## Metadata
- **Title**: Robust Multi-Agent Coverage Path Planning for Unmanned Aerial Vehicles (UAVs) in Complex 3D Environments with Deep Reinforcement Learning
- **Authors**: Julian Bialas, Mario Doeller, Robert Kathrein
- **Affiliation**: FH Kufstein Tirol – University of Applied Sciences, Kufstein, Austria; University of Passau, Germany; Josef Ressel Center for multimedia analysis in the mobility domain (Vision2Move)
- **Venue**: 2023 IEEE International Conference on Robotics and Biomimetics (ROBIO) 2023
- **Link/arXiv**: DOI: 10.1109/ROBIO58561.2023.10354596

## Taxonomy
- **Robustness / perturbation type targeted**: Agent failure / fault tolerance (an agent unexpectedly terminates or collides mid-mission) and dynamic environment changes (changes in the target area mid-flight); generalization over all system parameters. Note: "robustness" here is empirical/qualitative (low variance, reacting to in-flight disruptions), not a formal robust-MDP / adversarial / minimax setting.
- **Method paradigm**: Model-free deep reinforcement learning (Proximal Policy Optimization, PPO) under a Dec-POMDP formulation; centralized training with decentralized execution (CTDE); actor-critic with convolutional networks
- **Keywords**: Multi-agent coverage path planning (MACPP), UAVs, PPO, Dec-POMDP, deep reinforcement learning, 3D environments

## TL;DR
The paper proposes a PPO-based multi-agent coverage path planning (MACPP) framework for UAVs that operates in complex dynamic 3D environments, generalizes over all system parameters (target zones, agent positions, battery levels), runs in real time on hardware, and demonstrates robustness by allowing the remaining agents to dynamically re-cover the area of an agent that fails mid-flight.

## Problem & Motivation
Multi-agent coverage path planning (MACPP) with UAVs is essential for environmental monitoring, surveillance, and search-and-rescue, but existing approaches have limitations: genetic-algorithm and linear-optimization methods perform well offline but have long computation times and cannot adapt to dynamic environments; prior machine-learning methods (e.g., MADDPG-based) are limited to 2D maps or assign fixed, separate target areas with no dynamic flight pattern. The CPP problem is NP-hard and additionally requires coordination across agents. To react to unpredictable mission changes (unforeseen agent termination, collisions, or changes in the target area), replanning must be feasible in real time. The work extends the authors' prior single-agent system to a dynamic, decentralized-execution multi-agent system.

## Robustness Setting
- **Threat model / uncertainty set**: Not specified as a formal uncertainty set. Robustness is treated empirically: (i) the system must react in real time to unpredictable events such as an agent unexpectedly terminating or colliding, or a change in the target area mid-flight; (ii) generalization is sought across randomly generated maps and parameters (target area, start-and-landing zone, movement budget, 3D structure). The motion model assumes a safety controller on top of the RL model, so collisions/NFZ entries cause the agent to hover instead.
- **Setting**: cooperative; centralized training with decentralized execution (CTDE); online learning (the reward function is based on all agents)

## Method
- Formulates multi-agent CPP as a Decentralized Partially Observable Markov Decision Process (Dec-POMDP) over a 3D boolean grid map, with state composed of the 3D grid map, the target area (each cube has six individually coverable faces), no-fly zones (NFZ), the start-and-landing zone (SLZ), agent positions, and per-agent power/movement-budget levels.
- Each agent has six discrete actions (up, down, north, east, west, south); coverage is orientation-aware (each side sensor only covers the opposing-facing cells, with a 5×5×3 pyramid coverage volume, occlusion-aware); collisions or NFZ entry cause hovering.
- Trains with Proximal Policy Optimization (PPO) using the clipped surrogate objective; an actor network outputs action probabilities via softmax and a critic network estimates the state value, both fed by convolutional processing of three observation maps (3D local map, 2D local map, 2D global map) concatenated with the movement budget.
- Uses a partial observation per agent for scalability and a Dijkstra-based safe-landing mechanism on top of the policy; trains on randomly generated maps (geometric-shape sampling plus real Airborne Laser Scan point clouds) to improve generalization.
- Adds a communication procedure where each agent periodically transmits position, coverage status, and map ID to share outdoor coverage information; map reconstruction transfers existing coverage when map IDs differ.

## Theoretical Contributions
None / mostly empirical. The paper provides the Dec-POMDP formulation and the PPO clipped objective but no convergence, sample-complexity, or robustness-certification results.

## Experiments
- **Environment/Benchmark**: Randomly generated 3D grid maps (32×32×10) using sampled geometric shapes and Austrian government Airborne Laser Scan point clouds; Monte Carlo simulation comparing single-agent vs. multi-agent (n=3); hardware experiments with three Crazyflie 2.1 quadcopters using the CrazySwarm framework and motion capture, processed on a centralized i5 (5th-generation) computer.
- **Baselines**: Single-agent system (the authors' prior work) vs. the proposed multi-agent (n=3) system. No external robust-RL baselines.
- **Evaluation metrics**: Coverage ratio (across movement budgets and randomized maps), variance/interquartile range and outliers of the coverage ratio, and (in hardware) achieving over 99% target-area coverage while returning to the start-and-landing zones within movement constraints.

## Key Results
- The multi-agent system's coverage efficiency increases more rapidly than the single-agent system as more movement budget is granted (steeper coverage-ratio slope), indicating superior area coverage within a given time frame.
- The multi-agent system shows a smaller interquartile range and hardly any outliers, suggesting lower variance and higher robustness — consistent performance under varying conditions.
- The Monte Carlo results show the model generalizes over all randomized parameters (TA, SLZ, movement budget, 3D structure) and can handle in-flight changes of agent positions or target area, since the action prediction at state s_t is independent of s_{t-1}.
- Hardware experiment: three agents covered over 99% of the target area and returned within the movement budget; when the third agent was deliberately made to collide, the remaining agents dynamically changed their trajectories so the second agent covered the area initially assigned to the failed third agent, demonstrating adaptability and successful sim-to-hardware transfer.

## Limitations & Future Work
- Communication efficacy is limited to small agent groups, as message volume escalates rapidly with the number of agents; for larger groups transmission should target only neighboring agents (future work).
- Tested only with small swarms (n=3) on miniature indoor quadcopters with a centralized weak processor; outdoor autonomous evaluation with companion computers is future work.
- A communication protocol (planned via 5G and LoRaWAN) is needed to enable full autonomy and exchange of coverage information.
- Plans to incorporate additional sensor-evaluation models so agents can detect changing environmental conditions and optimize coverage from real-time sensor data.

## Relevance to Survey
This is an applied multi-agent deep-RL paper (PPO under Dec-POMDP, CTDE) for UAV coverage path planning rather than a formal robust-MARL contribution. Its connection to the robust-MARL landscape is empirical: it targets fault tolerance / agent-failure recovery (remaining agents re-cover a failed agent's region), real-time adaptation to dynamic environment changes, and generalization over randomized parameters — themes adjacent to robustness against agent failure and non-stationary environments. It does not engage with robust MDP, adversarial RL, distributionally robust RL, or minimax formulations, so it sits at the periphery of the survey as a resilience/fault-tolerance application example within cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Researchers have proposed several genetic algorithm-based MACPP methods that perform well in complex 3D environments. For instance, the authors of [3] proposed a sampling-based algorithm that uses a grid-based representation of the environment and uses an encoding and decoding strategy for the state processing. Similarly, Li et al. proposed a genetic algorithm-based method that samples viewpoints to optimize coverage and path lengths for multiple UAVs [4]. While these methods perform well in offline environments, they have a long calculation time and cannot adapt to dynamic environments."

> _[Introduction]_

"Linear optimization-based methods have also been proposed for MACPP. Melo et al. proposed a linear optimization-based method that is combined with a heuristic to find the optimal paths for multiple UAVs [5]. This method works well in 3D environments and can handle dynamic environments by reoptimzation. However, it also has a high computational time, and the model may not be scalable for large-scale problems. To overcome the limitation of static approaches, machine learning-based approaches seems to be a promising alternative. The authors of [6] proposed a MACPP algorithm based on Multi-Agent Deep Deterministic Policy Gradient (MADDPG) algorithm to solve the CPP problem. The MADDPG algorithm learns a centralized critic and decentralized actor networks for each UAV, which can generalize well over map parameters. However, this method is only applicable to 2D maps and may not be applicable in 3D environments as the scanning of vertical walls is not guaranteed (e.g for inspection). The same applies to the framework proposed by Bayerlein et al. [7], which is based on deep reinforcement learning. Another machine learning-based MACPP algorithm is proposed in [8]. This method only assigns separated target areas to the respective agents with no dynamic flight pattern within the region."

> _[Introduction]_

"Our framework is based on our previous work as described in [9], where we demonstrated the deep reinforcement model on a single-agent system."

### Cited references (resolved from the paper's bibliography)
- **[3]** W. Jing, D. Deng, Y. Wu, K. Shimada. *Multi-UAV coverage path planning for the inspection of large and complex structures.* IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2020.
- **[4]** M. Li, A. Richards, M. Sooriyabandara. *Reliability-aware multi-UAV coverage path planning using a genetic algorithm.* Proceedings of the 20th International Conference on Autonomous Agents and MultiAgent Systems (AAMAS) 2021.
- **[5]** A. G. Melo, M. F. Pinto, A. L. Marcato, L. M. Honório, F. O. Coelho. *Dynamic optimization and heuristics based online coverage path planning in 3D environment for UAVs.* Sensors 2021.
- **[6]** L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, L. Hanzo. *Multi-agent deep reinforcement learning-based trajectory planning for multi-UAV assisted mobile edge computing.* IEEE Transactions on Cognitive Communications and Networking 2020.
- **[7]** H. Bayerlein, M. Theile, M. Caccamo, D. Gesbert. *Multi-UAV path planning for wireless data harvesting with deep reinforcement learning.* IEEE Open Journal of the Communications Society 2021.
- **[8]** G. Sanna, S. Godio, G. Guglieri. *Neural network based algorithm for multi-UAV coverage path planning.* International Conference on Unmanned Aircraft Systems (ICUAS) 2021.
- **[9]** J. Bialas, M. Doller. *Coverage path planning for unmanned aerial vehicles in complex 3D environments with deep reinforcement learning.* IEEE International Conference on Robotics and Biomimetics (ROBIO) 2022.
