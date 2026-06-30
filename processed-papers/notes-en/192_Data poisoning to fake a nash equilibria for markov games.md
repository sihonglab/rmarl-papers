# 192. Data Poisoning to Fake a Nash Equilibrium in Markov Games

## Metadata
- **Title**: Data Poisoning to Fake a Nash Equilibrium in Markov Games
- **Authors**: Young Wu, Jeremy McMahan, Xiaojin Zhu, Qiaomin Xie
- **Affiliation**: University of Wisconsin - Madison
- **Venue**: AAAI 2024 (The Thirty-Eighth AAAI Conference on Artificial Intelligence)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Offline data poisoning / reward poisoning attacks on MARL (adversarial manipulation of the training dataset to install a fictitious Nash equilibrium)
- **Method paradigm**: Game-theoretic equilibrium characterization (unique Nash set / unique Nash polytope), attacker's theory-of-mind set, linear program / convex optimization, inverse reinforcement learning generalization
- **Keywords**: data poisoning, reward poisoning, two-player zero-sum Markov game, Markov-perfect Nash equilibrium, offline MARL, linear program

## TL;DR
The paper characterizes offline (reward) data poisoning attacks on two-player zero-sum Markov games by introducing the "unique Nash set" — the set of Q functions that make a target joint policy the unique Markov-perfect Nash equilibrium — and shows the optimal attack reduces to moving the attacker's theory-of-mind set inside this polytope, which can be solved efficiently as a linear program.

## Problem & Motivation
Data poisoning attacks are well studied for supervised learning and single-agent RL, but it is unclear whether they threaten Markov games. The paper answers affirmatively: under mild conditions an attacker can force two game-playing agents to adopt any fictitious Nash equilibrium (not necessarily a true NE of the original game) while minimizing the attack cost. Single-agent RL poisoning results cannot be directly transferred because MARL has no optimal policies (equilibria are computed instead), there may be multiple significantly different equilibria, and installing a target policy as the unique equilibrium is therefore difficult. The work targets the offline two-player zero-sum Markov game setting and aims to understand the structure of such attacks as a necessary step before designing more robust MARL algorithms.

## Robustness Setting
- **Threat model / uncertainty set**: An attacker observes the original offline dataset D (state, joint action, reward tuples) and may poison it into D' at cost C(D, D'). The attacker has a "theory of mind" (ToM) — an approximate belief, not full knowledge, of the victim's learning algorithm, modeled as the set of plausible Q functions (or rewards) the victim entertains given the data. The attack is successful iff the ToM set is moved inside the unique Nash set U(π†) for the target policy π†. Reward poisoning uses an L1 cost; the cost may be any convex function. Unlike prior work, full data coverage is NOT required, and the victims compute Markov Perfect Equilibrium (MPE), a weaker solution concept than Dominant Strategy Markov Perfect Equilibrium (DSMPE).
- **Setting**: Two-player zero-sum, competitive Markov game; offline; accommodates both model-based and model-free victims (maximum likelihood, pessimistic/optimistic, data-splitting, confidence-bound learners).

