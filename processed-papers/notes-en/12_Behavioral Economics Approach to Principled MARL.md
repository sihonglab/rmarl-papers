# 12. Tractable Multi-Agent Reinforcement Learning through Behavioral Economics

## Metadata
- **Title**: Tractable Multi-Agent Reinforcement Learning through Behavioral Economics
- **Authors**: Eric Mazumdar, Kishan Panaganti, Laixi Shi (alphabetical order)
- **Affiliation**: Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, CA, USA
- **Venue**: ICLR 2025
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Risk-aversion to environment/dynamics uncertainty and to opponents' strategies (uncertainty caused by the environment and other players); bounded rationality (imperfect optimization). Modeled via convex risk measures with a dual (adversarial) representation rather than an explicit uncertainty-set / threat model.
- **Method paradigm**: Behavioral-economics-inspired equilibrium concept (risk-averse quantal response equilibrium, RQE); game-theoretic equilibrium; convex risk measures with dual (worst-case) formulation; no-regret learning / CCE-RQE equilibrium collapse; quantal response / entropy-style regularization; dynamic programming for finite-horizon Markov games; generative-model sample complexity.
- **Keywords**: risk-averse quantal response equilibrium (RQE), bounded rationality, risk aversion, convex risk measures, Markov games, no-regret learning

## TL;DR
The paper introduces risk-averse quantal response equilibria (RQE), a class of equilibria arising when agents are both risk-averse and boundedly rational, and shows that a subclass of RQE is computationally tractable (via no-regret learning) in all n-player matrix and finite-horizon Markov games, independent of the underlying game structure, while also fitting human play data and admitting finite-sample guarantees under a generative model.

## Problem & Motivation
Principled MARL is hampered because desirable solution concepts such as Nash equilibria (NE) are intractable to compute even for two-player matrix games, and relaxations like (coarse) correlated equilibria (CCE) have their own limitations (large equilibrium sets, support on dominated strategies, intractable stationary Markov CCE in general-sum Markov games). Moreover, NE and CCE are poor predictors of how people actually play, since humans are imperfect optimizers (bounded rationality) and risk-averse. The paper draws on behavioral economics to imbue agents with these two human features, seeking an equilibrium concept that is both behaviorally expressive and computationally tractable, thereby opening a path to principled decentralized MARL algorithms centered on RQE rather than CCE or NE.

## Robustness Setting
- **Threat model / uncertainty set**: Robustness enters through risk-aversion modeled with convex risk measures (Föllmer–Schied), whose dual representation casts each risk-averse player as facing "intermediate adversaries" that seek to maximize the player's cost but are penalized (via a penalty function D, scaled by 1/τ) for deviating from the opponents' realized strategies / nominal dynamics. As the risk-aversion parameter τ → ∞ the player treats opponents and environment as fully adversarial (recovering min-max / security strategies). In Markov games, two separate penalty functions handle risk toward opponents' strategies (Dpol) and toward the stochastic environment/transition dynamics (Denv); examples include ℓp-norm and total-variation penalties. Crucially, players are NOT risk-averse to the randomness of their own mixed strategy, only to environment and opponent uncertainty.
- **Setting**: n-player general-sum, mixed cooperative/competitive; decentralized learning (no-regret / gradient-play / mirror descent); both full-information (known model) and unknown-model with access to a generative model/simulator; finite-horizon Markov games.

## Method
- Generalize expected-utility games to risk-averse games using convex risk measures, considering action-dependent risk-aversion (Eq. 3) and aggregate risk-aversion (Eq. 4, the focus); apply the Dual Representation Theorem to rewrite the risk-averse cost as a supremum over adversary distributions penalized by D and scaled by 1/τ (Eq. 5), defining the risk-averse Nash equilibrium (RNE).
- Add a strictly convex regularizer ν (degree of bounded rationality ϵ) to obtain quantal responses, yielding the risk-averse quantal response equilibrium (RQE; Eq. 6 / Definition 5), which always exists in matrix games because the game stays convex.
- Construct a related 2n-player game pairing each player with an adversary (Eqs. 7–8) and show that coarse correlated equilibria (CCE) of this 2n-player game coincide with RQE of the original game (an "equilibrium collapse"); hence no-regret learning computes RQE. Theorem 3 gives the tractability condition for 2-player games (ϵ1ϵ2 ≥ ξ1* ξ2*), independent of payoffs.
- Extend to finite-horizon risk-averse Markov games (RAMGs) with risk-averse value functions defined recursively via fpol (opponent risk) and fenv (environment risk) (Eqs. 9–11); define Markov RQE (Definition 7).
- Compute Markov RQE by backward dynamic programming (Algorithm 1), constructing per-step risk-adjusted payoff matrices (Eq. 13) and solving a matrix-game RQE at each (s, h). For unknown models, build an empirical reward and nominal transition kernel from N samples per state-action (generative model / model-based MARL) and run the same algorithm.

