# 157. Efficient Adversarial Attacks on Online Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Efficient Adversarial Attacks on Online Multi-Agent Reinforcement Learning
- **Authors**: Guanlin Liu, Lifeng Lai
- **Affiliation**: Department of Electrical and Computer Engineering, University of California, Davis
- **Venue**: Not specified (arXiv preprint)
- **Link/arXiv**: arXiv:2307.07670v1 [cs.LG] 15 Jul 2023

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial attacks on MARL — reward poisoning and action poisoning (and their mixture) by an exogenous attacker sitting between agents and environment; attacker forces agents to a target policy or maximizes an attacker-chosen reward function.
- **Method paradigm**: Poisoning attack design and analysis (action poisoning, reward poisoning, mixed attack), Markov games, equilibrium (NE/CE/CCE) manipulation, regret-based cost/loss bounds, exploration-then-attack for the black-box setting.
- **Keywords**: adversarial attacks, reward poisoning, action poisoning, Markov games, V-learning, online MARL

## TL;DR
The paper formulates adversarial poisoning attacks against online MARL, proves that action-poisoning-only and reward-poisoning-only attacks are fundamentally limited, and proposes a mixed (action + reward) attack strategy — plus an approximate version for the black-box setting — that forces any sub-linear-regret MARL agents to follow an attacker-chosen target policy with sub-linear cost and loss.

## Problem & Motivation
As MARL is increasingly deployed in safety-critical and security-related applications, understanding adversarial attacks is essential for building trustworthy systems. While adversarial attacks on single-agent RL have been widely studied, existing work on attacks against MARL is limited. The paper fills this gap by systematically studying an attacker who sits between the agents and the environment, can monitor states/actions/rewards, and can manipulate either the rewards (before agents receive them) or the actions (before the environment receives them). The attacker aims to force the agents into a target policy (or maximize an attacker-chosen reward) while minimizing the amount of manipulation, even when it has no prior information about the environment or the agents' algorithms.

## Robustness Setting
- **Threat model / uncertainty set**: An exogenous attacker between agents and environment. At each step it may override an agent's chosen action ak_i,h → ẽak_i,h and/or change the reward rk_i,h → ẽrk_i,h before the agent receives it. Attack cost = cumulative number of action manipulations plus magnitude of reward manipulations; attack loss = cumulative deviations from the target policy (Loss1) or regret w.r.t. the attacker's reward-maximizing policy (Loss2). Three capability levels: white-box (full knowledge of the MG), gray-box (no environment info but knows the target policy), black-box (no environment info and target policy unknown). The agents do not know the attacker is present.
- **Setting**: cooperative and competitive (general tabular episodic Markov game, since reward functions of different agents can be arbitrary); online MARL; the attacked learner can be decentralized (V-learning analyzed explicitly).

## Method
- Formalizes the attack: define action-poisoning-only, reward-poisoning-only, and mixed attacks; define attack cost and two attack-loss notions; call an attack "efficient and successful" if both cost and loss scale as o(T) where T = KH.
- White-box impossibility: proves there exist MGs and target policies where no action-poisoning-only (Thm 1) or bounded reward-poisoning-only (Thm 2) Markov attack can be both efficient and successful; the proofs hinge on the fact that, to be efficient, the attacker must not attack when agents follow the target policy.
- White-box constructive attacks under sufficient conditions: the d-portion action attack (Condition 1) and the η-gap reward attack (Condition 2) each make the target policy the unique {NE, CE, CCE}, with cost/loss bounded by the agents' regret bound R(T) (Thms 3–6).
- Gray-box mixed attack: if an agent picks the target action, do nothing; otherwise override the action to the target action and set its reward to 0. This makes the target policy the unique {NE, CE, CCE} and forces any sub-linear-regret agents to follow it with sub-linear cost/loss (Thms 7–8).
- Black-box approximate mixed attack: two phases — an exploration phase (Algorithm 1) that identifies an approximate optimal policy π† by minimizing an upper–lower value-function gap, then an attack phase running the mixed attack; analyzed on V-learning, with stopping time τ = K^{2/3} yielding O(K^{2/3}) cost/loss and O(K^{-1/3}) output-policy sub-optimality (Lemma 1, Thm 9).

