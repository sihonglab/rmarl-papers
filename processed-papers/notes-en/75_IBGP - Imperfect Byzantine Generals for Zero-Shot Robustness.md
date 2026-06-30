# 75. IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems

## Metadata
- **Title**: IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems
- **Authors**: Yihuan Mao, Yipeng Kang (equal contribution), Peilun Li, Ning Zhang, Wei Xu, Chongjie Zhang
- **Affiliation**: Tsinghua University; State Key Laboratory of General Artificial Intelligence (BIGAI); Shanghai Tree-Graph Blockchain Research Institute; Washington University in St. Louis
- **Venue**: Under review of AAMAS 2025 (preprint); arXiv 2024
- **Link/arXiv**: arXiv:2410.16237v2 [cs.MA]

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks (adversarial / Byzantine messages); malicious agents with unknown identities (from LLM-agent hallucinations or external attacks); fault tolerance / consensus under attack
- **Method paradigm**: Byzantine consensus protocols (randomized, multi-round broadcast with a global randomizer), partial-consensus protocol design, certified/provable robustness, integration with MARL (QMIX-based learnable communication)
- **Keywords**: Multi-agent Systems, Zero-shot Robustness, safety, Byzantine Generals Problem, consensus protocol, communicative MARL

## TL;DR
The paper introduces the Imperfect Byzantine Generals Problem (IBGP) — a relaxation of the classical BGP that requires only partial (k-of-n) consensus matching practical MAS coordination — and proposes a randomized multi-round (k, λ)-consensus protocol with provable zero-shot robustness against communication attacks, integrating it as a coordination module into MARL.

## Problem & Motivation
As heterogeneous (LLM-driven) agents increasingly coordinate in shared infrastructure (sensor networks, UAV control, autonomous vehicles), reliable message synchronization becomes safety-critical, yet such general-purpose agents lack a trustworthy predefined broadcast module: their messages can diverge from actions due to hallucinations or because they are compromised and behave maliciously. The classical Byzantine Generals Problem (BGP) addresses such adversarial consensus but demands global consensus among all benign agents, which is often unnecessary and inefficient in MAS where only partial coordination (e.g., a subset of predators hunting one prey, or a contribution threshold in a public-goods game) is required. The authors argue prior consensus work in MAS rarely considers adversarial attacks, and the few that do lack zero-shot adaptation to attackers and environments — motivating a refined "imperfect" BGP and a tailored protocol that tolerates a higher fraction of malicious agents (up to 50%) with less redundancy.

## Robustness Setting
- **Threat model / uncertainty set**: n benign agents and t attacker agents communicate over a complete network for several rounds; attackers can send arbitrary false messages to disturb coordination (only communication channels, not actions, of malicious agents are attacked). Agents are unaware of which communicating agents are benign or malicious. The goal is to avoid mis-coordination under *any* attack scheme (zero-shot, arbitrary attacks), not to maximize expected return. Initial proposals/decisions are binary M0, a ∈ {0,1} (1 = cooperate, 0 = give up). BGP feasible only when malicious agents <33%; IBGP tolerates up to 50%.
- **Setting**: cooperative MAS; decentralized (Dec-POMDP, partially observable); the consensus protocol is decentralized and online; trained by Q-learning (QMIX-based) with learnable communication; training/testing split where attackers are trained in the testing phase.

