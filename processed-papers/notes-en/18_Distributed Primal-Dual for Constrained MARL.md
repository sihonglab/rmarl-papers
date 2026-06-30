# 18. A Distributed Primal-Dual Method for Constrained Multi-agent Reinforcement Learning with General Parameterization

## Metadata
- **Title**: A Distributed Primal-Dual Method for Constrained Multi-agent Reinforcement Learning with General Parameterization
- **Authors**: Ali Kahe, Hamed Kebriaei
- **Affiliation**: School of ECE, College of Engineering, University of Tehran, Tehran, Iran; H. Kebriaei is also with the School of Computer Science, Institute for Research in Fundamental Sciences (IPM), Tehran, Iran
- **Venue**: Not specified (arXiv:2410.15335v2 [eess.SY], 7 May 2026)
- **Link/arXiv**: arXiv:2410.15335v2

## Taxonomy
- **Robustness / perturbation type targeted**: Safety constraints (cooperative Constrained MARL within the Constrained Markov Game framework — global constraint satisfaction as a counterpart to safety/feasibility); stochastic environment dynamics. Not adversarial/model-uncertainty robustness in the worst-case sense.
- **Method paradigm**: Distributed primal-dual (Lagrangian) optimization, actor-critic with linear/general function approximation, two/three-timescale stochastic approximation, consensus over networked agents
- **Keywords**: Constrained Multi-Agent Reinforcement Learning, Primal-Dual Algorithm, Actor-Critic Algorithm, Lagrange multiplier consensus, Constrained Markov Game

## TL;DR
The paper proposes a fully decentralized online primal-dual actor-critic algorithm for cooperative Constrained MARL in which each networked agent maintains local estimates of both primal (policy/critic) and dual (Lagrange multiplier) variables, proving consensus of the local Lagrange multipliers and convergence to an equilibrium point, and bounding its sub-optimality / duality gap relative to the unparameterized problem.

## Problem & Motivation
Many practical MARL applications (traffic control, smart grids, networked microgrids, EV rebalancing) require constraints to ensure safety, fairness, or efficiency, leading to Constrained MARL (CMARL), framed within the Constrained Markov Game (CMG) framework. The paper targets the cooperative CMARL problem where all agents minimize a global objective cost subject to global constraints that are composed of coupled local costs. Centralized training/coordination faces scalability and communication challenges, and agent independence during online operation is needed for practical deployment. Unlike single-agent constrained RL, which enjoys a zero duality gap, the cooperative CMARL problem can have a non-zero duality gap, posing challenges for satisfying global constraints. The shared Lagrange multipliers couple the otherwise decomposable Lagrangian, preventing fully distributed solutions; resolving this coupling via locally estimated multipliers is the key gap the paper addresses (claimed not addressed previously).

## Robustness Setting
- **Threat model / uncertainty set**: No adversary / uncertainty set. Constraints are modeled as global expected constraint-cost functions Gk(πθ) ≤ bk built from averaged local constraint costs, imposing implicit restrictions on the feasible product parameter space ΘC. Exogenous randomness (stochastic transitions and stochastic objective/constraint costs) is present; costs are bounded i.i.d. given state-action pairs.
- **Setting**: cooperative; fully decentralized / distributed online learning over networked agents (no centralized training or execution coordination; agents share only local critic and multiplier parameters with neighbors over a communication graph); online.

## Method
- Formulates the cooperative CMARL problem within the CMG framework as a minimax problem infθ supλ L(πθ, λ) with a global Lagrangian that decomposes into a sum of local Lagrangian functions Ln(πθ, λ); solves the dual (better suited to distributed constrained optimization).
- Because shared multipliers couple agents, introduces locally estimated Lagrange multipliers {λ̂n,k}; defines an estimated Lagrangian objective L̂(πθ, λ̂) that coincides with the true global Lagrangian under the consensus condition λ̂n,k = λk.
- Proposes a distributed primal-dual actor-critic algorithm (Algorithm 1) with two phases per step: (I) sampling and immediate local Lagrangian cost update; (II) learning and consensus — each agent updates its critic via TD learning (linear Q(s,a;w)=w⊤φ(s,a)), its actor via projected policy-gradient using a local advantage, its local constraint estimate Ĝn, and its dual variable λ̂n by an ascent step on (Ĝn − b), exchanging critic and multiplier parameters with neighbors through a doubly-stochastic weight matrix Ξt.
- Uses three-timescale step sizes (αt for critic, βt for actor, γt for multipliers, with βt/αt → 0 and γt/βt → 0) so the multiplier is quasi-static relative to the actor, which is in turn slower than the critic.

