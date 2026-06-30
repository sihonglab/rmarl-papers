# 152. Attacking Cooperative Multi-Agent Reinforcement Learning by Adversarial Minority Influence

## Metadata
- **Title**: Attacking Cooperative Multi-Agent Reinforcement Learning by Adversarial Minority Influence
- **Authors**: Simin Li, Jun Guo, Jingqiao Xiu, Yuwei Zheng, Pu Feng, Xin Yu, Jiakai Wang, Aishan Liu, Yaodong Yang, Bo An, Wenjun Wu, Xianglong Liu
- **Affiliation**: State Key Lab of Software Development Environment, Beihang University; Zhongguancun Laboratory; Institute of Data Space, Hefei Comprehensive National Science Center; Institute of Artificial Intelligence, Peking University; Nanyang Technological University, Singapore
- **Venue**: Neural Networks (Preprint, 2024)
- **Link/arXiv**: arXiv:2302.03322v3 [cs.LG]; code at https://github.com/DIG-Beihang/AMI

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents / adversarial policy attack on cooperative MARL (test-time, black-box, policy-based attack where a single agent in the environment influences victim agents); used as a worst-case robustness evaluation / algorithmic testing tool.
- **Method paradigm**: Adversarial policy attack, mutual-information-based unilateral influence (information-theoretic decomposition), reinforcement-learning-driven target oracle, PPO/GAE optimization, contraction-operator (Bellman) convergence analysis.
- **Keywords**: Multi-agent reinforcement learning, trustworthy reinforcement learning, adversarial attack, adversarial policy, minority influence, c-MARL robustness

## TL;DR
The paper proposes Adversarial Minority Influence (AMI), a practical black-box, policy-based attack in which a single adversarial agent unilaterally misleads a majority of cooperative victims into a jointly worst-case cooperation, by combining a unilateral influence filter (derived from decomposing mutual information) with a targeted adversarial oracle (an RL agent that generates worst-case victim targets); AMI is the first adversarial-policy attack demonstrated on real-world robot swarms.

## Problem & Motivation
Cooperative MARL (c-MARL) is increasingly used in security-sensitive applications, so assessing its worst-case performance under adversarial interference is crucial before real-world deployment. Existing observation-based attacks on c-MARL require white-box access to victim parameters and the ability to manipulate agent observations arbitrarily (e.g., pixel-wise camera manipulation), which is impractical in real-world settings like autonomous driving. Prior policy-based (adversarial policy) attacks were studied only in two-agent competitive games and neglected two c-MARL-specific challenges: (1) the influence problem — all agents mutually influence each other, so attacking one victim affects others and makes maximal deviation hard; and (2) the cooperation problem — merely perturbing victim actions arbitrarily or toward locally suboptimal cases does not guarantee a globally / jointly worst-case cooperative failure.

## Robustness Setting
- **Threat model / uncertainty set**: A single adversarial agent participates within the c-MARL environment as one of the agents (the first agent is selected as adversary). The attacker is black-box: it cannot manipulate victim observations, cannot choose which agent to control, and has no access to victim models (architectures, weights, gradients) or victim rewards. Following CTDE, the adversary may access global state and reward only during training; during deployment it relies solely on its local observation history. Victim joint policies are fixed during deployment. Sim2Real paradigm used for physical deployment.
- **Setting**: cooperative victims (c-MARL) with an adversarial agent; CTDE for the attack; test-time attack (not training-time poisoning/backdoor); online RL for the adversary, with both simulated and real-world deployment.

