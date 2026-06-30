# 68. Robust Multi-agent Communication Based on Decentralization-Oriented Adversarial Training

## Metadata
- **Title**: Robust Multi-agent Communication Based on Decentralization-Oriented Adversarial Training
- **Authors**: Xuyan Ma, Yawen Wang, Junjie Wang, Xiaofei Xie, Boyu Wu, Shoubin Li, Fanjiang Xu, Qing Wang
- **Affiliation**: State Key Laboratory of Intelligent Game, Beijing; Science and Technology on Integrated Information System Laboratory, Institute of Software, Chinese Academy of Sciences; University of Chinese Academy of Sciences; Singapore Management University
- **Venue**: IJCAI 2025 (inferred from anonymous submission URL "IJCAI2025-FB61"; arXiv preprint dated 30 Apr 2025)
- **Link/arXiv**: arXiv:2504.21278v1 [cs.MA]; code at https://anonymous.4open.science/r/IJCAI2025-FB61

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks (perturbation/masking of inter-agent communication channels and messages); robustness of multi-agent communication policies against learned adaptive attacks and heuristic attacks.
- **Method paradigm**: Adversarial training; learned adversary that identifies and masks critical communication channels; value-based CTDE (IGM principle, QMIX-style monotonic mixing); graph-based feature extraction; decentralization (anti-centralization) of communication structure.
- **Keywords**: multi-agent communication, robustness, adversarial training, decentralization, critical communication channels, MARL

## TL;DR
The paper proposes DMAC, a robustness-enhancing training method that uses a learned adversary (DMAC_Adv) to dynamically identify and mask critical communication channels and then adversarially retrains any learnable communication policy into a more decentralized structure, improving both robustness against communication attacks and normal-condition performance.

## Problem & Motivation
In cooperative MARL, communication is crucial for coordination, but training multi-agent communication is complex and existing methods frequently fall into local optima, concentrating communication in a limited number of channels and producing an unbalanced (over-centralized) structure. Drawing on decentralization theory in sociology, the authors note that an over-centralized network risks collapse if a few key nodes fail, whereas a decentralized network is more resilient under attack. Empirically (Figure 1), for T2MAC about 30% of channels account for nearly 70% of communication frequency, exposing such unbalanced policies to catastrophic breakdown when critical channels are damaged. The paper aims to train communication policies that adopt more decentralized, robust patterns without compromising task completion.

## Robustness Setting
- **Threat model / uncertainty set**: The adversary (DMAC_Adv) perturbs inter-agent communication by masking channels: a masking action a^c_{i,j} ∈ {0,1} closes the channel between target agents i, j (the observed message o_{i,j} becomes null when masked). The adversary's reward is dual-objective: maximize the reduction of the target MAS reward while minimizing the number of masked channels. At test time, robustness is evaluated against (1) a learned adaptive white-box attack (an RL attacker that minimizes the victim's reward, knowing the victim's reward) and (2) a heuristic attack (random messages within the valid message range).
- **Setting**: Cooperative MARL; value-based CTDE for the adversary; the target communication policy CP is learnable and the method is online retraining (adversarial training). The target joint policy π is fixed during adversary training; the communication policy CP is retrained on adversarial samples.

## Method
- Given a trained MARL joint policy π for n agents and a learnable communication policy CP (deciding whether agents communicate), DMAC enhances the robustness of CP by retraining it against adversarial samples that mask critical communication channels, forcing CP toward a decentralized pattern (Figure 2).
- The adversary DMAC_Adv models critical-channel identification as a Dec-POMDP G = <S, A^c, O, P, R^c, N, γ> with N = n(n−1)/2 masking agents; each masking agent learns policy π^c_{i,j}: h_{i,j} → a^c_{i,j} deciding whether to mask channel (i, j). Masking sets the observed message to null (Eq. 1). The objective maximizes an adversary reward r̂ inversely related to the target reward R and the mask count R_m, weighted by w1, w2 (Eq. 2).
- Feature extraction: target agents and their interactions are modeled as an undirected graph (vertices = agents with properties such as location, speed, health; edge weights = inter-agent distance, computed per environment, e.g., Euclidean distance in StarCraft II, grid count in Traffic Junction). Each vertex embedding e_v is computed by weighted neighbor aggregation (Eq. 3), and the per-agent feature is h_i = o_i ⊕ e_i.
- Architecture and training: DMAC_Adv has a masking-agent policy network π^c (learning individual values Q(a^c_{i,j}, h_{i,j})) and a critic network C learning the centralized value Q_tot, following the Individual-Global-MAX (IGM) principle (Eq. 4). The critic weights ω are constrained non-negative to satisfy IGM (Eq. 5), and the mixing can be replaced by VDN, QPLEX, or QTRAN. Training minimizes a TD loss (Eq. 6). The trained adversary then generates adversarial samples used to retrain CP, reducing reliance on critical channels and yielding decentralization (Algorithm 1).

