# 74. Bayesian Robust Cooperative Multi-Agent Reinforcement Learning Against Unknown Adversaries

## Metadata
- **Title**: Bayesian Robust Cooperative Multi-Agent Reinforcement Learning Against Unknown Adversaries
- **Authors**: Kiarash Kazari, György Dán
- **Affiliation**: KTH Royal Institute of Technology, Stockholm, Sweden
- **Venue**: ICLR 2026
- **Link/arXiv**: Code available at https://github.com/kiarashkaz/BATPAL

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents at deployment / execution time in cooperative MARL (a victim agent compromised via action manipulation or observation corruption), with an adversary whose objective is *unknown* and not necessarily worst-case; uncertainty about the adversarial objective.
- **Method paradigm**: Bayesian game (Bayesian Dec-POMDP) with a continuum of adversarial types; perfect Bayesian equilibrium (PBE); type-space partitioning by attack severity; externally constrained RL (log-barrier + PPO, EC-PPO); adversarial training with min-oracle via simultaneous (two-timescale) gradient descent-ascent; belief modeling.
- **Keywords**: cooperative MARL, adversarial robustness, Bayesian Dec-POMDP, perfect Bayesian equilibrium, externally constrained RL, non-worst-case adversary

## TL;DR
The paper proposes BATPAL, a Bayesian Dec-POMDP framework that models unknown adversarial objectives as a continuum of types, partitions adversarial policies by their severity (impact on team reward) into a finite set of types, and trains a single belief-conditioned c-MARL policy that is robust to a representative worst-case adversary in each partition, yielding adaptive, near-no-regret robustness against diverse and unseen attacks.

## Problem & Motivation
At deployment time, cooperative MARL (c-MARL) agents can be compromised by an adversary whose identity and objective are unknown, and the failure or compromise of even a single agent degrades team performance. Existing robust approaches (dataset augmentation, adversarial / saddle-point training) typically produce a single max-min policy against a worst-case adversary. The authors argue this has three fundamental limitations: (1) the worst-case assumption fails to capture adversaries with other objectives or non-cooperative failures that deviate substantially from worst case, making the max-min policy far from optimal; (2) the underlying optimization is non-convex and learning tends to converge to local stationary points (local Stackelberg equilibria), potentially far from the sought equilibrium; (3) training on perturbed versions of a single adversarial policy causes overfitting of the agents' representation of adversarial dynamics, so they fail to adapt to a different attack type at deployment. The paper addresses robustness to *unknown, non-worst-case* adversaries.

## Robustness Setting
- **Threat model / uncertainty set**: An adversary takes control of a single victim agent v (with extension to multiple victims in the Appendix). The adversarial objective is captured by a type θ_i ∈ Θ_i = [0, 1]; θ_i = 0 maximizes team reward (cooperative), θ_i = 1 minimizes team reward (worst-case adversary), and intermediate types maximize some other reward. Uncertainty about the type is captured by a Bayesian prior b0 and beliefs maintained from observation history. The continuous type space is discretized by partitioning adversarial policies into K severity levels based on the team value they impose against a reference policy π0; severity η_{ρv} = (Vmax − V^{π0,ρv}) / (Vmax − V^v_min) ∈ [0, 1].
- **Setting**: cooperative (c-MARL, Dec-POMDP) with an adversarial agent; CTDE-style with belief-conditioned decentralized execution; deployment/execution-time robustness (adversary acts at deployment, types fixed within an episode).

