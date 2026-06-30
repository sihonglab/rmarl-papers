# 168. The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning

## Metadata
- **Title**: The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning
- **Authors**: Jan Blumenkamp, Amanda Prorok
- **Affiliation**: Department of Computer Science and Technology, University of Cambridge, United Kingdom
- **Venue**: CoRL 2020 (4th Conference on Robot Learning)
- **Link/arXiv**: arXiv:2008.02616v2 [cs.RO], 4 Nov 2020; code: https://github.com/proroklab/adversarial_comms

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks / adversarial (manipulative) inter-agent communication; self-interested agents sending false messages over a shared learnable communication channel
- **Method paradigm**: Graph Neural Networks (Aggregation GNNs), policy-gradient actor-critic (VPG/PPO) with centralized critic, emergent communication, post-hoc interpretability (white-box analysis)
- **Keywords**: Graph Neural Networks, Multi-Agent Reinforcement Learning, Adversarial Communication, Interpretability, Self-interested agents

## TL;DR
The paper presents a multi-agent learning model with individual (non-shared) rewards and a common differentiable communication channel, and shows that a single self-interested agent learns highly manipulative (adversarial) communication strategies—without being explicitly optimized for adversariality—that let it significantly outperform a cooperative team.

## Problem & Motivation
GNN-based explicit communication has enabled complex multi-agent coordination, but existing work assumes full cooperation toward a shared global reward. When agents have self-interested local objectives, the standard design models them as separate learning systems, which precludes a single differentiable communication channel and thus prohibits learning inter-agent communication strategies. The paper addresses this gap, asking whether non-cooperative agents can learn manipulative communication policies, positing that understanding how adversarial communication emerges is the first step toward methods that can defend against it in real-world situations.

## Robustness Setting
- **Threat model / uncertainty set**: A self-interested agent shares the same differentiable communication channel as a cooperative team. While maximizing only its own reward (disregarding others' rewards), it can learn to communicate erroneous information—lying about its state/observations—to mislead cooperative agents, especially when rewards are drawn from a finite pool or resources are in contention. No explicit adversarial objective is imposed; manipulation emerges from self-interest.
- **Setting**: mixed cooperative–competitive (a cooperative team plus one self-interested agent); decentralized execution with centralized critic (CTDE-style); partially observable stochastic game; online policy-gradient learning.

## Method
- Models the system as a partially observable stochastic game with per-agent local rewards Ri, local observations, and a time-varying communication topology Et. Inter-agent communication uses Aggregation Graph Neural Networks (AGNNs) that aggregate messages over multiple graph hops and remain decentralizable/locally executable.
- Generalizes the homogeneous AGNN to a heterogeneous formulation (Eq. 4) with per-agent filter taps, so different agents (or sub-groups) can have locally unique communication policies while remaining decentralizable.
- Cooperative learning: a modified Vanilla Policy Gradient with a centralized critic in which each agent's gradient reinforces actions (across all agents' policies) that increase agent i's advantage; Lemma 1 shows this converges to a local maximum of the sum of all agents' returns.
- Self-interested learning: after fixing the cooperative team's parameters θc, one agent is replaced by a self-interested agent; its policy gradient (Eq. 6) optimizes only its own parameters θn to maximize its own advantage An, leading to manipulative communication (Lemma 2).
- White-box analysis: an interpreter f⁻¹_ψ is trained to invert the cooperative encoder fνc (reconstruct local observations from messages), revealing whether messages are truthful (cooperative) or false (self-interested), quantified via mean Average Precision (mAP).

## Theoretical Contributions
- **Lemma 1**: with a compatible TD(1) critic, the cooperative policy gradient converges with probability one to a local maximum of the expected sum of all agents' returns (proof in Appendix A).
- **Lemma 2**: with a compatible TD(1) critic, the self-interested policy gradient converges with probability one to a local maximum of the expected return of the self-interested agent, affecting only θn (proof in Appendix A).
- Otherwise mostly empirical (the contribution is the model, algorithm, and empirical demonstration of emergent adversarial communication).

## Experiments
- **Environment/Benchmark**: Custom grid-world tasks: (1) coverage in non-convex environments (N = 6 agents), (2) coverage in split environments (N = 6 agents), (3) path planning (N = 16 agents). Three experiment types: purely cooperative team; introduction of one self-interested agent with the cooperative policy held fixed (with and without its communication); cooperative team re-adaptation. Implemented with a PPO variation, distributed training on Ray and RLlib.
- **Baselines**: Internal ablations/comparisons rather than external baselines—cooperative team with vs. without communication; self-interested agent with vs. without (adversarial) communication; re-adaptation condition.
- **Evaluation metrics**: Average return per agent group (cooperative C vs. self-interested SI) over 100 episodes (±1σ); white-box interpreter mean Average Precision (mAP) on the test set.

