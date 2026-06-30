# 61. Certifiably Robust Policy Learning against Adversarial Multi-Agent Communication

## Metadata
- **Title**: Certifiably Robust Policy Learning against Adversarial Multi-Agent Communication
- **Authors**: Yanchao Sun, Ruijie Zheng, Parisa Hassanzadeh, Yongyuan Liang, Soheil Feizi, Sumitra Ganesh, Furong Huang
- **Affiliation**: University of Maryland, College Park; JPMorgan AI Research; Shanghai AI Lab
- **Venue**: ICLR 2023
- **Link/arXiv**: https://github.com/umd-huang-lab/cmarl_ame.git (code)

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial communication attacks (test-time arbitrary perturbation of a subset of inter-agent messages); related to sparse / ℓ0 input attacks; also covers natural / unintentional perturbations
- **Method paradigm**: Certified robustness via randomized ablation + ensemble (message-ensemble policy with majority vote / coordinate-wise median); provable defense
- **Keywords**: communicative MARL (CMARL), adversarial communication, certifiable defense, randomized ablation, message ensemble, Dec-POMDP

## TL;DR
The paper proposes Ablated Message Ensemble (AME), a certifiable defense for communicative MARL that aggregates actions from multiple randomly ablated subsets of received messages (majority vote for discrete actions, coordinate-wise median for continuous), provably guaranteeing performance as long as fewer than half of the messages (C < (N−1)/2) are arbitrarily corrupted.

## Problem & Motivation
Communication lets cooperative MARL agents share information and act better, but a communication-dependent policy can be drastically misled if messages are perturbed or corrupted at test time (e.g., a hacked IoT device altering "Bomb" into "Gold"). Prior empirical defenses for adversarial communication in MARL do not fully address three challenges: (I) attacks can be stealthy and strong (a false message far from the original yet semantically meaningful, not captured by the ℓp threat model), (II) the attacker can be adaptive to the victim and significantly reduce its reward, and (III) there can be multiple attackers/messages colluding. High-stakes applications also need robustness with theoretical guarantees, which empirical defenses lack — motivating a provably robust defense.

## Robustness Setting
- **Threat model / uncertainty set**: At test time, well-trained policies are executed; an attacker may arbitrarily perturb up to C of the N−1 communication messages received by a victim agent (sparse attack), with no assumption on the attack algorithm and no bound on per-message magnitude. The victim does not know which messages are adversarial. Assumption 3.1: C < (N−1)/2 (fewer than half the messages corrupted). Related to a constrained ℓ0 perturbation of the policy input (perturbing C messages of dimension d differs by up to dC dimensions).
- **Setting**: cooperative (Dec-POMDP, shared reward); decentralized execution with inter-agent communication; defense applied to a trained policy at test time (online execution); defense is independent of the underlying communication policy and policy-learning algorithm.

## Method
- **Message-ablation policy (training, Algorithm 1)**: train a single policy π̂ : Γ × M^k → A that maps the agent's interaction history and a randomly sampled k-ablation message subset ([m]_k, uniform over all k-samples) to an action, optimizing cumulative reward in a clean environment with any RL algorithm. The hyperparameter k controls a robustness/performance trade-off.
- **Message-ensemble policy (defense, Algorithm 2)**: at test time, aggregate the base actions π̂ produces over k-samples — argmax majority vote for discrete actions (Eq. 1) and coordinate-wise Median for continuous actions (Eq. 2) — so the executed action reflects the consensus of benign messages.
- **Robustness certificates**: for discrete actions, Condition 4.4 (Dominating Benign Votes: u_max(m) > C(N−1,k) − C(N−1−C,k)) guarantees the ensemble action lies in the benign action set A_benign (Theorem 4.5) and the reward is no lower than the worst clean reward of π̂ (Corollary C.1). For continuous actions, Condition 4.6 (Dominating Benign Samples: C(N−1−C,k) > ½C(N−1,k)) guarantees the action lies in Range(A_benign) (Theorem 4.7), with a bounded reward gap (ϵ_R + γ V_max ϵ_P)/(1−γ) under smooth dynamics (Theorem C.3).
- **Scaling up (Section 4.3)**: a partial-sample D-ensemble policy uses D randomly chosen k-samples instead of all C(N−1,k), giving high-probability guarantees (probability p_D increasing with D).

