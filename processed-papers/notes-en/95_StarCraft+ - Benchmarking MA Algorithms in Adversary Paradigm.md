# 95. StarCraft+: Benchmarking Multi-agent Algorithms in Adversary Paradigm

## Metadata
- **Title**: StarCraft+: Benchmarking Multi-agent Algorithms in Adversary Paradigm
- **Authors**: Yadong Li, Tong Zhang, Bo Huang, Zhen Cui
- **Affiliation**: School of Computer Science and Engineering, Nanjing University of Science and Technology, Nanjing, China; School of Information Science and Engineering, Zaozhuang University, Zaozhuang, China
- **Venue**: Not specified (arXiv preprint, arXiv:2512.16444v1 [cs.AI], 18 Dec 2025; manuscript formatted for an IEEE journal/LaTeX class)
- **Link/arXiv**: arXiv:2512.16444v1; code: https://github.com/dooliu/SC2BA

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial opponents (replacing fixed built-in AI bots with learning/evolving MARL-controlled opponents); opponent non-stationarity and diversity; generalization to unseen opponents; scenario perturbations (symmetric/asymmetric troop layouts)
- **Method paradigm**: Benchmark/environment construction (algorithm-vs-algorithm adversary), self-play-style dual-team competition, mixed-opponent training, empirical evaluation of value- and policy-based MARL algorithms
- **Keywords**: Multi-Agent Reinforcement Learning, evolvable opponents, dual-algorithm paired adversary, multi-algorithm mixed adversary, StarCraft Multi-Agent Challenge, robustness

## TL;DR
The paper builds SC2BA (StarCraft II Battle Arena), an algorithm-vs-algorithm benchmarking environment plus an APyMARL library, that replaces SMAC's fixed built-in AI opponents with learning/evolvable MARL-controlled opponents under two adversary modes (dual-algorithm paired and multi-algorithm mixed), and benchmarks eight classic MARL algorithms to expose effectivity, sensibility, and scalability problems while showing adversarial training boosts policy diversity, robustness, and generalization.

## Problem & Motivation
Deep MARL is widely benchmarked on SMAC, but in SMAC (and most MARL environments) opponent units are controlled by fixed built-in AI bots. This monotonic, static opponent leads to biased policies that exploit weaknesses of the pre-set strategies, limits strategy diversity, and generalizes poorly to other opponents. The paper argues that a good MAS for evaluating/learning MARL must address opponent non-monotonicity, opponent evolvability, adversarial fairness, and system usability. Existing frameworks (PyMARL, EPyMARL) only support single-team training against built-in bots and cannot manipulate dual-team adversarial agents, hindering algorithm-vs-algorithm research and comprehensive assessment.

## Robustness Setting
- **Threat model / uncertainty set**: The "perturbation" is the opponent itself. Instead of a fixed built-in AI bot, the opponent (blue team) is controlled by MARL algorithms that are either dynamically evolving (dual-algorithm paired mode) or a randomly selected, fixed, well-trained model per episode drawn from a pool of nine models (multi-algorithm mixed mode). Additional scenario stress comes from asymmetric troop layouts (e.g., 5m_vs_6m, 10m_vs_11m, MMM2). No formal uncertainty set is defined; the setting is empirical.
- **Setting**: mixed (cooperative within a team, competitive between two teams / zero-sum-style battle); CTDE following SMAC (decentralized partially observable agents, sight range 9, global state only available during training); online (algorithms learn through online competing interactions).

