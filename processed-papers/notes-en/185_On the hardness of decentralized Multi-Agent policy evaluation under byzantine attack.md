# 185. On the Hardness of Decentralized Multi-Agent Policy Evaluation under Byzantine Attacks

## Metadata
- **Title**: On the Hardness of Decentralized Multi-Agent Policy Evaluation under Byzantine Attacks
- **Authors**: Hairi, Minghong Fang (co-primary), Zifan Zhang, Alvaro Velasquez, Jia Liu
- **Affiliation**: University of Wisconsin-Whitewater (CS); University of Louisville (CSE); North Carolina State University (CS); University of Colorado, Boulder (CS); The Ohio State University (ECE)
- **Venue**: IFIP 2024 (ISBN 978-3-903176-65-2; published via IEEE Xplore)
- **Link/arXiv**: arXiv:2409.12882 (online companion, ref [15])

## Taxonomy
- **Robustness / perturbation type targeted**: Byzantine/fault tolerance — up to f faulty agents under a model poisoning attack, which can send arbitrary and inconsistent information to neighbors during communication in a fully decentralized network.
- **Method paradigm**: Impossibility/hardness theory; Byzantine-tolerant decentralized temporal-difference (TD) learning; f-trimmed-mean robust aggregation; decentralized consensus.
- **Keywords**: Multi-agent policy evaluation, Byzantine attack, Temporal difference learning, model poisoning, decentralized consensus, f-trimmed mean

## TL;DR
The paper proves that fully decentralized multi-agent policy evaluation under Byzantine model poisoning cannot recover the uniform-average value function of the normal agents, and that no correct algorithm can guarantee more than |N|−f positive weights even in a relaxed weighted-average formulation; it then proposes a Byzantine-tolerant decentralized TD (BDTD) algorithm using f-trimmed mean that guarantees asymptotic consensus among normal agents under scalar linear function approximation.

## Problem & Motivation
Policy evaluation is a core subproblem of cooperative MARL (the critic step in actor-critic). In a fully decentralized setting agents exchange parameters over a communication network to reach consensus on value functions modeled as the uniform average of agents' rewards. When up to f > 0 agents are Byzantine and perform model poisoning, they can send arbitrary — and crucially inconsistent — information to different neighbors, which is harder than the centralized server setting where a Byzantine agent sends only a single value. Existing MARL literature lacks a comprehensive study of robust designs in heterogeneous-reward settings; the closest prior work implicitly assumes homogeneous rewards. The paper asks whether the ideal uniform-average value function is even learnable under Byzantine faults, and characterizes the fundamental limits.

## Robustness Setting
- **Threat model / uncertainty set**: Up to f Byzantine agents (set F, actual count q = |F| can be smaller than f). Byzantine agents follow the true sampling policy and receive true environment data, but during communication they may send arbitrary (denoted ∗) and inconsistent parameters to different neighbors (local model poisoning, not data poisoning). The standard resilience condition n ≥ 3f + 1 is assumed. Agents are connected through a complete graph (the most ideal setting, used to strengthen the impossibility results); the impossibility results also hold for general graphs.
- **Setting**: cooperative; fully decentralized; online (decentralized TD learning over a networked multi-agent MDP). Heterogeneous local rewards.

## Method
- Formalizes the networked multi-agent MDP and a Byzantine variant, then frames a hierarchy of policy-evaluation targets: the uniform-average normal-agent value (Problem 2), a weighted-average normal-agent value (Problem 3), and a (ν, ξ)-admissible relaxation (Problem 4) requiring at least ν weights bounded away from zero by ξ.
- Proves impossibility results (Theorems 1 and 2) by contradiction via indistinguishable executions, where a Byzantine agent behaving like the correct algorithm forces normal agents to converge to two distinct fixed points.
- Proposes BDTD: each iteration normal agents send their parameter w^i_k to neighbors, perform a consensus update via the f-Trimmed Mean subroutine (sort received values, drop the largest f and smallest f, average the remaining n−2f), then perform a projected TD(0) step w^i_{k+1} ← Π_{2,R}(w̃^i_k + η_k δ^i_k ϕ(s_k)) with TD error δ^i_k = r^i_{k+1} + γϕ^T(s_{k+1})w^i_k − ϕ^T(s_k)w^i_k.
- Uses scalar (dimension d = 1) linear function approximation for the algorithm; diminishing step sizes satisfying Σ η_t = ∞, Σ η_t² < ∞ (e.g., η_t = 1/t); a projection radius R = 2r_max / (ϕ_min(1−γ)^{3/2}) for theoretical bounding (may be dropped in practice).

