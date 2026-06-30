# 85. Resilient Multi-Agent Reinforcement Learning with Adversarial Value Decomposition

## Metadata
- **Title**: Resilient Multi-Agent Reinforcement Learning with Adversarial Value Decomposition
- **Authors**: Thomy Phan, Lenz Belzner, Thomas Gabor, Andreas Sedlmeier, Fabian Ritz, Claudia Linnhoff-Popien
- **Affiliation**: LMU Munich; MaibornWolff
- **Venue**: AAAI 2021 (The Thirty-Fifth AAAI Conference on Artificial Intelligence)
- **Link/arXiv**: Code available at https://github.com/thomyphan/resilient-marl

## Taxonomy
- **Robustness / perturbation type targeted**: Agent changes (updates or failures of hardware/software components) in cooperative multi-agent systems; resilience against arbitrary portions of the MAS changing behavior, including unknown adversary/failure agents at test time
- **Method paradigm**: Adversarial training (protagonist vs. antagonist teams), value decomposition (VDN-based), CTDE, minimax/zero-sum sub-games, randomized adversary ratio
- **Keywords**: Resilience, cooperative MARL, adversarial value decomposition, antagonist-ratio, CTDE, VDN

## TL;DR
The paper proposes RADAR (Resilient Adversarial value Decomposition with Antagonist-Ratios), a value-decomposition scheme that trains competing protagonist/antagonist teams of varying size — sampling the adversary ratio uniformly during training — to improve worst-case resilience against arbitrary agent changes without introducing new hyperparameters.

## Problem & Motivation
In cooperative multi-agent systems, agents can change behavior due to updates (new software, temporary replacements) or failures (faulty hardware/software). A resilient MAS should still collaborate with novel agents or degrade gracefully rather than fail entirely. Most state-of-the-art cooperative MARL is evaluated only on idealized settings with the same or similar agents seen during training, risking overfitting and catastrophic failure when agents significantly change — especially dangerous in safety-critical environments. Prior resilient-MARL work based on adversarial learning targets specialized settings with a fixed number of adversaries (e.g., a single productive agent), lacking flexibility for arbitrary portions of the MAS changing and introducing extra hyperparameters (fraction of adversaries, degree of adversarial behavior) that increase sensitivity.

## Robustness Setting
- **Threat model / uncertainty set**: Agent changes modeled as a team of antagonist agents Dant whose rewards are the negation of the protagonist reward (rt,i = rt,pro = −rt,j), forming a zero-sum game between productive (protagonist) and adversarial (antagonist) teams. The antagonist-ratio Rant = |Dant|/|D| is sampled uniformly from [0,1) at each training phase so that arbitrary fractions of changing agents are covered. At test time, novel cooperative agents or novel antagonist (failure/attack) agents from a different training process are integrated.
- **Setting**: Cooperative MAS trained via mixed (cooperative-competitive) games; CTDE (centralized training, decentralized execution); online learning. Formulated as a partially observable Markov game.

## Method
- **Randomized Adversarial Training (RAT)**: Maintain a protagonist pool f̂pro and an antagonist pool f̂ant (2N agent representations). At each phase, sample Rant ∼ U; randomly assign ⌈RantN⌉ agents as antagonists and the rest as protagonists, run Ne episodes of mixed games, then update either the protagonist or antagonist pool in alternating epochs (à la Pinto et al. 2017) while the other pool is fixed.
- **RADAR (the main contribution)**: A CTDE scheme that approximates protagonist and antagonist policies with variable Rant using two separate VDN instances. Protagonist Q is factorized as Σ_{i∈Dy,pro} Q̂i,pro = E[(|Dy,pro|/N)·Gt,pro], normalizing the protagonist return by the number of participating protagonists; antagonist Q is the negation, Q̂ant = −Q̂pro.
- VDN is chosen because the linear sum is unbounded in the number of agents (handles variable team sizes), allows straightforward normalization w.r.t. Rant, and adds no extra learnable parameters or hyperparameters; non-linear factorization (QMIX/QTRAN) is left to future work.
- Local policies are derived from Q̂i,pro / Q̂i,ant via multi-armed bandits on values or via policy gradient (Eq. 1).
- **Agent test scheme**: A test suite T with disjoint subsets — Tideal (only training protagonists), Tcooperation (novel cooperative protagonists, R'ant = 1/2), and Tfailure,χ (novel antagonists at different R'ant = χ) — using normalized performance values to fairly compare MARL approaches against the same test agents, and reporting cooperation performance and worst-case performance.