## Method
- Builds the SC2BA environment on StarCraft II (via Linux SC2 binary, SC2 API, PySC2), with three modules: a configuration module (unified map file, controllable/customizable scenarios, assignment of distinct MARL models to each team), an interaction module (gym-style vectorized observation/state/action/reward exchange), and a bottom-level control module (game-engine API, procedural control of episodes).
- Defines two adversary modes: (1) dual-algorithm paired adversary, where two teams are each controlled by a continuously learning MARL algorithm that must adapt to an evolving opponent; (2) multi-algorithm mixed adversary, where one algorithm faces opponents whose control model is randomly selected each episode from a set of fixed, pre-trained models (eight algorithms plus one built-in AI bot).
- Designs symmetric and asymmetric combat scenarios (Table I: 3m, 8m, 25m, MMM, 2s3z, 3s5z, 1c3s5z, 5m_vs_6m, 10m_vs_11m, MMM2) and redefines the SMAC reward function, adding episodic penalties for failures and draws to discourage passive play; enforces fairness via matched battle forces, central-symmetric spatial stations, and identical (mirrored) observation views.
- Develops APyMARL, a PyTorch-based, modular library extending PyMARL with a standardized multi-agent environment interaction wrapper, dual-team adversarial training/testing controllers, and a flexible parameter configurator, enabling algorithm-to-algorithm training/testing.
- Benchmarks eight algorithms (QMIX, VDN, FOP, DOP, QPLEX, QTRAN, COMA, IQL); model parameters initialized randomly or from well-trained (built-in-AI) models; dual-algorithm mode trained for 10 million steps, mixed mode for 2 million steps (same as SMAC).

## Theoretical Contributions
None / mostly empirical. The paper is a benchmark/environment and empirical study; it provides no convergence, sample-complexity, equilibrium, or certified-robustness analysis.

## Experiments
- **Environment/Benchmark**: SC2BA (StarCraft II Battle Arena), built on StarCraft II / SMAC; symmetric scenarios (3m, 8m, 2s3z, 3s5z, MMM, 1c3s5z, 25m) and asymmetric scenarios (5m_vs_6m, 10m_vs_11m, MMM2).
- **Baselines**: Eight representative MARL algorithms compared against each other — QMIX, VDN, FOP, DOP, QPLEX, QTRAN, COMA, IQL — plus the SMAC built-in AI bots mode as a comparison training mode.
- **Evaluation metrics**: Median win percentage (averaged across scenarios), number of scenarios in which an algorithm dominates ("Maps Best"), median test return (normalized 0–1), and joint-action-distribution diversity via PCA + MeanShift clustering; five independent runs per case, 32 test episodes by default, following the SMAC protocol.

## Key Results
- In the dual-algorithm paired adversary mode, performances fluctuate (no algorithm reaches near-100% win rates as in built-in-AI SMAC); no fixed strategy guarantees consistent victory. DOP (policy-based) and QMIX (value-based) perform best, dominating four and two scenarios respectively, but no algorithm dominates all scenarios. Policy-based methods are less stable; value-based methods are more stable. Policy-based methods (esp. DOP) are more effective in hard scenarios.
- MARL algorithms are extremely sensitive to slight troop changes: in 5m_vs_6m all algorithms (including the best, DOP) almost fail against COMA (the poorest algorithm) when COMA gains just one extra unit; episode returns stay below 0.6.
- In the multi-algorithm mixed adversary mode, win rates rise with smaller fluctuations than the dual mode (opponents diverse but not updated); value-based methods improve more consistently; asymmetric scenarios remain very hard (none match symmetric-scenario performance; in 5m_vs_6m no algorithm exceeds 50% win rate).
- Adversarial training boosts generalization: increasing opponent diversity (mixed mode) improves performance against built-in AI bots in most scenarios; agents trained in paired/mixed SC2BA modes beat challengers trained only on built-in AI bots, with paired (evolvable/dynamic) opponents giving slightly higher win rates and higher learned joint-action diversity (visualized via PCA/MeanShift).

## Limitations & Future Work
- In the multi-algorithm mixed mode the blue-team models are fixed (pre-trained) and not jointly updated during adversary due to optimization complexity; jointly optimizing multiple blue-team models (dynamic mixed adversary) is left as future work.
- Current MARL algorithms lack scalability/robustness to troop-layout (asymmetric) changes; new mechanisms (e.g., rescheduling the reward function, richer evaluation metrics) are needed.
- Identified open problems include sensibility to scenario layout, difficulty of heterogeneous scenarios, fluctuation of algorithm adversary, and joint evolution of multiple opponents; future work will explore dynamic multi-algorithm mixed adversary and design more asymmetric scenarios.

