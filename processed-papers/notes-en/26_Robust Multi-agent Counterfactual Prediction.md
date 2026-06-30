# 26. Robust Multi-agent Counterfactual Prediction

## Metadata
- **Title**: Robust Multi-agent Counterfactual Prediction
- **Authors**: Alexander Peysakhovich, Christian Kroer, Adam Lerer (equal contribution)
- **Affiliation**: Facebook AI Research; Facebook Core Data Science
- **Venue**: NeurIPS 2019
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness of counterfactual predictions to violations of modeling assumptions in multi-agent systems — specifically relaxing the equilibrium assumption, point-identification, and correct specification of agents' reward functions (modeled via ε-equilibrium / bounded-rationality slack).
- **Method paradigm**: Game-theoretic equilibrium (Bayesian games), partial identification, ε-Bayesian-Nash-equilibrium set bounds (optimistic/pessimistic), fictitious play (first-order learning), worst-case / best-case interval estimation.
- **Keywords**: counterfactual prediction, mechanism design, Bayesian Nash equilibrium, ε-equilibrium, partial identification, fictitious play

## TL;DR
The paper introduces Robust Multi-agent Counterfactual Prediction (RMAC), which recasts counterfactual estimation in multi-agent systems as finding the worst- and best-case ε-Bayesian-Nash equilibria of a "revelation game" to bound how sensitive counterfactual conclusions are to violations of rationality, identification, and model-specification assumptions, and proposes Revelation Game Fictitious Play (RFP) to compute these bounds.

## Problem & Motivation
A central practical task for mechanism designers is to observe an existing set of rules in operation and predict how outcomes would change if the rules changed. This is hard because (1) agents are strategic — their optimal actions change with the rules and with others' behavior — and (2) agents have private information (types/reward functions) not observed by the designer. Existing approaches (structural estimation, inverse reinforcement learning) assume agents optimize latent utilities, that the system is in (Bayesian Nash) equilibrium, that types are point-identified from observed actions, and that the model is correctly specified, then learn types and solve for the counterfactual equilibrium. These assumptions are strong and rarely exactly true: human decisions need not obey utility maximization, mistakes/biases persist, and models are at best approximately correct. The gap addressed is the absence of a general, application-agnostic way to test how robust counterfactual conclusions are to such violations (as opposed to standard statistical uncertainty, which assumes the model is exactly correct).

## Robustness Setting
- **Threat model / uncertainty set**: Rather than an adversarial perturbation of the environment, the "uncertainty set" is the set of ε-BNE of a constructed revelation game. Allowing ε regret relaxes Assumptions 1–4 (equilibrium in G, equilibrium in G′, identification, and correct specification of reward functions) simultaneously, since the revelation-game loss is the max of the G-regret and G′-regret. ε is interpretable in the units of the game (e.g., dollars of foregone utility in an auction). RMAC reports the infimum (pessimistic) and supremum (optimistic) of an evaluation function V (e.g., revenue, welfare, truthfulness) over this ε-BNE set.
- **Setting**: Multi-agent, mixed (cooperative/competitive depending on mechanism); offline / logged-data (uses a dataset D of actions previously played in game G to predict outcomes in counterfactual game G′); the revelation game has one "data-player" per logged observation.

## Method
- Show that, under standard assumptions, the counterfactual-estimation problem is equivalent to solving for the Bayesian Nash equilibrium of a constructed "revelation game" with m data-players (one per logged data point), where each data-player reports a type θ̂ⱼ and a counterfactual action âⱼ and minimizes the maximum of its G-Regret and G′-Regret. Theorem 1: under Assumptions 1–3 the revelation game has a unique BNE where each agent reveals its true type and counterfactual action.
- Relax the assumptions by replacing BNE with ε-BNE (each player has at most ε regret). This makes the solution set-valued; RMAC selects the boundary equilibria — the ε-pessimistic (inf of V) and ε-optimistic (sup of V) elements — yielding interval bounds (Definition 3).
- Establish hardness: computing ε-RMAC bounds exactly is NP-hard even for restricted cases (Theorem 2); the Appendix gives a mathematical program with equilibrium constraints and a MIP for two-player games.
- Propose Revelation Game Fictitious Play (RFP, Algorithm 1): adapt fictitious play so that, at each step, each data-player updates its (θ̂, â) by choosing — among the set of ε-best-responses to the historical play — the one that minimizes (pessimistic, α = −1) or maximizes (optimistic, α = +1) the evaluation function V.
- Characterize RFP convergence: if RFP converges, it converges to a locally V-optimal ε-BNE of the revelation game (Theorem 3), analogous to standard fictitious-play results; general convergence guarantees are left to future work.

