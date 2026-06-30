# 181. Distributed robust optimization for multi-agent systems with guaranteed finite-time convergence

## Metadata
- **Title**: Distributed robust optimization for multi-agent systems with guaranteed finite-time convergence
- **Authors**: Xunhao Wu, Jun Fu
- **Affiliation**: State Key Laboratory of Synthetical Automation for Process Industries, Northeastern University, Shenyang 110819, China
- **Venue**: Not specified (Preprint submitted to Automatica; arXiv:2309.01201v1 [math.OC], 3 Sep 2023)
- **Link/arXiv**: arXiv:2309.01201v1

## Taxonomy
- **Robustness / perturbation type targeted**: Bounded (set-based) uncertainty in the local objective functions and constraints of agents (measurement/estimation and implementation errors); worst-case robust convex optimization with semi-infinite constraints. This is a distributed optimization/control formulation, not adversarial/RL robustness.
- **Method paradigm**: Distributed robust convex optimization (DRCO); right-hand-side restriction approach; cutting-surface / discretization-based outer-and-inner approximation (lower-bounding and upper-bounding procedures); finite-time consensus-based termination. Not an RL / minimax-game method.
- **Keywords**: Distributed robust convex optimization, Bounded uncertainty, Uniformly strongly connected network, Finite-time convergence, Semi-infinite constraints

## TL;DR
The paper proposes a distributed algorithm that, under the weakest network assumption (uniformly strong connectivity over time-varying unbalanced digraphs), drives all agents to finite-time converge to a feasible consensus solution of a distributed robust convex optimization problem (DRCO) with bounded uncertainty, satisfying global optimality to a guaranteed accuracy, by combining a lower-bounding (discretization) procedure, an upper-bounding (right-hand restriction) procedure, and two distributed termination methods.

## Problem & Motivation
In real-world multi-agent systems, each agent's local data (objective and constraint parameters) is uncertain due to measurement/estimation and implementation errors, so optimizing with nominal data is unsafe. The authors target the distributed robust convex optimization problem (DRCO) with bounded uncertainty. Prior constrained distributed optimization algorithms mostly require undirected/weight-balanced networks and assume exact data; existing DRCO methods either are confined to special constraint structures, cannot guarantee local feasibility for all agents, only converge probabilistically (scenario-based), or only converge asymptotically. The only prior finite-time method (the authors' own cutting-surface work [19]) satisfies only zero-order optimality and gives no specific global-optimality accuracy guarantee. The gap addressed is a distributed algorithm achieving finite-time convergence, local feasibility, and a certified global-optimality accuracy under uniformly strong connectivity.

## Robustness Setting
- **Threat model / uncertainty set**: Uncertain parameters δᵢ ∈ Δᵢ (local objective) and γᵢ ∈ Γᵢ (constraints) lie in non-empty compact sets; the robust optimum minimizes the global objective under the worst-case uncertainty (δᵢ = argmax fᵢ). After epigraphic reformulation the uncertainty is confined to the constraints, giving a semi-infinite constraint gᵢ(x, yᵢ) ≤ 0 for all yᵢ ∈ Yᵢ (Yᵢ compact). No probabilistic/distributional assumptions; pure set-membership bounded uncertainty.
- **Setting**: cooperative distributed optimization (agents minimize a common/global objective over a shared decision vector by consensus); fully decentralized over time-varying, possibly unbalanced directed graphs satisfying uniformly strong connectivity; no central coordinator; iterative/online updates with finite-time termination.

