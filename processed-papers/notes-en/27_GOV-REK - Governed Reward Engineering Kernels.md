# 27. GOV-REK: Governed Reward Engineering Kernels for Designing Robust Multi-Agent Reinforcement Learning Systems

## Metadata
- **Title**: GOV-REK: Governed Reward Engineering Kernels for Designing Robust Multi-Agent Reinforcement Learning Systems
- **Authors**: Ashish Rana, Michael Oesterle, Jannik Brinkmann
- **Affiliation**: Institute for Enterprise Systems, University of Mannheim, Germany
- **Venue**: AAMAS 2024 (Extended Abstract, 23rd International Conference on Autonomous Agents and Multi-Agent Systems)
- **Link/arXiv**: arXiv:2404.01131v2 [cs.MA] 14 Apr 2024

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to environment perturbations (randomized environment configurations, solution-trajectory blocker objects), changing system dynamics, and sparse-reward scenarios; fault tolerance with respect to reward-shaping pitfalls (positive reward cycle traps)
- **Method paradigm**: Reward shaping / potential-based reward shaping (PBRS), problem-agnostic reward distributions ("governance kernels"), Hyperband-like / Successive-Halving hyperparameter search over reward models, governance layer over a stochastic game
- **Keywords**: Cooperative Multi-Agent Systems, Sparse Reinforcement Learning, Robust Multi-Agent Systems, Reward Shaping, Governance Kernels, PBRS

## TL;DR
The paper proposes GOV-REK, a governance layer that dynamically assigns problem-agnostic reward distributions ("governance kernels") to MARL agents and iteratively searches over kernel configurations with a Hyperband-like algorithm, so that meaningful reward priors robustly jumpstart learning across different (especially sparse-reward) MARL problems without problem-specific reward engineering.

## Problem & Motivation
MARL problem formulation typically requires massive, problem-specific reward engineering effort that does not transfer across problems and is wasted when system dynamics change drastically. This is worsened in sparse-reward settings where solution trajectories explode exponentially at scale and reward signals are too sparse to guide learning. Prior reward-design approaches (domain knowledge, imitation learning, ethics-based shaping) are problem-specific and do not generalize. The goal is to define effective and robust reward signals for MARL agents in an automated, problem-agnostic manner.

## Robustness Setting
- **Threat model / uncertainty set**: Robustness is evaluated against randomized perturbations in environment configurations and against solution-trajectory blocker objects, plus changing/evolving system dynamics and increasing scale/complexity. No explicit adversary or formal uncertainty set; robustness is empirical jumpstart/stability of learning. Reward modifications are constrained to satisfy PBRS (policy invariance) using only normalized reward distributions, mitigating positive-reward-cycle traps (fault tolerance).
- **Setting**: Cooperative; Centralized Training Centralized Execution (CTCE) in fully observable settings and Centralized Training Decentralized Execution (CTDE) in partially observable settings; online learning over a stochastic game (SG) / POSG formulation.