## Method
- **Unilateral Influence Filter**: Starts from mutual information I(aᵅₜ; âᵛₜ₊₁,ᵢ | sₜ, aᵛₜ) as a bilateral agent-wise relation metric, then decomposes it into a "majority influence" term (entropy conditioned on the adversary action) and a "minority influence" term (entropy not conditioned on the adversary action). Because victim parameters are fixed while the adversary policy is learned, maximizing mutual information lets the attacker overfit/comply with victim policies (majority influence), yielding weak attacks. AMI keeps only the unilateral minority-influence term, which marginalizes the adversary action so the attacker cannot cater to victim policies. This is generalized to minimizing a distance d(·,·) between the expected victim policy under the adversary and a target distribution D.
- **Targeted Adversarial Oracle (TAO)**: An RL agent πᵗ (using global state as input, only at training time) that co-adapts with the attacker to generate globally / jointly worst-case target actions D for each victim. TAO adapts to the adversary's current perturbation budget (more aggressive targets when influence is strong, smaller effective perturbations when influence is weak). Optimized with PPO and GAE.
- **Overall training**: The unilateral influence Iᵅₜ toward TAO's target action is added as an auxiliary reward: r_AMI = rᵅ + λ·Iᵅ, where λ trades off the adversary's own reward against influence on victims. The adversary's policy πᵅ is trained with PPO using advantages from r_AMI (Algorithm 1). Distance metric d is ℓ₁ to a one-hot target for discrete control and target-action probability for continuous control.
- The framework defines Bellman operators Bᵗ (for TAO) and Bᵅ (for the adversary), each adding dependence on the other's action to avoid non-stationarity.

## Theoretical Contributions
- Proves that the Bellman operator Bᵗ for TAO is a contraction on a Banach space and, by Banach's fixed-point theorem (finite state/action spaces, infinitely-often visitation), tabular Qᵗ updates converge to the optimal Qᵗ,* (Appendix B).
- Proves analogously that the adversary's Bellman operator Bᵅ is a contraction and that tabular Qᵅ updates converge to Qᵅ,* (Appendix C).
- Provides the detailed derivation showing the minority-influence term equals minimizing a KL divergence between the victim policy and a uniform distribution (Appendix A), motivating the unilateral influence formulation.
- Convergence guarantees hold only in the tabular case, motivating PPO as the practical solver.

## Experiments
- **Environment/Benchmark**: (1) Real-world multi-robot rendezvous with 10 e-puck2 robots in an indoor playground; (2) StarCraft Multi-Agent Challenge (SMAC), six discrete-control tasks; (3) Multi-Agent Mujoco (MAMujoco), six continuous-control tasks. Victim policies trained with MAPPO; first agent selected as adversary.
- **Baselines**: Single-agent adversarial policy methods adapted to multi-agent — Gleave et al., Wu et al., Guo et al. — and the multi-agent observation-based attack GMA (Zan et al.). Also compared against using raw mutual information as the influence metric.
- **Evaluation metrics**: Adversary reward — defined per environment as (1) maximizing ally loss / minimizing enemy loss for SMAC, (2) minimizing agent speed in the +x direction for MAMujoco, (3) maximizing Euclidean distance between all agents for rendezvous. Results over 5 random seeds with 95% confidence intervals; real-world tests run 10 times per method with paired-samples t-test.

## Key Results
- AMI outperforms all baselines in both simulated and real-world rendezvous; the real-world improvement is statistically significant (p < .05) and on average 5.43 higher adversary reward than the best-performing baseline. AMI is the only method that fools a victim into grouping with the adversary instead of with the majority.
- In simulation, AMI outperforms competing methods in 10 out of 12 tasks across SMAC and MAMujoco.
- Behavior analysis (10m vs 11m) shows AMI induces "delayed arrival" and "unfocused fire" among victims; TAO generates more deterministic targets for highly susceptible agents and less deterministic (untargeted) goals for insusceptible ones.
- Ablations: both the unilateral and targeted properties are needed; removing the unilateral property (using bilateral influence) can even underperform Gleave et al.; performance is stable across distance metrics; using raw mutual information is ineffective and worsens with larger λ; performance is non-monotonic in λ.

## Limitations & Future Work
- Theoretical convergence guarantees hold only in the tabular case; the practical algorithm relies on PPO and an opponent-modeling network pϕ.
- Large λ can introduce critic-training instability and accumulate opponent-modeling errors, so λ must be tuned (performance is non-monotonic in λ).
- The work assumes fixed victim policies during deployment and a single adversarial agent (the first agent); broader future directions (e.g., defenses) are noted implicitly via the goal of strengthening resilience of cooperative multi-agent systems. Specific future-work items are otherwise Not specified.

## Relevance to Survey
This paper sits on the "adversarial agents / adversarial policy attacks" line of robust MARL, specifically targeting cooperative MARL (c-MARL) as a worst-case robustness evaluation and algorithmic testing tool. It connects the single-agent adversarial-policy literature (Gleave et al., Wu et al., Guo et al.) to the multi-agent cooperative setting, contrasts with observation-perturbation attacks and adversarial-communication attacks, and emphasizes practical black-box attacks validated on real robot swarms. As an attack/testing paper it complements the defense and certified-robustness lines by characterizing the threat surface that robust c-MARL methods must withstand.

