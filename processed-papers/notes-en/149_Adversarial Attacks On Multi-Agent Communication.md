# 149. Adversarial Attacks On Multi-Agent Communication

## Metadata
- **Title**: Adversarial Attacks On Multi-Agent Communication
- **Authors**: James Tu, Tsunhsuan Wang, Jingkang Wang, Sivabalan Manivasagam, Mengye Ren, Raquel Urtasun
- **Affiliation**: Waabi; University of Toronto; MIT (work done while all authors were at Uber ATG)
- **Venue**: Not specified (arXiv:2101.06560v2, 12 Oct 2021)
- **Link/arXiv**: arXiv:2101.06560v2 [cs.LG]

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks — adversarial perturbation of learned intermediate representations (feature-map messages) exchanged between cooperative agents; malicious/compromised agents
- **Method paradigm**: Adversarial attack generation (PGD/FGSM), adversarial training defense, robust aggregation (median/soft-median pooling), black-box transfer attacks with adversarial domain adaptation (ADDA), online attacks exploiting temporal consistency
- **Keywords**: multi-agent communication, adversarial attacks, intermediate feature perturbation, object detection, V2V, adversarial training, transfer attack, domain adaptation

## TL;DR
The paper studies adversarial robustness of cooperative multi-agent systems that communicate by sharing learned intermediate feature maps, showing that an indistinguishable perturbed message can severely degrade a victim's object detection but weakens as the number of benign agents grows, and that defenses (adversarial training, robust aggregation) and practical black-box transfer/online attacks (via domain adaptation and temporal consistency) are feasible.

## Problem & Motivation
Cooperative multi-agent systems (e.g., fleets of drones or self-driving vehicles) increasingly share information by transmitting intermediate neural-network representations rather than raw inputs, which improves perception and computational efficiency. However, deep networks are vulnerable to adversarial attacks, and shared messages can be modified by malicious or compromised agents to induce false outputs while remaining indistinguishable from benign messages. Prior adversarial-attack research focuses almost entirely on input domains (images, point clouds, text), and adversarial robustness of multi-agent deep learning systems during inference has scarcely been studied. The paper aims to characterize this novel feature-level communication threat and contribute an additional layer of fault tolerance at the neural-network level for safety-critical applications.

## Robustness Setting
- **Threat model / uncertainty set**: An attacker agent i targets a victim agent j by sending an indistinguishable adversarial message m′_i = m_i + δ to maximize error in the aggregated output Z′_j = G(m_1, …, m_i + δ, …, m_N). The perturbation is bounded by ‖δ‖_p ≤ ϵ (the paper uses p = ∞, ϵ = 0.1). Settings considered: white-box (full access to victim weights, PGD optimization), black-box transfer (no weight access; train a surrogate model G′ aligned via domain adaptation), and online/low-budget attacks exploiting temporal redundancy. Single- and multiple-attacker (cooperative and non-cooperative) cases are studied.
- **Setting**: cooperative multi-agent perception with one or more malicious agents; homogeneous agents sharing the same network; decentralized message passing with centralized-style aggregation at the receiver; inference-time (online) attacks.

## Method
- **Multi-agent framework**: Each agent i encodes sensor input x_i into an intermediate feature map m_i = F(x_i), broadcasts it, and a receiving agent j aggregates all messages Z_j = G(m_1, …, m_N). The task is object detection; output is a set of bounding-box proposals with class scores.
- **Adversarial perturbation generation**: A custom adversarial loss ℓ_adv(z′, z) (Eq. 1) pushes the perturbed output away from the unperturbed output — suppressing the correct class to create false negatives and boosting a non-background class to create false positives, while minimizing IoU. The optimal perturbation minimizes this loss over all proposals under an ϵ-ℓ_p bound (Eq. 2), solved with PGD and clipped to [−ϵ, ϵ]. A focal-loss term is added because non-maximum suppression (NMS) makes high-confidence proposals more important.
- **Transfer attack**: Because intermediate representations are model-dependent, vanilla transfer fails. The surrogate F′, G′ are trained with Adversarial Discriminative Domain Adaptation (ADDA): a discriminator D forces F′ to produce representations distributionally similar to F via a min-max objective (Eq. 4), using spectral normalization and the two-time-scale update rule for stability.
- **Online attack**: Exploits temporal redundancy by initializing the current perturbation from the previous time step and applying a rigid transformation H_{t→t+1} to account for egomotion (Eq. 5), enabling strong attacks with a single gradient update per frame.
- **Defenses**: (a) Adversarial training applied to intermediate features (Eq. 6); (b) when the threat model is unknown, robust message aggregation modules (median / soft-median pooling instead of mean pooling in the GNN).