## Key Results
- Introducing a self-interested agent decreases the cooperative team's average performance; the loss is significant when adversarial communication is enabled, and the self-interested agent significantly outperforms the cooperative team.
- When communicating, the self-interested agent's performance improves by 128% for non-convex coverage, 229% for split coverage, and 112% for path planning (range 112%–229%).
- The white-box interpreter's mAP is much higher for cooperative agents than for the self-interested agent (e.g., 0.82 vs. 0.29 in non-convex coverage), indicating the self-interested agent learns a deviant encoding / sends false messages.
- After re-adaptation, the cooperative team recoups its loss to a level on par with the purely cooperative (with-communication) case, neutralizing the adversarial communication; adversarial communication only arises under resource contention (no difference when resources are non-shared).

## Limitations & Future Work
- The shared AGNN formulation is homogeneous unless explicitly generalized; the study uses one self-interested agent against a cooperative team rather than arbitrary mixtures.
- Adversarial communication is studied as an emergent phenomenon (no defense is proposed beyond showing re-adaptation can counter it); analysis is confined to grid-world coverage/path-planning tasks.
- Future work will address co-optimization schemes, the study of equilibria, and generalization to arbitrary proportions of cooperative vs. self-interested agents.

## Relevance to Survey
This paper sits on the "communication robustness / adversarial communication" line of robust MARL, complementing work on adversarial attacks and faulty/manipulative agents. It is distinctive in showing that adversarial communication can emerge purely from self-interest over a shared differentiable channel (no explicit adversarial objective), and in providing an interpretability tool to detect deceptive messages. It connects mixed cooperative-competitive MARL (e.g., MADDPG-style learning), GNN-based communication, and the broader theme of robustness to manipulative/Byzantine signaling, while explicitly framing understanding emergent adversarial communication as a prerequisite for defending against it.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — opening]_

"We briefly review work in cooperative and non-cooperative multi-agent reinforcement learning, with a focus on approaches that model communication between agents."

> _[Section 2, Related Work — "Cooperative multi-agent reinforcement learning"]_

"Cooperative multi-agent reinforcement learning. Cooperation enables agents to achieve feats together that no individual agent can achieve on its own. Yet independently learning agents perform poorly in practice [11], since agents' policies change during training, resulting in a non-stationary environment. Hence, the majority of recent work leans on joint learning paradigms [12, 13, 14, 15]. These approaches avoid the need for explicit communication by making strong assumptions about the visibility of other agents and the environment. Some other approaches use communication, but with a predetermined protocol [16, 17]."

"Early work on learning communication considers discrete communication, through signal binarization [6], or categorical communication emissions [18]. The former approaches demonstrate emergent communication among few agents; scaling the learning process to larger agent teams requires innovations in the structure of the learnt communication models. The approach in [19] presents a more scalable approach by instantiating a GNN-inspired construction for learning continuous communication. Other, more recent work demonstrates the use of GNNs for learning communication policies that lead to successful multi-agent coordination in partially observed environments [8, 7, 4]."

> _[Section 2, Related Work — "Non-cooperative multi-agent reinforcement learning"]_

"Non-cooperative multi-agent reinforcement learning. Most work on non-cooperative multi-agent systems does not model learnable communication policies, since the assumption is made that agent behaviors evolve as a function of consequences observed in the environment. Social dilemma problems represent one type of non-cooperative system, where the collectively best outcomes are not aligned with individualistic decisions. Descriptive results were obtained for sequential social dilemmas [20] and common-pool resource problems [21]. Other work focuses on the development of learning algorithms for non-cooperative multi-player games [22, 23]. Yet none of these approaches include dedicated communication channels between agents."

"More closely related to our work, the work in [24] presents a learning scheme for mixed cooperative-competitive settings. The approach enables speaker agents to output semantic information, which is, in turn, observed by listener agents. In contrast to our approach, this type of communication is not differentiable, and assumes time-invariant fully connected agent topologies. To date, there is a lack of work in non-cooperative multi-agent reinforcement learning with continuous differentiable communication."

> _[Introduction — on GNNs and learned communication]_

