# 71. Effective Communications: A Joint Learning and Communication Framework for Multi-Agent Reinforcement Learning over Noisy Channels

## Metadata
- **Title**: Effective Communications: A Joint Learning and Communication Framework for Multi-Agent Reinforcement Learning over Noisy Channels
- **Authors**: Tze-Yang Tung, Szymon Kobus, Joan Pujol Roig, Deniz Gündüz
- **Affiliation**: Information Processing and Communications Laboratory (IPC-Lab), Dept. of Electrical and Electronic Engineering, Imperial College London, UK
- **Venue**: Not specified (arXiv:2101.10369v2 [eess.SP], 1 Apr 2021; an earlier version was presented at IEEE GLOBECOM, December 2020)
- **Link/arXiv**: arXiv:2101.10369v2 [eess.SP]

## Taxonomy
- **Robustness / perturbation type targeted**: Communication channel noise (the inter-agent communication link is a noisy channel — BSC, AWGN, and bursty-noise channels — so messages can be corrupted in transit); robustness of the learned communication code/protocol to channel errors.
- **Method paradigm**: MA-POMDP formulation with the noisy channel embedded in the environment dynamics; messages treated as part of the action; joint deep RL (DQN, DDPG, REINFORCE, actor-critic) for joint learning-and-communication.
- **Keywords**: noisy communication channel, MA-POMDP, learning to communicate, joint source-channel coding, effectiveness problem, deep reinforcement learning

## TL;DR
The paper formulates Shannon and Weaver's "effectiveness problem" as a multi-agent POMDP in which agents communicate over an explicit noisy channel (the channel is part of the environment dynamics and each transmitted message is part of the agent's action), and shows that jointly learning to cooperate and to communicate yields policies and codes that outperform schemes which design communication (channel coding) separately from the underlying MARL task.

## Problem & Motivation
Classical communication engineering deals almost exclusively with Shannon-Weaver "Level A" (reliable transmission of symbols), separating the design of a reliable network from the "language" used to coordinate among agents. The recent "learning to communicate" line in MARL instead targets "Level C" (effectiveness) but assumes error-free communication channels, ignoring physical-layer characteristics such as noise and interference. Real systems (autonomous vehicles, drone swarms, robot teams) communicate over noisy wireless links, so a framework is needed that accounts for both channel noise and the end-to-end cooperative learning objective at once. The paper argues that treating communication separately from the MARL task (e.g., applying a standard channel code on top of a separately learned policy) is suboptimal, and that codes which emerge from joint optimization can differ substantially from those used for reliable message reproduction.

## Robustness Setting
- **Threat model / uncertainty set**: The perturbation is channel noise on the inter-agent communication link. The channel is governed by a conditional distribution Pc and is used M times per step (M = channel bandwidth). Three channel models are studied: binary symmetric channel (BSC) with crossover probability pe; additive white Gaussian noise (AWGN) channel with noise variance σ²ₙ; and a bursty-noise (BN) channel modeled by a two-state Markov noise process (low-noise vs. high-noise state, transition probability pb). Environment transitions themselves may also be stochastic (the grid-world action succeeds w.p. 1−δ, and goes to a random neighbor w.p. δ).
- **Setting**: Fully cooperative (agents share a common team reward); point-to-point communication (one guide, one scout in the main example); each agent treats the other as part of its environment (decentralized perspective per agent, no central critic); online model-free deep RL; the channel model is assumed unknown to the agents.