## Theoretical Contributions
None / mostly empirical. The method relies on the IGM principle and value-decomposition (VDN/QPLEX/QTRAN) constructions from prior work; no new convergence, sample-complexity, or certified-robustness guarantee is proven in the text.

## Experiments
- **Environment/Benchmark**: Four multi-agent benchmarks — StarCraft Multi-Agent Challenge (SMAC, map 1c3s5z, 9 agents), Multi-Agent Particle Environments: Cooperative Navigation (CN, 7 target agents) and Predator Prey (PP, 8 target agents), and Traffic Junction (TJ, 10 target agents).
- **Baselines**: AME (certifiable defense via message-ensemble of randomly ablated message sets) and R-MACRL (defense via two-stage message refactoring/filter). Two target communication policies are enhanced: T2MAC and I2C.
- **Evaluation metrics**: Task completion / win rate under (1) learned adaptive attack and (2) heuristic attack, plus win rate under normal conditions; for decentralization, the High/Low/Average/Standard-Deviation of per-channel communication frequency (lower SD = more decentralized) and communication cost.

## Key Results
- Robustness (Table 1): Against the learned adaptive attack, DMAC improves T2MAC win rate by 47.9%–81.9% and I2C by 54.4%–99.0% across the four tasks vs. baselines; against the heuristic attack, T2MAC improves 37.9%–90.5% and I2C 38.3%–117.7%. Example: in SC, T2MAC under learned attack drops to 27.8% but reaches 60.4% with DMAC (original normal win rate 81.2%).
- Performance under normal conditions (Table 2): DMAC also yields the highest win rate among methods (e.g., SC T2MAC: 81.2% → 83.7% with DMAC, vs. 82.2% AME and 80.9% R-MACRL).
- Decentralization (Table 3, Figure 5): DMAC reduces the standard deviation of per-channel communication frequency (e.g., SC T2MAC SD 14.0 → 9.0), producing a more uniform/decentralized communication structure without much increase in communication cost (and sometimes reducing it).

## Limitations & Future Work
- Not explicitly stated as a dedicated section. The method targets robustness of communication policies specifically and assumes the underlying joint policy π is already trained and fixed; further evaluation details (e.g., critical-channel identification accuracy, ablation study) are deferred to the appendix. No analysis of computational overhead of training N = n(n−1)/2 masking agents at scale, or guarantees beyond empirical results. Future work is not specified in the main text.

## Relevance to Survey
This paper sits on the "communication robustness" line of robust MARL, specifically defending learnable inter-agent communication against adversarial channel/message attacks. It connects the adversarial-training paradigm ("fighting fire with fire," analogous to robust adversarial RL) with a structural objective (decentralization) and relates to attack works (Tu et al.; VSA) and defense works (AME; R-MACRL; Gaussian-process message filtering). It is a useful empirical reference for robustness-via-adversarial-retraining and for the sub-theme of communication-attack defenses in cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Communicative Multi-Agent Reinforcement Learning (CMARL)"]_

"There has been extensive research on encouraging communication between agents to improve performance on cooperative or competitive tasks. A communication policy defines how to decide whether to communicate with potential communicators for the purpose of message transportation [Zhu et al., 2024]. Communication policies can be predefined or learned. Early communication policies used full-connection communication [Sukhbaatar et al., 2016b; Das et al., 2019b; Pesce and Montana, 2020], where each pair of agents would be connected and transmit messages in a broadcast manner. Subsequent predefined partial communication [Jiang et al., 2020; Zhang et al., 2019] causes each agent communicating with a limited number of agents, rather than all others. In recent years, learning to determine how to build communication structures between agents has provided the ability to generalize to more scenarios [Sun et al., 2024; Meng and Tan, 2024], and it has become increasingly popular because of its flexibility. Learnable communication policies is divided into individual control [Ding et al., 2020; Mao et al., 2020] and global control [Kim et al., 2019; Liu et al., 2020]. In individual control, each agent actively and individually decides whether to communicate with other agents. On the contrary, global control constructs a globally shared communication policy which can endow more precise control of communication links between agents."

