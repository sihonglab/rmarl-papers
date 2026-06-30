# 154. A Robust and Constrained Multi-Agent Reinforcement Learning Electric Vehicle Rebalancing Method in AMoD Systems

## Metadata
- **Title**: A Robust and Constrained Multi-Agent Reinforcement Learning Electric Vehicle Rebalancing Method in AMoD Systems
- **Authors**: Sihong He, Yue Wang, Shuo Han, Shaofeng Zou, Fei Miao
- **Affiliation**: University of Connecticut (Computer Science and Engineering); University at Buffalo, SUNY (Electrical Engineering); University of Illinois, Chicago (Electrical and Computer Engineering)
- **Venue**: Not specified (arXiv:2209.08230v2, 27 Sep 2023)
- **Link/arXiv**: arXiv:2209.08230v2 [cs.MA]

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty — uncertainty in the state transition probability kernel (sim-to-real gap), modeled via a δ-contamination uncertainty set; combined with safety/fairness cost constraints
- **Method paradigm**: Robust + constrained MARL; worst-case (max-min) value over an uncertainty set; Lagrangian / primal-dual (gradient descent ascent); robust natural policy gradient (RNPG); CTDE actor-critic
- **Keywords**: Robust MARL, Constrained MARL, model uncertainty, EV rebalancing, AMoD, natural policy gradient, δ-contamination uncertainty set

## TL;DR
The paper is the first to formulate EV AMoD vehicle rebalancing as a robust and constrained MARL problem under state-transition-kernel uncertainty, and proposes ROCOMA — a CTDE algorithm using a newly developed robust natural policy gradient (RNPG) — to learn a rebalancing policy that maximizes worst-case reward while satisfying mobility/charging fairness constraints.

## Problem & Motivation
EVs are increasingly central to autonomous mobility-on-demand (AMoD) systems, but their unique charging patterns increase model uncertainty (e.g., in the state transition probability). Because there is usually a mismatch between the training (simulator) and test (real-world) environments, rebalancing policies computed on simulators can degrade significantly when deployed, and may violate operational constraints (e.g., fair mobility and charging service). Existing EV AMoD rebalancing literature has not explicitly considered model uncertainty in the state transition, and the coexistence of model uncertainty with constraints that decisions must satisfy makes the problem even harder. Robust constrained RL is already difficult even in tabular cases, and existing solutions cannot be directly applied due to the high-dimensional state/action spaces of transportation systems.

## Robustness Setting
- **Threat model / uncertainty set**: The transition kernel p is restricted to a δ-contamination uncertainty set P. With centroid kernel ˜p (from which training samples are generated), each conditional is P^a_s := {(1−δ)˜p^a_s + δq | q ∈ Δ(S)}, i.e., the state transition can be arbitrarily perturbed with small probability δ. Worst-case value functions are defined as v^π_r(s) = min_{p∈P} E_π[Σ γ^{t−1} r_t | s_1=s] (and analogously for cost v^π_c). Distribution-free worst-case modeling.
- **Setting**: Cooperative (region agents collaborate to maximize average team reward); centralized-training-decentralized-execution (CTDE); online / model-free policy-gradient training with constraints (constrained MARL).

