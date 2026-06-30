# 179. Distributed Resilience-Aware Control in Multi-Robot Networks

## Metadata
- **Title**: Distributed Resilience-Aware Control in Multi-Robot Networks
- **Authors**: Haejoon Lee, Dimitra Panagou
- **Affiliation**: Department of Robotics, University of Michigan, Ann Arbor; Department of Aerospace Engineering, University of Michigan, Ann Arbor
- **Venue**: Not specified (arXiv:2504.03120v3 [eess.SY], 10 Sep 2025)
- **Link/arXiv**: arXiv:2504.03120v3

## Taxonomy
- **Robustness / perturbation type targeted**: Misbehaving / malicious agents that share faulty or biased information (resilient consensus under an F-total attack); fault tolerance and Byzantine-style information attacks; safety constraints (inter-agent collision avoidance)
- **Method paradigm**: Control Barrier Functions (CBF) / CBF-based Quadratic Program; W-MSR (Weighted Mean-Subsequence-Reduced) resilient consensus; distributed/decentralized control; degree-based sufficient condition for network resilience; graph-theoretic robustness ((r,s)-robustness)
- **Keywords**: resilient consensus, multi-robot networks, Control Barrier Functions, W-MSR, malicious agents, distributed control

## TL;DR
The paper proposes a distributed CBF-based controller that lets each robot guarantee resilient consensus and collision avoidance during navigation without fixed topologies, by deriving a degree-based sufficient condition (normal agents keep at least F + ⌊n/2⌋ neighbors) that uses only locally available information instead of global state knowledge.

## Problem & Motivation
Consensus in multi-agent systems degrades when misbehaving agents share faulty/incorrect information, motivating resilient consensus (e.g., the W-MSR algorithm). However, W-MSR relies on combinatorial, globally-defined network resilience properties such as r-robustness and (r,s)-robustness that are hard to compute online. Prior control approaches either enforce fixed topologies with known resilience levels (impractical in dynamic/constrained environments) or maintain resilience without fixed topologies but require global state knowledge — which becomes unreliable when malicious agents share inaccurate state information. Existing CBF-based resilience controllers are centralized or assume each robot can accurately estimate the global state and control actions of all robots, and they often overlook inter-agent collisions. The paper aims to provide a fully distributed, locally-computable controller that guarantees resilient consensus and safety in time-varying networks.

## Robustness Setting
- **Threat model / uncertainty set**: F-total attack — at most F nodes in the graph are malicious. A malicious robot still transmits its connectivity level cᵢ and consensus state yᵢ but may deviate from the nominal update protocols. The main theoretical analysis assumes malicious robots conduct constant biased attacks on the connectivity value cᵢ(t) (cᵢ(t) = Σ aᵢⱼ + εᵢ), i.e., stealthy understating/overstating of connectivity, and assumes (Assumption 1) malicious robots follow the same physical control laws as normal robots and do not cause physical disruptions (e.g., collisions).
- **Setting**: cooperative multi-robot consensus with adversarial/malicious agents; fully distributed (decentralized) control using only local neighbor information; online control of physical states (continuous-time single-integrator dynamics) with discrete-time information sharing. Not an RL method (control-theoretic).

## Method
- Establishes a degree-based sufficient condition (Proposition 1): under an F-total attack, if the minimum degree of normal agents δ_L(G(t)) ≥ F′ = F + ⌊n/2⌋ for all t, normal agents achieve resilient consensus via W-MSR; this leverages Lemma 1 ([21, Property 5.23]) linking minimum degree to (r,s)-robustness, but relaxes the dependence to the connectivity of normal agents only.
- Defines a degree-maintenance constraint function hᵢ(x) = Σ_{j∈Nᵢ} aᵢⱼ(x) − F′ using a smooth weighted-adjacency approximation aᵢⱼ(x), plus a collision-avoidance constraint h_ij^col(x) = ∆ᵢⱼ(x)² − ∆_d².
- Composes all constraints into one centralized candidate CBF ϕ(x,w) = 1 − Σ Eᵢ(x) − Σ E_ij^c(x) (with Eᵢ = e^{−w_r hᵢ}, E_ij^c = e^{−w_c h_ij^col}); its CBF constraint (12) is centralized and needs global state/dynamics.
- Decomposes (12) into n separate distributed constraints (15), each using only local information; because robots may not know neighbors' true degrees, each robot uses ĥ_k(t) = c_k(t) − F′ built from shared connectivity levels. Lemma 3 proves the distributed constraints are feasible and that all robots satisfying (15) collectively satisfy (12).
- Constructs a CBF-QP controller (20): each robot solves arg min ‖u_{i,des} − uᵢ‖² subject to (15). Theorem 1 proves that under constant biased attacks on cᵢ this guarantees (a) δ_L(G(t)) ≥ F′, (b) no collisions, and (c) resilient consensus; Corollary 1 covers the nominal-update case where δ_min(G(t)) ≥ F′ holds for all agents.