## Method
- **Bayesian Dec-POMDP model (M_B)**: Extends the Dec-POMDP with type spaces Θ_i; the solution concept is a perfect Bayesian equilibrium (PBE), and policy quality is measured by the Bayesian regret R(π) = E_{(v,θv)∼b0}[max_{π'} V^{π',ρv,θv} − V^{π,ρv,θv}], which a PBE minimizes.
- **Reference-value based partitioning**: Because each adversary's reward is private, types are distinguished by their severity against a reference cooperative policy π0. A policy ρv belongs to type z = (v, k) if its severity falls in ((k−1)/K, k/K]. The discretized game M̂_B has finite type space {0, 1, …, K}; its PBE is a policy that maximizes, for each agent, the belief-weighted worst-case value within each partition (Eq. 4). Propositions 3.2–3.4 bound the KL diversity of resulting adversarial policies and give a severity-dependent regret bound k(Vmax − V^v_min)/K.
- **Externally constrained RL (EC-PPO)**: To find the worst-case adversary in each partition, the inner minimization is cast as a constrained problem where objective and constraints correspond to two different MDPs (MDP1 induced by fixing π, MDP0 by fixing π0). A log-barrier reformulation (Eq. 9) is solved by a biased policy-gradient update; Proposition 4.2 proves convergence to an ε-stationary / KKT point with adaptive step sizes. A practical variant (EC-PPO, Eq. 14) incorporates PPO clipping to handle feasibility and gradient-variance issues.
- **Bayesian adversarial MARL training (BATPAL)**: M̂_B is shown equivalent to a partially observable stochastic game with N+1 players (adversary as player N+1). The benign agents solve arg max_ω min_ψ V̄^{ω,ψ} via two-timescale simultaneous stochastic gradient descent-ascent (Eqs. 16–17), using the EC-PPO adversary as an approximate min-oracle. An RNN belief network b_{χi}(θ−i | τ_i) is trained with cross-entropy against true types and fed into the policy. Parameter sharing is used, with one c-MARL policy network and K adversarial networks (randomized one-per-update).

## Theoretical Contributions
- **Proposition 3.1**: With observable states, each partition Πz is nonempty (partitioning is feasible).
- **Proposition 3.2**: Lower bound on the expected KL divergence between two adversarial policies in terms of the difference of their reference initial-state values.
- **Proposition 3.3**: Lower bound on the diversity of the K adversarial policies produced by the partitioning.
- **Proposition 3.4**: Severity-dependent regret bound R_{ρ̂v}(π*_z) ≤ k(Vmax − V^v_min)/K, showing the partitioning mitigates sub-optimality of a single max-min policy.
- **Proposition 4.1**: Closed-form policy gradient of the externally constrained log-barrier objective.
- **Proposition 4.2**: Convergence guarantee for the (biased-gradient) externally constrained RL algorithm — after Niter iterations, min_n ||g_{ψn}|| ≤ ε with probability ≥ 1−δ, and as λ → 0 the point approaches a KKT point of the constrained problem.

## Experiments
- **Environment/Benchmark**: Level-Based Foraging (LBF, scenario 10x10-5p-10f-c); Multi-Particle Environments (MPE) Spread; StarCraft II Multi-Agent Challenge (SMAC) scenarios 2s3z and MMM (and 1c3s5z, 11m in the Appendix). Five, three, five, and ten agents respectively.
- **Baselines**: EIR-MAPPO (Li et al., 2024), Generalized Maxmin / Gen-Maxmin (Liu et al., 2024a), RAP (Vinitsky et al., 2020), vanilla MAPPO (Yu et al., 2022); Known Type (KT) as an empirical upper bound; ROMANCE (Yuan et al., 2023) in the Appendix. MAPPO is the backbone (built on HARL and EIR-MAPPO implementations).
- **Evaluation metrics**: SMAC: team win rate; LBF / MPE-Spread: mean episodic total reward (normalized). Evaluated against 10 adversarial policies (BATPAL severity-indexed attacks, attacks A-X trained against each baseline, and three unseen dynamic adversaries ACT, DYN-1, DYN-2 balancing impact and detectability), applied to a victim for 50 episodes.

## Key Results
- BATPAL performs at least as well as vanilla MAPPO under no attack (robustification does not compromise nominal optimality), and almost always outperforms each robust baseline even against the attack that baseline was trained against.
- Baselines often suffer their worst performance against BATPAL's training attacks (rather than their own), which the authors attribute to adversarial training getting stuck in local stationary points — supporting the disjoint-set adversarial search.
- BATPAL achieves near no-regret relative to the empirical KT upper bound in many cases, including against unseen attacks; ablations show the belief network, EC-PPO clipping, and severity-based partitioning are each important (No Belief, Perfect Belief, EC PG, and Fixed Types variants all degrade robustness).
- Increasing K generally improves robustness; even K = 4 gives satisfactory performance, and training-step growth with K is typically sublinear.

