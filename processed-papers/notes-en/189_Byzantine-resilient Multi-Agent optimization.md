# 189. Byzantine-Resilient Multiagent Optimization

## Metadata
- **Title**: Byzantine-Resilient Multiagent Optimization
- **Authors**: Lili Su, Nitin H. Vaidya
- **Affiliation**: Computer Science and Artificial Intelligence Laboratory, Massachusetts Institute of Technology (Lili Su); Department of Computer Science, Georgetown University (Nitin H. Vaidya)
- **Venue**: IEEE Transactions on Automatic Control, Vol. 66, No. 5, May 2021
- **Link/arXiv**: Full version available at https://sites.google.com/site/lilisuece/home/byzantine-resilient-multi-agent-optimization (DOI: 10.1109/TAC.2020.3008139)

## Taxonomy
- **Robustness / perturbation type targeted**: Byzantine faults / fault tolerance (an unknown subset of agents behave adversarially, can collude, and can send arbitrary, possibly inconsistent messages to different neighbors) in a decentralized multiagent optimization setting with no central coordinator
- **Method paradigm**: Byzantine-resilient (approximate) consensus combined with local gradient descent; trimming/filtering of received values (Trim removes the b largest and b smallest); projected gradient descent; provable robustness via graph-topological conditions (reduced graphs / source components)
- **Keywords**: Byzantine fault tolerance, distributed/multiagent optimization, approximate Byzantine consensus, gradient descent, (β, γ)-admissibility, directed networks

## TL;DR
The paper formulates Byzantine-resilient multiagent optimization without any central coordinator — where the goal is to minimize a convex combination of the good agents' local cost functions characterized by a new (β, γ)-admissibility metric — proves an impossibility result on the achievable γ, and gives a provably resilient algorithm (interleaving approximate Byzantine consensus with local gradient descent) whose guarantees are optimal (up to a factor 1/2 in β) for complete graphs.

## Problem & Motivation
Networked multiagent systems perform collaborative tasks where each agent holds a local cost function and the group aims to minimize a global objective aggregating these costs. The standard choice — the average of the local cost functions — is well-studied over adversary-free networks but is extremely vulnerable to Byzantine faults: the average can be completely controlled by even a single adversarial agent. Prior fault-tolerant work either assumed a central coordinator, restricted the fault model (e.g., broadcast-only adversaries), or did not characterize the structure of the convex coefficients of the achievable global objective. This work studies adversary-prone networks with no central coordinating agent under the canonical Byzantine fault model, and is the first to characterize the structure of the convex coefficients of achievable global objectives.

## Robustness Setting
- **Threat model / uncertainty set**: Byzantine fault model. A system adversary chooses an unknown subset A of agents (|A| ≤ b, n ≥ 3b+1) to compromise; the adversary has complete knowledge of the network (structure, local programs, current status, running history). Byzantine agents can collude and deviate arbitrarily from their programs, sending possibly inconsistent (differently valued) messages to different neighbors. The value of b is common knowledge to the good agents.
- **Setting**: Cooperative multiagent optimization; fully decentralized (no central coordinator), peer-to-peer over a directed communication graph G(V, E); synchronous iterative updates; deterministic (non-statistical) local cost functions. This is a distributed-optimization / control-theoretic robustness problem rather than an RL/MARL learning problem.

## Method
- Reformulates the objective: instead of minimizing the (manipulable) average, good agents aim to find x ∈ arg min over X of a convex combination Σ_{i∈V\A} α_i f_i(x), where the coefficients satisfy (β, γ)-admissibility: at least γ of the coefficients α_i are lower-bounded by β (so sufficiently many local functions meaningfully influence the decision).
- Each good agent runs a collaborative gradient-descent method (Algorithm 1) interleaving an approximate Byzantine consensus update with a local gradient step; agents exchange both local estimates and local gradients with neighbors.
- A Trim(·) function takes a multiset of size at least 2b+1 and removes the b largest and b smallest elements (breaking ties arbitrarily), filtering out potentially malicious extreme values; the estimate xᵢ is averaged from di−2b+1 trimmed elements (plus its own), while gᵢ is the average of the max and min of the trimmed gradients.
- The local estimate is updated by a projected gradient descent step xᵢ[t] ← P_X[xᵢ[t] − λ[t] gᵢ[t]], using diminishing stepsizes satisfying Σ λ[t] = ∞ and Σ λ²[t] < ∞.
- Provable resilience relies on a graph-topological condition (Assumption 1: every reduced graph — obtained by deleting Byzantine agents and up to b additional incoming edges per good agent — has a nonempty source component), which is necessary and sufficient for scalar Byzantine-resilient consensus.

