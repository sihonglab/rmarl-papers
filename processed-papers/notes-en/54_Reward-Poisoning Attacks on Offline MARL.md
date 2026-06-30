# 54. Reward-Poisoning Attacks on Offline Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Reward-Poisoning Attacks on Offline Multi-Agent Reinforcement Learning
- **Authors**: Young Wu, Jeremy McMahan, Xiaojin Zhu, Qiaomin Xie
- **Affiliation**: University of Wisconsin-Madison
- **Venue**: AAAI 2023 (The Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI-23)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Reward poisoning / data poisoning attacks (an exogenous attacker modifies the rewards stored in an offline dataset). This is an attack paper that motivates robustness/defense in offline MARL.
- **Method paradigm**: Game-theoretic equilibrium installation (Markov Perfect Dominant Strategy Equilibrium), optimal attack via convex optimization / linear programming, confidence-bound (uncertainty-aware) backward induction, cost-bound analysis.
- **Keywords**: reward poisoning, offline MARL, Markov Game, Markov Perfect Dominant Strategy Equilibrium (MPDSE), linear program, uncertainty-aware learners

## TL;DR
The paper introduces optimal reward-poisoning attacks against offline MARL, showing that an exogenous attacker can minimally perturb the dataset's rewards (under L1 cost) to install an attacker-chosen target policy as a Markov Perfect Dominant Strategy Equilibrium (MPDSE) — which any rational, even uncertainty-aware, learner is guaranteed to follow — and that this attack can be solved efficiently as a linear program and is cheaper than separately attacking each agent.

## Problem & Motivation
In offline MARL, agents learn policies from a fixed, pre-collected dataset without further environment interaction. Such pipelines are vulnerable to data-poisoning attacks: a third party who can manipulate the dataset's feedback can steer agents to wrong equilibria (e.g., disrupting autonomous vehicles, teaching robots faulty procedures, misleading economic agents, or corrupting video-game NPCs). Prior poisoning work targets single-agent RL, online learners, or assumes the attacker controls one of the learners; the multi-agent offline case where an external attacker poisons all learners' rewards simultaneously had not been studied. The authors observe that naively reducing the problem to separate single-agent attacks is provably suboptimal, motivating a new attack formulation tailored to the multi-agent structure, and intend the work as a first step toward defense.

## Robustness Setting
- **Threat model / uncertainty set**: The attacker has access to the original offline dataset D and a pre-specified target policy π†, and modifies the stored reward vectors before agents see the data, minimizing L1 cost C(r0, r†) = ‖r0 − r†‖1. Learners are assumed only to be rational (never play dominated actions, with an arbitrarily small margin ι). The attack is designed to be robust to uncertainty-aware learners: the attacker accounts for the set of all "plausible" Markov Games consistent with the dataset via reward/transition confidence sets (Hoeffding-type half-widths ρR, ρP), without knowing the learner's specific algorithm, and ensures π† is an ι-MPDSE for every plausible game. Full-coverage of the dataset (every (s,a,h) visited) is assumed and shown necessary.
- **Setting**: general-sum n-player Markov Games; mixed (cooperative/competitive); offline; partially decentralized agents (second accessibility level: each agent sees the joint action but only its own reward).

## Method
- Define the target equilibrium concept: an ι-strict Markov Perfect Dominant Strategy Equilibrium (ι-MPDSE), where the target action is at least ι better in Q-value than any alternative for each learner at every state/period; a strict MPDSE, if it exists, is unique, and rational learners are assumed to play it.
- Show that separately applying single-agent reward-poisoning incurs nonzero (suboptimal) cost (Tables 1–2 example), so a joint multi-agent formulation is required.
- Bandit-game (|S|=1, H=1) building block: formulate the minimal-cost attack as a convex optimization (LP under L1 cost) whose constraints encode the poisoned MLE rewards and the ι-strict dominance separation; extend to uncertainty-aware learners by enforcing an ι separation between the lower confidence bound of the target action and the upper confidence bounds of all other actions (formulations (1) and (2)).
- Markov-game generalization: a "Q confidence-bound backward induction" that maintains confidence upper/lower bounds Q̄ and Q on the learners' Q-function via backward induction, then enforces the ι-separation of target vs. other actions at all states/periods (formulation (3)–(7)); thanks to LP duality, the min/max over confidence sets still yields a linear program under L1 cost.
- Analyze attack cost: derive universal and instance-dependent upper/lower bounds relating minimal cost to the Markov Game structure (visit counts N, confidence half-widths ρ, dominance gaps), reducing Markov-game cost bounds to per-period bandit-game bounds.

