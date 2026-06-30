# 10. Robust Cooperative Multi-Agent Reinforcement Learning: A Mean-Field Type Game Perspective

## Metadata
- **Title**: Robust Cooperative Multi-Agent Reinforcement Learning: A Mean-Field Type Game Perspective
- **Authors**: Muhammad Aneeq uz Zaman, Mathieu Laurière, Alec Koppel, Tamer Başar
- **Affiliation**: Coordinated Science Laboratory, University of Illinois at Urbana-Champaign; Shanghai Frontiers Science Center of Artificial Intelligence and Deep Learning & NYU-ECNU Institute of Mathematical Sciences at NYU Shanghai; AI Research, JP Morgan Chase & Co.
- **Venue**: Proceedings of Machine Learning Research vol 242 (6th Annual Conference on Learning for Dynamics and Control, L4DC) 2024
- **Link/arXiv**: arXiv:2406.13992 (full version, Zaman et al., 2024)

## Taxonomy
- **Robustness / perturbation type targeted**: Model mis-specification / un-modeled (non-stochastic, possibly adversarial) disturbances on the transition dynamics, alongside stochastic noise with known distribution; worst-case (H-infinity-style) noise attenuation in a large-population multi-agent system.
- **Method paradigm**: Robust control as a zero-sum min-max dynamic game; Mean-Field Type Game (MFTG) / Robust Mean-Field Control (RMFC); Linear-Quadratic (LQ) benchmark; receding-horizon policy gradient descent-ascent; zero-order (model-free) policy optimization; Nash/saddle-point equilibrium.
- **Keywords**: Robust MARL, Mean-Field Type Game, Robust Mean-Field Control, Linear-Quadratic, zero-sum min-max game, receding-horizon gradient descent-ascent

## TL;DR
The paper formulates robust cooperative MARL with a large population of distributed-information agents subject to both stochastic and non-stochastic (adversarial) uncertainties as a Robust Mean-Field Control problem, shows it is equivalent to a 2-player Zero-Sum Mean-Field Type Game in the LQ setting, and proposes a model-free Receding-horizon Gradient Descent Ascent (RGDA) RL algorithm with a non-asymptotic convergence guarantee to the MFTG Nash equilibrium.

## Problem & Motivation
Prevailing MARL algorithms do not model the distinct effects of modeled and un-modeled uncertainties on transition dynamics, which can cause practical instability in safety-critical applications. Robust control addresses such uncertainties in the single-agent case by seeking a controller that guarantees a level of performance under worst-case disturbances, but extending this to many agents is hard: communicating local state/control information among agents scales exponentially with the number of agents. The paper instead assumes a distributed information structure where each agent observes only its own state and the average of the other agents' states; this structure breaks the gradient-dominance results used for single-agent LQ analysis. There is no standard theory for the robust multi-agent control problem under such distributed information, and no provable robust MARL algorithm in the large-population setting — gaps this work targets via the mean-field paradigm.

## Robustness Setting
- **Threat model / uncertainty set**: Each agent's linear dynamics are perturbed by two noise types: stochastic noises (i.i.d., Gaussian, known distribution: idiosyncratic ωᵢₜ ∼ N(0,Σ) and common ω̄ₜ ∼ N(0,Σ̄)) and non-stochastic noise u²ᵢₜ that is an un-modeled, possibly adversarial disturbance. Robustness is measured by a noise attenuation level γ (an upper bound on the ratio of a performance index to a noise index, i.e., the noise-to-output gain). The robust problem is reformulated as the zero-sum min-max game infᵤ₁ supᵤ₂ (Jₙ(u¹,u²) − γ²ϖₙ(u¹,u²)) ≤ 0, where the minimizing player is the controller and the maximizing player is the worst-case non-stochastic noise (adversary).
- **Setting**: Cooperative (large/infinite population mean-field), reformulated as a mixed cooperative-competitive 2-player zero-sum MFTG; distributed information structure (each agent sees own state + mean-field); model-free / data-driven RL (zero-order, cost-only access); finite-horizon.

