# 161. Adversarial attacks in consensus-based multi-agent reinforcement learning

## Metadata
- **Title**: Adversarial attacks in consensus-based multi-agent reinforcement learning
- **Authors**: Martin Figura, Krishna Chaitanya Kosaraju, Vijay Gupta
- **Affiliation**: Department of Electrical Engineering, University of Notre Dame, Notre Dame, IN, USA
- **Venue**: Not specified (arXiv:2103.06967 [eess.SY], 11 Mar 2021)
- **Link/arXiv**: arXiv:2103.06967v1

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agent / insider attack on communication in cooperative networked MARL (a participating agent is malicious, compromising consensus and critic updates and broadcasting false reward/value signals); related to fault tolerance and resilient consensus.
- **Method paradigm**: Consensus-based decentralized actor-critic (networked MARL); attack design + convergence (ODE / stochastic approximation) analysis; demonstrates fragility rather than proposing a defense.
- **Keywords**: consensus MARL, adversarial attack, malicious agent, networked MDP, distributed actor-critic, resilience

## TL;DR
The paper shows that a standard consensus-based cooperative MARL algorithm is fragile to insider attacks: a single malicious agent that compromises its consensus and critic updates and broadcasts identical signals can persuade all other agents in the network to converge to a policy that locally maximizes the adversary's own objective rather than the team objective.

## Problem & Motivation
Cooperative distributed MARL with decentralized rewards relies on agents communicating through a consensus protocol so the whole network can estimate team-average quantities and converge to a team-optimal policy while keeping individual rewards private. Linear consensus theory already shows that, in the presence of a single malicious agent that does not apply consensus updates, the limiting consensus value coincides with the adversary's value. The authors ask whether, in the consensus MARL algorithm of [9, Algorithm 2], a single adversarial participating agent can either prevent convergence or, worse, drive the other agents to optimize a utility function it chooses. Unlike commonly studied external data-poisoning attacks, here a participating agent itself is malicious. The work shows the answer is affirmative and motivates the development of resilient consensus MARL algorithms.

## Robustness Setting
- **Threat model / uncertainty set**: A single malicious participating agent (set N⁻ has exactly one element). The adversary can compromise the rewards rⁱ_{t+1} to incentivize its malicious behavior, ignores/omits the consensus step (does not apply consensus updates), can compromise consensus and critic updates, and transmits the same signal values to all its neighbors, spreading false information about network performance. The adversary acts greedily to maximize its own objective (2) instead of the team-average objective (1). More general attacks (multiple adversaries, arbitrary parameter updates, arbitrary policy changes) are noted as possible but out of scope.
- **Setting**: Cooperative (networked, team-average reward); fully decentralized / consensus-based actor-critic with local private rewards; online training over a (time-varying) communication graph.

## Method
- Considers a networked MDP (S, {Aⁱ}, P, {Rⁱ}, G) where each agent observes the global state and action but keeps its individual reward private; cooperative agents (N⁺) seek to maximize the discounted team-average objective J⁺(θ), while the adversary (N⁻) maximizes its own discounted objective J⁻(θ).
- Uses the consensus actor-critic Algorithm 1 (a discounted-reward version of [9, Algorithm 2]): each agent maintains linear approximations of the network value function V(s; vⁱ) and network reward function r̄(s,a; λⁱ), performs TD-style critic and reward-parameter updates, an actor update on a slower timescale, and a consensus step that averages λ̃ and ṽ with neighbors over Gₜ. The adversary runs the same algorithm but omits the consensus step.
- Casts the network-reward estimation as a distributed least-squares problem (Eqs. 3–4) whose stationary points let agents individually take gradient steps on λⁱ using their true private rewards and then share encoded parameters via consensus.
- Analyzes convergence via the limiting ODE / stochastic-approximation framework (two-timescale): proves the critic and reward parameters of all agents converge to the adversary's fixed point because the adversary's non-consensus updates make the consensus unbalanced and the limiting value coincide with the adversary's.

