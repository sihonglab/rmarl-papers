# 69. Towards Robust Multi-UAV Collaboration: MARL with Noise-Resilient Communication and Attention Mechanisms

## Metadata
- **Title**: Towards Robust Multi-UAV Collaboration: MARL with Noise-Resilient Communication and Attention Mechanisms
- **Authors**: Zilin Zhao, Chishui Chen, Haotian Shi, Jiale Chen, Xuanlin Yue, Zhejian Yang, Yang Liu
- **Affiliation**: Jilin University, Changchun, China (College of Software Engineering; College of Instrumentation and Electrical Engineering; School of Communication Engineering; School of Artificial Intelligence); China University of Mining and Technology, Xuzhou, China
- **Venue**: Not specified (arXiv preprint; supplementary materials reference IROS25; arXiv:2503.02913v1, 4 Mar 2025)
- **Link/arXiv**: arXiv:2503.02913v1 [cs.MA]; supplementary materials at https://github.com/zilin-zhao/iros25-supp

## Taxonomy
- **Robustness / perturbation type targeted**: Communication noise / sensor noise (distance-dependent multiplicative attenuation + additive Gaussian white noise on inter-UAV communicated sensor data); robust communication protocol design under noisy environments
- **Method paradigm**: Cooperative MARL with CTDE (COMA / counterfactual policy gradients); attention mechanisms (CBAM, channel/spatial attention); denoising autoencoder-based multi-sensor denoising and fusion network
- **Keywords**: Multi-UAV, informative path planning (IPP), MARL, COMA, communication robustness, attention mechanism, sensor fusion/denoising

## TL;DR
The paper proposes a COMA-based MARL framework for full-3D multi-UAV informative path planning that adds an attention-based multi-sensor denoising-and-fusion network (SenDFuse) and CBAM attention to make inter-UAV communication and decision-making robust to communication noise, improving path-planning efficiency and robustness (reported 78% improvement in entropy reduction).

## Problem & Motivation
Cooperative multi-UAV deployment improves large-scale information collection but raises two challenges: designing robust communication protocols and effective multi-agent decision-making, especially in noisy environments. Traditional IPP algorithms are either non-adaptive (static/pre-defined paths) or adaptive but suffer exponentially growing execution time; GNN-based IPP methods rely on supervised imitation and expert demonstrations. RL shifts the decision-making cost to training and avoids needing expert targets, but prior RL/MARL IPP work largely studied 2D or single-agent 3D settings, or fixed-altitude 3D problems, and focused on credit assignment. To the authors' knowledge, no prior work addresses multi-UAV communication protocol design under sensor fusion and communication noise, nor integrates composite attention mechanisms in this framework.

## Robustness Setting
- **Threat model / uncertainty set**: Communication noise on the sensor data exchanged between UAVs, modeled as a combination of distance-dependent multiplicative attenuation and additive Gaussian white noise: I_r(x,y) = α(x,y)·I(x,y) + n(x,y), with n ~ N(0, σ²). "Moderate noise" is α ~ U(0.8, 1), σ = 0.02; "loud noise" is α ~ U(0.6, 1), σ = 0.06. The local UAV's own data is assumed unaffected by noise; only data communicated from other UAVs carries noise.
- **Setting**: Cooperative (fully cooperative multi-UAV navigation); centralized training, decentralized execution (CTDE) via COMA; online RL. The SenDFuse Network is pre-trained offline and then deployed within the architecture.

