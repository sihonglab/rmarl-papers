# 28. Robust Multi-Agent Reinforcement Learning with State Uncertainty

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning with State Uncertainty
- **Authors**: Sihong He, Songyang Han, Sanbao Su, Shuo Han, Shaofeng Zou, Fei Miao
- **Affiliation**: University of Connecticut (CSE); University of Illinois, Chicago (ECE); University at Buffalo, SUNY (EE)
- **Venue**: Transactions on Machine Learning Research (TMLR) 2023
- **Link/arXiv**: arXiv:2307.16212v1; OpenReview: https://openreview.net/forum?id=CqTkapZ6H9; code: https://github.com/sihongho/robust_marl_with_state_uncertainty

## Taxonomy
- **Robustness / perturbation type targeted**: State / observation uncertainty (adversarial worst-case state perturbations of each agent's observed state, due to sensor errors, noise, missing information, communication issues, or malicious attacks)
- **Method paradigm**: Markov game with state perturbation adversaries (one adversary per agent), Nash-equilibrium-structured robust equilibrium, minimax operator / contraction mapping, robust multi-agent Q-learning, robust multi-agent actor-critic (CTDE), policy gradient
- **Keywords**: state uncertainty, robust MARL, Markov game with state perturbation adversaries (MG-SPA), robust equilibrium, RMAQ, RMAAC

## TL;DR
The paper provides the first systematic theoretical and empirical treatment of MARL under worst-case state uncertainty by modeling it as a Markov Game with State Perturbation Adversaries (MG-SPA), introducing robust equilibrium (RE) as the solution concept with existence guarantees, and proposing a convergent robust multi-agent Q-learning (RMAQ) algorithm plus a scalable robust multi-agent actor-critic (RMAAC) algorithm.

## Problem & Motivation
In real-world MARL applications, agents may not have perfect state information due to inaccurate measurement, noise, missing information, communication issues, or malicious attacks, and a policy not robust to such state uncertainty can lead to unsafe or catastrophic behavior. In single-agent RL, imperfect state information has been studied via POMDPs, but the conditional observation probabilities in POMDPs cannot capture the worst-case (adversarial) scenario. State uncertainty is even more challenging in MARL because each agent's misleading observation affects both its own and other agents' returns, and existing Dec-POMDP tools provide neither theoretical analysis nor algorithms for MARL under worst-case state uncertainties. Little prior work had studied state uncertainties in MARL in either problem formulation or algorithm design, motivating this work.

## Robustness Setting
- **Threat model / uncertainty set**: Each agent i is paired with a state perturbation adversary ĩ that always plays against it. The adversary observes the true state s, picks action b^ĩ via policy ρ^ĩ, and perturbs the observed state to s̃^i = f(s, b^ĩ) where f is the perturbation function (part of the model). The adversary's power is restricted: the perturbed state must lie in an ε-radius ball B_dist(ε, s) measured by an l-norm distance. Each adversary receives the negation of its agent's reward (worst-case / minimax modeling).
- **Setting**: cooperative, competitive, and mixed (general Markov game; experiments cover both cooperative and mixed scenarios); CTDE for the actor-critic algorithm (RMAAC); online, model-free learning; Markov policies as the main case, extended to history-dependent policies.

## Method
- Formulate MARL with state uncertainty as an MG-SPA tuple Ḡ := (N, M, S, {A^i}, {B^ĩ}, {r^i}, p, f, γ), adding an adversary set M = {1̃,…,Ñ}; define value/action-value functions under joint policies (π, ρ) and define robust equilibrium (RE), an NE-structured solution where no agent or adversary has incentive to deviate (Eq. 4). A maximin solution is argued to be insufficient for non-identical-interest MARL, motivating the NE-structured RE.
- Derive Bellman equations for the optimal value via a minimax operator L v^i(s) = max_{π^i} min_{ρ^ĩ}[r^i_d + γ P_d v^i](s); under Assumption 4.4 (bounded rewards; finite state/action spaces; stationary kernels; f bijective; shared reward function) prove L is a contraction on the complete space V (Propositions 4.5–4.6).
- Theorem 4.7 establishes that the optimal value function satisfies the Bellman equations, exists and is unique (Banach fixed point), corresponds to an RE, and that a mixed RE exists; existence is proved by constructing a 2N-player extensive-form game (EFG) whose NE maps to an RE. Results extend to history-dependent policies (Corollary 4.9.1).
- Propose RMAQ: a tabular value-iteration Q-learning update (Eq. 7) where, at each step, an NE policy of the 2N-player EFG over payoffs (q^1,…,q^N,−q^1,…,−q^N) is solved and used to update Q-values for all agents, with convergence to q* (Theorem 5.2) under Assumption 5.1.
- Propose RMAAC: a CTDE actor-critic with function approximation; derive the policy gradients w.r.t. agent parameters θ and adversary parameters ω (Theorem 5.3), where the adversary gradient includes an extra regularization term reg = ∇_{s̃^i} log π^i · ∇_{b^ĩ} f · ∇_{ω^i} ρ^ĩ accounting for the perturbation function; supports history-dependent policies via recent-observation inputs.

## Theoretical Contributions
- Contraction mapping property of the minimax operator L and completeness of the value-function space V (Propositions 4.5, 4.6).
- Existence and uniqueness of the optimal value function and existence of a (mixed) robust equilibrium for an MG-SPA under Assumption 4.4 (Theorem 4.7), proved via an equivalence to the NE of a constructed 2N-player extensive-form game.
- Convergence guarantee (with probability 1) of the RMAQ algorithm to the optimal action-value functions under Assumption 5.1 (Theorem 5.2).
- Policy gradient expressions for both agents and adversaries in the MG-SPA (Theorem 5.3).
- Extension of all results to history-dependent policies with a finite horizon (Corollary 4.9.1).

## Experiments
- **Environment/Benchmark**: A designed two-player game (two states, two actions, shared reward) to validate RMAQ; multi-agent particle environments (MPE) scenarios for RMAAC — Cooperative communication (CC), Cooperative navigation (CN), Physical deception (PD), Predator prey (PP), Keep away (KA), plus a larger-scale Predator prey+ (PP+).
- **Baselines**: MADDPG (no robustness); M3DDPG (robust MARL handling opponent-policy uncertainty via adversarial learning). For the two-player game: Nash equilibrium policy of the original game and a deterministic baseline policy.
- **Evaluation metrics**: Convergence of total discounted reward to the optimal MG-SPA state value (RMAQ); mean episode testing rewards and variance of testing rewards under optimally perturbed, cleaned, and randomly perturbed environments (RMAAC); ablations on history-dependent vs. Markov policies and on noise variance Σ and constraint ε.

## Key Results
- RMAQ converges: total discounted rewards converge to the optimal MG-SPA state value (≈49.99 vs. the theoretical 50.00), and the learned RE policy stays stable as adversary attack probability increases while NE and baseline policies degrade.
- Under optimally disturbed environments, RMAAC achieves the highest mean rewards in almost all MPE scenarios under both linear-noise (f1) and Gaussian-noise (f2) perturbation formats; the only exception is Keep away under linear noise, where RMAAC still wins under Gaussian noise.
- RMAAC attains the lowest variance of testing rewards in most scenarios (more robust to system randomness) and continues to outperform baselines in most scenarios under randomly perturbed environments; consistent with the robustness trade-off, under cleaned environments RMAAC beats all baselines only in Predator prey.
- Ablation: history-dependent policies (h = 4) outperform Markov policies across all five scenarios.

## Limitations & Future Work
- Computing an NE of the EFG each step is hard (computing an NE is PPAD-complete even for general-sum normal-form games), so RMAQ is not expected to scale to very large MARL problems; RMAAC with function approximation is proposed to address scalability.
- Theoretical analysis relies on Assumption 4.4, including finite state/action spaces, a bijective perturbation function, and a shared (common) reward function, which do not always hold in practice.
- Robust policies can sacrifice performance when no perturbation is present (robustness trade-off), so they may underperform non-robust baselines in cleaned environments.
- Future work: heterogeneous agent modeling under state uncertainty; methods for continuous state and action spaces, since discretization is suboptimal and adversarial perturbations can disrupt continuity.

## Relevance to Survey
This is a foundational reference for the "state/observation uncertainty" branch of robust MARL, extending the single-agent state-adversary formulations (e.g., Zhang et al. 2020a; 2021) to the multi-agent setting and providing the first equilibrium-based theory (MG-SPA, robust equilibrium) and convergent algorithms (RMAQ, RMAAC). It connects the model/game-theoretic equilibrium line (Markov games, Nash-Q learning) with the adversarial state-perturbation line, and sits adjacent to robust-MARL works on opponent-policy and reward uncertainty (M3DDPG; Zhang et al. 2020b), making it a key bridge between single-agent state-robust RL and robust MARL.

## Related Work (verbatim excerpts from the paper)

> _[Section 2, Related work — "Robust Reinforcement Learning"]_

"Recent robust reinforcement learning studied different types of uncertainties, such as action uncertainties (Tessler et al., 2019) and transition kernel uncertainties (Sinha et al., 2020; Yu et al., 2021b; Hu et al., 2020; Wang & Zou, 2021; Lim & Autef, 2019; Nisioti et al., 2021; He et al., 2022). Some recent attempts at adversarial state perturbations for single-agent validated the importance of considering state uncertainty and improving the robustness of the learned policy in Deep RL (Huang et al., 2017; Lin et al., 2017; Zhang et al., 2020a; 2021; Everett et al., 2021). The works of Zhang et al. (2020a; 2021) formulate the state perturbation in single-agent RL as a modified Markov decision process, then study the robustness of single-agent RL policies. The works of Huang et al. (2017) and Lin et al. (2017) show that adversarial state perturbation undermines the performance of neural network policies in single-agent reinforcement learning and proposes different single-agent attack strategies. In this work, we consider the more challenging problem of adversarial state perturbation for MARL, when the environment of an individual agent is non-stationary with other agents' changing policies during the training process."

> _[Section 2, Related work — "Robust Multi-Agent Reinforcement Learning"]_

"There is very limited literature on the solution concept or theoretical analysis when considering adversarial state perturbations in MARL. Other types of uncertainties have been investigated in the literature, such as uncertainties about training partner's type (Shen & How, 2021), the other agents' policies (Li et al., 2019; Sun et al., 2021; van der Heiden et al., 2020), and reward uncertainties (Zhang et al., 2020b). However, the policy considered in these papers relies on the true state information. Hence, the robust MARL considered in this work is fundamentally different since the agents do not know the true state information. Dec-POMDP enables a team of agents to optimize policies with the partial observable states (Oliehoek et al., 2016; Chen et al., 2022). The work of Lin et al. (2020) studies state perturbation in identical-interest MARL, and proposes an attack method to attack the state of one single agent in order to decrease the team reward. In contrast, we consider the worst-case scenario that the state of every agent can be perturbed by an adversary and focus on the theoretical analysis of robust MARL including the existence of optimal value function and robust equilibrium (RE). Our work provides formal definitions of the state uncertainty challenge in MARL, and derives both theoretical analysis and practical algorithms."

> _[Section 2, Related work — "Game Theory and MARL"]_

"MARL shares theoretical foundations with the game theory research field and a literature review has been provided to understand MARL from a game theoretical perspective (Yang & Wang, 2020a). A Markov game, sometimes called a stochastic game models the interaction between multiple agents (Owen, 2013; Littman, 1994). Algorithms to compute the Nash equilibrium (NE) in Dec-POMDP (Oliehoek et al., 2016), POSG (partially observable stochastic game) and analysis assuming that NE exists (Chades et al., 2002; Hansen et al., 2004; Nair et al., 2002) have been developed in the literature without proving the conditions for the existence of NE. The main theoretical contributions of this work include proving conditions under which the proposed MG-SPA has robust equilibrium solutions, and convergence analysis of our proposed robust multi-agent Q-learning algorithm. This is the first attempt to analyze the fundamental properties of MARL under adversarial state uncertainties."

### Cited references (resolved from the paper's bibliography)
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Sinha et al., 2020]** Sinha, O'Kelly, et al. *FormulaZero: Distributionally robust online adaptation via offline population synthesis.* ICML 2020.
- **[Yu et al., 2021b]** Yu, Gehring, Schäfer, Anandkumar. *Robust reinforcement learning: A constrained game-theoretic approach.* L4DC 2021.
- **[Hu et al., 2020]** Hu, Shao, Li, Jianye, Liu, Yang, Wang, Zhu. *Robust multi-agent reinforcement learning driven by correlated equilibrium.* 2020.
- **[Wang & Zou, 2021]** Wang, Zou. *Online robust reinforcement learning with model uncertainty.* NeurIPS 2021.
- **[Lim & Autef, 2019]** Lim, Autef. *Kernel-based reinforcement learning in robust Markov decision processes.* ICML 2019.
- **[Nisioti et al., 2021]** Nisioti, Bloembergen, Kaisers. *Robust multi-agent Q-learning in cooperative games with adversaries.* AAAI 2021.
- **[He et al., 2022]** He, Wang, Han, Zou, Miao. *A robust and constrained multi-agent reinforcement learning framework for electric vehicle AMoD systems.* arXiv 2022.
- **[Huang et al., 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[Lin et al., 2017]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* IJCAI 2017.
- **[Zhang et al., 2020a]** H. Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Zhang et al., 2021]** H. Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv 2021.
- **[Everett et al., 2021]** Everett, Lütjens, How. *Certifiable robustness to adversarial state uncertainty in deep reinforcement learning.* IEEE TNNLS 2021.
- **[Shen & How, 2021]** Shen, How. *Robust opponent modeling via adversarial ensemble reinforcement learning.* ICAPS 2021.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Sun et al., 2021]** Sun, Kim, How. *ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* arXiv 2021.
- **[van der Heiden et al., 2020]** van der Heiden, Salge, Gavves, van Hoof. *Robust multi-agent reinforcement learning with social empowerment for coordination and communication.* arXiv 2020.
- **[Zhang et al., 2020b]** K. Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Oliehoek et al., 2016]** Oliehoek, Amato, et al. *A concise introduction to decentralized POMDPs.* Springer 2016.
- **[Chen et al., 2022]** Chen, Liu, Luo, Yin. *Robust multi-agent reinforcement learning for noisy environments.* Peer-to-Peer Networking and Applications 2022.
- **[Lin et al., 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[Yang & Wang, 2020a]** Yang, Wang. *An overview of multi-agent reinforcement learning from game theoretical perspective.* arXiv 2020.
- **[Owen, 2013]** Owen. *Game theory.* Emerald Group Publishing 2013.
- **[Littman, 1994]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994.
- **[Chades et al., 2002]** Chades, Scherrer, Charpillet. *A heuristic approach for solving decentralized-POMDP: Assessment on the pursuit problem.* ACM Symposium on Applied Computing 2002.
- **[Hansen et al., 2004]** Hansen, Bernstein, Zilberstein. *Dynamic programming for partially observable stochastic games.* AAAI 2004.
- **[Nair et al., 2002]** Nair, Tambe, Yokoo, Pynadath, Marsella. *Towards computing optimal policies for decentralized POMDPs.* AAAI Workshop 2002.