## Theoretical Contributions
- **Impossibility result (Theorem 1)**: No algorithm can guarantee (β, γ)-admissibility with γ > |V\A| − b (i.e., > n − φ − b), for any β > 0, where φ is the actual number of Byzantine agents and b the maximum.
- **Convergence guarantee (Theorem 3, main result)**: Under Assumption 1, with γ ≜ min_{i∈V\A}(dᵢ+1−φᵢ−b) and β ≜ min{ 1 / (2 max_{i∈V\A}(dᵢ+1−φᵢ−b)), 1/(n−φ) }, the good agents' estimates converge: lim_{t→∞} Dist(xᵢ[t], X(β, γ)) = 0.
- **Optimality for complete graphs**: For a complete graph, Algorithm 1 guarantees β = 1/(2(n−φ−b)) and γ = n−φ−b, matching the impossibility bound on γ and matching the optimal β up to a multiplicative factor of 1/2.
- Supporting results: asymptotic consensus among good agents (Lemma 2, Corollary 1) via backward products of row-stochastic matrices M[t] ≥ ξ H[t]; bounded projection error (Proposition 1); convergence of the auxiliary trapped sequence to X(β, γ) (Lemma 4); convexity/closedness of X(β, γ) (Lemma 1).

## Experiments
- **Environment/Benchmark**: Not specified (this is a theoretical paper; no empirical experiments are reported — only illustrative analytical examples such as the n=4 scalar Example 1 and the vector state-estimation Example 2).
- **Baselines**: Not specified
- **Evaluation metrics**: Not specified

## Key Results
- The chosen global objective must exclude the average (1/n Σ fᵢ), since a single Byzantine agent can control it; restricting the summation to good agents and lower-bounding γ coefficients yields a robust objective.
- It is impossible to guarantee more than |V\A| − b entries of the coefficient vector α to be non-zero (Theorem 1), establishing a fundamental limit.
- The proposed Algorithm 1 provably converges to the valid-objective set X(β, γ) under Assumption 1 (Theorem 3), and for complete graphs achieves the impossibility-implied optimality (exactly in γ, within a factor 1/2 in β).

## Limitations & Future Work
- Restricted to scalar local cost functions; extension to general (multidimensional) local cost functions is left as an important future direction (attempts noted in [6]).
- Relies on Assumption 1; investigating minimal graph conditions and the trade-off between (β, γ)-admissibility and graph structure is open.
- Only asymptotic convergence is established; a finite-time convergence rate is of high practical interest.
- The algorithm exchanges both local estimates and local gradients for ease of analysis; whether gradient exchange can be relaxed (and quantifying its benefit) is open.

## Relevance to Survey
This work sits on the Byzantine / fault-tolerance line of robust multiagent learning and optimization, addressing decentralized cooperative settings where an adversarial subset of agents can behave arbitrarily. While framed in distributed-optimization and control theory rather than (MA)RL, its robustness-to-arbitrary-adversarial-agents threat model, its trimming-based resilient aggregation, and its graph-topological resilience conditions connect directly to Byzantine-robust distributed learning, fault-tolerant cooperative MARL, and robust consensus themes that the survey covers. It provides foundational impossibility limits and optimal achievability results that later robust/fault-tolerant decentralized learning algorithms build upon.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — "Byzantine-Resilient Consensus"]_

"There is a significant body of work on Byzantine-resilient consensus [12]–[18]. Readers are referred to [12] for comprehensive survey. Next we give a brief review on this line of work.

The Byzantine fault-tolerance problem was first introduced in [19], and has been one of the most fundamental problems in distributed computing for decades. Fisher et al. [20] showed that the fault-tolerant consensus problem cannot be solved in an asynchronous system. As one way to circumvent this impossibility result, the notion of approximate consensus was introduced [13], which only requires that processes agree with each other approximately rather than exactly in finite time. Reaching approximate consensus is of interest in synchronous systems as well [13]–[15]. The discussion in this article applies to synchronous systems.