## Method
- Reformulate the DRCO into a standard form via epigraphic reformulation so uncertainty appears only in semi-infinite constraints; assume strict convexity (unique optimum), an interior point (Assumption 3), and finite-time consensus solvers (Assumption 4).
- **Distributed lower-bounding procedure**: discretize each compact uncertainty set Yᵢ into a finite set ỹᵏᵢ, yielding a relaxation (DLBDk) whose feasible set contains Xᵢ; iteratively populate the maximum-violation point ŷᵢ = argmax gᵢ(xᵏ⁺¹ᵢ, yᵢ) (via a lower-level problem / LLP oracle) so that ∑fᵢ(x̃ᵏ⁺¹ᵢ) gives a non-decreasing lower bound that converges up to F*.
- **Distributed upper-bounding procedure**: tighten constraints by a positive right-hand restriction parameter εᵏᵢ on a finite uncertainty subset Ȳᵏᵢ (DUBDk), which is in general neither a relaxation nor a restriction; iteratively shrink εᵏᵢ ← εᵏᵢ/r and add violation points, producing an upper bound ∑fᵢ(xᵏ⁺¹ᵢ) ≥ F* and a locally feasible solution within finite iterations.
- **Two distributed termination methods**: adapt the minimum-consensus / finite-time consensus algorithm of [48] so all agents stop simultaneously when the gap between upper and lower bounds reaches accuracy ϵf. Method I checks |fᵢ(xᵏ⁺¹ᵢ) − fᵢ(x̃ᵏ⁺¹ᵢ)| ≤ ϵf per agent (accuracy ẽϵf = mϵf); Method II checks a neighbor-sum criterion and solves a linear program for a tighter, graph-dependent accuracy ϵf ≤ mϵf. Agents exchange only two-bit data [hᵢ(t), cᵢ(t)].

## Theoretical Contributions
- Convergence of the lower-bounding procedure: ∑fᵢ(x̃ᵏ⁺¹ᵢ) → F* with ∑fᵢ(x̃ᵏ⁺¹ᵢ) ≤ F* for all k (Lemma 2, Proposition 1).
- Convergence of the upper-bounding procedure: ∑fᵢ(zᵏ⁺¹ᵢ) → F*, plus finite-iteration local feasibility (Lemma 3, Propositions 2–3).
- Finite-time termination guarantees: Proposition 4/5 show the consensus-tracking variables reach the stopping criterion within T(m−1)+1 time slots.
- Theorem 1: Algorithm 1 with Method I terminates finitely and yields a feasible ẽϵf-approximate optimal consensus solution with ẽϵf = mϵf.
- Theorem 2: with known graph sequence, Method II yields a feasible ϵf-approximate solution where ϵf is the optimum of an explicit linear program and ϵf ≤ mϵf (less conservative).

## Experiments
- **Environment/Benchmark**: A numerical case study — a 6-agent distributed robust convex optimization problem with quadratic local objectives ‖x − uᵢ‖² and concave semi-infinite constraints gᵢ(x, yᵢ) = (x(1) − vᵢ)² + 2yᵢx(2) − yᵢ² − 1 ≤ 0, yᵢ ∈ [−1, 1], x ∈ R². Three network types: directed cycle graph, customized graph, complete graph. Implemented in MATLAB R2018b on an Intel Core i7-7700HQ.
- **Baselines**: Related distributed (robust) optimization algorithms — distributed cutting-plane consensus [5,6], distributed cutting-surface consensus [19], and distributed cutting-plane primal-dual algorithm [49] — compared qualitatively/graphically; also comparison of the paper's own Method I vs Method II (and a centralized reference).
- **Evaluation metrics**: Number of iterations to terminate; per-agent local feasibility; achieved global objective value vs the true optimum F* ≈ 38.687746; approximate-optimality accuracy (ϵf, ẽϵf, ̂ϵf) as a function of number of agents and graph structure.

## Key Results
- Algorithm 1 converges to the global optimal value within a finite number of iterations, with the upper/lower bounding procedures serving as upper and lower bounds of F*; the optimal point matches x* = [0, √7/4]ᵀ, F* ≈ 38.687746.
- All agents obtain locally feasible solutions across all three graph types; objective values are within the guaranteed accuracy of F* (e.g., bounds around 38.67–38.70).
- Method II is less conservative than Method I (ϵf ≤ mϵf) but its accuracy depends on the graph (complete graph ≈ centralized accuracy; directed cycle graph lowest), and it requires more iterations than Method I.

