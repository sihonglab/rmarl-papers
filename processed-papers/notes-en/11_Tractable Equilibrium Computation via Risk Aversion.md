# 11. Tractable Equilibrium Computation in Markov Games through Risk Aversion

## Metadata
- **Title**: Tractable Equilibrium Computation in Markov Games through Risk Aversion
- **Authors**: Eric Mazumdar, Kishan Panaganti, Laixi Shi (alphabetical order; equal contribution)
- **Affiliation**: California Institute of Technology (Department of Computing + Mathematical Sciences; Department of Economics)
- **Venue**: Not specified (arXiv preprint, August 2024)
- **Link/arXiv**: arXiv:2406.14156v2 [cs.GT]

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental uncertainty (reward/transition) and opponent-strategy randomness, handled via risk-aversion; closely linked to distributionally robust RL/MARL through duality (worst-case disturbances within a ball around the nominal model / opponent distribution).
- **Method paradigm**: Game-theoretic equilibrium; risk-sensitive / risk-averse decision-making; convex risk measures + dual representation; bounded rationality (quantal response); no-regret learning; equilibrium collapse (CCE = NE = RQE in an augmented 2n-player game).
- **Keywords**: risk-averse quantal response equilibrium (RQE), behavioral economics, bounded rationality, convex risk measures, Markov games, distributional robustness, sample complexity

## TL;DR
The paper introduces risk-averse quantal response equilibria (RQE) — combining risk-aversion (to opponents' and the environment's randomness) and bounded rationality — and shows that a class of RQE is computationally tractable (computable via no-regret learning) in all n-player matrix games and finite-horizon Markov games, with tractability depending only on agents' risk-aversion and bounded-rationality parameters rather than on the game structure, plus a first finite-sample guarantee for learning RQE with a generative model.

## Problem & Motivation
Desired MARL solution concepts such as Nash equilibria (NE) are intractable to compute (PPAD-hard even for two-player general-sum matrix games), and relaxations like (coarse) correlated equilibria (CCE) have drawbacks: they require coordination, raise an equilibrium-selection problem, may put support on dominated strategies, and stationary CE/CCE are intractable in dynamic Markov games. Moreover, NE and CCE poorly predict how people actually play games — people are observed to be imperfect optimizers (bounded rational) and risk-averse. Drawing on behavioral economics, the paper asks whether imbuing agents with these human features yields a tractable, individually rationalizable equilibrium concept. Risk-aversion alone can destroy game structure (e.g., a zero-sum game loses its zero-sum/strictly-competitive structure) and is insufficient for tractability; bounded rationality (quantal responses) is added to recover a tractable class.

## Robustness Setting
- **Threat model / uncertainty set**: Agents are risk-averse to the randomness introduced by opponents' mixed strategies and (in Markov games) to environmental randomness in rewards and transitions — but crucially NOT to their own randomness (otherwise an equilibrium may not exist). Risk is modeled with general convex risk measures whose dual representation introduces an "intermediate adversary" that maximizes the agent's cost over a ball around the nominal opponent/environment distribution, defined via a penalty function D(p, q) (e.g., KL, reverse-KL, ϕ-divergence, utility-based shortfall). Environmental risk uses penalty Denv,i over the transition kernel (e.g., TV/ℓ1, ϕ-divergence). Via duality this connects to distributionally robust RL.
- **Setting**: competitive / cooperative / mixed (general-sum n-player matrix games and finite-horizon Markov games); full-information (perfect model) and MARL with a generative model / simulator (sampling); equilibria computable in a decentralized manner via no-regret learning.

