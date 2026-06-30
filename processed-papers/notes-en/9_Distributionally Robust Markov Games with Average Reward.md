# 9. Distributionally Robust Markov Games with Average Reward

## Metadata
- **Title**: Distributionally Robust Markov Games with Average Reward
- **Authors**: Zachary Roch, Yue Wang
- **Affiliation**: Department of Electrical and Computer Engineering, University of Central Florida; Department of Computer Science, University of Central Florida (Orlando, Florida, USA)
- **Venue**: ICML 2026 (Proceedings of the 43rd International Conference on Machine Learning, PMLR)
- **Link/arXiv**: arXiv:2508.03136v4 [cs.MA]

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty / model mismatch (Sim-to-Real gap); distributional robustness over an (s,a)-rectangular uncertainty set of transition kernels; worst-case over plausible game models.
- **Method paradigm**: Distributionally robust Markov game (DR-MG) theory; average-reward criterion; robust Bellman equation; robust Nash equilibrium; game-theoretic equilibrium existence (Kakutani fixed point); robust Nash value iteration; two-time-scale TD descent (smoothed via Moreau envelope).
- **Keywords**: Distributionally Robust Markov Games, average reward, Nash Equilibrium, robust Bellman equation, weakly communicating, robust TD

## TL;DR
The paper formalizes distributionally robust Markov games (DR-MGs) under the long-run average-reward criterion, proves the existence of a stationary robust Nash Equilibrium under both irreducible and weakly communicating assumptions via the robust Bellman equation, designs two provably convergent algorithms (Robust Nash-Iteration and Robust TD Descent), and shows the average-reward NE can be approximated by discounted DR-MG equilibria as the discount factor approaches one.

## Problem & Motivation
Markov games model sequential multi-agent decision-making, but a mismatch between the assumed model and the true environment (the Sim-to-Real gap, due to non-stationarity, modeling errors, exogenous disturbances, or adversarial attacks) degrades policies derived from a misspecified model. Distributionally robust Markov games address this by optimizing worst-case performance over an uncertainty set, but prior DR-MG work focuses almost exclusively on finite-horizon or discounted-reward settings. For systems operating over extended/indefinite horizons (warehouse robotics, communication networks, autonomous vehicle coordination, financial markets, peer-to-peer energy trading), the long-run average reward is more natural, yet average-reward DR-MGs are largely unstudied: average-reward analysis hinges on the limiting behavior of the stochastic process, the correspondence between stationary policies and state-action frequencies breaks down, and (as the paper proves) without structural assumptions a stationary robust NE may not even exist. Existing discounted/finite-horizon techniques (backward induction; uniqueness of the discounted robust Bellman solution) cannot be transplanted to the average-reward case.

## Robustness Setting
- **Threat model / uncertainty set**: Standard (s,a)-rectangular uncertainty set P = ×_(s,a) P^a_s of transition kernels; after the joint action a is taken at state s, the next state is determined by an arbitrary kernel in the slice P^a_s. Agents adopt pessimism, optimizing worst-case (robust) average reward g^π_P,i = min over P in P of g^π_P,i. The uncertainty is conceptually a "player-specific environment" that minimizes the specific agent's payoff; because different agents have different reward functions, their worst-case kernels need not coincide, forcing a general-sum treatment even of two-player zero-sum games.
- **Setting**: competitive / general-sum multi-agent (N players, each with its own reward); model uncertainty (not opponent-policy robustness); infinite-horizon average reward; the work is theoretical/algorithmic (planning-style with known uncertainty sets, plus a TD-based algorithm). Studied under (a) irreducible DR-MGs (Assumption 4.1) and (b) weakly communicating DR-MGs (Assumption 5.1).

