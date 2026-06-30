# 39. Local Advantage Actor-Critic for Robust Multi-Agent Deep Reinforcement Learning

## Metadata
- **Title**: Local Advantage Actor-Critic for Robust Multi-Agent Deep Reinforcement Learning
- **Authors**: Yuchen Xiao, Xueguang Lyu, Christopher Amato
- **Affiliation**: Khoury College of Computer Sciences, Northeastern University, Boston, MA, USA
- **Venue**: 2021 International Symposium on Multi-Robot and Multi-Agent Systems (MRS), IEEE (DOI: 10.1109/MRS50823.2021.9620607)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Not adversarial/model-uncertainty robustness in the usual robust-MARL sense. Here "robustness" denotes consistently outstanding performance across diverse cooperative domains, i.e., resilience to environmental stochasticity, partial-observability/aliased observations, sparse vs. dense reward structures, and non-stationarity induced by other exploring agents (credit-assignment difficulty).
- **Method paradigm**: Multi-agent policy gradient / actor-critic; CTDE; per-agent local action-value critic trained via a centralized critic (centralized-double-critic sampling); advantage baseline for variance reduction; value-decomposition-free centralized critic.
- **Keywords**: MARL, actor-critic, CTDE, credit assignment, variance reduction, local critic, Dec-POMDP

## TL;DR
The paper proposes ROLA (Robust Local Advantage Actor-Critic), a cooperative-MARL policy-gradient method in which each agent learns an individual local action-value critic — trained by sampling joint next-actions from a fully centralized critic — and uses it to compute a low-variance local advantage baseline, implicitly achieving credit assignment and yielding consistently strong ("robust") performance across diverse benchmarks.

## Problem & Motivation
Multi-agent policy gradient methods suffer from high variance due to environmental stochasticity and non-stationarity from other exploring agents, a problem worsened by the difficulty of multi-agent credit assignment. Independent learning (IL) faces environmental non-stationarity; CTDE with a shared centralized critic still causes severe credit-assignment issues and extra variance because the critic conditions on the exponentially large joint observation-action space. COMA's counterfactual baseline only marginalizes over a single agent's actions while freezing others, so variance from other agents' exploration persists and credit assignment becomes noisy. SQDDPG requires a prior distribution over the coalition space; MAAC still relies on COMA's counterfactual scheme; LIIR depends on the underlying complexity of the ground-truth credit assignment. Value-function-factorization methods impose structural constraints (linear/monotonic mixing) that prevent learning the true joint action-value function and limit generality across domains. ROLA targets all of these issues simultaneously while seeking method "robustness" (strong performance across many domains).

## Robustness Setting
- **Threat model / uncertainty set**: No adversary or explicit uncertainty set. The sources of difficulty addressed are environmental natural stochasticity, partial observability with aliased/noisy observations, sparse vs. dense reward signals, and non-stationarity / high gradient variance caused by other agents' explorations. "Robustness" is defined operationally as the method always gaining outstanding performance over multiple domains.
- **Setting**: Fully cooperative (Dec-POMDP); CTDE (centralized training, decentralized execution); on-policy version described, with an off-policy variant possible via replay buffer and importance sampling.

## Method
- Step 1 — Learn a fully centralized critic Q^{π}_φ(x, a⃗) over joint actions, minimizing a squared TD-error loss with delayed target-policy parameters; x denotes accessible global signals (joint observations, joint action-observation histories, or the true state).
- Step 2 — Define a semi-centralized per-agent local critic Q^loc_{ψ_i}(x, a_i) that conditions only on agent i's own action but may access additional centralized information (satisfies a Dec-MDP/Dec-POMDP Bellman equation depending on x).
- Centralized-double-critic training: to update each local critic, sample a joint next-action a⃗′ from the centralized critic via a softmax operation, extract that agent's next action a′_i, and use it in the local TD target. This injects other agents' concurrent behaviors into each local critic, enabling implicit credit assignment and supplying extra centralized action-selection data (beyond decentralized trajectories).
- Policy update: fuse the local critic into each agent's policy gradient through a local advantage A_i(x, a_i) = Q^loc_{ψ_i}(x, a_i) − Σ_{ȧ_i} π_{θ_i}(ȧ_i|τ_i) Q^loc_{ψ_i}(x, ȧ_i), giving a per-agent baseline that reduces variance from both its own and other agents' explorations.
- Motivated by an "expected counterfactual advantage" (ECA) derivation from COMA's gradient: ROLA approximates this expected advantage cheaply via local critics rather than the exponential explicit marginalization that ECA requires.

