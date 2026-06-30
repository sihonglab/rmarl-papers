# 44. Wolfpack Adversarial Attack for Robust Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Wolfpack Adversarial Attack for Robust Multi-Agent Reinforcement Learning
- **Authors**: Sunwoo Lee, Jaebak Hwang, Yonghyeon Jo, Seungyul Han
- **Affiliation**: Graduate School of Artificial Intelligence, UNIST, Ulsan, South Korea
- **Venue**: ICML 2025 (Proceedings of the 42nd International Conference on Machine Learning, PMLR 267)
- **Link/arXiv**: arXiv:2502.02844v3 [cs.LG]; code at https://github.com/sunwoolee0504/WALL

## Taxonomy
- **Robustness / perturbation type targeted**: Coordinated adversarial attacks on cooperative MARL via an action-substitution attack policy (worst-case action perturbation through Qtot minimization); attacks target multiple agents simultaneously (an initial agent plus the group of follow-up agents that respond to it)
- **Method paradigm**: Adversarial attack design + adversarial training; LPA-Dec-POMDP formulation, value-based CTDE (VDN/QMIX/QPLEX), credit-assignment-based follow-up group selection (KL divergence), Transformer-based planner for critical attack-step selection
- **Keywords**: Robust MARL, coordinated adversarial attack, Wolfpack attack, CTDE, value decomposition, adversarial training

## TL;DR
The paper proposes the Wolfpack Adversarial Attack — a coordinated MARL attack that first targets one agent and then targets the group of agents that respond to assist it — and the Wolfpack-Adversarial Learning for MARL (WALL) framework that trains policies to defend against it by fostering system-wide collaboration, yielding substantially improved robustness over existing robust MARL methods.

## Problem & Motivation
CTDE value-based MARL methods (VDN, QMIX, QPLEX) suffer from mismatches between training and deployment environments, leading to degraded performance, so improving robustness is a critical focus. Existing adversarial attacks for robust MARL typically target only a single agent per attack and ignore the interdependencies in cooperative settings; this lets non-targeted agents learn to counteract the attack. The authors observe that policies trained under such simplistic attacks remain vulnerable to coordinated attacks where multiple cooperating agents are disrupted simultaneously. They therefore design a coordinated (Wolfpack) attack to expose this weakness and a defense (WALL) to train policies robust to it.

## Robustness Setting
- **Threat model / uncertainty set**: An adversarial attack policy π_adv : S × A × N → A substitutes an agent's chosen action with a worst-case action that minimizes the joint value (ã^i_t = arg min Qtot(s_t, a^i_t, a^{-i}_t)) for targeted agents. The environment is modeled as a Limited Policy Adversary Dec-POMDP (LPA-Dec-POMDP) with a budget K of attacks. The Wolfpack attacker is a special case: an initial attack on a uniformly random agent at step t_init, followed by follow-up attacks on a selected group N_follow-up over the next t_WP steps, with at most K_WP Wolfpack attacks per episode (K = K_WP × (t_WP + 1)).
- **Setting**: fully cooperative; CTDE (value-based, Dec-POMDP); online training; defense via adversarial training on the attacker-induced Dec-POMDP.

## Method
- **Wolfpack Adversarial Attack**: a two-stage coordinated attack. An initial attack disrupts a single (uniformly random) agent at step t_init; follow-up attacks then target the group of agents that responded to the initial attack over steps t_init+1, ..., t_init+t_WP. Attacks substitute targeted agents' actions with the Qtot-minimizing action; the attack budget k_t decreases by 1 per attacking step.
- **Follow-up agent group selection**: after the initial attack, the change in each agent's individual value ∆Q^tot is propagated to individual Q-functions via the CTDE credit-assignment principle (Eq. 1). The original and updated individual Q-functions are softmaxed into distributions, and the m agents with the largest KL divergence between their pre/post-attack action distributions are selected as N_follow-up (Eq. 2), since they exhibit the largest policy changes in response to the initial attack.
- **Planner-based critical attacking-step selection**: initial attack times are chosen to maximize the cumulative Q-value reduction ∆Q^WP_t over the attack window. A Transformer (Decision-Transformer-style) trained on the replay buffer predicts future states/observations to estimate ∆Q^WP_t cheaply; a temperature-T softmax over predicted reductions forms the initial-attack probability P_t,attack (Eq. 3, with L = 20). The Transformer is split into a planning Transformer (training only) and a Q-difference Transformer (evaluation) to reduce cost.
- **WALL defense**: performs value-based CTDE Q-learning (QMIX/VDN/QPLEX) on the LPA-Dec-POMDP induced by the Wolfpack attacker, minimizing the TD loss with an EMA target network (Algorithm 1), so non-attacked agents learn to back up and protect attacked agents (system-wide collaboration).

