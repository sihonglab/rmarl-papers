# 169. Communication-robust multi-agent learning by adaptable auxiliary multi-agent adversary generation

## Metadata
- **Title**: Communication-robust multi-agent learning by adaptable auxiliary multi-agent adversary generation
- **Authors**: Lei Yuan, Feng Chen, Zongzhang Zhang, Yang Yu
- **Affiliation**: National Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, China; Polixir Technologies, Nanjing, China
- **Venue**: Frontiers of Computer Science 2024, 18(6): 186331
- **Link/arXiv**: https://doi.org/10.1007/s11704-023-2733-5

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks / message perturbation in cooperative MARL (noise or hostile adversarial perturbations injected into inter-agent message channels)
- **Method paradigm**: Adversarial training; auxiliary adversary generation modeled as a cooperative MARL attack problem; population-based / evolutionary learning (Quality-Diversity); minimax-style alternating training; value decomposition (QMIX-style) for the attacker; actor-critic (MATD3)
- **Keywords**: multi-agent communication, adversarial training, robustness validation, reinforcement learning, attacker population, evolutionary learning

## TL;DR
The paper proposes MA3C (Multi-Agent Auxiliary Adversaries Generation for robust Communication), which models message-channel attacks as a cooperative MARL problem and trains an evolutionary, diversity-optimized attacker population alternately against the ego communication system to obtain a communication-robust cooperative policy.

## Problem & Motivation
Communication promotes coordination in cooperative MARL, but most existing methods focus only on communication efficiency and assume training and testing occur in similar/identical environments, ignoring policy drift caused by noise or hostile attacks. Deep networks are vulnerable to adversarial perturbations, so message channels under noise or attack can cause the system to crash, making communication robustness an emergent and severe issue. The communication-robustness problem is harder than single-agent or single-channel cases because, for N fully connected agents, there are N×(N−1) message channels, so a single attacker's action space grows quadratically with the number of agents; prior works rely on strong assumptions (e.g., identical perturbation on default channels, or only a limited number of agents receiving heuristic noise) to avoid this. The paper aims to design a robust communication policy that tolerates every channel being perturbed at different degrees at any time.

## Robustness Setting
- **Threat model / uncertainty set**: Auxiliary message adversaries add additive perturbations ξ to the messages received by each agent, transforming m into m̂ = m + ξ, where ξ = π̂(o). Perturbations are bounded to a set B (e.g., a p-norm ball B = { m̂ | ‖m − m̂‖_p = ε }) with magnitude ε and norm type p; in practice a 1-norm ball is used for most experiments (a discrete {ε, −ε} variant for Hallway). The attacker reward is the opposite of the ego reward (R̂ = −R). The attacker action space has dimension N×(N−1)×d_comm and is decomposed across N virtual agents, each responsible for the (N−1)·d_comm channels of one sender.
- **Setting**: Cooperative (fully cooperative Dec-POMDP with Communication, Dec-POMDP-Comm); CTDE (Centralized Training, Decentralized Execution); online; value-based ego system (deep Q-learning), MATD3 actor-critic for the attacker.