## Theoretical Contributions
- **Proposition 1**: full coverage (Nh(s,a) > 0) is necessary; otherwise there exist learners for which the attack is infeasible.
- **Propositions 2–3**: feasibility condition for the bandit attack (ι ≤ 2b − 2ρR(a)); under L1 cost the bandit attack is an LP.
- **Lemma 4**: if the Markov-game formulation (3)–(7) is feasible, π† is the unique ι-MPDSE of every plausible game G ∈ CIG.
- **Theorem 5 / Corollary 6**: feasibility of the Markov-game attack when ι ≤ 2b − (H+1)ρR_h(s,a) for all h,s,a, with an explicit visit-count condition (Hoeffding-type) guaranteeing feasibility.
- **Theorem 7**: under L1 cost, problem (3)–(7) can be formulated as a linear program (via LP duality).
- **Theorems 8, 9, 12 and Lemmas 10–11**: universal and instance-dependent cost bounds; near-tightness shown via a constructed high-cost instance; an exponential-in-n lower bound for some datasets (the price of installing an MPDSE rather than a Nash equilibrium).

## Experiments
- **Environment/Benchmark**: Not specified (the paper is theoretical; it uses small illustrative normal-form / Markov Game constructions, e.g., Tables 1–4, rather than empirical RL benchmarks).
- **Baselines**: Not specified (single-agent attack reduction is discussed analytically as a suboptimal baseline, but no empirical comparison is reported).
- **Evaluation metrics**: Not specified (analysis is in terms of attack feasibility and minimal L1 poisoning cost C*(I)).

## Key Results
- The target policy π† can be installed as the unique ι-MPDSE for every plausible Markov Game consistent with the poisoned dataset, guaranteeing rational (including uncertainty-aware) learners adopt it (Lemma 4).
- Reducing the attack to independent single-agent poisoning is provably suboptimal; the joint multi-agent attack can be strictly cheaper.
- Both the bandit and the full Markov-game attacks can be solved efficiently as linear programs under L1 cost (Propositions 3, Theorem 7).
- Minimal attack cost is characterized by the game structure: feasibility requires sufficiently populated datasets (visit-count bound in Corollary 6), and for some datasets the cost grows exponentially in the number of players n (Theorem 12).

## Limitations & Future Work
- The attack requires full dataset coverage (Assumption 1) and access to the original dataset; coverage is shown necessary, so sparse datasets are not attackable in this framework.
- For some games the minimal poisoning cost is exponential in the number of agents n — the price paid for installing an MPDSE rather than a (weaker-assumption) Nash equilibrium.
- The work is primarily theoretical (formulations, feasibility, and cost bounds) without large-scale empirical evaluation.
- The authors explicitly call for future study of defenses against such attacks in offline MARL, e.g., via robust statistics and reinforcement learning.

## Relevance to Survey
This paper sits on the "reward/data poisoning attacks" line within robust MARL, complementing the model-uncertainty and adversarial-policy lines. It is an attack-side contribution that motivates the need for robust and defensible offline MARL: by formalizing how an external adversary can manipulate offline reward data to control multi-agent equilibria, it frames the threat model that defensive robust-MARL methods must withstand. It connects to single-agent reward-poisoning and corruption-robust RL, offline MARL with uncertainty-aware (pessimistic/optimistic) algorithms, and mechanism design, and explicitly flags the open problem of defense against poisoning in the multi-agent offline setting.

## Related Work (verbatim excerpts from the paper)
> _[Section: Related Work — "Online Reward-Poisoning"]_

"Reward poisoning problem has been studied in various settings, including online single-agent reinforcement learners (Banihashem et al. 2022; Huang and Zhu 2019; Liu and Lai 2021; Rakhsha et al. 2021a,b, 2020; Sun, Huo, and Huang 2020; Zhang et al. 2020), as well as online bandits (Bogunovic et al. 2021; Garcelon et al. 2020; Guan et al. 2020; Jun et al. 2018; Liu and Shroff 2019; Lu, Wang, and Zhang 2021; Ma et al. 2018; Yang et al. 2021; Zuo 2020). Online reward poisoning for multiple learners is recently studied as a game redesign problem in (Ma, Wu, and Zhu 2021)."