## Theoretical Contributions
- **Proposition 1**: sufficient condition for resilient consensus in time-varying discrete-time W-MSR networks based solely on the minimum degree of normal agents (δ_L ≥ F + ⌊n/2⌋), contrasted with [7] which gives a similar bound for all agents in continuous-time dynamics.
- **Lemma 2**: choice of adjacency parameter q₁ = 2 + ε (0 < ε < 1/(n−1)) ensures hᵢ(x) ≥ 0 only if δᵢ(G(t)) ≥ F′.
- **Lemma 3**: feasibility of the distributed CBF constraints (15) and equivalence to the centralized constraint (12).
- **Theorem 1 & Corollary 1**: forward invariance of the safe set under the proposed distributed CBF-QP controller, guaranteeing degree maintenance, collision-free motion, and resilient consensus under the specified malicious-attack model.

## Experiments
- **Environment/Benchmark**: Simulations in a 2D plane with a time-varying network of n = 11 robots (single-integrator dynamics), communication range R = 3 m, minimum separation ∆_d = 0.3 m, F = 2 malicious robots, F′ = 2 + ⌊11/2⌋ = 7 required neighbors; desired controllers drive robots in four diverging directions to stress connectivity.
- **Baselines**: Not specified (no comparison against other controllers; three internal scenarios — nominal updating, understating, overstating of connectivity by malicious robots — are compared).
- **Evaluation metrics**: Whether normal robots maintain ≥ 7 neighbors, collision avoidance, evolution of the degree constraint function (9), and convergence of consensus states yᵢ(t).

## Key Results
- In all three malicious-update scenarios, robots stop dispersing so that normal robots maintain at least seven neighbors while avoiding collisions, validating Theorem 1 and Corollary 1.
- Malicious behavior affects network shape: understating connectivity forces normal robots to stay closer (more compact network), while overstating relaxes constraints (more dispersed network); one malicious robot fails to maintain seven neighbors under overstating.
- Despite these variations in connectivity updates, resilient consensus on yᵢ(t) is achieved in all scenarios, demonstrating the controller's effectiveness.

## Limitations & Future Work
- Considers only informational attacks where malicious robots disrupt consensus through information; joint physical and informational attacks are left as future work (Assumption 1).
- Theoretical guarantees assume constant biased attacks on cᵢ(t); extending the analysis to broader/varied attack strategies is future work (Remark 3).
- Analysis assumes continuous (real-time, τ₁ → 0) connectivity information sharing, whereas real systems use discrete updates; addressing discrete updates and more varied threats is future work.
- Performance (overall connectivity) depends on malicious robots' behavior; relies on CBF-QP local-Lipschitz-continuity assumptions (Assumption 2).

## Relevance to Survey
This is a control-theoretic (CBF) paper rather than an RL/MARL paper, but it is directly relevant to the robust-MARL survey's fault-tolerance / Byzantine-resilience and communication-robustness themes: it addresses multi-agent robustness to malicious agents that share faulty information, formalized via the F-total threat model and W-MSR resilient consensus. It connects the graph-theoretic resilience line ((r,s)-robustness, resilient consensus) with safety-constrained distributed control, complementing learning-based robust MARL approaches that handle adversarial agents and communication attacks, and offering a certified, guarantee-driven alternative to empirical robustness.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction]_

"The consensus problem in multi-agent systems finds numerous applications from control to optimization [1], [2]. However, the performance of consensus in general degrades in the presence of misbehaving agents that share faulty or incorrect information. Resilient consensus has therefore been extensively studied [3]–[7]. In particular, the Weighted Mean-Subsequence-Reduced (W-MSR) algorithm was introduced in [3] to guarantee consensus among non-misbehaving or normal agents despite the presence of misbehaving agents."

"The challenge of using W-MSR algorithm lies in its reliance on complex global topological network resilience properties, such as r-robustness and (r, s)-robustness [3]. These properties are inherently combinatorial, making them difficult to compute online [8]. Moreover, in many multi-robot applications, links between robots are formed if their relative distances are within a threshold, which further complicates the practical implementation of these network properties in real-time operation."

"To implement these network properties, [9], [10] enforce local inter-robot connectivity by maintaining predetermined topologies with known resilience levels. This approach eliminates the need for continuous resilience computation. However, its limitation is that the imposed connectivity constraints induce fixed topologies, making it impractical in dynamic or constrained environments where robots need flexible movements. There is earlier work considering the maintenance of network resilience without relying on fixed topologies [9], [11]–[15], but these resilience-aware approaches rely on global state knowledge (i.e., states of all robots). To obtain global state knowledge, each robot needs to accurately estimate it based on the information from its neighbor robots, which becomes challenging as information being shared is unreliable in adversarial settings."