## Method
- **Risk-adjusted games**: Transform expected-utility games into risk-adjusted cost games using convex risk measures, in two forms — aggregate risk aversion (Eq. 3/5; simpler, more conservative) and action-dependent risk aversion (Eq. 4/6; less conservative, harder). The dual representation theorem (Theorem 1) rewrites risk as a sup over an adversary distribution penalized by D(p, π).
- **Existence**: Because players are risk-averse only to others' randomness, the risk-adjusted objective is convex in the player's own strategy, so a risk-averse Nash equilibrium (RNE) always exists in all such games for any convex risk measure (Theorem 2).
- **Bounded rationality / RQE**: Constrain players to quantal responses (e.g., logit via negative-entropy regularizer, or log-barrier regularizer) by adding strictly convex regularization ϵ_i ν_i(π_i) (Eq. 8). The equilibrium of this risk-adjusted, regularized game is the risk-averse quantal response equilibrium (RQE) (Definition 5).
- **Tractability via equilibrium collapse**: Construct an auxiliary 2n-player game by associating an adversary p_i to each player (losses J_i in Eq. 9 and ̄J_i in Eq. 10 with parameters ξ_{i,j}). Show CCE = NE of the 2n-player game = RQE of the original game. Hence RQE is computable by any no-regret learning algorithm (gradient-play, mirror descent) when the risk-aversion / bounded-rationality parameters satisfy a simple relationship (Theorems 3, 6, 7, 8) — a condition independent of the payoff matrices.
- **Markov-game extension**: Define risk-averse Markov games (RAMGs) with two risk measures f^π_pol,i (opponent/strategy risk) and f_env,i (environment risk), recursive risk-averse value functions (Eqs. 12–16), and RQE for Markov games (Definition 7). Algorithm 1 solves backward in time, calling a matrix-game RQE solver at each (state, step). For unknown environments, build empirical reward/transition from N generative-model samples per state-action pair and run Algorithm 1.

## Theoretical Contributions
- Existence of risk-averse Nash equilibria in all aggregate and action-dependent risk-averse matrix games for any convex risk measure (Theorem 2).
- Computational tractability of a class of RQE via no-regret learning in 2-player (Theorem 3 / restated Theorem 6) and n-player (Theorem 7; action-dependent Theorem 8) matrix games, with the tractable class depending only on risk-aversion and bounded-rationality parameters, not the game structure. Specialized corollaries for entropic risk + log-barrier and reverse-KL + negative-entropy (Corollaries 6.1, 6.2).
- Tractable RQE computation for finite-horizon RAMGs with perfect information (Theorem 4, via Algorithm 1).
- First finite-sample complexity guarantee for learning a δ-RQE in RAMGs with a generative model: N_all ≥ 8 S ∏_i A_i H L √( (S/N) log( 2 S H ∏_i A_i / δ ) ) (Theorem 5; proof in Appendix C).
- Counterexample (Example 1) showing risk-aversion can destroy zero-sum / strict-competitiveness structure.

## Experiments
- **Environment/Benchmark**: (1) Thirteen 2-player matrix games from experimental behavioral economics — generalized matching pennies / matching-pennies games (Goeree–Holt–Palfrey Game 4 [28]; Selten–Chmura Games 1–12 [59], payoffs in Tables 2 and 3). (2) A 6×6 multi-agent "Cliff Walk" gridworld Markov game (cliff reward −2, step reward 0, goal reward 1; movement in intended direction with p_d = 0.9, reduced to 0.5 when agents are within one grid of each other; horizon H = 200). Appendix D.2 repeats with cliff −100 / goal 20 / step −0.1, H = 100, and an ℓ1 environmental-uncertainty metric.
- **Baselines**: Risk-neutral QRE / Nash strategies and observed human play (used as a comparison target rather than algorithmic baselines).
- **Evaluation metrics**: Match between tractable-RQE strategies and human-played aggregate strategies (up to ~1% accuracy in Fig. 1); qualitative behavior of learned policies in the gridworld (risk-averse vs. bounded-rational path choices); statistical deviation across runs (~2% sup-norm deviation over ~20 runs).

## Key Results
- The regime of risk-aversion / bounded-rationality parameters for which RQE are tractable is rich enough to capture observed human play in 13 different 2-player games (Fig. 1), recovering risk-averse and bounded-rational human behavior at up to ~1% accuracy; risk-averse QRE fit human data better than risk-neutral QRE.
- In the Cliff Walk gridworld, learned policies display intuitive risk-averse behavior: e.g., one agent takes a longer/safer route to avoid the cliff, another avoids the first agent's path to reduce falling risk, and an agent waits at a corner until the other passes — and tuning (ϵ_j, τ_j) trades off risk-aversion against goal-reaching (bounded rationality), consistent with Theorem 4.
- The tractable class of RQE is independent of the underlying payoffs, so the same class of quantal responses is tractable in all finite-action games and finite-horizon Markov games (unlike QRE/NE whose tractable regime depends on game structure).