## Theoretical Contributions
None / mostly empirical. The paper derives the expected counterfactual advantage (ECA) policy gradient from COMA's gradient as motivation and argues the local advantage is low-variance and unbiased, but provides no formal convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: Four cooperative benchmarks differing in reward density, environmental stochasticity, collaborative format, and number of agents — Capture Target, a variant of Box Pushing, OpenAI Cooperative Navigation (made partially observable via a view range), and Antipodal Navigation (partially observable, individual rewards). Each tested under two configurations (varying grid size or observation radius).
- **Baselines**: IA2C, Central-V, COMA, LIIR, SQDDPG, MAAC (Comparison 1); DOP, VDAC-mix, VDAC-sum (Comparison 2, VDN/value-decomposition-based); ECA (Comparison 3).
- **Evaluation metrics**: Mean test return (averaged discounted return) over 20 independent training trials, evaluated every 100 episodes over 10 episodes; curves smoothed (window 10) with 95% confidence intervals; convergence speed and variance also assessed.

## Key Results
- ROLA consistently outperforms IA2C, Central-V, COMA, LIIR, SQDDPG, and MAAC across all four domains, achieving the highest returns, fastest convergence, and lower evaluation variance, demonstrating its credit assignment, variance reduction, and cross-domain "robustness."
- In Box Pushing, ROLA always converges to the optimal value fastest and keeps performance fluctuation low as the grid grows; in dense-reward Cooperative Navigation its advantages become more pronounced as the view field shrinks.
- ROLA beats the VDN-based methods (DOP, VDAC-mix, VDAC-sum), whose decomposition/monotonicity constraints limit the centralized critic; ROLA's unconstrained centralized critic plus sampled-target-action training for local critics yields better policies.
- ROLA substantially exceeds ECA in both final return and sample efficiency, because explicit ECA computation suffers a single-approximator bias when the centralized Q is under-trained and incurs exponentially increasing computational cost.

## Limitations & Future Work
- Only an on-policy version is described; the off-policy extension (replay buffer + importance sampling) is mentioned but not evaluated.
- The reported global information used by the local critic is the environment state in experiments (chosen "without loss of generality"); the best choice of global signal is domain-dependent and not systematically studied.
- No theoretical guarantees; "robustness" is established empirically and is defined as strong multi-domain performance rather than robustness to adversaries or model uncertainty.
- Experiments are limited to small/medium cooperative grid-world and particle domains. (No explicit future-work section is given beyond the off-policy remark.)

## Relevance to Survey
This paper sits at the periphery of the robust MARL landscape: its use of "robust" denotes empirical resilience/consistency across cooperative domains (handling stochasticity, partial observability, sparse/dense rewards, and inter-agent non-stationarity) rather than adversarial perturbations, model/environment uncertainty, or distributional robustness. It connects to the cooperative CTDE actor-critic and credit-assignment line (COMA, MAAC, LIIR, value-decomposition methods) and is useful as a contrast point illustrating how the "robust MARL" terminology is sometimes used for cross-task generalization/variance reduction rather than worst-case/adversarial robustness.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"MARL methods often build off of single-agent RL methods. In terms of taking advantage of single-agent reinforcement learning techniques, the independent learning (IL) framework is the simplest solution, allowing each agent to learn an individual policy in such environments [9]. Although IL may sometimes work in practice, it encounters a crucial theoretical issue: the environment becomes non-stationary from each agent's perspective as other agents explore and update policies. This so-called environmental non-stationarity is known to generate a high variance on value and gradient estimations and impedes agents from collaborating well."

> _[Introduction]_

"Centralized training with decentralized execution (CTDE) [10], [11] has been a very promising learning framework for improving solution quality while maintaining decentralized execution in MARL. CTDE has been implemented with both value-based [12]–[15] and policy-gradient-based approaches [16]–[21]. In particular, policy gradient algorithms based on an actor-critic framework have become prominent for implementing the CTDE paradigm. The key idea is to train a centralized critic conditioned on accessible global information for directing each decentralized actor's optimization. This centralized critic is favored for its stationary learning targets, overcoming the major theoretical problem in IL, and has become the basis of many recent advances. However, with a global reward function in multi-agent cooperative problems, simply applying a shared centralized critic to compute the gradient for each agent's action still causes a severe credit assignment issue. It introduces extra variance on gradient estimation for each agent's policy since the critic conditions on joint observations and actions, where the joint space is of exponential size."

> _[Introduction]_