## Theoretical Contributions
None / mostly empirical. The paper provides loss-design analysis (a monotonicity criterion on the gradient magnitude of the proposal-score loss motivated by NMS) but no formal convergence, sample-complexity, or certified-robustness guarantees.

## Experiments
- **Environment/Benchmark**: Two multi-agent perception settings — (1) Multi-View ShapeNet: synthetic multi-view detection from RGB-D images of 10 ShapeNet object classes (a drone-fleet analogue; 50,000 training / 10,000 validation scenes, 2–7 viewpoints), and (2) Vehicle-to-Vehicle (V2V) communication: real-world LiDAR logs simulated with a high-fidelity LiDAR simulator using the V2VNet model (46,796 training / 96,862 validation frames, up to 7 agents).
- **Baselines**: No attack; uniform noise U(−ϵ, ϵ); white-box attack; transfer attack (with/without domain adaptation, ILAP, DI); negative task loss (−L_task) vs. proposed L_adv; aggregation variants (mean pool, GNN mean, GNN median, GNN soft-median); adversarial training with varying numbers of attackers.
- **Evaluation metrics**: Average Precision at 0.7 IoU (AP@0.7) — area under the precision-recall curve of bounding boxes correct above 0.7 IoU with a same-class ground-truth box.

## Key Results
- Indistinguishable white-box perturbations severely degrade detection (e.g., V2V AP@0.7 drops from 82.19 clean to 7.55 perturbed; ShapeNet from ~66 to 0.62), but attacks weaken as more benign agents are added because mean pooling dilutes the adversarial message.
- Adversarial training is highly effective: adversarially trained models recover near-clean performance under attack (V2V 83.44, ShapeNet 66.00) and even slightly improve clean performance; training must use an equal-or-greater threat model (number of attackers) to fully defend.
- Robust aggregation helps without knowing the threat model: GNN with median / soft-median pooling improves robustness over mean pooling (e.g., V2V GNN-Median perturbed AP 12.8 vs. Mean Pool 0.90 at 2 agents), at some cost to clean performance.
- Black-box transfer attacks are much harder at the feature level; domain adaptation is key (Transfer+DA drops ShapeNet to 42.59 vs. 66.21 without DA), and ILAP yields a small further improvement while DI is ineffective. The proposed L_adv beats −L_task, and online warping/reuse of perturbations strengthens low-budget attacks.

## Limitations & Future Work
- Adversarial-training defense requires knowledge of the threat model (and matching the attacker count); robustness to stronger attacks can sacrifice clean-data performance.
- Robust aggregation (median pooling) discards information, hurting clean performance as the number of agents grows.
- Transfer attacks remain difficult because feature perturbation domains are model-dependent; transferability is only "moderate" even with domain adaptation.
- The study focuses on object detection in two perception settings; broader tasks, more detection architectures, and detection-based defenses are left for future security protocols (the paper frames its contribution as an additional layer of fault tolerance toward more secure multi-agent systems).

## Relevance to Survey
This paper is a representative work on the "communication robustness / adversarial attacks on multi-agent communication" theme of robust MARL. Rather than environment/model uncertainty or robust Markov-game theory, it targets the inference-time communication channel of cooperative multi-agent deep learning systems, treating malicious/compromised agents that perturb shared intermediate representations. It connects the adversarial-attacks-on-deep-learning line (PGD/FGSM, transfer attacks, adversarial training) with cooperative multi-agent perception, and contributes defense lines — adversarial training and robust aggregation — that parallel minimax/adversarial-training and fault-tolerance themes elsewhere in the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Multi-Agent Deep Learning Systems"]_

