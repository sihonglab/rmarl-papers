# 193. Resilient Distributed Optimization for Multi-Agent Cyberphysical Systems

## Metadata
- **Title**: Resilient Distributed Optimization for Multi-Agent Cyberphysical Systems
- **Authors**: Michal Yemini, Angelia Nedić, Andrea J. Goldsmith, Stephanie Gil
- **Affiliation**: Bar-Ilan University (Faculty of Engineering); Arizona State University (Electrical, Computer and Energy Engineering); Princeton University (Electrical and Computer Engineering); Harvard University (Computer Science, School of Engineering and Applied Sciences)
- **Venue**: Not specified (arXiv:2212.02459v3, cs.RO, 14 Jan 2025; partially presented at IEEE Conference on Decision and Control [1])
- **Link/arXiv**: arXiv:2212.02459v3

## Taxonomy
- **Robustness / perturbation type targeted**: Malicious / Byzantine agents in distributed optimization (adversarial injection of falsified or manipulated data over a network); resilience even when malicious agents form a majority.
- **Method paradigm**: Resilient distributed (sub)gradient optimization exploiting stochastic inter-agent trust values; learning trusted neighbors; worst-case adversary modeling; convergence-rate analysis.
- **Keywords**: Distributed optimization, resilience, malicious agents, Byzantine agents, stochastic trust values, cyberphysical systems.

## TL;DR
The paper develops a new algorithmic and analytical framework for resilient distributed optimization in which legitimate agents exploit stochastic inter-agent trust observations to learn and discard malicious neighbors, recovering convergence (both in mean and almost surely) to the true global optimum together with expected convergence-rate bounds, even when malicious agents form the majority of the network.

## Problem & Motivation
Distributed optimization underlies many multi-agent cyberphysical tasks (distributed control/estimation, multi-robot mapping, federated learning), and its theory is mature for the benign case, but in the presence of malicious activity these guarantees no longer hold. Malicious agents can drive convergence to a non-optimal solution or prevent convergence by withholding or manipulating shared gradients/values. Existing data-based detection schemes have a hard upper bound on the number of tolerable malicious agents (typically cannot exceed half of the network connectivity), so they fail when adversaries form a majority. The paper instead exploits the physicality of cyberphysical systems — abstracted as a stochastic trust value α_ij measuring how much agent i can trust data from neighbor j — to achieve much stronger resilience.

## Robustness Setting
- **Threat model / uncertainty set**: An unknown subset M of agents is malicious; legitimate agents L do not know which (if any) of their neighbors are malicious. Malicious agents send falsified data in X to harm the optimization and may collaborate; their actions are unknown and treated worst-case. The model captures both identical-copy malicious inputs and the more general Byzantine case where an adversary sends different inputs to different legitimate neighbors. Legitimate agents have access to stochastic trust observations α_ij(t) ∈ [0,1] at every time t, with E[α_ij]−0.5 = E_L > 0 for legitimate links and E_M < 0 for malicious links (Assumption 1).
- **Setting**: Cooperative among legitimate agents (minimize the sum of local strongly convex objectives over a constraint set) with adversarial malicious agents; fully decentralized; online iterative optimization over an undirected communication graph.

## Method
- Each legitimate agent runs a projected distributed (sub)gradient update: it forms a weighted average c_i(t) of its own and neighbors' values, takes a gradient step on its local objective f_i, and projects onto the convex constraint set X (dynamics (2)/(7)).
- Trust learning: agent i accumulates β_ij(t) = Σ (α_ij(k) − 0.5) and defines a time-dependent trusted neighborhood N_i(t) = {j : β_ij(t) ≥ 0}; weights w_ij(t) are set to zero for neighbors classified as untrusted, so malicious inputs are eventually excluded (weight matrix (6)).
- A parameter T_0 controls how many trust observations are collected before optimization begins (used mainly for analysis/faster rates); the algorithm provably converges for any T_0 ≥ 0, including T_0 = 0.
- Misclassification analysis: the probability of misclassifying a legitimate/malicious neighbor decays exponentially in the number of observations (Lemma 1), implying an almost surely finite "correct classification time" T_f after which all classifications are correct (Corollary 1).
- After T_f the attacked dynamic reduces to a nominal malicious-free dynamic, enabling convergence proofs; two convergence-rate bounds are derived — one via the correct classification time (Theorem 4), a tighter one via the misclassification error probabilities applied directly to the attacked dynamic (Theorem 5).