## Relevance to Survey
This is an environment/benchmark contribution on the "adversarial agents" line of robust MARL: it operationalizes robustness as the ability to learn and adapt against evolving and diverse (rather than fixed/monotonic) opponents, directly addressing opponent non-stationarity and generalization to unseen opponents. It complements theory-oriented robust MARL work by providing a StarCraft II algorithm-vs-algorithm testbed (SC2BA/APyMARL) for empirically stress-testing the robustness, diversity, and generalization of cooperative MARL algorithms, and it surfaces practical fragilities (e.g., sensitivity to slight troop asymmetry) relevant to robustness evaluation.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work]_

"MARL simulation environments are typically classified into cooperative, competitive, and mixing settings based on specific requirements [31]. Cooperative MARL constitutes a great portion of MARL environments, where all agents collaborate with each other to achieve some shared goal."

> _[Section II, Related Work — competitive and mixed settings]_

"Competitive MARL settings are typically modeled as zero-sum games. MA competitive tasks primarily focus on classic games, including board games and poker games. At present, there are two notable competitive MARL environments: Go and Texas Hold'em Poker, which are archetypal instances of multiplayer perfect-information and partial-information extensive-form games, respectively. Go [39] is an ancient and intellectually captivating strategy board game, often regarded as one of the oldest, most complex, and highly challenging games in existence. Texas Hold'em Poker [40] usually entails the participation of two or more players, with each player initially receiving two face-down private cards."

> _[Section II, Related Work — RTS games and StarCraft]_

"In comparison to the former two settings, mixed-setting environments are more challenging. After achieving remarkable advancements in RL within board game environments, researchers turned their attention to electronic games and have developed excellent MARL simulation environments, such as Atari [41], Super Mario [42], Gran Turismo racing games [43], Doom [44], GRF [25], Dota2 [45], Honor of Kings [46], StarCraft [5]. Among them, Real-Time Strategy (RTS) games have garnered considerable attention. After AlphaZero [39] emerged as the strongest general-purpose AI in chess, DeepMind shifted its focus to the RTS game StarCraft II. Vinyals et al. [47] introduced the StarCraft II Learning Environment (SC2LE), which focuses on tackling the full game of StarCraft II by centralized controlling hundreds of agents to defeat competitors. Shortly thereafter, Vinyals et al. [5] trained AlphaStar using SC2LE, showcasing master-level proficiency and achieving the milestone of defeating professional human players for the first time. However, SC2LE focused on the 1v1 mode, where agents act the role of player and have centralized control over all combat units. This setup is fundamentally unrealistic in the real world. Therefore, Samvelyan et al. [29] proposed SMAC based on SC2LE, focusing on decentralized micromanagement challenges instead of centralized control over the entire game. The design of the SMAC environment simplifies the validation of MARL algorithms and reduces the demand for high computational resources. This accessibility has encouraged greater participation from researchers, significantly fostering the development of MARL research."

> _[Section II, Related Work — built-in AI bots, robustness, and online adversary]_

"However, in the aforementioned works, the enemy units were controlled by the built-in AI bots and the agents engaged in training and testing against adversaries with identical behavioral patterns. This setting prevents the enemy forces from exerting pressure on the agents, keeping them in a constant disadvantaged position. Instead, it allows the agents to easily find ways to defeat their opponents and achieve victory. Taking SMAC as an example, Ellis et al. [48] discovered that retained only agent ID and timestep information in the observations, QMIX [49] and MAPPO [50] algorithms achieved performance comparable to using all available information. This is highly disadvantageous for agents to learn robust strategies. Contrarily, Emergent tools [51] demonstrate the potential for simultaneous online learning by both factions. The hiders and seekers exhibit extraordinary strategy and counter-strategy in their game against each other. Inspired by this, we develop a new adversarial environment named SC2BA. Different from previous works, our work propose an online game platform with two competing teams, where agents from both sides could optimize themselves to struggle for victory. Accordingly, the algorithm-vs-algorithm adversary could be run directly and their performance could be validated more comprehensively."