## Theoretical Contributions
- Existence: all aggregate risk-averse games admit at least one RNE (Theorem 2); RQE always exist in matrix games.
- Tractability via equilibrium collapse: CCE of the constructed 2n-player game coincide with RQE; Theorem 3 gives payoff-independent conditions (on risk-aversion ξ* and bounded rationality ϵ) under which RQE are computable by no-regret learning in n-player matrix games.
- Markov games: Theorem 4 shows Algorithm 1 outputs a Markov RQE under a convexity + parameter condition, in contrast to Markov NE / Markov QRE which are intractable in general-sum Markov games.
- Sample complexity: Theorem 5 gives the first finite-sample guarantee for computing Markov RQE under a generative model, achieving a δ-RQE with Nall ≥ 8S(∏Ai)HL·sqrt((S/N)·log(2SH ∏Ai / δ)); the bound exhibits the "curse of multiagency" through the ∏i Ai dependence.

## Experiments
- **Environment/Benchmark**: (1) Behavioral-economics validation against human-play data in 13 different 2-player matrix games (matching-pennies-type games from Goeree et al., 2003 and Selten & Chmura, 2008), recovering average human strategies to within ~1% accuracy. (2) A Cliff Walk grid-world MARL benchmark: a 2-player grid where black cliff tiles give reward −2 (agents stuck), 0 per step and 1 for reaching each agent's goal; actions {up, down, left, right} succeed with probability pd = 0.9, reduced to pd = 0.5 when agents are at least a cell apart (multi-agent effect increasing cliff-fall risk); horizon H = 200; joint state = tuple of player positions.
- **Baselines**: Not specified (the paper compares RQE behavior against Nash equilibrium / human play conceptually and varies risk-aversion vs bounded-rationality regimes rather than competing algorithms).
- **Evaluation metrics**: Fit to observed human average strategies (parameter regime in Fig. 1 reproducing data); qualitative analysis of equilibrium policies / maximum-likelihood paths under varying risk-aversion (τ) and bounded-rationality (ϵ) levels.

## Key Results
- The computationally tractable RQE regime (blue region in Fig. 1, parameterized by τ1/τ2 and ϵ1/ϵ2) is rich enough to capture human play in the studied matrix games up to ~1% accuracy, showing RQE are behaviorally expressive while remaining tractable.
- In the Cliff Walk experiment, a more risk-averse / less boundedly-rational agent 2 prefers to hide far from obstacles, whereas a more risk-seeking agent 2 reaches its goal; agent 1's equilibrium strategy adapts accordingly (e.g., waiting until the path is clear), illustrating coupling between agents' risk preferences and learned policies.
- A class of Markov RQE is tractably computable via no-regret learning, with a generative-model sample-complexity bound (Theorem 5), in contrast to intractable Markov NE / Markov QRE.

## Limitations & Future Work
- The sample-complexity bound suffers from the curse of multiagency (dependence on ∏i Ai), limiting scalability in the number of agents/actions.
- Tractability holds only for parameter regimes satisfying the stated risk-aversion / bounded-rationality conditions (e.g., ϵ1ϵ2 ≥ ξ1*ξ2*); risk-averse NE/QRE without bounded rationality remain intractable in general.
- Empirical MARL validation is limited to a small grid-world (Cliff Walk); broader MARL benchmarks are not evaluated.
- The paper frames its contribution as opening the door to new decentralized MARL algorithms centered on RQE; concrete scalable algorithm design and large-scale deployment are left for future work.
- Detailed treatment of action-dependent risk-aversion and the in-depth related-work discussion are deferred to the supplementary material / Appendix A.