For undirected networks, approximate consensus can be achieved if and only if the network connectivity is at least 2b + 1 and n > 3b [21]; recall that b is the maximum number of Byzantine faults. For directed networks, a sufficient and necessary condition on the network structures was characterized in [22]. There has been increasing interest in designing iterative approximate Byzantine consensus algorithms wherein only local communication is allowed [14], [15], [23], [24]. In particular, [24] studied the convergence rate over complete networks, and [14], [15] considered arbitrary directed networks and derived necessary and sufficient topological conditions. Recently, Byzantine consensus subject to differential privacy requirements was considered in [25].

All the above works focus on scalar inputs. Multidimensional inputs have been studied recently [17], [26], [27]. Complete graphs were considered in [26], [27], where tight conditions on the number of agents were identified. Incomplete graphs were studied in [17].

Our article is most relevant to the line of work on approximate synchronous Byzantine consensus over arbitrary graphs [14], [15]. In our article, in each iteration, each good agent combines an approximate Byzantine consensus update with its local gradient descent update. Intuitively speaking, an approximate consensus update is used as a mechanism for each of the good agents to "robustly collect" information from others in the presence of Byzantine agents. This is in contrast to the exact Byzantine consensus protocols that are involved in Blockchains wherein exact Byzantine consensus is used as a "selection mechanism" to determine among the multiple blocks proposed which one should be appended to the blockchain."

> _[Section II, Related Work — "Distributed Optimization"]_

"Our article goes beyond Byzantine consensus in that the local inputs are functions, and the goal is to reach an agreement on a value that is a minimizer of some weighted average of these local cost functions.

Distributed optimization has a long history. The seminal works [28], [29] considered separable global objectives for which the local decision variables at different agents are allowed to be different. Nedic and Ozdaglar [1] studied the setting wherein the global objective is the average of these local cost functions, and the local variables at the agents are required to reach consensus asymptotically. Many follow-up works are inspired (see [30], [31] for comprehensive surveys). Nevertheless, little attention has been paid to adversary-prone networks.

Multiagent optimization over adversary-prone networks, to the best of our knowledge, was first considered by Sundaram and Gharesifard [5] and our technical reports [9]–[11], [32] with different fault models and global objectives. In contrast to the Byzantine fault model which assumes that a bad agent can send differently valued messages to different neighbors, in [5], an adversarial agent is only allowed to send identically valued (broadcast) messages. This difference is significant as in complete graphs; for the faults in [5], there exists a consensus algorithm that can tolerate less than 1/2 of the agents to be faulty; in contrast, it is well known that no consensus algorithms can tolerate more than 1/3 agents to be Byzantine [33]. It might be enough to consider the fault model in [5] when the networked agents communicate with each other via wireless communication. In fact, the more structure on the adversarial behaviors, the easier to secure multiagent optimization. Additionally, [5] considered the family of global objectives in the form of convex combinations of the local cost functions at the good agents, and no additional structures on the convex coefficients are required. Consequently, the local estimates at the good agent in [5] are only guaranteed to converge to a convex combination of the minima of those local functions. In contrast, in addition to being in the convex hull, we also characterize a structure of the convex coefficients."

> _[Section II, Related Work — "Byzantine-Tolerant Distributed Machine Learning"]_

"Another line of work that is relevant to the discussion of this article is Byzantine-tolerant distributed machine learning [34], [35]. The main difference between these papers and the problem considered here is that they considered the learning problem under a statistical learning framework. Specifically, they assumed that the training data is i.i.d. generated from a unknown distribution, and the learning goal there is to minimize the population loss, which is defined in a form of integration, where the integration is taken over the unknown underlying distribution."

