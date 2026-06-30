# 64. Robust Multi-Agent Communication With Graph Information Bottleneck Optimization

## Metadata
- **Title**: Robust Multi-Agent Communication With Graph Information Bottleneck Optimization
- **Authors**: Shifei Ding, Wei Du, Ling Ding, Jian Zhang, Lili Guo, Bo An
- **Affiliation**: China University of Mining and Technology (School of Computer Science and Technology), Xuzhou, China; Tianjin University (College of Intelligence and Computing); Nanyang Technological University (School of Computer Science and Engineering), Singapore
- **Venue**: IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), Vol. 46, No. 5, May 2024
- **Link/arXiv**: Digital Object Identifier 10.1109/TPAMI.2023.3337534

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks on GNN-based multi-agent communication — adversarial attacks and noise perturbations on the graph topological structure (adjacency matrix A, edge addition/deletion) and the agent feature embeddings (node features H)
- **Method paradigm**: Graph Information Bottleneck (GIB) optimization; information-theoretic regularizers (mutual-information minimization/maximization with variational bounds); graph attention network (GAT) communication; value function decomposition (VDN/QMIX/QPLEX) under CTDE
- **Keywords**: Graph neural network, multi-agent reinforcement learning, graph information bottleneck optimization, communication learning, adversarial robustness

## TL;DR
The paper proposes MAGI, a robust multi-agent communication mechanism that extends the graph information bottleneck principle to GNN-based MACRL: two information-theoretic regularizers learn a minimal-sufficient message representation (maximizing MI with action selection while minimizing MI with the agent feature/topology), yielding communication that stays robust under adversarial attacks and noise on both graph structure and agent features.

## Problem & Motivation
GNN-based multi-agent communicative RL (MACRL) treats agents and channels as nodes and edges in a graph and aggregates neighbor information for action coordination, but it is susceptible to adversarial attacks and noise perturbations on agent features and topological structure, and message representations can carry useless information that negatively affects action selection. The performance of MACRL methods degrades under such attacks, which puts practical applications (e.g., multi-agent autonomous driving) at risk. How to achieve robust communication under perturbations has been largely neglected. The paper rethinks what an "optimal" communication message representation is — one that is sufficient and minimal for action selection per the Information Bottleneck principle — and addresses two challenges in extending IB to GNN-based MACRL: the discrete (hard-to-optimize) topological structure information, and the non-i.i.d. nature of graph-structured agent features that violates standard IB assumptions.

## Robustness Setting
- **Threat model / uncertainty set**: Adversarial perturbations and noise applied to the input data D = (A, H). Feature perturbation: independent Gaussian noise η·φ·ε (ε ∼ N(0,1), φ the reference amplitude, η the feature noise ratio) added to agent features H. Structural perturbation: adding/deleting edges via projected gradient descent (PGD) on the adjacency matrix A. Additional stronger attacks evaluated: IG-JSMA (perturbs both features and edges) and GUA (flips connections between anchor agents). Adversarial attack defined (after Sun et al.) as a small modification of D that is imperceptible but sharply degrades the downstream (action selection) task.
- **Setting**: Cooperative (fully cooperative, discrete action); CTDE (centralized training with decentralized execution), modeled as a Dec-POMDP; online value-decomposition MARL. Explicitly not applicable to continuous-action or mixed competitive-cooperative scenarios.

## Method
- Model the multi-agent system as a graph G = (V, E, H) with adjacency matrix A; input feature data D = (A, H). Extract agent-level message representations M_H from D so that they facilitate action selection Y.
- MAGI objective: minimize MAGI_β(D, Y; M) ≜ [−I(Y; M) + β·I(D; M)], i.e., maximize the mutual information between message and optimal action while minimizing the MI between message and feature/topology data, producing a minimal-sufficient representation.
- Introduce a local-dependence assumption on graph-structured agent features (an agent's feature is independent of others' given neighbors within certain hops) to restrict the message space Ω and make optimization tractable; iterate message representations hierarchically through GNN layers, with each layer = one round of message exchange. Reduce the objective to optimizing two local series of distributions P(M_H^l | M_H^{l-1}, M_A^l) and P(M_A^l | M_H^{l-1}, A).
- Because the MI terms are intractable, derive variational bounds: a lower bound on I(Y; M_H^L) (reduced to a cross-entropy loss for action prediction) and an upper bound on I(D; M_H^L) decomposed into per-layer structural (AIB_l) and feature (HIB_l) regularizers, instantiated with categorical (uniform) and mixture-of-Gaussian variational distributions.
- Implement with GAT as the GNN: refine the graph structure M_A^l via attention weights (sample neighbors with categorical distributions) and refine message representation M_H^l by sum-pooling neighbors and sampling from a Gaussian. Concatenate message m_i with local history τ_i for the local action-value Q_i, and feed Q_i of all agents to a mixing network (VDN/QMIX/QPLEX) for Q_tot. Total loss L = L_TD + λ·L_IB (λ = 0.1).

