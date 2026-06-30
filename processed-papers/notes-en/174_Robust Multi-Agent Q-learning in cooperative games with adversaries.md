# 174. Robust Multi-agent Q-learning in Cooperative Games with Adversaries

## Metadata
- **Title**: Robust Multi-agent Q-learning in Cooperative Games with Adversaries
- **Authors**: Eleni Nisioti, Daan Bloembergen, Michael Kaisers
- **Affiliation**: Centrum Wiskunde & Informatica, Amsterdam, The Netherlands
- **Venue**: Not specified (Copyright © 2021, AAAI; likely an AAAI-affiliated workshop/conference paper)
- **Link/arXiv**: Code at https://github.com/eleninisioti/robust-marl

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents / action manipulation — a fixed number of adversaries adversarially select both which agents to attack and the actions those agents perform (a "multi-agent adversarial attack"); robustness without simulating attacks during training.
- **Method paradigm**: Minimax decision rules, temporal-difference / Q-learning, robust Bellman operator, linear programming (per-partition minimax), worst-case (zero-sum opponent) modeling, CTDE.
- **Keywords**: RoM-Q, multi-agent adversarial attack, minimax-Q, robust temporal difference learning, load balancing, cooperative MAS

## TL;DR
The paper introduces RoM-Q, a Q-learning-like algorithm that learns policies robust to a novel "multi-agent adversarial attack" in which a team of adversaries, aware of the joint Q-value function, performs a worst-case selection of both the agents to attack and the actions to take, achieving the highest rewards against all considered attacks on a toy load-balancing network.

## Problem & Motivation
In real-world cooperative multi-agent systems (e.g., communication networks, power grids), policies are typically learned offline assuming all agents share a common objective, leaving them vulnerable to misbehavior of even a single agent that can cause cascading failures into undesirable unsafe (e.g., over-flow) regions. Prior MARL robustness work studies performance against different types of agents, but the authors target robustness to attacks where adversaries adversarially choose which (most vulnerable/vital) agents to control and what actions to perform. The key gap addressed is learning such robust policies without requiring the simulation of attacks during training, by having a robust operator "imagine" worst-case attacks based on the agent's own value function (so no model of the adversary is needed).

## Robustness Setting
- **Threat model / uncertainty set**: A fixed number K of adversaries arrives at a random time step with probability δ during evaluation. Adversaries are aware of the (learned, not necessarily optimal) joint Q-value function and perform a worst-case (deterministic) selection of a partition cₖ of agents to control and the actions ⃗aₖ for those agents, choosing the partition/actions that bring the largest decrease in the immediate reward (a short-sighted, one-step attack), while remaining defenders follow their learned policy. Adversaries behave as zero-sum opponents and directly manipulate actions (argued to be at least as effective as observation manipulation).
- **Setting**: Cooperative MAS modeled as a (zero-sum) stochastic game with defenders vs. adversaries; centralized training (joint state-action Q-value function), greedy decentralized execution; online/off-line tabular learning, no attacks during training.

## Method
- Uses temporal-difference learning on a joint state-action Q-value function, defining the target value V^T(⃗s) with two minimizers — one over the adversarial action selection (⃗aⱼ) and one over the choice of adversarial partition (j ∈ Cₖ) — and a maximizer over the policies of the remaining (non-attacked) agents (maxπ₋ⱼ). This generalizes the minimax-Q target to an adversarial choice among multiple agents.
- The type/identity of an attacked agent is not known a priori (unlike minimax-Q); instead the algorithm picks the partition giving the minimum Q-value, making the V^T(⃗s) computation a mixed integer linear program, solved exactly by enumerating all partitions and solving one linear program per partition (number of partitions = (N!)/(K−N)!).
- Algorithm 1 (RoM-Q): at each step take ε-greedy action, observe reward and next state, update Q via standard TD; then for every subset cₖ of K adversaries solve the per-partition minimax LP to obtain π₋cₖ and V₋cₖ, choose the worst-case partition c̄ₖ = arg min V₋cₖ, assign defenders their corresponding policies, and update V(⃗s) with the worst-case value.
- A separate evaluation-time attack (Algorithm 2) computes the optimal deterministic adversarial policy σ*(⃗s) = (c̄ₖ, ⃗a_c̄ₖ): for each partition, adversaries marginalize over defenders' actions (max over ⃗a₋cₖ) and pick actions minimizing expected reward (min over ⃗acₖ) under the learned optimal joint policy; this attack is not part of RoM-Q and can be applied during evaluation against any policy.

