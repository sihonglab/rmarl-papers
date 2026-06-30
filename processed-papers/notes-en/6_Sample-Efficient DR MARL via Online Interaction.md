# 6. Sample-Efficient Distributionally Robust Multi-Agent Reinforcement Learning via Online Interaction

## Metadata
- **Title**: Sample-Efficient Distributionally Robust Multi-Agent Reinforcement Learning via Online Interaction
- **Authors**: Zain Ulabedeen Farhat, Debamita Ghosh (equal contribution), George K. Atia, Yue Wang
- **Affiliation**: Department of Electrical & Computer Engineering and Department of Computer Science, University of Central Florida, Orlando, FL, USA
- **Venue**: ICLR 2026
- **Link/arXiv**: arXiv:2508.02948v2 [cs.LG]

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty (sim-to-real gap, model mismatch from noise or adversarial attacks) modeled as distributional uncertainty over transition kernels; uncertainty sets measured by Total Variation (TV) distance and Kullback-Leibler (KL) divergence.
- **Method paradigm**: Distributionally Robust Markov Game (DRMG) theory; model-based online RL; optimism (UCB-style exploration bonus) combined with pessimism (worst-case robust optimization); robust value iteration; robust equilibrium learning (NE/CCE/CE).
- **Keywords**: Distributionally Robust Markov Games, online learning, regret bounds, sample complexity, TV/KL uncertainty sets, curse of multi-agency

## TL;DR
The paper pioneers online learning in Distributionally Robust Markov Games — where agents learn robust policies purely from environmental interaction without a simulator or offline dataset — by introducing the Multiplayer Optimistic Robust Nash Value Iteration (f-MORNAVI) meta-algorithm and providing the first provable regret and sample-complexity guarantees for TV- and KL-divergence uncertainty sets.

## Problem & Motivation
Well-trained multi-agent systems often fail when deployed due to model mismatch between training and deployment environments (the Sim-to-Real gap), a vulnerability amplified in the multi-agent setting through a cascading feedback loop of inter-agent interactions. DRMGs address this by optimizing worst-case performance over an uncertainty set of plausible models. However, existing DRMG methods assume either access to a generative model (a queryable oracle/simulator) or an offline setting (a large, pre-collected, comprehensive dataset) — assumptions that are untenable in high-stakes domains (e.g., autonomous systems, personalized healthcare) where simulators are impossible to build and exhaustive datasets are infeasible to collect. Agents must instead learn online, where data is earned through experience and naive exploration is costly. The central question is: how to design provably effective online algorithms for distributionally robust Markov games?

## Robustness Setting
- **Threat model / uncertainty set**: Each agent i maintains its own (possibly different) agent-wise (s,a)-rectangular uncertainty set Pᵢ of transition kernels, defined as an f-divergence ball of radius ρᵢ centered on a nominal kernel P⋆ (Definition 1). At each step the environment may transit following any kernel from the prescribed set; the agent optimizes worst-case (infimum) expected return over its own set. The work focuses on TV and KL divergence. A standard "fail-state" assumption (Assumption 3) is adopted only for the TV case to bypass the support-shift issue.
- **Setting**: general-sum (covers fully cooperative as a special case), competitive/mixed; multi-agent equilibrium learning (robust NE / CCE / CE); online (model-based interactive data collection from the nominal environment over K episodes), no simulator or offline dataset.