## Theoretical Contributions
- Theorem 1: equivalence of counterfactual estimation to a unique-BNE revelation game under the standard assumptions.
- Theorem 2: NP-hardness of computing exact ε-RMAC bounds (even with a single feasible type per data point and two data points, or with finite types, no objective, and a two-player G′).
- Theorem 3: if pessimistic/optimistic RFP converges, the limit is a locally V-optimal ε-BNE of the revelation game (with Definitions 4–5 formalizing convergence and local V-optimality).
- Appendix: mathematical program with equilibrium constraints for pure-strategy ε-BNE and a MIP for two-player games.

## Experiments
- **Environment/Benchmark**: Classic market-design domains — (1) auctions: a first-price 2-player auction G with uniform [0,1] types and bids discretized at 0.01, with counterfactual games being 2-player second-price auctions with varying reserves and N-player first-price auctions; (2) school choice: a 3-student / 3-school assignment problem comparing the Boston mechanism vs. random serial dictatorship (RSD); (3) Appendix: an auction with non-identification and social choice.
- **Baselines**: Comparison against standard statistical uncertainty (standard-error / ε = 0 bounds shown as a grey ribbon); RMAC at several ε levels (e.g., 0, 0.001, 0.01) compared against each other rather than against competing algorithms.
- **Evaluation metrics**: Counterfactual expected revenue (auctions); change in social welfare and change in truthfulness (school choice); width of the RMAC interval vs. statistical standard-error bounds.