"Multi-agent and distributed systems are widely employed in real-world applications to improve computation efﬁciency [27, 17, 2], collaboration [52, 59, 18, 41, 42], and safety [38, 35]. Recently, autonomous systems have improved greatly with the help of neural networks. New directions have opened up in cooperative multi-agent deep learning systems e.g., federated learning [27, 2]. Although multi-agent communication introduces a multitude of beneﬁts, communication channels are vulnerable to security breaches, as communication channels can be attacked [34, 45], encryption algorithms can be broken [46], and agents can be compromised [5, 61]. Thus, imperfect communication channels may be used to execute adversarial attacks which are especially effective against deep learning systems. While robustness has been studied in the context of federated learning [20, 1, 56, 19], the threat models are different as dataset poisoning and model poisoning are typically used. To the best of our knowledge, few works study adversarial robustness on multi-agent deep learning systems during inference."

> _[Section 2, Related Work — "Adversarial Attacks"]_

"Adversarial attacks were ﬁrst discovered in the context of image classiﬁcation [48], where a small imperceivable perturbation can drastically change a neural network's behaviour and induce false outputs. Such attacks were then extended to various applications such as semantic segmentation [57] and reinforcement learning [24]. There are two main settings for adversarial attacks - white box and black box. In a white box setting [48, 21, 30], the attacker has full access to the target neural network weights and adversarial examples can be generated using gradient-based optimization to maximize the network's error. In contrast, black box attacks are conducted without knowledge of the target neural network weights and therefore without any gradient computation. In this case, attackers can leverage real world knowledge to inject adversaries that resemble common real world objects [47, 36]. However, if the attacker is able to query the target model, the literature proposes several different strategies to perform query-based attacks [4, 12, 6, 10]. However, query-based attacks are infeasible for some applications as they typically require prohibitively large amounts of queries and computation. Apart from query-based attacks, a more practical but more challenging alternative is to conduct transfer attacks [39, 58, 16] which do not require querying the target model. In this setting, the attacker trains a surrogate model that imitates the target model. By doing so, the hope is that perturbations generated for the surrogate model will transfer to the target model."

> _[Section 2, Related Work — "Perturbations In Feature Space"]_

"While most works in the literature focus on input domains like images, some prior works have considered perturbations on intermediate representations within neural networks. Speciﬁcally, [25] estimated the projection of adversarial gradients on a selected subspace to reduce the queries to a target model. [40, 44, 14] proposed to generate adversarial perturbation in word embeddings for ﬁnding adversarial but semantically-close substitution words. [55, 60] showed that training on adversarial embeddings could improve the robustness of Transformer-based models for NLP tasks."