## Theoretical Contributions
- Mostly empirical / framework-level. The paper shows the proposed Wolfpack attacker is a special case of the adversarial policy of Definition 3.1, hence induces an LPA-Dec-POMDP; and invokes the result of Yuan et al. (2023) that MARL convergence within the LPA-Dec-POMDP is guaranteed. No new convergence/sample-complexity theorems are proved.

## Experiments
- **Environment/Benchmark**: Multi-Agent Particle Environment (MPE) predator-prey scenarios (PP 3/1, PP 6/2, PP 9/3) and StarCraft II Multi-Agent Challenge (SMAC) scenarios (2s3z, 3m, 3s vs 3z, 8m, MMM, 1c3s5z). Main results on QMIX baseline; additional results on VDN and QPLEX.
- **Baselines**: Attackers — Natural (no attack), Random Attack, Evolutionary Generation of Attackers (EGA, Yuan et al. 2023), and the proposed Wolfpack attack. Robust MARL defenses — Vanilla QMIX, RANDOM, RARL (Pinto et al. 2017), RAP (Vinitsky et al. 2020), ROMANCE (Yuan et al. 2023), ERNIE (Bukharin et al. 2024), and the proposed WALL.
- **Evaluation metrics**: Average cumulative reward (MPE) and average test win rate (SMAC), reported as mean ± std over 5 random seeds; ablations on components, step-selection temperature T, and number of follow-up agents m; computational cost and general robustness (Gaussian observation noise, test-time parameter shifts) in appendices.

## Key Results
- The Wolfpack attack is far more disruptive than existing attacks. On SMAC, it reduces Vanilla QMIX from 98.7% (natural) to 39.4% (−59.3%) vs. EGA's −29.1%; in MPE it drops Vanilla QMIX cumulative reward by 87.8 vs. 42.6 (EGA) and 9.5 (Random).
- WALL achieves the best robustness across all attack types and both benchmarks. On SMAC under the Wolfpack attack it reaches 93.4% mean win rate vs. ROMANCE 59.1% and Vanilla QMIX 39.4%; it also outperforms RANDOM (trained vs. Random Attack) and ROMANCE (trained vs. EGA) on their own attack types, and even exceeds baselines in the natural setting in MPE.
- Robustness gains generalize to VDN and QPLEX (e.g., WALL 91.0% vs. Vanilla VDN 44.1% under Wolfpack on SMAC; WALL 92.6% vs. Vanilla QPLEX 33.1%). Ablations confirm random initial-agent selection, KL-based follow-up selection, and planner-based step selection each contribute; m = 3 (8m) / m = 4 (MMM) and T = 0.5 are best. WALL incurs about 30% higher training cost than ROMANCE.

## Limitations & Future Work
- Additional computational overhead from training the Transformer to identify critical steps; the authors argue this is justified since baselines fail to match performance even with extended training.
- Requires hyperparameter tuning to construct the Wolfpack attack, though the method is reported to be not highly sensitive and the ablation study provides practical configuration guidelines.

## Relevance to Survey
Sits on the "adversarial attacks for robust MARL" line, specifically extending action-perturbation / worst-case attack policies (in the LPA-Dec-POMDP formulation of Yuan et al. 2023) from single-agent targeting to coordinated multi-agent targeting in cooperative CTDE. It connects adversarial-training-based robust MARL (RARL, RAP, ROMANCE, ERNIE) with value-decomposition CTDE (VDN/QMIX/QPLEX) and introduces a planning component (Transformer) for critical-step selection. A useful reference for the sub-theme of coordinated/critical-agent adversarial attacks and the corresponding adversarial-training defenses in cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Works — "Robust MARL Strategies"]_

"Robust MARL Strategies: Recent research has focused on robust MARL to address unexpected changes in multi-agent environments. Max-min optimization (Chinchuluun et al., 2008; Han & Sung, 2021) has been applied to traditional MARL algorithms for robust learning (Li et al., 2019; Wang et al., 2022). Robust Nash equilibrium has been redefined to better suit multi-agent systems (Zhang et al., 2020b; Li et al., 2023a). Regularization-based approaches have also been explored to improve MARL robustness (Lin et al., 2020; Li et al., 2023b; Wang et al., 2023; Bukharin et al., 2024), alongside distributional reinforcement learning methods to manage uncertainties (Li et al., 2020; Xu et al., 2021; Du et al., 2024; Geng et al., 2024)."