## Theoretical Contributions
- **Theorem 1**: When f > 0, evaluating the uniform-average normal-agent value function (Problem 2) is not solvable — no correct algorithm can reach the corresponding TD fixed point w*_N.
- **Theorem 2**: For any ξ > 0, the (ν, ξ)-admissible Problem 4 is not solvable for any ν > |N|−f; thus a (|N|−f, ξ)-admissible solution is the best achievable. Equivalently, no correct algorithm guarantees more than |N|−f positive weights in the relaxed weighted-average problem.
- **Theorem 3**: BDTD (Algorithm 2) achieves asymptotic consensus among normal agents, i.e., lim_{t→∞} |w^i_t − w̄_t| = 0 for all i ∈ N, even under heterogeneous rewards and inconsistent Byzantine faults (though the average parameter w̄_t itself may not converge depending on problem heterogeneity).
- Proofs are inspired by [32] but differ in two ways: convergence is for stochastic (expected mean-square) terms rather than deterministic terms, and the impossibility holds for general multi-agent policy evaluation (tabular and linear approximation), not just the scalar case.

## Experiments
- **Environment/Benchmark**: Cooperative navigation task "Simple Spread" from the Multi-Particle Environment (MPE) [24]; 10 agents covering all landmarks, with 2 malicious (Byzantine) agents; feature dimension 40; step-size 0.1; uniformly random policy; Intel Core i9-12900K CPU; each experiment repeated 10 times (variances small, omitted).
- **Baselines**: FedAvg [25], Krum [3], Coordinate-wise median (Median) [44], FLTrust [4], SCCLIP [18].
- **Evaluation metrics**: Mean squared Bellman error (MSBE) and consensus error (CE); smaller is better. Tested under Gaussian attack [3], Krum attack [11], and Trim attack [11].

## Key Results
- BDTD overall achieves the best performance across the various attack scenarios; even under the strong Trim attack its MSBE is comparable to FedAvg without any attacks.
- Existing Byzantine-robust aggregation rules (e.g., Krum, SCCLIP) are susceptible to poisoning; FLTrust is vulnerable to both Gaussian and Krum attacks (final MSBE of FLTrust is 0.801 under the Gaussian attack).
- Under the Krum attack, FLTrust has low MSBE but large CE (lack of consensus). The Krum aggregation rule keeps CE small under all three attacks but its MSBE becomes large, indicating normal agents reach a poor consensus.

## Limitations & Future Work
- The proposed BDTD algorithm and its consensus guarantee (Theorem 3) are derived only under scalar (d = 1) linear function approximation; extension to vector/general features is left open.
- The average parameter w̄_t may not have a limit depending on problem heterogeneity, so consensus does not imply convergence to a specific value function.
- TD(0) is used for simplicity; extension to TD(λ) with λ ∈ (0, 1] is stated to be straightforward but not carried out.
- Only model poisoning (not data poisoning) is considered. (No explicit future-work section beyond these remarks.)

## Relevance to Survey
This paper sits on the Byzantine/fault-tolerance line of robust MARL, specifically the robustness of the policy-evaluation (critic) subproblem in fully decentralized cooperative MARL. It contributes fundamental hardness/impossibility results that bound what any robust decentralized algorithm can achieve under heterogeneous rewards, complementing constructive Byzantine-resilient designs. It bridges Byzantine-robust distributed/federated learning (Krum, trimmed mean, FLTrust, clipping) with decentralized TD learning and Byzantine consensus theory, connecting robust MARL to the broader fault-tolerant distributed optimization and federated RL literature.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — A. Fault-free policy evaluation]_