## Method
- Formulates EV rebalancing as a robust and constrained MARL tuple G_rc = ⟨N, S, A, P, r, c, d, γ⟩, where the city is partitioned into N regions, each a "region agent" controlling vacant and low-battery EVs; reward is the negative total rebalancing distance, and a cost function c is the system fairness (weighted sum of charging fairness u_c and mobility fairness u_m).
- Goal: max_π E_{s∼ρ}[v^π_r(s)] subject to E_{s∼ρ}[v^π_c(s)] ≥ d. Reformulated via the Lagrangian into an equivalent max-min problem: max_θ min_{λ≥0} J(θ,λ) = v^{πθ}_r(ρ) + λ(v^{πθ}_c(ρ) − d).
- Proposes ROCOMA (Algorithm 1): adopts CTDE with centralized critics and decentralized actors; for the first time develops a robust natural policy gradient (RNPG) descent-ascent to update actor networks and the Lagrange multiplier in MARL.
- RNPG: the natural gradient ˜g* = F(θ)^{-1} ∇_θ v^π(s_1) (F is the Fisher information matrix) is obtained as the minimizer of a least-squares objective involving the policy score ψ_π(s,a)=∇log π(a|s,θ), the robust TD residual ϕ_π(τ) = r + γδ min_s v^π(s) + γ(1−δ)v^π(s') − v^π(s), and a bias term b_π; it is computed efficiently via stochastic gradient descent (Corollary 1).
- To handle high-dimensional state/action spaces, all agents share one policy π_θ and the joint score is decomposed as Σ_i ψ^θ_i(s,a) with ψ^θ_i(s,a) := π_{−i}(a_{−i}|s_{−i})∇π_i(a_i|s_i); policy networks output Dirichlet concentration parameters to satisfy the action simplex (sum-to-one) constraints. Parameters θ and λ are updated by Gradient Descent Ascent (GDA).

## Theoretical Contributions
- Proposition 1 (Robust Natural Policy Gradient): derives the RNPG ˜g* = F(θ)^{-1}∇_θ v^π(s_1) for robust and constrained MARL as the minimizer of a stated least-squares objective, with a full proof via the Fisher information matrix.
- Corollary 1: shows how to compute RNPG efficiently by SGD (initialize ˜g_0 = 0; average over W SGD iterations).
- (No convergence-rate / sample-complexity bound is stated; contributions are the gradient characterization plus the algorithm.)

## Experiments
- **Environment/Benchmark**: EV AMoD system simulator built from three real-world E-taxi data sets (E-taxi GPS data, transaction data, charging station data), used as both training and testing environment; the simulator parameters are modified so the testing environment differs from the training environment (e.g., the order generator parameters). The simulated map is a grid city.
- **Baselines**: No rebalancing (NO); MADDPG (state-of-the-art non-robust MARL); Constrained Optimization Policy (COP); Equally Distributed Policy (EDP); Randomly Distributed Policy (RDP); plus a Non-constrained MARL variant and a Non-robust MARL variant for ablation.
- **Evaluation metrics**: Rebalancing distance (lower better), system fairness (higher better), number of expired orders (lower better; orders canceled after waiting > 20 min), order response rate (higher better). Metrics computed over testing periods of 25 simulation steps; fairness constraint limit per testing period is −500; results averaged over 10 testing repetitions.

## Key Results
- Compared to a non-robust MARL method under model uncertainty, ROCOMA decreases the rebalancing distance and increases the system fairness by about 19.6% and 75.8%, respectively (Figure 3).
- Compared to no rebalancing (NO), ROCOMA decreases the number of expired orders by 98.4% and increases system fairness and order response rate by about 93.2% and 32.9%, respectively (Table I).
- Compared to a non-constrained MARL method, ROCOMA achieves 83.9% higher fairness with only 4% extra rebalancing distance (Table II), showing the value of the constrained design over reward-weighting.
- ROCOMA achieves higher system fairness and order response rate than EDP/RDP using less rebalancing distance; it takes slightly more distance than COP/MADDPG but yields better fairness and response rate, as those baselines ignore uncertainty.

## Limitations & Future Work
- Robustness is restricted to a δ-contamination transition-kernel uncertainty set with a small perturbation rate (δ = 0.05 in experiments); other uncertainty-set geometries are not studied.
- Evaluation is on a simulator built from real E-taxi data rather than real-world deployment; the "test" environment is a parameter-perturbed version of the same simulator.
- No convergence/sample-complexity guarantees are provided. (The paper does not explicitly list future-work directions.)

## Relevance to Survey
A domain-grounded instance of robust MARL that targets transition-kernel (model) uncertainty and combines it with constrained (safety/fairness) RL — sitting at the intersection of the "model/environment uncertainty" robustness line and the "constrained/safe MARL" line. Methodologically it contributes a robust natural policy gradient for constrained MARL and a worst-case (max-min) value formulation over a δ-contamination uncertainty set, connecting robust MDP / robust RL theory (Pinto et al.; Bagnell et al.) and the authors' related robust-MARL-with-state-uncertainty work to a large-scale transportation application.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work]_

"AMoD system vehicle rebalancing algorithms reallocate vacant vehicles, sometimes considering charging constraints. Heuristics lead to sub-optimal rebalancing solutions [12]. Other major categories of AMoD system rebalancing methods include optimization-based algorithms [13], Model Predictive Control (MPC) [14] and Reinforcement Learning (RL) [15]."

"Optimization and MPC-based approaches usually formulate the AMoD system vehicle rebalancing problem as an optimization problem, where the objective is to improve service quality [16], [17] or maximize the number of served passengers with fewer vehicles [10], [18], [19]. These model-based approaches usually rely on knowledge of the probability transition model of AMoD systems. Though robust and distributionally robust optimization-based methods have been designed to consider uncertainties caused by mobility demand, supply, or covariates predictions [4], [11], the probability transition error or uncertainty in system dynamics has not been addressed yet. Various RL-based methods include DQN, A2C and their variants [3], [20]–[22] have been proposed to solve the vehicle rebalancing problem. However, RL suffers from the sim-to-real gap; that is, the gap between the simulator and the real world often leads to unsuccessful implementation if the learned policy is not robust to model uncertainties [23]. None of the above RL-based rebalancing strategies consider this gap."

"Robust RL has been proposed to find a policy that maximizes the worst-case cumulative reward over an uncertainty set of MDPs [24]–[26]. To achieve a desired level of system fairness while minimizing rebalancing distance under model uncertainty, we put the fairness constraints in our RL formulation, which is known as Constrained RL that aims to find a policy that maximizes an objective function while satisfying certain cost constraints [27]. However, it remains challenging to design a robust EV rebalancing algorithm under model uncertainties and policy constraints, since the problem of robust constrained RL itself is already difficult to solve even in a simple tabular case. A robust and constrained RL for AMoD rebalancing cannot directly apply existing robust constrained RL solutions due to the high-dimensional state and action spaces commonly present in transportation systems. Our proposed robust and constrained MARL formulation and algorithm explicitly consider model uncertainties and policy constraints to learn robust rebalancing solutions for AMoD systems."

### Cited references (resolved from the paper's bibliography)
- **[3]** J. Wen, J. Zhao, P. Jaillet. *Rebalancing shared mobility-on-demand systems: A reinforcement learning approach.* IEEE ITSC 2017.
- **[4]** S. He, L. Pepin, G. Wang, D. Zhang, F. Miao. *Data-driven distributionally robust electric vehicle balancing for mobility-on-demand systems under demand and supply uncertainties.* IEEE/RSJ IROS 2020.
- **[10]** R. Zhang, F. Rossi, M. Pavone. *Model predictive control of autonomous mobility-on-demand systems.* IEEE ICRA 2016.
- **[11]** Z. Hao, L. He, Z. Hu, J. Jiang. *Robust vehicle pre-allocation with uncertain covariates.* Production and Operations Management 2020.
- **[12]** Z. Liu, T. Miwa, W. Zeng, M. G. Bell, T. Morikawa. *Dynamic shared autonomous taxi system considering on-time arrival reliability.* Transportation Research Part C 2019.
- **[13]** S. He, Z. Zhang, S. Han, L. Pepin, G. Wang, D. Zhang, J. A. Stankovic, F. Miao. *Data-driven distributionally robust electric vehicle balancing for autonomous mobility-on-demand systems under demand and supply uncertainties.* IEEE Transactions on Intelligent Transportation Systems 2023.
- **[14]** E. F. Camacho, C. B. Alba. *Model Predictive Control.* Springer 2013.
- **[15]** R. S. Sutton, A. G. Barto. *Reinforcement Learning: An Introduction.* MIT Press 2018.
- **[16]** J. Miller, J. P. How. *Predictive positioning and quality of service ridesharing for campus mobility on demand systems.* IEEE ICRA 2017.
- **[17]** J. Pfrommer, J. Warrington, G. Schildbach, M. Morari. *Dynamic vehicle redistribution and online price incentives in shared mobility systems.* IEEE Transactions on Intelligent Transportation Systems 2014.
- **[18]** A. Wallar, M. Van Der Zee, J. Alonso-Mora, D. Rus. *Vehicle rebalancing for mobility-on-demand systems with ride-sharing.* IEEE/RSJ IROS 2018.
- **[19]** R. Iglesias, F. Rossi, K. Wang, D. Hallac, J. Leskovec, M. Pavone. *Data-driven model predictive control of autonomous mobility-on-demand systems.* IEEE ICRA 2018.
- **[20]** J. Holler, R. Vuorio, Z. Qin, X. Tang, Y. Jiao, T. Jin, S. Singh, C. Wang, J. Ye. *Deep reinforcement learning for multi-driver vehicle dispatching and repositioning problem.* IEEE ICDM 2019.
- **[21]** K. Lin, R. Zhao, Z. Xu, J. Zhou. *Efficient large-scale fleet management via multi-agent deep reinforcement learning.* ACM SIGKDD 2018.
- **[22]** S. He, K. G. Shin. *Spatio-temporal capsule-based reinforcement learning for mobility-on-demand coordination.* IEEE Transactions on Knowledge and Data Engineering 2020.
- **[23]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML (PMLR) 2017.
- **[24]** J. A. Bagnell, A. Y. Ng, J. G. Schneider. *Solving uncertain Markov decision processes.* 2001.
- **[25]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research 2023.
- **[26]** S. Han, S. Su, S. He, S. Han, H. Yang, F. Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **[27]** Y. Wang, S. Zou. *Policy gradient method for robust reinforcement learning.* arXiv:2205.07344, 2022.