> _[Section: Related Work — "Offline Reward Poisoning"]_

"Ma et al. (2019); Rakhsha et al. (2020, 2021a); Rangi et al. (2022b); Zhang and Parkes (2008); Zhang, Parkes, and Chen (2009) focus on adversarial attack on offline single-agent reinforcement learners. Gleave et al. (2019); Guo et al. (2021) study the poisoning attack on multi-agent reinforcement learners, assuming that the attacker controls one of the learners. Our model instead assumes that the attacker is not one of the learners, and the attacker wants to and is able to poison the rewards of all learners at the same time. Our model pertains to many applications such as autonomous driving, robotics, traffic control, and economic analysis, in which there is a central controller whose interests are not aligned with any of the agents and can modify the rewards and therefore manipulate all agents at the same time."

> _[Section: Related Work — "Constrained Mechanism Design"]_

"Our paper is also related to the mechanism design literature, in particular, the K-implementation problem in (Monderer and Tennenholtz 2004; Anderson, Shoham, and Altman 2010). Our model differs mainly in that the attacker, unlike a mechanism designer, does not alter the game/environment directly, but instead modifies the training data, from which the learners infer the underlying game and compute their policy accordingly. In practical applications, rewards are often stochastic due to imprecise measurement and state observation, hence the mechanism design approach is not directly applicable to MARL reward poisoning. Conversely, constrained mechanism design can be viewed as a special case when the rewards are deterministic and the training data has uniform coverage of all period-state-action tuples."

> _[Section: Related Work — "Defense against Attacks on Reinforcement Learning"]_

"There is also recent work on defending against reward poisoning or adversarial attacks on reinforcement learning; examples include (Banihashem, Singla, and Radanovic 2021; Lykouris et al. 2021; Rangi et al. 2022a; Wei, Dann, and Zimmert 2022; Wu et al. 2022; Zhang et al. 2021a,b). These work focus on the single-agent setting where attackers have limited ability to modify the training data. We are not aware of defenses against reward poisoning in our offline multi-agent setting. Given the numerous real-world applications of offline MARL, we believe it is important to study the multi-agent version of the problem."