## Theoretical Contributions
- None / mostly empirical. The paper provides complexity analysis (expected complexity O(N) since E[Rant] = 0.5, worst case O(2N)) rather than convergence or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: Two cooperative gridworld domains — Predator-Prey PP[K,N] (K×K grid, N learning predators, N/2 randomly moving prey) and a Cyber-Physical Production System CPPS[N] (machine grid with task-completion). Instances include PP[7,4], PP[10,8], CPPS[4], and CPPS[16]; episodes reset after 50 steps.
- **Baselines**: State-of-the-art MARL — IAC, COMA, AC-QMIX (QMIX critic), and M3DDPG; plus ablations RADAR(χ) with fixed Rant ∈ {0, 1/2, (N−1)/N} and a RAT instantiation with Ψ = IAC.
- **Evaluation metrics**: Normalized per-domain performance gc (normalized number of protagonist main captures for PP; protagonist completion rate for CPPS), reported as cooperation performance (expectation over Tcooperation) and worst-case performance (minimum over Tcooperation ∪ ∪χ Tfailure,χ), with 95% confidence intervals over 20 training runs of 40,000 episodes.

## Key Results
- RADAR achieves the best worst-case performance in all settings except PP[7,4] (where COMA, AC-QMIX, and IAC are competitive); M3DDPG performs worst in all settings.
- RADAR is competitive with cooperative state-of-the-art MARL (COMA, AC-QMIX, IAC) in cooperation performance, performing best in CPPS[16] and only slightly behind elsewhere, indicating only a small cooperative-performance sacrifice for large worst-case gains.
- Ablations show value decomposition matters: RADAR and most fixed-ratio variants clearly outperform RAT (Ψ = IAC), which lacks credit assignment; fixed antagonist-ratio variants are setting-dependent and need tuning, whereas RADAR (variable Rant) needs none and ranks at least second-best across CPPS instances.
- RADAR becomes more resilient as the MAS grows (better worst-case in PP[10,8] and CPPS[16] than PP[7,4] and CPPS[4]), whereas cooperative MARL gets worse with more agents; extreme single-protagonist focus (RADAR((N−1)/N) and M3DDPG) yields sparse training signal and poor policies.

## Limitations & Future Work
- RADAR uses only linear (VDN) value decomposition; extending to non-linear factorization (e.g., QMIX) is left to future work and could yield more powerful resilient MARL.
- Rant is sampled uniformly; the authors plan adaptive sampling mechanisms for Rant to further improve performance and resilience.
- Evaluation is limited to two custom gridworld domains; the authors aim to provide adequate agent test sets for other established domains for consistent, fair evaluation.

## Relevance to Survey
This paper sits on the "agent failure / fault tolerance" and "adversarial agents" lines of robust MARL, framing resilience to arbitrary agent changes as a protagonist-vs-antagonist zero-sum sub-game embedded in cooperative MARL. It connects the adversarial-training paradigm (Pinto et al. 2017; minimax/Littman 1994) and CTDE value decomposition (VDN, QMIX, COMA) to robustness, and is a direct successor/competitor to M3DDPG (Li et al. 2019) and ARTS (Phan et al. 2020), generalizing them by allowing a variable, randomized number of adversaries. Its fair "agent test scheme" for worst-case evaluation is also relevant to robustness evaluation methodology.

## Related Work (verbatim excerpts from the paper)

> _[Section: Related Work — "Adversarial Reinforcement Learning"]_

"Adversarial learning is a popular paradigm to train two opponents alternately to improve each other's performance and robustness (Goodfellow et al. 2014; Pinto et al. 2017). Self-play RL is the simplest form of adversarial RL, where a single agent is trained to play against itself to ensure an adequate difficulty level and steady convergence to robust policies (Samuel 1959; Tesauro 1995; Silver et al. 2016). In (single-agent) RL, the environment can be modeled as adversary by adding disturbances to confront the original agent with worst case scenarios (Morimoto and Doya 2001; Rajeswaran et al. 2017; Pinto et al. 2017). These adversarial disturbances can be realized, e.g., with RL or coevolutionary approaches (Gabor et al. 2019; Wang et al. 2019)."

"Our work is mainly based on adversarial learning. In contrast to single-agent RL, where external changes can only occur within the environment, we focus on agent changes in cooperative MAS. For that, we integrate adversary agents into the training process in order to improve resilience."

> _[Section: Related Work — "Multi-Agent Reinforcement Learning"]_

"MARL is a long-standing AI research area with various approaches (Tan 1993; Panait and Luke 2005; Foerster et al. 2018; Son et al. 2019). While cooperative MARL has achieved impressive results in challenging domains, most approaches have been only evaluated with the same or similar agents as encountered during training. Thus, it remains unclear if these approaches offer resilience against arbitrary agent changes, which are expectable in the real world."

