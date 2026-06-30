# 77. Towards Fault Tolerance in Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Towards Fault Tolerance in Multi-Agent Reinforcement Learning
- **Authors**: Yuchen Shi, Huaxin Pei, Liang Feng, Yi Zhang, Danya Yao
- **Affiliation**: Department of Automation, Tsinghua University, Beijing; QiYuan Lab, Beijing; Beijing National Research Center for Information Science and Technology (BNRist), Tsinghua University
- **Venue**: Not specified (arXiv preprint, arXiv:2412.00534v1, 30 Nov 2024)
- **Link/arXiv**: arXiv:2412.00534v1 [cs.LG]; code: https://github.com/xbgit/FaultTolerance_AACFT

## Taxonomy
- **Robustness / perturbation type targeted**: Agent faults (system-level faults where a faulty agent loses its ability to observe, communicate, and act; faults occur at random agents and random times), causing chaotic state space and sample imbalance in the replay buffer.
- **Method paradigm**: Attention-augmented actor-critic (built on MADDPG/CTDE), special input configuration to flag faults, Prioritized Experience Replay (PER) extension, curriculum-capable platform.
- **Keywords**: Fault Tolerance, Multi-agent Reinforcement Learning, Attention, Prioritized Experience Replay, MADDPG, CTDE

## TL;DR
The paper improves fault tolerance in MARL by incorporating an attention mechanism into the actor and critic networks to automatically detect and de-emphasize faulty-agent information, and by extending Prioritized Experience Replay with per-module priority queues to mitigate sample imbalance between pre- and post-fault transitions; an open-source fault-tolerant MARL platform is also released.

## Problem & Motivation
Cooperative multi-agent systems (autonomous driving, drone formation, multi-robot control) inevitably suffer individual agent faults, and MARL algorithms are highly vulnerable to such unexpected faults during both training and execution. A failed agent loses its ability to move, communicate, and perceive, disrupting the communication structure and forcing task reallocation. This raises two key challenges: (1) the chaotic inputs of networks — the sudden reduction of valid agents reduces valid dimensions of the state space and injects invalid information from the failed agent; (2) sample imbalance — because faults are randomly assigned to different agents at random timesteps, the replay buffer stores many similar pre-fault transitions but highly varied post-fault transitions, so uniform sampling repeats inessential transitions and reduces training efficiency. Prior fault-tolerant cooperative control and rule/assignment-based methods do not specifically target MARL algorithms, and robust MARL (which balances performance under action deviation) is not designed for these specific fault types.

## Robustness Setting
- **Threat model / uncertainty set**: A multi-agent system with N potentially faulty agents modeled as Dec-POMDPs with an added fault component F. A fault occurs with probability p = F(s, t) depending on state s and time t; the next-state transition s′ = T(s, a₁, ..., a_N, p) depends on p. A faulty agent becomes incapacitated (cannot observe/communicate/act); its observation and action become invalid. A Boolean fault status Fᵢ marks each agent (1 = normal, 0 = fault). Fault types include restricting actions of faulty agents or adding noise to their observations; faults can disrupt communication, require recovery, require dynamic rescheduling, or introduce entirely new tasks.
- **Setting**: Cooperative; CTDE (centralized training with decentralized execution, built on MADDPG); online deep RL with replay buffer.

