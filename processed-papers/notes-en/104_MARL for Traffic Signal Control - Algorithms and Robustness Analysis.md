# 104. Multi-Agent Reinforcement Learning for Traffic Signal Control: Algorithms and Robustness Analysis

## Metadata
- **Title**: Multi-Agent Reinforcement Learning for Traffic Signal Control: Algorithms and Robustness Analysis
- **Authors**: Chunliang Wu, Zhenliang Ma, Inhi Kim
- **Affiliation**: Institute of Transport Studies, Department of Civil Engineering, Monash University, Clayton, VIC, Australia
- **Venue**: Not specified (IEEE publication; downloaded from IEEE Xplore)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/traffic uncertainty (stochastic traffic flow / random arrivals, varying traffic demand patterns), state/observation perturbation (noisy/uncertain sensor data), and system disturbances in the online traffic environment
- **Method paradigm**: Decentralized multi-agent deep RL (independent learners), Q-learning / Deep Q-Network (DQN) with dueling architecture, transfer learning (offline-to-online) for robustness evaluation
- **Keywords**: Traffic signal control, multi-agent reinforcement learning, dueling DQN, transfer learning, robustness, VISSIM microsimulation

## TL;DR
The paper proposes a decentralized multi-agent dueling-DQN traffic signal control method, builds a general RL + VISSIM microsimulation platform, and uses a transfer learning technique to test the robustness of the trained controller (and traditional methods) under stochastic flow, varying demand, and noisy sensor data, showing RL is robust to traffic-flow/demand variation but unstable under highly noisy sensors.

## Problem & Motivation
Urbanization and growing travel demand outpace road-capacity expansion, causing congestion. Traditional fixed-time and vehicle-actuated controllers are limited (historical-data based or myopic/greedy), and adaptive/model-based control suffers from the difficulty of precisely describing complex, dynamic, stochastic traffic dynamics. RL-based signal controllers have been widely validated offline for convergence accuracy, but few works examine the robustness of trained RL controllers when deployed in a dynamic online traffic environment — which is the actual purpose of controlling dynamic systems. The paper aims to build a general multi-agent RL signal control platform and, for the first time (per the authors), test the robustness of an optimal multi-agent RL signal control model using transfer learning techniques.

## Robustness Setting
- **Threat model / uncertainty set**: Perturbations are introduced at deployment/online testing time: (1) stochastic traffic flow via different random seeds per episode (random arrivals); (2) varying traffic demand (0.8x low and 1.2x high relative to base scenario); (3) uncertain/noisy sensor data via additive Gaussian noise on the observed vehicle counts (e.g., noise level 10 means vehicle counts fluctuate by ±10 around the true value). No explicit adversary; uncertainty is modeled as scenario shifts and observation noise.
- **Setting**: Cooperative multi-intersection network with decentralized control (each signal controller is an independent learning agent that can communicate with neighbors); decentralized execution; offline training transferred to online learning/testing.

## Method
- **MDP formulation per intersection**: State = current phase, elapsed green time, total number of vehicles in lanes sharing the same signal phase (grouped vehicle counts within camera view, e.g., 100m), and current phase of neighboring intersections. Actions = {extend current phase, terminate and switch to next phase}, decided every fixed interval (e.g., 10s) with a fixed phase sequence for safety and constraints on min/max phase duration. Reward = number of vehicles passing through the intersection at the time step (proxy for delay, collectible from loop detectors).
- **Decentralized multi-agent control**: Each signal controller learns its own policy independently using Q-learning to maximize expected rewards.
- **Function approximation**: A deep neural network approximates the Q-function; a dueling DQN architecture splits estimation into a state-value stream V(s) and an advantage stream A(s,a). Training minimizes a squared TD loss with a fixed separate target network; an experience replay buffer with random mini-batch sampling breaks temporal correlations and stabilizes learning.
- **Transfer learning for robustness**: The offline-trained model (function approximators + RL parameters) is transferred to the online environment, where it keeps learning and adjusting with new real-time observations; DNN parameters are fixed for a few episodes (e.g., 6) to collect enough online experience before being updated.

