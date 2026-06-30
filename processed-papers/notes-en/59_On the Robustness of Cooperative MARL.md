# 59. On the Robustness of Cooperative Multi-Agent Reinforcement Learning

## Metadata
- **Title**: On the Robustness of Cooperative Multi-Agent Reinforcement Learning
- **Authors**: Jieyu Lin, Kristina Dzeparoska, Sai Qian Zhang, Alberto Leon-Garcia, Nicolas Papernot
- **Affiliation**: University of Toronto; Harvard University; Vector Institute
- **Venue**: 2020 IEEE Symposium on Security and Privacy Workshops (SPW) 2020
- **Link/arXiv**: Not specified (DOI 10.1109/SPW50608.2020.00027)

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation via adversarial examples; adversarial attack on a single agent's observations in a cooperative team (attack-side study, exposing vulnerability)
- **Method paradigm**: Adversarial attack (offensive); two-step attack combining RL-trained adversarial policy + gradient-based targeted adversarial examples; extends FGSM/JSMA
- **Keywords**: cooperative MARL (c-MARL), adversarial examples, observation perturbation, QMIX, StarCraft Multi-Agent Challenge, robustness evaluation

## TL;DR
The paper presents the first robustness analysis of cooperative MARL against an adversary who can manipulate only one team agent's observations, proposing a novel two-step attack (RL-trained adversarial policy to pick a damaging target action, then targeted adversarial examples to lure the victim into it) that drops the team win rate from 98.9% to 0% on the StarCraft II benchmark.

## Problem & Motivation
c-MARL is increasingly used in critical infrastructure (traffic light control, autonomous driving, cellular base station control), so understanding its robustness to adversarial manipulation is a prerequisite for deployment. RL agents are known to be vulnerable to observation perturbations and to adversaries controlling an opponent's actions, but no prior work studied c-MARL in adversarial settings or characterized the attack surface created when agents cooperate. The authors hypothesize that the cooperative aspects that let teams outperform single agents also increase the team's vulnerability to a failure of one constituent agent. Directly applying known RL attacks is precluded by three c-MARL challenges: (1) team-reward estimation is hard and non-differentiable (joint value networks assume agents always pick optimal actions; team reward involves a max operation); (2) high misclassification rate is not equivalent to reward reduction (wrong actions must impact long-term reward); (3) the input feature space is low-dimensional, limiting how observations can be perturbed.

## Robustness Setting
- **Threat model / uncertainty set**: An adversary controls the observations of a single, predetermined vulnerable agent î, modifying its observation o^î_t with a minor perturbation to minimize the total team reward R. The first attack step assumes only black-box access (query the agent policy and environment); the second step (gradient-based adversarial example crafting) assumes access to the victim's model parameters and observations, though it could be extended to black-box via finite-differences or transferability of a replica model.
- **Setting**: cooperative (c-MARL, modeled as a Dec-POMDP with N agents); centralized-training-decentralized-execution (CTDE), with QMIX as the victim system; online execution-time attack.