## Method
- Formulates multi-UAV cooperative navigation as an informative path planning (IPP) problem in full 3D, maximizing information gain (Shannon entropy reduction of the belief map) subject to a per-UAV communication/sampling budget; uses a relative-entropy-reduction reward.
- Builds a SenDFuse Network (Sensor Denoising and Fusion Network) extending NestFuse from fusing two same-mode/different-modality images to fusing n same-modality/different-mode images; uses an attention-based fusion strategy combining channel attention C(·) and spatial attention S(·) with weights α + β = 1, and exploits its autoencoder structure for noise resistance.
- Trains SenDFuse as a denoising autoencoder: during training the fusion strategy is disabled, artificial noise is injected, and the network reconstructs clean images using a loss combining MSE, MAE, and (1 − SSIM); during deployment the attention-based fusion strategy processes deep features.
- Uses a shared Actor network and a Critic network both built on the CBAM (Convolutional Block Attention Module) structure; the Actor consumes eight 11×11 submaps (budget, ID, altitude, footprint, local sensor observation, local belief, local entropy, denoising-fusion map) and outputs a distribution over 6 discrete actions; the Critic additionally takes four global-information maps.
- Trains via COMA (counterfactual multi-agent policy gradients), computing a counterfactual baseline / advantage A_i = Q(s,u) − Σ π(u'_i)Q(s,(u_{-i},u'_i)) and updating with the policy gradient theorem, using TD(λ) for the critic, for credit assignment in the cooperative team.

## Theoretical Contributions
None / mostly empirical. The paper presents standard COMA formulas (counterfactual advantage, policy-gradient objective, TD(λ)) but provides no convergence, sample-complexity, or robustness-certification analysis.

## Experiments
- **Environment/Benchmark**: Three environment categories — Env1: synthetic manually-drawn star-shaped region; Env2: thermal imaging data from the HIT-UAV dataset (FLIR long-wave infrared, white-hot mode); Env3: visible-light aerial view of the Geology Palace, Chaoyang Campus, Jilin University. 4 UAVs deployed, communication budget b = 15, 1200 training episodes; noise set to moderate/loud as defined.
- **Baselines**: For comparison: "AG" (Adaptive Gain, adaptive information-gain IPP by Carbone et al.), "NL" (Non-adaptive Lawnmower), and "Random". For ablation: Base (no SenDFuse, no CBAM), CBAM-only, Fusion-only, and both modules ("Ours").
- **Evaluation metrics**: F1-Score (higher better) and Shannon entropy of the global map belief (lower better), measured across sampling progress (33% / 67% / 100% of budget); global reward / convergence during training; 10 trials with mean and standard deviation.

## Key Results
- The model incorporating both CBAM and SenDFuse achieves the best convergence speed and final reward in training; Fusion-only outperforms CBAM-only, and both outperform the naive Base model.
- As noise intensity increases (no/moderate/loud), the benefit of the two modules grows; the Fusion module is the most effective denoising/fusion method and also reduces the increasing-variance instability under heavy noise, while CBAM alone still beats the naive method.
- Against external baselines, the method achieves the best F1-Score and Entropy and best stability across Env1–Env3; AG is competitive on F1-Score but worse on entropy due to its conservative strategy leaving regions unexplored.
- The abstract reports a 78% improvement in entropy reduction in noisy environments.