> _[Section 2, Related Work — "Adversarial Attacks and Defenses in CMARL"]_

"Recently, the existence of adversarial communication in MARL has attracted increasing attention. For the adversarial attack of communication, much of the work has focused on directly attacking the victim by perturbing with the designated victim's observations or messages. Tu et al. [Tu et al., 2021] trained an attacker to learn how to generate adversarial perturbation and add them as noise to the victim agent's message. VSA [Ma and Li, 2023] constructed an attacker which generates adversarial perturbations on the received communication messages by disturbing its controlled malicious agent to make non-optimal actions. These attack methods often select the victim communication channel randomly or based on rules, resulting in inefficiency or lack of flexibility. As for the defense method, AME [Sun et al., 2023] proposed a defense method by constructing a message-ensemble policy that aggregates multiple randomly ablated message sets. [Mitchell et al., 2020] adopted a Gaussian Process-based probabilistic model to compute the posterior probabilities that whether each partner is truthful to achieve robust communication. To achieve robust communication, a Gaussian Process-based probabilistic model [Mitchell et al., 2020] was adopted to compute the posterior probabilities that whether each partner is truthful. R-MACRL [Xue et al., 2022] learned an anomaly detector and a message reconstructor to recover the true messages, to maintain multi-agent coordination under message attacks. However, these methods often add extra processing to the abnormal messages without really adjusting the existing communication policies."

### Cited references (resolved from the paper's bibliography)
- **[Zhu et al., 2024]** Zhu, Dastani, Wang. *A survey of multi-agent deep reinforcement learning with communication.* AAMAS 2024.
- **[Sukhbaatar et al., 2016b]** Sukhbaatar, Szlam, Fergus. *Learning multiagent communication with backpropagation.* NeurIPS 2016.
- **[Das et al., 2019b]** Das, Gervet, Romoff, Batra, Parikh, Rabbat, Pineau. *TarMAC: Targeted multi-agent communication.* ICML 2019.
- **[Pesce and Montana, 2020]** Pesce, Montana. *Improving coordination in small-scale multi-agent deep reinforcement learning through memory-driven communication.* Machine Learning, 2020.
- **[Jiang et al., 2020]** Jiang, Dun, Huang, Lu. *Graph convolutional reinforcement learning.* ICLR 2020.
- **[Zhang et al., 2019]** Zhang, Zhang, Lin. *Efficient communication in multi-agent reinforcement learning via variance based control.* NeurIPS 2019.
- **[Sun et al., 2024]** Sun, Zang, Li, Li, Xu, Wang, Zheng. *T2MAC: Targeted and trusted multi-agent communication through selective engagement and evidence-driven integration.* AAAI 2024.
- **[Meng and Tan, 2024]** Meng, Tan. *PMAC: Personalized multi-agent communication.* AAAI 2024.
- **[Ding et al., 2020]** Ding, Huang, Lu. *Learning individually inferred communication for multi-agent cooperation.* NeurIPS 2020.
- **[Mao et al., 2020]** Mao, Zhang, Xiao, Gong, Ni. *Learning agent communication under limited bandwidth by message pruning.* AAAI 2020.
- **[Kim et al., 2019]** Kim, Moon, Hostallero, Kang, Lee, Son, Yi. *Learning to schedule communication in multi-agent reinforcement learning.* ICLR 2019.
- **[Liu et al., 2020]** Liu, Wang, Hu, Hao, Chen, Gao. *Multi-agent game abstraction via graph attention neural network.* AAAI 2020.
- **[Tu et al., 2021]** Tu, Wang, Wang, Manivasagam, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[Ma and Li, 2023]** Ma, Li. *Grey-box adversarial attack on communication in multi-agent reinforcement learning.* AAMAS 2023.
- **[Sun et al., 2023]** Sun, Zheng, Hassanzadeh, Liang, Feizi, Ganesh, Huang. *Certifiably robust policy learning against adversarial multi-agent communication.* ICLR 2023.
- **[Mitchell et al., 2020]** Mitchell, Blumenkamp, Prorok. *Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication.* CoRR abs/2012.00508, 2020.
- **[Xue et al., 2022]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Misspoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* AAMAS 2022.