## Theoretical Contributions
- Impossibility results: Theorem 1 (action-poisoning-only) and Theorem 2 (bounded reward-poisoning-only) show no efficient-and-successful Markov attack exists in general.
- Sufficient conditions and bounds: Theorem 3/4 (d-portion attack makes π† the unique {NE,CE,CCE}; E[Loss1] ≤ 2m²R(T)/Δmin, E[Cost] ≤ 2m³R(T)/Δmin) and Theorem 5/6 (η-gap attack; E[Loss1] ≤ mR(T)/η, E[Cost] ≤ m²R(T)/η).
- Mixed attack guarantees: Theorem 7/8 (gray-box; E[Loss1] ≤ mR(T)/Rmin, E[Cost] ≤ 2mR(T)/Rmin).
- Black-box guarantees: Lemma 1 (confidence bound on V^{π*} − V^{π†}) and Theorem 9 (approximate mixed attack on V-learning; with τ = K^{2/3}, O(K^{2/3}) loss/cost and O(K^{-1/3}) output sub-optimality).

## Experiments
- **Environment/Benchmark**: (1) A simple Markov game with m = 2, H = 2, |S| = 3 (a cooperate/defect game, the example from Appendix C.2), with two target-policy cases; (2) a 3-agent recycling-robot system with 8 states, 2 actions per agent, H = 6, day/night energy-level transition dynamics. Attacks are run against V-learning agents.
- **Baselines**: The three proposed strategies compared against one another — mixed attack vs. η-gap (reward-only) attack vs. d-portion (action-only) attack; and mixed attack vs. approximate mixed attack (black-box).
- **Evaluation metrics**: Cumulative attack loss and cumulative attack cost as functions of episode k (scaling with T).

## Key Results
- Case 1 (conditions fail): the mixed attack's cost and loss scale sub-linearly in T, while the d-portion and η-gap attacks scale linearly — consistent with the impossibility results.
- Case 2 (Conditions 1 and 2 hold): all three strategies have sub-linear cost and loss, as predicted.
- Recycling-robot system: both the mixed attack and the approximate mixed attack achieve sub-linear cost and loss on V-learning for both attack goals (maximize agent 1's reward; minimize agents 2 and 3's reward), and the approximate (black-box) mixed attack nearly matches the (gray-box) mixed attack.

## Limitations & Future Work
- The sufficient conditions (Condition 1, Condition 2) under which action-only or reward-only attacks succeed may be strict and may not hold in practice.
- The constructive white-box attacks rely on full environment knowledge; the gray-box mixed attack requires the target policy.
- The paper is attack-focused (offensive); defenses are left as future work — the authors state they will investigate defense strategies to mitigate the effects of this attack.

## Relevance to Survey
This paper sits on the "adversarial attacks / poisoning" line of the robust MARL landscape, extending single-agent reward/action-poisoning attack theory to the multi-agent (Markov game) setting and analyzing attacks against equilibrium-learning and decentralized algorithms (V-learning). It motivates the need for robust and corruption-tolerant MARL by characterizing when efficient attacks exist; it connects to robust/corruption-robust RL defenses and to the broader trustworthy-MARL theme, providing the threat-model side that robust-training and defense works aim to counter.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.2, Related works]_

"Attacks on Single Agent RL: Adversarial attacks on single agent RL have been studied in various settings [17, 18, 19, 20, 21, 22, 23]. For example, [17, 20, 24] study online reward poisoning attacks in which the attacker could manipulate the reward signal before the agent receives it. [25] studies online action poisoning attacks in which the attacker could manipulate the action signal before the environment receives it. [24] studies the limitations of reward only manipulation or action only manipulation in single-agent RL."