## Limitations & Future Work
- The issue of getting stuck in local optima is mitigated but not eliminated; partitioning only restricts the search to smaller, non-overlapping feasible sets.
- The convergence guarantee relies on assumptions (unbiased estimators, smoothness/Lipschitz conditions, a strictly feasible starting point, and a nonzero-gradient MFCQ-type condition near constraint boundaries); the practical EC-PPO variant departs from the provably convergent update.
- The multiple-victim extension suffers a combinatorial explosion of victim-agent combinations that must be explored during training; for very severe attacks on many agents (e.g., ACT on 3 victims) no method produces a good policy.
- Each additional severity type requires an extra network, increasing training time; the empirical KT upper bound may not be the true optimum.

## Relevance to Survey
This paper sits on the "adversarial agents / execution-time robustness in cooperative MARL" line and connects the adversarial-training and robust-learning (max-min / saddle-point) threads to a Bayesian-game formulation. It directly extends and contrasts with worst-case c-MARL robustness works (M3DDPG, RAT/RADAR, ROMANCE/WALL, EIR-MAPPO) and the non-worst-case adversary line (Gen-Maxmin, Liu et al.). Its key contribution to the survey's "non-worst-case / unknown adversary" sub-theme is type-based diversity via severity partitioning plus belief-conditioned adaptation, and a novel externally constrained RL primitive with convergence analysis.

## Related Work (verbatim excerpts from the paper)
> _[Appendix A, Related Work]_

"Adversarial robustness in reinforcement learning has been studied mainly through two main approaches: adversarial training and robust learning. In adversarial training, a known form of adversarial perturbation is introduced during the training phase, allowing the agent to learn both adversarial and nominal transitions simultaneously. For example, Gleave et al. (2019); Pattanaik et al. (2017) employ this approach to defend against various types of manipulations. A closely related method is (Havens et al., 2018) which applies adversarial training within a meta-learning framework to enable adaptation to attacks. These methods primarily target training-time attacks and rely on prior knowledge of the adversary."

"Robust learning instead models the agent–adversary interaction as a game, often zero-sum, where the agent seeks a max–min policy for execution-time robustness. Such works are often categorized under robustness to uncertainty, but the uncertainty is explicitly modeled as being induced by an adversary. For instance, RARL (Pinto et al., 2017) and RARAL (Pan et al., 2019) consider adversaries capable of applying model disturbances and propose alternating optimization methods to find a robust policy. On the other hand, Tessler et al. (2019) and RAP (Vinitsky et al., 2020) study adversarial manipulation of actions. Although effective against worst-case attacks, such approaches can be overly conservative; recent work (Liu et al., 2024b) addresses this by considering arbitrary non-worst-case adversaries in a lifelong learning context."

"In MARL, robustness has been explored both at training and at execution. Training-time defenses include adversarial regularization for smooth policies (Bukharin et al., 2023) and consensus-based learning robust to Byzantine agents (Ye et al., 2024). Execution-time resilience has been studied through robust learning. M3DDPG (Li et al., 2019) adopts a max–min value function with the idea that each agent assumes all other agents to be adversarial. RAT (Phan et al., 2020) and RADAR Phan et al. (2021) consider environments with a subset of worst-case adversarial agents. ROMANCE (Yuan et al., 2023) and WALL (Lee et al., 2025) consider adversaries capable of targeting all agents but with a limited budget of attack numbers. Recently, Li et al. (2024) propose adversarial belief states that allow agents to adapt online when teammates are compromised. While this approach addresses the challenge of reacting to attacks on different agents, it remains focused on worst-case robustness and does not capture the diversity of adversarial strategies. Finally, Liu et al. (2024a) studies adaptation to non-worst-case adversaries in two-agent scenarios. However, the authors consider a fixed adversarial, which limits the generalization of the robustness to unseen attacks."

> _[Introduction — "Related Work" paragraph]_