## Theoretical Contributions
- Action certificate for discrete action space (Theorem 4.5): under Condition 4.4, the ensemble policy always selects a benign action despite arbitrary perturbation of up to C messages, independent of the attack algorithm.
- Reward certificate for discrete action space (Corollary C.1): cumulative reward under attack is no lower than the lowest clean cumulative reward of π̂ over random benign k-samples, for any attacker with C < (N−1)/2.
- Action certificate for continuous action space (Theorem 4.7): under Condition 4.6, the ensemble action lies in Range(A_benign).
- Reward certificate for continuous action space (Theorem C.3): bounded value gap (ϵ_R + γ V_max ϵ_P)/(1−γ) for an ϵ_R,ϵ_P-discrepant policy.
- High-probability guarantees for the partial-sample D-ensemble variant (Theorems C.4 and C.5, with explicit probabilities p_D).

## Experiments
- **Environment/Benchmark**: Four CMARL environments — FoodCollector (N=9, discrete/continuous action, pre-defined communication), InventoryManager (N=10 distributors, 3 products, continuous action, pre-defined communication), MARL-MNIST (N=9, discrete action, learned communication), Traffic Junction (N=10 cars, discrete action, learned communication).
- **Baselines**: (1) Vanilla — training without defense using all benign messages; (2) AT — adversarial training (alternating an adaptive RL attacker and the agent, as in Zhang et al. 2021). AME uses k=2 (largest solution to Eq. 6 for C=2).
- **Evaluation metrics**: Victim's local reward (precision for MARL-MNIST) under no attack and varying number of adversaries C, against Heuristic attacks (random/Perm/Swap/Flip) and Learned Adaptive (white-box RL worst-case) attacks; plus hyperparameter studies over ablation size k and sample size D. Results averaged over 5 random seeds.

## Key Results
- Vanilla and AT rewards drop drastically under attack; under strong adaptive attackers they sometimes perform worse than a non-communicative agent (communication can be a "double-edged sword"). AT does not beat Vanilla because it cannot adapt to arbitrary perturbations of several messages.
- With k=2, AME's reward under C=1 or C=2 is similar to its no-attack reward (matching the theory for N=9, N=10), and AME outperforms all baselines in all four environments under both non-adaptive and adaptive attacks.
- Even at C=3 (beyond the theoretical guarantee), AME remains more robust than Vanilla and AT.
- Hyperparameter studies confirm the robustness/performance trade-off: larger k raises natural reward but lowers robustness; smaller D lowers reward under attack but stays more robust than baselines (D=1 equals the un-ensembled ablation policy, robust to heuristic but less to adaptive attacks).

## Limitations & Future Work
- AME requires several conditions to hold (Conditions 4.4 / 4.6); although they can be quantified and checked in practice, future work aims to relax them or to learn a communication policy that satisfies them.
- Message ablation may sacrifice some natural performance (typical robustness/accuracy trade-off).
- Continuous-action guarantees rely on smoothness of environment dynamics and concentrated benign actions (small ϵ_R, ϵ_P); future work could optimize π̂ to minimize ϵ_R, ϵ_P.
- AME exploits information redundancy/consensus among benign messages; learning a communication policy that produces such redundancy is suggested as an extension. Training-time communication poisoning is left as future direction.

## Relevance to Survey
This is a key paper on the "communication robustness / adversarial communication" line of robust MARL and is, per the authors, the first certifiable defense in MARL against communication attacks. It connects the certified-robustness method line (randomized ablation/smoothing, ensemble defenses) with cooperative CMARL (Dec-POMDP), and contrasts with empirical/adversarial-training defenses and with ℓp-bounded threat models. It bridges single-agent robust RL (state/observation perturbation, adversarial training, certified RL) and MARL safety/fault tolerance under a strong sparse (ℓ0-like) threat model.