## Method
- **Input configuration for fault flagging**: Each agent's observation oᵢ = [oᵢ₁, ..., oᵢ(N+M)] encodes self-state, partial observations of other agents (with one-hot communication state cᵢⱼ over "normal" / "out of range" / "fault"), and environment/task states. When agent j fails (Fⱼ = 0), the critic input is set to oⱼ = z·1, aⱼ = 0, where the special flag z has absolute value much larger than normal values to make anomalies prominent.
- **Attention in the critic (AACFT)**: An encoder f_cᵢ maps (oᵢ, aᵢ) to embedding eᵢ; an attention module computes weights αᵢⱼ (query-key similarity, Eq. 3) and attention embedding bᵢ (Eq. 4); decoder g_cᵢ outputs Qᵢ(o, a) (Eq. 6). Attention diverts focus away from the faulty agent's observation. All critics share parameters and are updated jointly with a masked regression loss (faulty agents excluded via Fᵢ; Eq. 7).
- **Attention in the actor**: The faulty agent's state may still matter to others, so oᵢⱼ is set to Yᵢ(s_{j,t₀}) (state at fault time t₀) if still meaningful, else to z·1. A learnable token eᵢ₀ is added (as in attention-for-classification models); the actor attends from the token over embeddings to output the action μ_θᵢ(oᵢ) (Eq. 8), letting it dynamically decide how much attention to give the faulty agent at different task stages. The actor of a faulty agent is disabled and excluded from its loss (Eq. 9).
- **Prioritized Experience Replay for AACFT**: PER is extended across all N+1 modules (one shared critic queue Q_c plus one queue per actor Q_{a,i}); priorities are rank-based (pᵢ = 1/rank(i)) and monotonic with each module's loss, biasing sampling toward higher-loss (harder, often post-fault) transitions. Transitions involving a faulty agent i are not added to Q_{a,i}. Importance-sampling weights (Eq. 11, β annealed to 1) ensure unbiased updates (Algorithm 1).
- **Open-source platform (FTMAL)**: A highly decoupled platform centralizing fault management in a dedicated Fault Controller, with Runner, Algorithm, Environment, Curriculum, Configs, and Logging modules, enabling modular customization of faults, algorithms, and environments.

## Theoretical Contributions
None / mostly empirical. The paper presents methodology, network design, and an algorithm (Algorithm 1) but does not provide convergence or sample-complexity guarantees.

## Experiments
- **Environment/Benchmark**: Four scenarios modified from the Multi-Agent Particle Environment (MPE): Abandonment, Recovery, Navigation, and Patrol (predator-prey-style cooperative tasks with obstacles, prey/targets, and injected faults). Reward decomposed into individual terms (communication, boundary, collision, distance) plus a team goal reward (Eq. 12).
- **Baselines**: M3DDPG (robust MARL, minimax extension of MADDPG), MADDPG (automatic identification, single critic/actor handling pre- and post-fault), MADDPG+MC (manual identification with multiple critics, one per pre-fault and per other-agent fault). Ablations: AAFT (no critic attention), ACFT (no actor attention); and AACFT with vs. without PER.
- **Evaluation metrics**: Episode rewards (training curves), task completion rate (boxplots and tables), attention distribution visualizations, Additional Sampling Rate (Eq. 13) for PER analysis, and completion rate at different fault timesteps.

## Key Results
- **Necessity**: Vanilla MADDPG trained without faults drops from 0.872 task completion rate (no fault) to 0.382 when agent 2 fails at timestep 5, motivating fault tolerance.
- **Comparative**: All methods perform similarly in no-fault scenarios; only AACFT avoids reward decline in the abandonment/recovery scenarios. M3DDPG underperforms AACFT in all scenarios (robustness methods do not directly address fault tolerance). MADDPG approaches AACFT only in navigation; MADDPG+MC only surpasses AACFT in recovery when agent 2 fails (and is cumbersome/space-heavy). AACFT shows the largest gain when agent 3 fails in recovery (handling task redistribution).
- **Ablation**: AACFT beats AAFT and ACFT in most cases; both actor and critic attention modules are necessary (actor attention helps more in complex task-redistribution scenarios).
- **PER**: In the challenging patrol scenario, AACFT with PER significantly outperforms AACFT without PER (vanilla AACFT fails to learn an effective strategy). Additional Sampling Rate for post-fault transitions rises to nearly 30% later in training, and later-timestep pre-fault transitions (closer to faults) are sampled more.
- **Time adaptability**: AACFT keeps a high completion rate across fault timesteps (e.g., 0.789 at t=5 up to 0.846 at t=25, vs. 0.841 no-fault), increasing with later fault times.

## Limitations & Future Work
- Evaluation is limited to four MPE-derived predator-prey-style scenarios; faults are restricted to action restriction and observation noise.
- No theoretical guarantees are provided.
- Future work: design more types of faults within the platform to test adaptability and generalizability to different fault information, and explore the method in more complex environments to further validate effectiveness and practicality.