"In recent years, a range of approaches towards learning explicit communication were made [6, 7, 8, 9]. The key attribute of GNNs is that they operate in a localized manner, whereby information is shared over a multi-hop communication network through explicit communication with nearby neighbors only, hence resulting in fully decentralizable policies."

"One particularly promising approach leverages Graph Convolutional Neural Networks (GCNNs), which utilize graph convolutions to incorporate a graph structure into the learning process by concatenating layers of graph convolutions and nonlinearities [10, 4]. Recent work leverages GCNNs to automatically synthesize local communication and decision-making policies for solving complex multi-agent coordination problems [7, 8]. These learning approaches assume full cooperation, whereby all agents share the same goal of maximising a global reward. Yet there is a dearth of work that explores whether agents can utilize machine learning to synthesize communication policies that are not only cooperative, but instead, are non-cooperative or even adversarial."

### Cited references (resolved from the paper's bibliography)
- **[4]** A. Khan, E. Tolstaya, A. Ribeiro, V. Kumar. *Graph policy gradients for large scale robot control.* CoRL 2020 (PMLR v100).
- **[6]** J. Foerster, I. A. Assael, N. de Freitas, S. Whiteson. *Learning to communicate with deep multi-agent reinforcement learning.* NeurIPS (NIPS) 2016.
- **[7]** Q. Li, F. Gama, A. Ribeiro, A. Prorok. *Graph neural networks for decentralized multi-robot path planning.* IEEE/RSJ IROS 2020.
- **[8]** E. Tolstaya, F. Gama, J. Paulos, G. Pappas, V. Kumar, A. Ribeiro. *Learning decentralized controllers for robot swarms with graph neural networks.* CoRL 2020.
- **[9]** A. Prorok. *Graph neural networks for learning robot team coordination.* Federated AI for Robotics Workshop (IJCAI-ECAI/ICML/AAMAS) 2018.
- **[10]** F. Gama, E. Isufi, G. Leus, A. Ribeiro. *From graph filters to graph neural networks.* arXiv:2003.03777, 2020.
- **[11]** L. Matignon, G. J. Laurent, N. Le Fort-Piat. *Independent reinforcement learners in cooperative Markov games: a survey regarding coordination problems.* The Knowledge Engineering Review, 2012.
- **[12]** J. K. Gupta, M. Egorov, M. Kochenderfer. *Cooperative multi-agent control using deep reinforcement learning.* AAMAS 2017 (Springer).
- **[13]** T. Rashid, M. Samvelyan, C. S. de Witt, G. Farquhar, J. N. Foerster, S. Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[14]** J. N. Foerster, G. Farquhar, T. Afouras, N. Nardelli, S. Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[15]** S. Omidshafiei, J. Pazis, C. Amato, J. P. How, J. Vian. *Deep decentralized multi-task multi-agent reinforcement learning under partial observability.* ICML 2017.
- **[16]** D. Maravall, J. de Lope, R. Domínguez. *Coordination of communication in robot teams by reinforcement learning.* Foundations on Natural and Artificial Computation (Springer) 2011.
- **[17]** C. Zhang, V. Lesser. *Coordinating multi-agent reinforcement learning with limited communication.* AAMAS 2013.
- **[18]** I. Mordatch, P. Abbeel. *Emergence of grounded compositional language in multi-agent populations.* AAAI 2018.
- **[19]** S. Sukhbaatar, A. Szlam, R. Fergus. *Learning multiagent communication with backpropagation.* NeurIPS (NIPS) 2016.
- **[20]** J. Z. Leibo, V. Zambaldi, M. Lanctot, J. Marecki, T. Graepel. *Multi-agent reinforcement learning in sequential social dilemmas.* arXiv:1702.03037, 2017.
- **[21]** J. Perolat, J. Z. Leibo, V. Zambaldi, C. Beattie, K. Tuyls, T. Graepel. *A multi-agent reinforcement learning model of common-pool resource appropriation.* NeurIPS 2017.
- **[22]** J. Serrino, M. Kleiman-Weiner, D. C. Parkes, J. Tenenbaum. *Finding friend and foe in multi-agent games.* NeurIPS 2019.
- **[23]** P. Paquette, Y. Lu, S. S. Bocco, M. Smith, O.-G. Satya, J. K. Kummerfeld, J. Pineau, S. Singh, A. C. Courville. *No-press diplomacy: Modeling multi-agent gameplay.* NeurIPS 2019.
- **[24]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS (NIPS) 2017.