## Method
- Define the unique Nash set U(π) as the inverse image of the Nash map from a single target pure strategy profile back to the reward (normal-form) or Q-function (Markov game) space; characterize it as a polytope of games for which π is a strict Nash equilibrium in every stage game (Proposition 1, Theorem 1).
- Introduce the ι-strict unique Nash set U(π; ι) to avoid strict inequalities, giving a closed polytope where strict NE conditions hold with a reward gap of at least ι.
- Model the attacker's theory of mind T(D) as the plausible set of games the victim estimates from the data, with a linear outer approximation (hypercube) parameterized by a point estimate (e.g., R_MLE / Q_MLE) and a radius ρ; give concrete ToM examples for maximum-likelihood, pessimistic-optimistic (Cui and Du 2022), data-splitting, and confidence-bound (Wu et al. 2023) victims.
- Formulate the attacker's problem as minimizing cost C(D, D') subject to T(D') ⊆ U(π†); relax it using the ι-strict unique Nash polytope and the linear ToM hypercube so that moving one corner of the hypercube inside the polytope suffices, converting the problem into an efficiently solvable linear program (Proposition 2, Theorem 2), using a dual LP to keep constraints linear in the poisoned rewards.
- Provide a sufficient feasibility condition (Theorem 3): the reward poisoning problem is feasible if the ToM radius ρ(R)_h(s,a) ≤ (b − ι)/(4H).

## Theoretical Contributions
- Unique Nash polytope characterization for normal-form games (Proposition 1) and Markov games (Theorem 1), generalizing the reward polytope from inverse RL to MARL.
- Reward poisoning linear program formulations as relaxations of the attacker's problem (Proposition 2 for normal-form; Theorem 2 for Markov games), with proof that the LP solution is feasible for the original problem.
- A sufficient (but not necessary) feasibility condition for the reward poisoning LP (Theorem 3), including the radius bound (b − ι)/(4H).
- Discussion results: faking a unique mixed-strategy NE is generally impossible (sensitivity of mixing probabilities); faking a unique single-agent optimal policy adapts from the LP; faking a unique coarse correlated equilibrium per stage is equivalent to the problem for two-player zero-sum games.

## Experiments
- **Environment/Benchmark**: Rock Paper Scissors (RPS) game with partial coverage; Stochastic Matching Penny game (the penalty-kick game in soccer) with randomly generated datasets from Uniform distributions.
- **Baselines**: The "Feasible attack" (Table 1 construction, b = 1) and the Dominant Strategy Equilibrium (DSE) attack from (Wu et al. 2023).
- **Evaluation metrics**: Attack cost (L1 cost of modifying rewards); average costs across n = 1, 10, 100; before-vs-after reward distribution box plots.

## Key Results
- On the RPS toy dataset (target π† = (R, R)) with ρ = 0 and ι = 0.01, the proposed attack achieves cost 2.02, versus cost 4 for the feasible attack (Table 1, b = 1).
- Under partial coverage, the attack of (Wu et al. 2023) is not feasible due to its full-coverage requirement, whereas the proposed method works.
- On Stochastic Matching Penny, average attack costs (Table 6) for the proposed attack are 1.06 / 9.09 / 99.47 at n = 1 / 10 / 100, lower than the feasible attack (2.12 / 16.08 / 250.46) and the DSE attack (2.06 / 18.31 / 198.38).

## Limitations & Future Work
- Faking a unique mixed-strategy Nash equilibrium (or stochastic policy for Markov games) is in general impossible as long as the theory-of-mind set has non-zero volume, due to sensitivity of mixing probabilities to small reward perturbations.
- The L1 cost is used for simplicity to keep the optimization a linear program; more general convex costs remain convex but harder to solve.
- The feasibility condition (Theorem 3) is sufficient but not necessary.
- The work focuses on offline reward poisoning of two-player zero-sum Markov games; it is framed as a necessary step before designing more robust MARL algorithms.

## Relevance to Survey
This paper sits in the "adversarial attacks on MARL / reward (data) poisoning" line of robust MARL, providing an attack-side, game-theoretic characterization that motivates the need for robust offline MARL learners. By generalizing the inverse-RL reward polytope to the unique Nash set for Markov games, it connects inverse reinforcement learning, equilibrium-based MARL, and adversarial/security threat models. It complements the model-uncertainty and minimax-adversarial-training lines by characterizing what an attacker can force, thereby informing the design of robustness defenses against training-data corruption.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Data poisoning attacks have been well studied in supervised learning (intentionally forcing the learner to train a wrong classifier) and reinforcement learning (wrong policy) (Banihashem et al. 2022; Huang and Zhu 2019; Liu and Lai 2021; Rakhsha et al. 2021a,b, 2020; Sun, Huo, and Huang 2020; Zhang et al. 2020; Ma et al. 2019; Rangi et al. 2022; Zhang and Parkes 2008; Zhang, Parkes, and Chen 2009). Can data poisoning attacks be a threat to Markov Games, too? This paper answers this question in the affirmative: Under mild conditions, an attacker can force two game-playing agents to adopt any fictitious Nash Equilibrium (NE), which does not need to be a true NE of the original Markov Game."

> _[Introduction]_

"This problem is not well studied in the literature. Naive approaches – such as modifying all the actions in the dataset to those specified by the target policy (π†_1, π†_2) – might not achieve the attack goal for MARL learners who assign penalties due to the lack of data coverage. Modifying all the rewards in the dataset that coincide with the target policy to the reward upper bound might be feasible, but would not be optimal in terms of attack cost C. Results on data poisoning against single-agent RL cannot be directly applied to the multi-agent case. In particular, there are no optimal policies in MARL, and equilibrium policies are computed instead. There could be multiple equilibria that are significantly different, and consequently, installing a target policy as the unique equilibrium is difficult."

> _[Introduction]_

"Adversarial attacks on MARL have been studied in some recent work (Ma, Wu, and Zhu 2021; Gleave et al. 2019; Guo et al. 2021), but we are only aware of one previous work (Wu et al. 2023) on offline reward poisoning against MARL. Nonetheless, they require a strong assumption of full data coverage, and that the learners compute the Dominant Strategy Markov Perfect Equilibrium (DSMPE). In contrast, we do not require full coverage, and we consider a weaker solution concept, Markov Perfect Equilibrium (MPE). Our general attack framework also accommodates other forms of data poisoning."

> _[Introduction]_

"Understanding adversarial attacks in the multi-agent setting is critical since many real-life applications of MARL problems are susceptible to adversarial attacks. Examples of two-player zero-sum games include board games such as GO and Chess (Silver et al. 2017, 2016), where the learners use historical game plays as training data and an attacker can potentially alter the data to change the behavior of the trained agents. In the case of competitive robotics, for example, robot soccer (Gu et al. 2017; Riedmiller et al. 2009; Kober, Bagnell, and Peters 2013), they are trained on offline datasets and the attacker can mislead the trained policies by modifying the training sets. For finance application, especially algorithmic or high-frequency stock or option trading (Lee et al. 2007; Lee and O 2002) that are usually trained on historical prices, if the database is corrupted by an attacker, the learned trading strategies can be sub-optimal as well. There are also examples of multi-player games that have two-player games as special cases, for example, video games (Vinyals et al. 2019; Jaderberg et al. 2019; Berner et al. 2019), card games (Brown and Sandholm 2019; Brown, Sandholm, and Machine 2017), autonomous driving (Shalev-Shwartz, Shammah, and Shashua 2016), automated warehouses (Yang, Juntao, and Lingling 2020), and economic policymaking, which can all be trained on offline datasets and become vulnerable to adversarial attacks. In all of the above MARL applications, the threat of adversarial attacks has not been investigated."

### Cited references (resolved from the paper's bibliography)
- **[Banihashem et al. 2022]** Banihashem, Singla, Gan, Radanovic. *Admissible Policy Teaching through Reward Design.* arXiv:2201.02185, 2022.
- **[Huang and Zhu 2019]** Huang, Zhu. *Deceptive reinforcement learning under adversarial manipulations on cost signals.* International Conference on Decision and Game Theory for Security (Springer) 2019.
- **[Liu and Lai 2021]** Liu, Lai. *Provably Efficient Black-Box Action Poisoning Attacks Against Reinforcement Learning.* NeurIPS 2021.
- **[Rakhsha et al. 2020]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching via environment poisoning: Training-time adversarial attacks against reinforcement learning.* ICML 2020.
- **[Rakhsha et al. 2021a]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching in reinforcement learning via environment poisoning attacks.* JMLR 22(210):1–45, 2021.
- **[Rakhsha et al. 2021b]** Rakhsha, Zhang, Zhu, Singla. *Reward poisoning in reinforcement learning: Attacks against unknown learners in unknown environments.* arXiv:2102.08492, 2021.
- **[Sun, Huo, and Huang 2020]** Sun, Huo, Huang. *Vulnerability-aware poisoning mechanism for online rl with unknown dynamics.* arXiv:2009.00774, 2020.
- **[Zhang et al. 2020]** Zhang, Ma, Singla, Zhu. *Adaptive reward-poisoning attacks against reinforcement learning.* ICML 2020.
- **[Ma et al. 2019]** Ma, Zhang, Sun, Zhu. *Policy poisoning in batch reinforcement learning and control.* NeurIPS 2019.
- **[Rangi et al. 2022]** Rangi, Xu, Tran-Thanh, Franceschetti. *Understanding the Limits of Poisoning Attacks in Episodic Reinforcement Learning.* IJCAI-22.
- **[Zhang and Parkes 2008]** Zhang, Parkes. *Value-Based Policy Teaching with Active Indirect Elicitation.* AAAI 2008.
- **[Zhang, Parkes, and Chen 2009]** Zhang, Parkes, Chen. *Policy teaching through reward function learning.* ACM EC 2009.
- **[Ma, Wu, and Zhu 2021]** Ma, Wu, Zhu. *Game Redesign in No-regret Game Playing.* arXiv:2110.11763, 2021.
- **[Gleave et al. 2019]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[Guo et al. 2021]** Guo, Wu, Huang, Xing. *Adversarial policy learning in two-player competitive games.* ICML 2021.
- **[Wu et al. 2023]** Wu, McMahan, Zhu, Xie. *Reward Poisoning Attacks on Offline Multi-Agent Reinforcement Learning.* AAAI 2023.
- **[Silver et al. 2016]** Silver, Huang, Maddison, Guez, Sifre, Van Den Driessche, Schrittwieser, Antonoglou, Panneershelvam, Lanctot, et al. *Mastering the game of Go with deep neural networks and tree search.* Nature 529(7587):484–489, 2016.
- **[Silver et al. 2017]** Silver, Schrittwieser, Simonyan, Antonoglou, Huang, Guez, Hubert, Baker, Lai, Bolton. *Mastering the game of go without human knowledge.* Nature 550(7676):354–359, 2017.
- **[Gu et al. 2017]** Gu, Holly, Lillicrap, Levine. *Deep reinforcement learning for robotic manipulation with asynchronous off-policy updates.* ICRA 2017.
- **[Riedmiller et al. 2009]** Riedmiller, Gabel, Hafner, Lange. *Reinforcement learning for robot soccer.* Autonomous Robots 27:55–73, 2009.
- **[Kober, Bagnell, and Peters 2013]** Kober, Bagnell, Peters. *Reinforcement learning in robotics: A survey.* The International Journal of Robotics Research 32(11):1238–1274, 2013.
- **[Lee et al. 2007]** Lee, Park, Jangmin O, Lee, Hong. *A multiagent approach to q-learning for daily stock trading.* IEEE Transactions on Systems, Man, and Cybernetics-Part A 37(6):864–877, 2007.
- **[Lee and O 2002]** Lee, O. *A multi-agent Q-learning framework for optimizing stock trading systems.* International Conference on Database and Expert Systems Applications (Springer) 2002.
- **[Vinyals et al. 2019]** Vinyals, Babuschkin, Czarnecki, Mathieu, Dudzik, Chung, Choi, Powell, Ewalds, Georgiev, et al. *Grandmaster level in StarCraft II using multi-agent reinforcement learning.* Nature 575(7782):350–354, 2019.
- **[Jaderberg et al. 2019]** Jaderberg, Czarnecki, Dunning, Marris, Lever, Castaneda, Beattie, Rabinowitz, Morcos, Ruderman, et al. *Human-level performance in 3D multiplayer games with population-based reinforcement learning.* Science 364(6443):859–865, 2019.
- **[Berner et al. 2019]** Berner, Brockman, Chan, Cheung, Dębiak, Dennison, Farhi, Fischer, Hashme, Hesse, et al. *Dota 2 with large scale deep reinforcement learning.* arXiv:1912.06680, 2019.
- **[Brown and Sandholm 2019]** Brown, Sandholm. *Superhuman AI for multiplayer poker.* Science 365(6456):885–890, 2019.
- **[Brown, Sandholm, and Machine 2017]** Brown, Sandholm, Machine. *Libratus: The Superhuman AI for No-Limit Poker.* IJCAI 2017, 5226–5228.
- **[Shalev-Shwartz, Shammah, and Shashua 2016]** Shalev-Shwartz, Shammah, Shashua. *Safe, multi-agent, reinforcement learning for autonomous driving.* arXiv:1610.03295, 2016.
- **[Yang, Juntao, and Lingling 2020]** Yang, Juntao, Lingling. *Multi-robot path planning based on a deep reinforcement learning DQN algorithm.* CAAI Transactions on Intelligence Technology 5(3):177–183, 2020.
