# 41. Robust Multi-Agent Reinforcement Learning against Adversaries on Observation

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning against Adversaries on Observation
- **Authors**: Anonymous authors (paper under double-blind review)
- **Affiliation**: Not specified
- **Venue**: Under review as a conference paper at ICLR 2023
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation (adversarial attacks on agents' sensor observations in cooperative MARL; noise / jamming attacks)
- **Method paradigm**: Adversarial training, alternating attacker-victim training, hybrid (discrete-continuous) action attacker via HyAR, attacker pool / population-based curriculum, optional defense module (perturbation detection + observation reconstruction)
- **Keywords**: cooperative MARL, observation perturbation, adversarial attack, robust training, hybrid action space, QMIX

## TL;DR
The paper proposes ROMAO, a robust MARL training framework that progressively generates adversarial attacks on agents' observations via a hybrid-action attacker (which first picks an agent to attack, then outputs the perturbation vector) and alternately trains a victim team against an evolving pool of attackers, plus an optional defense module, to learn a cooperative policy robust to observation perturbations.

## Problem & Motivation
Neural networks (and hence deep RL policies) are vulnerable to small adversarial perturbations. In cooperative MARL, agents' most vulnerable components are the sensors, which can be disturbed by noise or jamming, and even a small perturbation on one agent's observation can make it deflect from coordination and cause the whole multi-agent system to fail. While adversarial-training-based robustness has been studied in single-agent RL, such studies are rare in cooperative MARL, where existing work mainly considers teammates that may betray or actions that are maliciously modified — leaving robustness to observation perturbations under-explored. The paper targets the realistic and reasonable setting of black-box attacks on observations and how to defend against them.

## Robustness Setting
- **Threat model / uncertainty set**: An attacker perturbs the observations of agents. The attacker shares the victim team's state space; its action space is Â : N × {Oi} — it first chooses one agent and then generates a perturbation with the same dimension as that agent's observation. The total perturbation is constrained so that its ℓ1 norm is ≤ a constant C (C = 10 used in practice). The attacker's reward is R̂ = −R (it minimizes the victim team's return). The setting is black-box: the attacker cannot access the parameters of the victims' Q functions, and the victim agents have no oracle information about whether they are under attack. Considered attack modes include attacking a random agent with random noise, attacking a specific agent with random noise, and attacking a specific observation dimension of a specific agent.
- **Setting**: cooperative (fully cooperative, partially observable, shared reward); CTDE (the defense module's training is done in the centralized training phase); online.

## Method
- **Hybrid action attacker (Section 4.1)**: Models the attacker's "select an agent (discrete) + output perturbation offsets (continuous)" decision as a Parameterized Action MDP (PAMDP). Uses HyAR (Li et al., 2021) to construct a unified, decodable latent representation space for the hybrid action, with TD3 as the policy on the latent space; the decoded action k (agent ID) and x_k (perturbation) are applied so the victim sees the perturbed observation o_{k_t} + x_{k_t}.
- **Attacker optimization (Section 4.2)**: The attacker minimizes the victim team's expected return without any auxiliary intrinsic rewards; on each new training turn the attacker's exploration and replay buffer are reset to eliminate bias from previous attacks.
- **Robust training via alternating training (Section 4.3)**: The attacker and the victim team (defender) are trained alternately. A pool stores all historical attacker models; when training the defender, an attacker is randomly sampled from the pool per episode so the victim defends against both the current and historical attackers, improving general robustness. The framework is agnostic to the specific MARL method.
- **Defense module (Section 4.4, optional)**: Because nearby agents may share part of their observations, an agent can reconstruct its observation from teammates' observations in its field of view; a perturbation detector (trained during centralized training, where both clean and perturbed observations are available) judges whether an agent is under attack. This module requires communication and is optional.

## Theoretical Contributions
None / mostly empirical.

## Experiments
- **Environment/Benchmark**: StarCraft II unit micromanagement benchmark (SMAC) maps 2s3z, 3m, 3s_vs_5z, 5m_vs_6m; and Predator-Prey (PP), a partially observable grid-world task.
- **Baselines**: Vanilla QMIX (trained without perturbations); Random QMIX / RanPert (trained under random perturbations); One-agent QMIX (trained with only agent 0 under attack, attack trained with TD3). The victim policy is QMIX in all cases.
- **Evaluation metrics**: Average test win rate (with standard deviation over five random seeds) under three attack modes and different perturbation ranges; average mean return on PP.

## Key Results
- Under various attack modes with limited perturbation range 5 (ℓ1 norm), ROMAO-trained QMIX is robust and stable across maps; it especially outperforms baselines on the extreme Attack Mode 3 (e.g., on 2s3z it reaches 94.6 vs Vanilla 72.6 / Random 83.1; on 5m_vs_6m it reaches 23.3 vs Vanilla 13.5 / Random 3.1).
- Vanilla QMIX performs worst (it has seen no attacks), Random QMIX overfits to the random pattern it was trained on and drops sharply under Attack Mode 3, while ROMAO's alternating training covers more attack types and handles extreme attacks better.
- On Predator-Prey, ROMAO achieves the best average mean return, outperforming RanPert and QMIX. The defense module improves all policies' win rates without further learning, and ROMAO generalizes best across perturbation ranges (best performance even under perturbations of 100).

## Limitations & Future Work
- Future work can concentrate on how to deal with concurrent attacks on multiple agents efficiently, as the combinatorial blow-up cannot be avoided when attacking multiple agents in ROMAO as the number of agents increases.
- The defense module requires communication, so it is only optional.
- (Note: the paper inconsistently refers to the framework as both "ROMAO" and "RAMAO" / "RAMAO".)

## Relevance to Survey
This paper sits on the "state/observation perturbation" main line of robust MARL, addressing a gap left by prior cooperative-MARL robustness work that focused on action perturbation, betraying teammates, or agent failure. Methodologically it connects the single-agent adversarial-training line (Pinto et al. 2017; Zhang et al. 2021; Pattanaik et al. 2018; Sun et al. 2021) to the cooperative MARL setting via an attacker-victim alternating-training / population-of-attackers scheme, and integrates a hybrid-action attacker (HyAR) and a communication-based defense module. It is closely related to Lin et al. (2020) on attacking observations in a team and to value-decomposition MARL (QMIX/VDN) as the victim backbone.

## Related Work (verbatim excerpts from the paper)

> _[Introduction]_

"In single-agent reinforcement learning, some research studies enhance policy robustness by using adversarial learning and achieve good results. Pinto et al. (2017) propose a method that jointly trains a pair of agents, including a protagonist and an adversary, and the protagonist learns to fulfill the original task goals while being robust to the disruptions generated by its adversary. Pattanaik et al. (2018) show that deep RL can be fooled easily and train an RL agent under naive attacks to improve its robustness. Zhang et al. (2021) propose a framework of alternating training with learned adversaries, which trains an adversary online with the agent using a policy gradient following the optimal adversarial attack framework. However, such studies are rare in cooperative MARL, and current works mainly focus on the setting where teammates may betray or agents' actions may be maliciously modified (Li et al., 2019; Phan et al., 2021; 2020; Hu & Zhang, 2022). However, in real-life applications of cooperative MARL, the most vulnerable parts of the agents are the sensors that can be disturbed by noise or jamming attacks. Agents are closely related to each other when cooperating to accomplish tasks, and even a small perturbation on one agent's observation from the sensors can make it deflect from coordination and cause the whole multi-agent system to fail."

> _[Section 2.1, Cooperative Multi-Agent Reinforcement Learning]_

"Cooperative MARL has made prominent progress these years. Research on it aims to help agents learn policies to coordinate and complete cooperative tasks. Many methods have emerged under the CTDE paradigm, most of which can be roughly divided into policy-based and value-based methods. MADDPG (Lowe et al., 2017), COMA (Foerster et al., 2018), and MAAC (Iqbal & Sha, 2019) are typical policy gradient-based methods that explore the optimization of multi-agent policy gradient methods, while MADDPG can also be employed in competitive scenarios. Another category of cooperative MARL approaches, value-based methods, mainly focus on factorizing the value function. VDN (Sunehag et al., 2018) aims to decompose the team value function into agent-wise value functions by a simple additive factorization. Following the Individual-Global-Max (IGM) principle (Son et al., 2019), QMIX (Rashid et al., 2018) improves the way of value function decomposition by learning a mixing network, which approximates a monotonic function value decomposition."

> _[Section 2.2, Adversarial Attack]_

"The adversarial attack has been explored in many areas. In image classification, the adversarial attack means generating adversarial examples. The adversarial example is a deceptive input to a model that is purposely designed to cause a model to make a mistake in its predictions but makes no difference to humans. Goodfellow et al. (2015) propose a simple and fast gradient-based method that is used to generate adversarial examples to make the model classify incorrectly while minimizing the amount of perturbation added to the pixels of the image. Loison et al. (2020) use feature selection to minimize the number of features modified while causing the wrong classification, and flat perturbations are added to features iteratively according to saliency value by decreasing order."

> _[Section 2.3, Adversarial Robustness of RL Agents]_

"Based on the effectiveness of adversarial attacks on images, Huang et al. (2017) propose a method to inject adversarial perturbation into the input to confuse the RL policy. Some researchers (Gleave et al., 2019; Zhao et al., 2020) focus on black box attacks in RL, which are more challenging because of the lack of information about the parameters of the target model. Adversarial training is empirically shown to improve agents' robustness to make the policies experience possible adversarial attacks. Pinto et al. (2017) propose a method to train an agent in the presence of disturbance and obtain more robust policies. Zhang et al. (2021) propose a method that involves the concurrent training of an attacker and the victim agent using policy gradient following the optimal adversarial attack framework. Sun et al. (2021) decouple the problem of finding state perturbations into finding the best policy perturbation directions and crafting correspondent state perturbations."

> _[Section 2.4, Adversarial Attacks in Cooperative MARL]_

"There could be various types of adversarial attacks in cooperative multi-agent systems. Some researchers focus on the setting where some teammates may betray and minimize their shared return (Phan et al., 2021; 2020; Li et al., 2019). Meanwhile, some researchers prefer the setting where components of a Markov Decision Process (MDP), such as states, actions, or observations, are perturbed. Hu & Zhang (2022) propose a sparse adversarial attack on actions of cooperative multi-agent systems and can make the victim team perform poorly when only a few agents are attacked at a few timesteps. Zhou & Liu (2022) propose a robust training framework for the state-of-the-art reinforcement learning method MFAC (Yang et al., 2018) when the state is perturbed. Lin et al. (2020) propose a method to attack one agent's observation in a team. It is achieved by an indirect way that the attacker first tries to find a wrong action it should encourage the victim agent to take. Then, the attacker uses adversarial examples to mislead the victim into choosing the action. This work is most relevant to our work because it considers the indirect attacks on observations, and the attacker only chooses one agent to attack. While in our work, we consider the setting that every agent is at risk of attack, and we cannot access the parameters of the Q functions of the victims. We focus on black box attacks on observations and how to defend against them, which is more reasonable and realistic."

> _[Appendix A.1.2, More Related Work — Adversarial Attacks in Cooperative MARL]_

"Some researchers focus on the setting where some teammates may betray and minimize their shared return. Phan et al. (2021) and Phan et al. (2020) propose to train competing teams of protagonist and antagonist agents of varying sizes to improve resilience against arbitrary agent changes. Li et al. (2019) extend MADDPG with a minimax objective to make the learned policy robust and behave well even with strategies not seen during training. Agents update policies considering a worst-case scenario: assuming that all other agents act adversarially."

### Cited references (resolved from the paper's bibliography)
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Pattanaik et al., 2018]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* AAMAS 2018.
- **[Zhang et al., 2021]** Huan Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Phan et al., 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Phan et al., 2020]** Phan, Gabor, Sedlmeier, Ritz, Kempter, Klein, Sauer, Schmid, Wieghardt, Zeller, Linnhoff-Popien. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
- **[Hu & Zhang, 2022]** Hu, Zhang. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv 2022.
- **[Lowe et al., 2017]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NIPS 2017.
- **[Foerster et al., 2018]** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[Iqbal & Sha, 2019]** Iqbal, Sha. *Actor-attention-critic for multi-agent reinforcement learning.* ICML 2019.
- **[Sunehag et al., 2018]** Sunehag, Lever, Gruslys, Czarnecki, Zambaldi, Jaderberg, Lanctot, Sonnerat, Leibo, Tuyls, Graepel. *Value-decomposition networks for cooperative multi-agent learning based on team reward.* AAMAS 2018.
- **[Son et al., 2019]** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning.* ICML 2019.
- **[Rashid et al., 2018]** Rashid, Samvelyan, Schröder de Witt, Farquhar, Foerster, Whiteson. *QMIX: monotonic value function factorisation for deep multi-agent reinforcement learning.* arXiv 2018.
- **[Goodfellow et al., 2015]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* ICLR 2015.
- **[Loison et al., 2020]** Loison, Combey, Hajri. *Probabilistic jacobian-based saliency maps attacks.* arXiv 2020.
- **[Huang et al., 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[Gleave et al., 2019]** Gleave, Dennis, Kant, Wild, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv 2019.
- **[Zhao et al., 2020]** Zhao, Shumailov, Cui, Gao, Mullins, Anderson. *Blackbox attacks on reinforcement learning agents using approximated temporal information.* DSN-W 2020.
- **[Sun et al., 2021]** Sun, Zheng, Liang, Huang. *Who is the strongest enemy? towards optimal and efficient evasion attacks in deep RL.* arXiv 2021.
- **[Zhou & Liu, 2022]** Zhou, Liu. *RomFac: A robust mean-field actor-critic reinforcement learning against adversarial perturbations on states.* arXiv 2022.
- **[Yang et al., 2018]** Yang, Luo, Li, Zhou, Zhang, Wang. *Mean field multi-agent reinforcement learning.* ICML 2018.
- **[Lin et al., 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* arXiv 2020.