## Relevance to Survey
This paper connects robust MARL to risk-sensitive decision-making and behavioral game theory. Its dual representation of convex risk measures recasts risk-aversion as a penalized worst-case (adversarial) optimization over opponents' strategies and environment dynamics, directly linking to robust RL / robust MDP and distributionally robust RL/MARL lines (the τ → ∞ limit recovers min-max/security strategies). It bridges the "model/environment uncertainty" theme (via fenv robustness to transitions, with TV/ℓp penalties) and the "opponent/agent uncertainty" theme (via fpol robustness to other agents) under a single equilibrium concept (RQE), while emphasizing computational tractability and finite-sample guarantees—situating it among robust/risk-sensitive MARL works that prioritize principled, decentralized algorithms over intractable Nash-based robustness.

## Related Work (verbatim excerpts from the paper)
> _[Note: the paper defers its dedicated related-work discussion to "Appendix A," which is not included in the extracted text. The verbatim excerpts below are the prior-work discussions found in the Introduction and Section 2.]_

> _[Introduction]_

"When viewed through the lens of game theory, many of these problems can be cast as problems of equilibrium computation under varying information structures, where the equilibrium represents a stable outcome for rational agents. The most common equilibrium concept is that of a Nash equilibrium (NE) (Nash, 1950): a solution under which no rational agent has an incentive to unilaterally seek to improve their outcome. Despite its popularity as a solution concept, computing a NE outside of highly structured games is known to be computationally intractable even for two-player matrix games (Daskalakis, 2013). Coupled with a host of negative results on their computation using gradient-based algorithms (Mertikopoulos et al., 2018; Mazumdar et al., 2020), converging to Nash is increasingly viewed as an unreasonable goal for decentralized reinforcement learning algorithms."

> _[Introduction]_

"While relaxations of NE like (coarse) correlated equilibria (CCE) are known to be more tractable to compute—and thus a more attainable goal for learning algorithms— they also have their limitations. Indeed, while CCE arise out of the use of no-regret learning algorithms (Cesa-Bianchi and Lugosi, 2006), the set of CCE can be large (exacerbating the problem of equilibrium selection that arises with NE) and may have support on strictly dominated strategies (Viossat and Zapechelnyuk, 2013), which means that they cannot necessarily be rationalized by individual agents in isolation (Dekel and Fudenberg, 1990). Furthermore, a dynamic versions of CCE—stationary Markov CCE—can also be intractable to compute in general-sum Markov games (Daskalakis et al., 2023b)."

> _[Introduction]_

"Beyond these hardness results, solution concepts like NE and CCE also fail to be predictive of what strategies people play in games (McKelvey and Palfrey, 1995; Erev and Roth, 1998), with people being observed to be imperfect optimizers (Goeree and Holt, 1999; Capra et al., 2002) and risk-averse (Goeree et al., 2003) when confronted with game theoretic scenarios. This aligns with celebrated work in behavioral economics and mathematical psychology which has repeatedly shown that dominant features of human decision-making are a failure to perfectly optimize (Luce, 1959) and risk-aversion (Kahneman and Tversky, 1979; Tversky and Kahneman, 1992)."

> _[Introduction]_

"The first observation is often referred to as bounded rationality which posits that individuals are naturally prone to making mistakes and often fail to be perfectly optimal (Luce, 1959). This is often captured in games through the idea of a quantal response equilibrium (QRE) (McKelvey and Palfrey, 1995). The second observation can be attributed to the fact that players typically face uncertainty and risk in their decisions. These arise from environmental uncertainties like unknown future events, noise, or even the mere presence of other players. This can lead people to prefer risk-averse strategies, i.e., strategies which give more certain outcomes at the cost of lower expected returns (Gollier, 2001). Interestingly, there is experimental evidence that neither of these properties alone can account for people's patterns of play observed in controlled experiments (Goeree et al., 2003; Goeree and Offerman, 2002), and that models of decision-making that incorporate both of these features have the best predictive power (Goeree et al., 2003)."

> _[Section 2.1, Bounded Rationality in Games]_

"In contrast to risk-aversion, which has been under-explored in game theory and multi-agent reinforcement learning, bounded rationality is more common. Many works studying the computational benefits of incorporating it into games (Sokota et al., 2023; Mertikopoulos and Sandholm, 2016; Cen et al., 2021; Leonardos et al., 2021; Evans and Ganesh, 2024; Jacob et al., 2022), with the most common form of bounded rationality found in the literature on learning in games being that of a quantal response. These capture bounded rationality by either assuming that the players are rational in a stochastically perturbed version of the game or equivalently that players' strategies are constrained to the set of quantal response functions (McKelvey and Palfrey, 1995; 1998)."