## Limitations & Future Work
- Finite-time convergence is proved, but the convergence rate is not analyzed (left to future thorough theoretical/computational analysis).
- Assumes a strictly convex global objective and fully continuous decision variables; extensions to nonconvex local cost functions or (mixed-)integer decision variables are future work.
- Requires globally solving lower-level problems (LLP); for nonconvex LLP only indirect methods (discretization, αBB) are available; Method II additionally requires a known graph sequence; numerical study is small-scale (6 agents).

## Relevance to Survey
This paper is on the optimization/control side of "robustness" rather than reinforcement learning: it addresses set-based bounded uncertainty in distributed multi-agent convex optimization via worst-case (robust optimization) formulations and certified finite-time consensus, not adversarial agents, robust MDPs, or robust MARL. It is tangential to robust MARL but connects to the broader theme of robustness to model/parameter uncertainty in multi-agent systems and to distributed/decentralized multi-agent solution methods over communication networks (relevant to communication-constrained and consensus-based MARL). It can serve as a control-theory reference point for "bounded-uncertainty robustness" and finite-time guarantees rather than as a core robust-MARL method.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"On the constrained distributed optimization, there are a considerable number of algorithms have been proposed, e.g., [1, 12, 13, 22, 27, 34, 46, 47]. However, to the best of our knowledge, most of the existing constrained distributed optimization algorithms can only be applied to bi-directional (or undirected) and weight-balanced communication networks, except for literature [46,47] which can be used to time-varying unbalanced directed graphs under the assumption of uniformly strong connectivity. Furthermore, these algorithms were designed for the case where the local data of all agents are completely accurate. However, these data of real-world optimization problems tend to be uncertain as a result of measurement/estimation errors and implementation errors [2]. Hence, the main focus of this article is to solve a distributed robust convex optimization problem (DRCO) with bounded uncertainty under the weakest assumption of network communication: uniformly strong connectivity [6]."

> _[Introduction]_

"Recently, some distributed algorithms for dealing with the DRCO were developed in [5,6,8,10,11,16,25,26,30,42,49,50,54], which can be categorized into four groups according to the treatment of uncertainty. Firstly, inspired by the robust counterpart approach in [2], some algorithms were proposed in [42,50], which make all the agents asymptotically converge to a feasible optimal solution of the DRCO by transforming the DRCO into a robust counterpart problem and then doing parallel computation with a constrained distributed optimization algorithm. However, these algorithms are confined to special constraint structures. Secondly, in [25, 26], some random projection algorithms were designed that almost surely converge to a feasible optimal solution of the DRCO, yet the local feasibility of the solutions of all the agents cannot be guaranteed. Thirdly, some scenario-based algorithms were developed in [8,10,11,16,30,54] by sampling a large number of scenarios from the uncertainty set to approximate the DRCO, which asymptotically converge to a probabilistically feasible approximate optimal solution. However, these algorithms can not converge to the feasible optimal solution of the DRCO. Fourthly, some most relevant algorithms to our article were presented in [5,6,19,49]. These algorithms are based on iteratively approximating the DRCO by populating the cutting-planes/cutting-surfaces into the existing finite sets of constraints. The algorithms given in [5,6,49] asymptotically converge to a feasible optimal solution, while the algorithm in [19] enables all agents to finite-time converge to feasible and approximately optimal solutions. With the exception of [19], to our best knowledge, none of the existing algorithms can guarantee the finite-time convergence and local feasibility of the solutions for all agents. However, the solutions in [19] only satisfy the zero-order optimality conditions and cannot provide specific accuracy assurance of global optimality. Therefore, the motivation of this article is to propose a novel distributed algorithm for locating a feasible consensus solution satisfying global optimality to a certain accuracy of the DRCO under a uniformly strongly connected network within a finite number of iterations."

