# 15. Multi-agent Policy Evaluation via Primal-dual Online Time-averaging

## Metadata
- **Title**: Multi-agent Policy Evaluation via Primal-dual Online Time-averaging
- **Authors**: Gang Chen, Changli Pu, Yaoyao Zhou
- **Affiliation**: School of Automation, Chongqing University, Chongqing, 400044, China
- **Venue**: Preprint submitted to Journal of Parallel and Distributed Computing, 2023 (not peer reviewed; SSRN preprint)
- **Link/arXiv**: https://ssrn.com/abstract=4564190

## Taxonomy
- **Robustness / perturbation type targeted**: External/environmental noise on estimations (e.g., Gaussian noise) and communication uncertainty (time-varying, jointly connected, directed communication networks). Robustness here means improving estimation robustness against ubiquitous noise and unreliable/changing inter-agent communication, not adversarial or model-uncertainty robustness.
- **Method paradigm**: Distributed policy evaluation; MSPBE minimization reformulated as a primal-dual saddle-point problem via Fenchel duality; primal-dual online time-averaging; distributed (consensus) optimization over time-varying jointly connected digraphs; Laplacian averaging.
- **Keywords**: Reinforcement learning, distributed policy evaluation, distributed optimization, multi-agent systems, primal-dual, online time-averaging, MSPBE

## TL;DR
The paper proposes a distributed multi-agent policy-evaluation algorithm that reformulates the MSPBE minimization as a primal-dual saddle-point problem and solves it with primal-dual online time-averaging over time-varying, jointly connected directed graphs, proving sublinear convergence and showing improved robustness to external noise and communication uncertainty.

## Problem & Motivation
The paper addresses distributed policy evaluation in cooperative MARL for two cases: (1) parallel computing, where a group of agents jointly learn the value function of a given joint policy (global state common, local rewards differ), and (2) distributed exploring, where the state space is partitioned into subspaces and each agent evaluates a common policy in its own subspace. Using a central controller to aggregate local rewards is expensive to maintain after attack/failure, cannot protect privacy, and some agents will not share local information for security/privacy reasons; hence a fully distributed framework is preferred. Prior distributed schemes mostly assume undirected, fixed topologies, but in practice communication can be one-directional (privacy) and time-varying (uncertain environment), and online estimation is affected by ubiquitous noise. The paper aims to improve estimation robustness on both fronts.