## Relevance to Survey
This paper sits in the "agent failure / fault tolerance" branch of robust MARL, distinct from (but adjacent to) the action-deviation/minimax robustness line represented by M3DDPG, which it explicitly contrasts as not addressing fault tolerance. It connects the attention-mechanism line (actor-attention-critic) and the prioritized-experience-replay / sample-reweighting line to fault-tolerant cooperative MARL, and contributes an open-source fault-tolerant MARL platform. It is a useful reference for survey themes on agent faults, communication-structure disruption, and robustness vs. fault-tolerance distinctions.

## Related Work (verbatim excerpts from the paper)
> _[Section II.A, Related Works — Fault tolerance]_

"In this paper, we focus on addressing highly critical system-level faults in agents, where the affected agent loses its ability to observe or act, as opposed to faults occurring in specific components of the agent [18]–[21]. In the existing studies, Pei et al. [22] construct a rule-based model to achieve fault tolerance in multi-vehicle cooperative driving at signal-free intersections. Kamel et al. [23] design task-reassignment algorithms taking use of Hungarian algorithm, to ensure the completion of robot teams task after a robot's fault. Nevertheless, these works do not specifically aim to achieve fault tolerance in MARL algorithm. Some researchers focus on robust MARL [24], [25], emphasizing performance balance when agent actions deviate. However, our research concentrates on enhancing performance in the event of specific types of faults, which is not the strength of robust MARL."

> _[Section II.B, Related Works — MARL]_

"CTDE framework for MARL, including QMIX [26], MADDPG [15], COMA [27], MAPPO [16], avoids the problem of non-stationarity when agents learn independently, and also avoids the problem of action space dimension explosion when a multi-agent system is modeled as a single agent. Recently, many studies have endeavored to enhance MARL algorithms, aiming to increase their adaptability to real-world MARL environments [28]–[33], such as R-MADDPG for partial observable environments [34], and MADDPG-M for environments with extremely noisy observations [35]. Similarly, we propose our model based on MADDPG, making it capable of fault tolerance problems in MARL."

> _[Section II.C, Related Works — Attention]_

"Attention mechanism has become a popular technique due to its superior performance, interpretability, and ease of integration with basic models [36]. Attention mechanism is widely employed for a variety of deep learning models across many different domains and tasks, including natural language processing [37]–[39], computer vision [40], [41], reinforcement learning [42]–[45]. Iqbal & Sha [42] using centrally computed critics that share an attention mechanism, dynamically selecting which agents to attend to, enable more effective learning in MARL. In our approach, the attention mechanism plays a crucial role in enhancing fault tolerance."

> _[Section II.D, Related Works — Transitions Reweighting]_

"Transitions reweighting is an effective method to improve utilization efficiency of transitions. There are typically two types: prioritizing easy transitions and prioritizing difficult transitions. The former is suitable for addressing issues with noisy labels in the dataset, as it tends to favor lower-loss examples which are more likely to be clean data [46]. It is also suitable for solving extremely difficult problems that require a step-by-step approach [47]. The latter prioritizes higher-loss samples that are more likely to belong to minority cases, thereby alleviating sample imbalance, such as Hard Example Mining (HEM) [48] and Prioritized Experience Replay (PER) [17]. Considering that data in RL problems is clean and there is sample imbalance in fault tolerance problems, we extend PER to fault tolerance problems based on MARL and adapt it to our proposed AACFT."