### Cited references (resolved from the paper's bibliography)
- **[1]** Bhagoji, Chakraborty, Mittal, Calo. *Analyzing federated learning through an adversarial lens.* ICML 2019.
- **[2]** Bonawitz, Eichner, Grieskamp, Huba, Ingerman, et al. *Towards federated learning at scale: System design.* CoRR 2019.
- **[4]** Brendel, Rauber, Bethge. *Decision-based adversarial attacks: Reliable attacks against black-box machine learning models.* ICLR 2018.
- **[5]** Brewster. *Watch Chinese hackers control Tesla's brakes from 12 miles away.* 2016.
- **[6]** Brunner, Diehl, Truong-Le, Knoll. *Guessing smart: Biased sampling for efficient black-box adversarial attacks.* CoRR abs/1812.09803, 2018.
- **[10]** Chen, Jordan, Wainwright. *HopSkipJumpAttack: A query-efficient decision-based attack.* arXiv:1904.02144, 2019.
- **[12]** Chen, Zhang, Sharma, Yi, Hsieh. *ZOO: Zeroth order optimization based black-box attacks to deep neural networks without training substitute models.* AISec 2017.
- **[14]** Cheng, Yi, Zhang, Chen, Hsieh. *Seq2Sick: Evaluating the robustness of sequence-to-sequence models with adversarial examples.* CoRR abs/1803.01128, 2018.
- **[16]** Cheng, Dong, Pang, Su, Zhu. *Improving black-box adversarial attacks with a transfer-based prior.* NeurIPS 2019.
- **[17]** Dillon, Wu, Chang. *Cloud computing: Issues and challenges.* AINA 2010.
- **[18]** Eshratifar, Pedram. *Energy and performance efficient computation offloading for deep neural networks in a mobile cloud computing environment.* GLSVLSI 2018.
- **[19]** Fang, Cao, Jia, Gong. *Local model poisoning attacks to Byzantine-robust federated learning.* USENIX Security 2020.
- **[20]** Ghosh, Hong, Yin, Ramchandran. *Robust federated learning in a heterogeneous environment.* arXiv:1906.06629, 2019.
- **[21]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* ICLR 2015.
- **[24]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* 2017.
- **[25]** Jiang, Ma, Chen, Bailey, Jiang. *Black-box adversarial attacks on video recognition models.* ACM MM 2019.
- **[27]** Konecný, McMahan, Yu, Richtárik, Suresh, Bacon. *Federated learning: Strategies for improving communication efficiency.* CoRR 2016.
- **[30]** Madry, Makelov, Schmidt, Tsipras, Vladu. *Towards deep learning models resistant to adversarial attacks.* arXiv:1706.06083, 2017.
- **[34]** Mokhtar, Azab. *Survey on security issues in vehicular ad hoc networks.* Alexandria Engineering Journal, 2015.
- **[35]** Nakamoto. *Bitcoin: A peer-to-peer electronic cash system.* Technical report, 2019.
- **[36]** Nassi, Nassi, Ben-Netanel, Mirsky, Drokin, Elovici. *Phantom of the ADAS: Phantom attacks on driver-assistance systems.* IACR 2020.
- **[38]** Obst, Hobert, Reisdorf. *Multi-sensor data fusion for checking plausibility of V2V communications by vision-based multiple-object tracking.* VNC 2014.
- **[39]** Papernot, McDaniel, Goodfellow, Jha, Celik, Swami. *Practical black-box attacks against machine learning.* AsiaCCS 2017.
- **[40]** Papernot, McDaniel, Swami, Harang. *Crafting adversarial input sequences for recurrent neural networks.* MILCOM 2016.
- **[41]** Rauch, Klanner, Rasshofer, Dietmayer. *Car2X-based perception in a high-level fusion architecture for cooperative perception systems.* IV 2012.
- **[42]** Rockl, Strang, Kranz. *V2V communications in automotive multi-sensor multi-target tracking.* VTC 2008.
- **[44]** Sato, Suzuki, Shindo, Matsumoto. *Interpretable adversarial perturbation in input embedding space for text.* IJCAI 2018.
- **[45]** Sedjelmaci, Senouci. *An accurate and efficient collaborative intrusion detection framework to secure vehicular networks.* Computers & Electrical Engineering, 2015.
- **[46]** Stupp, Rundle. *Capital One breach highlights shortfalls of encryption.* 2019.
- **[47]** Sun, Cao, Chen, Mao. *Towards robust LiDAR-based perception in autonomous driving: General black-box adversarial sensor attack and countermeasures.* USENIX Security 2020.
- **[48]** Szegedy, Zaremba, Sutskever, Bruna, Erhan, Goodfellow, Fergus. *Intriguing properties of neural networks.* ICLR 2014.
- **[52]** Wang, Manivasagam, Liang, Yang, Zeng, Urtasun. *V2VNet: Vehicle-to-vehicle communication for joint perception and prediction.* arXiv 2020.
- **[55]** Wu, Bamman, Russell. *Adversarial training for relation extraction.* EMNLP 2017.
- **[56]** Xie, Huang, Chen, Li. *DBA: Distributed backdoor attacks against federated learning.* ICLR 2020.
- **[57]** Xie, Wang, Zhang, Zhou, Xie, Yuille. *Adversarial examples for semantic segmentation and object detection.* ICCV 2017.
- **[58]** Xie, Zhang, Zhou, Bai, Wang, Ren, Yuille. *Improving transferability of adversarial examples with input diversity.* CVPR 2019.
- **[59]** Zeng, Mozaffari, Semiari, Saad, Bennis, Debbah. *Wireless communications and control for swarms of cellular-connected UAVs.* ACSSC 2018.
- **[60]** Zhu, Cheng, Gan, Sun, Goldstein, Liu. *FreeLB: Enhanced adversarial training for natural language understanding.* ICLR 2020.
- **[61]** Zorz. *Researchers hack BMW cars, discover 14 vulnerabilities.* 2018.