## Theoretical Contributions
- None / mostly empirical. The method builds on the convergence properties of minimax-Q (Littman 1994) but no new convergence/sample-complexity theorems are proven; the paper notes the V^T computation is a mixed integer linear program and the per-iteration LP count scales with the number of adversary partitions.

## Experiments
- **Environment/Benchmark**: A stylized load-balancing toy network of two inter-connected nodes (agents), each with capacity, task-arrival probability, and execution/off-loading/over-flow penalties plus a survival reward; described as a multi-agent variant of the classical cliff-walking problem with the cliff region set by node capacities. Hyper-parameters: Strain = 1,000,000 training samples, Seval = 20,000 evaluation samples, I = 40 trials, α = 0.01, ε = 0.1, γ = 0.9, K = 1 adversary.
- **Baselines**: Q-learning and minimax-Q (Littman 1994). Adversarial-policy pool {σ*_Q-learning, σ*_minimax-Q, σ*_RoM-Q} derived via Algorithm 2 from each method's learned policy.
- **Evaluation metrics**: Average system reward per sample (optimal value = 14; optimal episode sum = 700 over episode length 50), state-visit heatmaps / over-flow behavior under attacks, and total reward accrued per episode across different attack probabilities δ and adversarial policies, with 95% confidence intervals over I trials.

## Key Results
- In the absence of attacks none of the three methods over-flows; Q-learning keeps nodes close to capacity (highest no-attack reward), while minimax-Q and RoM-Q learn more conservative policies (executing tasks often to stay away from over-flow) yielding slightly lower no-attack rewards.
- Under attacks, Q-learning's performance drops drastically for δ > 0.1 with larger variance; minimax-Q and RoM-Q are both more robust than Q-learning, but minimax-Q (which keeps nodes idle at state = 1) ultimately over-flows significantly more often than RoM-Q.
- Most importantly, policies learned with RoM-Q achieve the highest reward against all types of attacks in the pool and are thus the most robust, demonstrating the value of accounting for differing agent vulnerabilities when adversaries choose victims adversarially.

## Limitations & Future Work
- The main limitation is computational complexity: each learning iteration solves a number of linear programs that scales with the number of combinations of K adversaries out of N agents (exhaustive enumeration), which was tractable only for the toy network.
- Although policies are learned offline (and can exploit resource-rich simulation), a reduced-complexity variant is desirable.
- Future work: express the mixed integer linear program in a standard form admitting approximate solutions with optimality guarantees (e.g., a multiple knapsack problem), or use (anytime) sampling approximations; experiments are limited to a two-node toy network.

## Relevance to Survey
This paper sits on the "adversarial agents / action-perturbation" line of robust MARL and the "minimax / robust temporal-difference" method line. It extends the classical minimax-Q (Littman 1994) and robust TD learning (Klima et al. 2019) by introducing an adversarial choice over which agents to attack (not just which actions), connecting to work on adversarial attacks on cooperative MARL (Lin et al. 2020) and minimax policy gradients (Li et al. 2019). It is a concrete tabular instantiation of the "imagine worst-case attacks without simulating them during training" paradigm relevant to safety/fault-tolerance and critical-infrastructure robustness themes.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Robustness is a long-standing pursuit in the control and reinforcement learning theory (Zhou, Doyle, and Glover 1996; Morimoto and Doya 2005). While single-agent approaches pursue robustness during learning or planning by considering stochastic perturbations in transition probabilities and rewards (Abbasi Yadkori et al. 2013; Mohammed et al. 2019) or time-variant Markov dynamics (Lecarpentier and Rachelson 2019), MARL studies robustness primarily in terms of performance in the presence of different types of agents. All robust approaches share, however, a common ground: the environment is governed by some sort of uncertainty. In MARL, a policy is considered robust when agents perform well in various multi-agent environments, not necessarily encountered during the training process."

> _[Introduction]_

"Minimax decision rules are a common tool for designing robust policies in MARL (Littman 1994; Li et al. 2019). Devised in game theory to compute best-response policies in zero-sum games (von Neumann and Morgenstern 1947), minimax decision rules can be straightforwardly adopted to design agents acting in their best interests by best-responding to other agents that behave as zero-sum opponents (Littman 1994). As is customary, in this work we refer to agents behaving as zero-sum opponents as adversaries."