> _[Section 2.1, Bounded Rationality in Games]_

"Despite the many works that focus on computing QRE, to the best of our knowledge there are no classes of QRE that are universally computable across all games. Indeed most works focus on zero-sum or approximately zero-sum games (Sokota et al., 2023; Mertikopoulos and Sandholm, 2016; Leonardos et al., 2021). In more general classes of games the class of QRE or equivalently the level of bounded rationality needed for computational tractability depends on the underlying game structure (e.g., the size of player's action spaces and the magnitude of their rewards) which may not be known a priori (Sun et al., 2024). Furthermore, we note that more work in behavioral economics has consistently highlighted that bounded rationality on its own is not enough to capture the nuances of human decision-making, even for simple games such as matching pennies (Goeree et al., 2003; Tversky and Kahneman, 1992). These findings motivate us to introduce risk-aversion into games."

> _[Section 2.2, Risk-Aversion in Games — Remark 1]_

"A crucial feature of our formulation of risk-aversion is that players are not risk-averse to the randomness introduced by their own strategy and only to the uncertainty caused by the environment and their opponents. This is a common approach taken (often implicitly) in the literature on single-agent risk-sensitive and robust decision-making (Shen et al., 2014). It also appears to be necessary to ensure the existence of equilibria introduced in Theorem 2 shortly; otherwise as studied in Fiat and Papadimitriou (2010), equilibria may not exist."

> _[Section 4, Risk-Averse Quantal Response Equilibria in Markov Games]_

"We remark that this definition reduces to the classical setup of multi-agent reinforcement learning (Zhang et al., 2021a) when agents are risk-neutral and to the well studied setup of risk-sensitive reinforcement learning (Shen et al., 2014) when there is only one agent."

> _[Section 4.2, Computing and Approximating Markov RQE]_

"A consequence of this result is that a class of Markov RQE are computationally tractable to compute via no-regret learning in finite-horizon Markov games. We remark that this is in stark contrast to both Markov Nash equilibria and Markov quantal response equilibria which cannot efficiently be computed in general-sum Markov games (Daskalakis et al., 2023b)."