## Method
- **Existence via best-response mapping**: For irreducible DR-MGs, reduce each agent to an induced single-agent distributionally robust MDP M_i(π_{-i}); show finding the best response equals solving the average-reward robust Bellman equation V(s) = Σ_a π(a|s)(r(s,a) − g + σ_{P^a_s}(V)); prove its solvability and uniqueness (up to a constant), then that the best-response set is convex and upper semi-continuous, so Kakutani's fixed-point theorem yields a robust NE.
- **Weakly communicating extension**: Where the per-policy Bellman correspondence fails, build a proxy "Bellman-greedy response set" G_i(π_{-i}) from the (uniquely solvable) optimal robust Bellman equation, show G_i(π_{-i}) ⊆ BR_i(π_{-i}), and apply Kakutani to the joint proxy map to get NE existence.
- **Robust Nash Iteration (Algorithm 2)**: Extends standard Nash value iteration to the robust average-reward setting, maintaining Q_i for all agents and solving a matrix-form game NE each step through a NE oracle; convergence proved under additional game-structure assumptions.
- **Robust TD Descent (Algorithm 1)**: Characterizes the robust NE through a global robust TD gap L(π) (a potential-function-like object with L(π)=0 iff π is a robust NE); smooths the non-smooth L via a Moreau-envelope proxy L_λ; runs a two-time-scale stochastic approximation (fast scale updates (g,V), slow scale updates π) with no NE oracle and polynomial per-iteration complexity.
- **Discounted-to-average connection**: Solve the (more tractable) discounted DR-MG and let γ → 1 to approximate the average-reward robust NE.

## Theoretical Contributions
- **Lemma 3.1**: There exists a finite-state two-player zero-sum average-reward DR-MG with no stationary robust Nash equilibrium (ill-posedness without structural assumptions).
- **Theorem 4.6**: Solvability and uniqueness (up to a constant vector) of the average-reward robust Bellman equation for any policy, and of the robust Bellman optimality equation, under irreducibility.
- **Theorem 4.7 / Theorem 4.8**: Convexity and semi-continuity of the best-response (optimal-policy) sets, leading to existence of a robust NE for irreducible DR-MGs.
- **Lemma 5.3 / Theorem 5.5**: Existence of a stationary robust NE for weakly communicating DR-MGs via the proxy Bellman-greedy map and strong duality / span bounds.
- **Theorem 6.1**: Robust Nash Iteration converges to a robust NE under Assumption 4.1 and an additional game-structure assumption (G.1).
- **Theorem 6.2 / Theorem 6.3**: TD-gap characterization of robust NE (L(π) ≥ 0, =0 iff NE), and weak convergence of Robust TD Descent to a stationary point of L_λ under Robbins-Monro step sizes — the first practical algorithm for average-reward DR-MGs with provable convergence.
- **Theorem 7.1**: Cluster points of γ-discounted DR-MG NE are average-reward DR-MG NE as γ → 1; an ε-NE of a sufficiently-discounted game is an O(ε)-NE under average reward.

## Experiments
- **Environment/Benchmark**: Synthetic planning-setting DR-MGs (Appendix J). (1) A two-player, two-state, two-action DR-MG with interval (TV-style) rectangular uncertainty on the next-state probability, intervals chosen so every induced chain is irreducible (Assumption 4.1); 30 independent random games. (2) A "Structured Random Environment" DR-MG with 20 states and 5 actions, states partitioned into 5 "prosperous" (reward ~N(2,1)) and 15 "deprived" (reward ~N(-2,1)) states with within-cluster persistence and a KL-divergence uncertainty ball (budget θ = 0.01). All experiments are planning (known rewards and uncertainty sets); robust Bellman equations solved via Relative Value Iteration (RVI).
- **Baselines**: Discounted-Reward Robust Nash-Iteration (Zhang et al., 2020; Shi et al., 2024) evaluated for discount factors γ from 0.5 to 0.99; and the non-robust average-reward Nash-Iteration (Li, 2003).
- **Evaluation metrics**: Global robust TD gap ΔR(π,g,V); robust Nash gap NashGap(π) = max_k (max_{ν_k} g^{ν_k,π_{-k}} − g^π); and worst-case (robust) long-run average reward of Player 1.

## Key Results
- Without structural assumptions, average-reward DR-MGs can fail to admit any stationary robust NE (impossibility example with a three-state, two-action, multi-chain zero-sum DR-MG where supₚ inf_q U = ε/2 ≠ inf_q supₚ U = ε/(1+ε)).
- A stationary robust NE provably exists for both irreducible and weakly communicating average-reward DR-MGs.
- Two provably convergent algorithms are provided: Robust Nash Iteration (converges to a robust NE under added assumptions / a NE oracle) and Robust TD Descent (no NE oracle, polynomial per-iteration cost, weak convergence to a stationary point of the smoothed TD gap).
- Average-reward robust NE can be approximated by discounted DR-MG NE for a discount factor γ close enough to 1, enabling tractable computation.