## Limitations & Future Work
- Computing exact RQE can be computationally expensive; the work provides approximate (δ-)RQE guarantees and notes exact computation may be unnecessary in practice.
- Theorem 5's sample-complexity proof is given explicitly for ℓ1/TV-type Denv (L Lipschitz); the authors only allude (not full proofs) to analogous guarantees for ϕ-divergence penalties.
- Experiments are small-scale (matching-pennies matrix games and a 6×6 gridworld); no large-scale MARL benchmarks.
- The paper does not investigate the effects of different environmental-uncertainty metrics (KL vs. ℓ1) and postpones this to future research.
- Results do not necessarily guarantee uniqueness of RQE (though monotone/socially-convex game connections might yield it).

## Relevance to Survey
This paper sits at the intersection of the "risk-sensitive / risk-averse MARL" and "robust / distributionally robust MARL" method lines, explicitly bridging them via classical duality between risk-sensitivity and distributional robustness. Its central message — that risk-aversion plus bounded rationality yields a computationally tractable, individually rationalizable equilibrium concept in all finite-horizon n-player Markov games, learnable by no-regret algorithms — addresses a core obstacle in robust MARL (existence and tractability of robust equilibria). It directly engages with and contrasts against robust-MARL equilibrium-tractability results (PPAD-hardness of robust NE outside zero-sum) and robust-MARL works targeting environmental uncertainty, making it a key reference for the "computational tractability of robust/risk-averse equilibria" theme and a complement to robust-Markov-game foundations such as [75] (Zhang et al. 2020) and [32] (He et al. 2023).

## Related Work (verbatim excerpts from the paper)

### Computational tractability of game theoretic solution concepts
> _[Section 1.1, Related Works — "Computational tractability of game theoretic solution concepts."]_

"This work proposes a new solution concept for game theoretic settings that is computationally tractable, yet retains many of the desirable properties of classical equilibrium concepts. This general question emerged from the finding that computing a Nash equilibrium—perhaps the most natural solution concept for a game between rational self-interested agents—is PPAD-hard [14], even for two-player general-sum matrix games. Despite this negative result, a large amount of subsequent work has focused on understanding the classes of games in which one can compute, approximate, or learn Nash equilibria efficiently. This is often done by assuming additional structure on the players' utilities and their relationships to one another, with large classes of games being zero-sum or competitive games, zero-sum polymatrix games [10,38], monotone games [31], smooth games [57], or socially concave games [21]."

> _[Section 1.1, Related Works — continued]_

"In games without such structure however, the natural targets for computation and learning became correlated [49] and coarse correlated equilibria [4, 5](CE and CCE respectively), both of which can be shown to emerge as the endpoint of no-regret learning and are thus considered to be computationally tractable targets for the design of learning algorithms. Despite this desirable property, the two concepts have significant drawbacks. Indeed both CE and CCE require some form of coordination between players to implement, introduce a highly nontrivial equilibrium selection problem [13], and may have support on dominated strategies [70]. Furthermore, in the dynamic game context of Markov games, stationary CE and CCE are also computationally intractable to compute [16]."

> _[Section 1.1, Related Works — continued]_