## Related Work (verbatim excerpts from the paper)

> _[Section 1, Introduction]_

"Although adversarial attacks and defenses have been extensively studied in supervised learning (Madry et al., 2018; Zhang et al., 2019) and reinforcement learning (Zhang et al., 2020b; Sun et al., 2022), there has been little discussion on the robustness issue against adversarial communication in MARL problems. Some recent works (Blumenkamp & Prorok, 2020; Xue et al., 2022; Mitchell et al., 2020) take the first step to investigate adversarial communications in MARL and propose several defending methods. However, these empirical defenses do not fully address the aforementioned challenges, and are not guaranteed to be robust, especially under adaptive attacks. In high-stakes applications, it is also important to ensure robustness with theoretical guarantees and interpretations."

> _[Section 1, Introduction]_

"In this paper, we address all aforementioned challenges by proposing a certifiable defense named Ablated Message Ensemble (AME), that can guarantee the performance of agents when a fraction of communication messages get arbitrarily perturbed. Inspired by the ensemble methods which are proved to be the optimal defense against poisoning attacks under the iid sample setting (Wang et al., 2022), we propose to defend by ablation and ensemble of message sets, which tackles the challenging interactive decision-making under partially observable environments with correlated message samples. [...] Levine & Feizi (2020) use a similar randomized ablation idea to defend against ℓ0 attacks in image classification. However, they provide high-probability guarantee for classification, which is not suitable for sequential decision-making problems, as the guaranteed probability decreases when it propagates over timesteps."

> _[Section 5, Related Work — "Certifiable Defenses"]_

"Certifiable Defenses. For more reliable application of deep learning, many approaches have been developed to certify the performance of neural networks, including semidefinite programming-based defenses (Raghunathan et al., 2018a;b), convex relaxation of neural networks (Gowal et al., 2019; Zhang et al., 2018; Wong & Kolter, 2018; Zhang et al., 2020a; Gowal et al., 2018), randomized smoothing of a classifier (Cohen et al., 2019; Hayes, 2020), etc. Most existing works focus on the ℓp threat model where the perturbation is small in ℓp norm, while we consider a different and practical threat model as discussed in Section 2."

> _[Section 5, Related Work — "Adversarial Robustness of RL Agents"]_

"Adversarial Robustness of RL Agents. Appendix A introduces existing adversarial attacks on single-agent and multi-agent problems. To improve the robustness of agents, adversarial training (i.e., introducing adversarial agents to the system during training (Pinto et al., 2017; Phan et al., 2021; Zhang et al., 2021; Sun et al., 2022)) and network regularization (Zhang et al., 2020b; Shen et al., 2020; Oikarinen et al., 2021) are empirically shown to be effective under ℓp attacks, although such robustness is not theoretically guaranteed. In an effort to certify RL agents' robustness, some approaches (Lütjens et al., 2020; Zhang et al., 2020b; Oikarinen et al., 2021; Fischer et al., 2019) apply network certification tools to bound the Q networks. Kumar et al. (2021) and Wu et al. (2022) apply randomized smoothing (Cohen et al., 2019) to RL for provable robustness."

> _[Section 5, Related Work — "Adversarial Attacks and Defenses in CMARL"]_

"Adversarial Attacks and Defenses in CMARL. Appendix A discusses literature of learning effective communication among agents (Foerster et al., 2016; Sukhbaatar et al., 2016; Das et al., 2019). Note that the focus of this paper is defending against adversarial perturbations on existing communications, which is orthogonal to the concrete communication strategy. Recently, the existence of adversarial communication in MARL has attracted increasing attention. Blumenkamp & Prorok (2020) show that in a cooperative game, communication policies of some self-interest agents can hurt other agents' performance. To achieve robust communication, Mitchell et al. (2020) adopt a Gaussian Process-based probabilistic model to compute the posterior probabilities that whether each partner is truthful. Tu et al. (2021) investigate the vulnerability of multi-agent autonomous systems against ℓp communication attacks on vision tasks. Xue et al. (2022) propose to learn an anomaly detector and a message reconstructor to recover the true messages, and train two populations of defenders and attackers to improve the generalizability of defense. But in our formulation, the attacker may arbitrarily replace the messages so that recovering the true message is infeasible."