## Method
- Formulate a Markov game with noisy communications as an MA-POMDP: each agent i's action has two components, an environment action a_i and a transmitted signal m_i; its observation is the partial environment observation o_i plus the received channel output m̂_i. The channel is part of the environment dynamics, and the goal is to maximize the discounted sum of the shared team reward.
- Guided-robot example: split a single-agent MDP into a guide (observes the full state but cannot act on the environment) and a scout (acts on the environment but observes only the channel output). The guide transmits a codeword over M channel uses; the scout decodes it and chooses among 16 grid-world actions. With a perfect channel this recovers the original single-agent MDP, giving a performance upper bound.
- For the BSC and binary-input AWGN/BN channels, train both agents with deep Q-learning (DQN) using replay buffers, target networks, and ε-greedy exploration, minimizing the DQN squared-Bellman-error loss; the shared reward updates both the guide and scout networks.
- When the guide can output real-valued (continuous) channel inputs under an average-power constraint, use deep deterministic policy gradient (DDPG) for the guide (a parameterized deterministic policy plus critic, with Ornstein-Uhlenbeck exploration noise), and DQN for the scout. Relaxing the constellation from BPSK to real-valued inputs substantially improves performance.
- Joint channel-coding-and-modulation special case: a one-step MDP where the transmitter (agent 1) sends B bits over M channel uses and the receiver (agent 2) reconstructs the message; the reward is the negative cross-entropy. Solve with DDPG, REINFORCE, or actor-critic (the critic subtracts a learned baseline / state value to reduce policy-gradient variance), reducing block error rate (BLER).

## Theoretical Contributions
None / mostly empirical. The paper restates the deterministic policy gradient compatibility result (Theorem 1, attributed to [42]) used to justify DDPG, and notes that one of its conditions is generally not satisfied in practice; it does not provide new convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: (1) Guided-robot grid-world of size L×L: a guide and a scout connected by a noisy channel must cooperate to reach a treasure as quickly as possible, over BSC, AWGN, and BN channels, with channel bandwidth M ∈ {7, 10} and grid noise δ ∈ {0, 0.05}. (2) Joint channel-coding-and-modulation problem over AWGN and BN channels.
- **Baselines**: Separate learning and communication (a separately trained RL policy whose chosen actions are protected by a (7,4) Hamming code), using either random-codeword (RC) or hand-crafted (HC) action-to-codeword associations; "Optimal actions with Hamming code" (HC/RC) as a separation-based lower bound; "Optimal actions without noise" as an overall lower bound; for the coding problem, BPSK + (7,4) Hamming code and the model-free supervised-learning approach of [32] (REINFORCE-based).
- **Evaluation metrics**: Average number of steps to reach the treasure (grid-world); block error rate (BLER) and convergence behavior (joint coding-modulation); also computation time.

## Key Results
- Across BSC, AWGN, and BN channels, agents that jointly learn to collaborate and communicate require fewer average steps to reach the treasure than the separation-based schemes (HC and RC with a (7,4) Hamming code); neither approach matches the "optimal actions with Hamming code" bound, attributed to limited DQN capacity and the difficulty of learning under noise.
- Relaxing the guide's channel input from BPSK to real-valued ("Real") inputs gives the best performance, with the largest gains at low SNR; the authors stress that Shannon capacity is not the right metric, since channels with similar capacity can yield very different MARL rewards. The performance advantage over separation is most pronounced on the more challenging bursty-noise (BN) channel.
- For joint channel coding and modulation, the learning approaches (DDPG, REINFORCE, actor-critic) beat the BPSK + Hamming (7,4) code; adding a critic (actor-critic) outperforms the plain REINFORCE method of [32]. On average the learning-based results beat Hamming (7,4) by 1.24, 2.58, and 3.70 dB for DDPG, REINFORCE, and actor-critic, respectively; actor-critic converges fastest and reaches the lowest BLER. The DRL encoder/decoder adds only ~13% computation time (≈323 µs vs. 286 µs) over the separation baseline.

## Limitations & Future Work
- The study is restricted to point-to-point communication; extensions to multi-user communication channels (and the associated coordination problems) are left to future work.
- Reported results are for simple fully-connected DNN architectures; the authors note (Remark 1) that RNNs/LSTMs should help in these POMDPs but did not yield improvements in their initial experiments, likely due to architecture limitations.
- The guide/scout policies do not reach the optimal-with-Hamming-code bound, owing to limited network capacity and the challenge of learning under noisy channels.
- Only the channel modulation-and-coding problem is treated explicitly; the framework's reduction to source coding and joint source-channel coding (Remark 2) is described but not experimentally explored.