## Theoretical Contributions
- Derivation of variational lower/upper bounds for the two intractable mutual-information terms in the MAGI objective (Eqs. 3–6, 8–11), enabling a tractable IB-style training objective for GNN-based communication.
- Conditions on the index sets S_H, S_A guaranteeing the Markovian conditional independence between M_H^L and D used in the upper bound on I(D; M_H^L).
- Otherwise mostly empirical; no convergence, sample-complexity, or certified-robustness guarantees are claimed.

## Experiments
- **Environment/Benchmark**: StarCraft II Multi-Agent Challenge (SMAC) — scenarios MMM2, MMM3 (super-hard), 1o2r vs 4r, 2c3s5z, 8m vs 9m (with the ally vision range reduced from 9 to 2 to make coordination harder); and MAgent (Battle scenario, hundreds of agents, default K = 40 allies vs Z = 24 enemies, varied K ∈ {20, 30, 40, 50}).
- **Baselines**: QMIX, TarMAC, MAGIC (TarMAC, MAGIC, and MAGI all use GAT as the GNN). Methods with a "+A" suffix denote evaluation under adversarial attack. Ablation variants: MAGI-VD (no value-decomposition component), MAGI-IB (no IB component), MAGI w/ IBr1, MAGI w/ IBr2; integrations MAGI(VDN), MAGI(QPLEX).
- **Evaluation metrics**: Win rate (SMAC), mean reward, kill number, kill-death rate (Battle), learning curves with 95% confidence intervals; robustness measured by performance under Gaussian noise (η ∈ {0.5, 1.0, 1.5, 2.0, 2.5}) + PGD edge attacks, and under IG-JSMA and GUA attacks; sensitivity to λ ∈ {0.05, 0.10, 0.15}.

## Key Results
- Under adversarial attacks and noise (η = 1.5, GN+PGD), MAGI significantly outperforms all baselines across SMAC scenarios; MAGI+A shows only slight degradation versus MAGI, whereas TarMAC+A and MAGIC+A degrade significantly, showing existing GNN-based MACRL is susceptible to attacks while MAGI is robust.
- On the Battle scenario MAGI achieves the best kill number, kill-death rate, and mean reward; MAGI-trained agents learn coordination behaviors (e.g., encircling) under perturbation, while baselines fall back to sub-optimal behaviors (e.g., gathering in a corner).
- Scalability holds: MAGI is best across K ∈ {20, 30, 40, 50}. Ablations show both IB regularizers contribute (removing IB causes the largest drop / highest variance), the VD module further aids coordination, and MAGI generalizes across attacks (best under IG-JSMA and GUA) and value-factorization choices (MAGI(VDN), MAGI(QPLEX) beat their base methods).

## Limitations & Future Work
- The method is specifically designed for discrete-action, fully cooperative scenarios; it is not applicable to continuous-action environments or mixed competitive-cooperative scenarios.
- Future work aims to develop a more versatile and robust communication model adaptable to a broader range of scenarios, and to apply the method to real-world large-scale multi-agent systems.

## Relevance to Survey
This paper sits on the "communication robustness / adversarial attacks on communication" line of robust MARL, specifically defending GNN-based MACRL against perturbations of both graph topology and agent features — a threat surface broader than prior message-level defenses (e.g., Mitchell et al., Xue et al., Sun et al.). It connects the information-bottleneck / minimal-sufficient-representation method line (NDQ, MASIA, the IB communication approach) with CTDE value-decomposition methods (VDN/QMIX/QPLEX), positioning robust certified/defended communication as an instance of representation-level robustness rather than worst-case game-theoretic robustness.

