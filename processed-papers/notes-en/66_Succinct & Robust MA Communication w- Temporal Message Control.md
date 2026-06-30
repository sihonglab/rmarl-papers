# 66. Succinct and Robust Multi-Agent Communication With Temporal Message Control

## Metadata
- **Title**: Succinct and Robust Multi-Agent Communication With Temporal Message Control
- **Authors**: Sai Qian Zhang, Jieyu Lin, Qi Zhang
- **Affiliation**: Harvard University; University of Toronto; Microsoft
- **Venue**: NeurIPS 2020
- **Link/arXiv**: Not specified (code: https://github.com/saizhang0218/TMC ; video demo: https://tmcpaper.github.io/tmc/)

## Taxonomy
- **Robustness / perturbation type targeted**: Communication robustness — transmission loss / packet loss in lossy and bandwidth-limited wireless networking environments (not adversarial); also reduction of redundant inter-agent messages.
- **Method paradigm**: Value function decomposition (QMIX/VDN) + learned inter-agent communication; temporal smoothing regularizer; action-confidence regularizer; message buffering protocol with threshold-based transmission.
- **Keywords**: cooperative MARL, inter-agent communication, communication overhead, transmission loss robustness, temporal message control, value decomposition

## TL;DR
The paper presents Temporal Message Control (TMC), a cooperative MARL communication framework that uses a temporal-smoothing regularizer plus a message-buffering protocol so agents transmit only when a message carries new information, drastically cutting communication overhead while naturally providing robustness to packet/transmission loss in lossy networks.

## Problem & Motivation
Communication can substantially improve cooperative MARL performance, but existing communication schemes assume a reliable channel and require agents to exchange an excessive, redundant number of messages at run time. This is impractical for real applications (autonomous driving, drone control) that have limited bandwidth and unreliable channels. Because consecutive observations are often highly similar, the resulting messages are highly time-correlated and redundant; sending all of them wastes bandwidth and can inject noisy messages that hurt performance. Prior work paid little attention to transmission reliability and message-exchange efficiency, motivating a method that leverages temporal locality to make communication both succinct and robust to loss.

## Robustness Setting
- **Threat model / uncertainty set**: Non-adversarial communication-channel unreliability. Packet/message loss is modeled with a multi-state (three-state) Markov loss model fitted to real 802.11ac wireless traces under light/medium/heavy background traffic (average loss rates 1.5%, 8.2%, 15.6%). Losses are bursty and temporally correlated. Lost messages are treated as missing (other baselines set lost messages to zero). Line-of-sight blockage by obstacles also causes loss in the grid-world environments.
- **Setting**: Fully cooperative; centralized training with decentralized execution (CTDE); online (deep Q-learning with value decomposition). Transmission loss is generally not included during training (except for the AC(light)/AC(heavy) Message-Dropout variants).

## Method
- **Agent network**: Each agent has a local action generator (GRU + MLP) producing local Q-values, a message encoder (MLP) producing a message, a combining block, a sent-message buffer, and a received-message buffer. Message dimension equals local Q-value dimension, so the global Q-value is an element-wise sum of the local Q-values and the valid buffered messages.
- **Temporal smoothing regularizer (L_s)**: Penalizes the squared difference between an agent's current message and its recent messages within a smoothing window w_s (weighted by β), encouraging temporally similar messages so the current message need not be sent if it is close to a previously sent one.
- **Action-confidence regularizer (L_r)**: Maximizes the gap between the largest and second-largest global Q-values, building confidence in action selection so the choice is not flipped by small temporal variation in (possibly stale) buffered messages.
- **Training loss**: TD error on the team Q-value (Q_team from a mixing network) plus λ_s·L_s minus λ_r·L_r; trained with ε-greedy and a target network.
- **Communication protocol (Algorithm 1)**: On the sender side, agent n broadcasts its new message only if its Euclidean distance from the last sent message exceeds threshold δ, or a timeout (t − t_last > w_s) is reached. On the receiver side, agent n stores the latest message per teammate with a valid bit, expires messages older than w_s, and computes the global Q-value as the sum of the local Q-value and currently valid buffered messages. Because each delivered message can be reused for up to w_s timesteps, the buffering naturally mitigates loss.

## Theoretical Contributions
None / mostly empirical. The robustness is argued and demonstrated empirically (e.g., via correlation analysis of lost vs. last-delivered messages), not via formal guarantees.

## Experiments
- **Environment/Benchmark**: StarCraft Multi-Agent Challenge (SMAC) combat scenarios — 3s5z, 3s_vs_4z, 2c_vs_64zg, 3s_vs_5z, 6h_vs_8z, 6z_vs_24zg; Predator-Prey (PP) and Cooperative Navigation (CN) on a 7×7 grid world with obstacles blocking line-of-sight communication. Lossy transmission simulated with Markov loss models (M_light, M_medium, M_heavy) fitted to real 802.11ac wireless traces.
- **Baselines**: QMIX (no communication), VBC (+QMIX/+VDN), SchedNet, AC (all-to-all communication variant of TMC without regularizers and without transmission limit), and Message-Dropout variants AC(light) and AC(heavy). TMC uses QMIX as mixing network on SMAC and VDN on PP/CN.
- **Evaluation metrics**: Game winning rate (with 95% confidence intervals, averaged over 15 training runs), communication overhead (average number of communicating agent pairs per timestep), and winning rate / normalized reward under light/medium/heavy transmission loss.

## Key Results
- TMC achieves on average 23% higher winning rate and up to 80% reduction in communication overhead vs. existing schemes; communication-based methods beat communication-free QMIX, and TMC+QMIX matches AC/VBC on easy SMAC maps and outperforms them on hard maps (3s_vs_5z, 6h_vs_8z, 6z_vs_24zg).
- On communication overhead (hard SMAC, no loss), TMC outperforms VBC and SchedNet by 1.3× and 3.7×, respectively.
- Under transmission loss, VBC, SchedNet, and AC degrade severely (VBC and SchedNet drop to 0% under heavy loss); TMC maintains the best winning rate across all three loss patterns. Analysis shows that with the smoothing penalty, 65% of lost messages have l2 distance < δ to the last delivered message (93% for messages within w_s), explaining TMC's loss robustness.
- On PP and CN, TMC+VDN achieves 1.24× and 1.35× higher reward and 3.2× and 2.9× lower communication overhead than the other approaches, respectively.

## Limitations & Future Work
- Robustness is empirical with no formal guarantees; effectiveness depends on hyperparameters (w_s, δ, λ_s, λ_r, β), which are tuned per scenario.
- Loss is modeled as a non-adversarial Markov channel process; adversarial communication attacks are not considered.
- The authors note dual-use/security concerns (e.g., misuse for controlling drones) as a flaw and future research direction.
- Suggested extensions: applying the TMC idea to other communication-dependent AI fields (e.g., federated learning) and to efficient communication patterns for Human-Computer Interaction.

## Relevance to Survey
This paper sits on the "communication robustness" line of robust MARL: rather than environment/model uncertainty or adversarial agents, it targets robustness to unreliable communication channels (transmission/packet loss) and message efficiency in cooperative CTDE value-decomposition MARL. It connects to the communication-learning line (CommNet, TarMAC, MAAC, SchedNet, VBC) and to message-robustness work such as Message-Dropout, and is a natural reference point for survey themes on succinct/efficient communication and fault/loss tolerance in MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work]_