"There is some prior work towards resilient MARL: Minimax-Q was proposed in (Littman 1994) as an adaptation of Q-Learning for zero-sum games. While guaranteeing convergence to safe policies w.r.t. worst case opponents, Minimax-Q becomes intractable if the (joint) action space of the opponent j is large. (Li et al. 2019) proposes M3DDPG, which considers extreme cases, where each agent i considers itself the sole productive agent, while all other agents are modeled as adversaries who attempt to minimize Qπ_i. M3DDPG can lead to poor policies, if the problem is too difficult or even unsolvable for single productive agents, leading to insufficient training signal. (Phan et al. 2020) proposes ARTS, where productive and adversary agents are trained simultaneously according to a fixed adversary ratio, since most CDTE approaches need a predefined input dimension to approximate Q̂ ≈ Qπ. ARTS can improve resilience against agent failures with adequately chosen adversary ratios. However, an ideal ratio needs to be known a priori, which is an unrealistic assumption. Furthermore, a fixed ratio can lead to sensitive policies when N is sufficiently large."

"We propose an adversarial value decomposition scheme, where the number of productive and adversary agents can change dynamically during training. Furthermore, we propose an agent test scheme to evaluate performance and resilience of MARL approaches in a fair way."

> _[Background — "Adversarial Reinforcement Learning"]_

"In zero-sum games, there are N = 2 agents with opposing goals. The value functions of agent i and j (and analogously the rewards) are defined by Qπ_i = −Qπ_j. A minimax equilibrium policy of agent i is defined by π∗_i = argmaxπi minπj Q∗_i, which corresponds to a best response to the worst case, represented by π∗_j (Littman 1994). Adversarial RL approaches attempt to approximate π∗_i with alternating optimization or reformulation of the minimax objective by applying standard RL techniques to each agent (Littman 1994; Pinto et al. 2017; Li et al. 2019)."

### Cited references (resolved from the paper's bibliography)
- **(Goodfellow et al. 2014)** Goodfellow, Pouget-Abadie, Mirza, Xu, Warde-Farley, Ozair, Courville, Bengio. *Generative Adversarial Nets.* NeurIPS 2014.
- **(Pinto et al. 2017)** Pinto, Davidson, Sukthankar, Gupta. *Robust Adversarial Reinforcement Learning.* ICML 2017.
- **(Samuel 1959)** Samuel. *Some Studies in Machine Learning using the Game of Checkers.* IBM Journal of Research and Development 1959.
- **(Tesauro 1995)** Tesauro. *Temporal Difference Learning and TD-Gammon.* Communications of the ACM 1995.
- **(Silver et al. 2016)** Silver, Huang, Maddison, Guez, Sifre, Van Den Driessche, et al. *Mastering the Game of Go with Deep Neural Networks and Tree Search.* Nature 2016.
- **(Morimoto and Doya 2001)** Morimoto, Doya. *Robust Reinforcement Learning.* NeurIPS 2001.
- **(Rajeswaran et al. 2017)** Rajeswaran, Ghotra, Ravindran, Levine. *EPOpt: Learning Robust Neural Network Policies using Model Ensembles.* ICLR 2017.
- **(Gabor et al. 2019)** Gabor, Sedlmeier, Kiermeier, Phan, et al. *Scenario Co-evolution for Reinforcement Learning on a Grid World Smart Factory Domain.* GECCO 2019.
- **(Wang et al. 2019)** Wang, Lehman, Clune, Stanley. *POET: Open-Ended Coevolution of Environments and their Optimized Solutions.* GECCO 2019.
- **(Tan 1993)** Tan. *Multi-Agent Reinforcement Learning: Independent versus Cooperative Agents.* ICML 1993.
- **(Panait and Luke 2005)** Panait, Luke. *Cooperative Multi-Agent Learning: The State of the Art.* Autonomous Agents and Multiagent Systems 2005.
- **(Foerster et al. 2018)** Foerster, Farquhar, Afouras, Nardelli, Whiteson. *Counterfactual Multi-Agent Policy Gradients.* AAAI 2018.
- **(Son et al. 2019)** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to Factorize with Transformation for Cooperative Multi-Agent Reinforcement Learning.* ICML 2019.
- **(Littman 1994)** Littman. *Markov Games as a Framework for Multi-Agent Reinforcement Learning.* Machine Learning Proceedings 1994 (Elsevier).
- **(Li et al. 2019)** Li, Wu, Cui, Dong, Fang, Russell. *Robust Multi-Agent Reinforcement Learning via Minimax Deep Deterministic Policy Gradient (M3DDPG).* AAAI 2019.
- **(Phan et al. 2020)** Phan, Gabor, Sedlmeier, Ritz, Kempter, Klein, Sauer, Schmid, Wieghardt, Zeller, et al. *Learning and Testing Resilience in Cooperative Multi-Agent Systems (ARTS).* AAMAS 2020.