"Attacks on MARL: [26] considers a game redesign problem where the designer knows the full information of the game and can redesign the reward functions. The proposed redesign methods can incentivize players to take a specific target action profile frequently with a small cumulative design cost. [27, 28] study the poisoning attack on multi-agent reinforcement learners, assuming that the attacker controls one of the learners. [29] studies the reward poisoning attack on offline multi-agent reinforcement learners."

"Defense Against Attacks on RL: There is also recent work on defending against adversarial attacks on RL [30, 31, 32, 33, 34, 35]. These work focus on the single-agent RL setting where an adversary can corrupt the reward and state transition."

> _[Section 1, Introduction — prior-work context]_

"As RL models, including single agent RL and MARL, are being increasingly used in safety critical and security related applications, it is critical to developing trustworthy RL systems. As a first step towards this important goal, it is essential to understand the effects of adversarial attacks on RL systems. Motivated by this, there have been many recent works that investigate adversarial attacks on single agent RL under various settings [17, 18, 19, 20, 21, 22, 23]."

"On the other hand, except the ones that will be reviewed below, existing work on adversarial attacks on MARL is limited. In this paper, we aim to fill in this gap and systematically investigate the impact of adversarial attacks on online MARL."

### Cited references (resolved from the paper's bibliography)
- **[17]** Behzadan, Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* International Conference on Machine Learning and Data Mining in Pattern Recognition, Springer 2017.
- **[18]** Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* International Conference on Decision and Game Theory for Security, Springer 2019.
- **[19]** Ma, Zhang, Sun, Zhu. *Policy poisoning in batch reinforcement learning and control.* NeurIPS 2019.
- **[20]** Zhang, Ma, Singla, Zhu. *Adaptive reward-poisoning attacks against reinforcement learning.* ICML 2020.
- **[21]** Sun, Huo, Huang. *Vulnerability-aware poisoning mechanism for online RL with unknown dynamics.* ICLR 2021.
- **[22]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching via environment poisoning: Training-time adversarial attacks against reinforcement learning.* ICML 2020.
- **[23]** Rakhsha, Zhang, Zhu, Singla. *Reward poisoning in reinforcement learning: Attacks against unknown learners in unknown environments.* arXiv:2102.08492, 2021.
- **[24]** Rangi, Xu, Tran-Thanh, Franceschetti. *Understanding the limits of poisoning attacks in episodic reinforcement learning.* IJCAI-22, 2022.
- **[25]** Liu, Lai. *Provably efficient black-box action poisoning attacks against reinforcement learning.* NeurIPS 2021.
- **[26]** Ma, Wu, Zhu. *Game redesign in no-regret game playing.* IJCAI 2022.
- **[27]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* ICLR 2020.
- **[28]** Guo, Wu, Huang, Xing. *Adversarial policy learning in two-player competitive games.* ICML 2021.
- **[29]** Wu, McMahan, Zhu, Xie. *Reward poisoning attacks on offline multi-agent reinforcement learning.* arXiv:2206.01888, 2022.
- **[30]** Banihashem, Singla, Radanovic. *Defense against reward poisoning attacks in reinforcement learning.* arXiv:2102.05776, 2021.
- **[31]** Zhang, Chen, Zhu, Sun. *Robust policy gradient against strong data corruption.* ICML 2021.
- **[32]** Lykouris, Simchowitz, Slivkins, Sun. *Corruption-robust exploration in episodic reinforcement learning.* COLT 2021.
- **[33]** Chen, Du, Jamieson. *Improved corruption robust algorithms for episodic reinforcement learning.* ICML 2021.
- **[34]** Wei, Dann, Zimmert. *A model selection approach for corruption robust reinforcement learning.* ALT 2022.
- **[35]** Wu, Yang, Du, Wang. *On reinforcement learning with adversarial corruption and its application to block MDP.* ICML 2021.