## Method
- Formulate a robust N-agent control problem with linear dynamics, a quadratic performance index Jₙ and noise index ϖₙ; finding a viable attenuation level γ is equivalent to solving the min-max game over the robust cost Jγₙ. Because of the distributed information structure, single-agent robust control theory does not apply, so the analysis passes to the mean-field limit (N → ∞).
- Introduce the Robust Mean-Field Control (RMFC) problem and show, under interchangeability of inf and sup, that infᵤ₁ supᵤ₂ Jγ(u¹,u²) is the Nash equilibrium (saddle point) of a 2-player Zero-Sum Mean-Field Type Game (ZS-MFTG), with the controller as minimizer and the non-stochastic disturbance as maximizer.
- In the LQ setting, change variables to yₜ = xₜ − x̄ₜ and zₜ = x̄ₜ to decouple the cost into two 2-player LQ dynamic games (over (K¹,K²) and (L¹,L²)); give sufficient conditions (Coupled Algebraic Riccati equations, positive-definiteness conditions on γ²I − Mγₜ) for existence/uniqueness of the Nash equilibrium and the closed-form Nash value.
- Propose the Receding-horizon Gradient Descent Ascent (RGDA) algorithm (Algorithm 1): an outer loop solving the receding-horizon min-max problem backwards-in-time from t = T−1 (rendering each per-timestep subproblem convex-concave), and an inner loop of gradient descent (on minimizing controls (K¹,L¹)) ascent (on maximizing controls (K²,L²)) to find each timestep's saddle point. Approximate the mean-field with M finite agents.
- Make the algorithm truly model-free by estimating gradients with a zero-order stochastic gradient (cost-only evaluations of perturbed controllers, smoothing radius r, mini-batch size Nb), and project iterates onto a D-ball to ensure stability.

## Theoretical Contributions
- Theorem 2: sufficient conditions (Coupled Algebraic Riccati equations + γ²I − Mγₜ > 0) for existence and uniqueness of the ZS-MFTG Nash equilibrium and closed-form Nash value; linear optimal controllers.
- Theorem 3: sufficient conditions under which a given γ is a viable attenuation level for the original robust N-agent control problem, with the ZS-MFTG Nash controller also serving as the robust controller for the finite-agent game (condition approaches the mean-field condition as N → ∞).
- Theorem 4: linear convergence of the inner-loop gradient descent-ascent (enabled by the convex-concave receding-horizon cost), with per-timestep optimality gaps ≤ ϵ given suitable learning rate, iteration count K = Ω(log(1/ϵ)), mini-batch size Nb = Ω(1/ϵ), and smoothing radius r = O(ϵ).
- Theorem 5: non-asymptotic guarantee that the total accumulated (Nash gap) error over the backwards-in-time outer loop remains O(ϵ), i.e., error does not blow up across timesteps.

## Experiments
- **Environment/Benchmark**: Synthetic LQ mean-field simulations. Main run: horizon T = 3, M = 1000 agents, state/action dimension m = p = 2, inner-loop iterations K = 1000, mini-batch Nb = 5×10⁴, learning rate ηₖ = 0.001; additional runs for T = 15 and T ∈ {2,3,4,5}.
- **Baselines**: E-RGDA (exact-gradient version of RGDA, with access to exact policy gradients); E-DDPG (an exact 2-player zero-sum version of the MADDPG algorithm (Lowe et al., 2017), without the receding-horizon approach).
- **Evaluation metrics**: Error = norm of the difference between iterates and the Nash controllers (mean and standard deviation across runs); convergence behavior versus iteration and versus increasing horizon T.

## Key Results
- RGDA (with stochastic zero-order gradients) imitates E-RGDA in a noisy fashion, showing a downward error trend; the approximation can be sharpened by increasing the mini-batch size Nb and decreasing the smoothing radius r.
- E-RGDA achieves linear convergence: by solving the last timestep first and moving backwards, convexity-concavity at each next timestep is preserved.
- Compared to the E-DDPG baseline, for all T > 1 E-DDPG first diverges until it hits the projection threshold and only then converges, with convergence taking significantly longer as the horizon increases; the receding-horizon approach of RGDA ameliorates this overshooting problem.

## Limitations & Future Work
- Restricted to the Linear-Quadratic (LQ) setting to obtain tractable benchmark solutions; general (non-LQ) robust mean-field problems are not addressed.
- Relies on gradient descent-ascent updates and convex-concave structure induced by the receding-horizon reformulation.
- Future work: explore robust mean-field problems beyond the LQ setting and develop RL algorithms beyond gradient descent-ascent updates; the study of concrete real-world examples is left for future work.

