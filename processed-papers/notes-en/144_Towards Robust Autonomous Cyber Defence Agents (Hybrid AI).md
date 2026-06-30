# 144. Towards Robust Autonomous Cyber Defence Agents using Hybrid AI models

## Metadata
- **Title**: Towards Robust Autonomous Cyber Defence Agents using Hybrid AI models
- **Authors**: Laurin Holz, Johannes Loevenich, Roberto Rigolin F. Lopes
- **Affiliation**: Secure Communications & Information (SIX), Thales Deutschland, Ditzingen, Germany
- **Venue**: IEEE NetSoft 2025 (2025 IEEE 11th International Conference on Network Softwarization)
- **Link/arXiv**: DOI: 10.1109/NETSOFT64993.2025.11080605

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial resilience and safety of MARL agents in Autonomous Cyber Defence (ACD) under uncertainty, partial observability, and adversarial/unexpected inputs (state/observation perturbations, fault tolerance, manipulation); robustness verified via Formal Verification (FV)
- **Method paradigm**: Hybrid AI (MARL + symbolic AI / knowledge graphs + augmented/fine-tuned LLMs) combined with Formal Verification (reachability analysis, model checking, fuzz testing, temporal logic, theorem proving, abstract interpretation); curriculum learning; CTDE; human-in-the-loop verification
- **Keywords**: Software-Defined Defence, Autonomous Cyber Defence, Multi-Agent Reinforcement Learning, Formal Verification, Cyber Security

## TL;DR
This thesis/position paper proposes a framework that applies Formal Verification techniques to MARL-based Autonomous Cyber Defence agents — augmented with an LLM-based human-in-the-loop interface — to provide mathematically grounded guarantees of correctness, safety, and adversarial robustness in mission-critical military network infrastructures.

## Problem & Motivation
Software-Defined Defence (SDD) provides interfaces for multi-layer monitoring and control that enable Autonomous Cyber Defence (ACD) in critical (military) network infrastructure, where hybrid AI models (MARL + symbolic AI + LLMs) can detect, predict, protect, respond, and recover from cyberattacks. However, there is limited research assessing the robustness and security of these agents, and the non-transparent, stochastic nature of learned MARL policies hinders trust and deployment in critical environments. The paper proposes to design and evaluate Formal Verification methods to quantify and improve the robustness of hybrid AI cybersecurity solutions, and to integrate LLMs to translate formal outputs (temporal logic formulas, counterexamples, violated properties) into natural-language explanations for human-in-the-loop oversight.

## Robustness Setting
- **Threat model / uncertainty set**: ACD agents operate under high uncertainty and partial observability, with only partial/local/noisy views of the global network state; they must detect and mitigate evolving cyber threats. Robustness is assessed against unexpected/adversarial inputs in the input space, environmental variability, and manipulation (via fuzz testing for fault tolerance/resilience, and reachability analysis to check unsafe states). The threat is modeled within a POMDP M = (S, A, T, R, Ω, O, γ); adversarial behaviours influence the transition function T.
- **Setting**: Cooperative (two or more blue defender agents collaborating to defend user hosts and operational servers), partially observable, multi-agent; training strategies include CTDE, Independent Learning, CTCE, and hierarchical MARL; simulated/emulated environments (online training).

## Method
- Phase A — Model training: Train MARL agents in simulated Automated Cyber Operation (ACO) gym environments using a curriculum learning approach, evaluating CTDE, Independent Learning, CTCE, and hierarchical MARL; agents are assessed on performance, adaptability, and robustness against cyber threats.
- Phase B — Formal Verification: Pass the trained MARL agent, its environment, and the properties to be verified into a verification framework integrating reachability analysis (detecting unsafe/undesired states), model checking (temporal-logic safety/liveness across all execution paths), fuzz testing (fault tolerance/resilience to adversarial inputs), temporal logic (LTL/CTL for time-sensitive behaviours), theorem proving (mathematically grounded correctness guarantees), and abstract interpretation (higher-level static analysis, policy anomaly detection).
- Failure handling: When verification fails, a counterexample is generated for the violated property and processed by an LLM-based diagnostic interface that interprets the failure in natural language and suggests corrective actions, feeding a human-in-the-loop loop (retrain the policy, modify the environment, or refine specifications).
- Phase C — Reporting/interface: Integrate the verified agent and its FV report into a human-machine interface (powered by augmented/fine-tuned LLMs) so operators can interrogate and explore verification results, enhancing interpretability and trust.

