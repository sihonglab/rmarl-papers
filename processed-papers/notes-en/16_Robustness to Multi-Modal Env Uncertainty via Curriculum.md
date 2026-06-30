# 16. Robustness to Multi-Modal Environment Uncertainty in MARL using Curriculum Learning

## Metadata
- **Title**: Robustness to Multi-Modal Environment Uncertainty in MARL using Curriculum Learning
- **Authors**: Aakriti Agrawal, Rohith Aralikatti, Yanchao Sun, Furong Huang
- **Affiliation**: Department of Computer Science, University of Maryland
- **Venue**: Pre-print (Under Review); arXiv 2023
- **Link/arXiv**: arXiv:2310.08746v1 [cs.LG] 12 Oct 2023

## Taxonomy
- **Robustness / perturbation type targeted**: Multi-modal environment uncertainty — simultaneous uncertainty in two of {reward, state/observation, action} (and transition dynamics in the general formulation); covers reward uncertainty, state/observation perturbation, and action uncertainty
- **Method paradigm**: Robust Markov game, maximin (worst-case) optimization, robust Nash equilibrium, curriculum learning (lookahead curriculum with progressive noise increase)
- **Keywords**: Multi-modal uncertainty, robust MARL, curriculum learning, robust Markov game, robust Nash equilibrium, sim-to-real

## TL;DR
The first work to formulate and address robustness to multi-modal (simultaneous, two-at-a-time) environment uncertainty in MARL, proposing an efficient lookahead curriculum-learning approach that progressively increases noise to achieve state-of-the-art robustness to reward, state, and action uncertainty across cooperative and competitive environments.

## Problem & Motivation
Real-world MARL requires training in simulation and transferring to the real world, where agents may lack accurate knowledge of environment parameters (reward/transition shifts), face noise in state/action/reward signals, or encounter hardware issues — all leading to environment uncertainty. Prior robustness work studies uncertainty in only a single environment variable (reward, transition, state, or action) individually, because a multi-agent system is already highly complex and non-stationary. However, real-world settings do not reveal which parameter is uncertain and may have uncertainty in multiple parameters simultaneously, motivating robustness to multi-modal uncertainty. The only prior multi-modal work (Kardeş et al., 2011b) handles reward + transition dynamics theoretically only.

## Robustness Setting
- **Threat model / uncertainty set**: A general robust Markov game $\bar{G}_{general}$ with uncertainty sets for reward ($\bar{R}^i_s$), transition probability ($\bar{P}_s$), perturbed state/observation ($\bar{O}^i$), and perturbed action ($\bar{A}^i$). Each uncertainty type is modeled with a truncated normal distribution: perturbed reward $\bar{R}^i = N_{trunc}(R^i, \epsilon)$, perturbed state $\bar{s}^i = N_{trunc}(s^i, \mu)$, perturbed action $\bar{a}^i = N_{trunc}(a^i, \nu)$, each truncated at 2× the standard deviation; increasing the std increases uncertainty. State perturbation affects only the observed state (input to the policy), not the true system state. Uncertainty types are categorized as aleatoric (reward, observation, action) vs epistemic.
- **Setting**: cooperative, competitive, and mixed (general robust Markov game); transition dynamics are deterministic in the experiments (no transition uncertainty studied empirically); online training via curriculum learning.

## Method
- Defines a general robust Markov game including four uncertainty types (state, action, reward, transition), and follows a maximin approach: minimize the Bellman value over the four uncertainty sets while maximizing over the agent's own policy $\pi^i$; introduces the robust Nash equilibrium (RNE) solution concept.
- Builds on Zhang et al. (2020) as the base model and injects state, reward, and action uncertainty (equations 3, 2, 4) into it.
- Uses curriculum learning to order training by increasing task difficulty, where difficulty is measured by the noise parameter ($\epsilon$, $\mu$, $\nu$); training first at low noise lets the model learn faster at higher noise, improving sample efficiency.
- Single-uncertainty case: "Lookahead CL" (Algorithm 1) starts noise at 0 and repeatedly increments $\lambda \in \{\epsilon, \mu, \nu\}$ by $\Delta\lambda$, retraining until success at each level until convergence fails.
- Multi-uncertainty case: Algorithms 2 (reward + state/action) and 3 (state + action) simultaneously increment two noise parameters, using a "SkipAhead" step for the evaluation-relevant parameter (no skip ahead for reward, since reward uncertainty is not used at evaluation), training to success at each combined level.