## Relevance to Survey
This paper sits on the "communication robustness" theme of the robust MARL landscape: rather than perturbing the environment model, agents, or observations adversarially, the perturbation is channel noise on the inter-agent communication link, and robustness is achieved by jointly learning policies and communication codes that tolerate/compensate for channel errors. It connects the "learning to communicate" MARL line (which assumes error-free channels) with classical information-theoretic communication (channel/source coding), and provides a concrete example of how MARL agents can adapt their messaging to remain robust to noise — relevant to survey discussions of communication attacks/perturbations and fault-tolerant coordination over imperfect channels.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Works]_

"The study of communication for multi-agent systems is not new [34]. However, due to the success of deep neural networks (DNNs) for reinforcement learning (RL), this problem has received renewed interest in the context of DNNs [24] and deep RL (DRL) [18], [35], [36], where partially observable multi-agent problems are considered. In each case, the agents, in addition to taking actions that impact the environment, can also communicate with each other via a limited-capacity communication channel. Particularly, in [18], two approaches are considered: reinforced inter-agent learning (RIAL), where two centralized Q-learning networks learn to act and communicate, respectively, and differentiable inter-agent learning (DIAL), where communication feedback is provided via backpropagation of gradients through the channel, while the communication between agents is restricted during execution. Similarly, in [37], [38], the authors propose a centralized learning, decentralized execution approach, where a central critic is used to learn the state-action values of all the agents and use those values to train individual policies of each agent. Although they also consider the transmitted messages as part of the agents' actions, the communication channel is assumed to be noiseless."

> _[Section II, Related Works]_

"CommNet [35] attempts to leverage communications in cooperative MARL by using multiple continuous-valued transmissions at each time step to make decisions for all agents. Each agent broadcasts its message to every other agent, and the averaged message received by each agent forms part of the input. However, this solution lacks scalability as it depends on a centralized network by treating the problem as a single RL problem. Similarly, BiCNet [39] utilizes recurrent neural networks to connect individual agent's policy with a centralized controller aggregating the hidden states of each agent, acting as communication messages."

> _[Section II, Related Works]_

"The reliance of the aforementioned works on a broadcast channel to communicate with all the agents simultaneously may be infeasible or highly inefﬁcient in practice. To overcome this limitation, in [19], the authors propose an attentional communication model that learns when communication is needed and how to integrate shared information for cooperative decision making. In [21], directional communication between agents is achieved with a signature-based soft attention mechanism, where each message is associated to the target recipient. They also propose multi-stage communication, where multiple rounds of communication take place before an action is taken."

> _[Section II, Related Works]_

"It is important to note that, with the exception of [40], all of the prior works discussed above rely on error-free communication channels. MARL with noisy communications is considered in [40], where two agents placed on a grid world aim to coordinate to step on the goal square simultaneously. However, for the particular problem presented in [40], it can be shown that even if the agents are trained independently without any communication at all, the total discounted reward would still be higher than the average reward achieved by the scheme proposed in [40]."

> _[Introduction]_

"It is well-known that multi-agent reinforcement learning (MARL) problems are notoriously difﬁcult, and are a topic of continuous research. Originally, these problems were approached by treating each agent independently, as in a standard single-agent reinforcement learning (RL) problem, while treating other agents as part of the state of the environment. Consensus and cooperation are achieved through common or correlated reward signals. However, this approach leads to overﬁtting of policies due to limited local observations of each agent and it relies on other agents not varying their policies [16]. It has been observed that these limitations can be overcome by leveraging communication between the agents [5], [17]. Recently, there has been signiﬁcant interest in the emergence of communication among agents within the RL literature [18]–[21]. These works consider MARL problems, in which agents have access to a dedicated communication channel, and the objective is to learn a communication protocol, which can be considered as a 'language' to achieve the underlying goal, which is typically translated into maximizing a speciﬁc reward function. This corresponds to Level C, as described by Shannon and Weaver in [2], where the agents change their behavior based on the messages received over the channel in order to maximize their reward. However, the focus of the aforementioned works is the emergence of communication protocols within the limited communication resources that can provide the desired impact on the behavior of the agents, and, unlike Shannon and Weaver, these works ignore the physical layer characteristics of the channel."

