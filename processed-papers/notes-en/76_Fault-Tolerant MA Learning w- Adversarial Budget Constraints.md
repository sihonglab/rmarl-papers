# 76. Learning Robust Multi-Agent Policies via Selective Adversarial Fault Induction

## Metadata
- **Title**: Learning Robust Multi-Agent Policies via Selective Adversarial Fault Induction
- **Authors**: David Mguni, Yaqi Sun, Haojun Chen, Wanrong Yang, Amir Darabi, Larry Olanrewaju Orimoloye, Yaodong Yang
- **Affiliation**: Queen Mary University of London; Peking University; University of Liverpool; Snowflake Inc.
- **Venue**: Not specified (Preprint, arXiv:2508.08800v2, February 2026)
- **Link/arXiv**: arXiv:2508.08800v2 [cs.MA]

## Taxonomy
- **Robustness / perturbation type targeted**: Agent malfunctions / fault tolerance (actuator-level failures where an entire agent temporarily loses control to a fault policy); selectively induced, state-dependent, budget-constrained adversarial faults in cooperative MARL.
- **Method paradigm**: Switcher–Adversary mechanism; fault-switching (N+2)-player nonzero-sum Markov game; minimax / worst-case adversarial training; Q-learning with contraction-based convergence; switching control (optimal stopping) with cost/budget constraints; plug-and-play robustness layer.
- **Keywords**: fault-tolerant MARL, agent malfunction, switching control, minimax Markov game, malfunction budget, plug-and-play robustness

## TL;DR
The paper introduces MARTA, a plug-and-play robustness layer that augments standard cooperative MARL algorithms with a Switcher–Adversary mechanism which selectively induces agent malfunctions in performance-critical states, formulated as a fault-switching (N+2)-player Markov game with a switching-augmented Bellman operator proven to be a contraction (yielding a unique minimax value and convergence), and shows consistent robustness gains across TJ, LBF, MPE SimpleTag, and SMACv2.

## Problem & Motivation
Most successful MARL methods assume agents reliably execute the actions prescribed by their learned policies, an assumption that underpins centralised-training-decentralised-execution coordination. This makes MARL systems highly vulnerable to agent malfunctions: when an agent deviates from its intended behaviour due to faults or failures, coordination can break down, causing severe performance degradation. Such malfunctions are commonplace in real-world systems (e.g., industrial robots, factorised control as in multi-agent MuJoCo or dexterous manipulation). In single-agent RL, fault-tolerant policies are often induced via an adversary that minimises the learner's expected return (zero-sum game), but such always-on adversaries acting in exact opposition often induce overly pessimistic behaviour, causing excessive caution and degrading performance at higher levels of fault tolerance. MARTA addresses this by selectively, state-dependently inducing faults with a cost/budget, calibrating the robustness vs. nominal-performance trade-off.

## Robustness Setting
- **Threat model / uncertainty set**: A Switcher learns when and which agent should malfunction so as to maximally disrupt coordination; the malfunctioning agent's action is overridden by an Adversary policy σ^i while the other agents act normally. Two malfunction regimes: a random (Uniform) fault policy modelling stochastic actuator/sensor failures, and a Worst-case policy (adversarial via softmax(−Q*)) trained to maximally degrade collective performance. Each malfunction activation incurs a positive cost c > 0 (MARTA), or is limited by a fixed budget n on the number of malfunctions (MARTA-B). The Adversary/Switcher objective is −v (negated team value plus cost penalty).
- **Setting**: Cooperative, team-reward (Dec-MDP); partially observable; centralised training with decentralised execution; online model-free learning (Q-learning and actor-critic variants). The induced game is nonzero-sum with N+2 players (N cooperative agents, Switcher, Adversary).

