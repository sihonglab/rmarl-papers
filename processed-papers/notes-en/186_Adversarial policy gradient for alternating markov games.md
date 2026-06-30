# 186. Adversarial Policy Gradient for Alternating Markov Games

## Metadata
- **Title**: Adversarial Policy Gradient for Alternating Markov Games
- **Authors**: Chao Gao, Martin Müller, Ryan Hayward
- **Affiliation**: University of Alberta (email domain ualberta.ca)
- **Venue**: ICLR 2018 (Workshop track)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Worst-case / adversarial opponent in two-player zero-sum alternating-turn games (estimate the minimum rather than the mean return); robustness motivated by analogy to robust adversarial RL where errors occur in simulated models.
- **Method paradigm**: Adversarial policy gradient, minimax / worst-case "critic", generalized policy iteration, self-play, Monte Carlo policy gradient (REINFORCE variants), actor-critic, game-theoretic (Alternating Markov Games).
- **Keywords**: Alternating Markov Games, adversarial policy gradient, minimax, self-play REINFORCE, Monte Carlo policy gradient, Hex

## TL;DR
The paper derives an adversarial policy gradient objective tailored to two-player zero-sum Alternating Markov Games (AMGs) — switching the opponent to "greedy" (min/max) when computing each player's gradient — and shows that estimating the minimum rather than the mean return in self-play Monte Carlo policy gradient yields stronger pure neural-net Hex players that, combined with search, consistently beat the prior state-of-the-art MoHex 2.0 from 9×9 to 13×13.

## Problem & Motivation
Standard RL policy gradient methods (e.g., self-play REINFORCE in AlphaGo) have been applied to two-player alternate-turn zero-sum games by simply negating the opponent's reward, treating the game as a single-agent MDP. The paper argues this ignores the two-agent nature of AMGs: the corresponding Bellman equations and resulting policy iteration algorithms are fundamentally different from MDPs. Naively computing gradients for both policies simultaneously (treating the other as a static environment) ignores that the opponent is a dynamic adversary that also adapts, and an alternating fix-and-optimize scheme is analogous to a policy-iteration variant (Algo.1) known to be non-convergent in general. The gap is therefore a principled policy gradient formulation that reflects the convergent policy-iteration schemes for AMGs.

## Robustness Setting
- **Threat model / uncertainty set**: The opponent is treated as a worst-case adversary; when computing one player's policy gradient, the other player is switched to "greedy" (the max player faces the opponent's min response and vice versa), forcing each player to adjust action preferences according to the worst-case response. The "critic" estimates the minimum (worst-case) return rather than the mean. No explicit uncertainty set over models is constructed; robustness is by analogy to robust adversarial RL.
- **Setting**: competitive (two-player zero-sum, alternating-turn); self-play (π1 and π2 share parameters); online / model-free RL.

## Method
- Reviews the distinct Bellman equations for AMGs (separate value/action-value functions for the two players, with the optimal recursion alternating max at the max player's states and min at the min player's states), and reviews the four candidate policy-iteration schemes (Algo.1–Algo.4); only Algo.3 and Algo.4 (which switch one player to greedy and then compute the optimal counter policy for the other) are guaranteed to converge.
- Formulates an adversarial policy gradient objective (Eq. 12) in which, when optimizing one player, the opponent is simultaneously switched to greedy: J_{π1} uses r + γ min_{a'} q_{π2}(s',a') and J_{π2} uses r + γ max_{a'} q_{π1}(s',a'); the resulting gradients (Eq. 13) are score-function gradients weighted by this worst-case bootstrap target.
- Adversarial Monte Carlo Policy Gradient (introducing a parameter k to limit the number of next-actions considered): AMCPG-A runs k extra self-play games from (s,a) and takes the minimum of the k returns and the observed return z; AMCPG-B samples s', selects the top-k actions suggested by π, and self-plays from each, again taking the minimum. Using "mean" instead of "minimum" recovers a self-play REINFORCE variant; with k = |A(s')|, AMCPG-B is a genuine implementation of Eq. 12 (though min/max can still introduce a "winner's curse" bias).
- Notes the same idea can be implemented in an adversarial actor-critic framework (min operator on the critic), and that bias might be alleviated by soft-min operators as in soft-update Q-learning.
- Introduces a board-size-independent convolutional neural net architecture (no board-size-dependent fully connected layers, 12 binary feature planes) so a single model trained on 9×9 Hex can be reused on larger boards and combined with MCTS (MoHex 2.0) as a prior.