## Relevance to Survey
This paper extends robust control's classical zero-sum dynamic-game formulation of model uncertainty to the large-population, distributed-information MARL regime via the mean-field game/control paradigm, introducing Robust Mean-Field Control and its equivalence to Zero-Sum Mean-Field Type Games. It connects the "model/environment uncertainty + worst-case minimax" main line of robust (MA)RL with scalable mean-field methods and policy-gradient theory for LQ games, and complements model-uncertainty robust MARL (e.g., Zhang et al., 2020b / paper #1) and robust-MARL-with-state-uncertainty (He et al., 2023) by providing provable algorithms and non-asymptotic guarantees in the infinite-population limit.

## Related Work (verbatim excerpts from the paper)
> _[Section 1, Introduction — opening / motivation]_

"Prevailing algorithms for Multi-Agent Reinforcement Learning (MARL) (Zhang et al., 2021b; Li et al., 2021), however, do not model the distinct effects of modeled and un-modeled uncertainties on the transition dynamics, which can result in practical instability in safety-critical applications (Riley et al., 2021)."

"In this paper we consider a large population multi-agent setting, with stochastic and non-stochastic (un-modeled, possibly adversarial) uncertainties. These types of formulations have been studied under the guise of robust control in the single-agent case (Bas¸ar and Bernhard, 2008). The uncertainties (modeled and un-modeled) affect the performance of the system and might even lead to instability. Robust control seeks the robust controller which guarantees a certain level of performance for the system in under a worst-case hypothesis on these uncertainties."

"To overcome this difficulty, we utilize the mean-field game and control paradigm, first introduced in the purely non-cooperative agent setting in (Lasry and Lions, 2006; Huang et al., 2006), which replaces individual agents by a distribution over agent types, which enables characterization and computation of the solution. The approach has then been extended to the cooperative setting through the notion of mean field control (Bensoussan et al., 2013; Carmona and Delarue, 2018). Building on this paradigm, this work is the first to develop scalable algorithms for MARL that can handle model mis-specification or adversarial inputs in the sense of robust control in the very large or possibly infinite number of agents defined by the mean-field."

> _[Section 1, Introduction — "Literature Review" paragraph]_

"Literature Review: Robust control gained importance in the 1970s when control theorists realized the shortcomings of optimal control theory in dealing with model uncertainties (Athans et al., 1977; Harvey and Stein, 1978). The work of (Bas¸ar, 1989) was the first one to formulate the robust control problem as a zero-sum dynamic game between the controller and the uncertainty. Robust RL first introduced by (Morimoto and Doya, 2005) has recently had an increase in interest in for the single agent setting, where its ability to process trajectory data without explicit knowledge of system parameters can be used to learn robust controllers to address worst-case uncertainty (Zhang et al., 2020a; Kos and Song, 2017; Zhang et al., 2021c). Some recent works consider RL in scenarios with reward uncertainties (Zhang et al., 2020b), state uncertainty (He et al., 2023) or uncertainty in other agents' policies (Sun et al., 2022). There have been some works on the intersection of RL for robust and multi-agent control (Li et al., 2019; He et al., 2023), yet there has not been any significant effort to provide (1) sufficient conditions for solvability of the multi-agent robust control problem i.e. determining the noise attenuation level of a system and (2) provable Robust multi-agent RL (RMARL) algorithms in the large population setting, as proposed in this paper."

"This is made possible due to the mean-field game and control paradigm, which considers the limiting case as the number of agents approaches infinity. This paradigm was first introduced in the context of non-cooperative game theory as Mean-Field Games (MFGs) concurrently by (Lasry and Lions, 2006; Huang et al., 2006). Since then, the question of learning equilibria in MFGs has gained momentum, see (Lauri`ere et al., 2022b). In particular, there have been several works dealing with RL for MFGs (Guo et al., 2019; Elie et al., 2020; Perrin et al., 2020; Zaman et al., 2020; Xie et al., 2021; Anahtarci et al., 2023), deep RL for MFGs (Perrin et al., 2021; Cui and Koeppl, 2021a; Lauri`ere et al., 2022a), learning in multi-population MFGs (P´erolat et al., 2022; Zaman et al., 2021, 2023b), independent learning in MFGs (Yongacoglu et al., 2022; Yardim et al., 2023), oracle-free RL for MFGs (Angiuli et al., 2022; Zaman et al., 2023a) and RL for graphon games (Cui and Koeppl, 2021b; Fabian et al., 2023). There have also been several works on RL for MFC, which is the cooperative counterpart, see e.g. (Carmona et al., 2019a,b; Gu et al., 2021; Mondal et al., 2022; Angiuli et al., 2022). But these works require ability to sample from the true transition model, and hence are inapplicable in the case of mis-specification or modeling errors. To address this setting, we introduce the Robust MFC problem. We will connect this problem to MFTGs Tembine (2017), which contain mixed cooperative-competitive elements. Zero-sum MFTG model a zero-sum competition between two infinitely large teams of agents. Prior work on the theoretical framework of zero-sum MFTG include (Choutri et al., 2019; Tembine, 2017; Cosso and Pham, 2019; Carmona et al., 2021; Guan et al., 2024). Related to RL, the works (Carmona et al., 2020, 2021) propose a data-driven RL algorithm based on Policy Gradient to compute the Nash equilibrium between the two coalitions in an LQ setting but do not provide a theoretical analysis of the algorithm."