## Method
- Formulates a fault-switching (N+2)-player nonzero-sum Markov game: at each state the Switcher chooses an action from the discrete set A_S = {0} ∪ N (action 0 = no malfunction, action i = malfunction agent i); if agent i is selected, its action is sampled from the adversarial policy σ^i while agents −i follow their intended policy π_{−i}.
- The N cooperative agents maximise the expected discounted team return; the Switcher and Adversary minimise it (objective −v), with the Switcher's value including an activation penalty c·1_N(g(s_t)) per triggered malfunction, encouraging interventions only where the harm is greatest. Larger c makes the Switcher more selective; as c → 0 the framework reduces to a classic always-on robust adversarial setting (overly cautious).
- Defines a switching-augmented joint Bellman operator that incorporates an intervention operator M̂ and activation penalties; proves it is a contraction (Lemmas E.9–E.12), giving a unique minimax value (Theorem 3.1), a Markov perfect equilibrium (Proposition 3.2), and convergence of a Q-learning variant (Theorem 3.3). Convergence is also extended to linear function approximation via a projected Bellman operator (Theorem 3.4).
- MARTA-B replaces the per-step cost with a budget constraint on the total number of malfunctions, tracking remaining budget y_t in an augmented state space X := S × N, and learns an optimal budget-respecting Switcher policy (Theorem D.2).
- Concrete realisation: N MARL agents each with an action policy π^i and adversarial policy σ^i using the same backbone (QMIX or VDN); the Switcher trained with soft actor–critic over an action space of size N+1; joint training with a shared replay buffer. Implemented as a plug-and-play layer without architectural modification.

## Theoretical Contributions
- Existence and uniqueness of the minimax value v* of the fault-switching game G (Theorem 3.1), via the contraction property of the switching-augmented Bellman operator and the Banach fixed-point theorem.
- The equilibrium policy is a Markov perfect equilibrium (Proposition 3.2).
- Convergence with probability 1 of a Q-learning variant to Q* (Theorem 3.3), and convergence under linear function approximation with an error bound ‖Φr* − Q*‖ ≤ (1 − γ²)^{−1/2}‖ΠQ* − Q*‖ (Theorem 3.4).
- Characterisation of the optimal Switcher policy via an obstacle condition determinable at each state (Proposition E.8).
- Convergence of MARTA-B under a fixed Switcher malfunction budget (Theorem D.2).
- Guarantees hold under standard RL/stochastic-approximation assumptions (Assumptions 1–6) and for tabular and linear function approximation; they do not extend directly to deep neural network parameterisations.

## Experiments
- **Environment/Benchmark**: Traffic Junction (TJ); Level-Based Foraging (LBF, 5×5–4p–1f); Multi-Agent Particle Environment (MPE) SimpleTag; StarCraft Multi-Agent Challenge v2 (SMACv2; maps 3m, 8m, 2s3z). Faults injected via Uniform and Worst-case fault policies, fixed/resampled faulty agents, and aligned vs. shifted train–test fault distributions (difficulty bands Easy/Medium/Hard).
- **Baselines**: Base MARL learners QMIX and VDN (with vs. without MARTA); MADDPG; M3DDPG; EIR; and a "random switching policy" ablation (Bernoulli trigger replacing the learned Switcher).
- **Evaluation metrics**: Test return mean / final return, Area Under the Learning Curve (AUC), win rate and episode return (SMACv2), fault-conditioned win rate, TJ collision/failure rate, LBF failure rate, MPE capture rate, SMAC focused fire rate; results averaged over 3 seeds with 95% confidence intervals.

## Key Results
- MARTA delivers large final-performance gains: up to 116.7% in SMAC (MARTA-VDN, 3m), 21.4% in MPE SimpleTag, and 44.6% in LBF; MARTA-QMIX achieves +11.1% (TJ), +21.4% (MPE), +44.6% (LBF), +114.9% (SMACv2 3m), +9.3% (SMACv2 8m). It also significantly reduces failure rates (e.g., TJ collision rate dropped from 17.5% to 5.0% for MARTA-VDN).
- The learned switching control substantially outperforms random malfunction activation; ablations show the switch cost c calibrates the fault–performance trade-off (preference for fault tolerance increases as c → 0), and MARTA remains robust across varying malfunction probability p and agent count N.
- As a plug-and-play layer, MARTA improves both QMIX and VDN backbones; MARTA-MADDPG consistently outperforms MADDPG and M3DDPG under the same malfunction process; and MARTA matches EIR under aligned (Case 1) faults while consistently outperforming EIR under dynamic, distribution-shifted (Case 2) faults.
- Execution-time overhead is minimal (no auxiliary safety filter or online optimisation at execution), with only modest training-time overhead from the lightweight Switcher.