## Theoretical Contributions
None / mostly empirical. The paper is an algorithmic and empirical study (MDP formulation + dueling DQN + transfer learning); no convergence, sample-complexity, or equilibrium-existence proofs are provided.

## Experiments
- **Environment/Benchmark**: A custom platform integrating a Python RL controller with the VISSIM microsimulator via the COM interface. Road network with four signalized intersections (150m spacing), each with four phases and a fixed phase sequence; decentralized control. Training: 150 episodes, each 3600s with 5 min warm-up; robustness scenarios: stochastic traffic flow (random seeds), low/high demand (0.8x / 1.2x), and Gaussian sensor noise on observations.
- **Baselines**: Fixed-time control (optimized via the Webster method) and vehicle-actuated control.
- **Evaluation metrics**: Average vehicle delay of the whole road network (objective is to minimize vehicle delay); cumulative reward during offline training is also tracked.

## Key Results
- Offline, after ~50 training episodes the agent-based system converges; final average delay per vehicle is reduced by 29.1% vs. fixed-time control and 16.1% vs. actuated control.
- Under stochastic traffic flow and under both low and high demand patterns, the agent-based system outperforms fixed-time and actuated control; its delay varies more than the baselines under random arrivals but remains lower.
- The RL method is relatively stable when sensor noise is less than 20, but performs poorly at the start of online testing when sensor data is too noisy; it keeps improving via online learning as testing proceeds (notably under congestion and noisy observations).

## Limitations & Future Work
- The trained RL controller is unstable under highly noisy sensor data (high observation noise).
- Experiments are limited to a fixed four-intersection VISSIM network without route choice or changing traffic-split fractions.
- Future work: investigate robustness in more complex traffic environments (real networks with route-choice possibilities and changing traffic-split fractions); study how other theories such as optimal control theory can be applied to strengthen the robustness of RL-based signal control methods.

## Relevance to Survey
This paper sits on the application/empirical edge of the robust MARL landscape: a decentralized cooperative MARL system whose robustness is evaluated against environment/distribution shift (stochastic flow, demand change) and observation perturbation (sensor noise), rather than via adversarial training or formal robust-MDP guarantees. It connects the robust-MARL theme to real-world multi-agent traffic signal control and to robustness-via-transfer-learning / online adaptation, and is representative of how observation-noise and non-stationary-environment robustness is assessed empirically in cooperative MARL applications.

## Related Work (verbatim excerpts from the paper)
> _[Section: Related Work]_

"This section focuses on the studies that applied RL for traffic signal control. Table І summarizes and compares the studies with respect to the following aspects: RL algorithms, RL value function approximators, control strategies (phases, states, and rewards), experiment designs (road network scale, benchmark, and performance metrics)."

"Two types of RL algorithms, namely model-based and model-free approaches, are used for the design of traffic signal controllers [14, 17, 19]. For the model-based approach, an exact model is required to describe the environment adequately, and the agent uses it to find an optimal policy [23]. Although the model-based RL method is more efficient in convergence and data requirement compared with the model-free RL method, building an exact model describing the stochastic traffic environment is not trivial or hardly possible. Thus, the model-free RL method is more frequently used in the literature. The model-free RL is further divided into value-based (Q-learning and State-action-reward-state-action (SARSA)) and policy-based (Actor-critic) methods [14, 22]. Earlier studies mainly used the discrete model-free RL, which stores the estimated state-action values in tabular form [17]. However, it is impossible to trace all station-action pairs in a complex traffic environment, given the massive number of station-action pairs. To address that challenge, several studies proposed various value function approximators such as tile coding and neural network to estimate state-action pairs [18, 19]. Recently, with the rise of machine learning, deep learning algorithms are endowed with strong predictive ability. Thus, several studies have attempted to use deep neural networks (DNN) to approximate objective functions [15, 16, 20]. One common issue is that most of those studies focus on signal control for one intersection."