"COMA [16], as a representative multi-agent actor-critic-based method, achieves variance reduction by using a counterfactual baseline, inspired from difference rewards [22], to credit each agent. The counterfactual baseline is a promising idea, but it estimates the contribution of each agent's action by marginalizing over only the corresponding agent's counterfactual action choices while keeping other agents' actions fixed. As a result, the estimation variance caused by other agents' explorations still exists, which leads to noisy credit assignments. SQDDPG [19] extends COMA's idea to capture the average contribution of an agent's action by sequentially adding the agent into a set of sampled coalitions. Although it theoretically improves the effectiveness of resolving the two problems mentioned above, it has a strong requirement on a prior distribution over the coalition space, which is often not available without having good knowledge of a given domain's properties. MAAC [20] utilizes a centralized attention mechanism to solve tasks that require agents to selectively focus on different things in order to produce rich collaborations. However, it still suffers from inefficient credit assignment and variance reduction due to the pure dependency on COMA's counterfactual scheme. LIIR [21] explicitly approximates each agent's individual reward based on global reward signals, and its performance highly depends on the underlying complexity of the ground truth credit assignment shaped by the domain reward function."

> _[Introduction]_

"Value function factorization has also become popular in MARL for learning individual Q-functions [12]–[15]. Such methods have recently been introduced into actor-critic frameworks [23], [24] to learn critics. However, these factorization methods have an inherent limitation caused by restricting the relationship between the joint Q-values and decentralized Q-values, such as assuming a linear summation constraint, a non-linear monotonic constraint, or other weighted constraints. These constraints prevent the methods from learning the true joint action-value function in general and potentially limit each method to work well in particular tasks (such as the SMAC domains [6] in most related papers) but perform worse in some other domains [25]."

### Cited references (resolved from the paper's bibliography)
- **[6]** M. Samvelyan, T. Rashid, C. S. de Witt, G. Farquhar, N. Nardelli, T. G. J. Rudner, C.-M. Hung, P. H. S. Torr, J. Foerster, S. Whiteson. *The StarCraft Multi-Agent Challenge.* arXiv:1902.04043, 2019.
- **[9]** M. Tan. *Multi-agent reinforcement learning: Independent vs. cooperative agents.* ICML 1993.
- **[10]** F. A. Oliehoek, M. T. J. Spaan, N. A. Vlassis. *Optimal and approximate Q-value functions for decentralized POMDPs.* Journal of Artificial Intelligence Research, 2008.
- **[11]** L. Kraemer, B. Banerjee. *Multi-agent reinforcement learning as a rehearsal for decentralized planning.* Neurocomputing, 2016.
- **[12]** T. Rashid, M. Samvelyan, C. S. de Witt, G. Farquhar, J. Foerster, S. Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[13]** T. Rashid, G. Farquhar, B. Peng, S. Whiteson. *Weighted QMIX: Expanding monotonic value function factorisation.* NeurIPS 2020.
- **[14]** A. Mahajan, T. Rashid, M. Samvelyan, S. Whiteson. *MAVEN: Multi-agent variational exploration.* NeurIPS 2019.
- **[15]** T. Wang, H. Dong, Victor Lesser, C. Zhang. *ROMA: Multi-agent reinforcement learning with emergent roles.* ICML 2020.
- **[16]** J. Foerster, G. Farquhar, T. Afouras, N. Nardelli, S. Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[17]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[18]** S. Li, Y. Wu, X. Cui, H. Dong, F. Fang, S. Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[19]** J. Wang, Y. Zhang, T.-K. Kim, Y. Gu. *Shapley Q-value: A local reward approach to solve global reward games (SQDDPG).* 2020.
- **[20]** S. Iqbal, F. Sha. *Actor-attention-critic for multi-agent reinforcement learning (MAAC).* ICML 2019.
- **[21]** Y. Du, L. Han, M. Fang, T. Dai, J. Liu, D. Tao. *LIIR: Learning individual intrinsic reward in multi-agent reinforcement learning.* NeurIPS 2019.
- **[22]** D. H. Wolpert, K. Tumer. *Optimal payoff functions for members of collectives.* Advances in Complex Systems, 2001.
- **[23]** J. Su, S. Adams, P. A. Beling. *Value-decomposition multi-agent actor-critics (VDAC).* AAAI 2021.
- **[24]** Y. Wang, B. Han, T. Wang, H. Dong, C. Zhang. *DOP: Off-policy multi-agent decomposed policy gradients.* ICLR 2021.
- **[25]** J. Yang, A. Nakhaei, D. Isele, K. Fujimura, H. Zha. *CM3: Cooperative multi-goal multi-stage multi-agent reinforcement learning.* ICLR 2020.