## Method
- **IBGP formalization (partial consensus):** Redefines BGP's Agreement and Consistency to require only a coordination threshold k. Agreement: #(M0_i = 1, a_i = 1) ∈ {0} ∪ [k, n] (either no benign agent acts, or at least k observing M0=1 cooperate). Mis-coordination is 0 < #(M0_i=1, a_i=1) < k (some try to coordinate but fail). Only agents observing M0=1 may take cooperative action a=1.
- **(k, λ)-consensus protocol:** A multi-round broadcast scheme using an independent global randomizer (à la Rabin's randomized Byzantine generals) that samples the total number of rounds r_tot from a distribution R, revealed only at the last round. Each round, active agents broadcast 1 iff the number of received "1" messages ≥ k+λ; in the decision round agents act a_i=1 iff received "1" messages ≥ k. A single-round threshold process is shown (via didactic examples) to be inadequate; the randomized round count prevents attackers from forcing mis-coordination.
- **Theoretical robustness:** Setting λ = t makes the (k, t)-protocol robust under any attack on IBGP(t, k) with confidence 1 − max_r{p(r_tot = r)} (Theorem 1). Relaxed/aggressive variants (λ < t) and per-agent varying λ_i trade robustness for efficiency under benign attacker distributions.
- **Multi-target extensions:** Run the protocol independently per target; a "dispersion defense" round (random permutations + majority vote) disperses attacker influence so only a small ratio of targets mis-coordinate (Theorem 2). A greedy target-selection algorithm gives a 1/k_max-approximation to the NP-complete optimal selection.
- **Integration with MARL:** The consensus process is a subprocess in a Dec-POMDP. Agents learn local Q-values; a special "propose to catch" action sets M0_i=1 to enter the consensus, and the protocol decides whether cooperation proceeds, providing robustness without retraining the agents against attacks.

## Theoretical Contributions
- **Theorem 1:** the (k, t)-protocol is robust with confidence 1 − max_r{p(r_tot = r)} under any attack on IBGP(t, k) (proof by enumerating initialization cases plus a monotonic-deactivation lemma).
- **Theorem 2:** in an m-target environment, the (k+λ)-protocol with dispersion defense causes at most 3t/λ targets to mis-coordinate with high probability (Hoeffding-based bound).
- **Theorem 3:** under an attacker-distance condition dist(Atk, Atk_all-1) ≥ t−λ, the relaxed (k+λ)-protocol does not fail with high probability.
- **Theorem 4:** the consensus-based sensor-network algorithm is robust if at most one attacker is in any neighborhood (given mild connectivity assumptions).
- NP-completeness of optimal target selection (reduction to Set Packing) and a 1/k_max-approximation guarantee for the greedy selection algorithm.

## Experiments
- **Environment/Benchmark**: Predator-prey (modified, single/multi-target/large-scale: Predator-prey(4,1,2,1), (5,2,2,1), (20,4,2,2), (20,1,4,2)); Hallway (Hallway(3,1,2,1), Hallway(10,1,5,2)); SMAC-based StarCraft II environments 4bane_vs_1hM(4,1,3,1) and a new 3z_vs_1r(3,1,2,1); plus a continuous Sensor Network case study.
- **Baselines**: Recursive training (the recursive-training contribution from Xue et al. [23]); AME (Sun et al. [20]); ADMAC (Yu et al. [24]).
- **Evaluation metrics**: Robustness percentage = ratio of performance with attackers (testing phase) to performance without attackers (training phase); attackers are trained to maximally harm benign agents, displaying zero-shot robustness against any attack scheme.

## Key Results
- The IBGP protocol largely maintains performance from training to testing across all environments, achieving high robustness percentages (e.g., 96.1±5.4% on Predator-prey(4,1,2,1), 100% on the two large-scale Predator-prey tasks, 96.7±4.7% on Hallway(3,1,2,1), 98.4±2.2% on 4bane_vs_1hM).
- Baselines are substantially less robust: recursive training often drops to ~0% (it prioritizes adaptation to attackers, not zero-shot robustness); AME degrades in several environments (its majority-taking can leave multiple majority actions exploitable); ADMAC is low because its reliability estimator was trained on specific small-disturbance attacks.
- On the challenging 3z_vs_1r task (requiring both resilience and efficiency), IBGP reaches 51.5±2.6% while baselines fail to converge or score low.
- Sensor Network case study: agents' beliefs stay consistent with the true target signal (near-zero std), and a vanilla-broadcasting counterexample shows mis-coordination without the consensus protocol; varying λ per agent yields the most adaptive protocol on average.

## Limitations & Future Work
- The IBGP protocol is only effective in environments where a specific target exists, rather than arbitrary RL environments.
- The single-target protocol is conservative under multiple targets (each target as conservative as the single-agent case) absent the dispersion defense; optimal target selection is NP-complete.
- Future work: explore a generalized trainable framework for consensus protocols adaptable to more complex and realistic settings.

## Relevance to Survey
Sits on the "communication robustness / adversarial communication attacks" line of robust MARL, with a strong "Byzantine / fault tolerance" and "certified / provable robustness" flavor. Distinct from value/model-uncertainty robust MARL, it brings distributed-systems consensus theory (BGP, PBFT, randomized Byzantine generals) into communicative MARL, and directly contrasts with certified-robustness and active-defense communication baselines (AME, ADMAC) and adaptation-based defenses (recursive training). Its emphasis on zero-shot robustness for heterogeneous LLM-agent coordination connects the robust-MARL theme to emerging LLM multi-agent systems.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work]_