## Theoretical Contributions
- Mostly conceptual/derivational rather than new convergence proofs: it derives the adversarial policy gradient objective and gradients (Eq. 12–13) by analogy to the convergent AMG policy-iteration schemes (Algo.3/Algo.4, whose convergence is attributed to Hoffman & Karp, 1966; Condon, 1990; 1992), and explains why naive simultaneous or alternating gradient schemes correspond to the non-convergent Algo.1/Algo.2.
- Observes that the resulting Monte Carlo policy gradient estimates are biased (no longer unbiased) due to the min/max operator (winner's curse), motivating an adversarial actor-critic alternative.

## Experiments
- **Environment/Benchmark**: The game of Hex, board sizes 9×9 and 11×11 for pure policy gradient training, and 9×9 to 13×13 for the neural-net-plus-MCTS evaluation. Initial weights from supervised learning on MoHex self-play data (9×9). Implemented in TensorFlow.
- **Baselines**: REINFORCE-V (vanilla self-play REINFORCE), REINFORCE-A ("AlphaGo-like", opponent sampled from past parameters), REINFORCE-B (single sampled state-action pair using the mean of k+1 returns); search baselines MoHex 2.0, MoHex 2011, Wolve, and ExIt (Expert Iteration).
- **Evaluation metrics**: Winrate against 1-ply Wolve over training iterations (pure neural net); head-to-head overall winrates of MoHex-CNN9 vs MoHex 2.0 and vs MoHex 2011 (with MoHex2.0 as black/white), at fixed simulation counts and fixed time-per-move; per-game compute time.

## Key Results
- The proposed AMCPG-A and AMCPG-B learn better pure neural-net policies than the REINFORCE variants, tend to learn faster, and achieve better results even at k = 1, with the advantage clearer on the regular 11×11 board — confirming the benefit of estimating the minimum rather than the mean return for AMGs.
- REINFORCE-B matches REINFORCE-V despite using significantly fewer training samples (attributed to high correlation of the reward signal within a game); REINFORCE-A yields only small improvements, consistent with prior Go findings.
- With a single neural net trained only on 9×9 Hex used as the MCTS prior, MoHex-CNN9 defeats MoHex 2.0 on every board size from 9×9 to 13×13 (overall winrates roughly 57.7%–70.5% at 10^4 simulations), and beats MoHex 2.0 even under equal time-per-move; against MoHex 2011, MoHex-CNN9 is competitive with or stronger than ExIt.

## Limitations & Future Work
- The adversarial Monte Carlo policy gradient estimates are no longer unbiased, are sample-inefficient, and may have high variance; the authors suggest an adversarial actor-critic framework is more appealing.
- The min/max operator can introduce bias ("winner's curse"); soft-min operators are suggested as a remedy.
- Practical implementation of the exact objective (k = |A(s')|) is infeasible for large action spaces, motivating the subset-of-actions parameter k.

## Relevance to Survey
A workshop paper that sits at the intersection of two-player zero-sum game RL and robustness via worst-case (minimax) objectives. Its core mechanism — replacing the mean return with the worst-case (minimum) return as the learning target and switching the opponent to greedy — is a concrete instance of the adversarial / minimax method line that underlies robust adversarial RL (it explicitly draws the analogy to Pinto et al., 2017's robust adversarial reinforcement learning). For a Robust MARL survey it is a useful early example of injecting an adversarial/worst-case "critic" into policy gradient in a multi-agent (two-player) setting, and of connecting convergent game-theoretic policy iteration to adversarial policy optimization.

## Related Work (verbatim excerpts from the paper)
> _[Section 5, Related Work]_

"Games are studied by different disciplines, including game theory, reinforcement learning and computational complexity. Shapley (1953) introduced the notion of Stochastic Games, which is a multi-player framework that generalizes both Markov Decision Process (only one player) and repeated games (only one state). Condon (1990; 1992) initiated the study of Simple Stochastic Games, which are two-player games played on a directed graph with min, max and restricted probabilistic transition nodes. While her concern was largely from a computational complexity perspective, Condon (1990) showed that several variants of Hoffman-Karp's algorithms are incorrect. Littman (1996) formulated the notion of Alternating Markov Games, which is more general than Simple Stochastic Games by removing the restriction in action sets and probabilistic transitions. Littman (1994) proposed a minimax-Q learning algorithm that is applicable to Alternating Markov Games as well as two-player zero-sum games played with matrix payoffs."

> _[Section 5, Related Work — adversarial / robustness paragraph]_

"Adversarial methods have also been adopted in MDP (Pinto et al., 2017), since errors may occur in simulated models, maximizing a worst-case return will generally produce more robust results. The alternating procedure proposed by Pinto et al. (2017) resembles Algo.1. The idea of adversarial learning is also used in generative models (Goodfellow et al., 2014), which leverage adversarial examples to train a more robust classifier."

> _[Section 4, Adversarial Policy Gradient — motivation for the worst-case formulation]_

"The above formulation implies that, when computing the gradient for one policy, the other policy is simultaneously switched to "greedy". This joint-change forces the current player to adjust the action preferences according to the worst-case response of the opponent, which is desirable due to the adversarial nature of the game."

### Cited references (resolved from the paper's bibliography)
- **(Shapley, 1953)** L. S. Shapley. *Stochastic games.* Proceedings of the National Academy of Sciences, 39(10):1095–1100, 1953.
- **(Condon, 1990)** A. Condon. *On algorithms for Simple Stochastic Games.* Advances in Computational Complexity Theory, pp. 51–72, 1990.
- **(Condon, 1992)** A. Condon. *The complexity of stochastic games.* Information and Computation, 96(2):203–224, 1992.
- **(Littman, 1996)** M. L. Littman. *Algorithms for sequential decision making.* PhD thesis, Brown University, 1996.
- **(Littman, 1994)** M. L. Littman. *Markov games as a framework for multi-agent reinforcement learning.* Proceedings of the Eleventh International Conference on Machine Learning, vol. 157, pp. 157–163, 1994.
- **(Pinto et al., 2017)** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **(Goodfellow et al., 2014)** I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, Y. Bengio. *Generative adversarial nets.* NeurIPS (Advances in Neural Information Processing Systems), pp. 2672–2680, 2014.