## Robustness Setting
- **Threat model / uncertainty set**: No explicit adversary or uncertainty set. "Uncertainty" enters through (i) external noise added to estimations (experiments inject Gaussian noise (1/√(2πσ))exp[−(x−µ)²/2σ²]) and (ii) the communication network being time-varying and possibly disconnected at some instants, modeled as a sequence of uniformly jointly strongly connected, weight-balanced digraphs (Assumption 1, with integer B>0 over which the union graph is strongly connected). Online time-averaging is designed to reduce the effects of noise on policy estimation.
- **Setting**: Cooperative (goal: maximize the sum / average of agents' local rewards); fully decentralized / distributed (no central controller); online learning. Policy evaluation only (fixed given policy), not policy improvement.

## Method
- Formulate policy evaluation as minimizing the mean squared projected Bellman error (MSPBE) with an ℓ₂ regularizer; rewrite it in weighted least-squares form J(θ) = ½‖Aθ − b‖²_{C⁻¹} + ½ρ‖θ‖², with A, b, C as expectations over the stationary distribution and estimated by finite sample averages (M samples).
- Apply Fenchel duality to introduce a dual variable ω and turn the (empirical) MSPBE into a saddle-point (max over ω) objective; because rewards are private, each agent forms its own empirical EM-MSPBE Jᵢ(θᵢ, ωᵢ) (parallel-computing case shares Â, Ĉ; distributed-exploring case uses agent-specific Âᵢ, Ĉᵢ).
- Cast the two cases into a consensus form: minimize (1/N)Σᵢ Jᵢ(θᵢ) subject to θ₁ = ··· = θ_N, then its primal-dual version with both θ and ω consensus constraints.
- Algorithm 1 (primal-dual online time-averaging): each agent updates primal/dual variables with a consensus (Laplacian) term using stepsize σ and a gradient step with learning rate η_t, then maintains running time-averages θᵃ and ωᵃ (θᵃ_{t+1} = ((t−1)/t)θᵃ_t + (1/t)θ_t, similarly for ω). The time-averaged iterates are the reported estimates and are smoother under noise.
- Analysis uses the state-transition matrix φ(t,l) of the time-varying graph and a Laplacian-averaging bound (Lemma 1) to prove consensus and convergence.

## Theoretical Contributions
- Consensus guarantee (Theorem 1): for η_t = ε/T^△ (0.5 < △ < 1) or η_t = ε/√t, the consensus constraints on primal and dual variables are satisfied as T → ∞.
- Cumulative primal/dual evaluation-error bounds (Lemmas 3–5) leading to saddle-point convergence.
- Convergence rate (Theorem 2): under constant learning rate η = ε/T^△, Algorithm 1 achieves convergence rate O(1/T^{1−△}).
- Convergence rate (Theorem 3): under time-varying learning rate η_t = ε/√t, Algorithm 1 achieves convergence rate O(1/√t).
- Results hold over general time-varying, jointly connected digraphs, more general than prior undirected-graph-based algorithms.

## Experiments
- **Environment/Benchmark**: (1) Parallel-computing policy evaluation on the Mountain Car task (SARSA used to learn the policy; reward −1 per step until the top; six agents; global state, local rewards as random proportions averaging to R^π_c; γ = 0.9, d = 16, ρ = 0.2; feature φ(s) = 2exp(‖s−c‖²/b²); communication sequence G_t = {G₁, G₂}, B = 2). (2) Distributed exploring on a 9×6 grid partitioned into six 3×3 grids with six robots (actions up/down/left/right; six-dimensional feature; time-varying network as in Fig.1).
- **Baselines**: Inexact ADMM [18] (on an undirected cycle graph, parameters c = 1.5, µ = 7.5); comparison of constant vs. time-varying learning rates within Algorithm 1; comparison across different communication graphs (including fully connected) in the exploring experiment.
- **Evaluation metrics**: Consensus convergence of θᵃ_i; MSPBE / primal-dual estimation error J convergence; convergence speed; accuracy level (up to 1% error); noise-immunity of the time-averaged θᵃ; computational complexity comparison vs. ADMM.

## Key Results
- Both learning-rate schedules converge under time-varying, jointly connected topologies, matching the theoretical rates O(1/T^{1−△}) and O(1/√t); the time-varying rate converges faster than the constant rate, and larger gain ε or k yields faster convergence (Figs.3–4).
- Algorithm 1 reaches the same accuracy level (up to 1% error) as inexact ADMM [18], but ADMM requires inverting the estimate C in (5), so Algorithm 1 has lower computational complexity (Fig.5).
- Under injected Gaussian noise, raw θ keeps fluctuating while the time-average θᵃ stays smooth and converges to the optimal solution, demonstrating the noise-reduction/robustness benefit of online time-averaging (Fig.6).
- In distributed exploring, errors under different graphs converge to the same accuracy (up to 1% error); the fully connected graph converges slowly early on due to heavy information exchange, while fewer information exchanges save communication resources and reduce information loss (Figs.8–9).

## Limitations & Future Work
- Scope is limited to policy evaluation of a fixed given policy (no policy improvement/control). Not specified beyond this.
- Restricted to linear function approximation and to weight-balanced, uniformly jointly strongly connected digraphs (Assumption 1).
- Experiments use small-scale settings (six agents; simplified 3×3 grids), and the paper notes the grid could be divided more delicately in practice.
- No explicit future-work section is given. Not specified.

## Relevance to Survey
This paper sits on the periphery of the robust MARL landscape: it does not address adversarial perturbations, model uncertainty, or distributionally robust formulations, but rather "robustness" in the sense of resilience to external estimation noise and to uncertain/time-varying communication topologies in fully decentralized MARL. It connects to the communication-robustness / fault-tolerance and distributed-optimization themes (avoiding a single central controller that is vulnerable to attack/failure, tolerating intermittently disconnected and directed networks). It is most relevant as a robust distributed policy-evaluation building block, linking the primal-dual saddle-point reformulation line (Fenchel-dual MSPBE, double averaging) with online time-averaging and consensus over jointly connected graphs.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"One direct way to solve the policy evaluation problem of collaborative MARL is to utilize a central controller, which could collect the local reward information of all agents and calculate the estimated policy value. In this way, we can utilize the traditional single-agent reinforcement learning scheme. However, the use of the central controller may face a lot of problems. For example, it is too expensive to maintain after the attack or failure and cannot protect privacy. In some scenarios, some agents do not share local information for security and privacy reasons. Therefore, another solution is to utilize a fully distributed control framework in which the agent shares local information with its neighbors through the communication network, and the decision-making process is determined by the state of the agent itself and the information received. It is like applying parallel ideas to deal with big data problems [9, 10]. Motivated by the pioneering work of [11, 12, 13], we mainly focus on the distributed policy evaluation problem of MARL."

> _[Introduction]_

"The development of MARL can be traced back to Littman's pioneering work on the Markov game [14]. Most of the early works are based on the tabular setting, which may face the curse of dimensionality. To solve this problem, a group of agents is used to learn the approximate value function of the centralized reward under a given policy, and a distributed gradient temporal-difference (GTD) method is proposed in [15]. The work [16] studied two fully decentralized actor-critic algorithms to solve the problem of linear function approximation in policy evaluation, which could tackle large-scale MARL problems. In [17], a variance-reduced method based on the eligibility traces is presented. Different from the gradient-based methods in policy evaluation problems, a distributed alternating directions method of multipliers (ADMM) algorithm is proposed in [18]. Some works use deep neural networks to approximate the value functions [19]. By the primal-dual reformulation of policy evaluation in reinforcement learning, some centralized algorithms are investigated, such as GTD2 [20], PDBG and SVAG [13]. The work [11] uses Fenchel duality to transform the minimized mean square Bellman error (MSPBE) into a kind of distributed saddle-point problem. By using the proposed double averaging algorithm, a fully distributed MARL setting is realized."

> _[Introduction]_

"Most of the existing works are feasible under the framework of undirected and fixed topologies [11, 17, 18]. Due to the actual privacy consideration, an agent may broadcast its local information to another agent, but the receiver may be unwilling to transmit the local information back to the previous agent. Moreover, in the uncertain environment, the communication network may be time-varying. Therefore, to tackle this problem, we mainly focus on a sequence of time-varying and jointly connected digraphs in this paper. Motivated by the Laplacian averaging [21], we combine the MARL with primal-dual running-time averaging in the process of policy evaluation."

> _[Introduction]_

"Our algorithm is feasible under this general situation and thus the result is more general as compared with the existing algorithms based on undirected graphs [11, 17, 18]. Moreover, our analysis method is different from the existing works [11, 17, 18, 22, 23]. In fact, considering the primal-dual optimization and online time-averaging, the analyses become more challenging. Motivated by the running time-average analyses [21], we shed some light on its application in the online learning."

### Cited references (resolved from the paper's bibliography)
- **[9]** Nakib, Souquet, Talbi. *Parallel fractal decomposition based algorithm for big continuous optimization problems.* Journal of Parallel and Distributed Computing 2019.
- **[10]** Gu, Qi, Wu, Wang, Xu, Yuan, Huang. *Sparkdq: Efficient generic big data quality management on distributed data-parallel computation.* Journal of Parallel and Distributed Computing 2021.
- **[11]** Wai, Yang, Wang, Hong. *Multi-agent reinforcement learning via double averaging primal-dual optimization.* NeurIPS 2018.
- **[12]** Valcarcel Macua, Chen, Zazo, Sayed. *Distributed policy evaluation under multiple behavior strategies.* IEEE Transactions on Automatic Control 2015.
- **[13]** Du, Chen, Li, Xiao, Zhou. *Stochastic variance reduction methods for policy evaluation.* ICML 2017.
- **[14]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994.
- **[15]** Lee, Yoon, Hovakimyan. *Primal-dual algorithm for distributed reinforcement learning: Distributed GTD.* IEEE CDC 2018.
- **[16]** Zhang, Yang, Liu, Zhang, Başar. *Fully decentralized multi-agent reinforcement learning with networked agents.* ICML 2018.
- **[17]** Cassano, Yuan, Sayed. *Multiagent fully decentralized value function learning with linear convergence rates.* IEEE Transactions on Automatic Control 2021.
- **[18]** Zhao, Yi, Li. *Distributed policy evaluation via inexact ADMM in multi-agent reinforcement learning.* Control Theory and Technology 2020.
- **[19]** Omidshafiei, Pazis, Amato, How, Vian. *Deep decentralized multi-task multi-agent reinforcement learning under partial observability.* ICML 2017.
- **[20]** Sutton, Maei, Precup, Bhatnagar, Silver, Szepesvári, Wiewiora. *Fast gradient-descent methods for temporal-difference learning with linear function approximation.* ICML 2009.
- **[21]** Mateos-Núñez, Cortés. *Distributed saddle-point subgradient algorithms with Laplacian averaging.* IEEE Transactions on Automatic Control 2017.
- **[22]** Sha, Zhang, You, Zhang, Başar. *Fully asynchronous policy evaluation in distributed reinforcement learning over networks.* Automatica 2022.
- **[23]** Ren, Haupt, Guo. *Communication-efficient hierarchical distributed optimization for multi-agent policy evaluation.* Journal of Computational Science 2021.