> _[Section 2, Related Works — "Adversarial Attacks for Resilient RL"]_

"Adversarial Attacks for Resilient RL: To strengthen RL, numerous studies have explored adversarial learning to train policies under worst-case scenarios (Pattanaik et al., 2017; Tessler et al., 2019; Pinto et al., 2017; Chae et al., 2022). These attacks introduce perturbations to various MDP components, including state (Zhang et al., 2020a; 2021a; Everett et al., 2021; Li et al., 2023c; Qiaoben et al., 2024), action (Tan et al., 2020; Lee et al., 2021; Liu et al., 2024), and reward (Wang et al., 2020a; Zhang et al., 2020c; Rakhsha et al., 2021; Xu et al., 2022; Cai et al., 2023; Bouhaddi & Adi, 2023; Xu et al., 2024; Bouhaddi & Adi, 2024). Adversarial attacks have recently been extended to multi-agent setups, introducing uncertainties to state or observation (Han et al., 2022; He et al., 2023; Zhang et al., 2023; Zhou et al., 2023), actions (Yuan et al., 2023), and rewards (Kardes¸ et al., 2011). Further research has applied adversarial attacks to value decomposition frameworks (Phan et al., 2021), selected critical agents for targeted attacks (Yuan et al., 2023; Zhou et al., 2024), and analyzed their effects on inter-agent communication (Xue et al., 2021; Tu et al., 2021; Sun et al., 2023; Yuan et al., 2024)."

> _[Section 2, Related Works — "Model-based Frameworks for Robust RL"]_

"Model-based Frameworks for Robust RL: Model-based methods have been extensively studied to enhance RL robustness (Berkenkamp et al., 2017; Panaganti & Kalathil, 2021; Curi et al., 2021; Clavier et al., 2023; Shi & Chi, 2024; Ramesh et al., 2024), including adversarial extensions (Wang et al., 2020c; Kobayashi, 2024). Transition models have been leveraged to improve robustness (Mankowitz et al., 2019; Ye et al., 2024; Herremans et al., 2024), and offline setups have been explored for robust training (Rigter et al., 2022; Bhardwaj et al., 2024). In multi-agent systems, model-based approaches address challenges like constructing worst-case sets (Shi et al., 2024) and managing transition kernel uncertainty (He et al., 2022)."

> _[Section 1, Introduction — prior-work discussion]_

"To improve learning robustness, single-agent RL methods have explored strategies based on game theory (Yu et al., 2021), such as max-min approaches and adversarial learning (Goodfellow et al., 2014; Huang et al., 2017; Pattanaik et al., 2017; Pinto et al., 2017). In multi-agent systems, simultaneous agent interactions introduce additional uncertainties (Zhang et al., 2021b). To address this, methods like perturbing local observations (Lin et al., 2020), training with adversarial policies for Nash equilibrium (Li et al., 2023a), adversarial value decomposition (Phan et al., 2021), and attacking inter-agent communication (Xue et al., 2021) have been proposed. However, these approaches often target a single agent per attack, overlooking interdependencies in cooperative MARL, making them vulnerable to scenarios where multiple agents are attacked simultaneously."