## Related Work (verbatim excerpts from the paper)

> _[Section 2.1, Overview of Adversarial Attacks]_

"Initially proposed in the field of computer vision, adversarial attacks consist of carefully crafted perturbations that, while imperceptible to humans, can deceive deep neural networks (DNNs) into making incorrect predictions [27, 28, 29]. Given a DNN Fθ, a clean image x, a perturbed image xadv, and the ground truth label y, an adversarial example can be formulated as follows: Fθ (xadv) ̸= y s.t. ∥x −xadv∥≤ϵ. (1) In this formulation, ∥·∥ represents a distance metric used to constrain the distance between x and xadv by ϵ. Subsequently, it was demonstrated that reinforcement learning (RL) is also susceptible to adversarial attacks [18, 30, 31]. Owing to the sequential decision-making nature of RL, adversarial attacks in this context aim to generate a perturbation policy πα that minimizes the victim's cumulative reward P t γtrt, which can be expressed as: min πα X t γtrt. (2) Adversarial attacks are important to distinguish as test-time attacks, where the adversary targets a specific victim without participating in the training process. As another line of research, training-time attacks interfere with victim training, resulting in trained victims either failing to perform well (poisoning attack) [32, 33] or executing adversary-specified actions when specific triggers are present (backdoor attack) [34, 35, 36]. Note that our method is a test-time attack, and is not related to training-time attacks."

> _[Section 2.2, RL Attacks by Observation Perturbation]_

"Test-time perturbation of RL observations can deceive the policy of RL agents, causing them to execute suboptimal actions and fail to achieve their goals. For single-agent RL attacks, early research employed heuristics such as preventing victims from selecting the best action [18] or choosing actions with the lowest value at critical time steps [30, 31]. Later work framed the adversary and victim within an MDP [19], enabling the optimal observation perturbation to be learned as an action within the current state using an RL agent [37, 38]. For c-MARL attacks, Lin et al. [16] proposed a two-step attack that first learns a worst-case attack policy and then employs a gradient-based attack [39] to execute it. [17] generated attacks on one victim and transfer it to the rest of the victims. However, they assume attacker can modify victim observations and has white-box access to victim parameters, which can be impractical in real world Another line of research, termed adversarial communication, targets communicative c-MARL by sending messages to victim agents that cause failure upon receiving the adversarial message. Adversarial messages can be added to representations [40] or learned by the adversary [41, 42, 43]. However, these methods are inapplicable when victim agents do not communicate, a common assumption in many mainstream c-MARL algorithms [1, 3, 2]."

> _[Section 2.3, RL Attacks by Adversarial Policy]_

"Distinct from observation-based attacks, adversarial policy attacks do not necessitate access to victim observations or parameters (black-box). Rather, they introduce an adversarial agent whose actions are designed to deceive victim agents, causing them to take counterintuitive actions and ultimately fail to achieve their goals. In this paper, the terms "policy-based attack" and "adversarial policy" are used interchangeably. Gleave et al. [20] were the first to introduce adversarial policy in two-agent zero-sum games. This approach was latter applied to multi-agent consensus game, where agents have similar, but non-identical objectives [44]. Subsequent research has enhanced adversarial policy by exploiting victim agent vulnerabilities. Wu et al. [21] induced larger deviations in victim actions by perturbing the most sensitive feature in victim observations, identified through a saliency-based approach. However, larger deviations in victim actions do not necessarily correspond to strategically worse policies. Guo et al. [22] extended adversarial policies to general-sum games by simultaneously maximizing the adversary's reward and minimizing the victim's rewards. Yet, none of these studies have considered adversarial policies in c-MARL settings. To better evaluate the performance of our attack in multi-agent adversarial policy scenario, we adapt some observation-based attack in MARL [17] as baselines."

> _[Introduction]_

