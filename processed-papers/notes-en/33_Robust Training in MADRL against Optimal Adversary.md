# 33. Robust Training in Multiagent Deep Reinforcement Learning Against Optimal Adversary

## Metadata
- **Title**: Robust Training in Multiagent Deep Reinforcement Learning Against Optimal Adversary
- **Authors**: Weiran Guo, Guanjun Liu, Ziyuan Zhou, Jiacun Wang, Ying Tang, Miaomiao Wang
- **Affiliation**: School of Computer Science and Technology, Tongji University (Shanghai, China); Department of Computer Science and Software Engineering, Monmouth University (NJ, USA); Department of Electrical and Computer Engineering, Rowan University (NJ, USA); Space Optoelectronic Measurement and Perception Lab, Beijing Institute of Control Engineering (Beijing, China)
- **Venue**: IEEE Transactions on Systems, Man, and Cybernetics: Systems, Vol. 55, No. 7, July 2025
- **Link/arXiv**: https://doi.org/10.1109/TSMC.2025.3561276 (DOI 10.1109/TSMC.2025.3561276)

## Taxonomy
- **Robustness / perturbation type targeted**: State / observation adversarial perturbation (attacks on agents' observations within an ℓ-norm budget ϵ); sensor noise / virtual-to-physical (sim-to-real) gap
- **Method paradigm**: Adversarial training (train-time attack injection), max-min / worst-case return optimization, policy-level adversary (actor-director), zero-sum game between victim and adversarial agents
- **Keywords**: Industry 5.0, multiagent reinforcement learning, robustness, state-adversarial attack, MAPDA, CTDE, SEAC

## TL;DR
The paper proposes MAPDA, a train-time multiagent policy-directed adversarial attack that converts the optimal state adversary into an equivalent optimal policy adversary (via an actor-director architecture), and injects it during training to robustify CTDE-based (QMIX, VDN) and shared-experience (SEAC) MADRL algorithms against strong state-observation attacks.

## Problem & Motivation
MADRL is highly sensitive to minor changes in agents' observations: models trained in a virtual environment degrade in the physical world because of sensor noise, and malicious state adversarial attacks (far more potent than random noise) can severely deteriorate performance, threatening productivity and manufacturing safety in Industry 5.0 settings. Although robust single-agent DRL (SADRL) has been studied extensively, its techniques cannot be directly replicated in MADRL: MADRL has a much larger state/action space (causing gradient explosion/vanishing) and agents' relationships are coupled rather than independent. Prior MADRL robustness efforts either only attack (without offering defenses), have large adversary state/action spaces with high compute demand and no assured outcomes, lack optimal attacks during training, lack a theoretical foundation, or are limited to one algorithm type or environment type. This work fills that gap with a generally applicable robust-training method using an optimal adversary.

## Robustness Setting
- **Threat model / uncertainty set**: A set of victim agents M ⊆ N has its observations perturbed within an attacking budget ϵ: Bⁱ_ϵ = {oⁱ′ ∈ Oⁱ : ‖oⁱ′ − oⁱ‖ ≤ ϵ}. The paper introduces the State-Adversarial Dec-POMDP (SA-Dec-POMDP) and then the Policy-Adversarial Dec-POMDP (PA-Dec-POMDP), proving that state attacks are equivalent to policy attacks (Property 1) and that the optimal state adversary corresponds to an optimal policy adversary lying at the boundary of the adversarial-policy set (Properties 2–3). A "director" (policy adversary over m adversarial agents) selects the worst perturbing direction; an "actor" generates the perturbation (FGSM/PGD) at the farthest edge of the adversarial-policy set. The adversarial agents receive reward rⁱ⁻ = −rⁱ, forming a zero-sum game with the victims.
- **Setting**: Cooperative MADRL (CTDE via QMIX/VDN; shared-experience SEAC); centralized training with decentralized execution and decentralized actor-critic; online training; train-time adversarial robustification.

## Method
- Formulate robust training as a max-min worst-case return: max over joint policy π, min over perturbed joint observation õ, of the discounted return (Eq. 11). Decompose into an inner-minimum (find the optimal/strongest attack) and an outer-maximum (train victims to be robust against it) problem.
- Inner minimum (MAPDA): translate state attacks into policy attacks. Prove equivalence of state and policy perturbations (Property 1), define the adversarial-policy set Cⁱ_ϵ(πⁱ), and show the optimal adversary lies at its boundary (Properties 2–3). Reduce the perturbation space from |O| to |A|, lowering training complexity. Build an actor-director attack: director f outputs ā = f(o) minimizing victim reward; actor g pulls the policy to the farthest allowed edge, producing õ = g(f(o), o).
- For VDN/QMIX, exploit the Mixing operation (sum for VDN; monotonic mixing network for QMIX) so the local optimal adversary is also the global optimal adversary; for SEAC the relatively independent training makes local and global optima equivalent. This justifies combining per-agent optimal adversaries into the optimal joint adversary.
- Implementation: the director can use the victims' algorithm or another MADRL algorithm (e.g., MAPPO); the actor uses FGSM (or PGD) with cross-entropy-style multiclass loss L = J(Q/π for action a) − J(Q/π for direction ā) (Eqs. 20–21; shared loss for VDN/QMIX, individual loss for SEAC). Algorithm 1 generates train-time perturbations.
- Outer maximum (robust training, Algorithm 2): train victim agents and adversarial agents simultaneously, both updated by their MADRL algorithms with the standard loss functions (Eq. 4 for QMIX/VDN; Eq. 7 for SEAC). The robustified variants are named RoQMIX, RoVDN, and RoSEAC.

## Theoretical Contributions
- Property 1: equivalence between perturbing an agent's observation and perturbing its policy (in terms of action distributions), for both individual agents and the whole system.
- Property 2: equivalence between the optimal state adversary and the optimal policy adversary (both minimize the resulting value).
- Property 3: existence of an optimal adversarial policy at the boundary of the adversarial-policy set Cⁱ_ϵ(πⁱ) (extending the SADRL boundary result of [16] to the multiagent decomposition).
- Argument that the combination of local optimal policy adversaries yields the global optimal policy adversary in VDN/QMIX (via IGM/Mixing monotonicity) and in SEAC (independent training).
- Otherwise mostly empirical; no convergence or sample-complexity guarantees are claimed (the authors note future work to "strengthen the theoretical foundation").

## Experiments
- **Environment/Benchmark**: Two Industry-5.0-related environments — MARL_CAVs [36] (connected & autonomous vehicles vs. human-driven vehicles on a ramp; 3 CAVs and 5 CAVs scenarios) and robotic-warehouse RWARE [37] (2ag and 4ag robots in a 10×11 grid) — plus the general SMAC [38] environment (2 Stalkers versus 1 Spine Crawler, 2s_versus_1sc).
- **Baselines**: Original (non-robust) QMIX, VDN, SEAC; FGSM-trained models [18]; PGD-trained models [35]; ATLA-trained models [14] (directly trains the state adversary with action space matching victim state-space dimensions, via MAPPO).
- **Evaluation metrics**: Episode total reward (return) and collision frequency (crash rate) in MARL_CAVs; average return per episode in RWARE; average return per episode and win rate in SMAC; percentage performance improvement of robust models over robustness-free models. Testing uses random noise, Gaussian noise, and FGSM attacks at increasing perturbation sizes, plus clean (attack-free) observations.

## Key Results
- Under mild perturbations (random/Gaussian noise), robust models give consistent but subtle gains: e.g., RoQMIX improves return over original QMIX from a minimum of 2.7% (5CAVs, Gaussian) up to 9.8% (5CAVs, random); RoVDN from 1.7% (5CAVs, random) to 12.6% (3CAVs, Gaussian); RoSEAC from 1.9% (4ag, random) to 14.5% (4ag, Gaussian).
- Under stronger FGSM attacks the improvements are much larger: RoQMIX from a minimum of 9% (5CAVs) up to 857.6% (3CAVs); RoVDN from 40.8% (3CAVs) to 63.4% (5CAVs); RoSEAC from 51.8% (2ag) to 176.5% (4ag).
- Generalization: robust models degrade minimally as perturbation intensity increases and retain a noticeable advantage even under strong FGSM; the method also transfers to SMAC (2s_versus_1sc), surpassing baselines under FGSM, showing applicability beyond industrial settings.
- Clean observations: the robust method outperforms robustly-trained baselines in most cases and sometimes the non-robust models; occasional small clean-observation degradation is attributed to overfitting the generated noise but stays within acceptable limits. Crash-rate improvements are limited because all methods already handle basic anti-crash tasks under clean observations.

## Limitations & Future Work
- The robust models do not show significant crash-rate improvement under random/Gaussian noise (only slight improvement under FGSM), and may exhibit a minor performance decrease under clean observations due to overfitting the generated noise.
- The theoretical foundation is acknowledged to need strengthening (future work to develop validated, more reliable robust training methods).
- Future work: explore state adversarial attacks further, improve the MAPDA algorithm, design more efficient training frameworks, optimize the search for the best attack strategies, account for physical influences (e.g., friction) during deployment, and investigate additional attack forms such as backdoor attacks integrated with the methodology.

## Relevance to Survey
This paper sits on the "state/observation adversarial perturbation" main line of robust MARL and the "adversarial training (train-time attack injection) + worst-case/minimax" method line. It connects state-adversarial RL theory (SA-MDP, optimal/boundary adversary from PAAD) to the multiagent CTDE and shared-experience settings, extending the SADRL optimal-policy-adversary result of Sun et al. (PAAD) to cooperative MADRL (QMIX/VDN/SEAC). It is closely related to other state-adversarial MADRL works (Han et al. SA-MARL, Zhou et al. robust mean-field actor-critic, Guo et al. robust QMIX, Yu et al. ADMAC) and to the broader robust-SADRL / SA-MDP literature (Zhang et al., ATLA), making it a useful node for the observation-robustness and adversarial-training portions of the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — A. Robust SADRL]_