### Cited references (resolved from the paper's bibliography)
- **[Zhang et al., 2021b]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control 2021.
- **[Li et al., 2021]** Li, Tang, Zhang, Li. *Distributed reinforcement learning for decentralized linear quadratic control: A derivative-free policy optimization approach.* IEEE Transactions on Automatic Control 2021.
- **[Riley et al., 2021]** Riley, Calinescu, Paterson, Kudenko, Banks. *Utilising assured multi-agent reinforcement learning within safety-critical scenarios.* Procedia Computer Science 2021.
- **[Bas¸ar and Bernhard, 2008]** Başar, Bernhard. *H-infinity optimal control and related minimax design problems: a dynamic game approach.* Springer 2008.
- **[Lasry and Lions, 2006]** Lasry, Lions. *Jeux à champ moyen. I – le cas stationnaire.* Comptes Rendus Mathématique 2006.
- **[Huang et al., 2006]** Huang, Malhamé, Caines. *Large population stochastic dynamic games: Closed-loop McKean-Vlasov systems and the Nash certainty equivalence principle.* Communications in Information & Systems 2006.
- **[Bensoussan et al., 2013]** Bensoussan, Frehse, Yam, et al. *Mean field games and mean field type control theory.* Springer 2013.
- **[Carmona and Delarue, 2018]** Carmona, Delarue. *Probabilistic Theory of Mean Field Games with Applications I.* Springer 2018.
- **[Athans et al., 1977]** Athans, Castanon, Dunn, Greene, Lee, Sandell, Willsky. *The stochastic control of the F-8C aircraft using a multiple model adaptive control (MMAC) method – part I: Equilibrium flight.* IEEE Transactions on Automatic Control 1977.
- **[Harvey and Stein, 1978]** Harvey, Stein. *Quadratic weights for asymptotic regulator properties.* IEEE Transactions on Automatic Control 1978.
- **[Bas¸ar, 1989]** Başar. *A dynamic games approach to controller design: Disturbance rejection in discrete time.* Proc. 28th IEEE Conference on Decision and Control 1989.
- **[Morimoto and Doya, 2005]** Morimoto, Doya. *Robust reinforcement learning.* Neural Computation 2005.
- **[Zhang et al., 2020a]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Kos and Song, 2017]** Kos, Song. *Delving into adversarial attacks on deep policies.* arXiv preprint arXiv:1705.06452 2017.
- **[Zhang et al., 2021c]** Zhang, Zhang, Hu, Başar. *Derivative-free policy optimization for linear risk-sensitive and robust control design: Implicit regularization and sample complexity.* NeurIPS 2021.
- **[Zhang et al., 2020b]** Zhang, Sun, Tao, Genc, Mallya, Başar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[He et al., 2023]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research 2023.
- **[Sun et al., 2022]** Sun, Kim, How. *ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* ICRA 2022.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Lauri`ere et al., 2022b]** Laurière, Perrin, Pérolat, Girgin, Muller, Élie, Geist, Pietquin. *Learning mean field games: A survey.* arXiv preprint arXiv:2205.12944 2022.
- **[Guo et al., 2019]** Guo, Hu, Xu, Zhang. *Learning mean-field games.* NeurIPS 2019.
- **[Elie et al., 2020]** Elie, Perolat, Laurière, Geist, Pietquin. *On the convergence of model free learning in mean field games.* (AAAI) 2020.
- **[Perrin et al., 2020]** Perrin, Pérolat, Laurière, Geist, Elie, Pietquin. *Fictitious play for mean field games: Continuous time analysis and applications.* NeurIPS 2020.
- **[Zaman et al., 2020]** Zaman, Zhang, Miehling, Başar. *Reinforcement learning in non-stationary discrete-time linear-quadratic mean-field games.* IEEE CDC 2020.
- **[Xie et al., 2021]** Xie, Yang, Wang, Minca. *Learning while playing in mean-field games: Convergence and optimality.* ICML 2021.
- **[Anahtarci et al., 2023]** Anahtarci, Kariksiz, Saldi. *Q-learning in regularized mean-field games.* Dynamic Games and Applications 2023.
- **[Perrin et al., 2021]** Perrin, Laurière, Pérolat, Geist, Élie, Pietquin. *Mean field games flock! The reinforcement learning way.* IJCAI 2021.
- **[Cui and Koeppl, 2021a]** Cui, Koeppl. *Approximately solving mean field games via entropy-regularized deep reinforcement learning.* AISTATS 2021.
- **[Lauri`ere et al., 2022a]** Laurière, Perrin, Girgin, Muller, Jain, Cabannes, Piliouras, Pérolat, Elie, Pietquin, et al. *Scalable deep reinforcement learning algorithms for mean field games.* ICML 2022.
- **[P´erolat et al., 2022]** Pérolat, Perrin, Elie, Laurière, Piliouras, Geist, Tuyls, Pietquin. *Scaling mean field games by online mirror descent.* AAMAS 2022.
- **[Zaman et al., 2021]** Zaman, Bhatt, Başar. *Adversarial linear-quadratic mean-field games over multigraphs.* IEEE CDC 2021.
- **[Zaman et al., 2023b]** Zaman, Miehling, Başar. *Reinforcement learning for non-stationary discrete-time linear–quadratic mean-field games in multiple populations.* Dynamic Games and Applications 2023.
- **[Yongacoglu et al., 2022]** Yongacoglu, Arslan, Yüksel. *Independent learning and subjectivity in mean-field games.* IEEE CDC 2022.
- **[Yardim et al., 2023]** Yardim, Cayci, Geist, He. *Policy mirror ascent for efficient and independent learning in mean field games.* ICML 2023.
- **[Angiuli et al., 2022]** Angiuli, Fouque, Laurière. *Unified reinforcement Q-learning for mean field game and control problems.* Mathematics of Control, Signals, and Systems 2022.
- **[Zaman et al., 2023a]** Zaman, Koppel, Bhatt, Başar. *Oracle-free reinforcement learning in mean-field games along a single sample path.* AISTATS 2023.
- **[Cui and Koeppl, 2021b]** Cui, Koeppl. *Learning graphon mean field games and approximate Nash equilibria.* 2021.
- **[Fabian et al., 2023]** Fabian, Cui, Koeppl. *Learning sparse graphon mean field games.* AISTATS 2023.
- **[Carmona et al., 2019a]** Carmona, Laurière, Tan. *Linear-quadratic mean-field reinforcement learning: convergence of policy gradient methods.* arXiv preprint arXiv:1910.04295 2019.
- **[Carmona et al., 2019b]** Carmona, Laurière, Tan. *Model-free mean-field reinforcement learning: mean-field MDP and mean-field Q-learning.* arXiv preprint arXiv:1910.12802 2019.
- **[Gu et al., 2021]** Gu, Guo, Wei, Xu. *Mean-field controls with Q-learning for cooperative MARL: convergence and complexity analysis.* SIAM Journal on Mathematics of Data Science 2021.
- **[Mondal et al., 2022]** Mondal, Agarwal, Aggarwal, Ukkusuri. *On the approximation of cooperative heterogeneous multi-agent reinforcement learning (MARL) using mean field control (MFC).* JMLR 2022.
- **[Tembine, 2017]** Tembine. *Mean-field-type games.* AIMS Mathematics 2017.
- **[Choutri et al., 2019]** Choutri, Djehiche, Tembine. *Optimal control and zero-sum games for Markov chains of mean-field type.* Mathematical Control and Related Fields 2019.
- **[Cosso and Pham, 2019]** Cosso, Pham. *Zero-sum stochastic differential games of generalized McKean–Vlasov type.* Journal de Mathématiques Pures et Appliquées 2019.
- **[Carmona et al., 2021]** Carmona, Hamidouche, Laurière, Tan. *Linear-quadratic zero-sum mean-field type games: Optimality conditions and policy optimization.* Journal of Dynamics & Games 2021.
- **[Guan et al., 2024]** Guan, Afshari, Tsiotras. *Zero-sum games between mean-field teams: Reachability-based analysis under mean-field sharing.* AAAI 2024.
- **[Carmona et al., 2020]** Carmona, Hamidouche, Laurière, Tan. *Policy optimization for linear-quadratic zero-sum mean-field type games.* IEEE CDC 2020.