"Regardless of the solution algorithm, the key challenges for an effective RL-based signal controller are definitions of states, actions, and rewards, which are problem-specific. In the previous studies, queue length, cumulative vehicle delay, and the number of vehicles arriving at intersections are commonly used to characterize the environment state. More recently, some studies attempt to use an image as the state to obtain more comprehensive traffic environment information [15]. However, extracting useful information from images needs a large number of samples, and the training process is time-consuming. Even if a model can continuously extract traffic state information, it does not necessarily guarantee that an agent can learn a better signal control policy. Action definition is based on signal phases. For the multi-phase intersections, studies often assume that the agents can randomly select a phase without considering the pre-defined phase sequence. Frequently changing phase sequence is not practical and could confuse drivers and cause safety concerns [16]. Also, the immediate reward is usually measured by queue length and travel delay. However, the travel delay of vehicles is rather difficult to collect in the real-world."

"Another challenge is how to guarantee the robustness of the signal controllers under a real traffic environment with complex and dynamic traffic and noisy observations from sensors. Most studies in the literature validated the proposed RL-based algorithms offline about their convergence accuracy; however, it is not clear about the robustness of these algorithms in an online traffic environment. Aslani, et al. [19] firstly attempted to test the robustness of different RL algorithms against system disturbances for multi intersections. They found that the value-based RL is lack of robustness under perturbations. After training for a couple of hours, the policy-based RL can handle the disturbances. It is worth noting that tile coding is used as an approximator to estimate the value-function. The estimation accuracy of this method is questionable. It might lead to the instability of RL-based control algorithms. Rodrigues and Azevedo [21] designed an RL-based controller for an isolated intersection and evaluated its robustness under varying demand and sensor failures. They found that the RL algorithm performs better only when the phase sequence is varied. They also pointed out that in order to develop a robust RL-based signal control algorithm, it is essential to extract more comprehensive traffic state information for offline training."

### Cited references (resolved from the paper's bibliography)
- **[14]** S. El-Tantawy, B. Abdulhai, H. Abdelgawad. *Design of Reinforcement Learning Parameters for Seamless Application of Adaptive Traffic Signal Control.* Journal of Intelligent Transportation Systems, 2014.
- **[15]** S. S. Mousavi, M. Schukat, E. Howley. *Traffic light control using deep policy-gradient and value-function-based reinforcement learning.* IET Intelligent Transport Systems, 2017.
- **[16]** X. Liang, X. Du, G. Wang, Z. Han. *A Deep Reinforcement Learning Network for Traffic Light Cycle Control.* IEEE Transactions on Vehicular Technology, 2019.
- **[17]** M. Wiering. *Multi-agent reinforcement learning for traffic light control.* ICML 2000.
- **[18]** I. Arel, C. Liu, T. Urbanik, A. G. Kohls. *Reinforcement learning-based multi-agent system for network traffic signal control.* IET Intelligent Transport Systems, 2010.
- **[19]** M. Aslani, S. Seipel, M. S. Mesgari, M. Wiering. *Traffic signal optimization through discrete and continuous reinforcement learning with robustness analysis in downtown Tehran.* Advanced Engineering Informatics, 2018.
- **[20]** L. Li, Y. Lv, F.-Y. Wang. *Traffic signal timing via deep reinforcement learning.* IEEE/CAA Journal of Automatica Sinica, 2016.
- **[21]** F. Rodrigues, C. L. Azevedo. *Towards Robust Deep Reinforcement Learning for Traffic Signal Control: Demand Surges, Incidents and Sensor Failures.* IEEE Intelligent Transportation Systems Conference (ITSC) 2019.
- **[22]** T. Chu, J. Wang, L. Codeca, Z. Li. *Multi-Agent Deep Reinforcement Learning for Large-Scale Traffic Signal Control.* IEEE Transactions on Intelligent Transportation Systems, 2019.
- **[23]** J. Jin, X. Ma. *Hierarchical multi-agent control of traffic lights based on collective learning.* Engineering Applications of Artificial Intelligence, 2018.