## Related Work (verbatim excerpts from the paper)

> _[Section II.A, Related Work — Multi-Agent Communicative Reinforcement Learning]_

"Multi-agent communicative reinforcement learning methods aim at achieving consensus and cooperation of multiple agents through communication learning. Agents need to enhance action coordination by learning to communicate with other agents and process the message representations they receive. Previous MACRL methods can be divided into two main categories. The first category focuses on generating meaningful messages for the message senders. One straightforward approach is to treat raw local observations or the local information history as messages. For example, NDQ [11] aims to generate minimal messages for different teammates, allowing them to learn decomposable value functions. NDQ optimizes the message generator utilizing two information-theoretic regularizers to achieve expressive communication."

"The second category of work aims to efﬁciently extract the most useful messages at the receiver's end. For example, MASIA [12] explicitly addresses the optimization of multiple received messages and introduces two self-supervised representation objectives. These objectives aim to make the received information representation both abstract of the true states and predictive of the multi-step future information. TarMAC [15] achieves targeted communication through a soft-attention mechanism, in which the sender broadcasts a key encoding the agents' properties, and the receiver processes all received messages for a weighted sum of messages to make decisions."

"The most relevant works to the idea of this paper are NDQ [11] and MASIA [12], both of which aim to achieve efﬁcient communication. NDQ aims to ensure communication is both expressive (effectively reducing the uncertainty of action-value functions of agents) and succinct (only sending necessary and useful information). MASIA focuses on ensuring communication is both compact (high information density) and sufﬁcient (containing a rich amount of information). Our method is designed to ensure communication is sufﬁcient (efﬁciently facilitating the action selection of agents), minimal (not containing unnecessary information), and robust (not vulnerable to adversarial attacks and noise). Different from NDQ and MASIA, we aim at the redundancy and efﬁciency issue of communication information in the GNN-based MACRL methods and consider the robustness of these methods, which NDQ and MASIA do not pay attention to."

> _[Section II.B, Related Work — GNN-Based MACRL]_

"In contrast to the above methods, GNN-based MACRL methods generally utilize neighboring communication architecture. In this architecture, agents communicate with neighbors simultaneously, which can reduce communication costs. Meanwhile, the powerful information aggregation ability and representation learning capability provided by GNN can make GNN-based MACRL methods suitable for large-scale agent scenarios. DGN [22] ﬁrst extends GNN to MACRL methods and adopts neighboring architecture, where multiple rounds of communications are utilized to widen the receptive ﬁeld. NerveNet [23] utilizes GNN to represent the policy of the agent and propagate information over the graph structure of agents and then predicts actions for the agents."

"HAMA [24] adopts a hierarchical GNN based on a pre-deﬁned hierarchical graph and attention mechanism to facilitate agents to capture interrelations. However, the predeﬁned ﬁxed grouping scheme adopted by HAMA restricts its adaptability in dynamic settings. GA2NET [25] adopts a two-stage attentional mechanism to model the multi-agent setting, which can infer whether there is interaction between two agents and then evaluate the importance of interaction. TarMAC [16] utilizes GNN with a soft attention mechanism to learn whom to receive messages and what messages to pass. MAGIC [15] presents an attentional GNN to operate on the constructed graph for multiple rounds of communication, which can tackle the issue of when to communicate."

"Recent GNN-based MACRL methods have successfully promoted action coordination by efﬁcient communication learning, which aggregates information on agent features and models interactions among agents by diverse graph neural networks. Despite signiﬁcant progress in GNN-based MACRL, if these methods encounter adversarial attacks and noise perturbations, multi-agent action coordination will rapidly disintegrate. The issue that how to achieve robust communication under adversarial attacks and noise perturbations has been largely unstudied. Our work intends to provide a promising way to address this, which extends the graph information bottleneck optimization to GNN-based MACRL methods."

> _[Section II.C, Related Work — Value Function Decomposition]_