"In robust learning the agent–adversary interaction is modeled as a game, and the agents seek a max–min policy for execution-time robustness. RARL (Pinto et al., 2017) and RARAL (Pan et al., 2019) focus on adversarial disturbances with alternating optimization, while Tessler et al. (2019) and RAP (Vinitsky et al., 2020) study adversarial manipulation of actions. Although effective against worst-case attacks, such approaches can be overly conservative; recent work (Liu et al., 2024b) addresses this by considering non-worst-case adversaries, but in a lifelong learning context. For execution-time robustness in MARL, M3DDPG (Li et al., 2019) adopts a max–min value function, while RAT (Phan et al., 2020) and RADAR (Phan et al., 2021) consider environments with a subset of adversarial agents. Yuan et al. (2023) and Lee et al. (2025) model budget-limited attacks, and Liu et al. (2024a) studies adjustable, non-worst-case adversaries in two-agent scenarios. Most recently, Li et al. (2024) propose to maintain belief states about what teammates are compromised, but considers a worst case adversary only, leaving agents undefended against unseen adversaries."

> _[Introduction — motivation paragraph on existing robust approaches]_

"Existing approaches for obtaining robust policies rely on dataset augmentation or on adversarial training (Gleave et al., 2019; Pattanaik et al., 2017; Havens et al., 2018; Pinto et al., 2017; Phan et al., 2021; Liu et al., 2024a; Li et al., 2024). Dataset augmentation involves introducing one or more adversarial perturbations during training, allowing agents to learn under adversarial and nominal conditions simultaneously (Gleave et al., 2019; Pattanaik et al., 2017; Havens et al., 2018). The alternative approach is based on jointly training the benign and the adversarial agents, typically formulated as a zero-sum Stackelberg game, and a saddle-point equilibrium in policies is sought after (Pinto et al., 2017; Phan et al., 2021; Liu et al., 2024a). These approaches typically yield a single policy optimized for adversarial conditions and thus they are typically suboptimal when all agents are cooperative. Even if the trained policy can maintain a belief about the presence of an adversary, as in Li et al. (2024), robust learning based on saddle-point equilibria against a worst case adversary found using gradient descent has three fundamental limitations."

### Cited references (resolved from the paper's bibliography)
- **[Gleave et al., 2019]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[Pattanaik et al., 2017]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* arXiv:1712.03632, 2017.
- **[Havens et al., 2018]** Havens, Jiang, Sarkar. *Online robust policy learning in the presence of unknown adversaries.* NeurIPS 2018.
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning (RARL).* ICML 2017.
- **[Pan et al., 2019]** Pan, Seita, Gao, Canny. *Risk averse robust adversarial reinforcement learning (RARAL).* ICRA 2019.
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Vinitsky et al., 2020]** Vinitsky, Du, Parvate, Jang, Abbeel, Bayen. *Robust reinforcement learning using adversarial populations (RAP).* arXiv:2008.01825, 2020.
- **[Liu et al., 2024a]** Liu, Chakraborty, Sun, Huang. *Rethinking adversarial policies: A generalized attack formulation and provable defense in RL.* ICLR 2024.
- **[Liu et al., 2024b]** Liu, Deng, Sun, Liang, Huang. *Beyond worst-case attacks: Robust RL with adaptive defense via non-dominated policies.* ICLR 2024.
- **[Bukharin et al., 2023]** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* NeurIPS 2023.
- **[Ye et al., 2024]** Ye, Figura, Lin, Pal, Das, Liu, Gupta. *Resilient multi-agent reinforcement learning with function approximation.* IEEE Transactions on Automatic Control, 2024.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[Phan et al., 2020]** Phan, Gabor, Sedlmeier, Ritz, Kempter, Klein, Sauer, Schmid, Wieghardt, Zeller, et al. *Learning and testing resilience in cooperative multi-agent systems (RAT).* AAMAS 2020.
- **[Phan et al., 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition (RADAR).* AAAI 2021.
- **[Yuan et al., 2023]** Yuan, Zhang, Xue, Yin, Chen, Guan, Li, Qian, Yu. *Robust multi-agent coordination via evolutionary generation of auxiliary adversarial attackers (ROMANCE).* AAAI 2023.
- **[Lee et al., 2025]** Lee, Hwang, Jo, Han. *Wolfpack adversarial attack for robust multi-agent reinforcement learning (WALL).* ICML 2025.
- **[Li et al., 2024]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game (EIR-MAPPO).* ICLR 2024.
