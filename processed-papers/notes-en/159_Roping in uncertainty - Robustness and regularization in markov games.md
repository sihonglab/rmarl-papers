# 159. Roping in Uncertainty: Robustness and Regularization in Markov Games

## Metadata
- **Title**: Roping in Uncertainty: Robustness and Regularization in Markov Games
- **Authors**: Jeremy McMahan, Giovanni Artiglio, Qiaomin Xie
- **Affiliation**: University of Wisconsin-Madison, USA
- **Venue**: ICML 2024 (Proceedings of the 41st International Conference on Machine Learning, PMLR 235)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty in Markov games (reward-function uncertainty and transition uncertainty), under s-rectangular and (s,a)-rectangular uncertainty sets; sim-to-real gap.
- **Method paradigm**: Robust Markov game (RMG) theory; robustness-regularization equivalence (duality via support functions / Legendre-Fenchel transform); regularized Markov games; game-theoretic equilibrium (robust Nash equilibrium); computational complexity (PPAD-hardness) and polynomial-time planning.
- **Keywords**: Robust Markov game, robust Nash equilibrium, regularization, s-rectangularity, support function, PPAD-hardness, player-decomposability

## TL;DR
The paper establishes a general equivalence between computing a Markov-perfect robust Nash equilibrium (MPRNE) of an s-rectangular RMG and computing a Nash equilibrium of an appropriately constructed regularized Markov game (the regularizer being the uncertainty set's support function), yielding a planning algorithm and provable robustness guarantees for regularized methods; it also proves that computing an RNE is PPAD-hard even for reward-uncertain two-player zero-sum matrix games, and identifies an "efficiently player-decomposable" uncertainty structure (covering L1 and L∞ balls) solvable in polynomial time.

## Problem & Motivation
Offline RL and RL in simulated environments suffer from the sim-to-real gap, where slight model differences yield poor real-world performance. Robust MDPs (RMDP) and later robust Markov games (RMG) were introduced to combat this, and regularization has been a popular empirical approach to improving robustness and convergence of multi-agent RL. However, while RMDPs are well understood, RMGs are much less so: the seminal RMG work proved only asymptotic convergence; a sample-efficient learning method for (s,a)-rectangular RMGs exists but relies on a planning oracle that does not yet exist in the literature; and the robustness-regularization duality, proven for MDPs, had not been established for the multi-agent (game) setting. Unlike classical RMDPs, solving RMGs is already hard with only reward uncertainty, since a single-stage reward-uncertain game can capture arbitrary general-sum games. This work aims to provide the missing efficient planning oracle, formalize the robustness-regularization equivalence in games, and characterize when RMGs are tractable.

## Robustness Setting
- **Threat model / uncertainty set**: A robust Markov game (S, {Ai}, P⋆, r⋆, H, U) with nominal game G⋆=(P⋆,r⋆) and uncertainty set U := P × Ur (transition kernels P and reward functions Ur), centered on the nominal model. Uncertainty sets are closed, convex, and satisfy a rectangular condition: s-rectangularity (Definition 2.2) or the special case (s,a)-rectangularity (Definition 2.3). Reward uncertainty sets may be policy-dependent, Ur(π) = r⋆ + R(π). The robust value of each player takes the worst case (infimum) over the uncertainty set. Examples include L1/L∞-ball, TV, KL, Chi-square, and Wasserstein uncertainty sets.
- **Setting**: Multi-player general-sum Markov games and the two-player zero-sum special case (TPZS RMG); finite-horizon H; planning (model known) with results extending to learning via off-the-shelf regularized-MG solvers; centralized solution concept (Markov-perfect robust Nash equilibrium).

## Method
- Define the robust value functions of a joint policy via worst-case (infimum) over the uncertainty set, leading to the Markov-perfect robust Nash equilibrium (MPRNE) solution concept, in which each player plays a robust best response under the worst-case model.
- For reward uncertainty, rewrite the robust value via the Legendre-Fenchel duality: Vπ_i = π⊤_i r⋆_i π−i − σ_Ri(−πi π⊤_−i), where σ_Ri is the support function of the uncertainty set; this shows the robust value equals the regularized value of a σ_Ri-regularized game.
- Prove the robustness-regularization equivalence (Theorems 3.1, 3.6): π is an MPRNE of the RMG iff π is an MPNE of the regularized MG whose regularizer is Ωi,h(s,μ) := σ_Ri,s,h(−μi μ⊤_−i); for common regularizers (ℓp/ℓq-norm, entropy, KL), the equivalence is interpretable both directions, so the two problems are polynomial-time equivalent.
- For transition uncertainty (Section 5), derive a robust policy-evaluation equation replacing the linear expected-future-value term with a support function σ_Ps,h(·), and introduce a generalized "policy-value regularized MG" whose regularizer is that support function; give closed-form regularizers for ball, TV, KL, Chi-square, and Wasserstein sets.
- Extend zero-sum games to the robust setting (Definition 4.1) and define the "efficiently player-decomposable" structure (Definition 4.2): when σ_Ri(−μi μ⊤_−i) decomposes as Ωh_i,i(μi) + Ωh_i,−i(μ−i), the equivalent regularized game is zero-sum and (with strongly convex regularizers) solvable in polynomial time via backward induction; this covers L1 and L∞-ball sets.

## Theoretical Contributions
- Existence of robust Nash equilibrium for s-rectangular RMGs under Assumption 2.1 (Theorem 2.1), via Kakutani's fixed-point theorem.
- Robustness-regularization equivalence for matrix games (Theorem 3.1), with interpretable regularizer-uncertainty correspondences (Theorem 3.3), and its extension to Markov games (Proposition 3.5, Theorem 3.6), proving regularized solutions are provably robust (Corollaries 3.2, 3.4, 3.7).
- PPAD-hardness of computing an RNE for TPZS RMGs with (s,a)-rectangular reward uncertainty even for H=S=1 (Theorem 4.1), and for transition uncertainty even for S=H=2 (Theorem 5.5).
- Polynomial-time solvability for efficiently player-decomposable TPZS RMGs (Lemma 4.2, Theorems 4.3, 4.5; Corollary 4.4), including ball-constrained and decomposable-kernel uncertainty sets.
- Robust Bellman equation for RMGs with general s-rectangular reward and transition uncertainty (Proposition B.1), and equivalent policy-value regularizers for TV, KL, Chi-square, and Wasserstein transition uncertainty (Corollaries 5.3, 5.4, F.1).

## Experiments
- **Environment/Benchmark**: Not specified (theoretical paper; no empirical experiments reported).
- **Baselines**: Not specified.
- **Evaluation metrics**: Not specified.

## Key Results
- Computing an MPRNE of an s-rectangular RMG reduces to computing an MPNE of a regularized MG; for common regularizers (ℓp/ℓq-norm, entropy, KL) the two problem classes are polynomial-time equivalent, so off-the-shelf regularized-MG solvers efficiently yield robust policies—mathematically confirming the empirical phenomenon.
- Even the simplest reward-uncertain two-player zero-sum RMG with (s,a)-rectangularity and H=S=1 is PPAD-hard, in sharp contrast to classical zero-sum games solvable by LP; transition-uncertain TPZS RMGs with (s,a)-rectangularity and H=2 are also PPAD-hard.
- For efficiently player-decomposable uncertainty (support function splits into per-player terms), the equivalent regularized game is zero-sum and an MPRNE can be computed in polynomial time; this class includes L1 and L∞-ball uncertainty sets.
- The shape of the reward uncertainty set determines the equivalent regularizer (e.g., a ball-constrained set corresponds to norm regularization) and its size (radius) determines the regularization magnitude.

## Limitations & Future Work
- General s-rectangular RMGs can map to general-sum regularized games, which are hard to solve; efficient algorithms are guaranteed only under the efficiently player-decomposable structure and for the two-player zero-sum case.
- Computing an RNE is PPAD-hard even for simple reward- or transition-uncertain RMGs, so tractability requires special uncertainty structure.
- The paper is theoretical with no empirical evaluation reported; the authors note the equivalence "opens the path to efficient planning and learning algorithms for achieving robustness in games via regularization" (future direction).

## Relevance to Survey
This paper sits on the "model/environment uncertainty" main line of robust MARL, directly building on the robust Markov game framework (Zhang et al., 2020b; Kardeş et al., 2011) and the sample-efficient (s,a)-rectangular RMG learning line (Blanchet et al., 2023), for which it supplies the missing efficient planning oracle. Its central contribution—the robustness-regularization duality extended from RMDPs (Derman et al., 2021; 2023) to Markov games—connects the robust-MDP/robust-RL line, the regularized-MDP/regularized-game line, and the game-theoretic-equilibrium line. The PPAD-hardness results and the player-decomposability tractable class are key computational-complexity landmarks for distributionally robust MARL.

## Related Work (verbatim excerpts from the paper)

> _[Section 1.1, Related Work — "Robust MDPs."]_

"Robust MDPs have been studied under many different uncertainty structures. The original structure, called (s, a)-rectangularity, was first introduced in (Satia & Lave, 1973; Nilim & El Ghaoui, 2003). Many attempts to generalize (s, a)-rectangularity have led to a rich family of rectangularity notions including s-rectangularity (Epstein & Schneider, 2003; Wiesemann et al., 2013), r-rectangularity (Goh et al., 2018; Goyal & Grand-Clément, 2023), k-rectangularity (Mannor et al., 2016), and d-rectangularity (Ma et al., 2023b). Many standard MDP techniques have also been extended to the robust setting including dynamic programming (Iyengar, 2005; Ho et al., 2018), policy iteration (Kaufman & Schaefer, 2013; Ho et al., 2021), policy gradient (Kumar et al., 2023; Wang et al., 2023), and function approximation (Lim & Autef, 2019; Tamar et al., 2014). Regularized MDP techniques also successfully solve robust MDPs due to a general equivalence for many uncertainty sets (Derman et al., 2021; 2023; Kumar et al., 2022) including both (s, a) and s-rectangularity."

"In the learning setting, standard RL approaches have been successfully “robustified” including model-based approaches (Wang & Zou, 2021), Q-learning (Liu et al., 2022), policy gradient (Wang & Zou, 2022; Badrinath & Kalathil, 2021), and kernel methods (Lim & Autef, 2019). Strong theoretical results have also pinned down the sample complexity of many methods (Panaganti & Kalathil, 2022; Shi & Chi, 2023; Yang et al., 2022). In fact, Pinto et al. (2017) showed that robust learning is equivalent to learning in adversarial games and this is further exploited using game-theoretical techniques (Hayashi et al., 2005)."

> _[Section 1.1, Related Work — "Robust MGs."]_

"Robust normal form games were first introduced by Aghassi & Bertsimas (2006). Perchet (2020) showed that robust games can be reduced to general sum games, but computationally efficient methods have yet to be established. The notion of robustness has been extended to Markov games (Zhang et al., 2020b; Kardeş et al., 2011). A sample efficient approach for learning robust policies under (s, a)-rectangularity is derived by Blanchet et al. (2023), but their method relies on a planning oracle that has yet to be derived in the literature. Our work provides the efficient planning oracle needed to make those methods tractable and extends beyond just (s, a)-rectangularity. In contrast, Ma et al. (2023a) addresses the problem of learning a robust CCE with low sample complexity whereas we focus on computing the stronger solution concept of robust NE."

> _[Section 1.1, Related Work — "Regularization in MDP and MGs."]_

"Various regularization methods have been extensively used in MDPs (Kumar et al., 2023; Geist et al., 2019) and games (Grill et al., 2019; Cen et al., 2021; Zhang et al., 2023; Mertikopoulos & Sandholm, 2016), with diverse motivations, such as improved exploration (Lee et al., 2018), stability (Schulman et al., 2017) and convergence (Cen et al., 2021; Zhan et al., 2023). Popular regularizers include a variety of entropy functions and KL divergence. Recent works relate regularization to robustness in MDP/RL (Brekelmans et al., 2022; Eysenbach & Levine, 2021; Husain et al., 2021). In particular, Derman et al. (2023) provides an equivalence between regularization and robustness in MDPs. However, the robustness-regularization duality is much less understood in games. Our work fills this gap and opens the path to efficient planning and learning algorithms for achieving robustness in games via regularization."

> _[Introduction]_

"To combat the sim-to-real gap, robust policies were studied using the framework of robust Markov decision processes (RMDP) (Satia & Lave, 1973) and later robust Markov Games (RMG) (Zhang et al., 2020b). Robust approaches have been effective in the real world, especially for navigating UAVs in mission-critical multi-agent environments (Chen et al., 2023) and in queuing systems (Kardeş et al., 2011). In practice, regularization has been a popular approach to improving the robustness and convergence of multi-agent RL algorithms with empirical success."

"Although many advances have been made for RMDPs, RMGs are much less understood. The seminal paper (Zhang et al., 2020b) devised algorithms to learn a robust NE (RNE) for RMGs but only proved asymptotic convergence of their methods. On the other hand, Blanchet et al. (2023) proposed provably sample-efficient algorithms to learn an RNE for the special case of (s, a)-rectangular RMGs, but their methods require an efficient planning oracle that does not currently exist in the literature. Creating such a planning oracle is one of the goals of this work. Lastly, adding a regularizer to the value function of an MG has shown promise to improve robustness empirically, but formal guarantees have not been shown in the multi-agent setting (Zhang et al., 2020a)."

### Cited references (resolved from the paper's bibliography)
- **[Aghassi & Bertsimas, 2006]** Aghassi, M. and Bertsimas, D. *Robust game theory.* Mathematical Programming, 107(1–2):231–273, 2006.
- **[Badrinath & Kalathil, 2021]** Badrinath, K. P. and Kalathil, D. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML 2021.
- **[Blanchet et al., 2023]** Blanchet, J., Lu, M., Zhang, T., and Zhong, H. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* 2023.
- **[Brekelmans et al., 2022]** Brekelmans, R., Genewein, T., Grau-Moya, J., Délétang, G., Kunesch, M., Legg, S., and Ortega, P. *Your policy regularizer is secretly an adversary.* arXiv:2203.12592, 2022.
- **[Cen et al., 2021]** Cen, S., Wei, Y., and Chi, Y. *Fast policy extragradient methods for competitive games with entropy regularization.* NeurIPS 2021.
- **[Chen et al., 2023]** Chen, S., Liu, G., Zhou, Z., Zhang, K., and Wang, J. *Robust multi-agent reinforcement learning method based on adversarial domain randomization for real-world dual-UAV cooperation.* IEEE Transactions on Intelligent Vehicles, 2023.
- **[Derman et al., 2021]** Derman, E., Geist, M., and Mannor, S. *Twice regularized MDPs and the equivalence between robustness and regularization.* NeurIPS 2021.
- **[Derman et al., 2023]** Derman, E., Men, Y., Geist, M., and Mannor, S. *Twice regularized Markov decision processes: The equivalence between robustness and regularization.* 2023.
- **[Epstein & Schneider, 2003]** Epstein, L. and Schneider, M. *Recursive multiple-priors.* Journal of Economic Theory, 113(1):1–31, 2003.
- **[Eysenbach & Levine, 2021]** Eysenbach, B. and Levine, S. *Maximum entropy RL (provably) solves some robust RL problems.* ICLR 2021.
- **[Geist et al., 2019]** Geist, M., Scherrer, B., and Pietquin, O. *A theory of regularized Markov decision processes.* ICML 2019.
- **[Goh et al., 2018]** Goh, J., Bayati, M., Zenios, S. A., Singh, S., and Moore, D. *Data uncertainty in Markov chains: Application to cost-effectiveness analyses of medical innovations.* Operations Research, 66(3):697–715, 2018.
- **[Goyal & Grand-Clément, 2023]** Goyal, V. and Grand-Clément, J. *Robust Markov decision processes: Beyond rectangularity.* Mathematics of Operations Research, 48(1):203–226, 2023.
- **[Grill et al., 2019]** Grill, J.-B., Darwiche Domingues, O., Menard, P., Munos, R., and Valko, M. *Planning in entropy-regularized Markov decision processes and games.* NeurIPS 2019.
- **[Hayashi et al., 2005]** Hayashi, S., Yamashita, N., and Fukushima, M. *Robust Nash equilibria and second-order cone complementarity problems.* Journal of Nonlinear and Convex Analysis, 6:283–296, 2005.
- **[Ho et al., 2018]** Ho, C. P., Petrik, M., and Wiesemann, W. *Fast Bellman updates for robust MDPs.* ICML 2018.
- **[Ho et al., 2021]** Ho, C. P., Petrik, M., and Wiesemann, W. *Partial policy iteration for ℓ1-robust Markov decision processes.* JMLR, 22(1), 2021.
- **[Husain et al., 2021]** Husain, H., Ciosek, K., and Tomioka, R. *Regularized policies are reward robust.* AISTATS 2021.
- **[Iyengar, 2005]** Iyengar, G. N. *Robust dynamic programming.* Mathematics of Operations Research, 30(2):257–280, 2005.
- **[Kardeş et al., 2011]** Kardeş, E., Ordóñez, F., and Hall, R. W. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 59(2):365–382, 2011.
- **[Kaufman & Schaefer, 2013]** Kaufman, D. L. and Schaefer, A. J. *Robust modified policy iteration.* INFORMS Journal on Computing, 25(3):396–410, 2013.
- **[Kumar et al., 2022]** Kumar, N., Levy, K., Wang, K., and Mannor, S. *Efficient policy iteration for robust Markov decision processes via regularization.* 2022.
- **[Kumar et al., 2023]** Kumar, N., Derman, E., Geist, M., Levy, K., and Mannor, S. *Policy gradient for rectangular robust Markov decision processes.* 2023.
- **[Lee et al., 2018]** Lee, K., Choi, S., and Oh, S. *Sparse Markov decision processes with causal sparse Tsallis entropy regularization for reinforcement learning.* IEEE Robotics and Automation Letters, 3(3):1466–1473, 2018.
- **[Lim & Autef, 2019]** Lim, S. H. and Autef, A. *Kernel-based reinforcement learning in robust Markov decision processes.* ICML 2019.
- **[Liu et al., 2022]** Liu, Z., Bai, Q., Blanchet, J., Dong, P., Xu, W., Zhou, Z., and Zhou, Z. *Distributionally robust Q-learning.* ICML 2022.
- **[Ma et al., 2023a]** Ma, S., Chen, Z., Zou, S., and Zhou, Y. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR, 24(371):1–40, 2023.
- **[Ma et al., 2023b]** Ma, X., Liang, Z., Blanchet, J., Liu, M., Xia, L., Zhang, J., Zhao, Q., and Zhou, Z. *Distributionally robust offline reinforcement learning with linear function approximation.* 2023.
- **[Mannor et al., 2016]** Mannor, S., Mebel, O., and Xu, H. *Robust MDPs with k-rectangular uncertainty.* Mathematics of Operations Research, 41(4):1484–1509, 2016.
- **[Mertikopoulos & Sandholm, 2016]** Mertikopoulos, P. and Sandholm, W. H. *Learning in games via reinforcement and regularization.* Mathematics of Operations Research, 41(4):1297–1324, 2016.
- **[Nilim & El Ghaoui, 2003]** Nilim, A. and El Ghaoui, L. *Robustness in Markov decision problems with uncertain transition matrices.* NIPS 2003.
- **[Panaganti & Kalathil, 2022]** Panaganti, K. and Kalathil, D. *Sample complexity of robust reinforcement learning with a generative model.* AISTATS 2022.
- **[Perchet, 2020]** Perchet, V. *Finding robust Nash equilibria.* ALT 2020.
- **[Pinto et al., 2017]** Pinto, L., Davidson, J., Sukthankar, R., and Gupta, A. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Satia & Lave, 1973]** Satia, J. K. and Lave, R. E. *Markovian decision processes with uncertain transition probabilities.* Operations Research, 21(3):728–740, 1973.
- **[Schulman et al., 2017]** Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. *Proximal policy optimization algorithms.* arXiv:1707.06347, 2017.
- **[Shi & Chi, 2023]** Shi, L. and Chi, Y. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* 2023.
- **[Tamar et al., 2014]** Tamar, A., Mannor, S., and Xu, H. *Scaling up robust MDPs using function approximation.* ICML 2014.
- **[Wang et al., 2023]** Wang, Q., Ho, C. P., and Petrik, M. *Policy gradient in robust MDPs with global convergence guarantee.* ICML 2023.
- **[Wang & Zou, 2021]** Wang, Y. and Zou, S. *Online robust reinforcement learning with model uncertainty.* NeurIPS 2021.
- **[Wang & Zou, 2022]** Wang, Y. and Zou, S. *Policy gradient method for robust reinforcement learning.* ICML 2022.
- **[Wiesemann et al., 2013]** Wiesemann, W., Kuhn, D., and Rustem, B. *Robust Markov decision processes.* Mathematics of Operations Research, 38(1):153–183, 2013.
- **[Yang et al., 2022]** Yang, W., Zhang, L., and Zhang, Z. *Towards theoretical understandings of robust Markov decision processes: Sample complexity and asymptotics.* 2022.
- **[Zhan et al., 2023]** Zhan, W., Cen, S., Huang, B., Chen, Y., Lee, J. D., and Chi, Y. *Policy mirror descent for regularized reinforcement learning: A generalized framework with linear convergence.* SIAM Journal on Optimization, 33(2):1061–1091, 2023.
- **[Zhang et al., 2023]** Zhang, F., Tan, V. Y. F., Wang, Z., and Yang, Z. *Learning regularized monotone graphon mean-field games.* 2023.
- **[Zhang et al., 2020a]** Zhang, K., Kakade, S., Basar, T., and Yang, L. *Model-based multi-agent RL in zero-sum Markov games with near-optimal sample complexity.* NeurIPS 2020.
- **[Zhang et al., 2020b]** Zhang, K., Sun, T., Tao, Y., Genc, S., Mallya, S., and Basar, T. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
