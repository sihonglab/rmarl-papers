# 156. SoK: Adversarial Machine Learning Attacks and Defences in Multi-Agent Reinforcement Learning

## Metadata
- **Title**: SoK: Adversarial Machine Learning Attacks and Defences in Multi-Agent Reinforcement Learning
- **Authors**: Maxwell Standen, Junae Kim, Claudia Szabo
- **Affiliation**: Defence Science and Technology Group; The University of Adelaide
- **Venue**: Not specified (arXiv preprint, 2023)
- **Link/arXiv**: arXiv:2301.04299v1 [cs.LG] 11 Jan 2023

## Taxonomy
- **Robustness / perturbation type targeted**: Execution-time adversarial (AML) attacks against MARL/DRL: action perturbation, observation perturbation, communication perturbation, malicious communications, natural adversarial examples; defences including adversarial training, competitive training, robust learning, certified robustness, input alteration
- **Method paradigm**: Systematization of Knowledge (SoK) / survey; taxonomy construction (Attack Vectors); new modelling frameworks (OA-POSG, AR-POSG); literature review methodology
- **Keywords**: Adversarial Machine Learning, MARL, Attack Vectors, communication attacks, adversarial policies, POSG frameworks

## TL;DR
A systematization-of-knowledge survey of execution-time adversarial machine learning attacks and defences against MARL (and DRL/MAL), introducing a cyber-security-inspired "Attack Vector" taxonomy and two new modelling frameworks (Observation-Adversarial POSG and Action-Robust POSG) that capture multiple simultaneous attack vectors plus their tempo, magnitude, and location.

## Problem & Motivation
DRL has moved from single-agent fully-observable games to partially-observable multi-agent settings used in safety-critical applications (cyber defence, power networks, autonomous driving), but remains vulnerable to AML attacks that exploit the underlying neural networks. While prior surveys have covered AML for single-agent DRL, to the authors' knowledge no work covers AML attacks against MARL, and existing classifications (e.g., MDP-based taxonomies, information-based taxonomies) cannot capture attacks unique to MARL such as attacks on inter-agent communications in cooperative MARL and adversarial policies in competitive MARL. There is a critical need for MARL practitioners to understand both the attacks and the defences before deployment.

## Robustness Setting
- **Threat model / uncertainty set**: Execution-time adversarial attacks defined as the intentional manipulation of aspects of an environment to reduce the performance of a target network and cause a target agent to take irrational/self-defeating actions. Adversary knowledge is classified as white-box, black-box, or no-information; attack objective as untargeted, targeted (action), state-based, or reward-based. Five Attack Vectors: Action Perturbation, Observation Perturbation, Communication Perturbation, Malicious Communications, Natural Adversarial Examples.
- **Setting**: Cooperative / competitive / mixed multi-agent environments; centralized and decentralized training, centralized and decentralized execution; focus restricted to execution-time (not training-time) attacks; surveys offline DRL and cooperative decentrally-executable multi-agent deep learning.