## Method
- **Model-based online framework (f-MORNAVI):** A meta-algorithm for episodic, finite-horizon DRMGs that synergizes pessimism (robust optimization) with optimism (UCB-style exploration), instantiated for TV and KL uncertainty sets.
- **Stage 1 — Nominal Transition Estimation:** Maintain an empirical estimate of the nominal kernel P̂ᵏ from historical interaction data (empirical counts), defaulting to uniform when a state-action pair is unvisited (eq. 4). A model-based approach is used because model-free DRMG estimators are biased/sample-inefficient due to the non-linearity of the worst-case expectation.
- **Stage 2 — Optimistic Robust Planning:** Construct upper (optimistic) and lower (pessimistic) robust Q-estimates via empirical robust Bellman operators plus/minus a data-driven bonus term βᵏ tailored to the geometry of the uncertainty set (eqs. 5–6), where the worst-case expectation is the support function computed through its f-divergence dual. The bonus makes the estimates a high-probability confidence interval around the true robust Q-values. An EQUILIBRIUM subroutine (NASH / CCE / CE) solves the per-state matrix game on the optimistic Q-values to produce the policy (eq. 7), and robust value functions are updated (eq. 8).
- **Stage 3 — Execution and Data Collection:** Execute the episode policy, observe rewards and next states, and append the transitions to the dataset.
- **Bonus design:** For TV, a Bernstein-type concentration via an ε-net of [0, H/ρ_min] yields a variance-aware bonus; for KL, a self-normalized concentration on empirical log-moment-generating functions yields a bonus scaling with H/ρᵢ and the smallest positive nominal-kernel entry.

## Theoretical Contributions
- **Hardness of online DRMGs (two lower bounds):** (1) With the support-shift issue (possible under TV), there exists a TV-DRMG on which any online algorithm incurs Ω(ρK·min{H, ∏ᵢAᵢ}) regret — linear in K, hence information-theoretically intractable (Theorem 1). (2) Even without support shift (e.g., KL), any algorithm suffers a minimax lower bound Ω(√(K∏ᵢAᵢ)), revealing an inevitable "curse of multi-agency" dependence on the joint action space (Theorem 2). These establish a separation between online DRMGs and generative-model/offline settings, and between robust and non-robust MGs.
- **Near-optimal regret upper bounds (first for online general-sum DRMGs):** TV-MORNAVI achieves Regret = Õ(√(min{ρ_min⁻¹, H}·H²SK·∏ᵢAᵢ)) under Assumption 3 (Theorem 4); KL-MORNAVI achieves Regret = Õ(√(H⁴exp(2H²)KS·∏ᵢAᵢ·ρ_min⁻²·(P⋆_min)⁻¹)) (Theorem 5), for EQUILIBRIUM ∈ {NASH, CE, CCE} with high probability.
- **Sample complexity (Corollary 6):** Via online-to-batch conversion, finding an ε-equilibrium requires KH = Õ(ε⁻²·min{ρ_min⁻¹, H}·H³S·∏ᵢAᵢ) for TV-DRMG and KH = Õ(ε⁻²H⁵exp(2H²)S·∏ᵢAᵢ·ρ_min⁻²·(P⋆_min)⁻¹) for KL-DRMG; near-optimal except for the ∏ᵢAᵢ term.
- Supporting results: strong-duality for f-divergence (Lemma 7), TV/KL dual representations (Corollary 8), and the robust Bellman equation under (s,a)-rectangularity (Proposition 9).

## Experiments
- **Environment/Benchmark**: Small-scale tabular DRMGs constructed for validation — a 2-agent, 2-step fully cooperative DRMG (states s0, sH, sM, sT; risky/safe/mediocre joint actions) and a general-sum variant with terminal 2×2 matrix games at each terminal state. Both KL- and TV-divergence uncertainty sets are tested.
- **Baselines**: Non-robust Multi-Nash Value Iteration (Liu et al., 2021); CCE is computed in practice due to PPAD-hardness of NE.
- **Evaluation metrics**: Averaged robust value function of Player 1 (and both players in the general-sum case) versus number of samples/episodes (with standard deviation over 10 runs), and robust value versus uncertainty radius ρ.

## Key Results
- f-MORNAVI (both KL and TV) converges to the robust equilibrium as the number of samples grows, validating the convergence/sample-efficiency guarantees.
- When ρ ≈ 0 (no model mismatch), the non-robust baseline outperforms the robust algorithm (which is conservative); as ρ increases and model mismatch is introduced, the non-robust equilibrium's performance degrades significantly while f-MORNAVI maintains stable, more robust performance.
- The same qualitative behavior holds in the general-sum DRMG for both players, confirming enhanced robustness across cooperative and general-sum settings.
- Theoretically, the method attains complexities comparable to generative-model and offline settings despite the harder online regime, matching or improving prior bounds in all parameters except the joint-action-product term ∏ᵢAᵢ.