"Given the success of centralized training and decentralized execution scheme [19, 9], the value function decomposition method has been proposed to improve agent learning performance. In Value-Decomposition Network (VDN) [33], the joint Q-value is deﬁned as the sum of the individual agent Q-values. More recently, QMIX [23] use a neural network with non-negative weights to estimate the joint Q-value using both individual Q-values and the global state variables. QTRAN [31] further removes the constraint on non-negative weights in QMIX, and provides a general factorization for the joint Q-value. However, these methods all disallow inter-agent communication."

"There has been extensive research [7, 32, 12, 5, 11, 13] on learning effective communication between the agents for performance enhancement of cooperative MARL. However, these methods have not considered quality and efﬁciency of inter-agent message exchange. Recently, the authors of [39] propose a technique to reduce communication overhead during the execution phase. However, these methods do not consider transmission loss, which limits their applicability in real settings. Kim et. al [14] proposes an efﬁcient training algorithm called Message-Dropout (MD). The authors demonstrate that randomly dropping some messages during the training phase can yield a faster convergence speed and make the trained model robust against message loss. However, in practice, the transmission loss pattern is always changing spatially and temporally [34]. Adopting a ﬁxed random loss pattern during training can not generalize to the intricate and dynamic loss pattern during execution. Also, MD incurs high communication overhead, which makes it less practical in real applications. In contrast, TMC enables the agents to transmit with minimal communication overhead in potentially lossy network environment, while still attaining a good performance."