> _[Section 5, Related Work]_

"To the best of our knowledge, our AME is the first certifiable defense in MARL against communication attacks. Moreover, we consider a strong threat model where up to half of the communication messages can be arbitrarily corrupted, capturing many realistic types of attacks."

> _[Appendix A, Additional Related Work — "Other Attacks in RL and MARL"]_

"Other Attacks in RL and MARL Adversarial attacks and defenses in RL systems have recently attracted more and more attention, and are considered in many different scenarios. The majority of related work on adversarial RL focuses on directly attacking a victim by perturbing its observations (Huang et al., 2017; Oikarinen et al., 2021; Zhang et al., 2020b; Sun et al., 2022; Korkmaz, 2021; 2022; 2023; Liang et al., 2022) or actions (Tessler et al., 2019; Pinto et al., 2017). However, an attacker may not have direct access to the specific victim's observation or action. In this case, indirect attacks via other agents can be an alternative. Gleave et al. (2020); Liu et al. (2022) propose to attack the victim by changing the other agent's actions. Therefore, even if the victim agent has well-protected sensors, the attacker can still influence it by manipulating other under-protected agents. But the intermediary agent whose actions are altered will obtain sub-optimal reward, which makes the attack noticeable and less stealthy. In contrast, we consider the scenario where an attacker alters the communication messages sent from some other agents to the victim without changing the behaviors of these agents. In this case, it is relatively hard for the victim to identify the attacks. Training-time attacks, or poisoning (Behzadan & Munir, 2017; Huang & Zhu, 2019; Rakhsha et al., 2020; Sun et al., 2021) propose to manipulate the training data such that the agent learns a bad or target policy, different from evasion attacks that deprave a well-trained policy."