### Cited references (resolved from the paper's bibliography)
- **[1]** Bastianello, Schenato, Carli. *A novel bound on the convergence rate of ADMM for distributed optimization.* Automatica 2022.
- **[2]** Ben-Tal, Ghaoui, Nemirovski. *Robust optimization.* Princeton University Press 2009.
- **[5]** Bürger, Notarstefano, Allgöwer. *Distributed robust optimization via cutting-plane consensus.* Proc. 51st IEEE Conference on Decision and Control 2012.
- **[6]** Bürger, Notarstefano, Allgöwer. *A polyhedral approximation framework for convex and robust distributed optimization.* IEEE Transactions on Automatic Control 2014.
- **[8]** Carlone, Srivastava, Bullo, Calafiore. *Distributed random convex programming via constraints consensus.* SIAM Journal on Control and Optimization 2014.
- **[10]** Chamanbaz, Notarstefano, Bouffanais. *Randomized constraints consensus for distributed robust linear programming.* IFAC-PapersOnLine 2017.
- **[11]** Chamanbaz, Notarstefano, Bouffanais. *A randomized distributed ellipsoid algorithm for uncertain feasibility problems.* Proc. IEEE 56th Annual Conference on Decision and Control 2017.
- **[12]** Chen, Yang, Song, Lewis. *A distributed continuous-time algorithm for nonsmooth constrained optimization.* IEEE Transactions on Automatic Control 2020.
- **[13]** Chen, Yang, Song, Lewis. *Fixed-time projection algorithm for distributed constrained optimization on time-varying digraphs.* IEEE Transactions on Automatic Control 2021.
- **[16]** Falsone, Margellos, Prandini, Garatti. *A scenario-based approach to multi-agent optimization with distributed information.* IFAC-PapersOnLine 2020.
- **[19]** Fu, Wu. *A cutting-surface consensus approach for distributed robust optimization of multi-agent systems.* Submitted to IEEE Transactions on Automatic Control 2023.
- **[22]** Hamedani, Aybat. *Multi-agent constrained optimization of a strongly convex function over time-varying directed networks.* Proc. 55th Annual Allerton Conference on Communication, Control, Computing 2017.
- **[25]** Lee, Nedić. *Distributed random projection algorithm for convex optimization.* IEEE Journal of Selected Topics in Signal Processing 2013.
- **[26]** Lee, Nedić. *Asynchronous gossip-based random projection algorithms over networks.* IEEE Transactions on Automatic Control 2016.
- **[27]** Lin, Xu, Ren, Yang, Gui. *Angle-based analysis approach for distributed constrained optimization.* IEEE Transactions on Automatic Control 2021.
- **[30]** Margellos, Falsone, Garatti, Prandini. *Distributed constrained optimization and consensus in uncertain networks via proximal minimization.* IEEE Transactions on Automatic Control 2018.
- **[34]** Nedić, Ozdaglar, Parrilo. *Constrained consensus and optimization in multi-agent networks.* IEEE Transactions on Automatic Control 2010.
- **[42]** Wang, Li. *Distributed robust optimization in networked system.* IEEE Transactions on Cybernetics 2017.
- **[46]** Xie, You, Song, Wu. *Distributed random-fixed projected algorithm for constrained optimization over digraphs.* IFAC-PapersOnLine 2017.
- **[47]** Xie, You, Tempo, Song, Wu. *Distributed convex optimization with inequality constraints over time-varying unbalanced digraphs.* IEEE Transactions on Automatic Control 2018.
- **[49]** Yang, Huang, Wu, Wang, Chiang. *Distributed robust optimization (DRO), part I: framework and example.* Optimization and Engineering 2014.
- **[50]** Yang, Wu, Huang, Wang, Verdú. *Distributed robust optimization for communication networks.* Proc. IEEE INFOCOM 2008.
- **[54]** You, Tempo, Xie. *Distributed algorithms for robust convex optimization via the scenario approach.* IEEE Transactions on Automatic Control 2019.