"In this paper, we focus on the design of distributed controllers based on Control Barrier Functions (CBFs) [16], where each robot computes its control inputs using locally-available information only, so that it maintains a resilient structure and ensures resilient consensus without fixed topologies. The problem of developing CBF-based controllers for improving or maintaining resilience of multi-robot networks without relying on fixed network topologies has been studied in [11], [13]–[15]. However, these approaches take a centralized CBF form, or assume that each robot can accurately estimate the global state knowledge and the control actions of all other robots at every time instant. These assumptions are unrealistic in complex and adversarial networks, and difficult to resolve due to the global nature of the resilience properties."

"In contrast to earlier work [11]–[14], our approach (a) focuses on local connectivity of normal agents rather than enforcing global resilience properties, (b) eliminates reliance on potentially unreliable global state estimation, and (c) explicitly accounts for inter-agent collisions, which is overlooked in previous CBF-based approaches [11], [13], [14], [17]–[19]."

### Cited references (resolved from the paper's bibliography)
- **[1]** H. Zhu, J. Juhl, L. Ferranti, J. Alonso-Mora. *Distributed multi-robot formation splitting and merging in dynamic environments.* ICRA 2019.
- **[2]** X. Tan, D. V. Dimarogonas. *Distributed implementation of control barrier functions for multi-agent systems.* IEEE Control Systems Letters 2022.
- **[3]** H. J. LeBlanc, H. Zhang, X. Koutsoukos, S. Sundaram. *Resilient asymptotic consensus in robust networks.* IEEE Journal on Selected Areas in Communications 2013.
- **[4]** Y. Wang, H. Ishii, F. Bonnet, X. Défago. *Resilient real-valued consensus in spite of mobile malicious agents on directed graphs.* IEEE Transactions on Parallel and Distributed Systems 2022.
- **[5]** H. Lee, D. Panagou. *Construction of the sparsest maximally r-robust graphs.* IEEE 63rd Conference on Decision and Control (CDC) 2024.
- **[6]** H. Lee, D. Panagou. *Minimal construction of graphs with maximum robustness.* arXiv:2507.00415, 2025.
- **[7]** H. J. LeBlanc, X. D. Koutsoukos. *Low complexity resilient consensus in networked multi-agent systems with adversaries.* 15th ACM International Conference on Hybrid Systems: Computation and Control (HSCC) 2012.
- **[8]** H. Zhang, E. Fata, S. Sundaram. *A notion of robustness in complex networks.* IEEE Transactions on Control of Network Systems 2015.
- **[9]** D. Saldaña, A. Prorok, S. Sundaram, M. F. M. Campos, V. Kumar. *Resilient consensus for time-varying networks of dynamic agents.* American Control Conference (ACC) 2017.
- **[10]** J. Usevitch, D. Panagou. *Resilient leader-follower consensus to arbitrary reference values in time-varying graphs.* IEEE Transactions on Automatic Control 2020.
- **[11]** L. Guerrero-Bonilla, V. Kumar. *Realization of r-robust formations in the plane using control barrier functions.* IEEE Control Systems Letters 2020.
- **[12]** K. Saulnier, D. Saldaña, A. Prorok, G. J. Pappas, V. Kumar. *Resilient flocking for mobile robot teams.* IEEE Robotics and Automation Letters 2017.
- **[13]** M. Cavorsi, B. Capelli, S. Gil. *Multi-robot adversarial resilience using control barrier functions.* Robotics: Science and Systems (RSS) 2022.
- **[14]** Z. Zhang, Y. Wu, J. Jiang, N. Zheng, W. Meng. *Realization of robust formation for multi-UAV systems using control barrier functions.* Unmanned Systems 2024.
- **[15]** H. Lee, D. Panagou. *Maintaining strong r-robustness in reconfigurable multi-robot networks using control barrier functions.* IEEE International Conference on Robotics and Automation (ICRA) 2025.
- **[16]** A. Ames, S. D. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, P. Tabuada. *Control barrier functions: Theory and applications.* 18th European Control Conference (ECC) 2019.
- **[17]** P. Bhatia, S. B. Roy, P. Sujit, L. M. Alvarez, A. McFadyen. *Decentralized connectivity maintenance for multi-agent systems using control barrier functions.* International Conference on Unmanned Aircraft Systems (ICUAS) 2024.
- **[18]** N. De Carli, P. Salaris, P. R. Giordano. *Distributed control barrier functions for global connectivity maintenance.* IEEE International Conference on Robotics and Automation (ICRA) 2024.
- **[19]** B. Capelli, L. Sabattini. *Connectivity maintenance: Global and optimized approach through control barrier functions.* IEEE International Conference on Robotics and Automation (ICRA) 2020.
