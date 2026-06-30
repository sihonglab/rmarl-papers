# 73. Byzantine Robust Cooperative Multi-Agent Reinforcement Learning as a Bayesian Game

## Metadata
- **Title**: Byzantine Robust Cooperative Multi-Agent Reinforcement Learning as a Bayesian Game
- **Authors**: Simin Li, Jun Guo, Jingqiao Xiu, Ruixiao Xu, Xin Yu, Jiakai Wang, Aishan Liu, Yaodong Yang, Xianglong Liu
- **Affiliation**: SKLSDE Lab, Beihang University, China; Zhongguancun Laboratory, China; Institute of Artificial Intelligence, Peking University & BigAI, China; Institute of data space, Hefei Comprehensive National Science Center, China
- **Venue**: ICLR 2024
- **Link/arXiv**: arXiv:2305.12872v3 [cs.GT]; code at https://github.com/DIG-Beihang/EIR-MAPPO

## Taxonomy
- **Robustness / perturbation type targeted**: Byzantine failures / adversarial (and faulty) agents in cooperative MARL — any ally agent can be compromised and take arbitrary, worst-case actions (action perturbation / non-oblivious adversarial policy); also evaluated against random allies and observation-based / transfer-based attacks.
- **Method paradigm**: Bayesian game formulation (types assigned by nature), robust Markov perfect Bayesian equilibrium (ex interim vs. ex ante), maximin / worst-case optimization, robust Harsanyi-Bellman equation, two-timescale actor-critic with belief inference.
- **Keywords**: Byzantine robustness, cooperative MARL, Bayesian game, ex interim equilibrium, robust Markov perfect Bayesian equilibrium, posterior belief, non-oblivious adversary

## TL;DR
The paper formalizes Byzantine-robust cooperative MARL as a Bayesian Adversarial Robust Dec-POMDP (BARDec-POMDP) that treats potential adversaries as nature-assigned types, proposes the ex interim robust Markov perfect Bayesian equilibrium (which weakly dominates prior ex ante robust approaches as time goes to infinity), and realizes it via a robust Harsanyi-Bellman equation and a belief-conditioned two-timescale actor-critic (EIR-MAPPO) with almost-sure convergence guarantees.

## Problem & Motivation
Cooperative MARL (c-MARL) assumes full cooperation, but real-world deployments deviate from this: individual agents may act unpredictably due to hardware/software malfunction or display worst-case adversarial behavior if compromised by a non-oblivious adversary. This "Byzantine failure" undermines the cooperative premise and renders learned policies non-robust. Defenders are left in the dark about which ally is compromised and what its actions might be. Single-agent RL handles uncertainty via robust MDPs (maximin between an uncertainty set and a robust agent), but extending robustness to c-MARL under uncertain allies is much harder. Prior robust MARL methods presuppose every agent is potentially adversarial, which (as the paper argues) corresponds to a conservative ex ante equilibrium that masks the trade-off between cooperation and robustness and yields overly conservative strategies given the low likelihood that adversaries control all agents.

## Robustness Setting
- **Threat model / uncertainty set**: At the onset of an episode, nature draws a type θ from type space Θ = ×ᵢΘᵢ with θᵢ ∈ {0,1}; θᵢ = 1 means agent i is adversarial and its action is replaced by an adversary policy π̂ⁱ(·|Hⁱ, θ), formalized by an action-perturbation probability Pα. Within an episode the type cannot change and there is exactly one attacker (the paper assumes one agent is vulnerable per episode, in line with M3DDPG). The attacker can arbitrarily manipulate the actions of agents with θᵢ = 1. A worst-case adversary is shown to always exist (the attacker solves an RL/POMDP/Dec-POMDP problem against fixed defenders).
- **Setting**: cooperative (c-MARL, Dec-POMDP with shared reward); CTDE — defender uses global state and other agents' information during training but relies only on partial observations and is agnostic to others' types during testing; online; the defender's policy is fixed during an attack and must resist the worst-case adversary π̂*.