## Limitations & Future Work
- The min–max duality / saddle-point structure breaks down for DR-MGs, so standard discounted/zero-sum existence arguments cannot be reused; existence requires structural assumptions (irreducibility or weakly communicating).
- For DR-MGs, the set of stationary points of L_λ does not necessarily coincide with robust NE (gradient domination fails due to non-smoothness of the worst-case objective); Robust TD Descent only guarantees convergence to a stationary point of L_λ.
- Future work: explore local gradient domination under a strict-equilibrium assumption for local finite-time convergence; extend beyond (s,a)-rectangularity to handle state-coupled ambiguity; investigate fully shared worst-case kernels (robust cooperative games or robust Stackelberg games where nature acts as an adversarial leader).

## Relevance to Survey
This paper sits squarely on the distributionally robust MARL line, extending the robust Markov game / robust Nash equilibrium framework (model uncertainty main line) from the discounted and finite-horizon settings to the previously underexplored long-run average-reward criterion. It connects the operations-research robust stochastic game lineage (Kardeş et al., 2011; Zhang et al., 2020) to single-agent robust average-reward MDP theory (Wang et al., 2023b;c; Wang & Si, 2025) and to game-theoretic equilibrium-existence and convergent-algorithm design (robust Nash iteration, TD-based stochastic approximation). It is a foundational reference for the "distributionally robust MARL" and "robust average-reward RL" sub-themes of the survey, and complements the model-uncertainty robust-MARL works it builds on.

## Related Work (verbatim excerpts from the paper)
> _[Appendix A, Related Works — "Non-robust Markov Games"]_

"Markov Games (Littman, 1994) provide a foundational mathematical framework for multi-agent sequential decision-making. The majority of early work focused on two-player zero-sum MGs, especially under the discounted-reward setting. Under these settings, the existence of a stationary Nash Equilibrium was established in (Shapley, 1953) by formulating the problem as a Max-Min problem. It is later extended to multi-player general-sum MGs in (Fink, 1964). The average-reward criterion, while more suitable for systems with long operational horizons, presents greater analytical challenges. Unlike the discounted case, a stationary NE is not generally guaranteed to exist, even in two-player zero-sum games (Filar & Vrieze, 1996). Instead, NE existence has only been proven under some additional assumptions on the structure of the game, including irreducibility, zero-sum (Guo & Yang, 2008; Hern´andez-Lerma & Lasserre, 2000; Guo & Hern´andez-Lerma, 2003; Zheng & Guo, 2024; Nowak, 1999; IWASE et al., 1976; K¨uenle & Schurath, 2003; Tanaka & Wakuta, 1977; Ja´skiewicz & Nowak, 2001; Filar & Vrieze, 1996), or single recurrent class under any policy (Sobel, 1971; Sahabandu et al., 2024). However, these non-robust methods cannot be applied to our robust setting."

> _[Appendix A, Related Works — "Distributionally Robust MDPs"]_

"To address the performance degradation that occurs when a model is mis-specified, (single-agent) distributionally robust MDPs are first developed in (Iyengar, 2005; Nilim & El Ghaoui, 2003) for both finite horizon and infinite horizon discounted reward settings. Studies under the average reward setting are limited until recently. In (Wang et al., 2023b;c), fundamental understandings of robust average reward are developed under the unichain assumption, and is later extended to more general settings like weakly communicating ones (Grand-Clement et al., 2023; Wang & Si, 2025). A huge body of robust reinforcement learning for average reward is also developed, mainly focusing on the sample complexity (Xu et al., 2025b;a; Roch et al., 2025b;a; Chen et al., 2025; Grand-Cl´ement & Petrik, 2023; Chatterjee et al., 2024; Wang et al., 2024). However, single-agent robust MDPs with average reward are still not fully studied (e.g., uniqueness or solvability of robust Bellman equation are not clear). These works are all developed for single-agent settings, and do not address the challenges we faced in multi-agent DR-MGs."

> _[Appendix A, Related Works — "Distributionally Robust Markov Games"]_