## Key Results
- In auctions, even very small ε produces RMAC revenue bounds far wider than statistical standard-error bounds: an ε of 0.01 corresponds to only ~4% misoptimization/misspecification (vs. a winner's average expected utility of 0.25) yet yields wide revenue intervals; a worst-case ε-equilibrium is expected to decrease counterfactual revenue by roughly √(2ε).
- Counterfactual estimates for auction reserve changes are asymmetric in robustness: increasing the reserve gives robust predictions, while decreasing the reserve does not.
- In school choice, when point identification fails (multiple type distributions consistent with observed Boston actions), RMAC with small ε still yields a valid interval covering both possibilities: switching Boston→RSD may increase truthfulness by 26% (if all types are A>B>C) or by 0% (if types matched the Boston actions); RSD→Boston has much tighter bounds because truthful RSD well-specifies the types.

## Limitations & Future Work
- Exact RMAC computation is NP-hard, so it is not expected to scale beyond small instances; the practical RFP method may cycle and is only guaranteed to converge to an ε-BNE if it converges (no general convergence guarantee).
- Theoretical study of RFP (or other learning algorithms in the revelation game), including convergence in specific Bayesian-game classes, is left to future work.
- Modifications to fictitious play are known to change real-world performance substantially; richer environments would require multi-agent learning with function approximation (e.g., deep-learning-based methods).
- Extending RMAC to no-regret learning as a solution concept, and combining it with optimal/automated mechanism design, are noted as promising directions.

## Relevance to Survey
This paper sits at the intersection of robustness and multi-agent systems but from a game-theoretic / mechanism-design and econometrics angle rather than the standard robust-MDP/MARL line. Its robustness notion is robustness of *counterfactual conclusions* to violations of equilibrium, identification, and specification assumptions, operationalized through ε-equilibrium sets and worst-case/best-case (optimistic/pessimistic) interval bounds. It connects to the survey's themes of worst-case/minimax robustness, partial identification under model misspecification, ε-equilibrium / bounded-rationality robustness, and learning-in-games (fictitious play) — offering a complementary, equilibrium-set view of robustness to the model-uncertainty and adversarial-RL lines that dominate robust MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.1, Related Work]_

"Our work is closely related to the notion of partial identiﬁcation (Manski, 2003). The main idea behind partial identiﬁcation is that many statistical models are only able to recover a set of parameters consistent with the data, not a single point estimate. The PI literature focuses on models where this 'identiﬁed set' can be extracted easily. The revelation game is strongly related in that the equilibrium relaxation we employ makes the counterfactual predictions a set rather than a point. We focus on ﬁnding this set's worst (in terms of some evaluation function) and best elements."

"Existing work in the ﬁeld of market design has used econometric techniques to estimate counterfactuals in speciﬁc applications (Athey and Nekipelov, 2010; Chawla et al., 2017; Agarwal, 2015). These approaches are, like ours, designed with the goal of answering counterfactual questions. However, while they allow for measures of statistical uncertainty they do not allow analysts to check for robustness of conclusions to violations of assumptions. Haile and Tamer (2003) consider using 'incomplete' models of auctions to provide some form of robustness but, like much of the literature on the econometrics of auctions (and unlike RMAC), requires hand-deriving estimators speciﬁcally tailored to the auction at hand."

"Since the pioneering work of Myerson (1981) there is a large subﬁeld of game theory dedicated to designing mechanisms that optimize some quantity (e.g. seller revenue). Myerson-style results often require the auctioneer to know the distribution of types (valuations) in the population. These strong assumptions are relaxed in robust mechanism design (Bergemann and Morris, 2005), automated mechanism design (Conitzer and Sandholm, 2002), and recent work in using deep learning methods to approximate optimal mechanisms (Dütting et al., 2017; Feng et al., 2018). Optimal mechanism design is related to, but different from, the RMAC problem as it typically assumes access to at least some direct information about the distribution of types, whereas the RMAC problem is to robustly infer the underlying types from observed actions. However, these problems are related and combining insights from these literatures with RMAC is an interesting direction for future work."

"There is recent interest in relaxing equilibrium assumptions in structural models. Nekipelov et al. (2015) consider replacing equilibrium assumptions with the assumption that individuals are no-regret learners. This, again, gives a set valued solution concept which can be worked out explicitly for the special case of auctions. Given the prominence of no-regret learning in algorithmic game theory a natural extension of the work in this paper is to consider expanding RMAC to learning as a solution concept."

> _[Introduction — prior-work discussion]_

"A common class of approaches to this question assume that observed actions are coming from a multi-agent system where all agents are optimizing some latent reward functions. In other words, that the system is in some form of Nash equilibrium. Further, they assume that once changes are made, the system will again equilibriate. Given these two assumptions, counterfactual prediction becomes a question of how equilibria change as the mechanism changes. Such assumptions are typical in the ﬁeld of inverse reinforcement learning (Ng et al., 2000) and in structural estimation in economics (Berry et al., 1995; Athey and Nekipelov, 2010)."

"A downside of this approach is that it requires strong assumptions that are not always completely true in practice. For example, this process requires assuming that agents are optimizing their utility given the behavior of others so that an analyst can infer underlying 'taste' parameters from agent actions. It is well known, however, that human decisions do not always obey the axioms of utility maximization (Camerer et al., 2011) and that both mistakes and biases can persist even when there is ample opportunity for learning (Erev and Roth, 1998; Fudenberg and Peysakhovich, 2016)."

### Cited references (resolved from the paper's bibliography)
- **Manski (2003)** Charles F. Manski. *Partial identification of probability distributions.* Springer Science & Business Media, 2003.
- **Athey and Nekipelov (2010)** Susan Athey, Denis Nekipelov. *A structural model of sponsored search advertising auctions.* Sixth Ad Auctions Workshop, Vol. 15, 2010.
- **Chawla et al. (2017)** Shuchi Chawla, Jason D. Hartline, Denis Nekipelov. *Mechanism Redesign.* arXiv:1708.04699, 2017.
- **Agarwal (2015)** Nikhil Agarwal. *An empirical model of the medical match.* American Economic Review 105(7), 2015.
- **Haile and Tamer (2003)** Philip A. Haile, Elie Tamer. *Inference with an incomplete model of English auctions.* Journal of Political Economy 111(1), 2003.
- **Myerson (1981)** Roger B. Myerson. *Optimal auction design.* Mathematics of Operations Research 6(1), 1981.
- **Bergemann and Morris (2005)** Dirk Bergemann, Stephen Morris. *Robust mechanism design.* Econometrica 73(6), 2005.
- **Conitzer and Sandholm (2002)** Vincent Conitzer, Tuomas Sandholm. *Complexity of mechanism design.* UAI 2002.
- **Dütting et al. (2017)** Paul Dütting, Zhe Feng, Harikrishna Narasimhan, David C. Parkes. *Optimal auctions through deep learning.* arXiv:1706.03459, 2017.
- **Feng et al. (2018)** Z. Feng, H. Narasimhan, D. C. Parkes. *Optimal auctions through deep learning.* AAMAS 2018.
- **Nekipelov et al. (2015)** Denis Nekipelov, Vasilis Syrgkanis, Eva Tardos. *Econometrics for learning agents.* ACM Conference on Economics and Computation (EC) 2015.
- **Ng et al. (2000)** Andrew Y. Ng, Stuart J. Russell, et al. *Algorithms for inverse reinforcement learning.* ICML 2000.
- **Berry et al. (1995)** Steven Berry, James Levinsohn, Ariel Pakes. *Automobile prices in market equilibrium.* Econometrica, 1995.
- **Camerer et al. (2011)** Colin F. Camerer, George Loewenstein, Matthew Rabin. *Advances in behavioral economics.* Princeton University Press, 2011.
- **Erev and Roth (1998)** Ido Erev, Alvin E. Roth. *Predicting how people play games: Reinforcement learning in experimental games with unique, mixed strategy equilibria.* American Economic Review, 1998.
- **Fudenberg and Peysakhovich (2016)** Drew Fudenberg, Alexander Peysakhovich. *Recency, records, and recaps: Learning and nonequilibrium behavior in a simple decision problem.* ACM Transactions on Economics and Computation (TEAC) 4(4), 2016.