"With the discovery of the vulnerability of SADRL to state adversarial attacks, numerous attacks targeting SADRL have emerged. Kos and Song [17] applied two commonly used attacks in deep learning, namely random noise and fast gradient sign method (FGSM) [18], to SADRL, demonstrating the effectiveness of these attacks in SADRL. Building on this, Tretschk et al. [19] proposed a network-based approach using the adversarial transformer network (ATN) [20] to generate state perturbations, successfully misleading the agent's actions. Zhang et al. [14] introduced the alternating training with learned adversaries (ATLA) attack framework, aiming to minimize the agent's rewards through state adversarial perturbations. To address the drawback of high training dimensionality in ATLA, Sun et al. [16] proposed PAAD, which generates state perturbations at the policy level. These achievements primarily focus on state adversarial attacks against SADRL, but there is a lack of detailed discussions on how to defend against these attacks."

"In order to resist state adversarial attacks on SADRL, such as those mentioned above, existing research has proposed a series of defense methods. For example, Zhang et al. [13] introduced a method of adding a regularization term to the loss function to minimize the distance between the attacked policy and the normal policy, ensuring that the agent does not exhibit overly abnormal behavior after an attack. Shen et al. [21] leveraged the smooth transitional properties of continuous state spaces and propose training a smooth policy to enhance robustness. Liu et al. [22] presented a novel approach that uses only benign samples, significantly reducing training costs and risks. Robust SADRL has been applied in real-world traffic scenarios such as autonomous driving [23]. These studies are specific to SADRL and have not been validated in MADRL."