## Limitations & Future Work
- The dependence on the joint action space ∏ᵢAᵢ (the curse of multi-agency) appears inevitable in online DRMGs, since agents must estimate the entire nominal kernel to compute the worst case; whether any algorithm can overcome it under general settings is left as an open question.
- The TV results require the fail-state assumption (Assumption 3) to avoid the support-shift hardness.
- The KL bound carries an exp(H²)/(P⋆_min)⁻¹ factor inherent to KL-based robust RL, controlled only for moderate horizons and non-vanishing minimum kernel entries.
- The method is model-based (higher memory consumption) and experiments are limited to small-scale tabular games due to the computational difficulty of equilibrium identification in Markov games.

## Relevance to Survey
This is a core theory paper on the "distributionally robust MARL" main line, extending single-agent online distributionally robust RL to the multi-agent / Markov-game setting. It is the first to study the online interactive-data-collection regime for DRMGs (as opposed to generative-model and offline settings of Shi et al. 2024, Jiao & Li 2024, Blanchet et al. 2023, Li et al. 2025), and connects the DRMG framework (Zhang et al. 2020; Kardeş et al. 2011) with optimistic exploration theory and the curse-of-multi-agency literature. It is a natural successor/companion to the foundational Robust MARL with Model Uncertainty work and a reference point for sample-efficient robust equilibrium learning.

## Related Work (verbatim excerpts from the paper)

> _[Appendix B, Related Works — "Single-Agent Robust RL"]_

"Single-Agent Robust RL. Robust RL for single-agent settings has been extensively studied across a wide range of formulations. In particular, a substantial body of work has examined the generative-model setting (Clavier et al., 2023; Liu et al., 2022; Panaganti & Kalathil, 2022; Ramesh et al., 2024; Shi et al., 2023; Wang et al., 2023b;c;d; 2024b;e; 2023a; Wang & Zou, 2022; Xu et al., 2023; Yang et al., 2022; 2023; Roch et al., 2025b;a; Xu et al., 2025), where the agent is assumed to have access to a simulator. These studies develop distributionally robust RL algorithms under various uncertainty sets, including TV, KL, χ2, and Wasserstein divergences. Another, and arguably more challenging, line of research focuses on the offline setting (Blanchet et al., 2023; Ma et al., 2022; Panaganti et al., 2022; Shi & Chi, 2024; Zhang et al., 2024a; Liu & Xu, 2024; Wang et al., 2024d; Blanchet et al., 2023; Wang et al., 2024a). In this setting, the agent must learn exclusively from a fixed offline dataset, without the ability to collect additional online samples. Finally, we consider the online setting (Badrinath & Kalathil, 2021; Dong et al., 2024; Li et al., 2022; Liang et al., 2024; Wang & Zou, 2021), where the agent learns exclusively through direct interaction with the environment. Prior work spans model-based, model-free, and policy-gradient approaches, with some methods, such as the policy optimization algorithm of (Dong et al., 2024), achieving sublinear regret guarantees."

> _[Appendix B, Related Works — "Robust MARL"]_

"Robust MARL. Besides the distributionally robust Markov games we considered in our paper, there are also other works that investigate robustness in MARL for cooperative tasks, where all agents share a unified objective. (Bukharin et al., 2023) enhance robustness through adversarial regularization, perturbing the environment to encourage Lipschitz-continuous policies. (Lin et al., 2020) explore adversarial attacks on MARL agents as a means of improving resilience, while (Li et al., 2019) extend this approach to continuous action spaces by modifying the MADDPG algorithm (Lowe et al., 2017) to focus on worst-case actions—a narrower interpretation of worst-case optimization in robust RL. (Wang et al., 2022) studied robust MARL with network agents.