"For effectiveness and scalability in multi-agent environments, CTDE has become a prevalent MARL paradigm. Value function factorization methods further explore the CTDE paradigm based on the Individual-Global-Max (IGM) principle [9], which is an essential assumption that ensures consistency between local greedy action selections and joint action selections. VDN [7] adopts linear value factorization to ensure the sufﬁcient condition for the IGM principle. Due to its excellent scalability, this simple linear architecture has become very prevalent in MARL and has inspired many subsequent approaches. QMIX [8] presents a monotonic mixing network to enhance the expressiveness of the decomposed function class. QTRAN [6] aims at realizing the entire IGM function class, however, its proposed goal is computationally intractable and necessitates two additional soft regularizers to approximate IGM, where the strict IGM guarantee is not guaranteed. QPLEX [9] extends the IGM principle into the dueling network architecture, however, it has potential limitations in terms of scalability. Our work utilizes different value decomposition methods in the proposed MARL framework to demonstrate the ﬂexibility of the proposed method."

> _[Section II.E, Related Work — Adversarial Attacks and Defenses in MACRL]_

"Robust single-agent RL has been investigated from different perspectives [31], and recently, the issue of adversarial attacks and defenses in MACRL has gained signiﬁcant attention. Researchers have been exploring various approaches to achieve robust communication in the face of adversarial attacks. Tu et al. [32] focus on exploring adversarial attacks speciﬁcally in the multi-agent setting where perturbations are introduced to learned intermediate representations. Mitchell et al. [33] propose a method that utilizes a Gaussian Process-based probabilistic module to calculate posterior probabilities, determining the truthfulness of each partner. Xue et al. [34] propose a two-stage message ﬁlter that involves learning an anomaly detector and a message reconstructor to recover the true messages. They employ two populations of defenders and attackers for training, aiming to improve the generalizability of defense mechanisms. Sun et al. [35] introduce the ﬁrst certiﬁable defense in MARL against communication attacks, which considers a particularly strong threat model in which half of communication messages can be arbitrarily compromised. Nevertheless, these previous methods generally focus on the malicious perturbations on the received message itself, but the adversarial attacks can also be the perturbations on the communication structure and agent feature, which has not been paid attention to in the previous work. This paper tries to solve this problem by using the GNN-based MACRL methods as a starting point."

### Cited references (resolved from the paper's bibliography)
- **[6]** Son, Kim, Kang, Hostallero, Yi. *Learning to factorize with transformation for cooperative multi-agent reinforcement learning (QTRAN).* ICML 2019.
- **[7]** Sunehag et al. *Value-decomposition networks for cooperative multi-agent learning (VDN).* AAMAS 2020.
- **[8]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[9]** Wang, Ren, Liu, Yu, Zhang. *QPLEX: Duplex dueling multi-agent Q-learning.* ICLR 2019.
- **[11]** Wang, Wang, Zheng, Zhang. *Learning nearly decomposable value functions via communication minimization (NDQ).* arXiv:1910.05366, 2019.
- **[12]** Guan et al. *Efficient multi-agent communication via self-supervised information aggregation (MASIA).* NeurIPS 2022.
- **[15]** Niu, Paleja, Gombolay. *Multi-agent graph-attention communication and teaming (MAGIC).* AAMAS 2021.
- **[16]** Das et al. *TarMAC: Targeted multi-agent communication.* ICML 2019.
- **[22]** Jiang, Dun, Lu. *Graph convolutional reinforcement learning for multi-agent cooperation (DGN).* ICLR 2018.
- **[23]** Wang, Liao, Ba, Fidler. *NerveNet: Learning structured policy with graph neural networks.* ICLR 2018.
- **[24]** Ryu, Shin, Park. *Multi-agent actor-critic with hierarchical graph attention network (HAMA).* AAAI 2020.
- **[25]** Liu, Wang, Hu, Hao, Chen, Gao. *Multi-agent game abstraction via graph attention neural network (GA2NET).* AAAI 2020.
- **[31]** Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[32]** Tu, Wang, Sivabalan, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[33]** Mitchell, Blumenkamp, Prorok. *Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication.* arXiv:2012.00508, 2020.
- **[34]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* arXiv:2108.03803, 2021.
- **[35]** Sun et al. *Certifiably robust policy learning against adversarial multi-agent communication.* ICLR 2022.