### Cited references (resolved from the paper's bibliography)
- **[Banihashem et al. 2022]** Banihashem, Singla, Gan, Radanovic. *Admissible Policy Teaching through Reward Design.* arXiv:2201.02185, 2022.
- **[Huang and Zhu 2019]** Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* Int. Conf. on Decision and Game Theory for Security (Springer), 2019.
- **[Liu and Lai 2021]** Liu, Lai. *Provably Efficient Black-Box Action Poisoning Attacks Against Reinforcement Learning.* NeurIPS 34, 2021.
- **[Rakhsha et al. 2021a]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching in reinforcement learning via environment poisoning attacks.* JMLR 22(210):1–45, 2021.
- **[Rakhsha et al. 2021b]** Rakhsha, Zhang, Zhu, Singla. *Reward poisoning in reinforcement learning: Attacks against unknown learners in unknown environments.* arXiv:2102.08492, 2021.
- **[Rakhsha et al. 2020]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching via environment poisoning: Training-time adversarial attacks against reinforcement learning.* ICML, 2020.
- **[Sun, Huo, and Huang 2020]** Sun, Huo, Huang. *Vulnerability-aware poisoning mechanism for online rl with unknown dynamics.* arXiv:2009.00774, 2020.
- **[Zhang et al. 2020]** Zhang, Ma, Singla, Zhu. *Adaptive reward-poisoning attacks against reinforcement learning.* ICML, 2020.
- **[Bogunovic et al. 2021]** Bogunovic, Losalka, Krause, Scarlett. *Stochastic linear bandits robust to adversarial attacks.* AISTATS (PMLR), 2021.
- **[Garcelon et al. 2020]** Garcelon, Roziere, Meunier, Teytaud, Lazaric, Pirotta. *Adversarial Attacks on Linear Contextual Bandits.* arXiv:2002.03839, 2020.
- **[Guan et al. 2020]** Guan, Ji, Bucci Jr, Hu, Palombo, Liston, Liang. *Robust stochastic bandit algorithms under probabilistic unbounded adversarial attack.* AAAI 34, 4036–4043, 2020.
- **[Jun et al. 2018]** Jun, Li, Ma, Zhu. *Adversarial attacks on stochastic bandits.* NeurIPS 31:3640–3649, 2018.
- **[Liu and Shroff 2019]** Liu, Shroff. *Data poisoning attacks on stochastic bandits.* ICML (PMLR), 2019.
- **[Lu, Wang, and Zhang 2021]** Lu, Wang, Zhang. *Stochastic Graphical Bandits with Adversarial Corruptions.* AAAI 35, 8749–8757, 2021.
- **[Ma et al. 2018]** Ma, Jun, Li, Zhu. *Data poisoning attacks in contextual bandits.* Int. Conf. on Decision and Game Theory for Security (Springer), 186–204, 2018.
- **[Yang et al. 2021]** Yang, Hajiesmaili, Talebi, Lui, Wong. *Adversarial Bandits with Corruptions: Regret Lower Bound and No-regret Algorithm.* NeurIPS, 2021.
- **[Zuo 2020]** Zuo. *Near Optimal Adversarial Attack on UCB Bandits.* arXiv:2008.09312, 2020.
- **[Ma, Wu, and Zhu 2021]** Ma, Wu, Zhu. *Game Redesign in No-regret Game Playing.* arXiv:2110.11763, 2021.
- **[Ma et al. 2019]** Ma, Zhang, Sun, Zhu. *Policy poisoning in batch reinforcement learning and control.* NeurIPS 32:14570–14580, 2019.
- **[Rangi et al. 2022b]** Rangi, Xu, Tran-Thanh, Franceschetti. *Understanding the Limits of Poisoning Attacks in Episodic Reinforcement Learning.* IJCAI-22, 3394–3400, 2022.
- **[Zhang and Parkes 2008]** Zhang, Parkes. *Value-Based Policy Teaching with Active Indirect Elicitation.* AAAI 8, 208–214, 2008.
- **[Zhang, Parkes, and Chen 2009]** Zhang, Parkes, Chen. *Policy teaching through reward function learning.* 10th ACM Conference on Electronic Commerce, 295–304, 2009.
- **[Gleave et al. 2019]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[Guo et al. 2021]** Guo, Wu, Huang, Xing. *Adversarial policy learning in two-player competitive games.* ICML (PMLR), 3910–3919, 2021.
- **[Monderer and Tennenholtz 2004]** Monderer, Tennenholtz. *k-Implementation.* Journal of Artificial Intelligence Research 21:37–62, 2004.
- **[Anderson, Shoham, and Altman 2010]** Anderson, Shoham, Altman. *Internal implementation.* 9th Int. Conf. on Autonomous Agents and Multiagent Systems (AAMAS), vol. 1, 191–198, 2010.
- **[Banihashem, Singla, and Radanovic 2021]** Banihashem, Singla, Radanovic. *Defense against reward poisoning attacks in reinforcement learning.* arXiv:2102.05776, 2021.
- **[Lykouris et al. 2021]** Lykouris, Simchowitz, Slivkins, Sun. *Corruption-robust exploration in episodic reinforcement learning.* COLT, 3242–3245, 2021.
- **[Rangi et al. 2022a]** Rangi, Tran-Thanh, Xu, Franceschetti. *Saving stochastic bandits from poisoning attacks via limited data verification.* AAAI 36, 8054–8061, 2022.
- **[Wei, Dann, and Zimmert 2022]** Wei, Dann, Zimmert. *A model selection approach for corruption robust reinforcement learning.* Int. Conf. on Algorithmic Learning Theory (PMLR), 1043–1096, 2022.
- **[Wu et al. 2022]** Wu, Li, Xu, Zhang, Kailkhura, Kenthapadi, Zhao, Li. *COPA: Certifying Robust Policies for Offline Reinforcement Learning against Poisoning Attacks.* arXiv:2203.08398, 2022.
- **[Zhang et al. 2021a]** Zhang, Chen, Zhu, Sun. *Corruption-robust offline reinforcement learning.* arXiv:2106.06630, 2021.
- **[Zhang et al. 2021b]** Zhang, Chen, Zhu, Sun. *Robust policy gradient against strong data corruption.* ICML (PMLR), 12391–12401, 2021.