## Theoretical Contributions
None / mostly conceptual. The paper is a thesis proposal / position paper presenting a hypothesis and methodology; no new theorems or proofs are provided (it cites existing FV approaches with correctness/convergence guarantees, such as ALMANAC).

## Experiments
- **Environment/Benchmark**: Not specified (proposed/planned). The paper states future implementation in simulated/emulated environments — Cyber Operations Research Gym (CybORG) and BRETAGNE — for MARL to defend critical military network infrastructure; no experiments are reported yet.
- **Baselines**: Not specified
- **Evaluation metrics**: Not specified (planned: performance, adaptability, robustness; FV outputs such as correctness proofs, counterexamples, coverage metrics)

## Key Results
- No empirical results reported; the paper is a thesis proposal outlining a hypothesis, problem definition (POMDP formulation), and three-phase methodology (training, formal verification, reporting).
- Provides a comparative analysis table (Table I) positioning the proposed approach against prior work along five axes (cybersecurity, hybrid AI, MARL, formal verification, user interface), arguing that no existing work covers all five — the gap this thesis addresses.

## Limitations & Future Work
- The framework is proposed but not yet implemented or empirically validated; results are entirely prospective.
- Stated future work: in the coming month, implement the described FV methods to improve the CTDE training process in a simulated/emulated environment (CybORG/BRETAGNE) for MARL defending critical military networks; prioritise FV approaches that deal with partial observability; make FV results (correctness proofs, counterexamples, coverage metrics) available to an LLM agent that optimises experiments and automatically adapts the training process; in the first year, refine the methodology to provide a foundation for the full verification framework.

## Relevance to Survey
This paper sits at the intersection of robust MARL and trustworthy/verifiable AI applied to a concrete safety-critical domain (autonomous cyber defence in military networks). It connects the robust MARL theme to Formal Verification (reachability analysis, model checking, temporal logic, theorem proving) and to robustness testing against state/observation perturbations on critical agents. It is a useful applied reference for the sub-themes of safety, fault tolerance, adversarial robustness, and partial observability in cooperative MARL, and for the emerging line that combines MARL with symbolic AI and LLMs for interpretability and human-in-the-loop trust.

## Related Work (verbatim excerpts from the paper)
> _[Section II, State of the Art]_

"Recent investigation has introduced ACD agents using DRL models trained and tested in gym environments [4], [5], [8]. For example, the study in [8] proposes a Reinforcement Learning (RL) model to compute an optimal defensive strategy for the single blue agent. The approach uses causal graphs to capture how actions influence the environment, combined with a search tree to predict and evaluate the agent's subsequent actions. This method ensures the intrinsic explicability of the agent, and also provides mathematical proofs of the optimality of the strategy and the convergence of the proposed algorithm. A hybrid ACD solution is presented in [4], combining DRL, rule-based systems and augmented LLMs. While FV is not explicitly addressed, the integration of LLMs enables the generation of human-readable explanations of agent behaviours and system states, significantly improving interpretability."

"The investigation in [6] extends this line of research by focusing on MARL within the proposed Building a Reproducible and Efficient Training AI Gym for Network Environments (BRETAGNE) environment. The study investigates the coordinated behaviour of multiple defender agents working together against dynamic threats. Although FV is not covered in this context, the use of LLM plays a key role in increasing the transparency of agent decision making. By combining MARL and LLMs, the approach aims to both improve the scalability of ACD systems and assist human experts in interpreting the actions."

"FV has long been a key component in software correctness assurance, particularly through techniques such as Bounded Model Checking (BMC). [9] introduced the Efficient SMT-based Bounded Model Checker (ESBMC)-Python, a BMC-based verifier specifically tailored for Python programs. This tool translates Python code into an intermediate representation suitable for Satisfiability Modulo Theories (SMT)-based analysis, allowing it to detect runtime errors and logical inconsistencies."

"Building on this foundation, [10] proposed a framework that combines BMC with LLMs to develop self-healing software. Their framework, ESBMC-AI, uses BMC to discover vulnerabilities and generate counterexamples, which are then passed to a LLM for automated repair suggestions. These repairs are then re-verified, creating a feedback loop that improves the robustness and security of the software."