"While c-MARL has achieved notable success, research has exposed the vulnerability of c-MARL agents to observation-based adversarial attacks [16, 17], wherein adversaries introduce perturbations to an agent's observation, causing it to execute suboptimal actions. Given the interrelated nature of victim actions for cooperation, other c-MARL agents may become disoriented and being non-robust (see Fig. 1). As c-MARL algorithms frequently feature in security-sensitive applications, assessing their worst-case performance against potential adversarial interference is crucial before real world deployment. However, observation-based attacks against c-MARL depend on white-box access to victim and complete control of agent observations, rendering them highly impractical. For instance, in autonomous driving scenarios, it can be prohibitively hard for attackers to access the architectures, weights, and gradients utilized by a vehicle or to introduce arbitrary pixel-wise manipulations to camera input at each timestep [16, 18, 19]."

> _[Introduction]_

"Although policy-based attacks have been investigated in two-agent competitive games [20, 21, 22], these studies have neglected two crucial challenges in c-MARL, resulting in diminished attack efficacy. Ideally, the adversary should influence victims toward a cooperatively inferior policy. This gives rise to two issues: (1) The influence problem, wherein all agents mutually influence one another in c-MARL; consequently, attacking a single victim impacts the policies of other victims as well. In the face of such intricate agent-wise influence, it becomes difficult for the adversary to maximally deviate victim policies and identify the optimal attack strategy. (2) The cooperation problem, which arises as merely perturbing victim actions arbitrarily or toward locally suboptimal cases is insufficient to indicate the failure of cooperative victims. The adversary faces the challenge of exploring and deceiving victims into a long-term, jointly detrimental failure scenario."

### Cited references (resolved from the paper's bibliography)
- **[1]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[2]** Lowe, Wu, Tamar, Harb, Pieter Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[3]** Yu, Velu, Vinitsky, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative, multi-agent games.* arXiv 2021.
- **[16]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[17]** Zan, Zhu, Hu. *Adversarial attacks on cooperative multi-agent deep reinforcement learning: a dynamic group-based adversarial example transferability method.* Complex & Intelligent Systems 2023.
- **[18]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[19]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[20]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv 2019.
- **[21]** Wu, Guo, Wei, Xing. *Adversarial policy training against deep reinforcement learning.* USENIX Security 2021.
- **[22]** Guo, Wu, Huang, Xing. *Adversarial policy learning in two-player competitive games.* ICML 2021.
- **[27]** Szegedy, Zaremba, Sutskever, Bruna, Erhan, Goodfellow, Fergus. *Intriguing properties of neural networks.* arXiv 2013.
- **[28]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* arXiv 2014.
- **[29]** Carlini, Wagner. *Towards evaluating the robustness of neural networks.* IEEE Symposium on Security and Privacy (SP) 2017.
- **[30]** Kos, Song. *Delving into adversarial attacks on deep policies.* arXiv 2017.
- **[31]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* arXiv 2017.
- **[32]** Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* International Conference on Decision and Game Theory for Security 2019.
- **[33]** Wu, Li, Xu, Zhang, Kailkhura, Kenthapadi, Zhao, Li. *COPA: Certifying robust policies for offline reinforcement learning against poisoning attacks.* arXiv 2022.
- **[34]** Behzadan, Hsu. *Sequential triggers for watermarking of deep reinforcement learning policies.* arXiv 2019.
- **[35]** Kiourti, Wardega, Jha, Li. *TrojDRL: Trojan attacks on deep reinforcement learning agents.* arXiv 2019.
- **[36]** Wang, Javed, Wu, Guo, Xing, Song. *BackdooRL: Backdoor attack against competitive reinforcement learning.* arXiv 2021.
- **[37]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv 2021.
- **[38]** Sun, Zheng, Liang, Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL.* arXiv 2021.
- **[39]** Papernot, McDaniel, Jha, Fredrikson, Celik, Swami. *The limitations of deep learning in adversarial settings.* IEEE European Symposium on Security and Privacy (EuroS&P) 2016.
- **[40]** Tu, Wang, Wang, Manivasagam, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[41]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* arXiv 2021.
- **[42]** Blumenkamp, Prorok. *The emergence of adversarial communication in multi-agent reinforcement learning.* CoRL 2021.
- **[43]** Mitchell, Blumenkamp, Prorok. *Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication.* arXiv 2020.
- **[44]** Figura, Kosaraju, Gupta. *Adversarial attacks in consensus-based multi-agent reinforcement learning.* American Control Conference (ACC) 2021.