## Limitations & Future Work
- Theoretical guarantees are derived under tabular or linear function approximation and standard assumptions; they do not extend directly to deep neural network parameterisations (the analysis characterises the idealised optimisation problem MARTA solves).
- The framework focuses on cooperative, team-reward settings and on non-strategic actuator-level malfunctions; strategic adversarial teammates (e.g., Byzantine deviations) represent a different robustness regime.
- Future-work directions are Not specified beyond noting that MARTA can be combined with more sophisticated robust architectures and complements existing robust MARL techniques.

## Relevance to Survey
This paper sits on the fault-tolerance / agent-malfunction line of robust MARL, distinct from but adjacent to the model-uncertainty and observation/action-perturbation lines. Methodologically it connects the game-theoretic equilibrium and minimax adversarial-training paradigm to switching-control / optimal-stopping theory, contributing a budgeted, state-dependent variant of worst-case adversarial training with contraction-based convergence guarantees. It explicitly positions itself against shielding/backup-policy and constrained-MARL safety methods, robust/adversarial MARL (M3DDPG, EIR), diagnostic/poisoning attack work (RTCA, One4all), and Byzantine-robust cooperative MARL, making it a useful node connecting fault tolerance, safety, and adversarial robustness themes.

## Related Work (verbatim excerpts from the paper)
> _[Section 6, Related Work — "Fault tolerance and safety in MARL."]_

"Fault tolerance and safety in MARL. Safety and robustness in MARL have been studied through shielding, backup policies and constrained optimisation. Shielding approaches (Zhang et al., 2019; ElSayed-Aly et al., 2021) use additional safety layers or backup policies to override unsafe actions. Qin et al. (Qin et al., 2021) employ control barrier functions to enforce safety constraints, but without formal guarantees. These methods often require per-timestep safety checks or dedicated certificates, and their cost grows with the number of agents. In contrast, MARTA embeds robustness directly into the training dynamics avoiding runtime safety layers and preserving the architecture of the underlying MARL learner. Constrained MARL formulations (Gu et al., 2021; Lu et al., 2021) treat safety as a constrained optimisation problem. These methods often face convergence and scalability challenges. By contrast, the MG underlying MARTA has a unique solution to which MARTA has convergence guarantees for tabular and linearly approximated settings."

> _[Section 6, Related Work — "Robust and adversarial MARL."]_

"Robust and adversarial MARL. Adversarial training methods for RL and MARL (Pinto et al., 2017; Li et al., 2019; Zhang et al., 2020) typically introduce an opponent that perturbs actions, observations or dynamics to construct worst-case trajectories. These methods improve robustness but often induce overly conservative behaviour, since the agent is trained under an adversary that is active at every step. Moreover, most such work focuses on perturbations in a single-agent MDP or on model uncertainty, rather than on explicit agent malfunctions in cooperative teams. MARTA differs in three ways. First, it targets actuator-level failures in which an entire agent temporarily loses control to a fault policy, rather than small perturbations around nominal actions or states. Second, it models the timing and location of faults through a Switcher that explicitly reasons over state-dependent costs or budgets, rather than assuming an always-on adversary. Third, it provides convergence guarantees for this switching-augmented game, including under linear function approximation and budget constraints."

> _[Section 6, Related Work — "Diagnostics and poisoning attacks in MARL."]_

"Diagnostics and poisoning attacks in MARL. Recent work has examined the vulnerability of MARL systems to targeted perturbations or poisoning attacks. RTCA (Zhou & Liu, 2023) proposes a resilience testing framework that perturbs the states of critical agents to expose weaknesses. Zheng et al. study training-time poisoning in which a single manipulated agent can poison policies. These works are primarily diagnostic or attack-oriented: they evaluate the weakness of existing MARL policies or design efficient attacks, rather than providing a defence scheme that yields robust policies. MARTA is complementary. It is a training-time defence mechanism that induces controlled, state-dependent malfunctions then trains agents to jointly best respond."

> _[Section 6, Related Work — "Byzantine-robust MARL and adversarial teammates."]_