"Policy evaluation, which aims to evaluate how good a given policy is, is an important sub-problem in designing a complete RL algorithm, which can be incorporated into the actor-critic framework as the critic step. Temporal difference (TD) learning [33] is a simple yet effective learning algorithm first proposed in the single-agent setting to evaluate a given policy. The convergence theory in TD learning has been developed first in asymptotic regime [36], [37] and then in finite-time horizon [2], [29], [43]."

"The multi-agent policy evaluation, based on distributed TD learning, has been recently studied [8], [9], [41]. Various aspects of fully-decentralized MARL algorithms have been studied. Notably, the sample and communication efficiencies of actor-critic algorithms have been investigated in [7], [16], [17], [23]."

> _[Section II, Related Work — B. Distributed Learning with Byzantine Agents]_

"Byzantine agents with local model poisoning attack is a common modeling for robust design of distributed algorithm design. A large body of papers [3], [6], [11], [12], [18], [21], [22], [42], [44] in the literature have adopted it as a common failure model in federated learning problem, where a server is involved to facilitate the collaborative learning process within the supervised setting. In robust algorithm design, one feature that is different from fault-free counterpart is to design robust filtering mechanism. For instance, in the Krum aggregation rule, as described by [3], the server receives local models from agents and selects one received local model that has the smallest distance to its subset of neighbors as the output. In [4], a key system assumption is that the server holds a trusted dataset. The server maintains a server model based on the current global model and its trusted dataset. Upon receiving one local model from any agent, the server considers this received local model as benign if it is positive related to the server model."

"Recently work in [5], [10] studied the effect of Byzantine agents in the so-called federated reinforcement learning (FRL) framework, where a central server is assumed to be present. However, we note that FRL and MARL differ significantly in that FRL is a multiple independent identical learner and the action from one agent does not affect the outcomes of other agents. In contrast, the global state transition and local rewards are dependent upon joint actions in MARL. In [5], the results are further extended the results to the offline setting. The closest related work [41] studied the policy value evaluation in the presence of Byzantine agents for a given policy. However, the analysis implicitly assumes the setting of homogeneous rewards, i.e. the rewards for all agents are the same. In our work, we consider a more general heterogeneous reward setting. The offline competitive MARL has been studied in [40], where the data poisoning fault model is considered. Specifically, the rewards in the offline data are adversarially changed so that the new Nash equilibrium learned from the poisoned data is significantly different from the Nash equilibrium learned from the original data."

"There are a series of works [30]–[32] on decentralized optimization problems where the local objective functions are heterogeneous and convex. An important subproblem in both our work and work in decentralized optimization [30]–[32] is decentralized consensus, meaning all agents are required to agree with each other. Existing work in [38], [39] have focused on these fundamental problems and proposed f-trimmed-mean-based algorithms. A recent paper [13] has investigated on the topic of Byzantine-robust decentralized federated learning."