## Method
- Conducts a systematic literature review (based on Kitchenham's methodology with forward snowballing): two search strings over top conferences since 2010, 350 candidate papers narrowed to 85 by accept/reject criteria, then 57 in the final set.
- Proposes a classification of AML attacks along three properties: Attack Vector (means of attack), Information (adversary knowledge: white-box / black-box / none), and Objective (untargeted, targeted, state-based, reward-based).
- Identifies and analyzes five Attack Vectors and surveys representative attacks and target algorithms for each, including which RL framework each paper used.
- Proposes a classification of AML defences: Adversarial Training, Competitive Training, Robust Learning, Adversarial Detection, Input Alteration, Memory, Regularisation, plus when each is applied (during training, before/during/after an attack).
- Reviews existing RL frameworks (MDP, POMDP, DEC-POMDP, SG, POSG, PR-MDP, NR-MDP, SA-MDP) and their ability to model each Attack Vector, then proposes two new frameworks: Observation-Adversarial POSG (OA-POSG) and Action-Robust POSG (AR-POSG), which add per-agent adversarial operators with tempo (Θ), magnitude (∆), and scope (Σ) parameters.

## Theoretical Contributions
None / mostly survey and conceptual framework. The paper contributes formal definitions of two new modelling frameworks (OA-POSG as an 11-tuple, AR-POSG as a 10-tuple) that extend the POSG with per-agent observation/action adversarial functions, but provides no convergence, sample-complexity, or certified-robustness results.

## Experiments
- **Environment/Benchmark**: Not applicable — this is a survey (SoK). No new experiments are run; it tabulates experimental platforms used by surveyed papers (e.g., MuJoCo, OpenAI Gym, ALE, Point-Goal/Car-Goal, StarCraft II, Multi-View ShapeNet).
- **Baselines**: Not applicable (compares against prior surveys: Ilahi et al., Bai et al., Chen et al., Ren et al.).
- **Evaluation metrics**: Not applicable (discusses reward, win rate, and proposes counterfactual regret as a better metric for evaluating Action Perturbation attacks).

## Key Results
- Surveys 57 papers and finds many AML attacks/defences for single-agent DRL but few for MARL; competitive-MARL attacks (e.g., adversarial policies) and communication attacks are often overlooked.
- Standard frameworks (MDP, POMDP, DEC-POMDP) cannot model any of the identified Attack Vectors; SG and POSG can model Malicious Communications and Natural Adversarial Examples but not Communication or Action/Observation Perturbations directly.
- The proposed OA-POSG and AR-POSG are the only frameworks (to the authors' knowledge) capable of modelling Communication Perturbation attacks and multiple simultaneous attack vectors, while capturing tempo, magnitude, and location.
- Identifies gaps: white-box Malicious Communications, patch attacks, action-/state-based and untargeted Communication Perturbation attacks, action-/state-based Natural Adversarial Examples, attacks targeting multiple agents, and quantifying defence generalisation.

## Limitations & Future Work
- Data collection only captured papers that considered improved robustness in the context of defending against an AML attack; the Robust Learning category could be extended to approaches not tied to specific adversary capabilities (e.g., robustness to non-stationary environments).
- Online adversarial training is excluded because it must first handle data-poisoning attacks before being a viable defence.
- Future directions: AML attacks against multiple agents (cascading effects, switching targeted agent, homogeneous vs heterogeneous systems, shared vs individual rewards); combining Attack Vectors; quantifying defence generalisation across attack types; using attacker metrics (tempo, preferred vectors) to craft defences; defences during (not only before) an attack.

## Relevance to Survey
This is a foundational systematization for the "adversarial attacks / defences in MARL" branch of the robust MARL landscape. It connects the communication-robustness, adversarial-policy (competitive MARL), observation/action-perturbation, and certified-robustness lines, and explicitly relates robust-RL framework variants (SA-MDP, PR-MDP/NR-MDP, robust adversarial RL/RARL) to multi-agent settings. Its proposed OA-POSG/AR-POSG frameworks are directly relevant to formalizing robust MARL threat models, and its taxonomy is a useful organizing scaffold for the survey's attack/defence sections.

## Related Work (verbatim excerpts from the paper)

> _[Section 1, Introduction]_

"Despite existing research interest [9], there are many challenges with the application of AML techniques to Multi-Agent Reinforcement Learning (MARL), Multi-Agent Learning (MAL), and DRL, including discovering effective attacks [10–13] and ﬁnding defences that can generalise to unseen attacks [14, 15]."

"AML attacks exist in a large potential solution space. Attacks against supervised image classiﬁers use approximation techniques such as Fast Gradient Sign Method (FGSM) [16] to ﬁnd adversarial examples for single static images. DRL involves many sequential observations and ﬁnding an effective attack requires knowing when, how, and what to attack. Huang et al. [11] showed that approaches such as FGSM attacks were able to attack DRL by altering the observation at every time step. Subsequent research has found attacks that reduced the number of perturbed time-steps required to degrade the agent performance [10, 12, 13], demonstrating the importance of discovering the best attack timing."

"Adversarial training may defend against AML attacks on supervised learning and DRL [15]. Adversarial training uses both original and adversarially produced examples to retrain a vulnerable algorithm. In supervised learning, the retrained algorithm is then more robust against similar future attacks [17]. However, adversarial training in DRL produces a narrow robustness only against the speciﬁc attack being used and thus is unable to generalise to other attacks [14]."

"There is a critical need for MARL practitioners to understand the AML attacks and defences [18]. A number of previous works have surveyed the state of AML as applied to DRL [9, 15, 19–21]. However, to the best of our knowledge, there is no work concerning the application of AML against MARL."

> _[Section 2.2, Related Work]_

"There are multiple surveys that focus on AML for DRL [9, 15, 19, 36]. However our analysis has found that these surveys have limited coverage of AML as applied to MARL and MAL [9]. Several surveys focus strongly on Observation Perturbation attacks [9, 19, 36], including on the information used to craft an attack and when an attack should occur. In our analysis of previous work that classiﬁes AML attacks [9, 15] speciﬁcally against MARL, we found no surveys that covered AML defences for MARL; we have identiﬁed several that covered AML defences for DRL [9, 15, 19, 36]. Our work is unique due to its focus on AML execution-time attacks and defences for DRL, MAL and MARL."

"MAL is a major focus of our work and attacks against it can be highly effective as discussed by Ilahi et al. [9]. Their survey discusses an Observation Perturbation attack against c-MARL by Lin et al. [37] and in competitive environments by Gleave et al. [38]. To build from this work, we have found additional work that investigates attacks against cooperative MARL [37, 39] and cooperative multi-agent supervised learning [40]. We also found a number of AML attacks in competitive MARL [41–45], which is often overlooked due to the focus of AML on direct Observation Perturbations."

"Observation Perturbation attacks against DRL algorithms have been covered by a number of surveys [9, 19, 36]. These have largely focused on the work inspired by Huang et al. [11]. Discovering effective Observation Perturbation attacks with white and black-box information was covered by Chen et al. [19]. Discovering when to attack is a unique problem for AML attacks against DRL and approaches to this question were covered by Ilahi et al. [9]. We believe our work presents the most extensive survey of Observation Perturbation attacks against DRL to date."

"DRL practitioners must understand potential AML attacks and researchers assist in this requirement through the classiﬁcation of AML attacks such as those proposed in previous work [9, 15]. Ilahi et al. [9] presents a taxonomy based on Markov Decision Processes (MDPs) to categorise an attack, which uses the major categories of reward space, action space, state space, and agent space to cover both test-time and training-time attacks. Bai et al. [15] classiﬁed attacks based on the information an adversary requires to create the attack. However, neither of these classiﬁcations support the categorisation of AML attacks unique against MARL, such as attacks against communications in cooperative MARL and adversarial policies in competitive MARL. To address this gap, we have developed a classiﬁcation of AML attacks against MARL and DRL that covers the means of attack, the aim of the attack, and the knowledge of the target required by an adversary."

"No AML defences for MARL have been covered by previous surveys to the best of our knowledge. To ﬁnd related work, we consider surveys that cover AML defences for DRL [9, 15, 19, 36]. Ilahi et al. [9] propose a taxonomy that features a number of classiﬁcations including adversarial training, defensive distillation, robust learning, and adversarial detection, however it fails to consider Competitive Training, which aims to use a competitor in the environment to train the DRL agent. Our work addresses this gap. Chen et al. [19] also use Input Alteration, which includes the minor categories of various adversarial training, as the alteration covers both test and training time. They further propose two other categories of altering objective function and altering network structure to improve the robustness against AML attacks. However, the examples they use for AML defence are from supervised learning. Bai et al. [15] focussed on adversarial training which was a category in both Ilahi et al. [9] and Chen et al. [19], however Bai et al. restructured adversarial training as a competitive multi-agent problem. This move towards using multi-agent perspectives to better understand AML attacks is one that we expand upon. Adversarial Training, Input Alteration, and Robust Learning were categories used by Ren et al. [36]. We have drawn from these existing classiﬁcations and our own analyses and present a classiﬁcation system for defences for both MARL and DRL."

"Our paper is unique in focusing on execution-time AML attacks against DRL and defences against those attacks. Ilahi et al. [9] covered both execution-time and training-time attacks and defences. Chen et al. [19] focused on execution-time attacks against DRL but looked at AML defences for supervised learning. Bai et al. [15] focused on adversarial training as a defence against execution-time attacks in both DRL and supervised learning. Ren et al. [36] covered AML attacks and defences against the whole deep learning ﬁeld including supervised learning and DRL. Our unique focus allows us to better analyse the problem of defending a DRL algorithm from execution-time attacks. Related work has covered aspects of AML applied to DRL, however there remain gaps in the coverage of existing surveys around AML attacks and defences for MARL, and the classiﬁcation of AML attacks and defence when applied to DRL and MAL."

### Cited references (resolved from the paper's bibliography)
- **[9]** I. Ilahi, M. Usama, et al. *Challenges and Countermeasures for Adversarial Attacks on Deep Reinforcement Learning.* IEEE Transactions on Artificial Intelligence 2021.
- **[10]** Y.-C. Lin, Z.-W. Hong, et al. *Tactics of Adversarial Attack on Deep Reinforcement Learning Agents.* IJCAI 2017.
- **[11]** S. Huang, N. Papernot, et al. *Adversarial Attacks on Neural Network Policies.* ICLR 2017.
- **[12]** J. Sun, T. Zhang, et al. *Stealthy and Efficient Adversarial Attacks against Deep Reinforcement Learning.* AAAI 2020.
- **[13]** Y. Qiaoben, X. Zhou, et al. *Strategically-timed State-Observation Attacks on Deep Reinforcement Learning Agents.* Workshop on Adversarial Machine Learning 2021.
- **[14]** J. Kos, D. Song. *Delving into adversarial attacks on deep policies.* ICLR 2017.
- **[15]** T. Bai, J. Luo, et al. *Recent Advances in Adversarial Training for Adversarial Robustness.* IJCAI 2021.
- **[16]** I. J. Goodfellow, J. Shlens, et al. *Explaining and Harnessing Adversarial Examples.* ICLR 2015.
- **[17]** A. Madry, A. Makelov, et al. *Towards Deep Learning Models Resistant to Adversarial Attacks.* ICLR 2018.
- **[18]** R. S. Siva Kumar, M. Nyström, et al. *Adversarial Machine Learning-Industry Perspectives.* IEEE Security and Privacy Workshops 2020.
- **[19]** T. Chen, J. Liu, et al. *Adversarial attack and defense in reinforcement learning-from AI security view.* Cybersecurity 2019.
- **[20]** A. Prorok, M. Malencia, et al. *Beyond Robustness: A Taxonomy of Approaches towards Resilient Multi-Robot Systems.* 2021.
- **[21]** O. Eigner, S. Eresheim, et al. *Towards Resilient Artificial Intelligence: Survey and Research Issues.* IEEE International Conference on Cyber Security and Resilience 2021.
- **[36]** K. Ren, T. Zheng, et al. *Adversarial Attacks and Defenses in Deep Learning.* Engineering 2020.
- **[37]** J. Lin, K. Dzeparoska, et al. *On the Robustness of Cooperative Multi-Agent Reinforcement Learning.* IEEE Security and Privacy Workshops 2020.
- **[38]** A. Gleave, M. Dennis, et al. *Adversarial Policies: Attacking Deep Reinforcement Learning.* ICLR 2020.
- **[39]** W. Xue, W. Qiu, et al. *Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning.* AAMAS 2022.
- **[40]** J. Tu, T. Wang, et al. *Adversarial Attacks On Multi-Agent Communication.* IEEE/CVF ICCV 2021.
- **[41]** T. Fujimoto, A. P. Pedersen. *Adversarial Attacks in Cooperative AI.* 2021.
- **[42]** J. Uesato, B. O'Donoghue, et al. *Adversarial risk and the dangers of evaluating against weak attacks.* ICML 2018.
- **[43]** W. Guo, X. Wu, et al. *Adversarial Policy Learning in Two-player Competitive Games.* ICML 2021.
- **[44]** A. Pan, Y. Lee, et al. *Improving Robustness of Reinforcement Learning for Power System Control with Adversarial Training.* 2021.
- **[45]** T. Phan, T. Gabor, et al. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
