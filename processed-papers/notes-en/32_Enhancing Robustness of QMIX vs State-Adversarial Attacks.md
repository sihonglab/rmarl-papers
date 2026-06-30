# 32. Enhancing the Robustness of QMIX against State-adversarial Attacks

## Metadata
- **Title**: Enhancing the Robustness of QMIX against State-adversarial Attacks
- **Authors**: Weiran Guo, Guanjun Liu, Ziyuan Zhou, Ling Wang, Jiacun Wang
- **Affiliation**: Department of Computer Sciences, Tongji University, Shanghai, China; College of Transportation Engineering, Tongji University; Department of Computer Science and Software Engineering, Monmouth University, West Long Branch, USA
- **Venue**: Not specified (arXiv:2307.00907v1 [cs.LG], 3 Jul 2023)
- **Link/arXiv**: arXiv:2307.00907

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation (state-adversarial attacks on an agent's observation input in cooperative MARL)
- **Method paradigm**: Adversarial training (max-min worst-case reward), transfer of single-agent robust RL techniques to MARL; gradient-based adversary (FGSM/PGD), policy (hinge-like) regularization, alternating training with learned adversaries (ATLA), policy adversarial actor director (PA-AD)
- **Keywords**: multi-agent reinforcement learning, robustness, state-adversarial attacks, QMIX, adversarial training

## TL;DR
The paper migrates four single-agent (SARL) robustness techniques — gradient-based adversary, policy regularization, ATLA, and PA-AD — to the cooperative MARL algorithm QMIX, and empirically compares their robustness against state-adversarial attacks on SMAC, summarizing each method's strengths and weaknesses.

## Problem & Motivation
Deep RL agents remain vulnerable to state-adversarial attacks (perturbations applied to an agent's observation without changing the underlying environment), which correspond in practice to sensor-limitation noise or malicious attacks (e.g., in autonomous driving). Most prior robustness work targets single-agent RL (SARL); robust MARL is comparatively underexplored even though multi-agent settings are common (games, transportation) and harder, because agents are interconnected and attacking one agent can reduce the whole system's total return. The paper aims to adapt existing SARL robustness techniques to the cooperative MARL setting using QMIX as the running example.

## Robustness Setting
- **Threat model / uncertainty set**: A state adversary perturbs the observations of M of the N agents (the experiments take the most extreme case M = N, dense attacks at every timestep). The perturbed observation õ^i = o^i + δ^i is bounded by an l∞-norm perturbation budget ε. The adversary aims to minimize the multi-agent system's total (discounted) reward. Modeled as a state-adversarial stochastic game (SaSG) and a state-adversarial Dec-POMDP with tuple < S, {A^i}_N, P, {R^i}_N, {O^i}_N, {B^i}_M, γ >, where B^i is the set of adversarial states applied on agent i; the state adversary changes only with the current state and is time-invariant.
- **Setting**: Cooperative (c-MARL); centralized training with decentralized execution (CTDE, via QMIX); online; the worst-case reward (max-min) is addressed through adversarial training.

## Method
- Formulates a per-agent max-min objective for the attacked single agents: maximize over policy π^i while minimizing over the perturbed observation õ^i of Σ_{a^i} π^i(a^i|õ^i) Q_{φ^i}(õ^i, a^i); the attacking policy minimizes the system's total discounted reward (Eq. 2). Leverages QMIX's monotonic constraint between individual Q^i and global Q_tot.
- **Gradient-based adversary**: Crafts a max-norm constrained perturbation via FGSM, δ^i = ε·sign(∇_{õ^i} L(θ^i, õ^i, u^i)), where L is the cross-entropy loss toward the highest-probability target action u^i. Easy but not guaranteed optimal (per [10]).
- **Policy regularization**: Adds a robust hinge-like regularizer L_reg(φ) measuring total-variation distance between clean and perturbed action distributions, keeping the best action unchanged after perturbation; total loss L_tot(φ) = L(φ) + κ·L_reg(φ), bounding both the TD error and value-function perturbation.
- **ATLA in MARL**: Trains a separate adversary network (using a continuous-action MARL algorithm such as MAPPO/MADDPG) to output worst-case perturbations, with reward equal to the negative of the victim team's reward; equivalent to two multi-agent teams cross-training against each other (Algorithm 1).
- **PA-AD in MARL**: A director v outputs the optimal adversarial perturbation direction (solving an RL problem with negative-reward signal) and an actor g produces the optimal perturbation along that direction via a gradient-based/supervised method (e.g., FGSM/PGD), reducing the action space and simplifying training (Algorithm 2; targeted loss Eq. 7).

## Theoretical Contributions
Mostly empirical. The paper discusses the theoretical foundation of the transferred methods in the multi-agent setting (e.g., relies on the QMIX monotonicity constraint, cites that the value-function gap can be bounded if action-distribution differences are small [10], and that the joint optimal adversarial perturbation exists and is unique [17]), but provides no new convergence, sample-complexity, or certified-robustness proofs of its own.

## Experiments
- **Environment/Benchmark**: StarCraft Multi-Agent Challenge (SMAC), StarCraft II; four maps: 2m_vs_1z, 3m, 3s_vs_3z, and 2s3z. Most extreme dense-attack case M = N at every timestep.
- **Baselines**: Vanilla QMIX (trained on clean states) compared against QMIX robustly trained with each of the four methods (FGSM/gradient-based, policy regularization, ATLA, PA-AD); cross-attack evaluation among the attack methods.
- **Evaluation metrics**: Winning rate ("Win") and accumulated reward (mean ± std) over 32 test episodes per round, under No Attack, FGSM Attack, ATLA Attack, and PA-AD Attack (policy regularization is a defense, not used as an attack).

## Key Results
- Gradient-based (FGSM) adversarial training is easy and effective at boosting robustness, but does not generate the strongest attack, so the trained QMIX is not robust enough against stronger attacks.
- Policy regularization works well against weaker interference but performs poorly under stronger/optimal adversaries and is unstable even in clean states (e.g., on 3m it drops to 0.34 win / 11.60 reward with no attack).
- ATLA is hard to scale to MARL: the adversary must produce perturbations for multiple agents, multiplying state/action space; the authors encountered gradient explosion and obtained highly disappointing outcomes (e.g., on 3m the ATLA-trained model degrades to ~0.02 win under attacks).
- PA-AD generates the perturbation direction and only then applies state interference, reducing the action space and simplifying training; it is the most consistently robust across maps and attacks (e.g., on 2m_vs_1z it keeps 0.98 win / 19.80 reward even under PA-AD attack).

## Limitations & Future Work
- ATLA scales poorly to multi-agent settings (multiplied state/action spaces, gradient explosion, poor results), especially when image inputs are used as states.
- Policy regularization is unstable in clean states and weak against optimal adversaries; gradient-based training cannot resist stronger attacks.
- Future work: optimize the adversarial networks used in training, explore more robust training methods combining high efficiency and good results, and apply them to MARL algorithms other than QMIX.

## Relevance to Survey
A survey-style, empirical bridge paper that systematically transfers four single-agent state-robustness techniques (gradient-based adversary, policy regularization, ATLA, PA-AD) into cooperative MARL (QMIX). It connects the state/observation-perturbation robustness line (SA-MDP / SA-RL, RADIAL, ATLA, PA-AD) to c-MARL robustness, and explicitly references robust Markov games with model uncertainty (Zhang et al. [15]), RMA3C (Han et al. [16]), and RomFac (Zhou & Liu [17]). Useful for the survey as a comparative taxonomy of adversarial-training defenses for state-adversarial attacks in cooperative MARL and as an entry point to the c-MARL adversarial-attack evaluation literature.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — A. Adversarial Attack and Adversarial Training in SARL]_

"There are mainly three types of adversarial attack and training methods to bolster the robustness of SARL. 1) Modifying the loss function. Zhang et al. [2] alter the loss function of the training stage with regularization, making it more consistent with the latent mathematical relations of the reinforcement learning problem. Oikarinen et al. [3] propose RADIAL-RL to derive the adversarial loss. 2) Applying heuristic attacks. Pattanaik et al. [4] use attacks for machine learning image recognition, e.g., FGSM [5], PGD [6], etc., on the state observation of the agent. 3) Training a network for the adversary. Tretschk et al. [7] attack the agent sequentially using the most current adversarial attack method, Adversarial Transformer Network (ATN) [8], which learns to create the assault and is simple to integrate into the policy network. Zhang et al. [9] propose ATLA, and Sun et al. [10] propose PA-AD, both utilizing an opponent that generates the optimal adversary to teach the agent to be resilient to various attack strengths."

> _[Section II, Related Work — B. Adversarial Attack in MARL]_

"Attacks on multi-agent systems and evaluation frameworks have been a significant focus of much of the existing research on MARL robustness. Guo et al. [11] propose MARLSafe, a robustness testing framework for c-MARL algorithms that evaluates three aspects of attacks, including the one involving state observation. Pham et al. [12] propose the first model-based adversarial attack framework for c-MARL. Lin et al. [13] and Hu and Zhang [14], respectively, choose to apply attacks on one of the agents in the multi-agent system and during a few of the timesteps, proving that even if the agents are not all attacked the whole time, they still perform poorly."

> _[Section II, Related Work — C. Adversarial Training in MARL]_

"Zhang et al. [15] propose robust Markov games that consider model uncertainty and improve model performance using function approximation and mini-batch updates. To overcome the difficulty of training resilient policies under adversarial state perturbations based on a gradient descent ascent technique, Han et al. [16] offer the Robust Multi-Agent Adversarial Actor-Critic (RMA3C) algorithm. Zhou and Liu [17] propose a brand-new objective function and a repetitive regularization method to enhance MARL's defending ability. Shi et al. [18] consider generalizability and use random noise to bridge the real and virtual settings."

### Cited references (resolved from the paper's bibliography)
- **[2]** H. Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020 (Advances in Neural Information Processing Systems, vol. 33, pp. 21024–21037).
- **[3]** T. Oikarinen, W. Zhang, A. Megretski, L. Daniel, T.-W. Weng. *Robust deep reinforcement learning through adversarial loss.* NeurIPS 2021 (vol. 34, pp. 26156–26167).
- **[4]** A. Pattanaik, Z. Tang, S. Liu, G. Bommannan, G. Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* arXiv:1712.03632, 2017.
- **[5]** I. J. Goodfellow, J. Shlens, C. Szegedy. *Explaining and harnessing adversarial examples.* arXiv:1412.6572, 2014.
- **[6]** A. Madry, A. Makelov, L. Schmidt, D. Tsipras, A. Vladu. *Towards deep learning models resistant to adversarial attacks.* arXiv:1706.06083, 2017.
- **[7]** E. Tretschk, S. J. Oh, M. Fritz. *Sequential attacks on agents for long-term adversarial goals.* arXiv:1805.12487, 2018.
- **[8]** S. Baluja, I. Fischer. *Learning to attack: Adversarial transformation networks.* AAAI 2018 (vol. 32).
- **[9]** H. Zhang, H. Chen, D. Boning, C.-J. Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **[10]** Y. Sun, R. Zheng, Y. Liang, F. Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL.* arXiv:2106.05087, 2021.
- **[11]** J. Guo, Y. Chen, Y. Hao, Z. Yin, Y. Yu, S. Li. *Towards Comprehensive Testing on the Robustness of Cooperative Multi-agent Reinforcement Learning.* IEEE/CVF CVPR 2022, pp. 115–122.
- **[12]** N. H. Pham, L. M. Nguyen, J. Chen, H. T. Lam, S. Das, T.-W. Weng. *Evaluating Robustness of Cooperative MARL: A Model-based Approach.* arXiv:2202.03558, 2022.
- **[13]** J. Lin, K. Dzeparoska, S. Q. Zhang, A. Leon-Garcia, N. Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020, pp. 62–68.
- **[14]** Y. Hu, Z. Zhang. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv:2205.09362, 2022.
- **[15]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020 (vol. 33, pp. 10571–10583).
- **[16]** S. Han, S. Su, S. He, S. Han, H. Yang, F. Miao. *What is the Solution for State Adversarial Multi-Agent Reinforcement Learning?* arXiv:2212.02705, 2022.
- **[17]** Z. Zhou, G. Liu. *RomFac: A robust mean-field actor-critic reinforcement learning against adversarial perturbations on states.* arXiv:2205.07229, 2022.
- **[18]** H. Shi, G. Liu, K. Zhang, Z. Zhou, J. Wang. *MARL Sim2real Transfer: Merging Physical Reality With Digital Virtuality in Metaverse.* IEEE Transactions on Systems, Man, and Cybernetics: Systems, vol. 53, no. 4, pp. 2107–2117, April 2023.