"More recently, a new equilibrium concept—a smoothed Nash equilibrium— has been proposed as an alternative to these other equilibrium concepts [15] and motivated by similar considerations of individual and independent rationalizability and computational tractability. By applying ideas from smoothed analysis to the problem of computing Nash equilibria the authors show that one can efficiently find approximate classes of smoothed Nash equilibria—though to the best of our knowledge this cannot be done in a decentralized way. Our approach is orthogonal and is rooted in giving MARL agents a foundation rooted in behavioral economics by imbuing them with a realistic feature of human decision-making: risk-aversion. The question of computational tractability of risk-averse Nash equilibria has been analyzed in [22]. The work shows that if agents are risk-averse with respect to all the randomness in the game (including their own) then a risk-averse Nash equilibrium may not even exist in mixed strategies, and even understanding if such equilibria exist can be NP-complete. Our formulation overcomes this by incorporating risk-aversion in a different way. Indeed, we show that when agents are risk-averse only to the randomness introduced to their opponents (and the environment) then the risk-averse Nash equilibria will always exist. We note that such formulations of risk-aversion are common in the literature on risk-sensitive control [8,62] and risk-sensitive reinforcement learning [63] where agents are implicitly presumed to be risk-averse only to the randomness that is outside their control (i.e., the environment). Furthermore we show that introducing bounded rationality into the game allows a class of risk-averse quantal response equilibria (RQE) to be computationally tractable in all finite action and finite-horizon Markov games."

### Predictive power of equilibrium concepts
> _[Section 1.1, Related Works — "Predictive power of equilibrium concepts."]_

"Another driving force in moving beyond the Nash and correlated equilibrium concepts stems from their lack of predictive power in experimental settings (see e.g., [9,18,43,44,52]). To address this, a line of work originating in economics seeks to understand the natural solution concepts in game where players have behaviorally plausible restrictions to their strategy spaces, and to study whether such equilibria were better predictors of human play than Nash or (coarse) correlated equilibria [28,29,33]. The most common restriction is that players have bounded rationality,—i.e., they may fail to perfectly optimize—a model with roots in mathematical psychology [42]. Under this restriction, a natural equilibrium concept that emerged was that of a quantal response equilibrium (QRE) which induces bounded rationality by either assuming that the players are rational in a stochastically perturbed version of the game or equivalently that they optimize a regularized version of their utility [44,45,47]. Beyond their use as a better model for human decision-making in games, QRE have also increasingly been adopted as a solution concept in multi-agent reinforcement learning and learning in games [12, 20, 35, 41, 47, 68] due to their links with KL and entropy regularized reinforcement learning. Despite these developments QRE are not computable in all games. Indeed the class of QRE or equivalently the level of bounded rationality needed for computational tractability depends on the underlying game structure which may not be known a priori. In contrast we show that the addition of risk aversion allows for the same class of quantal response equilibria to be computationally tractable to compute in all finite action games and finite-horizon Markov games. Furthermore we show that this class of risk-averse QRE is nontrivial and can capture human data better than risk-neutral QRE—a finding which is in line with findings in behaviorial economics [28,29]."

### Risk-averse and robust multi-agent reinforcement learning
> _[Section 1.1, Related Works — "Risk-averse and robust multi-agent reinforcement learning."]_

"Our work builds on and provides an additional justification for risk-sensitive (multi-agent) reinforcement learning. This line of work has roots going back to seminal work by Jacobson on risk-sensitive control [36], and more recently in risk-sensitive reinforcement learning [63]. In these works, the aim is to find a controller or policy for a system that accounts for stochasticity or uncertainty in the environment or system in a more nuanced way than risk-neutral approaches like optimal control or reinforcement learning [8]. Due to classic duality results (see e.g., [77]) this line of work is closely related to the literature on robust control and distributionally robust reinforcement learning [34,53,64,73] which seeks to find solutions that are robust to worst case environmental disturbances. Our work rigorously extends these formulations to the multi-agent regime though it is not the first to consider risk-aversion in MARL. Indeed, risk-sensitive MARL has been the focus of several recent works (e.g., [25,67,71,74]). Several provide rigorous definitions of risk-averse equilibria and some guarantees on their computation by assuming structure on the risk-adjusted game. Oftentimes this is done by assuming that the risk-adjusted game is itself zero-sum [74], monotone [71], or that it satisfies other strong conditions [25]. Other works are more empirical in nature [19,24,55,61,67,78], showing the promise of risk-averse algorithms for MARL."

> _[Section 1.1, Related Works — continued]_