## Limitations & Future Work
Not specified. (No dedicated limitations/future-work discussion; the conclusion only summarizes contributions. Implicit constraints include the assumption that the local UAV's own data is noise-free and evaluation limited to small fleets (4 UAVs) and a few environments.)

## Relevance to Survey
This paper sits on the "communication robustness" line of robust MARL rather than the formal robust-MDP/robust-Markov-game line: it treats robustness empirically as resilience to communication/sensor noise in a cooperative CTDE setting (COMA), achieved through a denoising-autoencoder fusion network and attention mechanisms. It connects to themes of communication-robust MARL, noise/perturbation resilience, and multi-agent cooperation (information path planning), complementing the theory-heavy model-uncertainty and adversarial-training works in the survey by offering an application-oriented, architecture-level robustness approach.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"In recent years, UAV technology has made significant advancements, with its applications expanding across various domains [1]. These developments have provided efficient and cost-effective solutions for numerous industries. Due to their high flexibility, high mobility, and low deployment costs, UAVs are increasingly employed for monitoring complex terrains [2], [3]. Moreover, in large-scale terrain monitoring tasks, deploying multiple UAVs to explore target areas and establish communication systems for information exchange can significantly enhance exploration efficiency and reduce overall costs [4], [5]. However, a major challenge in this context lies in designing robust communication protocols [6], [7] and developing effective decision-making strategies for multiple agents [8]."

> _[Introduction]_

"The informative path planning (IPP) problem is a critical challenge in such scenarios [2]. IPP focuses on planning information-rich paths for each agent while considering constrained resource budgets (i.e., time, energy, etc.) to achieve efficient collaborative data collection. Traditional algorithms for IPP problem have been extensively studied [9], such as non-adaptive methods [10], [11], which rely on static and pre-defined paths or assume uniform target distributions. However, real-world scenarios are often far more complex. Some studies have proposed adaptive algorithms [12], [13], enabling UAVs to make dynamic decisions in real time, but as the planning horizon expands, these algorithms suffer from exponentially increasing execution times due to the need to evaluate a vast number of candidate paths, rendering them infeasible for time-sensitive tasks. Meanwhile, GNN-based IPP methods [14], [15] have been studied. Although these methods can address the execution time issue, they still rely on supervised imitation learning and require expert demonstrations for training."

> _[Introduction]_

"Reinforcement learning (RL) methods have emerged as a promising approach for effective online decision-making in robotics [16]–[18]. By simulating interactions between UAVs and their environment, RL enables UAVs to learn and adapt in dynamic scenarios, progressively improving their path-planning strategies. In the context of the IPP problem, the advantage of RL methods lies in shifting the computational burden of decision-making from the deployment to the training [19]: with proper training, agents can make high-quality decisions during deployment with constant-time complexity. Furthermore, RL methods do not require supervised training or imitation of artificially defined expert targets. Therefore, Chen et al. [20] and Tan et al. [21] studied RL for IPP scenarios in 2D spaces, while other reachers' works [22]–[26] investigated single-agent RL in 3D environments. In work by Zeng et al. [27], single-agent autonomous exploration for acquiring spatial information about crops in 3D agricultural environments was studied, and Bartolomei et al. [28] explored UAV scanning of regions of interest for semantic segmentation, but these works did not address multi-UAV scenarios. Thus, recent works [8], [29] have studied 3D but fixed-altitude IPP problems. Westheider et al. [30] and Wang et al. [31] focusd on solving the credit assignment problem in the multi-agent IPP problem. Between them, the former brought the MARL-IPP problem into full-3D environment for the first time. However, to the best of our knowledge, no existing research addresses the design of multi-UAV communication protocols in this context, particularly under conditions involving sensor fusion and communication noise. Moreover, no prior work has explored the integration of composite attention mechanisms within this framework."

### Cited references (resolved from the paper's bibliography)
- **[1]** Muchiri, Kimathi. *A review of applications and potential applications of UAV.* Proceedings of the Sustainable Research and Innovation Conference 2022.
- **[2]** Popović, Vidal-Calleja, Hitz, Chung, Sa, Siegwart, Nieto. *An informative path planning framework for UAV-based terrain monitoring.* Autonomous Robots 2020.
- **[3]** Jiménez-Jiménez, Ojeda-Bustamante, Marcial-Pablo, Enciso. *Digital terrain models generated with low-cost UAV photogrammetry: Methodology and accuracy.* ISPRS International Journal of Geo-Information 2021.
- **[4]** Liu, Lai, Lin, Leung. *Joint communication and trajectory optimization for multi-UAV enabled mobile internet of vehicles.* IEEE Transactions on Intelligent Transportation Systems 2022.
- **[5]** Werner, Báča, Štibinger, Doubravová, Šolc, Rusňák, Saska. *Autonomous localization of multiple ionizing radiation sources using miniature single-layer Compton cameras onboard a group of micro aerial vehicles.* IEEE/RSJ IROS 2024.
- **[6]** Meng, He, Wu, Li. *Multi-UAV collaborative sensing and communication: Joint task allocation and power optimization.* IEEE Transactions on Wireless Communications 2022.
- **[7]** Rockenbauer, Lim, Müller, Siegwart, Schmid. *Traversing Mars: Cooperative informative path planning to efficiently navigate unknown scenes.* IEEE Robotics and Automation Letters 2024.
- **[8]** Bayerlein, Theile, Caccamo, Gesbert. *Multi-UAV path planning for wireless data harvesting with deep reinforcement learning.* IEEE Open Journal of the Communications Society 2021.
- **[9]** Aggarwal, Kumar. *Path planning techniques for unmanned aerial vehicles: A review, solutions, and challenges.* Computer Communications 2020.
- **[10]** Bähnemann, Schindler, Kamel, Siegwart, Nieto. *A decentralized multi-agent unmanned aerial system to search, pick up, and relocate objects.* IEEE SSRR 2017.
- **[11]** Meliou, Krause, Guestrin, Hellerstein. *Nonmyopic informative path planning in spatio-temporal models.* AAAI 2007.
- **[12]** Hollinger, Englot, Hover, Mitra, Sukhatme. *Active planning for underwater inspection and the benefit of adaptivity.* The International Journal of Robotics Research 2013.
- **[13]** Blanchard, Sapsis. *Informative path planning for anomaly detection in environment exploration and monitoring.* Ocean Engineering 2022.
- **[14]** Tzes, Bousias, Chatzipantazis, Pappas. *Graph neural networks for multi-robot active information acquisition.* IEEE ICRA 2023.
- **[15]** Li, Gama, Ribeiro, Prorok. *Graph neural networks for decentralized multi-robot path planning.* IEEE/RSJ IROS 2020.
- **[16]** Singh, Kumar, Singh. *Reinforcement learning in robotic applications: a comprehensive survey.* Artificial Intelligence Review 2022.
- **[17]** Ao, Chen, Tschopp, Breyer, Siegwart, Cramariuc. *Unified data collection for visual-inertial calibration via deep reinforcement learning.* IEEE ICRA 2022.
- **[18]** Cao, Zhao, Wang, Xiang, Sartoretti. *Deep reinforcement learning-based large-scale robot exploration.* IEEE Robotics and Automation Letters 2024.
- **[19]** Popović, Ott, Rückin, Kochenderfer. *Learning-based methods for adaptive informative path planning.* Robotics and Autonomous Systems 2024.
- **[20]** Chen, Martin, Huang, Wang, Englot. *Autonomous exploration under uncertainty via deep reinforcement learning on graphs.* IEEE/RSJ IROS 2020.
- **[21]** Tan, Ma, Liang, Chng, Cao, Sartoretti. *IR²: Implicit rendezvous for robotic exploration teams under sparse intermittent connectivity.* IEEE/RSJ IROS 2024.
- **[22]** Lodel, Brito, Serra-Gómez, Ferranti, Babuška, Alonso-Mora. *Where to look next: Learning viewpoint recommendations for informative trajectory planning.* IEEE ICRA 2022.
- **[23]** Cao, Wang, Vashisth, Fan, Sartoretti. *CAtNIPP: Context-aware attention-based network for informative path planning.* Conference on Robot Learning (PMLR) 2023.
- **[24]** Wei, Zheng. *Informative path planning for mobile sensing with reinforcement learning.* IEEE INFOCOM 2020.
- **[25]** Vashisth, Rückin, Magistri, Stachniss, Popović. *Deep reinforcement learning with dynamic graphs for adaptive informative path planning.* IEEE Robotics and Automation Letters 2024.
- **[26]** Cao, Wang, Vashisth, Fan, Sartoretti. *CAtNIPP: Context-aware attention-based network for informative path planning.* Proceedings of the 6th Conference on Robot Learning (PMLR vol. 205) 2023.
- **[27]** Zeng, Zaenker, Bennewitz. *Deep reinforcement learning for next-best-view planning in agricultural applications.* IEEE ICRA 2022.
- **[28]** Bartolomei, Teixeira, Chli. *Semantic-aware active perception for UAVs using deep reinforcement learning.* IEEE/RSJ IROS 2021.
- **[29]** Viseras, Garcia. *DeepIG: Multi-robot information gathering with deep reinforcement learning.* IEEE Robotics and Automation Letters 2019.
- **[30]** Westheider, Rückin, Popović. *Multi-UAV adaptive path planning using deep reinforcement learning.* IEEE/RSJ IROS 2023.
- **[31]** Wang, Xiang, Huang, Sartoretti. *SCRIMP: Scalable communication for reinforcement- and imitation-learning-based multi-agent pathfinding.* IEEE/RSJ IROS 2023.