### Cited references (resolved from the paper's bibliography)
- **[Nash, 1950]** J. F. Nash. *Non-cooperative games.* Princeton University, 1950.
- **[Daskalakis, 2013]** C. Daskalakis. *On the complexity of approximating a nash equilibrium.* ACM Transactions on Algorithms (TALG), 9(3):1–35, 2013.
- **[Mertikopoulos et al., 2018]** P. Mertikopoulos, C. Papadimitriou, G. Piliouras. *Cycles in adversarial regularized learning.* Proceedings of the Twenty-Ninth Annual ACM-SIAM Symposium on Discrete Algorithms, 2018.
- **[Mazumdar et al., 2020]** E. Mazumdar, L. J. Ratliff, S. S. Sastry. *On gradient-based learning in continuous games.* SIAM Journal on Mathematics of Data Science, 2(1):103–131, 2020.
- **[Cesa-Bianchi and Lugosi, 2006]** N. Cesa-Bianchi, G. Lugosi. *Prediction, learning, and games.* Cambridge University Press, 2006.
- **[Viossat and Zapechelnyuk, 2013]** Y. Viossat, A. Zapechelnyuk. *No-regret dynamics and fictitious play.* Journal of Economic Theory, 148(2):825–842, 2013.
- **[Dekel and Fudenberg, 1990]** E. Dekel, D. Fudenberg. *Rational behavior with payoff uncertainty.* Journal of Economic Theory, 52(2):243–267, 1990.
- **[Daskalakis et al., 2023b]** C. Daskalakis, N. Golowich, K. Zhang. *The complexity of markov equilibrium in stochastic games.* Proceedings of Thirty Sixth Conference on Learning Theory (COLT), PMLR vol. 195, 2023.
- **[McKelvey and Palfrey, 1995]** R. D. McKelvey, T. R. Palfrey. *Quantal response equilibria for normal form games.* Games and Economic Behavior, 10(1):6–38, 1995.
- **[McKelvey and Palfrey, 1998]** R. D. McKelvey, T. R. Palfrey. *Quantal response equilibria for extensive form games.* Experimental Economics, 1:9–41, 1998.
- **[Erev and Roth, 1998]** I. Erev, A. Roth. *Predicting how people play games: Reinforcement learning in experimental games with unique, mixed strategy equilibria.* American Economic Review, 88(4):848–81, 1998.
- **[Goeree and Holt, 1999]** J. K. Goeree, C. A. Holt. *Stochastic game theory: For playing games, not just for doing theory.* Proceedings of the National Academy of Sciences, 96(19):10564–10567, 1999.
- **[Capra et al., 2002]** C. M. Capra, J. K. Goeree, R. Gomez, C. A. Holt. *Learning and noisy equilibrium behavior in an experimental study of imperfect price competition.* International Economic Review, 43(3):613–636, 2002.
- **[Goeree et al., 2003]** J. K. Goeree, C. A. Holt, T. R. Palfrey. *Risk averse behavior in generalized matching pennies games.* Games and Economic Behavior, 45(1):97–113, 2003.
- **[Luce, 1959]** R. D. Luce. *Individual Choice Behavior: A Theoretical Analysis.* Wiley, 1959.
- **[Kahneman and Tversky, 1979]** D. Kahneman, A. Tversky. *Prospect theory: An analysis of decision under risk.* Econometrica, 47(2):263–291, 1979.
- **[Tversky and Kahneman, 1992]** A. Tversky, D. Kahneman. *Advances in prospect theory: Cumulative representation of uncertainty.* Journal of Risk and Uncertainty, 5:297–323, 1992.
- **[Gollier, 2001]** C. Gollier. *The economics of risk and time.* MIT Press, 2001.
- **[Goeree and Offerman, 2002]** K. Goeree, T. Offerman. *Efficiency in auctions with private and common values: An experimental study.* American Economic Review, 92(3):625–643, 2002.
- **[Sokota et al., 2023]** S. Sokota, R. D'Orazio, J. Z. Kolter, N. Loizou, M. Lanctot, I. Mitliagkas, N. Brown, C. Kroer. *A unified approach to reinforcement learning, quantal response equilibria, and two-player zero-sum games.* ICLR 2023.
- **[Mertikopoulos and Sandholm, 2016]** P. Mertikopoulos, W. H. Sandholm. *Learning in games via reinforcement and regularization.* Mathematics of Operations Research, 41(4):1297–1324, 2016.
- **[Cen et al., 2021]** S. Cen, Y. Wei, Y. Chi. *Fast policy extragradient methods for competitive games with entropy regularization.* Advances in Neural Information Processing Systems 34, 2021.
- **[Leonardos et al., 2021]** S. Leonardos, G. Piliouras, K. Spendlove. *Exploration-exploitation in multi-agent competition: Convergence with bounded rationality.* Advances in Neural Information Processing Systems 34, 2021.
- **[Evans and Ganesh, 2024]** B. P. Evans, S. Ganesh. *Learning and calibrating heterogeneous bounded rational market behaviour with multi-agent reinforcement learning.* arXiv:2402.00787, 2024.
- **[Jacob et al., 2022]** A. P. Jacob, D. J. Wu, G. Farina, A. Lerer, H. Hu, A. Bakhtin, J. Andreas, N. Brown. *Modeling strong and human-like gameplay with kl-regularized search.* ICML 2022.
- **[Sun et al., 2024]** Y. Sun, T. Liu, P. R. Kumar, S. Shahrampour. *Linear convergence of independent natural policy gradient in games with entropy regularization.* IEEE Control Systems Letters, 8:1217–1222, 2024.
- **[Shen et al., 2014]** Y. Shen, M. J. Tobia, T. Sommer, K. Obermayer. *Risk-sensitive reinforcement learning.* Neural Computation, 26(7):1298–1328, 2014.
- **[Fiat and Papadimitriou, 2010]** A. Fiat, C. Papadimitriou. *When the players are not expectation maximizers.* Algorithmic Game Theory: Third International Symposium (SAGT 2010), Springer, 2010.
- **[Zhang et al., 2021a]** K. Zhang, Z. Yang, T. Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, pages 321–384, 2021.