## Method
- **BARDec-POMDP formulation**: Augments Dec-POMDP with a type space Θ, an adversary policy π̂, and an action-perturbation transition Pα(at|at, π̂, θ) so that the Byzantine adversary is modeled as an uncertain transition; existing robust MARL (M3DDPG Θ=1ᴺ, plain Dec-POMDP Θ=0ᴺ) become special cases.
- **Solution concepts**: Defines ex ante robust Markov perfect Bayesian equilibrium (RMPBE), which maximizes expected value under the prior p(θ) (what prior robust c-MARL implicitly seeks), and the proposed ex interim RMPBE, where each agent maximizes expected value under its posterior belief bⁱ = p(θ|Hⁱ) updated by Bayes' rule (consistency) and acts with sequential rationality. Existence of mixed-strategy RMPBE is proved via Kakutani's fixed point theorem; pure-strategy equilibria need not exist (zero-sum-like), so optimal robust policies are stochastic.
- **Robust Harsanyi-Bellman equation**: A Bellman-type value update that accounts for the posterior belief over other agents' types and the worst-case adversary, defining two Q functions (before perturbation Qⁱ for defender decision-making; after perturbation for policy gradients / adversary), shown to be a contraction converging to the optimal value via Banach's fixed point theorem.
- **Two-timescale actor-critic (EIR-MAPPO)**: Derives the policy gradient theorem for robust agents and adversaries (the type θ cuts off gradients of agents/adversaries appropriately); updates the adversary on a faster timescale (essentially equilibrated) and the defender on a slower timescale (quasi-static), giving almost-sure convergence under stochastic-approximation assumptions. The critic is trained with TD loss, and the belief network pξ(θ|Hⁱ) (a GRU approximating the Bayes posterior, since true beliefs are inaccessible at deployment) is trained with binary cross-entropy. Built on top of MAPPO.