### Cited references (resolved from the paper's bibliography)
- **[5]** O. Vinyals, I. Babuschkin, W. M. Czarnecki, et al. *Grandmaster level in StarCraft II using multi-agent reinforcement learning.* Nature, vol. 575, no. 7782, pp. 350–354, 2019.
- **[25]** K. Kurach, A. Raichuk, P. Stańczyk, et al. *Google Research Football: A novel reinforcement learning environment.* AAAI 2020, pp. 4501–4510.
- **[29]** M. Samvelyan, T. Rashid, C. S. De Witt, et al. *The StarCraft Multi-Agent Challenge.* arXiv:1902.04043, 2019.
- **[31]** K. Zhang, Z. Yang, T. Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, pp. 321–384, 2021.
- **[39]** D. Silver, J. Schrittwieser, K. Simonyan, et al. *Mastering the game of Go without human knowledge.* Nature, vol. 550, no. 7676, pp. 354–359, 2017.
- **[40]** M. Bowling, N. Burch, M. Johanson, et al. *Heads-up limit hold'em poker is solved.* Science, vol. 347, no. 6218, pp. 145–149, 2015.
- **[41]** V. Mnih, K. Kavukcuoglu, D. Silver, et al. *Playing Atari with deep reinforcement learning.* arXiv:1312.5602, 2013.
- **[42]** S. Kühn, T. Gleich, R. C. Lorenz, et al. *Playing Super Mario induces structural brain plasticity: gray matter changes resulting from training with a commercial video game.* Molecular Psychiatry, vol. 19, no. 2, pp. 265–271, 2014.
- **[43]** P. R. Wurman, S. Barrett, K. Kawamoto, et al. *Outracing champion Gran Turismo drivers with deep reinforcement learning.* Nature, vol. 602, no. 7896, pp. 223–228, 2022.
- **[44]** M. Kempka, M. Wydmuch, G. Runc, et al. *ViZDoom: A Doom-based AI research platform for visual reinforcement learning.* IEEE Conference on Computational Intelligence and Games (CIG), 2016, pp. 341–348.
- **[45]** C. Berner, G. Brockman, B. Chan, et al. *Dota 2 with large scale deep reinforcement learning.* arXiv:1912.06680, 2019.
- **[46]** D. Ye, Z. Liu, M. Sun, et al. *Mastering complex control in MOBA games with deep reinforcement learning.* AAAI 2020, pp. 6672–6679.
- **[47]** O. Vinyals, T. Ewalds, S. Bartunov, et al. *StarCraft II: A new challenge for reinforcement learning.* arXiv:1708.04782, 2017.
- **[48]** B. Ellis, S. Moalla, M. Samvelyan, et al. *SMACv2: An improved benchmark for cooperative multi-agent reinforcement learning.* arXiv:2212.07489, 2022.
- **[49]** T. Rashid, M. Samvelyan, C. S. De Witt, et al. *Monotonic value function factorisation for deep multi-agent reinforcement learning (QMIX).* Journal of Machine Learning Research, vol. 21, no. 1, pp. 7234–7284, 2020.
- **[50]** C. Yu, A. Velu, E. Vinitsky, et al. *The surprising effectiveness of PPO in cooperative multi-agent games (MAPPO).* NeurIPS, vol. 35, pp. 24611–24624, 2022.
- **[51]** B. Baker, I. Kanitscheider, T. Markov, et al. *Emergent tool use from multi-agent autocurricula.* arXiv:1909.07528, 2019.