> _[Section II, Related Work — B. State Adversarial Attacks on MADRL]_

"Many studies have demonstrated the vulnerability of MADRL against attacks. Even when only a few agents are attacked in a small number of timesteps, the performance of MADRL will be greatly impacted [24]. To evaluate the robustness of MADRL, Pham et al. [25] presented a model-based method that generates strong attacks. Lin et al. [11] proposed model-based strong attacks, but they are limited to the same category of MADRL algorithms and thus not necessarily effective in other types of algorithms (e.g., experience-sharing). Zhou and Liu [26] used differential evolution to attack important agents and make multiagent systems much less effective with precision attacks. However, this work only focuses on attacks on algorithms in the CTDE paradigm. All these works investigate adversarial attacks on MADRLs but do not offer a solution on how to counter the attacks."

> _[Section II, Related Work — C. Robust Training in MADRL]_

"Han et al. [27] proposed a robust MADRL that addresses adversarial state attacks. However, the adversary's state and action spaces in this method are large, leading to much computating resources demand and no assurance of favorable outcomes. Shi et al. [28] utilized random noise to connect virtual and real environments. However, their method lacks the inclusion of optimal attacks during training. Zhou et al. [29] introduced a novel objective function and a repetitive regularization technique to strengthen the defensive capabilities of MADRL. However, the effectiveness of the regularization method needs improvement. Additionally, the method does not investigate novel approaches to perturbing the agents' observations. Guo et al. [30] investigated various methods to transfer robust training techniques from SADRL to MADRL. Although the work makes QMIX more robust, it lacks a theoretical foundation. Yu et al. [31] proposed the active defense multiagent communication (ADMAC) framework, which specifically addresses the defense of MADRL in communication-critical tasks. However, its generality is limited."