"Byzantine-robust MARL and adversarial teammates. Li et al. (Li et al., 2023) study Byzantine-robust cooperative MARL through a Bayesian game formulation, in which some teammates may behave adversarially. Their focus is on strategic deviations modelled through adversarial types and on robust reasoning about such behaviour. MARTA instead models non-strategic actuator malfunctions, such as stuck actuators, corrupted control modules and state-dependent controller failures. These represent different robustness regimes. Strategic adversaries may deliberately coordinate to mislead, whereas actuator faults in physical systems are often non-strategic yet catastrophic for coordination. MARTA introduces a specific fault-switching MG (with budgets), and proves existence and uniqueness of a minimax value and convergence under both tabular and linearly approximated settings. This yields a different set of theoretical guarantees tailored to the malfunction setting."

> _[Section 6, Related Work — "Shielding, backup policies and scalability."]_

"Shielding, backup policies and scalability. Shielding and backup-policy methods (Zhang et al., 2019; ElSayed-Aly et al., 2021; Qin et al., 2021) provide valuable tools for enforcing safety constraints by modifying actions at execution time. However, their reliance on online constraint checking and per-agent safety mechanisms can create scalability challenges as the number of agents grows. MARTA takes a complementary approach which avoids runtime safety layers and allows robustness to scale with the underlying MARL learner without redesigning its architecture. Finally, MARTA is intentionally plug-and-play. It attaches to standard value-based and actor–critic MARL algorithms without altering their internal networks, and can also be combined with more sophisticated robust architectures. In this sense, MARTA acts as a general robustness layer that complements rather than replaces existing robust MARL techniques."

> _[Introduction — single-agent fault-tolerant RL background]_

"In single-agent reinforcement learning (RL), a substantial body of work has studied fault-tolerant (FT) policies that maintain performance under failures (Mguni, 2019; Fan et al., 2021). A common approach, inspired by control theory, introduces an adversarial agent that selects actions to minimise the learner's expected return (Pinto et al., 2017). By exposing the agent to worst-case outcomes, such methods aim to induce robust policies. This formulation leads to a zero-sum game between the controller and the adversary, which is amenable to theoretical analysis due to its structural properties (Osborne & Rubinstein, 1994). However, adversaries that act in exact opposition to the agent's objective often induce overly pessimistic behaviour, causing agents to proceed with excessive caution and degrading performance at higher levels of fault tolerance (Grau-Moya et al., 2018)."

### Cited references (resolved from the paper's bibliography)
- **[ElSayed-Aly et al., 2021]** ElSayed-Aly, Bharadwaj, Amato, Ehlers, Topcu, Feng. *Safe multi-agent reinforcement learning via shielding.* arXiv:2101.11196, 2021.
- **[Fan et al., 2021]** Fan, Ma, Dai, Jing, Tan, Low. *Fault-tolerant federated reinforcement learning with theoretical guarantee.* NeurIPS 2021.
- **[Grau-Moya et al., 2018]** Grau-Moya, Leibfried, Bou-Ammar. *Balancing two-player stochastic games with soft q-learning.* IJCAI 2018.
- **[Gu et al., 2021]** Gu, Kuba, Wen, Chen, Wang, Tian, Wang, Knoll, Yang. *Multi-agent constrained policy optimisation.* arXiv:2110.02793, 2021.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Li et al., 2023]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a bayesian game.* arXiv:2305.12872, 2023.
- **[Lu et al., 2021]** Lu, Zhang, Chen, Başar, Horesh. *Decentralized policy gradient descent ascent for safe multi-agent reinforcement learning.* AAAI 2021.
- **[Mguni, 2019]** Mguni. *Cutting your losses: Learning fault-tolerant control and optimal stopping under adverse risk.* arXiv:1902.05045, 2019.
- **[Osborne & Rubinstein, 1994]** Osborne, Rubinstein. *A course in game theory.* MIT Press, 1994.
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Qin et al., 2021]** Qin, Zhang, Chen, Chen, Fan. *Learning safe multi-agent control with decentralized neural barrier certificates.* arXiv:2101.05436, 2021.
- **[Zhang et al., 2019]** Zhang, Bastani, Kumar. *MAMPS: Safe multi-agent reinforcement learning via model predictive shielding.* arXiv:1910.12639, 2019.
- **[Zhang et al., 2020]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Zhou & Liu, 2023]** Zhou, Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv:2306.06136, 2023.
- **[Zheng et al.]** Zheng, Li, Chen, Dong, Zhang, Lin. *One4all: Manipulate one agent to poison the cooperative multi-agent reinforcement learning.* Computers & Security, 2023.