Another line of research focuses on the robustness in MARL under observation uncertainty, under the formulation of partially observable MDPs. The framework of observation-robust games is proposed in (He et al., 2023; Han et al., 2024). Observation-robust cooperative MARL is studied in (Zhou et al., 2024)."

> _[Appendix B, Related Works — "Non-Robust Markov Games"]_

"Non-Robust Markov Games. Markov games (MGs), or stochastic games, introduced by (Shapley, 1953), form the standard foundation for MARL, particularly in equilibrium learning. Comprehensive surveys such as (Busoniu et al., 2008; Oroojlooy & Hajinezhad, 2023; Zhang et al., 2021a) offer thorough coverage of the field's evolution. Early work in MARL focused on asymptotic convergence guarantees (Littman et al., 2001; Littman & Szepesvári, 1996), whereas recent research emphasizes finite-sample analyses to establish non-asymptotic guarantees, especially for learning Nash equilibria (NE)—a central solution concept. The existence of NE in general-sum MGs was shown by (Fink, 1964), and the algorithmic foundation was laid by the seminal work of (Littman, 1994). Classical algorithms such as Nash-Q (Hu & Wellman, 2003), FF-Q (Littman et al., 2001), and correlated-Q learning (Greenwald & Hall, 2003) were proposed to compute NE and its variants. However, computing NE in general-sum multi-player settings remains PPAD-complete (Daskalakis, 2013), and no polynomial-time algorithms exist for this case (Jin et al., 2023; Deng et al., 2023). In contrast, the two-player zero-sum setting admits tractable solutions, with the first polynomial-time algorithm developed by (Hansen et al., 2013). To address the computational intractability in general-sum MGs, attention has shifted to weaker notions like CE and CCE, with polynomial-time algorithms such as V-learning (Jin et al., 2022; Mao & Başar, 2023; Song et al., 2022) and Nash value iteration (Liu et al., 2021) enabling efficient computation. Furthermore, significant progress in finite-sample analysis—spanning both model-based and model-free algorithms—has been achieved in the two-player zero-sum setting, as evidenced by (Bai & Jin, 2020; Xie et al., 2020; Cui et al., 2023; Chen et al., 2022; Liu et al., 2021; Feng et al., 2024; Li et al., 2024b), advancing the theoretical understanding of equilibrium learning in standard MARL without robustness considerations."

> _[Introduction — DRMG framework and the generative-model/offline gap]_

"To enable MARL against such uncertainty, the framework of Distributionally Robust Markov Games (DRMGs) offers a principled and powerful solution (Zhang et al., 2020; Kardeş et al., 2011). DRMG approach embraces a principle of pessimism. It defines an uncertainty set of plausible environment models centered around the nominal one, and the goal is to maximize the worst-case expected returns across the entire uncertainty set. ... The prevailing algorithmic frameworks fall into two main categories: those that assume access to a generative model (Shi et al., 2024; Jiao & Li, 2024), which is tantamount to having a perfect, queryable oracle or simulator, and those designed for the offline setting (Li et al., 2025; Blanchet et al., 2023), which presuppose the existence of a large, static, and sufficiently comprehensive dataset collected beforehand."