## Theoretical Contributions
- Exponential decay of misclassification probability (Lemma 1, restated from [41]) and existence of an a.s. finite correct classification time T_f (Corollary 1).
- Asymptotic convergence of the nominal (malicious-free) dynamic to the optimal point with an explicit O(1/T) rate bound (Theorem 1).
- Almost sure convergence of the iterates to the true optimal point x⋆_L (Theorem 2), and convergence in the r-th mean for all r ≥ 1 (Theorem 3).
- Finite-time expected convergence-rate upper bounds on (1/|L|) Σ E[‖x_i(t) − x⋆_L‖²]: via correct classification time (Theorem 4, Corollary 3) and a tightened bound (Theorem 5) with an explicitly exponentially-T_0-decaying error term C_M(T_0), achieving O(1/T) for large T.
- A supporting d-dimensional Frobenius-norm contraction bound (Proposition 1) that avoids the √d scaling of naive per-dimension analysis.

## Experiments
- **Environment/Benchmark**: Numerical simulations of distributed optimization with |L| = 15 legitimate agents and |M| ∈ {15, 30} malicious agents, each malicious agent connected to all legitimate agents. A multi-dimensional (d = 5, λ = 0.1) constrained strongly convex regularized least-squares problem on the ball X = {‖x‖ ≤ η = 30}; trust values uniformly distributed with E[α_ij] = 0.55 (legitimate) / 0.45 (malicious), noise width ℓ ∈ {0.6, 0.8}, averaged over 100 realizations. Supplementary material adds a one-dimensional constrained consensus setup, Bernoulli trust observations, and connectivity comparisons.
- **Baselines**: W-MSR algorithm [11] (one-dimensional) and its multi-dimensional extension [64]; the nominal no-malicious dynamic (14) as an ideal reference.
- **Evaluation metrics**: Average squared error e(t) = (1/|L|) Σ_{i∈L} ‖x_i(t) − x⋆_L‖² versus time t; comparison of numerical curves against the derived analytical upper bounds.

## Key Results
- Algo. 1 recovers convergence to the true nominal optimum and mitigates malicious inputs even in higher dimensions, tolerating up to 30 = 2|L| malicious agents, whereas the multi-dimensional W-MSR baseline [64] becomes more vulnerable as dimension d grows and (in the 1-D case) W-MSR fails to converge because the number of malicious agents exceeds its tolerance threshold.
- The observation window T_0 does not affect whether the algorithm converges (it always recovers the global optimum) but governs the rate of recovery; higher trust-value variance increases misclassification errors, so larger T_0 helps mostly when variance is high (e.g., beneficial up to T_0 ≈ 100 for ℓ = 0.8, less so for ℓ = 0.6).
- Numerical and analytical results jointly validate the O(1/T) expected convergence rate, and increased inter-connectivity among legitimate agents (lower ρ_L) reduces the mean squared error, though the analytical bounds are more pessimistic than the observed numerical performance.

## Limitations & Future Work
- The analysis assumes µ-strongly convex, L-smooth local objectives, a compact convex constraint set X with a known bound η, and trust observations satisfying first-moment homogeneity and independence (Assumption 1); the authors note possible relaxations (per-link E_ij, dependent observations such as Markov chains/martingales, global rather than individual strong convexity, relaxing Assumption 3) at the cost of slower rates, but these are discussed rather than fully developed.
- The derived analytical upper bounds are loose in finite-time/short-time regimes (dominated by worst-case constants such as the maximal gradient and second-largest eigenvalue modulus), so they are pessimistic relative to numerical performance.
- The work focuses on deriving the resilience framework using the trust model α_ij rather than on deriving the trust values themselves from physical-layer measurements.