## Theoretical Contributions
- Formalizes the general robust Markov game $\bar{G}_{general}$ with four simultaneous uncertainty types and defines the Robust Nash Equilibrium (Definition 1).
- Theorem 1: Existence of robust Nash equilibrium → existence of optimal value function; proven via showing the operator $L^i$ is a contraction mapping on the value-function space $V$ (appendix 12).
- Notes that fully proving existence of the NE policy for $\bar{G}_{general}$ (with all uncertainties, partially observable) is out of scope; appendices reproduce the NE results for state uncertainty (He et al., 2023) and reward/transition uncertainty (Kardeş et al., 2011b / Zhang et al., 2020).

## Experiments
- **Environment/Benchmark**: Three multi-particle environments — Cooperative Navigation (cooperative, 3 agents/3 landmarks), Keep Away (competitive, 1 agent + 1 adversary), Physical Deception (mixed cooperative-competitive, 2 collaborative agents + 1 adversary). Tested with single-parameter uncertainty and combinations of two (state+reward, action+reward, state+action).
- **Baselines**: Base method without curriculum learning (the Zhang et al., 2020 base model); for reward and state robustness the state-of-the-art is Zhang et al. (2020) / Han et al. (2022). Action uncertainty has no baseline (this is the first work on it).
- **Evaluation metrics**: Success rate (e.g., all landmarks occupied; agent reaches goal within 100 steps; convergence defined as success rate > 90%), maximum noise level at which the model converges, and reward / training plots. Models evaluated 1000 times reporting mean and standard deviation (reward uncertainty shown via training plots only).

## Key Results
- Cooperative Navigation single-uncertainty: CL extends robustness from $\epsilon = 9$ (baseline) to $\epsilon = 47$/48 for reward, from $\mu = 0.5$ to $\mu = 1.1$ for state, and from $\nu = 2.0$ to $\nu = 2.4$ for action — achieving state-of-the-art robustness.
- Multi-modal (two-uncertainty) combinations: CL still outperforms the baseline; e.g., reward+state learns up to $\mu = 0.7$ (with $\epsilon$ up to 29 during training), reward+action up to $\nu = 2.4$ (with $\epsilon$ up to 50), state+action up to $\nu = 3$ (when $\mu = 0$) and $\mu = 1$ (when $\nu = 0$).
- Across Keep Away and Physical Deception, CL on a single parameter beats the no-CL baseline; CL on multiple parameters reaches a slightly lower max noise than single-parameter CL, but the same model then supports uncertainty in two parameters simultaneously, which is useful.

## Limitations & Future Work
- Does not show results for three uncertainties combined, as it makes learning difficult and reduces final robustness; future work aims to combine all three uncertainties.
- Transition-dynamics uncertainty is not studied empirically because the experimental transition dynamics are deterministic.
- A full theoretical proof of NE existence for the general multi-modal robust Markov game is out of scope; future work aims at conditional theoretical guarantees on NE existence for MARL with multi-modal uncertainty.
- Sim-to-real performance of the robust MARL model is identified as future work.

## Relevance to Survey
Sits on the "environment/model uncertainty" main line of robust MARL but is distinctive as the first paper to target multi-modal (multiple simultaneous) uncertainty rather than a single perturbation type, and the first to handle action uncertainty in MARL. Method-wise it links the robust Markov game / robust Nash equilibrium framework (Kardeş et al. 2011; Zhang et al. 2020; Han/He et al. 2022/2023) to the curriculum-learning-for-robustness line (Wu & Vorobeychik 2022; Mysore 2019), bridging robust-RL formulations with training-schedule techniques. A useful connector between the model-uncertainty, state-adversarial, and action-robust sub-lines of the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work]_