> _[Section: Related work]_

"When studying robustness in MARL, there are two essentially distinct ways to view adversaries. The Bayesian approach views adversaries as players in a game played between themselves and the cooperative agents comprising the system (Johanson, Zinkevich, and Bowling 2008). Under this direction, agents need to follow some form of opponent-aware reinforcement learning and attempt to learn policies that converge to the Nash equilibria of a general-sum or zero-sum game. The second approach computes best-response policies to attacks based on the agents' current estimation of the values of the optimal policy that can be found a priori. A robust operator "imagines" attacks during training, in order to come up with a policy robust to this type of attack without requiring the simulation of attacks during training (Klima et al. 2019). As the effect of an attack is calculated based on an agent's own value function, a model of the adversary is not required."

> _[Section: Related work]_

"When studying robustnes in MARL, in addition to the policies followed by adversaries, we also need to define the type of attack. We consider that policies define the actions that an adversary performs when controlling an agent, while the type of attack includes all other parameters required to fully describe the attack, which, among others, may include the number of attackers, selection of agents and probability of occurrence. We can argue that safety is in the eye of the designer, with different approaches to robustness anticipating different types of attacks. In the spirit of the recent deep reinforcement learning bloom, adversaries often manipulate the observations of agents with the aim of fooling the function approximators used for decision making. This type of attack can be at most as effective as the direct manipulation of actions considered in our single-step multi-agent adversarial attack. The work in (Lin et al. 2020) introduces a novel attack in cooperative systems, where an attacker first uses reinforcement learning to find the actions that will have the worst long-term effect on the system reward and, then, manipulates the observations of an agent to lead the victim to taking the wrong action. In contrast, our attack is short-sighted, choosing the actions that will bring the lowest reward in the current state. This is more appropriate in critical systems, where adversarial attacks attempt to bring the largest damage in a short time span."

> _[Section: Related work]_

"A variety of RL algorithms have already been combined with minimax updates. The stage was set by the seminal work of (Littman 1994) that introduced minimax-Q by blending the framework of MDPs with Markov games. Minimax policy gradients were introduced in (Li et al. 2019) to ensure robustness to various types of opponents in a multi-agent setting with a continuous action space. Robust temporal difference learning (Klima et al. 2019) considered security games where agents are attacked with a certain probability and modified classical temporal difference learning with minimax updates. Our work resembles this approach, as we also define a temporal difference algorithm for being robust to a certain type of attack. However, the type of attack that we consider here differs from the one in (Klima et al. 2019): adversaries in our formulation come in a certain number and find the most vulnerable agents to attack, instead of assuming that all agents are attacked with an equal probability."

### Cited references (resolved from the paper's bibliography)
- **[Abbasi Yadkori et al. 2013]** Abbasi Yadkori, Bartlett, Kanade, Seldin, Szepesvari. *Online learning in Markov decision processes with adversarially chosen transition probability distributions.* NeurIPS (Advances in Neural Information Processing Systems 26) 2013.
- **[Johanson, Zinkevich, and Bowling 2008]** Johanson, Zinkevich, Bowling. *Computing robust counter-strategies.* NeurIPS (Advances in Neural Information Processing Systems 20) 2008.
- **[Klima et al. 2019]** Klima, Bloembergen, Kaisers, Tuyls. *Robust temporal difference learning for critical domains.* AAMAS 2019.
- **[Lecarpentier and Rachelson 2019]** Lecarpentier, Rachelson. *Non-stationary Markov decision processes: a worst-case approach using model-based reinforcement learning.* NeurIPS 2019.
- **[Li et al. 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Lin et al. 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* arXiv abs/2003.03722, 2020.
- **[Littman 1994]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* ICML (Eleventh International Conference on Machine Learning) 1994.
- **[Mohammed et al. 2019]** Mohammed, Hang, Haitham, Vladimir, Rui, Mingtian, Jun. *Wasserstein robust reinforcement learning.* arXiv abs/1907.13196, 2019.
- **[Morimoto and Doya 2005]** Morimoto, Doya. *Robust reinforcement learning.* Neural Computation 17(2):335–359, 2005.
- **[von Neumann and Morgenstern 1947]** von Neumann, Morgenstern. *Theory of games and economic behavior.* Princeton University Press, 1947.
- **[Zhou, Doyle, and Glover 1996]** Zhou, Doyle, Glover. *Robust and Optimal Control.* Prentice-Hall, 1996.