## Theoretical Contributions
- **Existence of worst-case adversary** (Proposition 2.1): for any robust c-MARL with fixed agent policy, a worst-case (most harmful) adversary exists (attacker solves a POMDP/Dec-POMDP).
- **Existence of RMPBE** (Proposition 2.2): under finite agents/state/observation/action spaces, stationary policies, and compact type space, both ex ante and ex interim mixed-strategy RMPBE exist (via Kakutani's fixed point theorem; extension of Kardeş et al. 2011).
- **Weak dominance** (Proposition 2.3): under the belief/consistency assumptions, finite type space and nonzero prior, as t → ∞ the ex interim policy weakly dominates the ex ante policy under the worst-case adversary.
- **Convergence of robust Harsanyi-Bellman equation** (Proposition 3.1): value iteration converges to the optimal Q via a contraction-mapping argument and Banach's fixed point theorem.
- **Policy gradient theorem** (Theorem 3.1) and **almost-sure convergence** of the two-timescale actor-critic under stochastic-approximation assumptions (Borkar; Borkar & Meyn). Finite-sample / global convergence without restrictive assumptions remains open.

## Experiments
- **Environment/Benchmark**: Three cooperative MARL environments — a toy iterative matrix game (proposed by Han et al., 2022, rewarding XNOR/XOR actions across states), Level-Based Foraging (LBF) map 12x12-4p-3f-c, and StarCraft Multi-Agent Challenge (SMAC) map 4m vs 3m (reduces to 3m under one adversary).
- **Baselines**: MADDPG, M3DDPG, MAPPO, RMAAC, EAR-MAPPO (ex ante robust MAPPO variant of Phan et al. 2020 / Zhang et al. 2020c, also an ablation of the proposed method without belief), and an ideal "True Type" oracle that is granted access to the true type. The proposed method is EIR-MAPPO (ex interim robust MAPPO).
- **Evaluation metrics**: Cooperative reward and robust (attacked) reward, with 5 seeds for cooperation and 5×N attacks per environment, plotted with 95% confidence intervals. Four threat types evaluated: (1) non-oblivious worst-case adversaries, (2) random agents, (3) noisy observations with ℓ∞-bounded adversarial noise (ϵ ∈ {0.2, 0.5, 1.0}), and (4) transferred adversaries trained on a surrogate algorithm.

## Key Results
- Under the hardest non-oblivious attack, EIR-MAPPO consistently delivers robust performance close to the maximum achievable reward (50 for Toy, 1.0 for LBF, 20 for SMAC), outperforming baselines by large margins and matching the ideal "True Type" defense, while maintaining cooperative performance on par with MAPPO.
- Across diverse uncertainties, EIR-MAPPO surpasses baselines in average reward by 5.81% on Toy, 5.88% on LBF, and 25.45% on SMAC; EIR-MAPPO and True Type yield the highest reward in almost all LBF and SMAC settings.
- Behaviorally, EIR-MAPPO learns intricate micromanagement (focused fire and kiting simultaneously) under attack, whereas MADDPG/M3DDPG are easily swayed, MAPPO/RMAAC lack micromanagement, and EAR-MAPPO performs unfocused fire / bad kiting.
- EIR-MAPPO also remains robust to observation perturbations it never trained against (whereas RMAAC, designed for observation attacks, fails against unseen action perturbations), because observational attacks ultimately reduce to a form of action uncertainty.

## Limitations & Future Work
- The threat model assumes a single attacker controlling one agent per episode with a fixed type within an episode; richer type spaces (multiple adversaries, intermittent perturbation, non-binary types) are noted only as straightforward extensions, not evaluated.
- Establishing finite-sample, global convergence guarantees without restrictive assumptions remains an open problem; the two-timescale adversary learning rate requires extensive tuning and can be unstable.
- A MADDPG (deterministic) implementation is not advised since pure-strategy RMPBE need not exist.
- Future work: apply the method to c-MARL applications such as robot swarm control, traffic light management, and power grid maintenance.

## Relevance to Survey
A central robust-MARL contribution on the "adversarial / Byzantine agents" line, recasting fault/attack tolerance through a Bayesian-game lens with nature-assigned types. It explicitly reframes prior robust c-MARL (M3DDPG, ROMAX, Phan et al., Nisioti et al.) as pursuing a conservative ex ante equilibrium and proposes a less conservative, belief-conditioned ex interim equilibrium that provably weakly dominates them, connecting robust MDP theory (Nilim & El Ghaoui; Iyengar; Wiesemann et al.; robust stochastic games of Kardeş et al.), action-robust RL (Tessler et al.), state-adversarial MDP/MARL (Zhang et al. 2020a; He et al. 2023), and ad hoc coordination Bayesian games (Harsanyi; Albrecht & Ramamoorthy). It sits at the intersection of the "adversarial agents / action perturbation" robustness theme and the "game-theoretic equilibrium + actor-critic with convergence guarantees" method line.

## Related Work (verbatim excerpts from the paper)

> _[Section 1, Introduction — "Related Work." paragraph]_

"Our research belongs to the field of robust RL, theoretically framed as robust MDPs (Nilim & El Ghaoui, 2005; Iyengar, 2005; Tamar et al., 2013; Wiesemann et al., 2013). This framework trains a defender to counteract a worst-case adversary amid uncertainty, which can stem from environment transitions (Pinto et al., 2017; Mankowitz et al., 2019), actions (Tessler et al., 2019), states (Zhang et al., 2020a; 2021) and rewards (Wang et al., 2020). In robust MARL, action uncertainty has been a central focus. M3DDPG (Li et al., 2019) enhances robustness in MARL through agents taking jointly worst-case actions under a small perturbation budget. Evaluation was done via one agent consistently introducing worst-case perturbations. This is later known as adversarial policy (Gleave et al., 2019) or non-oblivious adversary (Dinh et al., 2023), a practical and detrimental form of attack. Follow-up works either enhanced M3DDPG (Sun et al., 2022) or defended against uncertain adversaries by presupposing each agent as potentially adversarial (Nisioti et al., 2021; Phan et al., 2020; 2021), which our BARDec-POMDP formulation interprets as seeking a conservative ex ante equilibrium. Another approach by Kalogiannis et al. (2022) studies a special case that the adversary is known. Besides action perturbation, studies have also explored robust MARL under uncertainties in reward (Zhang et al., 2020c), environmental dynamics (Zhao et al., 2020), and observations (Han et al., 2022; He et al., 2023; Zhou & Liu, 2023)."

"Bayesian games and their MARL applications represents another relevant field. With roots in Harsanyi's pioneering work (Harsanyi, 1967), Bayesian games have been used to analyze games with incomplete information by transforming them into complete information games featuring chance moves made by nature. Within MARL, Bayesian games have been utilized to coordinate varying agent types, a concept known as ad hoc coordination (Albrecht & Ramamoorthy, 2015; Albrecht et al., 2016; Stone et al., 2010; Barrett et al., 2017). This problem was theoretically framed as a stochastic Bayesian game and solved using the Harsanyi-Bellman ad hoc coordination algorithm (Albrecht & Ramamoorthy, 2015). Subsequent research has concentrated on agents with varying types (Ravula, 2019), open ad hoc teamwork (Rahman et al., 2022), and human coordination (Tylkin et al., 2021; Strouse et al., 2021). Our work differs from these works by assuming a worst-case, non-oblivious adversary with conflicting goals, whereas in ad hoc coordination, agents have common goals and non-conflicting secondary objectives (Grosz & Kraus, 1999; Mirsky et al., 2022)."

> _[Section 1, Introduction — opening / motivation paragraphs]_

"In single-agent reinforcement learning (RL), robustness under uncertainty is addressed through a maximin optimization between an uncertainty set and a robust agent within the framework of robust Markov Decision Processes (MDPs) (Nilim & El Ghaoui, 2005; Iyengar, 2005; Wiesemann et al., 2013; Pinto et al., 2017; Tessler et al., 2019; Zhang et al., 2020a). However, ensuring robustness in c-MARL when dealing with uncertain allies presents a greater challenge. This is largely due to the potential for Byzantine failure (Yin et al., 2018; Xue et al., 2021), situations where defenders are left in the dark regarding which ally may be compromised and what their resulting actions might be."

"To address Byzantine failures, we employ a Bayesian game approach, which treats Byzantine adversaries as types assigned by nature, with each agent operating unaware of others' type. We formalize robust c-MARL as a Bayesian Adversarial Robust Dec-POMDP (BARDec-POMDP), where existing robust MARL researches (Li et al., 2019; Sun et al., 2022; Phan et al., 2020; 2021) can be reinterpreted as pursuing an ex ante equilibrium (Shoham & Leyton-Brown, 2008), viewing all other agents as potential adversaries. However, these methods might not yield optimal outcomes as they can mask the trade-offs between the equilibria that cooperative and robustness-focused agents aim for. Moreover, this approach can result in overly conservative strategies (Li et al., 2019; Sun et al., 2022), given the low likelihood of adversaries taking control of all agents."

> _[Section 2.3, Threat Model]_

"The robustness towards action perturbations in both single and multi-agent RL has gained prominence since the pioneering works of (Tessler et al., 2019; Li et al., 2019). Action uncertainties, formulated as a type of adversarial attack known as adversarial policy (Gleave et al., 2019; Wu et al., 2021; Guo et al., 2021), or non-oblivious adversary (Dinh et al., 2023), represent a pragmatic and destructive form of attack that is challenging to counter."

### Cited references (resolved from the paper's bibliography)
- **[Nilim & El Ghaoui, 2005]** A. Nilim, L. El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 2005.
- **[Iyengar, 2005]** G. N. Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **[Tamar et al., 2013]** A. Tamar, H. Xu, S. Mannor. *Scaling up robust MDPs by reinforcement learning.* arXiv:1306.6189, 2013.
- **[Wiesemann et al., 2013]** W. Wiesemann, D. Kuhn, B. Rustem. *Robust Markov decision processes.* Mathematics of Operations Research, 2013.
- **[Pinto et al., 2017]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Mankowitz et al., 2019]** D. J. Mankowitz, N. Levine, R. Jeong, et al. *Robust reinforcement learning for continuous control with model misspecification.* arXiv:1906.07516, 2019.
- **[Tessler et al., 2019]** C. Tessler, Y. Efroni, S. Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Zhang et al., 2020a]** H. Zhang, H. Chen, C. Xiao, B. Li, M. Liu, D. Boning, C.-J. Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Zhang et al., 2021]** H. Zhang, H. Chen, D. Boning, C.-J. Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **[Wang et al., 2020]** J. Wang, Y. Liu, B. Li. *Reinforcement learning with perturbed rewards.* AAAI 2020.
- **[Li et al., 2019]** S. Li, Y. Wu, X. Cui, H. Dong, F. Fang, S. Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[Gleave et al., 2019]** A. Gleave, M. Dennis, C. Wild, N. Kant, S. Levine, S. Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[Dinh et al., 2023]** L. C. Dinh, D. H. Mguni, L. Tran-Thanh, J. Wang, Y. Yang. *Online Markov decision processes with non-oblivious strategic adversary.* Autonomous Agents and Multi-Agent Systems, 2023.
- **[Sun et al., 2022]** C. Sun, D.-K. Kim, J. P. How. *ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* ICRA 2022.
- **[Nisioti et al., 2021]** E. Nisioti, D. Bloembergen, M. Kaisers. *Robust multi-agent Q-learning in cooperative games with adversaries.* AAAI 2021.
- **[Phan et al., 2020]** T. Phan, T. Gabor, A. Sedlmeier, et al. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
- **[Phan et al., 2021]** T. Phan, L. Belzner, T. Gabor, A. Sedlmeier, F. Ritz, C. Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Kalogiannis et al., 2022]** F. Kalogiannis, I. Anagnostides, I. Panageas, et al. *Efficiently computing Nash equilibria in adversarial team Markov games.* arXiv:2208.02204, 2022.
- **[Zhang et al., 2020c]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Zhao et al., 2020]** E. Zhao, A. R. Trott, C. Xiong, S. Zheng. *ERMAS: Learning policies robust to reality gaps in multi-agent simulations.* 2020.
- **[Han et al., 2022]** S. Han, S. Su, S. He, S. Han, H. Yang, F. Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **[He et al., 2023]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research, 2023.
- **[Zhou & Liu, 2023]** Z. Zhou, G. Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv:2306.06136, 2023.
- **[Harsanyi, 1967]** J. C. Harsanyi. *Games with incomplete information played by "Bayesian" players, i–iii part i. the basic model.* Management Science, 1967.
- **[Albrecht & Ramamoorthy, 2015]** S. V. Albrecht, S. Ramamoorthy. *A game-theoretic model and best-response learning method for ad hoc coordination in multiagent systems.* arXiv:1506.01170, 2015.
- **[Albrecht et al., 2016]** S. V. Albrecht, J. W. Crandall, S. Ramamoorthy. *Belief and truth in hypothesised behaviours.* Artificial Intelligence, 2016.
- **[Stone et al., 2010]** P. Stone, G. Kaminka, S. Kraus, J. Rosenschein. *Ad hoc autonomous agent teams: Collaboration without pre-coordination.* AAAI 2010.
- **[Barrett et al., 2017]** S. Barrett, A. Rosenfeld, S. Kraus, P. Stone. *Making friends on the fly: Cooperating with new teammates.* Artificial Intelligence, 2017.
- **[Ravula, 2019]** M. C. R. Ravula. *Ad-hoc teamwork with behavior-switching agents.* PhD thesis, 2019.
- **[Rahman et al., 2022]** A. Rahman, I. Carlucho, N. Höpner, S. V. Albrecht. *A general learning framework for open ad hoc teamwork using graph-based policy learning.* arXiv:2210.05448, 2022.
- **[Tylkin et al., 2021]** P. Tylkin, G. Radanovic, D. C. Parkes. *Learning robust helpful behaviors in two-player cooperative Atari environments.* AAMAS 2021.
- **[Strouse et al., 2021]** DJ Strouse, K. McKee, M. Botvinick, E. Hughes, R. Everett. *Collaborating with humans without human data.* NeurIPS 2021.
- **[Grosz & Kraus, 1999]** B. J. Grosz, S. Kraus. *The evolution of SharedPlans.* Foundations of rational agency, 1999.
- **[Mirsky et al., 2022]** R. Mirsky, I. Carlucho, A. Rahman, et al. *A survey of ad hoc teamwork research.* EUMAS 2022.
- **[Yin et al., 2018]** D. Yin, Y. Chen, R. Kannan, P. Bartlett. *Byzantine-robust distributed learning: Towards optimal statistical rates.* ICML 2018.
- **[Xue et al., 2021]** W. Xue, W. Qiu, B. An, Z. Rabinovich, S. Obraztsova, C. K. Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* arXiv:2108.03803, 2021.
- **[Shoham & Leyton-Brown, 2008]** Y. Shoham, K. Leyton-Brown. *Multiagent systems: Algorithmic, game-theoretic, and logical foundations.* Cambridge University Press, 2008.
- **[Wu et al., 2021]** X. Wu, W. Guo, H. Wei, X. Xing. *Adversarial policy training against deep reinforcement learning.* USENIX Security 2021.
- **[Guo et al., 2021]** W. Guo, X. Wu, S. Huang, X. Xing. *Adversarial policy learning in two-player competitive games.* ICML 2021.