### Cited references (resolved from the paper's bibliography)
- **[15]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[16]** Yu, Velu, Vinitsky, Gao, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative multi-agent games (MAPPO).* NeurIPS 2022.
- **[17]** Schaul. *Prioritized experience replay.* ICLR 2016.
- **[18]** Kumar, Cohen. *Towards a fault-tolerant multi-agent system architecture.* Proc. 4th International Conference on Autonomous Agents 2000.
- **[19]** Arfat, Eassa. *A survey on fault tolerant multi agent system.* IJ Inf. Technol. Comput. Sci, 2016.
- **[20]** Liu, Han, He. *Adaptive fault-tolerant boundary control of an autonomous aerial refueling hose system with prescribed constraints.* IEEE Transactions on Automation Science and Engineering, 2022.
- **[21]** Zhu, Wang, Zhang, Yang. *A GOA-based fault-tolerant trajectory tracking control for an underwater vehicle of multi-thruster system without actuator saturation.* IEEE Transactions on Automation Science and Engineering, 2024.
- **[22]** Pei, Zhang, Zhang, Pei, Feng, Li. *Fault-tolerant cooperative driving at signal-free intersections.* IEEE Transactions on Intelligent Vehicles, 2022.
- **[23]** Kamel, Yu, Zhang. *Fault-tolerant cooperative control design of multiple wheeled mobile robots.* IEEE Transactions on Control Systems Technology, 2018.
- **[24]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[25]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game.* arXiv:2305.12872, 2023.
- **[26]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[27]** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual multi-agent policy gradients (COMA).* AAAI 2018.
- **[28]** Long, Zhou, Gupta, Fang, Wu, Wang. *Evolutionary population curriculum for scaling multi-agent reinforcement learning.* ICLR 2019.
- **[29]** Brittain, Wei. *Scalable autonomous separation assurance with heterogeneous multi-agent reinforcement learning.* IEEE Transactions on Automation Science and Engineering, 2022.
- **[30]** Yu, Yang, Gao, Chen, Li, Liu, Xiang, Huang, Yang, Wu et al. *Asynchronous multi-agent reinforcement learning for efficient real-time multi-robot cooperative exploration.* AAMAS 2023.
- **[31]** Li, Hao, Tang, Zheng, Fu. *RACE: improve multi-agent reinforcement learning with representation asymmetry and collaborative evolution.* ICML 2023.
- **[32]** Miao, Cui, Li, Wu. *Effective multi-agent deep reinforcement learning control with relative entropy regularization.* IEEE Transactions on Automation Science and Engineering, 2024.
- **[33]** Zhu, Huang, Zuo, Zhao, Sun. *Multi-task multi-agent reinforcement learning with task-entity transformers and value decomposition training.* IEEE Transactions on Automation Science and Engineering, 2024.
- **[34]** Wang, Everett, How. *R-MADDPG for partially observable environments and limited communication.* arXiv:2002.06684, 2020.
- **[35]** Kilinc, Montana. *Multi-agent deep reinforcement learning with extremely noisy observations.* arXiv:1812.00922, 2018.
- **[36]** Brauwers, Frasincar. *A general survey on attention mechanisms in deep learning.* IEEE Transactions on Knowledge & Data Engineering, 2021.
- **[37]** Bahdanau, Cho, Bengio. *Neural machine translation by jointly learning to align and translate.* ICLR 2015.
- **[38]** Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin. *Attention is all you need.* NeurIPS 2017.
- **[39]** Minaee, Mikolov, Nikzad, Chenaghlu, Socher, Amatriain, Gao. *Large language models: A survey.* arXiv:2402.06196, 2024.
- **[40]** Mnih, Heess, Graves et al. *Recurrent models of visual attention.* NeurIPS 2014.
- **[41]** Dosovitskiy, Beyer, Kolesnikov, Weissenborn, Zhai, Unterthiner, Dehghani, Minderer, Heigold, Gelly et al. *An image is worth 16x16 words: Transformers for image recognition at scale.* ICLR 2020.
- **[42]** Iqbal, Sha. *Actor-attention-critic for multi-agent reinforcement learning.* ICML 2019.
- **[43]** Phan, Ritz, Altmann, Zorn, Nüßlein, Kölle, Gabor, Linnhoff-Popien. *Attention-based recurrence for multi-agent reinforcement learning under stochastic partial observability.* ICML 2023.
- **[44]** Hu, Zhang, Li, Chen, Ding, Wang. *Attention-guided contrastive role representations for multi-agent reinforcement learning.* arXiv:2312.04819, 2023.
- **[45]** He, Li, Xu, Zhu, Lu. *Novel distributed GRUs based on hybrid self-attention mechanism for dynamic soft sensing.* IEEE Transactions on Automation Science and Engineering, 2024.
- **[46]** Li, Yang, Song, Cao, Luo, Li. *Learning from noisy labels with distillation.* ICCV 2017.
- **[47]** Wang, Huang, Huang, Wang, Teng, Ko, Jeon, Wu. *Curriculum reinforcement learning from avoiding collisions to navigating among movable obstacles in diverse environments.* IEEE Robotics and Automation Letters, 2023.
- **[48]** Shrivastava, Gupta, Girshick. *Training region-based object detectors with online hard example mining (HEM).* CVPR 2016.