> _[Introduction — on lack of communication and overfitting in value decomposition]_

"However, even though value function decomposition has demonstrated outstanding performance in solving simple tasks [33], it does not allow explicit information exchange between agents during execution phrase, which hinders its performance in more complex scenarios. In certain cases, some agents may overﬁt their strategies to the behaviours of the other agents, causing serious performance degradation [17, 18]."

> _[Introduction — on prior communication work and message redundancy]_

"Motivated by the drawbacks due to lack of communication, recent studies [13, 5, 11] have introduced inter-agent communication during the execution phase, which enables agents to better coordinate and react to the environment with their joint experience. However, while an extensive amount of work has concentrated on leveraging communication for better overall performance, little attention has been paid to the reliability of transmission channel and efﬁciency during the message exchange. Moreover, recent work has shown that the message exchange between agents tends to be excessive and redundant [39]."

> _[Section 4.4, Improvement on Messaging Reliability — on robustness against transmission loss]_

"Existing communication schemes (e.g., VBC [39], MAAC [11], etc) have not taken message loss into account when designing their communication protocols. These agents will lose the information in the messages when the transmission loss occurs. In contrast, TMC naturally mitigates the impact of message loss, as each delivered message can be used for at most ws timesteps, even if the subsequent messages are lost in the future."

### Cited references (resolved from the paper's bibliography)
- **[5]** Das, Gervet, Romoff, Batra, Parikh, Rabbat, Pineau. *TarMAC: Targeted multi-agent communication.* arXiv preprint arXiv:1810.11187, 2018.
- **[7]** Foerster, Assael, de Freitas, Whiteson. *Learning to communicate with deep multi-agent reinforcement learning.* NeurIPS 2016.
- **[9]** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[11]** Iqbal, Sha. *Actor-attention-critic for multi-agent reinforcement learning.* arXiv preprint arXiv:1810.02912, 2018.
- **[12]** Jiang, Lu. *Learning attentional communication for multi-agent cooperation.* NeurIPS 2018.
- **[13]** Kim, Moon, Hostallero, Kang, Lee, Son, Yi. *Learning to schedule communication in multi-agent reinforcement learning (SchedNet).* arXiv preprint arXiv:1902.01554, 2019.
- **[14]** Kim, Cho, Sung. *Message-dropout: An efficient training method for multi-agent deep reinforcement learning.* AAAI 2019.
- **[17]** Lanctot, Zambaldi, Gruslys, Lazaridou, Tuyls, Pérolat, Silver, Graepel. *A unified game-theoretic approach to multiagent reinforcement learning.* NeurIPS 2017.
- **[18]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* arXiv preprint arXiv:2003.03722, 2020.
- **[19]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[23]** Rashid, Samvelyan, de Witt, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* arXiv preprint arXiv:1803.11485, 2018.
- **[31]** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning.* arXiv preprint arXiv:1905.05408, 2019.
- **[32]** Sukhbaatar, Fergus, et al. *Learning multiagent communication with backpropagation (CommNet).* NeurIPS 2016.
- **[33]** Sunehag, Lever, Gruslys, Czarnecki, Zambaldi, Jaderberg, Lanctot, Sonnerat, Leibo, Tuyls, et al. *Value-decomposition networks for cooperative multi-agent learning (VDN).* arXiv preprint arXiv:1706.05296, 2017.
- **[34]** Tse, Viswanath. *Fundamentals of wireless communication.* Cambridge University Press, 2005.
- **[39]** Zhang, Zhang, Lin. *Efficient communication in multi-agent reinforcement learning via variance based control (VBC).* arXiv preprint arXiv:1909.02682, 2019.