### Cited references (resolved from the paper's bibliography)
- **[1]** A. Nedic, A. Ozdaglar. *Distributed subgradient methods for multi-agent optimization.* IEEE Trans. Autom. Control, 2009.
- **[5]** S. Sundaram, B. Gharesifard. *Distributed optimization under adversarial nodes.* IEEE Trans. Autom. Control, 2019.
- **[9]** L. Su, N. H. Vaidya. *Byzantine multi-agent optimization: Part I.* arXiv:1506.04681, 2015.
- **[10]** L. Su, N. H. Vaidya. *Fault-tolerant distributed optimization (Part IV): Constrained optimization with arbitrary directed networks.* arXiv:1511.01821, 2015.
- **[11]** L. Su, N. H. Vaidya. *Byzantine multi-agent optimization: Part III.* Univ. of Illinois at Urbana-Champaign, Tech. Rep., 2015.
- **[12]** R. Wattenhofer. *Blockchain Science: Distributed Ledger Technology.* Inverted Forest Publishing, 2019.
- **[13]** D. Dolev, N. A. Lynch, S. S. Pinter, E. W. Stark, W. E. Weihl. *Reaching approximate agreement in the presence of faults.* J. ACM, 1986.
- **[14]** H. J. LeBlanc, H. Zhang, S. Sundaram, X. Koutsoukos. *Consensus of multi-agent networks in the presence of adversaries using only local information.* Proc. 1st Int. Conf. High Confidence Netw. Syst., 2012.
- **[15]** N. H. Vaidya, L. Tseng, G. Liang. *Iterative approximate Byzantine consensus in arbitrary directed graphs.* Proc. ACM Symp. Princ. Distrib. Comput. (PODC), 2012.
- **[16]** R. Friedman, A. Mostefaoui, S. Rajsbaum, M. Raynal. *Asynchronous agreement and its relation with error-correcting codes.* IEEE Trans. Comput., 2007.
- **[17]** N. H. Vaidya. *Iterative Byzantine vector consensus in incomplete graphs.* Distrib. Comput. and Netw. (Springer), 2014.
- **[18]** L. Tseng, N. H. Vaidya. *Iterative approximate consensus in the presence of Byzantine link failures.* Networked Syst. (Springer), 2014.
- **[19]** M. Pease, R. Shostak, L. Lamport. *Reaching agreement in the presence of faults.* J. ACM, 1980.
- **[20]** M. J. Fischer, N. A. Lynch, M. S. Paterson. *Impossibility of distributed consensus with one faulty process.* J. ACM, 1985.
- **[21]** M. J. Fischer, N. A. Lynch, M. Merritt. *Easy impossibility proofs for distributed consensus problems.* Proc. 4th Annu. ACM Symp. Princ. Distrib. Comput. (PODC), 1985.
- **[22]** L. Tseng, N. H. Vaidya. *Fault-tolerant consensus in directed graphs.* Proc. ACM Symp. Princ. Distrib. Comput. (PODC), 2015.
- **[23]** N. H. Vaidya. *Matrix representation of iterative approximate Byzantine consensus in directed graphs.* arXiv:1203.1888, 2012.
- **[24]** A. D. Fekete. *Asymptotically optimal algorithms for approximate agreement.* Distrib. Comput., 1990.
- **[25]** D. Fiore, G. Russo. *Resilient consensus for multi-agent systems subject to differential privacy requirements.* Automatica, 2019.
- **[26]** H. Mendes, M. Herlihy. *Multidimensional approximate agreement in Byzantine asynchronous systems.* Proc. 45th Annu. ACM Symp. Theory Comput. (STOC), 2013.
- **[27]** N. H. Vaidya, V. K. Garg. *Byzantine vector consensus in complete graphs.* Proc. ACM Symp. Princ. Distrib. Comput. (PODC), 2013.
- **[28]** J. N. Tsitsiklis. *Problems in decentralized decision making and computation.* DTIC Document, Tech. Rep., 1984.
- **[29]** J. Tsitsiklis, D. Bertsekas, M. Athans. *Distributed asynchronous deterministic and stochastic gradient optimization algorithms.* IEEE Trans. Autom. Control, 1986.
- **[30]** S. Boyd et al. *Distributed optimization and statistical learning via the alternating direction method of multipliers.* Found. Trends Mach. Learn., 2011.
- **[31]** A. Nedic, J. Liu. *Distributed optimization for control.* Annu. Rev. Control Robot. Auton. Syst., 2018.
- **[32]** L. Su, N. H. Vaidya. *Byzantine multi-agent optimization: Part II.* arXiv:1507.01845, 2015.
- **[33]** L. Lamport, R. Shostak, M. Pease. *The Byzantine generals problem.* ACM Trans. Programm. Languages Syst., 1982.
- **[34]** Y. Chen, L. Su, J. Xu. *Distributed statistical machine learning in adversarial settings: Byzantine gradient descent.* Proc. ACM Meas. Anal. Comput. Syst. (POMACS), 2017.
- **[35]** D. Yin, Y. Chen, K. Ramchandran, P. Bartlett. *Byzantine-robust distributed learning: Towards optimal statistical rates.* Proc. 35th Int. Conf. Mach. Learn. (ICML), 2018.