"Extending distributional robustness to the multi-agent setting is a recent and active area of research. However, the literature has overwhelmingly concentrated on the finite-horizon (Ma et al., 2023; Shi et al., 2025; 2024; Jiao & Li, 2024; Li et al., 2025; Blanchet et al., 2023; Farhat et al., 2026) and discounted-reward criteria (Zhang et al., 2020; Kardes¸ et al., 2011). These settings are often more analytically tractable because the influence of future rewards diminishes, simplifying the analysis. However, none of these methods can be extended to the average-reward setting, as we discussed earlier."

> _[Introduction]_

"To address this vulnerability, the framework of distributionally robust Markov Games (DR-MGs) has been developed (Zhang et al., 2020; Kardes¸ et al., 2011), extending the principles of distributionally robust Markov Decision Processes (MDPs) (Bagnell et al., 2001; Nilim & El Ghaoui, 2003; Iyengar, 2005) to the multi-agent setting. Instead of relying on a single, fixed MG model, the robust approach seeks to find an equilibrium that optimizes the worst-case performance over a predefined uncertainty set of plausible game models under potential model mismatches. The resulting robust equilibrium provides a performance guarantee across all models within this set, thereby ensuring each agent's resilience against model mismatch."

> _[Introduction — on the Sim-to-Real gap and sources of model mismatch]_

"However, a critical challenge in practice is the potential for a mismatch between the assumed MG model and the true underlying environment. This discrepancy, commonly called the Sim-to-Real gap (McMahan et al., 2024), can arise from various sources, including environmental non-stationarity, inherent modeling errors, exogenous disturbances, or even adversarial attacks (Bukharin et al., 2023; Ma et al., 2023). Consequently, policies derived from a misspecified model can exhibit significantly degraded performance when deployed."