### Cited references (resolved from the paper's bibliography)
- **[2]** C. Shannon, W. Weaver. *The Mathematical Theory of Communication.* University of Illinois Press, 1949.
- **[5]** K.-C. Jim, L. Giles. *How communication can improve the performance of multi-agent systems.* Fifth Int'l Conf. on Autonomous Agents (AGENTS '01), 2001.
- **[16]** M. Lanctot, V. Zambaldi, A. Gruslys, A. Lazaridou, K. Tuyls, J. Perolat, D. Silver, T. Graepel. *A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning.* arXiv:1711.00832, 2017.
- **[17]** T. Balch, R. Arkin. *Communication in reactive multiagent robotic systems.* Autonomous Robots, 1994.
- **[18]** J. N. Foerster, Y. M. Assael, N. de Freitas, S. Whiteson. *Learning to Communicate with Deep Multi-Agent Reinforcement Learning.* arXiv:1605.06676, 2016.
- **[19]** J. Jiang, Z. Lu. *Learning attentional communication for multi-agent cooperation.* NeurIPS (Proc. 32nd Int'l Conf. on Neural Information Processing Systems), 2018.
- **[20]** N. Jaques, A. Lazaridou, E. Hughes, C. Gulcehre, P. Ortega, D. Strouse, J. Leibo, N. de Freitas. *Social Influence as Intrinsic Motivation for Multi-Agent Deep Reinforcement Learning.* arXiv:1810.08647, 2019.
- **[21]** A. Das, T. Gervet, J. Romoff, D. Batra, D. Parikh, M. Rabbat, J. Pineau. *TarMAC: Targeted multi-agent communication.* ICML (36th Int'l Conf. on Machine Learning), PMLR, 2019.
- **[24]** A. Lazaridou, A. Peysakhovich, M. Baroni. *Multi-Agent Cooperation and the Emergence of (Natural) Language.* arXiv:1612.07182, 2017.
- **[34]** K. Wagner, J. A. Reggia, J. Uriagereka, G. S. Wilkinson. *Progress in the Simulation of Emergent Communication and Language.* Adaptive Behavior, 2016.
- **[35]** S. Sukhbaatar, A. Szlam, R. Fergus. *Learning multiagent communication with backpropagation.* NIPS'16 (Proc. 30th Int'l Conf. on Neural Information Processing Systems), 2016.
- **[36]** S. Havrylov, I. Titov. *Emergence of Language with Multi-agent Games: Learning to Communicate with Sequences of Symbols.* 2017.
- **[37]** R. E. Wang, M. Everett, J. P. How. *R-MADDPG for Partially Observable Environments and Limited Communication.* arXiv:2002.06684, 2020.
- **[38]** R. Lowe, Y. Wu, A. Tamar, J. Harb, O. Pieter Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS (Advances in Neural Information Processing Systems, vol. 30), 2017.
- **[39]** P. Peng, Y. Wen, Y. Yang, Q. Yuan, Z. Tang, H. Long, J. Wang. *Multiagent Bidirectionally-Coordinated Nets: Emergence of Human-level Coordination in Learning to Play StarCraft Combat Games.* arXiv:1703.10069, 2017.
- **[40]** A. Mostaani, O. Simeone, S. Chatzinotas, B. Ottersten. *Learning-based Physical Layer Communications for Multiagent Collaboration.* IEEE Int'l Symp. on Personal, Indoor and Mobile Radio Comms. (PIMRC), 2019.