## Relevance to Survey
This paper sits on the fault-tolerance / Byzantine-robustness line of robust multi-agent learning, addressing resilience of distributed optimization (the optimization backbone of federated learning and multi-robot/cyberphysical coordination) against malicious and Byzantine agents. Its distinctive contribution to the robust-MARL landscape is the use of physicality-derived stochastic trust observations to learn and exclude adversarial neighbors, breaking the classical "less-than-half malicious agents" tolerance barrier of data-based resilient consensus/optimization methods (e.g., W-MSR). It connects the communication-robustness and trust-based defense theme to convergence-guaranteed distributed optimization, complementing game-theoretic and minimax robust-MARL formulations with an optimization-theoretic, adversary-tolerant perspective.

## Related Work (verbatim excerpts from the paper)

> _[Section I, Introduction]_

"However, in the presence of malicious activity, many of these known results are no longer applicable, requiring a new theoretical characterization of performance for the adversarial case."

"In particular, malicious agents can greatly interfere with the result of a distributed optimization scheme, driving the convergence to a non-optimal solution or preventing convergence altogether. They can accomplish this by either not sharing key information or by manipulating key information such as the shared gradients, which are critical for the correct functioning of the distributed optimization scheme [10]–[12]. Note that while well-established stochastic optimization methods characterize the effect of noise in distributed multi-agent systems [13], [14], malicious agents have the ability to inject intentionally biased or manipulated information which can lead to a greater potential damage for these systems. As a result, recent works have increasingly turned their attention to the investigation of robust and resilient versions of distributed optimization methods in the face of malicious intent and/or severe (potentially biased) noise [10]–[12], [15], [16]. These approaches can be coarsely divided into two categories: those that use the transmitted data between nodes to infer the presence of anomalies (for example see [11], [17]), and those that exploit additional side information from the network or the physicality of the underlying cyberphysical system to provide additional channels of resilience [18]–[20]."

"Indeed, the physicality of cyberphysical systems has been shown to provide many new channels of verification and establishing inter-agent trust through watermarking [21], wireless signal characteristics [20], [22], side information [23], and camera or LiDAR data cross-validation [24]. By exploiting these physicality-based measurements, agents can extract additional information about the trustworthiness of their neighbors."

> _[Section I.A, Related work]_

"In the absence of malicious agents, the legitimate agents can construct iterates converging to an optimal point x⋆_L by using either their gradients, or sub-gradients when their objective functions are not differentiable. Each agent i updates its data value by considering the data values of its neighbors, and its self-serving gradient direction of its objective function fi or the directions obtained from its neighbors. Convergence to an optimal point x⋆_L can be achieved for constrained multi-agent problems in [5], [7], [14], [25]–[30] and with limited gradient information [31], [32]. Additionally, a zero-order method has been proposed in [33]. Some works, such as [5], assume that the weight matrices, which dictate how agents incorporate the data they receive from their neighbors, are doubly-stochastic. However, works such as [28] overcome this assumption by performing additional weighted averaging steps. Finally, it has been established that the convergence rate of distributed gradient algorithms with diminishing step size is at best O(1/T) where T is the algorithm running time, see for example [30]."

"To harm the system, a malicious agent can send falsified data to their legitimate neighbors. If the legitimate agents are unaware that this data comes from malicious neighbors, then the malicious agents will succeed in controlling the system [10], [11], [34]–[39]. To combat the harmful effect of an attack, the approach taken in [34]–[36] requires the pre-existence of a set of trusted agents such that all other agents (legitimate or malicious) are connected to at least one trusted agent. Nonetheless, this approach is unrealistic when communication is sporadic such as in robotic and ad-hoc networks. The approaches in [10], [11], [37]–[40] rely on the agent data values to detect and discard malicious inputs. In general, data-based approaches have an upper bound on the number of tolerable malicious agents which cannot exceed half of the network connectivity; in some cases, this condition can be relaxed to half of the number of agents in the system - see, for example, [39]. Thus, they are not robust when malicious agents form a majority [37]. When the number of malicious agents exceeds the tolerable number, the attack succeeds and malicious agents evade detection. In contrast with the existing works, our proposed method provides a significantly stronger resilience to malicious activity by exploiting the physical aspect of the problem, i.e., the wireless medium. Thus, each legitimate agent can learn trustworthy neighbors while optimizing the system objective. Our prior work [41] studies the implications of the agents' learning ability, with regards to the trustworthiness of their neighbors, on distributed consensus systems. This work considers the more general case of distributed optimization systems where the agent's goal is to minimize the sum of their local objective function under limited information exchange."