### Cited references (resolved from the paper's bibliography)
- **[Bagnell et al., 2001]** Bagnell, Ng, Schneider. *Solving uncertain Markov decision processes.* 2001.
- **[Blanchet et al., 2023]** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* NeurIPS 2023.
- **[Bukharin et al., 2023]** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* NeurIPS 2023.
- **[Chatterjee et al., 2024]** Chatterjee, Goharshady, Karrabi, Novotný, Zikelic. *Solving long-run average reward robust MDPs via stochastic games.* IJCAI 2024.
- **[Chen et al., 2025]** Chen, Wang, Si. *Sample complexity of distributionally robust average-reward reinforcement learning.* NeurIPS 2025.
- **[Farhat et al., 2026]** Farhat, Ghosh, Atia, Wang. *Sample-efficient distributionally robust multi-agent reinforcement learning via online interaction.* arXiv 2026 (arXiv:2508.02948).
- **[Filar & Vrieze, 1996]** Filar, Vrieze. *Competitive Markov decision processes.* Springer-Verlag 1996.
- **[Fink, 1964]** Fink. *Equilibrium in a stochastic n-person game.* Journal of Science of the Hiroshima University, Series A-I (Mathematics) 1964.
- **[Grand-Clément et al., 2023] / [Grand-Clement et al., 2023]** Grand-Clement, Petrik, Vieille. *Beyond discounted returns: Robust Markov decision processes with average and Blackwell optimality.* arXiv 2023 (arXiv:2312.03618).
- **[Grand-Clément & Petrik, 2023]** Grand-Clément, Petrik. *Reducing Blackwell and average optimality to discounted MDPs via the Blackwell discount factor.* NeurIPS 2023.
- **[Guo & Hernández-Lerma, 2003]** Guo, Hernández-Lerma. *Zero-sum games for continuous-time Markov chains with unbounded transition and average payoff rates.* Journal of Applied Probability 2003.
- **[Guo & Yang, 2008]** Guo, Yang. *A new condition and approach for zero-sum stochastic games with average payoffs.* Stochastic Analysis and Applications 2008.
- **[Hernández-Lerma & Lasserre, 2000]** Hernández-Lerma, Lasserre. *Zero-sum stochastic games in Borel spaces: average payoff criteria.* SIAM Journal on Control and Optimization 2000.
- **[Iyengar, 2005]** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research 2005.
- **[IWASE et al., 1976]** Iwase, Tanaka, Wakuta. *On Markov games with the expected average reward criterion.* Science Reports of Niigata University, Series A 1976.
- **[Jaśkiewicz & Nowak, 2001]** Jaśkiewicz, Nowak. *On the optimality equation for zero-sum ergodic stochastic games.* Mathematical Methods of Operations Research 2001.
- **[Jiao & Li, 2024]** Jiao, Li. *Minimax-optimal multi-agent robust reinforcement learning.* arXiv 2024 (arXiv:2412.19873).
- **[Kardeş et al., 2011]** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research 2011.
- **[Küenle & Schurath, 2003]** Küenle, Schurath. *The optimality equation and ε-optimal strategies in Markov games with average reward criterion.* Mathematical Methods of Operations Research 2003.
- **[Li et al., 2025]** Li, Zheng, Ni, Shan, Zhang, Li. *Sample-efficient tabular self-play for offline robust reinforcement learning.* arXiv 2025 (arXiv:2512.00352).
- **[Littman, 1994]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994 (Elsevier).
- **[Ma et al., 2023]** Ma, Chen, Zou, Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* Journal of Machine Learning Research 2023.
- **[McMahan et al., 2024]** McMahan, Artiglio, Xie. *Roping in uncertainty: Robustness and regularization in Markov games.* ICML 2024.
- **[Nilim & El Ghaoui, 2003]** Nilim, El Ghaoui. *Robustness in Markov decision problems with uncertain transition matrices.* NIPS 2003.
- **[Nowak, 1999]** Nowak. *Optimal strategies in a class of zero-sum ergodic stochastic games.* Mathematical Methods of Operations Research 1999.
- **[Roch et al., 2025a]** Roch, Atia, Wang. *A reduction framework for distributionally robust reinforcement learning under average reward.* ICML 2025.
- **[Roch et al., 2025b]** Roch, Zhang, Atia, Wang. *Provably sample-efficient robust reinforcement learning with average reward.* arXiv 2025 (arXiv:2505.12462).
- **[Sahabandu et al., 2024]** Sahabandu, Moothedath, Allen, Bushnell, Lee, Poovendran. *RL-ARNE: A reinforcement learning algorithm for computing average reward Nash equilibrium of nonzero-sum stochastic games.* IEEE Transactions on Automatic Control 2024.
- **[Shapley, 1953]** Shapley. *Stochastic games.* Proceedings of the National Academy of Sciences 1953.
- **[Shi et al., 2024]** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* ICML 2024.
- **[Shi et al., 2025]** Shi, Gai, Mazumdar, Chi, Wierman. *Breaking the curse of multiagency in robust multi-agent reinforcement learning.* ICML 2025.
- **[Sobel, 1971]** Sobel. *Noncooperative stochastic games.* The Annals of Mathematical Statistics 1971.
- **[Tanaka & Wakuta, 1977]** Tanaka, Wakuta. *On continuous time Markov games with the expected average reward criterion.* 1977.
- **[Wang et al., 2023b]** Wang, Velasquez, Atia, Prater-Bennette, Zou. *Robust average-reward Markov decision processes.* AAAI 2023.
- **[Wang et al., 2023c]** Wang, Velasquez, Atia, Prater-Bennette, Zou. *Model-free robust average-reward reinforcement learning.* ICML 2023.
- **[Wang et al., 2024]** Wang, Velasquez, Atia, Prater-Bennette, Zou. *Robust average-reward reinforcement learning.* Journal of Artificial Intelligence Research 2024.
- **[Wang & Si, 2025]** Wang, Si. *Bellman optimality of average-reward robust Markov decision processes with a constant gain.* arXiv 2025 (arXiv:2509.14203).
- **[Xu et al., 2025a]** Xu, Ganesh, Aggarwal. *Efficient Q-learning and actor-critic methods for robust average reward reinforcement learning.* arXiv 2025 (arXiv:2506.07040).
- **[Xu et al., 2025b]** Xu, Mondal, Aggarwal. *Finite-sample analysis of policy evaluation for robust average reward reinforcement learning.* arXiv 2025 (arXiv:2502.16816).
- **[Zhang et al., 2020]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Zheng & Guo, 2024]** Zheng, Guo. *Zero-sum non-stationary stochastic games with the long-run average criterion.* Applied Mathematics & Optimization 2024.