"The scope of FV is expanding to include AI-based systems, in particular those incorporating neural networks. In this context, [11] has developed Verify AI (VERIFAI), a toolkit for the formal analysis of AI-driven systems. VERIFAI focuses on verifying system-level properties by exploring structured input spaces and monitoring the behaviour of neural networks under uncertainty."

"In the context of MARL, FV remains a significantly under-explored area, with only a limited number of approaches available to address the unique challenges posed by multi-agent systems. One notable contribution in this domain is the work by [12], who proposed a novel reachability analysis framework specifically tailored for MARL. Their approach formulates the reachability problem in MARL as a Mixed Integer Linear Program (MILP), enabling the verification of state specifications in multi-agent environments."

"The investigation reported in [13] focused on the robustness properties of a trained MARL system to adjust the trustworthiness of the model against unexpected perturbations in the input space. The framework called Robustness Testing for Critical Agents (RTCA) employs a Differential Evolution (DE)-based selection of critical agents in the system whose state perturbations would adversely affect the team's performance. Secondly, RTCA uses a team cooperation policy evaluation method as the objective function for DE optimisation."

"The investigation in [14] explored the verification of temporal logic specifications in MARL ensuring that the learned policies adhere to the desired temporal behaviours. The proposed Automaton/Logic Multi-Agent Natural Actor-Critic (ALMANAC) framework is accompanied by rigorous correctness and convergence guarantees. This ensures that the learned policies are both reliable and efficient. The experiments presented demonstrate the ability of the algorithm to guide MARL to satisfy complex temporal objectives in environments with probabilistic behaviours."

"While various approaches have explored the use of MARL and LLMs in the cybersecurity context, the integration of FV into these models remains underexplored. FV are well established in traditional software verification and have seen growing application to AI components such as neural networks. However, their use in the context of MARL remains limited. This work addresses this gap by proposing a framework that brings together FV, MARL and LLMs to enable both robust agent behaviour and improved interpretability in complex cyber environments."

### Cited references (resolved from the paper's bibliography)
- **[4]** J. Loevenich, E. Adler, T. Hürten, R. R. F. Lopes. *Design and evaluation of an Autonomous Cyber Defence agent using DRL and an augmented LLM.* Computer Networks, vol. 262, p. 111162, 2025.
- **[5]** M. Standen, D. Bowman, S. Hoang, T. Richer, M. Lucas, R. V. Tassel, P. Vu, M. Kiely, K. C., N. Konschnik, J. Collyer. *CybORG: Cyber Operations Research Gym.* 2022 (https://github.com/cage-challenge/CybORG).
- **[6]** Y. Gourlet, T. Lefeuvre, J. F. Loevenich, T. Hürten, F. Spelter, E. Adler, J. Braun, L. Moxon, R. R. F. Lopes. *BRETAGNE: Building a Reproducible and Efficient Training AI Gym for Network Environments.* MILCOM 2024.
- **[8]** K. Hammar, N. Dhir, R. Stadler. *Optimal Defender Strategies for CAGE-2 using Causal Modeling and Tree Search.* arXiv 2024.
- **[9]** B. Farias, R. Menezes, E. B. de Lima Filho, Y. Sun, L. C. Cordeiro. *Esbmc-python: A bounded model checker for python programs.* ISSTA 2024 (Proc. 33rd ACM SIGSOFT Int. Symp. on Software Testing and Analysis).
- **[10]** N. Tihanyi, R. Jain, Y. Charalambous, M. A. Ferrag, Y. Sun, L. C. Cordeiro. *A new era in software security: Towards self-healing software via large language models and formal verification.* arXiv 2024.
- **[11]** T. Dreossi, D. J. Fremont, S. Ghosh, E. Kim, H. Ravanbakhsh, M. Vazquez-Chanlatte, S. A. Seshia. *VerifAI: A toolkit for the design and analysis of artificial intelligence-based systems.* 2019.
- **[12]** X. Wang, J. Peng, S. Li, B. Li. *Formal Reachability Analysis for Multi-Agent Reinforcement Learning Systems.* IEEE Access, vol. 9, pp. 45812–45821, 2021.
- **[13]** Z. Zhou, G. Liu. *Robustness Testing for Multi-Agent Reinforcement Learning: State Perturbations on Critical Agents.* IOS Press, 2023, pp. 3131–3139.
- **[14]** L. Hammond, A. Abate, J. Gutierrez, M. Wooldridge. *Multi-Agent Reinforcement Learning with Temporal Logic Specifications.* arXiv 2021.