"The Byzantine Generals Problem [11] describes a scenario where a group of Byzantine generals must agree on a common plan of action, even though some of the generals may be traitors. This models a large type of distributed consistency problem in computer science. Byzantine consensus protocols in a distributed network can be used to reach an agreement on a single value, even in the presence of faulty or malicious nodes. Important works of Byzantine consensus protocols include Practical Byzantine Fault Tolerance (PBFT) [2] and Randomized Byzantine Generals [16]. PBFT is a solution to the Byzantine Generals Problem that is designed for practical use in distributed systems. Rabin's work [16] provided a solution to the Byzantine Generals Problem that did not require a centralized authority or a trusted third party. Instead, it introduced the idea of a randomized protocol where each node chooses a random value that is used to break ties in the event of conflicting messages. The randomization ensures that Byzantine nodes cannot predict the outcome of the protocol, making it more difficult for them to interfere with the consensus process."

"In the context of MAS research, one important research branch of MAS involves learning a communications system to achieve a common goal. Some use explicit communication systems with discrete or continuous signals, mainly to convey informative local observations to each other, to deal with partial observation [8, 21]. Some use communication for global value optimization [1, 9]. Different from these categories, in MAS research, consensus refers to achieving a global agreement over a particular feature of interest [4–6, 12–14, 25]. It has been widely studied as it affects communication and collaboration between agents. However, very few of them paid attention to adversarial attacks. Recently some researchers have investigated algorithms to mitigate the impact of malicious agents [20, 23]. However, their methodologies lack zero-shot adaption ability to the attackers and the environment."

> _[Introduction — prior-work / motivation passages]_

"Traditionally, this issue relates to the consensus problem in distributed systems, such as the Byzantine Generals Problem (BGP) [11], where the primary objective is to synchronize content across all benign nodes and achieve system-wide consistency, even in the presence of node failures. In this context, a perfect protocol is essential. However, in the coordination of multi-agent systems, consensus serves as a means to achieve team goals, allowing for a relaxation of stringent requirements; often, it suffices to synchronize only a minimal number of benign agents."

### Cited references (resolved from the paper's bibliography)
- **[1]** Böhmer, Kurin, Whiteson. *Deep coordination graphs.* ICML 2020.
- **[2]** Castro, Liskov. *Practical Byzantine Fault Tolerance.* OSDI 1999.
- **[4]** Dorri, Kanhere, Jurdak. *Multi-agent systems: A survey.* IEEE Access 6, 2018.
- **[5]** Fan, Zhang, Wang. *Bipartite flocking for multi-agent systems.* Communications in Nonlinear Science and Numerical Simulation, 2014.
- **[6]** Fu, Wang. *Adaptive coordinated tracking of multi-agent systems with quantized information.* Systems & Control Letters, 2014.
- **[8]** Kang, Wang, de Melo. *Incorporating pragmatic reasoning communication into emergent language.* NeurIPS 2020.
- **[9]** Kang, Wang, Yang, Wu, Zhang. *Non-Linear Coordination Graphs.* NeurIPS 2022.
- **[11]** Lamport, Shostak, Pease. *The Byzantine Generals Problem.* ACM Trans. Program. Lang. Syst. 4(3), 1982.
- **[12]** Liu, Xie, Zhang. *Containment control of multi-agent systems by exploiting the control inputs of neighbors.* International Journal of Robust and Nonlinear Control, 2014.
- **[13]** Olfati-Saber. *Flocking for multi-agent dynamic systems: Algorithms and theory.* IEEE Transactions on Automatic Control, 2006.
- **[14]** Olfati-Saber, Murray. *Consensus problems in networks of agents with switching topology and time-delays.* IEEE Transactions on Automatic Control, 2004.
- **[16]** Rabin. *Randomized byzantine generals.* FOCS (SFCS) 1983.
- **[20]** Sun, Zheng, Hassanzadeh, Liang, Feizi, Ganesh, Huang. *Certifiably Robust Policy Learning against Adversarial Multi-Agent Communication.* ICLR 2023.
- **[21]** Wang, Wang, Zheng, Zhang. *Learning Nearly Decomposable Value Functions Via Communication Minimization.* ICLR 2020.
- **[23]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-Spoke or Mis-Lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning.* AAMAS 2022.
- **[25]** Yu, Chen, Cao, Kurths. *Second-order consensus for multiagent systems with directed topologies and nonlinear dynamics.* IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics), 2009.