"Finally, this work also relates to stochastic optimization, see for example [42]–[49]. However, unlike the typical assumption that the stochastic gradients are unbiased and statistically independent of the weights, in this work the stochastic gradients are biased, where the bias occurs due to the adversarial inputs of the malicious agents. Furthermore, learning the trustworthiness of neighboring agents and adjusting agents' weight accordingly leads to a correlation between the agents' values and the weights that are assigned to them. To this end, our analysis could not rely on previous results when analyzing the rate of convergence of the agents' dynamic."

### Cited references (resolved from the paper's bibliography)
- **[5]** A. Nedić, A. Ozdaglar. *Distributed subgradient methods for multi-agent optimization.* IEEE Trans. Automat. Contr. 2009.
- **[7]** A. Nedić, A. Olshevsky. *Distributed optimization over time-varying directed graphs.* IEEE Trans. Automat. Contr. 2015.
- **[10]** N. Ravi, A. Scaglione, A. Nedić. *A case of distributed optimization in adversarial environment.* IEEE ICASSP 2019.
- **[11]** S. Sundaram, B. Gharesifard. *Distributed optimization under adversarial nodes.* IEEE Trans. Automat. Contr. 2019.
- **[12]** A.-Y. Lu, G.-H. Yang. *Distributed secure state estimation in the presence of malicious agents.* IEEE Trans. Automat. Contr. 2021.
- **[13]** J. Tsitsiklis, D. Bertsekas, M. Athans. *Distributed asynchronous deterministic and stochastic gradient optimization algorithms.* IEEE Trans. Automat. Contr. 1986.
- **[14]** A. Nedić, A. Olshevsky. *Stochastic gradient-push for strongly convex functions on time-varying directed graphs.* IEEE Trans. Automat. Contr. 2016.
- **[15]** M. Zhu, S. Martínez. *On distributed constrained formation control in operator–vehicle adversarial networks.* Automatica 2013.
- **[16]** K. Saulnier, D. Saldana, A. Prorok, G. J. Pappas, V. Kumar. *Resilient flocking for mobile robot teams.* IEEE Robotics and Automation Letters 2017.
- **[17]** F. Pasqualetti, A. Bicchi, F. Bullo. *Consensus computation in unreliable networks: A system theoretic approach.* IEEE Trans. Automat. Contr. 2012.
- **[18]** A. A. Cárdenas, T. Roosta, G. Taban, S. Sastry. *Cyber Security: Basic Defenses and Attack Trends.* 2008.
- **[19]** A. A. Cardenas, S. Amin, S. Sastry. *Secure control: Towards survivable cyber-physical systems.* International Conference on Distributed Computing Systems Workshops 2008.
- **[20]** J. Xiong, K. Jamieson. *SecureArray: Improving wifi security with fine-grained physical-layer information.* ACM MobiCom 2013.
- **[21]** Y. Mo, S. Weerakkody, B. Sinopoli. *Physical authentication of control systems: Designing watermarked control inputs to detect counterfeit sensor outputs.* IEEE Control Systems Magazine 2015.
- **[22]** S. Gil, S. Kumar, M. Mazumder, D. Katabi, D. Rus. *Guaranteeing spoof-resilient multi-robot networks.* Autonomous Robots 2017.
- **[23]** C. E. Shannon. *Channels with side information at the transmitter.* IBM Journal of Research and Development 1958.
- **[24]** C. Pippin, H. Christensen. *Trust modeling in multi-robot patrolling.* IEEE ICRA 2014.
- **[25]** A. Nedić, A. Ozdaglar, P. A. Parrilo. *Constrained consensus and optimization in multi-agent networks.* IEEE Trans. Automat. Contr. 2010.
- **[26]** S. S. Ram, A. Nedić, V. V. Veeravalli. *Distributed stochastic subgradient projection algorithms for convex optimization.* J. Optim. Theory Appl. 2010.
- **[27]** J. C. Duchi, A. Agarwal, M. J. Wainwright. *Dual averaging for distributed optimization: Convergence analysis and network scaling.* IEEE Trans. Automat. Contr. 2012.
- **[28]** K. I. Tsianos, S. Lawlor, M. G. Rabbat. *Push-sum distributed dual averaging for convex optimization.* IEEE CDC 2012.
- **[29]** K. I. Tsianos, S. Lawlor, M. G. Rabbat. *Consensus-based distributed optimization: Practical issues and applications in large-scale machine learning.* Allerton Conf. Commun. Control Comput. 2012.
- **[30]** K. I. Tsianos, M. G. Rabbat. *Distributed strongly convex optimization.* Allerton Conf. Commun. Control Comput. 2012.
- **[31]** S. Magnússon, C. Enyioha, N. Li, C. Fischione, V. Tarokh. *Convergence of limited communication gradient methods.* IEEE Trans. Automat. Contr. 2018.
- **[32]** R. Saha, S. Rini, M. Rao, A. J. Goldsmith. *Decentralized optimization over noisy, rate-constrained networks: Achieving consensus by communicating differences.* IEEE J. Sel. Areas Commun. 2022.
- **[33]** Y. Tang, J. Zhang, N. Li. *Distributed zero-order algorithms for nonconvex multiagent optimization.* IEEE Trans. Control Netw. Syst. 2021.
- **[34]** W. Abbas, Y. Vorobeychik, X. Koutsoukos. *Resilient consensus protocol in the presence of trusted nodes.* International Symposium on Resilient Control Systems (ISRCS) 2014.
- **[35]** J. S. Baras, X. Liu. *Trust is the cure to distributed consensus with adversaries.* 27th Mediterranean Conference on Control and Automation (MED) 2019.
- **[36]** C. Zhao, J. He, Q.-G. Wang. *Resilient distributed optimization algorithm against adversarial attacks.* IEEE Trans. Automat. Contr. 2020.
- **[37]** B. Turan, C. A. Uribe, H.-T. Wai, M. Alizadeh. *Resilient primal-dual optimization algorithms for distributed resource allocation.* IEEE Trans. Control Netw. Syst. 2021.
- **[38]** W. Fu, Q. Ma, J. Qin, Y. Kang. *Resilient consensus-based distributed optimization under deception attacks.* International Journal of Robust and Nonlinear Control 2021.
- **[39]** S. Yu, S. Kar. *Secure distributed optimization under gradient attacks.* IEEE Trans. Signal Process. 2023.
- **[40]** T. Ding, Q. Xu, S. Zhu, X. Guan. *A convergence-preserving data integrity attack on distributed optimization using local information.* IEEE CDC 2020.
- **[41]** M. Yemini, A. Nedić, A. J. Goldsmith, S. Gil. *Characterizing trust and resilience in distributed consensus for cyberphysical systems.* IEEE Trans. Robot. 2022.
- **[42]** J. Duchi, E. Hazan, Y. Singer. *Adaptive subgradient methods for online learning and stochastic optimization.* Journal of Machine Learning Research 2011.
- **[43]** S. Ghadimi, G. Lan. *Optimal stochastic approximation algorithms for strongly convex stochastic composite optimization, I: a generic algorithmic framework.* SIAM J. Optim. 2012.
- **[44]** S. Ghadimi, G. Lan. *Optimal stochastic approximation algorithms for strongly convex stochastic composite optimization, II: shrinking procedures and optimal algorithms.* SIAM J. Optim. 2013.
- **[45]** R. Johnson, T. Zhang. *Accelerating stochastic gradient descent using predictive variance reduction.* NeurIPS 2013.
- **[46]** A. Jalilzadeh, A. Nedić, U. V. Shanbhag, F. Yousefian. *A variable sample-size stochastic quasi-Newton method for smooth and nonsmooth stochastic convex optimization.* IEEE CDC 2018.
- **[47]** C. Wilson, V. Veeravalli, A. Nedić. *Adaptive sequential stochastic optimization.* IEEE Trans. Automat. Contr. 2019.
- **[48]** A. Nedić, S. Lee. *On stochastic subgradient mirror-descent algorithm with weighted averaging.* SIAM J. Optim. 2014.
- **[49]** S. Pu, A. Nedić. *Distributed stochastic gradient tracking methods.* Mathematical Programming 2021.