### Cited references (resolved from the paper's bibliography)
- **[2]** Bhandari, Russo, Singal. *A finite time analysis of temporal difference learning with linear function approximation.* COLT (PMLR) 2018.
- **[3]** Blanchard, El Mhamdi, Guerraoui, Stainer. *Machine learning with adversaries: Byzantine tolerant gradient descent.* NeurIPS 2017.
- **[4]** Cao, Fang, Liu, Gong. *FLTrust: Byzantine-robust federated learning via trust bootstrapping.* NDSS 2021.
- **[5]** Chen, Zhang, Zhang, Wang, Zhu. *Byzantine-robust online and offline distributed reinforcement learning.* AISTATS 2023.
- **[6]** Chen, Su, Xu. *Distributed statistical machine learning in adversarial settings: Byzantine gradient descent.* POMACS 2017.
- **[7]** Chen, Zhou, Chen, Zou. *Sample and communication-efficient decentralized actor-critic algorithms with finite-time analysis.* arXiv:2109.03699, 2021.
- **[8]** Doan, Maguluri, Romberg. *Finite-time analysis of distributed TD(0) with linear function approximation on multi-agent reinforcement learning.* ICML 2019.
- **[9]** Doan, Maguluri, Romberg. *Finite-time performance of distributed temporal-difference learning with linear function approximation.* SIAM Journal on Mathematics of Data Science 2021.
- **[10]** Fan, Ma, Dai, Jing, Tan, Low. *Fault-tolerant federated reinforcement learning with theoretical guarantee.* NeurIPS 2021.
- **[11]** Fang, Cao, Jia, Gong. *Local model poisoning attacks to Byzantine-robust federated learning.* USENIX Security Symposium 2020.
- **[12]** Fang, Liu, Gong, Bentley. *AFLGuard: Byzantine-robust asynchronous federated learning.* ACSAC 2022.
- **[13]** Fang, Zhang, Hairi, Khanduri, Liu, Lu, Liu, Gong. *Byzantine-robust decentralized federated learning.* CCS 2024.
- **[16]** Hairi, Zhang, Liu. *Sample and communication efficient fully decentralized MARL policy evaluation via a new approach: Local TD update.* AAMAS 2024.
- **[17]** Hairi, Liu, Lu. *Finite-time convergence and sample complexity of multi-agent actor-critic reinforcement learning with average reward.* ICLR 2022.
- **[18]** He, Karimireddy, Jaggi. *Byzantine-robust decentralized learning via self-centered clipping.* arXiv:2202.01545, 2022.
- **[21]** Karimireddy, He, Jaggi. *Learning from history for Byzantine robust optimization.* ICML 2021.
- **[22]** Karimireddy, He, Jaggi. *Byzantine-robust learning on heterogeneous datasets via bucketing.* ICLR 2022.
- **[23]** Liu, Wei, Ying. *Scalable and sample efficient distributed policy gradient algorithms in multi-agent networked systems.* arXiv:2212.06357, 2022.
- **[29]** Srikant, Ying. *Finite-time error bounds for linear stochastic approximation and TD learning.* COLT 2019.
- **[30]** Su, Vaidya. *Byzantine multi-agent optimization: Part I.* arXiv:1506.04681, 2015.
- **[31]** Su, Vaidya. *Fault-tolerant multi-agent optimization: Part III.* arXiv:1509.01864, 2015.
- **[32]** Su, Vaidya. *Fault-tolerant multi-agent optimization: Optimal iterative distributed algorithms.* PODC 2016.
- **[33]** Sutton. *Learning to predict by the methods of temporal differences.* Machine Learning 1988.
- **[36]** Tsitsiklis, Van Roy. *Average cost temporal-difference learning.* Automatica 1999.
- **[37]** Tsitsiklis, Van Roy. *On average versus discounted reward temporal-difference learning.* Machine Learning 2002.
- **[38]** Vaidya. *Matrix representation of iterative approximate Byzantine consensus in directed graphs.* arXiv:1203.1888, 2012.
- **[39]** Vaidya, Tseng, Liang. *Iterative approximate Byzantine consensus in arbitrary directed graphs.* PODC 2012.
- **[40]** Wu, McMahan, Zhu, Xie. *Reward poisoning attacks on offline multi-agent reinforcement learning.* arXiv:2206.01888, 2022.
- **[41]** Wu, Shen, Chen, Ling. *Byzantine-resilient decentralized policy evaluation with linear function approximation.* IEEE Transactions on Signal Processing 2021.
- **[42]** Xie, Koyejo, Gupta. *Generalized Byzantine-tolerant SGD.* arXiv:1802.10116, 2018.
- **[43]** Xu, Wang, Liang. *Improving sample complexity bounds for (natural) actor-critic algorithms.* arXiv:2004.12956, 2020.
- **[44]** Yin, Chen, Kannan, Bartlett. *Byzantine-robust distributed learning: Towards optimal statistical rates.* ICML 2018.