### Cited references (resolved from the paper's bibliography)
- **[Madry et al., 2018]** Madry, Makelov, Schmidt, Tsipras, Vladu. *Towards deep learning models resistant to adversarial attacks.* ICLR 2018.
- **[Zhang et al., 2019]** H. Zhang, Yu, Jiao, Xing, El Ghaoui, Jordan. *Theoretically principled trade-off between robustness and accuracy.* ICML 2019.
- **[Zhang et al., 2020b]** H. Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Sun et al., 2022]** Sun, Zheng, Liang, Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL.* ICLR 2022.
- **[Blumenkamp & Prorok, 2020]** Blumenkamp, Prorok. *The emergence of adversarial communication in multi-agent reinforcement learning.* 2020.
- **[Xue et al., 2022]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* AAMAS 2022.
- **[Mitchell et al., 2020]** Mitchell, Blumenkamp, Prorok. *Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication.* 2020.
- **[Wang et al., 2022]** Wang, Levine, Feizi. *Lethal dose conjecture on data poisoning.* NeurIPS 2022.
- **[Levine & Feizi, 2020]** Levine, Feizi. *Robustness certificates for sparse adversarial attacks by randomized ablation.* AAAI 2020.
- **[Raghunathan et al., 2018a]** Raghunathan, Steinhardt, Liang. *Certified defenses against adversarial examples.* arXiv:1801.09344, 2018.
- **[Raghunathan et al., 2018b]** Raghunathan, Steinhardt, Liang. *Semidefinite relaxations for certifying robustness to adversarial examples.* NeurIPS 2018.
- **[Gowal et al., 2019]** Gowal, Dvijotham, Stanforth, Bunel, Qin, Uesato, Arandjelovic, Mann, Kohli. *Scalable verified training for provably robust image classification.* ICCV 2019.
- **[Zhang et al., 2018]** H. Zhang, Weng, Chen, Hsieh, Daniel. *Efficient neural network robustness certification with general activation functions.* NeurIPS 2018.
- **[Wong & Kolter, 2018]** Wong, Kolter. *Provable defenses against adversarial examples via the convex outer adversarial polytope.* ICML 2018.
- **[Zhang et al., 2020a]** H. Zhang, Chen, Xiao, Gowal, Stanforth, Li, Boning, Hsieh. *Towards stable and efficient training of verifiably robust neural networks.* ICLR 2020.
- **[Gowal et al., 2018]** Gowal, Dvijotham, Stanforth, Bunel, Qin, Uesato, Arandjelovic, Mann, Kohli. *On the effectiveness of interval bound propagation for training verifiably robust models.* arXiv:1810.12715, 2018.
- **[Cohen et al., 2019]** Cohen, Rosenfeld, Kolter. *Certified adversarial robustness via randomized smoothing.* ICML 2019.
- **[Hayes, 2020]** Hayes. *Extensions and limitations of randomized smoothing for robustness guarantees.* CVPR Workshops 2020.
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Phan et al., 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Zhang et al., 2021]** H. Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[Shen et al., 2020]** Shen, Li, Jiang, Wang, Zhao. *Deep reinforcement learning with robust and smooth policy.* ICML 2020.
- **[Oikarinen et al., 2021]** Oikarinen, W. Zhang, Megretski, Daniel, Weng. *Robust deep reinforcement learning through adversarial loss.* NeurIPS 2021.
- **[Lütjens et al., 2020]** Lütjens, Everett, How. *Certified adversarial robustness for deep reinforcement learning.* CoRL 2020.
- **[Fischer et al., 2019]** Fischer, Mirman, Stalder, Vechev. *Online robustness training for deep reinforcement learning.* arXiv:1911.00887, 2019.
- **[Kumar et al., 2021]** Kumar, Levine, Feizi. *Policy smoothing for provably robust reinforcement learning.* arXiv:2106.11420, 2021.
- **[Wu et al., 2022]** Wu, Li, Huang, Vorobeychik, Zhao, Li. *Crop: Certifying robust policies for reinforcement learning through functional smoothing.* ICLR 2022.
- **[Foerster et al., 2016]** Foerster, Assael, De Freitas, Whiteson. *Learning to communicate with deep multi-agent reinforcement learning.* NeurIPS 2016.
- **[Sukhbaatar et al., 2016]** Sukhbaatar, Fergus, et al. *Learning multiagent communication with backpropagation.* NeurIPS 2016.
- **[Das et al., 2019]** Das, Gervet, Romoff, Batra, Parikh, Rabbat, Pineau. *Tarmac: Targeted multi-agent communication.* ICML 2019.
- **[Tu et al., 2021]** Tu, T. Wang, J. Wang, Manivasagam, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[Huang et al., 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv:1702.02284, 2017.
- **[Korkmaz, 2021]** Korkmaz. *Investigating vulnerabilities of deep neural policies.* UAI 2021.
- **[Korkmaz, 2022]** Korkmaz. *Deep reinforcement learning policies learn shared adversarial features across MDPs.* AAAI 2022.
- **[Korkmaz, 2023]** Korkmaz. *Adversarial robust deep reinforcement learning requires redefining robustness.* AAAI 2023.
- **[Liang et al., 2022]** Liang, Sun, Zheng, Huang. *Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning.* NeurIPS 2022.
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Gleave et al., 2020]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* ICLR 2020.
- **[Liu et al., 2022]** Liu, Chakraborty, Huang. *Controllable attack and improved adversarial training in multi-agent reinforcement learning.* NeurIPS 2022 Workshop on Trustworthy and Socially Responsible ML.
- **[Behzadan & Munir, 2017]** Behzadan, Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* MLDM 2017.
- **[Huang & Zhu, 2019]** Y. Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* GameSec 2019.
- **[Rakhsha et al., 2020]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching via environment poisoning: Training-time adversarial attacks against reinforcement learning.* ICML 2020.
- **[Sun et al., 2021]** Sun, Huo, Huang. *Vulnerability-aware poisoning mechanism for online RL with unknown dynamics.* ICLR 2021.