"To fill the above research gap, we propose the MAPDA attack framework to enhance MADRL's robustness. Our approach is not limited to one type of MADRL algorithm (e.g., CTDE-based algorithms like QMIX and VDN) or one type of environment (e.g., reward-dense type); it can be applied to various settings."

> _[Section I, Introduction — single-agent robustness background]_

"There has been a lot of investigation into robust measures in single-agent deep reinforcement learning (SADRL) [12], [13], [14], [15], but it is not desirable to directly replicate the experience of SADRL into MADRL. Robust training of MADRL algorithms is of more challenges compared to SADRL due to the following reasons. 1) MADRL has a larger state and action space than SADRL, leading to undesired training results and causing problems such as gradient explosion or gradient vanishing. 2) The relationship among agents is not independent but associated. An MADRL problem is not a simple copy-and-paste of multiple SADRL problems, and agents' interactions must be considered."

### Cited references (resolved from the paper's bibliography)
- **[11]** J. Lin, K. Dzeparoska, S. Q. Zhang, A. Leon-Garcia, N. Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[12]** V. Behzadan, A. Munir. *Whatever does not kill deep reinforcement learning, makes it stronger.* arXiv:1712.09344, 2017.
- **[13]** H. Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[14]** H. Zhang, H. Chen, D. Boning, C.-J. Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary (ATLA).* ICLR 2021.
- **[15]** M. Yang, G. Liu, Z. Zhou, J. Wang. *Probabilistic automata-based method for enhancing performance of deep reinforcement learning systems.* IEEE/CAA Journal of Automatica Sinica, 2024.
- **[16]** Y. Sun, R. Zheng, Y. Liang, F. Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL (PAAD).* ICLR 2022.
- **[17]** J. Kos, D. Song. *Delving into adversarial attacks on deep policies.* ICLR 2017.
- **[18]** I. J. Goodfellow, J. Shlens, C. Szegedy. *Explaining and harnessing adversarial examples (FGSM).* ICLR 2015.
- **[19]** E. Tretschk, S. J. Oh, M. Fritz. *Sequential attacks on agents for long-term adversarial goals.* ACM Computer Science in Cars Symposium 2018.
- **[20]** S. Baluja, I. Fischer. *Learning to attack: Adversarial transformation networks (ATN).* AAAI 2018.
- **[21]** Q. Shen, Y. Li, H. Jiang, Z. Wang, T. Zhao. *Deep reinforcement learning with robust and smooth policy.* ICML 2020.
- **[22]** Z. Liu et al. *Towards robust and safe reinforcement learning with benign off-policy data.* ICML 2023.
- **[23]** X. He, W. Huang, C. Lv. *Trustworthy autonomous driving via defense-aware robust reinforcement learning against worst-case observational perturbations.* Transportation Research Part C: Emerging Technologies, 2024.
- **[24]** Y. Hu, Z. Zhang. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv:2205.09362, 2022.
- **[25]** N. H. Pham, L. M. Nguyen, J. Chen, H. T. Lam, S. Das, T.-W. Weng. *Evaluating robustness of cooperative MARL: A model-based approach.* OpenReview, 2023.
- **[26]** Z. Zhou, G. Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* Frontiers in Artificial Intelligence and Applications, IOS Press, 2023.
- **[27]** S. Han, S. Su, S. He, S. Han, H. Yang, F. Miao. *What is the solution for state-adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2023.
- **[28]** H. Shi, G. Liu, K. Zhang, Z. Zhou, J. Wang. *MARL Sim2Real transfer: Merging physical reality with digital virtuality in metaverse.* IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2023.
- **[29]** Z. Zhou, G. Liu, M. Zhou. *A robust mean-field actor-critic reinforcement learning against adversarial perturbations on agent states.* IEEE Transactions on Neural Networks and Learning Systems, 2024.
- **[30]** W. Guo, G. Liu, Z. Zhou, L. Wang, J. Wang. *Enhancing the robustness of QMIX against state-adversarial attacks.* Neurocomputing, 2024.
- **[31]** L. Yu, Y. Qiu, Q. Yao, Y. Shen, X. Zhang, J. Wang. *Robust communicative multi-agent reinforcement learning with active defense (ADMAC).* AAAI 2024.