## Theoretical Contributions
- **Theorem 1**: Under Assumptions 1 and 3–7, for any fixed policy π(a|s; θ), the critic and reward parameters converge almost surely (limₜ vⁱₜ = v_θ, limₜ λⁱₜ = λ_θ for all i ∈ N), and v_θ, λ_θ are the unique solutions of the fixed-point equations (5)–(6) defined with respect to the adversary's reward R̂ʲ (j ∈ N⁻) — i.e., the whole network converges to the adversary's reward/value.
- Supporting **Lemmas 1–3**: boundedness of the parameter sequence (sup‖zₜ‖ < ∞ a.s.); asymptotic convergence of the adversary's parameters to z_θ; and convergence of the disagreement vector to zero (consensus), leveraging the analysis of [9].
- **Theorem 2** ([9, Theorem 4.10]): the policy parameter converges a.s. to an asymptotically stable equilibrium of the actor ODE; the authors note the network policy converges to a point where the estimated TD error is zero and hence locally maximizes the adversary's objective (2) rather than the team objective (1).

## Experiments
- **Environment/Benchmark**: A 6×6 grid-world with N = {1,2,3,4,5} agents (|S| = 36⁵ ≈ 60.5 million states, |A| = 5⁵); each agent's reward depends on distance to its desired position minus collision penalties; actors, critics, and global reward functions approximated by neural networks with two hidden layers; communication graph fully connected. Agent 1 is the adversary; agents 2–5 are cooperative.
- **Baselines**: The decentralized actor-critic algorithm of [9] (the adversary-free network) is the comparison.
- **Evaluation metrics**: Cumulative team-average rewards per episode (true vs. estimated), per-agent true cumulative rewards per episode, and final network states (whether agents reach their desired grid positions), over 200 training episodes.

## Key Results
- The adversary-free network performs significantly better than the attacked network on cumulative team-average rewards (Fig. 1); the estimated reward function converges in both scenarios but more slowly under attack.
- In the adversary-free case all agents reach their desired positions; under attack, only the adversary reaches its desired position while the cooperative agents perform poorly (Fig. 2).
- Per-agent results (Fig. 3) show the adversary quickly learns a near-optimal policy (it acts greedily w.r.t. the rest of the network), while the remaining agents perform markedly worse than in the adversary-free scenario — confirming the network ends up maximizing the adversary's objective.

## Limitations & Future Work
- The analysis is deliberately narrow: exactly one adversary (Assumption 7) that learns from compromised rewards, omits consensus, and broadcasts identical signals; more general attacks (multiple adversaries, arbitrary parameter updates, arbitrary policy changes) are not analyzed.
- Requires all agents to use the same basis functions / networks so parameters can reach consensus; the authors note this could be relaxed with gossip-based algorithms [21] but that convergence analysis is challenging.
- The paper demonstrates fragility but does not propose a defense; future work is to develop resilient consensus-based MARL algorithms, with the unique challenge of providing robustness for functions jointly estimated by the network while keeping rewards private.

## Relevance to Survey
This paper sits on the "adversarial agents / communication attacks" and "fault tolerance / resilient consensus" lines of robust MARL, specifically targeting fully decentralized, consensus-based networked actor-critic methods (the Zhang et al. [9] family). It is an attack/vulnerability-analysis contribution that exposes the fragility of vanilla consensus MARL to insider adversaries, motivating later work on Byzantine-resilient and resilient consensus MARL, and connects the MARL literature to the resilient-consensus / distributed-systems robustness literature.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction]_

"Consensus algorithms are generally devised for distributed systems to find agreement on signal values over networks [10]. These algorithms find applications in many fields including sensor networks [11], coordination of vehicles [12], or even blockchain [13]. In practice, consensus algorithms must be robust to faults that arise from relatively frequent occurrences of interrupted communication links or corrupted signals [14]. Therefore, the convergence of resilient consensus algorithms was rigorously studied under different considerations for the nature of adversarial attacks [15], graph topology [16], [17], or frequency of communication [18]. These research efforts naturally complement studies of the influence of adversarial attacks on network performance. A simple yet powerful result from the analysis of linear consensus [11] states that the topology of a consensus matrix determines the limiting value for the consensus updates. In the presence of a single malicious agent, which does not apply consensus updates, the limiting value coincides with the adversary's value."