## Method
- **Message channel level attacking**: Model the attacker as a cooperative multi-agent attack problem with N virtual agents that together perturb all N×(N−1) channels, satisfying "comprehensiveness" (consider all channels) and "specificity" (perturb each agent's received messages distinctly). Decomposing the joint action space (motivated by QMIX) makes the attacker action dimension grow linearly rather than quadratically with N.
- **Attacker optimization (MATD3)**: Extend TD3 to a multi-agent setting with a centralized critic (similar to COMA); maintain two Q-networks with target networks, train via clipped double-Q TD targets, and optimize actors via the deterministic policy gradient.
- **Attacker population optimization**: Instead of one attacker (which causes ego-system over-fitting), maintain a fixed-size population and force the ego system to perform well against all attackers. Optimize population diversity using a trajectory representation z_j obtained from a transformer-based trajectory encoder trained with a forward-prediction loss; attacker distance is measured in this representation space. Population is updated via alternating evolution (MATD3 updates of selected instances) and selection using a FIFO queue, distance threshold, and attack-performance comparison.
- **Robust communication and training**: Alternately train the ego system (uniformly sampling an attacker per episode, rolling out, and updating from the buffer — equivalent to adversarial training against the whole population) and update the population against the latest ego system, iteratively enhancing both (Algorithms 1 and 2).

## Theoretical Contributions
None / mostly empirical. The work is primarily empirical; the formulation casts attacker learning as maximizing a discounted return with reward R̂ = −R and uses Quality-Diversity / population-based learning, but no convergence, sample-complexity, equilibrium-existence, or certified-radius guarantees are claimed.

## Experiments
- **Environment/Benchmark**: Hallway (two instances: Hallway-6×6 and Hallway-4×5×9), StarCraft Multi-Agent Challenge (SMAC) maps 1o_2r_vs_4r and 1o_10b_vs_1r, a newly created environment Gold Panner (GP-4r and GP-9r), and Traffic Junction (TJ). Applied on top of three communication methods: Full-Comm, NDQ, and TarMAC.
- **Baselines**: Vanilla (no adversarial training), Noise Adv. (adversarial training with random noise), Instance Adv. (single attacker with a historical pool, i.e., no-population ablation), MA3C w/o div. (variant of RAP, no explicit diversity), and AME (message-ensemble defense). Additional attacker-learning comparisons: TD3 (single-agent attacker) and Random Noise.
- **Evaluation metrics**: Success/win rate (mean ± standard deviation over five independent runs) under three test modes — Normal (no attack), Random noise, and Aggressive Attackers (unseen trained attackers); attacker attack ability; generalization to unseen perturbation ranges (zero-shot); fine-tuning transfer to larger perturbation ranges; parameter sensitivity; training-efficiency (time, CPU memory, GPU memory).

## Key Results
- Under Aggressive Attackers, MA3C consistently outperforms baselines; e.g., on Hallway-4×5×9 Vanilla drops to 0.00 success and AME to 0.00, while MA3C reaches 0.98; on GP-9r MA3C reaches 0.76 vs. AME 0.00.
- The diversity mechanism helps: MA3C generally beats MA3C w/o div. (RAP-style, no explicit diversity), and population beats single-attacker Instance Adv.; AME degrades badly on GP where specific channels are vital.
- MA3C generalizes to unseen/larger perturbation ranges (highest win rate across ranges in SMAC-1o_2r_vs_4r) and transfers to larger ranges after fine-tuning with a few samples; the transformer trajectory encoder reduces the aggressive-attack performance drop (e.g., 7% for MA3C vs. 19% for ordinary encoder and 21% for MA3C w/o div. on GP-4r). Cost: substantially more training time and GPU memory (e.g., GP-4r: MA3C 5d 2h 56m vs. Full-Comm 9h 9m).

## Limitations & Future Work
- Only a limited/bounded perturbation set is considered; developing an autonomous paradigm (e.g., curriculum learning) to find the communication-ability boundary is left as future work.
- MARL communication under open-environment scenarios is challenging and remains future work.
- The inclusion of auxiliary adversaries (maintaining and evolving a population) brings substantial extra training overhead (time and GPU memory); improving training efficiency via code and algorithm-design optimization is future work.

## Relevance to Survey
This paper sits on the "communication robustness in cooperative MARL" line of the robust MARL landscape, complementing other perturbation types (observation perturbation, action perturbation, model/reward uncertainty). It connects the adversarial-training / auxiliary-adversary paradigm with population-based and Quality-Diversity evolutionary learning, and explicitly contrasts itself with single-agent robust RL, R-MADDPG (model uncertainty / robust Nash equilibrium), M3DDPG (opponent-policy robustness), ensemble defenses (AME), and other cooperative-MARL robustness works (ARTS, RADAR), making it a useful node linking communication-attack threat models to adversarial-population methods.

## Related Work (verbatim excerpts from the paper)

### Multi-agent communication
> _[Section 2, Related work]_

"Multi-agent communication Communication is a significant topic in MARL under partial observability, which typically studies when to send what messages to whom [1]. The early relevant works mainly consider combining communication with any existing MARL methods, using broadcasted messages to promote coordination within a team [6] or designing end-to-end training paradigms that update the message network and policy network together with the back-propagated gradients [22]. To improve communication in complex scenarios, researchers investigate the efficiency of communication from multiple aspects like designing positive listening protocol [23,24]. To avoid redundant communication, some works employ techniques such as gate mechanisms [2,4,25] to decide whom to communicate with, or attention mechanisms [5,21,26,27] to extract the most valuable part from multiple received messages for decision-making. What content to share is also a critical point. A direct practice is to only share local observations or their embeddings [6,20], but it inevitably causes bandwidth wasting or even degrades the coordination efficiency. Some methods utilize techniques like teammate modeling to generate more succinct and efficient messages [8,28,29]. Besides, VBC [28] and TMC [29] also answer the question of when to communicate by utilizing a fixed threshold to control the chance of communication. In terms of the robustness of communication in cooperative MARL, [30] filters valuable content from noisy messages by Gaussian process modeling. AME [31] utilizes an ensemble-based defense method to reach robustness but it only assumes no more than half of the message channels in the system can be attacked. [18] considers the communication robustness in situations where one agent in the cooperating group is taken over by a learned adversary, and then the policy-search response-oracle (PSRO) technique is applied."

### Robustness in cooperative MARL
> _[Section 2, Related work]_

"Robustness in cooperative MARL Previous cooperative MARL [32] works either concentrate on improving coordination ability from diverse aspects like scalability [33], credit assignment [34], and non-stationarity [35], or applying the cooperative MARL technique to multiple domains like autonomous vehicle teams [36,37], power management [38], and dynamic algorithm configuration [39]. Those approaches ignore the robustness of the learned policy when encountering uncertainties, perturbations, or structural changes in the environment [10], hastening the robustness test in the MARL [40]. For the altering of the opponent policy, M3DDPG [41] learns a minimax variant of MADDPG [42] and trains the MARL policy in an adversarial way, showing potential in solving the problem of poor local optima compared with multiple baselines. [43] applies the social empowerment technique to avoid the MARL overfitting to their specific trained partners. As for the uncertainty caused by the inaccurate knowledge of the MARL dynamic model, R-MADDPG [44] proposes the concept of robust Nash equilibrium, treats the uncertainty of environment as a natural agent, and exhibits superiority when encountering reward uncertainty. Consider the observation perturbation, [16] learns an adversarial observation policy to attack one participant in a cooperative MARL system, demonstrating the high vulnerability of cooperative MARL facing observation perturbation. For the action robustness in cooperative MARL, ARTS [45] and RADAR [46] learn resilient MARL policies via adversarial value decomposition. [17] further designs an action regularizer to attack the cooperative MARL system efficiently."

### Population-based reinforcement learning (PBRL)
> _[Section 2, Related work]_

"Population-based reinforcement learning (PBRL) Population-Based Training (PBT) has been widely used in machine learning and made tremendous success in different domains [47], which also reveals great potential for reinforcement learning problems [48,49]. One successful application of PBRL is to train multiple policies to generate diverse behaviors that can accelerate the learning of downstream tasks [50]. Another category focus on applying population training to facilitate reinforcement learning in aspects like efficient exploration [51], model learning [52], robustness [19], and zero-shot coordination [53,54]. Among all these works, [19] is most similar to our work, which maintains a population with different individuals by the different network initialization, without an explicit diversity constraint among individuals. However, our work differs because we further consider the robustness of multi-agent communication beyond the single-agent RL setting, and we explicitly optimize the diversity of the attacker population."

### Single-agent and multi-agent robustness background
> _[Introduction]_

"Let's review the numerous successes achieved in modern Reinforcement Learning (RL). Most approaches depend highly on deep neural networks, which are, however, shown to be vulnerable to any adversarial attacks [9], i.e., any slight perturbation in the input may lead to entirely different decision-making of a Deep Reinforcement Learning (DRL) agent [10]. This poses a significant risk to the application of most DRL algorithms, including MARL communication algorithms, because the noise or hostile attacks in the environment can cause the system to crash. Thus, improving the robustness of the decision system, which means that we hope the system still works well when attacked, is an emergent and severe issue. For the mentioned problem in a single-agent system, many efficient methods are proposed, including adversarial regularizers designing [11,12]. They enjoy theoretical robustness guarantee, but with limited robustness ability [13]. On the other hand, other approaches introduce auxiliary adversaries to promote robustness via adversarial training, model the training process from a game theory perspective to gain the worst-case performance guarantee and show high effectiveness in different domains [14,15]. As a consequence, the MARL community also investigates the robustness of a multi-agent system from various aspects, including the uncertainty in local observation [16], model function [15], action making [17], etc. However, the communication process in MARL is much more complex. For instance, if we consider a fully connected multi-agent with N agents, there are total N×(N−1) message channels. If we train an adversary to attack these channels, the attacker's action space may grow dramatically with the number of agents. Previous works make strong assumptions to alleviate this problem, such as some default channels suffering from the same message perturbation [18] or only a limited number of agents sustaining some heuristic noise injection."

### Cited references (resolved from the paper's bibliography)
- **[1]** Zhu C, Dastani M, Wang S. *A survey of multi-agent reinforcement learning with communication.* arXiv preprint arXiv:2203.08975, 2022.
- **[2]** Ding Z, Huang T, Lu Z. *Learning individually inferred communication for multi-agent cooperation.* NeurIPS 2020.
- **[4]** Xue D, Yuan L, Zhang Z, Yu Y. *Efficient multi-agent communication via Shapley message value.* IJCAI 2022.
- **[5]** Guan C, Chen F, Yuan L, Wang C, Yin H, Zhang Z, Yu Y. *Efficient multi-agent communication via self-supervised information aggregation.* NeurIPS 2022.
- **[6]** Foerster J N, Assael Y M, de Freitas N, Whiteson S. *Learning to communicate with deep multi-agent reinforcement learning.* NeurIPS 2016.
- **[8]** Yuan L, Wang J, Zhang F, Wang C, Zhang Z, Yu Y, Zhang C. *Multi-agent incentive communication via decentralized teammate modeling.* AAAI 2022.
- **[9]** Chakraborty A, Alam M, Dey V, Chattopadhyay A, Mukhopadhyay D. *Adversarial attacks and defences: a survey.* arXiv preprint arXiv:1810.00069, 2018.
- **[10]** Moos J, Hansel K, Abdulsamad H, Stark S, Clever D, Peters J. *Robust reinforcement learning: a review of foundations and recent advances.* Machine Learning and Knowledge Extraction, 2022, 4(1): 276–315.
- **[11]** Zhang H, Chen H, Xiao C, Li B, Liu M, Boning D S, Hsieh C J. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[12]** Oikarinen T, Zhang W, Megretski A, Daniel L, Weng T W. *Robust deep reinforcement learning through adversarial loss.* NeurIPS 2021.
- **[13]** Xu M, Liu Z, Huang P, Ding W, Cen Z, Li B, Zhao D. *Trustworthy reinforcement learning against intrinsic vulnerabilities: robustness, safety, and generalizability.* arXiv preprint arXiv:2209.08025, 2022.
- **[14]** Pan X, Seita D, Gao Y, Canny J. *Risk averse robust adversarial reinforcement learning.* ICRA 2019.
- **[15]** Zhang H, Chen H, Boning D S, Hsieh C J. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[16]** Lin J, Dzeparoska K, Zhang S Q, Leon-Garcia A, Papernot N. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops 2020.
- **[17]** Hu Y, Zhang Z. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv preprint arXiv:2205.09362, 2022.
- **[18]** Xue W, Qiu W, An B, Rabinovich Z, Obraztsova S, Yeo C K. *Mis-spoke or mis-lead: achieving robustness in multi-agent communicative reinforcement learning.* AAMAS 2022.
- **[19]** Vinitsky E, Du Y, Parvate K, Jang K, Abbeel P, Bayen A. *Robust reinforcement learning using adversarial populations.* arXiv preprint arXiv:2008.01825, 2020.
- **[20]** Wang T, Wang J, Zheng C, Zhang C. *Learning nearly decomposable value functions via communication minimization (NDQ).* ICLR 2020.
- **[21]** Das A, Gervet T, Romoff J, Batra D, Parikh D, Rabbat M, Pineau J. *TarMAC: targeted multi-agent communication.* ICML 2019.
- **[22]** Sukhbaatar S, Szlam A, Fergus R. *Learning multiagent communication with backpropagation.* NeurIPS 2016.
- **[23]** Lowe R, Foerster J N, Boureau Y, Pineau J, Dauphin Y N. *On the pitfalls of measuring emergent communication.* AAMAS 2019.
- **[24]** Eccles T, Bachrach Y, Lever G, Lazaridou A, Graepel T. *Biases for emergent communication in multi-agent reinforcement learning.* NeurIPS 2019.
- **[25]** Mao H, Zhang Z, Xiao Z, Gong Z, Ni Y. *Learning agent communication under limited bandwidth by message pruning.* AAAI 2020.
- **[26]** Mao H, Zhang Z, Xiao Z, Gong Z, Ni Y. *Learning multi-agent communication with double attentional deep reinforcement learning.* Autonomous Agents and Multi-Agent Systems, 2020, 34(1): 32.
- **[27]** Wang Y, Zhong F, Xu J, Wang Y. *ToM2C: target-oriented multi-agent communication and cooperation with theory of mind.* ICLR 2021.
- **[28]** Zhang S Q, Zhang Q, Lin J. *Efficient communication in multi-agent reinforcement learning via variance based control (VBC).* NeurIPS 2019.
- **[29]** Zhang S Q, Zhang Q, Lin J. *Succinct and robust multi-agent communication with temporal message control (TMC).* NeurIPS 2020.
- **[30]** Mitchell R, Blumenkamp J, Prorok A. *Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication.* arXiv preprint arXiv:2012.00508, 2020.
- **[31]** Sun Y, Zheng R, Hassanzadeh P, Liang Y, Feizi S, Ganesh S, Huang F. *Certifiably robust policy learning against adversarial multi-agent communication (AME).* ICLR 2023.
- **[32]** OroojlooyJadid A, Hajinezhad D. *A review of cooperative multi-agent deep reinforcement learning.* arXiv preprint arXiv:1908.03963, 2019.
- **[33]** Christianos F, Papoudakis G, Rahman M A, Albrecht S V. *Scaling multi-agent reinforcement learning with selective parameter sharing.* ICML 2021.
- **[34]** Wang J, Ren Z, Han B, Ye J, Zhang C. *Towards understanding cooperative multi-agent Q-learning with value factorization.* NeurIPS 2021.
- **[35]** Papoudakis G, Christianos F, Rahman A, Albrecht S V. *Dealing with non-stationarity in multi-agent deep reinforcement learning.* arXiv preprint arXiv:1906.04737, 2019.
- **[36]** Peng Z, Li Q, Hui K M, Liu C, Zhou B. *Learning to simulate self-driven particles system with coordinated policy optimization.* NeurIPS 2021.
- **[37]** Kouzehgar M, Meghjani M, Bouffanais R. *Multi-agent reinforcement learning for dynamic ocean monitoring by a swarm of buoys.* Global Oceans 2020.
- **[38]** Wang J, Xu W, Gu Y, Song W, Green T C. *Multi-agent reinforcement learning for active voltage control on power distribution networks.* NeurIPS 2021.
- **[39]** Xue K, Xu J, Yuan L, Li M, Qian C, Zhang Z, Yu Y. *Multi-agent dynamic algorithm configuration.* NeurIPS 2022.
- **[40]** Guo J, Chen Y, Hao Y, Yin Z, Yu Y, Li S. *Towards comprehensive testing on the robustness of cooperative multi-agent reinforcement learning.* IEEE/CVF CVPR Workshops 2022.
- **[41]** Li S, Wu Y, Cui X, Dong H, Fang F, Russell S. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[42]** Lowe R, Wu Y, Tamar A, Harb J, Abbeel P, Mordatch I. *Multi-agent actor-critic for mixed cooperative-competitive environments (MADDPG).* NeurIPS 2017.
- **[43]** T. van der Heiden T, Salge C, Gavves E, van Hoof H. *Robust multi-agent reinforcement learning with social empowerment for coordination and communication.* arXiv preprint arXiv:2012.08255, 2020.
- **[44]** Zhang K, Sun T, Tao Y, Genc S, Mallya S, Başar T. *Robust multi-agent reinforcement learning with model uncertainty (R-MADDPG).* NeurIPS 2020.
- **[45]** Phan T, Gabor T, Sedlmeier A, Ritz F, Kempter B, Klein C, Sauer H, Schmid R, Wieghardt J, Zeller M, Linnhoff-Popien C. *Learning and testing resilience in cooperative multi-agent systems (ARTS).* AAMAS 2020.
- **[46]** Phan T, Belzner L, Gabor T, Sedlmeier A, Ritz F, Linnhoff-Popien C. *Resilient multi-agent reinforcement learning with adversarial value decomposition (RADAR).* AAAI 2021.
- **[47]** Jaderberg M, Dalibard V, Osindero S, Czarnecki W M, Donahue J, Razavi A, Vinyals O, Green T, Dunning I, Simonyan K, Fernando C, Kavukcuoglu K. *Population based training of neural networks.* arXiv preprint arXiv:1711.09846, 2017.
- **[48]** Jaderberg M, Czarnecki W M, Dunning I, Marris L, Lever G, Castañeda A G, et al. *Human-level performance in 3D multiplayer games with population-based reinforcement learning.* Science, 2019, 364(6443): 859–865.
- **[49]** Qian H, Yu Y. *Derivative-free reinforcement learning: a review.* Frontiers of Computer Science, 2021, 15(6): 156336.
- **[50]** Derek K, Isola P. *Adaptable agent populations via a generative model of policies.* NeurIPS 2021.
- **[51]** Parker-Holder J, Pacchiano A, Choromanski K, Roberts S. *Effective diversity in population based reinforcement learning.* NeurIPS 2020.
- **[52]** Luo F M, Xu T, Lai H, Chen X H, Zhang W, Yu Y. *A survey on model-based reinforcement learning.* arXiv preprint arXiv:2206.09328, 2022.
- **[53]** Zhao R, Song J, Haifeng H, Gao Y, Wu Y, Sun Z, Wei Y. *Maximum entropy population based training for zero-shot human-AI coordination.* arXiv preprint arXiv:2112.11701, 2021.
- **[54]** Xue K, Wang Y, Yuan L, Guan C, Qian C, Yu Y. *Heterogeneous multi-agent zero-shot coordination by coevolution.* arXiv preprint arXiv:2208.04957, 2022.