### Cited references (resolved from the paper's bibliography)
- **[Chinchuluun et al., 2008]** Chinchuluun, Migdalas, Pardalos, Pitsoulis. *Pareto optimality, game theory and equilibria, volume 17.* Springer New York 2008.
- **[Han & Sung, 2021]** Han, Sung. *A max-min entropy framework for reinforcement learning.* NeurIPS 2021.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Wang et al., 2022]** Wang, Wang, Zhou, Velasquez, Zou. *Data-driven robust multi-agent reinforcement learning.* IEEE MLSP 2022.
- **[Zhang et al., 2020b]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Li et al., 2023a]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a bayesian game.* arXiv:2305.12872, 2023.
- **[Lin et al., 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[Li et al., 2023b]** Li, Xu, Guo, Feng, Wang, Liu, Yang, Liu, Lv. *Mir2: Towards provably robust multi-agent reinforcement learning by mutual information regularization.* arXiv:2310.09833, 2023.
- **[Wang et al., 2023]** Wang, Chen, Huang, Zhang, Zhao, Qu. *Regularization-adapted anderson acceleration for multi-agent reinforcement learning.* Knowledge-Based Systems 2023.
- **[Bukharin et al., 2024]** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* NeurIPS 2024.
- **[Li et al., 2020]** Li, Wang, Tian, Jia, Zheng. *Multi-agent reinforcement learning based on value distribution.* Journal of Physics: Conference Series 2020.
- **[Xu et al., 2021]** Xu, Li, Bai, Fan. *Mmd-mix: Value function factorisation with maximum mean discrepancy for cooperative multi-agent reinforcement learning.* IJCNN 2021.
- **[Du et al., 2024]** Du, Chen, Wang, Xing, Yang, Philip, Chang, He. *Robust multi-agent reinforcement learning via bayesian distributional value estimation.* Pattern Recognition 2024.
- **[Geng et al., 2024]** Geng, Xiao, Li, Wei, Wang, Zhao. *Noise distribution decomposition based multi-agent distributional reinforcement learning.* IEEE Transactions on Mobile Computing 2024.
- **[Pattanaik et al., 2017]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* arXiv:1712.03632, 2017.
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Chae et al., 2022]** Chae, Han, Jung, Cho, Choi, Sung. *Robust imitation learning against variations in environment dynamics.* ICML 2022.
- **[Zhang et al., 2020a]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Zhang et al., 2021a]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **[Everett et al., 2021]** Everett, Lütjens, How. *Certifiable robustness to adversarial state uncertainty in deep reinforcement learning.* IEEE Transactions on Neural Networks and Learning Systems 2021.
- **[Li et al., 2023c]** Li, Li, Feng, Wang, Pan. *Ats-o2a: A state-based adversarial attack strategy on deep reinforcement learning.* Computers & Security 2023.
- **[Qiaoben et al., 2024]** Qiaoben, Ying, Zhou, Su, Zhu, Zhang. *Understanding adversarial attacks on observations in deep reinforcement learning.* Science China Information Sciences 2024.
- **[Tan et al., 2020]** Tan, Esfandiari, Lee, Sarkar et al. *Robustifying reinforcement learning agents via action space adversarial training.* American Control Conference (ACC) 2020.
- **[Lee et al., 2021]** Lee, Esfandiari, Tan, Sarkar. *Query-based targeted action-space adversarial policies on deep reinforcement learning agents.* ACM/IEEE 12th International Conference on Cyber-Physical Systems 2021.
- **[Liu et al., 2024]** Liu, Kuang, Wang. *Robust deep reinforcement learning with adaptive adversarial perturbations in action space.* arXiv:2405.11982, 2024.
- **[Wang et al., 2020a]** Wang, Liu, Li. *Reinforcement learning with perturbed rewards.* AAAI 2020.
- **[Zhang et al., 2020c]** Zhang, Ma, Singla, Zhu. *Adaptive reward-poisoning attacks against reinforcement learning.* ICML 2020.
- **[Rakhsha et al., 2021]** Rakhsha, Zhang, Zhu, Singla. *Reward poisoning in reinforcement learning: Attacks against unknown learners in unknown environments.* arXiv:2102.08492, 2021.
- **[Xu et al., 2022]** Xu, Zeng, Singh. *Efficient reward poisoning attacks on online deep reinforcement learning.* arXiv:2205.14842, 2022.
- **[Cai et al., 2023]** Cai, Zhu, Hu. *Reward poisoning attacks in deep reinforcement learning based on exploration strategies.* Neurocomputing 2023.
- **[Bouhaddi & Adi, 2023]** Bouhaddi, Adi. *Multi-environment training against reward poisoning attacks on deep reinforcement learning.* SECRYPT 2023.
- **[Xu et al., 2024]** Xu, Gumaste, Singh. *Reward poisoning attack against offline reinforcement learning.* arXiv:2402.09695, 2024.
- **[Bouhaddi & Adi, 2024]** Bouhaddi, Adi. *When rewards deceive: Counteracting reward poisoning on online deep reinforcement learning.* IEEE International Conference on Cyber Security and Resilience (CSR) 2024.
- **[Han et al., 2022]** Han, Su, He, Han, Yang, Zou, Miao. *What is the solution for state-adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **[He et al., 2023]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* arXiv:2307.16212, 2023.
- **[Zhang et al., 2023]** Zhang, Sun, Huang, Miao. *Safe and robust multi-agent reinforcement learning for connected autonomous vehicles under state perturbations.* arXiv:2309.11057, 2023.
- **[Zhou et al., 2023]** Zhou, Liu, Zhou. *A robust mean-field actor-critic reinforcement learning against adversarial perturbations on agent states.* IEEE Transactions on Neural Networks and Learning Systems 2023.
- **[Yuan et al., 2023]** Yuan, Zhang, Xue, Yin, Chen, Guan, Li, Qian, Yu. *Robust multi-agent coordination via evolutionary generation of auxiliary adversarial attackers.* AAAI 2023.
- **[Kardes¸ et al., 2011]** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research 2011.
- **[Phan et al., 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Zhou et al., 2024]** Zhou, Liu, Guo, Zhou. *Adversarial attacks on multiagent deep reinforcement learning models in continuous action space.* IEEE Transactions on Systems, Man, and Cybernetics: Systems 2024.
- **[Xue et al., 2021]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* arXiv:2108.03803, 2021.
- **[Tu et al., 2021]** Tu, Wang, Wang, Manivasagam, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[Sun et al., 2023]** Sun, Zheng, Hassanzadeh, Liang, Feizi, Ganesh, Huang. *Certifiably robust policy learning against adversarial multi-agent communication.* ICLR 2023.
- **[Yuan et al., 2024]** Yuan, Jiang, Li, Chen, Zhang, Yu. *Robust cooperative multi-agent reinforcement learning via multi-view message certification.* Science China Information Sciences 2024.
- **[Berkenkamp et al., 2017]** Berkenkamp, Turchetta, Schoellig, Krause. *Safe model-based reinforcement learning with stability guarantees.* NeurIPS 2017.
- **[Panaganti & Kalathil, 2021]** Panaganti, Kalathil. *Sample complexity of model-based robust reinforcement learning.* IEEE Conference on Decision and Control (CDC) 2021.
- **[Curi et al., 2021]** Curi, Bogunovic, Krause. *Combining pessimism with optimism for robust and efficient model-based deep reinforcement learning.* ICML 2021.
- **[Clavier et al., 2023]** Clavier, Pennec, Geist. *Towards minimax optimality of model-based robust reinforcement learning.* arXiv:2302.05372, 2023.
- **[Shi & Chi, 2024]** Shi, Chi. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* Journal of Machine Learning Research 2024.
- **[Ramesh et al., 2024]** Ramesh, Sessa, Hu, Krause, Bogunovic. *Distributionally robust model-based reinforcement learning with large state spaces.* AISTATS 2024.
- **[Wang et al., 2020c]** Wang, Nair, Althoff. *Falsification-based robust adversarial reinforcement learning.* IEEE ICMLA 2020.
- **[Kobayashi, 2024]** Kobayashi. *Lira: Light-robust adversary for model-based reinforcement learning in real world.* arXiv:2409.19617, 2024.
- **[Mankowitz et al., 2019]** Mankowitz, Levine, Jeong, Shi, Kay, Abdolmaleki, Springenberg, Mann, Hester, Riedmiller. *Robust reinforcement learning for continuous control with model misspecification.* arXiv:1906.07516, 2019.
- **[Ye et al., 2024]** Ye, He, Gu, Zhang. *Towards robust model-based reinforcement learning against adversarial corruption.* arXiv:2402.08991, 2024.
- **[Herremans et al., 2024]** Herremans, Anwar, Mercelis. *Robust model-based reinforcement learning with an adversarial auxiliary model.* arXiv:2406.09976, 2024.
- **[Rigter et al., 2022]** Rigter, Lacerda, Hawes. *Rambo-rl: Robust adversarial model-based offline reinforcement learning.* NeurIPS 2022.
- **[Bhardwaj et al., 2024]** Bhardwaj, Xie, Boots, Jiang, Cheng. *Adversarial model for offline reinforcement learning.* NeurIPS 2024.
- **[Shi et al., 2024]** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* arXiv:2404.18909, 2024.
- **[He et al., 2022]** He, Wang, Han, Zou, Miao. *A robust and constrained multi-agent reinforcement learning framework for electric vehicle amod systems.* Dynamics 2022.
- **[Yu et al., 2021]** Yu, Gehring, Schäfer, Anandkumar. *Robust reinforcement learning: A constrained game-theoretic approach.* Learning for Dynamics and Control (L4DC) 2021.
- **[Goodfellow et al., 2014]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* arXiv:1412.6572, 2014.
- **[Huang et al., 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv:1702.02284, 2017.
- **[Zhang et al., 2021b]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control 2021.