## Method
- Inserts an intermediary "governance" layer between agents and the environment that adds agent-specific or agent-agnostic reward signals (R' = R + G), without changing the available states or actions; only the policy that selects them may change.
- Defines "governance kernels": simplified, non-parametric reward models (resembling Gaussian-process kernels: linear, periodic, squared-exponential; 3D surface kernels: diagonal, ellipsoid, hyperboloid) defined purely on geometric similarity in state space (stage games) or joint-action space (static games), under the exploration-expectation assumption E_a[R(s,a,s')] → R'(s,s').
- Enforces PBRS consistency by normalizing all reward values per state/joint-action element, so additional rewards introduce only soft (not strict) exploration constraints; introduces decaying governance kernels to encourage exploration of more global/diverse trajectories at larger scales.
- Searches for ideal agent reward models with a repeated Hyperband-like procedure (Algorithm 1): runs Successive-Halving brackets over multiple rounds with budget multiplier η=3, pruning worst kernel configurations, while genetically mutating (m=0.5) and superimposing (s=0.5) the best kernels across rounds; renormalizes merged kernels to keep PBRS valid.
- Kernel selection can be single-objective (maximize reward) or multi-objective (maximize reward and minimize episode length).

## Theoretical Contributions
None / mostly empirical. The paper invokes the PBRS policy-invariance result (necessary-and-sufficient potential-function constraint) and its temporal/multi-agent extensions to justify constraining kernels, but contributes no new convergence, sample-complexity, or equilibrium theorems; contributions are an inductive-bias formulation and an empirical framework.

## Experiments
- **Environment/Benchmark**: 2D-grid road and 3D-grid drone package-delivery environments (cooperative, sparse goal reward), in CTCE fully observable settings; an N-player social dilemma problem in a partially observable CTDE setting (governance kernels defined over joint-action space). Grid sizes include 5x5 and 10x10 (2D), 3x3 and 5x5 (3D); social dilemma uses a 16-agent, 16-episode-length setting.
- **Baselines**: Proximal Policy Optimization (PPO) from Stable Baselines3 (CTCE) and RLlib (CTDE) with default hyperparameters; Multi-Objective Reward Shaping (MORS), which assigns manually designed dense subtask rewards via domain knowledge; also qualitative comparison of A2C vs PPO under governance.
- **Evaluation metrics**: Average accumulated reward returns and average episode length (with 95% confidence intervals over five random seeds); robustness against blocker objects and randomized perturbations; scalability under different reward decays; cooperation rate and contribution symmetry.

## Key Results
- Governed MARLS trained for 120K timesteps are generally robust to an increasing number of blocker objects and to randomized environment perturbations, though average episode length grows as more blockers/randomization are added.
- GOV-REK converges relatively faster than MORS (especially under randomized initial configurations) and yields shorter episode lengths; MORS accumulates more post-convergence reward but with larger episode lengths, indicating it is more prone to positive-reward cycles, whereas GOV-REK's PBRS compliance makes it more fault tolerant.
- For scalability, higher decay rates with decaying governance kernels give faster convergence on larger 10x10 2D-grid (and improved 3D-grid) environments; best kernel combinations were agent-specific squared-exponential + agent-agnostic linear (5x5 2D road), agent-agnostic hyperboloid + diagonal (3x3 3D drone), and linear + periodic (social dilemma).
- In the social dilemma, governed agents accumulate more average reward (especially with zero-mean kernels), with larger gains in heterogeneous and sparse settings, demonstrating efficacy in non-spatial (S = φ) environments.

## Limitations & Future Work
- At larger scales the baseline PPO agents fail to consistently satisfy the exploration-expectation assumption E_a[R(s,a,s')] → R'(s,s'); cooperation inconsistencies and sub-optimality appear at larger and highly randomized configurations, with longer episodes and lower reward.
- The simplistic surface governance kernels improve interpretability but can hamper agent performance; selected kernels are not optimized for per-episode random reconfigurations.
- Future work: experiment with other algorithms (RND, NGU, Agent57) to better hold the exploration-expectation assumption; explore a paradigm trading between the rigid/simplistic reward-exploration method and a fully fluid, complex state-similarity learning method (as in NGU and ATA).

## Relevance to Survey
This work sits on the "robustness via reward design / reward shaping" line of robust MARL rather than the adversarial/worst-case or distributionally robust lines. It contributes a problem-agnostic, automated reward-engineering mechanism (a governance layer producing PBRS-consistent reward priors) that empirically delivers robust learning jumpstart, robustness to environment perturbations, scalability, and fault tolerance against reward-shaping pitfalls in sparse cooperative MARL. It connects robust MARL to governance / normative multi-agent systems, reward shaping, and HPO-style automated configuration search, offering a complementary, non-adversarial notion of "robustness" for the survey's taxonomy.

## Related Work (verbatim excerpts from the paper)
> _[Section: Related Work]_

"Defining a good MARL goal is a challenging objective, where expected agent rewards need to be jointly maximized in a completely observable or partially observable setting. The defined rewards for a given goal must stabilize the agent's learning behavior while adapting to changing dynamics in the environment. The stability convergence requirement ensures the stationary policy convergence, and the adaptability constraint ensures no performance detriment with evolving policies of other agents, provided agents are rational [10, 15]. Further, for training MARLS, the Centralized Training Centralized Execution (CTCE) paradigm optimizes the joint policy for agents together, and the Centralized Training Decentralized Execution (CTDE) paradigm agents maintain separate policies but exchange information during training [50, 27, 21]. In this study, we train our MARLS with CTCE in a fully observable setting and CTDE in a partially observable setting against two different MARL problems to quantify the scalability and adaptability performance aspects. Previously, architectures utilizing additional novelties like imitation-based learning [42, 11], curiosity-driven learning [5, 40], curriculum learning [3], self- or temporal-attention [30, 31], and evolutionary learning [36] have shown efficacy for a wide range of RL problems. With our proposed GOV-REK framework, we focus on improving the performance of existing baseline algorithms with an additional coordinating governance layer that primarily alters agent incentives to achieve convergence."

> _[Section: Related Work]_

"For defining meaningful agent motivation, reward-shaping has been widely studied in the past, where this approach has proven its efficacy for achieving faster convergence [24, 45]. Also, incorporating other novel mechanisms, like learning ethical human behavior demonstrations [46], multi-objective reward shaping (MORS) [13], additional rewards for sub-goal completion [28], and context-sensitive rewards for agents [11], have shown further improvements. However, reward-shaping agents are often susceptible to falling under continuous positive reward cycle traps, especially for sparse environments where additional rewards can dominate the accurate underlying reward model. Formally, the reward function for the underlying Markov Decision Process (MDP) can be modified with the relation R′ = R + F, where F(s, s, s′) is the additional transition reward model, and ft is defined analogously to rt in a temporal setting. The Potential Based Reward Shaping (PBRS) maintains a potential function Φ : S →R is a necessary and sufficient constraint designed for policy invariance which applies to MARLS as well [20, 19]. This relation can further be modified to incorporate the temporal element given by F(s, t, s′, t′) = γΦ(s′, t′) −Φ(s, t), where γ denotes the discount factor. Furthermore, our GOV-REK approach restricts all our agent solution trajectories to always satisfy PBRS constraints by using only normalized reward distributions as additional reward signals."

> _[Section: Related Work]_

"The task of finding optimal strategies or policies in MARL systems is still an open challenge [49]. To mitigate this problem, researchers have proposed a paradigm where agents are provided with assistive information for learning. Approaches, like Environment-Mediated Multi-Agent Systems (EMMAS) [44], Electronic Institutions (EI) [25], and Normative Multi-Agent Systems (NorMAS) [17, 37] generally employ a restrictive strategy to limit original solution policy space for empirically achieving faster convergence. Further, the Autonomic Electronic Institutions (AEI) approach dynamically evolves these constraints to achieve even faster convergence [9]. As shown in Figure 3, the Governed Multi-Agent System (GMAS) approach queries every execution step to obtain permissible actions, and the learning happens between those steps [39]. Also, in each learning step, the governance optimizes its learning policy for maximizing the system objective while evolving the action-space constraints. The black-box ANN agents also update their policies at each learning step, where the agents are not part of the governance. All the above-discussed approaches strictly constrain the agent action spaces, which might be suboptimal when a massive exploration of the joint state-action space is needed, like in sparse reward problems. However, with our proposed approach, the additional reward signals introduce only soft constraints on agent exploration behavior, which prohibits strictly restricting the exploration capacity of agents. Second, our reward models are evolved in a more stable manner, where only better reward models are selected after each round of significant model training as highlighted in Figure 3."

> _[Introduction]_

"Previously, architectural novelties introduced in Agent Temporal Attention (ATA) [47], Random Network Distillation (RND) [14], Never Give Up (NGU) [2], and Shared Experience Actor-Critic (SEAC) [16] methods have successfully improved the learning behavior in reinforcement learning (RL) systems against sparse problems. However, these approaches improve sample efficiency by introducing novelties like attention, curiosity, and experience sharing as part of the learning process rather than directly influencing agent motivations. Our approach proposes an intermediary governance layer between agents and the environment, which directly incentivizes agents with additional rewards selected in an automated manner to improve the baseline RL algorithms."

### Cited references (resolved from the paper's bibliography)
- **[2]** Badia, Sprechmann, Vitvitskyi, Guo, Piot, Kapturowski, et al. *Never give up: Learning directed exploration strategies.* arXiv 2020.
- **[3]** Baker, Kanitscheider, Markov, Wu, Powell, McGrew, Mordatch. *Emergent tool use from multi-agent autocurricula.* arXiv 2019.
- **[5]** Bellemare, Srinivasan, Ostrovski, Schaul, Saxton, Munos. *Unifying count-based exploration and intrinsic motivation.* NeurIPS 2016.
- **[9]** Bou, López-Sánchez, Rodríguez-Aguilar. *Towards self-configuration in autonomic electronic institutions.* Workshop on Coordination, Organizations, Institutions, and Norms in Agent Systems (Springer) 2006.
- **[10]** Bowling, Veloso. *Rational and convergent learning in stochastic games.* IJCAI 2001.
- **[11]** Brys, Harutyunyan, Suay, Chernova, Taylor, Nowé. *Reinforcement learning from demonstration through shaping.* IJCAI 2015.
- **[13]** Brys, Harutyunyan, Vrancx, Taylor, Kudenko, Nowé. *Multi-objectivization of reinforcement learning problems by reward shaping.* IJCNN 2014.
- **[14]** Burda, Edwards, Storkey, Klimov. *Exploration by random network distillation.* arXiv 2018.
- **[15]** Chalkiadakis. *Multiagent reinforcement learning: Stochastic games with multiple learning players.* Univ. of Toronto Tech. Rep. 2003.
- **[16]** Christianos, Schäfer, Albrecht. *Shared experience actor-critic for multi-agent reinforcement learning.* NeurIPS 2020.
- **[17]** Conte, Falcone, Sartor. *Agents and norms: How to fill the gap?* AI & Law 1999.
- **[19]** Devlin, Kudenko. *Theoretical considerations of potential-based reward shaping for multi-agent systems.* AAMAS 2011.
- **[20]** Devlin, Kudenko. *Dynamic potential-based reward shaping.* AAMAS 2012.
- **[21]** Du, Ding. *A survey on multi-agent deep reinforcement learning: from the perspective of challenges and applications.* Artificial Intelligence Review 2021.
- **[24]** Eschmann. *Reward function design in reinforcement learning.* Reinforcement Learning Algorithms: Analysis and Applications 2021.
- **[25]** Esteva, Rodriguez-Aguilar, Sierra, Garcia, Arcos. *On the formal specification of electronic institutions.* Agent Mediated Electronic Commerce (Springer) 2001.
- **[27]** Gronauer, Diepold. *Multi-agent deep reinforcement learning: a survey.* Artificial Intelligence Review 2022.
- **[28]** Harutyunyan, Devlin, Vrancx, Nowé. *Expressing arbitrary reward functions as potential-based advice.* AAAI 2015.
- **[30]** Iqbal, Sha. *Actor-attention-critic for multi-agent reinforcement learning.* ICML 2019.
- **[31]** Jiang, Lu. *Learning attentional communication for multi-agent cooperation.* NeurIPS 2018.
- **[36]** Long, Zhou, Gupta, Fang, Wu, Wang. *Evolutionary population curriculum for scaling multi-agent reinforcement learning.* arXiv 2020.
- **[37]** Neufeld. *Reinforcement Learning Guided by Provable Normative Compliance.* ICAART 2022.
- **[39]** Oesterle, Bartelt, Lüdtke, Stuckenschmidt. *Self-learning governance of black-box multi-agent systems.* Workshop on Coordination, Organizations, Institutions, Norms, and Ethics for Governance of Multi-Agent Systems (Springer) 2022.
- **[40]** Ostrovski, Bellemare, Oord, Munos. *Count-based exploration with neural density models.* ICML 2017.
- **[42]** Schaal. *Learning from demonstration.* NeurIPS 1996.
- **[44]** Weyns, Brueckner, Demazeau. *Engineering Environment-Mediated Multi-Agent Systems (EEMMAS 2007).* Springer 2008.
- **[45]** Wirth, Akrour, Neumann, Fürnkranz, et al. *A survey of preference-based reinforcement learning methods.* JMLR 2017.
- **[46]** Wu, Lin. *A low-cost ethics shaping approach for designing reinforcement learning agents.* AAAI 2018.
- **[47]** Xiao, Ramasubramanian, Poovendran. *Agent-Temporal Attention for Reward Redistribution in Episodic Multi-Agent Reinforcement Learning.* arXiv 2022.
- **[49]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control 2021.
- **[50]** Zhao, Queralta, Westerlund. *Sim-to-real transfer in deep reinforcement learning for robotics: a survey.* IEEE SSCI 2020.