> _[Section I, Introduction]_

"In the consensus MARL algorithm in [9, Algorithm 2], every agent estimates the team-average reward and value function using linear approximations and exchanges parameters with other agents through a consensus protocol. Interestingly, this scheme guarantees the asymptotic convergence to the team-average optimal policy even with simultaneous actor, critic, and consensus updates over time-varying communication graphs. Furthermore, the algorithm retains the convergence property even with sparse data transmission for strongly connected graphs [19]."

> _[Section I, Introduction]_

"In this paper, we study the effects of adversarial attacks on the consensus MARL algorithm [9, Algorithm 2] with discounted rewards in the objective function. The attacks we consider are different from the commonly studied data poisoning attacks in ML or RL, which seek to understand if changing the data or rewards by an external agent can degrade the performance of RL algorithms [20]. Here, we consider a MARL setting where a participating agent itself is malicious. Specifically, we ask whether a single adversarial agent can either prevent convergence of the algorithm, or even worse, lead the other agents to optimize a utility function that it chooses. We show that the answer to this question is in the affirmative by designing a suitable attack and analyzing the convergence of the algorithm under it."

### Cited references (resolved from the paper's bibliography)
- **[9]** K. Zhang, Z. Yang, H. Liu, T. Zhang, T. Başar. *Fully decentralized multi-agent reinforcement learning with networked agents.* arXiv preprint arXiv:1802.08757, 2018.
- **[10]** R. Olfati-Saber, J. A. Fax, R. M. Murray. *Consensus and cooperation in networked multi-agent systems.* Proceedings of the IEEE, 95(1):215–233, 2007.
- **[11]** R. Olfati-Saber, J. S. Shamma. *Consensus filters for sensor networks and distributed sensor fusion.* Proceedings of the 44th IEEE Conference on Decision and Control, 2005.
- **[12]** W. Ren, R. W. Beard, E. M. Atkins. *Information consensus in multivehicle cooperative control.* IEEE Control Systems Magazine, 27(2):71–82, 2007.
- **[13]** D. Mingxiao, M. Xiaofeng, Z. Zhe, W. Xiangwei, C. Qijun. *A review on consensus algorithm of blockchain.* IEEE International Conference on Systems, Man, and Cybernetics (SMC), 2017.
- **[14]** M. J. Fischer. *The consensus problem in unreliable distributed systems (a brief survey).* International Conference on Fundamentals of Computation Theory, Springer, 1983.
- **[15]** H. J. LeBlanc, H. Zhang, X. Koutsoukos, S. Sundaram. *Resilient asymptotic consensus in robust networks.* IEEE Journal on Selected Areas in Communications, 31(4):766–781, 2013.
- **[16]** D. Saldana, A. Prorok, S. Sundaram, M. F. Campos, V. Kumar. *Resilient consensus for time-varying networks of dynamic agents.* American Control Conference (ACC), 2017.
- **[17]** S. Sundaram, C. N. Hadjicostis. *Finite-time distributed consensus in graphs with time-invariant topologies.* American Control Conference, 2007.
- **[18]** D. Ding, Z. Wang, D. W. Ho, G. Wei. *Observer-based event-triggering consensus control for multiagent systems with lossy sensors and cyber-attacks.* IEEE Transactions on Cybernetics, 47(8):1936–1947, 2016.
- **[19]** Y. Lin, K. Zhang, Z. Yang, Z. Wang, T. Başar, R. Sandhu, J. Liu. *A communication-efficient multi-agent actor-critic algorithm for distributed reinforcement learning.* IEEE 58th Conference on Decision and Control (CDC), 2019.
- **[20]** Y. Ma, X. Zhang, W. Sun, J. Zhu. *Policy poisoning in batch reinforcement learning and control.* Advances in Neural Information Processing Systems (NeurIPS), 2019.