## Theoretical Contributions
- Theorem 1: consensus of the locally estimated Lagrange multipliers — the disagreement component λ̂t⊥ → 0 almost surely.
- Proposition 1: convergence of the distributed actor-critic (for fixed λ̂) to an asymptotically stable equilibrium of the projected dynamical system (almost surely), via a two-timescale argument building on the networked MARL results of [9].
- Theorem 2: the consensus vector of the multipliers ⟨λt⟩ converges almost surely to a point λ̄ with 1⊗λ̄ in the set of asymptotically stable equilibria of the multiplier dynamics.
- Proposition 2: feasibility — if λ̄ ∈ Int(Λ), all constraints are satisfied.
- Proposition 3 (with supporting Lemmas 3–7): an upper bound on the parameterized duality gap ∆̄param in terms of the maximal multipliers, individual/product parameterization errors ϵn, stationary-distribution discrepancy, and the unparameterized duality gap ∆̄.

## Experiments
- **Environment/Benchmark**: A custom cooperative, stochastic Cournot game with time-varying demand (discretized: 10 states from [0.1,0.9], 10 actions per agent from [0,1], 10×10^5 state-action pairs; binomial state transitions). Agent-specific price-bound constraints with weights m1..m5 and global bound b = 0.75. Linear critics (20-dim) and softmax policies with linear parameterization (10-dim). Learning rates αt = t^-0.6, βt = t^-0.75, γt = t^-0.9.
- **Baselines**: Not specified (no comparison baselines; evaluation is on the proposed algorithm's own convergence behavior).
- **Evaluation metrics**: Convergence/consensus of locally estimated Lagrange multipliers; global objective cost J and global constraint cost violation (Ĝ − b) during training.

## Key Results
- Figure 1: the locally estimated Lagrange multipliers reach consensus and then converge, empirically confirming Theorems 1 and 2.
- Figure 2: the algorithm reduces the global objective cost J while keeping constraint violations (Ĝ − b) near zero during training.

## Limitations & Future Work
- Linear function approximation of the Q-function may introduce error relative to the true policy gradient; convergence is to an ϵ-neighborhood of a local minimum (Remark 2) and relies on assumptions (Slater's condition, doubly-stochastic communication, sufficiently large Θ, unique fixed-point map).
- Evaluation is limited to a single synthetic stochastic Cournot game with no comparison baselines.
- Cooperative CMARL has a non-zero duality gap; the method solves the dual and only bounds sub-optimality rather than recovering the exact primal solution.
- Future work: adaptations for more complex environments and dynamic constraints.

## Relevance to Survey
This paper sits on the "safety / constraint satisfaction" line of robust MARL rather than the worst-case adversarial / model-uncertainty line. It contributes a fully decentralized primal-dual mechanism (local Lagrange-multiplier estimation with consensus) for constrained cooperative MARL, connecting to the broader theme that constrained/safe MARL is a component of trustworthy, robust multi-agent deployment. It is most relevant to surveys' coverage of constrained Markov games, safe MARL, and distributed/networked actor-critic methods; one of its motivating references is an explicitly "robust and constrained" multi-agent RL method for EV rebalancing ([12]).

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction — "Related Works:" subsection]_

"A widely used approach for solving single-agent constrained reinforcement learning problems is the primal-dual method, which demonstrates a zero duality gap by converting the original problem into an unconstrained Markov decision process with a Lagrangian cost [14], [16]. This relaxed MDP is solved through alternating updates of the primal and dual variables. This approach has been extended to cooperative CMARL by relaxing the constrained problem into an unconstrained cooperative MARL [17], [15], [18]. Such relaxation enables the use of existing MARL algorithms, such as distributed actor-critic methods for networked agents [9]."

"Although there are many works on CMARL, only a few address the general problem where agent's local costs are coupled through global constraint functions. For instance, in the CMARL formulation of [19], each agent's actions indirectly influence others through state transition dynamics, but the method requires some coordination, preventing full decentralization. In contrast, [18] achieves decentralization through parameter sharing among agents, though it solves a distributed constrained MDP with networked agents rather than a true CMARL problem. This approach assumes homogeneous agents, with policies converging to a consensus. A recent extension by [20] builds on this by reducing gradient estimation variance for improved scalability."

"For general CMARL formulation, [21] adopts the centralized training, decentralized execution framework, improving computational efficiency and scalability in large-scale multi-agent environments. It separates an agent's policy into two components: a base policy for reward maximization and a perturbation policy for constraint satisfaction. However, it requires communication between agents during execution, distinguishing it from fully distributed methods."

"Another notable work is [22], which operates in distributed settings. They propose a scalable method for general utility and constraint functions, modeled as nonlinear functions of the state-action occupancy measure. Their approach decomposes the state space for each agent, directly estimating local state-action occupancy measures while leveraging spatial correlation decay and truncated policy gradient estimators for scalability and convergence. However, despite its general policy parameterization, directly estimating local occupancy measures remains challenging in large state-action spaces."

> _[Section I, Introduction — motivation paragraphs on CMARL and constraints]_

"While MARL holds great promise, many practical applications impose constraints that must be respected to ensure safety, fairness, or efficiency. For example, in networked microgrid management, maintaining power balance and preventing system overloads are critical for system stability [11]; similarly, in electric vehicle rebalancing systems, agents must consider factors such as battery life and access to charging stations [12]. Incorporating these types of constraints into reinforcement learning leads to the development of CMARL, which extends MARL frameworks to handle complex environments where satisfying constraints is as crucial as maximizing objective costs. CMARL is framed within the Constrained Markov Game (CMG) framework [13], where each agent has its own local constraints and objective costs."

"Although recent advancements in constrained single-agent reinforcement learning have demonstrated a zero duality gap [14], the duality gap for the cooperative CMARL problem can be non-zero [15]. This inherent complexity poses significant challenges for algorithms attempting to satisfy global constraints [15]. In our study, we provide an analysis on the feasibility and sub-optimality of the equilibrium point of the proposed online algorithm."

### Cited references (resolved from the paper's bibliography)
- **[9]** Zhang, Yang, Liu, Zhang, Başar. *Fully decentralized multi-agent reinforcement learning with networked agents.* ICML 2018.
- **[11]** Zhang, Dehghanpour, Wang, Qiu, Zhao. *Multi-agent safe policy learning for power management of networked microgrids.* IEEE Transactions on Smart Grid, 2021.
- **[12]** He, Wang, Han, Zou, Miao. *A robust and constrained multi-agent reinforcement learning electric vehicle rebalancing method in AMoD systems.* IEEE/RSJ IROS 2023.
- **[13]** Altman, Shwartz. *Constrained Markov games: Nash equilibria.* Advances in Dynamic Games and Applications, Springer 2000.
- **[14]** Paternain, Chamon, Calvo-Fullana, Ribeiro. *Constrained reinforcement learning has zero duality gap.* NeurIPS 2019.
- **[15]** Chen, Zhou, Huang. *On the hardness of constrained cooperative multi-agent reinforcement learning.* ICLR 2024.
- **[16]** Bhatnagar, Lakshmanan. *An online actor-critic algorithm with function approximation for constrained Markov decision processes.* Journal of Optimization Theory and Applications, 2012.
- **[17]** Diddigi, Reddy, KJ, Bhatnagar. *Actor-critic algorithms for constrained multi-agent reinforcement learning.* AAMAS 2019.
- **[18]** Lu, Zhang, Chen, Başar, Horesh. *Decentralized policy gradient descent ascent for safe multi-agent reinforcement learning.* AAAI 2021.
- **[19]** Zhao, Yang, Lu, Zhou, Li. *Multi-agent first order constrained optimization in policy space.* NeurIPS 2023.
- **[20]** Hassan, Wadith, Rashid, Khan. *DePAInT: A decentralized safe multi-agent reinforcement learning algorithm considering peak and average constraints.* Applied Intelligence, 2024.
- **[21]** Yang, Jin, Ding, You, Fan, Wang, Zhou. *DeCOM: Decomposed policy for constrained cooperative multi-agent reinforcement learning.* AAAI 2023.
- **[22]** Ying, Zhang, Ding, Koppel, Lavaei. *Scalable primal-dual actor-critic method for safe multi-agent reinforcement learning with general utilities.* NeurIPS 2024.