### Cited references (resolved from the paper's bibliography)
- **[Badrinath & Kalathil, 2021]** Panaganti Badrinath, Kalathil. *Robust Reinforcement Learning Using Least Squares Policy Iteration with Provable Performance Guarantees.* ICML 2021.
- **[Bai & Jin, 2020]** Bai, Jin. *Provable Self-Play Algorithms for Competitive Reinforcement Learning.* ICML 2020.
- **[Blanchet et al., 2023]** Blanchet, Lu, Zhang, Zhong. *Double Pessimism is Provably Efficient for Distributionally Robust Offline Reinforcement Learning: Generic Algorithm and Robust Partial Coverage.* NeurIPS 2023.
- **[Bukharin et al., 2023]** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust Multi-Agent Reinforcement Learning via Adversarial Regularization: Theoretical Foundation and Stable Algorithms.* NeurIPS 2023.
- **[Busoniu et al., 2008]** Busoniu, Babuska, De Schutter. *A Comprehensive Survey of Multiagent Reinforcement Learning.* IEEE Trans. SMC Part C, 2008.
- **[Chen et al., 2022]** Chen, Zhou, Gu. *Almost Optimal Algorithms for Two-player Zero-Sum Linear Mixture Markov Games.* ALT 2022.
- **[Clavier et al., 2023]** Clavier, Le Pennec, Geist. *Towards Minimax Optimality of Model-based Robust Reinforcement Learning.* arXiv:2302.05372, 2023.
- **[Cui et al., 2023]** Cui, Zhang, Du. *Breaking the Curse of Multiagents in a Large State Space: RL in Markov Games with Independent Linear Function Approximation.* COLT 2023.
- **[Daskalakis, 2013]** Daskalakis. *On the Complexity of Approximating a Nash Equilibrium.* ACM Transactions on Algorithms, 2013.
- **[Deng et al., 2023]** Deng, Li, Mguni, Wang, Yang. *On the Complexity of Computing Markov Perfect Equilibrium in General-Sum Stochastic Games.* National Science Review, 2023.
- **[Dong et al., 2024]** Dong, Li, Wang, Zhang. *Online Policy Optimization for Robust Markov Decision Process.* UAI 2024.
- **[Feng et al., 2024]** Feng, Yin, Wang, Yang, Liang. *Improving Sample Efficiency of Model-Free Algorithms for Zero-Sum Markov Games.* ICML 2024.
- **[Fink, 1964]** Fink. *Equilibrium in a Stochastic n-Person Game.* Journal of Science of the Hiroshima University, Series A-I, 1964.
- **[Greenwald & Hall, 2003]** Greenwald, Hall. *Correlated Q-Learning.* ICML 2003.
- **[Han et al., 2024]** Han, Su, He, Han, Yang, Zou, Miao. *What is the Solution for State-Adversarial Multi-Agent Reinforcement Learning?* TMLR 2024.
- **[Hansen et al., 2013]** Hansen, Miltersen, Zwick. *Strategy Iteration is Strongly Polynomial for 2-Player Turn-Based Stochastic Games with a Constant Discount Factor.* Journal of the ACM, 2013.
- **[He et al., 2023]** He, Han, Su, Han, Zou, Miao. *Robust Multi-Agent Reinforcement Learning with State Uncertainty.* TMLR 2023.
- **[Hu & Wellman, 2003]** Hu, Wellman. *Nash Q-learning for General-Sum Stochastic Games.* JMLR 2003.
- **[Jiao & Li, 2024]** Jiao, Li. *Minimax-Optimal Multi-Agent Robust Reinforcement Learning.* CoRR abs/2412.19873, 2024.
- **[Jin et al., 2022]** Jin, Liu, Wang, Yu. *V-Learning – A Simple, Efficient, Decentralized Algorithm for Multiagent RL.* ICLR 2022 Workshop.
- **[Jin et al., 2023]** Jin, Muthukumar, Sidford. *The Complexity of Infinite-Horizon General-Sum Stochastic Games.* ITCS 2023.
- **[Kardeş et al., 2011]** Kardeş, Ordóñez, Hall. *Discounted Robust Stochastic Games and an Application to Queueing Control.* Operations Research, 2011.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust Multi-Agent Reinforcement Learning via Minimax Deep Deterministic Policy Gradient.* AAAI 2019.
- **[Li et al., 2022]** Li, Zhao, Lan. *First-Order Policy Optimization for Robust Markov Decision Process.* CoRR abs/2209.10579, 2022.
- **[Li et al., 2024b]** Li, Jiao, Shan, Yan. *Provable Memory Efficient Self-Play Algorithm for Model-free Reinforcement Learning.* ICLR 2024.
- **[Li et al., 2025]** Li, Zheng, Ni, Shan, Zhang, Li. *Sample Efficient Robust Offline Self-Play for Model-based Reinforcement Learning.* OpenReview preprint, 2025.
- **[Liang et al., 2024]** Liang, Ma, Blanchet, Yang, Zhang, Zhou. *Single-Trajectory Distributionally Robust Reinforcement Learning.* ICML 2024.
- **[Lin et al., 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the Robustness of Cooperative Multi-Agent Reinforcement Learning.* CoRR abs/2003.03722, 2020.
- **[Littman, 1994]** Littman. *Markov Games as a Framework for Multi-Agent Reinforcement Learning.* ICML 1994.
- **[Littman & Szepesvári, 1996]** Littman, Szepesvári. *A Generalized Reinforcement-Learning Model: Convergence and Applications.* ICML 1996.
- **[Littman et al., 2001]** Littman et al. *Friend-or-Foe Q-Learning in General-Sum Games.* ICML 2001.
- **[Liu et al., 2021]** Liu, Yu, Bai, Jin. *A Sharp Analysis of Model-Based Reinforcement Learning with Self-Play.* ICML 2021.
- **[Liu et al., 2022]** Liu, Bai, Blanchet, Dong, Xu, Zhou, Zhou. *Distributionally Robust Q-Learning.* ICML 2022.
- **[Liu & Xu, 2024]** Liu, Xu. *Minimax Optimal and Computationally Efficient Algorithms for Distributionally Robust Offline Reinforcement Learning.* NeurIPS 2024.
- **[Lowe et al., 2017]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments.* NIPS 2017.
- **[Ma et al., 2022]** Ma, Liang, Blanchet, Liu, Xia, Zhang, Zhao, Zhou. *Distributionally Robust Offline Reinforcement Learning with Linear Function Approximation.* CoRR abs/2209.06620, 2022.
- **[Mao & Başar, 2023]** Mao, Başar. *Provably Efficient Reinforcement Learning in Decentralized General-Sum Markov Games.* Dynamic Games and Applications, 2023.
- **[Oroojlooy & Hajinezhad, 2023]** Oroojlooy, Hajinezhad. *A Review of Cooperative Multi-Agent Deep Reinforcement Learning.* Applied Intelligence, 2023.
- **[Panaganti & Kalathil, 2022]** Panaganti, Kalathil. *Sample Complexity of Robust Reinforcement Learning with a Generative Model.* AISTATS 2022.
- **[Panaganti et al., 2022]** Panaganti, Xu, Kalathil, Ghavamzadeh. *Robust Reinforcement Learning using Offline Data.* NeurIPS 2022.
- **[Ramesh et al., 2024]** Ramesh, Sessa, Hu, Krause, Bogunovic. *Distributionally Robust Model-based Reinforcement Learning with Large State Spaces.* AISTATS 2024.
- **[Roch et al., 2025a]** Roch, Atia, Wang. *A Reduction Framework for Distributionally Robust Reinforcement Learning under Average Reward.* ICML 2025.
- **[Roch et al., 2025b]** Roch, Zhang, Atia, Wang. *A Finite-Sample Analysis of Distributionally Robust Average-Reward Reinforcement Learning.* arXiv:2505.12462, 2025.
- **[Shapley, 1953]** Shapley. *Stochastic Games.* PNAS, 1953.
- **[Shi & Chi, 2024]** Shi, Chi. *Distributionally Robust Model-Based Offline Reinforcement Learning with Near-Optimal Sample Complexity.* JMLR 2024.
- **[Shi et al., 2023]** Shi, Li, Wei, Chen, Geist, Chi. *The Curious Price of Distributional Robustness in Reinforcement Learning with a Generative Model.* NeurIPS 2023.
- **[Shi et al., 2024]** Shi, Mazumdar, Chi, Wierman. *Sample-Efficient Robust Multi-Agent Reinforcement Learning in the Face of Environmental Uncertainty.* arXiv:2404.18909, 2024.
- **[Song et al., 2022]** Song, Mei, Bai. *When Can We Learn General-Sum Markov Games with a Large Number of Players Sample-Efficiently?* ICLR 2022.
- **[Wang & Zou, 2021]** Wang, Zou. *Online Robust Reinforcement Learning with Model Uncertainty.* NeurIPS 2021.
- **[Wang & Zou, 2022]** Wang, Zou. *Policy Gradient Method for Robust Reinforcement Learning.* ICML 2022.
- **[Wang et al., 2022]** Wang, Wang, Zhou, Velasquez, Zou. *Data-Driven Robust Multi-Agent Reinforcement Learning.* IEEE MLSP 2022.
- **[Wang et al., 2023a]** Wang, Ho, Petrik. *Policy Gradient in Robust MDPs with Global Convergence Guarantee.* ICML 2023.
- **[Wang et al., 2023b]** Wang, Si, Blanchet, Zhou. *A Finite Sample Complexity Bound for Distributionally Robust Q-learning.* AISTATS 2023.
- **[Wang et al., 2023c]** Wang, Si, Blanchet, Zhou. *On the Foundation of Distributionally Robust Reinforcement Learning.* CoRR abs/2311.09018, 2023.
- **[Wang et al., 2023d]** Wang, Velasquez, Atia, Prater-Bennette, Zou. *Model-Free Robust Average-Reward Reinforcement Learning.* ICML 2023.
- **[Wang et al., 2024a]** Wang, Shi, Chi. *Sample Complexity of Offline Distributionally Robust Linear Markov Decision Processes.* RLJ 2024.
- **[Wang et al., 2024b]** Wang, Si, Blanchet, Zhou. *Sample Complexity of Variance-Reduced Distributionally Robust Q-Learning.* JMLR 2024.
- **[Wang et al., 2024d]** Wang, Sun, Zou. *A Unified Principle of Pessimism for Offline Reinforcement Learning under Model Mismatch.* NeurIPS 2024.
- **[Wang et al., 2024e]** Wang, Velasquez, Atia, Prater-Bennette, Zou. *Robust Average-Reward Reinforcement Learning.* Journal of Artificial Intelligence Research, 2024.
- **[Xie et al., 2020]** Xie, Chen, Wang, Yang. *Learning Zero-Sum Simultaneous-Move Markov Games Using Function Approximation and Correlated Equilibrium.* COLT 2020.
- **[Xu et al., 2023]** Xu, Panaganti, Kalathil. *Improved Sample Complexity Bounds for Distributionally Robust Reinforcement Learning.* AISTATS 2023.
- **[Xu et al., 2025]** Xu, Ganesh, Aggarwal. *Efficient Q-learning and Actor-Critic Methods for Robust Average Reward Reinforcement Learning.* arXiv:2506.07040, 2025.
- **[Yang et al., 2022]** Yang, Zhang, Zhang. *Toward Theoretical Understandings of Robust Markov Decision Processes: Sample Complexity and Asymptotics.* The Annals of Statistics, 2022.
- **[Yang et al., 2023]** Yang, Wang, Kozuno, Jordan, Zhang. *Robust Markov Decision Processes without Model Estimation.* arXiv:2302.01248, 2023.
- **[Zhang et al., 2020]** Zhang, Sun, Tao, Genc, Mallya, Başar. *Robust Multi-Agent Reinforcement Learning with Model Uncertainty.* NeurIPS 2020.
- **[Zhang et al., 2021a]** Zhang, Yang, Başar. *Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms.* Handbook of Reinforcement Learning and Control, 2021.
- **[Zhang et al., 2024a]** Zhang, Hu, Li. *Soft Robust MDPs and Risk-Sensitive MDPs: Equivalence, Policy Gradient, and Sample Complexity.* ICLR 2024.
- **[Zhou et al., 2024]** Zhou, Liu, Zhou. *A Robust Mean-Field Actor-Critic Reinforcement Learning Against Adversarial Perturbations on Agent States.* IEEE TNNLS, 2024.