"**Robustness in RL.** Robustness in reinforcement learning is due to adversarial attacks (Liang et al., 2022) or uncertainty in model/environment parameters. In single agent RL, robustness to uncertainty is handled by maximin optimisation between the agent and the uncertainty set in the form of zero sum game (Tessler et al., 2019; Wiesemann et al., 2013; Xie et al., 2022; Nilim & El Ghaoui, 2005). In MARL, uncertainty is defined in the form of robust Markov game. The agents individually maximise their return while interacting with each other in presence of uncertainty. MARL research has made tremendous advancements in the recent times, however there is only very few work handling uncertainty. Kardeş et al. (2011b) is the only work on multi-modal uncertainty (reward and transition dynamics) but it only handles it theoretically. Some of the robustness to single uncertainty works handle reward, transition dynamics (Zhang et al., 2020) or state (Han et al., 2022) uncertainty. Li et al. (2019b); Sun et al. (2022) develop robustness to the adversarial agent's actions by training the agent to handle the worst case action of the adversarial agents in a competitive setting. Robustness to action perturbations in cooperative environment with adversaries had been studied in Nisioti et al. (2021); Phan et al. (2020; 2021)."

> _[Section 2, Related Work — Curriculum learning]_

"Curriculum learning Wang et al. (2022); Narvekar et al. (2020) has been widely used for improving robustness in various different domains, such as object classification (Sitawarin et al., 2021), automatic speech recognition (Braun et al., 2017), etc. CL for robustness in RL. Wu & Vorobeychik (2022) is the closest work to ours on using CL to improve robustness in RL. They implement bootstrapped opportunistic curriculum learning to improve robustness in single agent RL with RADIAL-DQN as baseline. Mysore (2019) develops robustness by developing generalisation to multiple tasks. They formulate the training curriculum as a multi-armed bandit problem which selects the task to train the RL model to give maximum reward gain."

"There is no existing work which uses CL for multi-modal uncertainty. It is also first time it is being used to handle robustness in MARL."

> _[Introduction]_

"Though there has been some work on robustness to uncertainty in reward, transition dynamics (Zhang et al., 2020), state (Han et al., 2022) and action (Li et al., 2019a) but they have been studied individually. Real world setting will not foretell the exact uncertain parameter and will have uncertainty in multiple environment parameters thus requiring the need to develop robustness to multi-modal uncertainty."

### Cited references (resolved from the paper's bibliography)
- **[Liang et al., 2022]** Liang, Sun, Zheng, Huang. *Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning.* NeurIPS 2022.
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Wiesemann et al., 2013]** Wiesemann, Kuhn, Rustem. *Robust Markov decision processes.* Mathematics of Operations Research, 2013.
- **[Xie et al., 2022]** Xie, Sodhani, Finn, Pineau, Zhang. *Robust policy learning over multiple uncertainty sets.* ICML 2022.
- **[Nilim & El Ghaoui, 2005]** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 2005.
- **[Kardeş et al., 2011b]** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **[Zhang et al., 2020]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Han et al., 2022]** Han, Su, He, Han, Yang, Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv preprint arXiv:2212.02705, 2022.
- **[Li et al., 2019a / 2019b]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Sun et al., 2022]** Sun, Kim, How. *Romax: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* ICRA 2022.
- **[Nisioti et al., 2021]** Nisioti, Bloembergen, Kaisers. *Robust multi-agent q-learning in cooperative games with adversaries.* AAAI 2021.
- **[Phan et al., 2020]** Phan, Gabor, Sedlmeier, Ritz, Kempter, Klein, Sauer, Schmid, Wieghardt, Zeller, et al. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
- **[Phan et al., 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Wang et al., 2022]** Wang, Chen, Zhu. *A survey on curriculum learning.* IEEE Transactions on Pattern Analysis & Machine Intelligence, 2022.
- **[Narvekar et al., 2020]** Narvekar, Peng, Leonetti, Sinapov, Taylor, Stone. *Curriculum learning for reinforcement learning domains: A framework and survey.* JMLR 2020.
- **[Sitawarin et al., 2021]** Sitawarin, Chakraborty, Wagner. *SAT: Improving adversarial training via curriculum-based loss smoothing.* 14th ACM Workshop on Artificial Intelligence and Security, 2021.
- **[Braun et al., 2017]** Braun, Neil, Liu. *A curriculum learning method for improved noise robustness in automatic speech recognition.* EUSIPCO 2017.
- **[Wu & Vorobeychik, 2022]** Wu, Vorobeychik. *Robust deep reinforcement learning through bootstrapped opportunistic curriculum.* ICML 2022.
- **[Mysore, 2019]** Mysore. *Reward-guided curriculum for robust reinforcement learning.* 2019.