## Method
- Two-step attack (Figure 2). Step 1: train an adversarial policy with RL to estimate which action, if taken by the victim, would most decrease total team reward R; the non-victim agents' policies are treated as fixed/part of the environment, reducing the problem to single-agent RL that minimizes R (trained with DQN). This circumvents the non-differentiable operations in QMIX's reward estimation and needs only black-box access.
- Target-action selection variants: naive baselines (Random action, Local Worst by lowest individual Q-value, QMIX Worst by feeding each action's Q-value through the mixing network and choosing min Q_total), plus RL-based Optimized Worst (OW) and OW with Regularization (OWR).
- OWR adds a regularization penalty λ·d_diff² to the DQN loss, where d_diff is the Q-value difference between the target action and the original best action; this favors target actions that are easier to achieve with a limited perturbation budget in Step 2, so reward and team win rate decrease consistently.
- Step 2: gradient-based targeted adversarial-example crafting to lure the victim into the target action. The authors extend FGSM into a targeted iterative method (it-FGSM, taking the gradient on the target Q-value instead of the loss) and extend JSMA into d-JSMA, which (a) perturbs two features simultaneously via a new saliency map that filters out feature pairs whose perturbation moves target and non-target Q-values in the same direction, and (b) uses a dynamic step size θ (start small, increase and retry until success or max θ).

## Theoretical Contributions
None / mostly empirical. The work is an empirical attack study; it formulates the attack as a single-agent RL minimization (Eq. 2), defines a regularized DQN loss (Eq. 3), and a new saliency map / perturbation direction for d-JSMA (Eqs. 4-6), but provides no formal robustness/convergence guarantees.

## Experiments
- **Environment/Benchmark**: StarCraft Multi-Agent Challenge (SMAC), StarCraft II; the "2s3z" map (2 Stalkers, 3 Zealots per team). One ally Stalker is the victim; the rest of the allies use their original centrally-trained policy. Victim system trained with QMIX.
- **Baselines**: Target-action selection methods — Random action, QMIX Worst, Local Worst (LW), Optimized Worst (OW), Optimized Worst with Regularization (OWR). Adversarial-example methods — FGSM, it-FGSM, JSMA (fixed θ), d-JSMA (dynamic θ), in combinations with LW/OW/OWR.
- **Evaluation metrics**: Average team reward, team win rate, misclassification rate, target action success rate, total reward reduction, and average L1-norm perturbation budget.

## Key Results
- Directly controlling the victim with the RL-learned adversarial policy: OW and OWR have the highest negative impact, reducing average reward from a 20.00 baseline to 9.39 (OW) and 9.35 (OWR), each yielding a 100% loss rate (0% team win rate vs. 99.80% baseline).
- The full two-step attack with d-JSMA+OWR achieves the best attack performance: 10.62 total reward reduction (close to the 10.65 from directly controlling the victim with OWR) using an average L1-norm perturbation of only 8.33, outperforming d-JSMA+OW and the JSMA variants while needing a lower budget.
- Headline result: perturbing only a single agent's observation degrades the team win rate from 98.9% to 0% and the team reward from 20 to 9.4; regularization (OWR) consistently reduces the required perturbation, and d-JSMA methods concentrate density in the low-perturbation range.

## Limitations & Future Work
- The Step-2 gradient-based crafting assumes white-box access to the victim's model parameters/observations; black-box extension (finite-differences or replica + transferability) is suggested but not evaluated.
- Evaluation is limited to a single SMAC map ("2s3z") and the QMIX system, with one predetermined victim agent assumed already chosen.
- The paper is attack-focused; concrete defenses are only discussed qualitatively (Section V): isolating malicious agents by having each agent estimate other agents' action values/reward (using inverse RL and model-based RL), or formulating all agents as potential adversaries during centralized training so agents react better to adversarial actions at execution.

## Relevance to Survey
This is a foundational attack-side paper in robust c-MARL: it is presented as the first robustness analysis of cooperative teams of RL agents and characterizes the attack surface that emerges from cooperation (a single compromised agent jeopardizing the whole team). It sits on the "state/observation perturbation" and "adversarial attacks on MARL" lines, and motivates defensive/robust-training and fault-tolerance work. It contrasts with competitive-setting adversarial-policy attacks (Gleave et al.) and connects single-agent adversarial-example literature (FGSM/JSMA/i-FGSM) to the cooperative multi-agent regime, providing an evaluation tool for assessing and validating c-MARL robustness.

## Related Work (verbatim excerpts from the paper)
> _[Section VI, Related Work]_

"Prior work has demonstrated that RL is vulnerable to input perturbation attacks, where the attacker modiﬁes the agent's observation with the goal of degrading its performance; for example, using the FGSM [13] to attack three RL networks [5]. Other attacks reduce the number of adversarial examples needed to decrease the agent's reward [17] or trigger misbehavior of the agent after a delay [18]. The learning process of DQN itself can be attacked [19], by constructing a replica model of the victim and transferring adversarial examples from the FGSM and JSMA [16] techniques to craft adversarial examples. None of this work studies c-MARL, and the effects of cooperation."

"The closest work to ours is perhaps Gleave et al. [6]. They focus on attacks in the competitive multi-agent setting whereas we instead consider cooperative teams of agents. Furthermore, they assume full control over one of the agents (i.e., they were able to directly control the agent's actions), whereas we only perturb the agent's environment."

> _[Introduction]_

"RL agents are known to be vulnerable to adversaries perturbing their observations with adversarial examples [5], as well as adversaries directly controlling the actions of one of the victim's opponents [6]. When exploited, this vulnerability results in agents taking unintended actions, often with adverse consequences. We hypothesize that cooperative aspects of c-MARL agents, which enable them to outperform classic RL agents when operating as a team, also increase the vulnerability of a team to failures of one of its constituent agents."

"To the best of our knowledge, this work is the ﬁrst to study c-MARL in adversarial settings and characterize the attack surface exposed by enabling agents to cooperate more effectively. Our goal is to understand the impact an adversary can have on the long-term reward of a team of agents."

### Cited references (resolved from the paper's bibliography)
- **[5]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[6]** Gleave, Dennis, Kant, Wild, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv 2019.
- **[13]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* arXiv 2014.
- **[16]** Papernot, McDaniel, Jha, Fredrikson, Celik, Swami. *The limitations of deep learning in adversarial settings.* IEEE European Symposium on Security and Privacy (EuroS&P) 2016.
- **[17]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* arXiv 2017.
- **[18]** Zhao, Shumailov, Cui, Gao, Mullins, Anderson. *Blackbox attacks on reinforcement learning agents using approximated temporal information.* arXiv 2019.
- **[19]** Behzadan, Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* International Conference on Machine Learning and Data Mining in Pattern Recognition (Springer) 2017.