"One last closely related line of work is the emerging literature on robust multi-agent reinforcement learning [7,32,66,75]. Once again due to duality arguments, these works can be seen as tackling a similar problem to the risk-averse MARL problem. The focus of these previous works, however, is on robustness in the face of only environmental uncertainties (and not opponent strategies), and questions of existence and computational tractability are either assumed away or the focus is on extensions of correlated equilibrium concepts. A recent related work in this literature analyzed the computational tractability of robust Nash equilibria in Markov games, but only provided strong guarantees on the zero-sum regime, showing that computing such equilibria in general is PPAD-hard [46]. To the best of our knowledge, no previous work in either of these literatures highlights the broad benefits afforded by risk-aversion in MARL in terms of computational tractability of equilibria. In our work we show that risk-aversion (and by extension distributional robustness), when combined with bounded rationality yields a computationally tractable class of individually rationalizable equilibria in all finite-horizon n-player Markov games. Furthermore we show that these equilibria can be computed using no-regret learning algorithms."

### Cited references (resolved from the paper's bibliography)
- **[4]** R. J. Aumann. *Subjectivity and correlation in randomized strategies.* Journal of Mathematical Economics 1974.
- **[5]** R. J. Aumann. *Correlated equilibrium as an expression of Bayesian rationality.* Econometrica 1987.
- **[7]** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning: Generic algorithm and robust partial coverage.* NeurIPS 2024.
- **[8]** V. Borkar. *Risk-sensitive control, single controller games and linear programming.* Journal of Dynamics and Games 2023.
- **[9]** Brown, Rosenthal. *Testing the minimax hypothesis: A re-examination of O'Neill's game experiment.* Econometrica 1990.
- **[10]** Cai, Candogan, Daskalakis, Papadimitriou. *Zero-sum polymatrix games: A generalization of minmax.* Mathematics of Operations Research 2016.
- **[12]** Cen, Wei, Chi. *Fast policy extragradient methods for competitive games with entropy regularization.* NeurIPS 2021.
- **[13]** Cesa-Bianchi, Lugosi. *Prediction, learning, and games.* Cambridge University Press 2006.
- **[14]** C. Daskalakis. *On the complexity of approximating a Nash equilibrium.* ACM Transactions on Algorithms 2013.
- **[15]** Daskalakis, Golowich, Haghtalab, Shetty. *Smooth Nash equilibria: Algorithms and complexity.* arXiv 2023.
- **[16]** Daskalakis, Golowich, Zhang. *The complexity of Markov equilibrium in stochastic games.* COLT 2023.
- **[18]** Erev, Roth. *Predicting how people play games: Reinforcement learning in experimental games with unique, mixed strategy equilibria.* American Economic Review 1998.
- **[19]** Eriksson, Basu, Alibeigi, Dimitrakakis. *Risk-sensitive Bayesian games for multi-agent reinforcement learning under policy uncertainty.* arXiv 2022.
- **[20]** Evans, Ganesh. *Learning and calibrating heterogeneous bounded rational market behaviour with multi-agent reinforcement learning.* arXiv 2024.
- **[21]** Even-Dar, Mansour, Nadav. *On the convergence of regret minimization dynamics in concave games.* STOC 2009.
- **[22]** Fiat, Papadimitriou. *When the players are not expectation maximizers.* SAGT 2010.
- **[24]** Ganesh, Vadori, Xu, Zheng, Reddy, Veloso. *Reinforcement learning for market making in a multi-agent dealer market.* NeurIPS 2019.
- **[25]** Gao, Lui, Hernandez-Leal. *Robust risk-sensitive reinforcement learning agents for trading markets.* arXiv 2021.
- **[28]** Goeree, Holt, Palfrey. *Risk averse behavior in generalized matching pennies games.* Games and Economic Behavior 2003.
- **[29]** Goeree, Offerman. *Efficiency in auctions with private and common values: An experimental study.* American Economic Review 2002.
- **[31]** Golowich, Pattathil, Daskalakis. *Tight last-iterate convergence rates for no-regret learning in multi-player games.* NeurIPS 2020.
- **[32]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* TMLR 2023.
- **[33]** Ho, Camerer, Chong. *A cognitive hierarchy model of games.* Quarterly Journal of Economics 2004.
- **[34]** G. N. Iyengar. *Robust dynamic programming.* Mathematics of Operations Research 2005.
- **[35]** Jacob, Wu, Farina, Lerer, Hu, Bakhtin, Andreas, Brown. *Modeling strong and human-like gameplay with KL-regularized search.* ICML 2022.
- **[36]** D. Jacobson. *Optimal stochastic linear systems with exponential performance criteria and their relation to deterministic differential games.* IEEE Transactions on Automatic Control 1973.
- **[38]** Kalogiannis, Panageas. *Zero-sum polymatrix Markov games: Equilibrium collapse and efficient computation of Nash equilibria.* 2023.
- **[41]** Leonardos, Piliouras, Spendlove. *Exploration-exploitation in multi-agent competition: Convergence with bounded rationality.* NeurIPS 2021.
- **[42]** R. D. Luce. *Individual Choice Behavior: A Theoretical Analysis.* Wiley 1959.
- **[43]** McKelvey, Palfrey. *An experimental study of the centipede game.* Econometrica 1992.
- **[44]** McKelvey, Palfrey. *Quantal response equilibria for normal form games.* Games and Economic Behavior 1995.
- **[45]** McKelvey, Palfrey. *Quantal response equilibria for extensive form games.* Experimental Economics 1998.
- **[46]** McMahan, Artiglio, Xie. *Roping in uncertainty: Robustness and regularization in Markov games.* ICML 2024.
- **[47]** Mertikopoulos, Sandholm. *Learning in games via reinforcement and regularization.* Mathematics of Operations Research 2016.
- **[49]** Moulin, Vial. *Strategically zero-sum games: The class of games whose completely mixed equilibria cannot be improved upon.* International Journal of Game Theory 1978.
- **[52]** B. O'Neill. *Nonmetric test of the minimax theory of two-person zerosum games.* PNAS 1987.
- **[53]** Panaganti, Kalathil. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML 2021.
- **[55]** Qiu, Wang, Yu, Wang, He, An, Obraztsova, Rabinovich. *RMIX: Learning risk-sensitive policies for cooperative reinforcement learning agents.* NeurIPS 2021.
- **[57]** T. Roughgarden. *Intrinsic robustness of the price of anarchy.* Journal of the ACM 2015.
- **[61]** Shen, Ma, Li, Liu, Fu, Mei, Liu, Wang. *RiskQ: Risk-sensitive multi-agent reinforcement learning value factorization.* NeurIPS 2023.
- **[62]** Shen, Stannat, Obermayer. *Risk-sensitive Markov control processes.* SIAM Journal on Control and Optimization 2013.
- **[63]** Shen, Tobia, Sommer, Obermayer. *Risk-sensitive reinforcement learning.* Neural Computation 2014.
- **[64]** Shi, Chi. *Distributionally robust model-based offline reinforcement learning with near-optimal sample complexity.* arXiv 2022.
- **[66]** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* arXiv 2024.
- **[67]** Slumbers, Mguni, Blumberg, Mcaleer, Yang, Wang. *A game-theoretic framework for managing risk in multi-agent systems.* ICML 2023.
- **[68]** Sokota, D'Orazio, Kolter, Loizou, Lanctot, Mitliagkas, Brown, Kroer. *A unified approach to reinforcement learning, quantal response equilibria, and two-player zero-sum games.* ICLR 2023.
- **[70]** Viossat, Zapechelnyuk. *No-regret dynamics and fictitious play.* Journal of Economic Theory 2013.
- **[71]** Wang, Shen, Zavlanos, Johansson. *Learning of Nash equilibria in risk-averse games.* arXiv 2024.
- **[73]** Xu, Panaganti, Kalathil. *Improved sample complexity bounds for distributionally robust reinforcement learning.* AISTATS 2023.
- **[74]** Yekkehkhany, Murray, Nagi. *Risk-averse equilibrium for games.* arXiv 2020.
- **[75]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[77]** Zhang, Hu, Li. *Soft robust MDPs and risk-sensitive MDPs: Equivalence, policy gradient, and sample complexity.* ICLR 2024.
- **[78]** Zhang, Liu, Whiteson. *Mean-variance policy iteration for risk-averse reinforcement learning.* AAAI 2021.
