# 113. Distributed Robust Dispatch for Networked Microgrids With Coalition Game-Guided Multiagent Adversarial Safe Reinforcement Learning

## Metadata
- **Title**: Distributed Robust Dispatch for Networked Microgrids With Coalition Game-Guided Multiagent Adversarial Safe Reinforcement Learning
- **Authors**: Tianjiao Pu, Shuai Du, Lei Dong, Ji Qiao
- **Affiliation**: China Electric Power Research Institute, Beijing, China; North China Electric Power University, Beijing, China
- **Venue**: IEEE Transactions on Industrial Informatics, Vol. 22, No. 1, January 2026
- **Link/arXiv**: Digital Object Identifier 10.1109/TII.2025.3609841

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty in state transition probability (source-load fluctuations of renewable generation and load); distributionally robust formulation with an adversary that perturbs the transition distribution; safety constraints (constrained MDP / CVaR).
- **Method paradigm**: Distributionally robust constrained MDP (DR-CMDP); adversarial safe RL (max-min / minimax); Wasserstein GAN with gradient penalty (WGAN-GP) as adversary; CVaR risk-sensitive constraint; constrained policy optimization (CPO); cooperative/coalition game theory (Shapley / Aumann-Shapley value) for multiagent convergence.
- **Keywords**: Adversarial safe reinforcement learning, coalition game-guided multiagent training, distributed robust dispatch, networked microgrids, WGAN-GP, CVaR.

## TL;DR
The paper proposes a coalition game-guided multiagent adversarial safe RL method for distributed robust economic dispatch of networked microgrids, formulating each microgrid's problem as a distributionally robust constrained MDP (DR-CMDP) whose adversary is a WGAN-GP that perturbs only the source-load transition distribution while a CVaR-constrained protagonist guarantees safety, all coordinated privately via a coalition game using only boundary power and HMAC integrity checks.

## Problem & Motivation
Distributed economic dispatch of networked microgrids (NMGs) must handle the flexibility and uncertainty introduced by distributed energy resources (DERs). Model-driven optimization (consensus algorithms, SO, RO, DRO) is effective but its solving complexity and decision time escalate as network size and number of management entities grow. RL/MARL reduces online decision time via offline training but (i) typically incorporates operation constraints only as reward penalties, leading to unsafe decisions, and (ii) usually shares states and actions to build a global critic, overlooking privacy. Existing safe RL (SRL) work on NMGs assumes predefined source/load probability distributions, which inadequately captures uncertainty and lacks robustness. Existing adversarial training for robustness simply gives the adversary the same action space as the protagonist, a generic design unsuited to source-load uncertainty in MG dispatch, and pairs the adversary only with traditional (unsafe) RL protagonists. The paper addresses robustness, safety, and privacy simultaneously.

## Robustness Setting
- **Threat model / uncertainty set**: The state transition probability p is treated as uncertain, following a distribution μ inside an ambiguity set (DR-CMDP). An adversary agent (network parameters ϕ) simulates this distribution via WGAN-GP, restricted to the source-load component s2 (PV and load at t−1). The learned transition is bounded inside an average ε-Wasserstein ball around the initial/reference distribution μ0 (transition Wasserstein distance constraint). The adversary perturbs only the source-load transition distribution, not the protagonist's full action space.
- **Setting**: Cooperative multiagent (networked microgrids coordinated via coalition game); privacy-preserving decentralized training without a global critic that shares local states/actions (only boundary power P^BB is shared); offline training with online execution; per-MG protagonist vs. environment-perturbing adversary forms a per-agent zero-sum-style max-min while MGs cooperate.

## Method
- **DR-CMDP formulation**: Reformulate each MG's dispatch as (s, a, R, C, ρ, p), combining CMDP (constraint function C bounding the action space with safety constraints, derived from power-flow result constraints) and DR-MDP (additional distribution on transition p). State includes time, prior MT/ESS energy, and lagged PV/load; action is the MT/ESS active and reactive power setpoints sampled from a DNN policy π_θ.
- **Adversary as WGAN-GP**: The transition is simplified so only the source-load part p(s2|s) is uncertain; a WGAN-GP (separately for PV and load) generates its distribution μ_ϕ. Wasserstein distance is chosen over KL/JS because it stays meaningful and differentiable even when supports do not overlap during alternating updates.
- **Adversarial max-min objective**: In each episode the protagonist maximizes and the adversary minimizes the expected discounted return E_{μϕ}[E_{πθ, p∼μϕ}[Σ γ^t R_t]]; well-defined via three constraints: a CVaR safety constraint (risk level α = 0.05), a KL trust-region constraint on the policy, and the ε-Wasserstein constraint on the transition.
- **Protagonist update**: Trust-region (importance sampling + advantage) objective augmented with an entropy bonus and a proposed gradient-penalty term that uses the coalition-game benefit to indirectly represent other MGs' unknown cost discrepancies; CVaR made tractable via a Gaussian closed-form (mean JC, variance JS−JC²); solved with CPO; domain randomization of radial topology per episode for adaptability.
- **Coalition game-guided framework**: Reward = operation-cost reward + coalition-contribution reward (Shapley value, or Aumann-Shapley for many agents); mid-market rate ensures superadditivity, Shapley value ensures a nonempty core. Power flow is decomposed using boundary buses as slack buses so local data is never shared; HMAC verifies sender identity and message integrity, and corrupted episodes are discarded (fault tolerance via offline training).
- **Adversary update**: WGAN-GP pretrained on historical PV/load, then trained to minimize the return subject to the Wasserstein constraint via a PPO Wasserstein-penalized loss; GAE reuses the shared state/reward so the adversary needs no separate critic.

## Theoretical Contributions
- Largely empirical/algorithmic. Provides a game-theoretic convergence argument rather than formal proofs: rationality is met by the adversarial SRL, and convergence/stability is ensured by guaranteeing coalition stability through Superadditivity (Property 1, via mid-market rate) and a Nonempty core (Property 2, via Shapley value). No formal regret/sample-complexity/convergence-rate theorems are given.

## Experiments
- **Environment/Benchmark**: Modified IEEE-123 bus system divided into three MGs (each with a MT, PV panel, ESS, 4 controllable switches), 24-h dispatch with 1-h steps; and a larger practical-grid-derived system (716-bus MG, scaled to 6 MGs / a 4296-bus system) for scalability. PV/load data sourced from California ISO (CAISO).
- **Baselines**: Model-driven — second-order cone programming (SOCP), distributed model predictive control (DMPC), distributionally robust optimization (DRO). RL — PPO, PPO-Lag, multiagent soft actor-critic (MASAC), MASAC-Lag, and FOCOPS. Plus ablations (non-CVaR variant; without coalition-game guidance; protagonist-only / adversary-only training).
- **Evaluation metrics**: Total operation cost, constraint violations (CVs) computed from constraint function C, online decision time, Wasserstein distance, performance under varying prediction errors, seasonal data, topology variations, and scaling (number of agents).

## Key Results
- Against model-driven methods over three cases (initial, worst-case, and fluctuation-after-decision): SOCP yields low costs in Cases I/II but suffers power shortages and higher total cost in Case III; the proposed method attains robustness comparable to DRO while substantially reducing online decision time. At a prediction error of about 6% the proposed method already performs better.
- Against RL/SRL methods in Case III: traditional PPO/MASAC frequently violate constraints; SRL methods (PPO-Lag, MASAC-Lag, FOCOPS) have lower but nonzero CVs and assume predefined source/load distributions; the proposed CVaR-constrained adversarial SRL achieves the lowest cost with no constraint violations, and outperforms its non-CVaR implementation.
- Ablations confirm coalition-game guidance speeds convergence and improves final reward; HMAC allows safely discarding corrupted episodes (assumed once every 10 episodes) while preserving convergence; voltage amplitudes are maintained at [0.968, 1.050] p.u., and the method remains safe and robust under topology changes and larger-scale systems (A-S value chosen over Shapley once agents ≥ 6 to reduce computation time).

## Limitations & Future Work
- The framework depends on accurate historical data for WGAN-GP pretraining.
- Scalability to larger networks considering the hierarchical structure of an actual distribution system remains limited.
- Future work: incorporate hierarchical coordination mechanisms with distribution system operators to address these limitations.

## Relevance to Survey
This paper sits on the distributionally robust RL line applied to a cooperative, privacy-preserving MARL setting (networked microgrids). It connects the robust-MDP / distributionally robust MDP (DR-MDP) theory to constrained/safe RL (CMDP, CVaR, CPO) and to adversarial training, while contributing a domain-tailored adversary design (a WGAN-GP perturbing only the source-load transition distribution within a Wasserstein ambiguity set) rather than the generic same-action-space adversary common in robotics-oriented robust RL. It also bridges to game-theoretic MARL via coalition (cooperative) game theory for convergence and to communication-robustness/integrity themes via HMAC. As such it is a representative application-domain instance of the "environment/transition uncertainty + adversarial training + safety constraints" cluster within robust MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction]_

"The safety requirements associated with the real-world application of RL have led to the development of safe RL (SRL). The primary model of SRL is built upon the constrained Markov decision process (CMDP), which extends traditional Markov decision process (MDP) by integrating safety constraints that reflect real-world conditions. SRL methods update policies within the CMDP context and guarantee both performance improvement and constraint satisfaction, which have been progressively applied to the economic dispatch of NMGs. Zhang et al. [12] presented a multiagent safe policy learning method based on constrained policy optimization (CPO) for optimal power management of NMGs. Lu et al. [13] proposed a multiagent SRL algorithm based on proximal policy optimization (PPO) for optimizing the energy trading strategy in NMGs. A two-stage data-driven method with safety model framework was constructed in [14] to hierarchically coordinate NMGs. However, these studies assume predefined probability distributions for source and load, which inadequately capture their uncertainty and lack robustness."

> _[Section I, Introduction]_

"In addition to safety, robustness is also a critical requirement for the practical application of RL. The modeling of robustness typically involves the robust MDP, which directly incorporates uncertainty in the elements of the MDP. However, the robust MDP formulation assumes no distributional information on elements, which may obtain overly conservative solutions like RO. Therefore, another more complex formulation, named as distributionally robust Markov decision process (DR-MDP) [15], has emerged. DR-MDP assumes uncertainty in the latent distribution generating the MDP elements. It explicitly encodes a prior probability distribution and facilitates a better balance between performance and robustness. To solve the DR-MDP problem, existing methods usually construct the adversary agent to model environmental discrepancies, and then alternately optimize the policies of both the adversary and the protagonist until convergence [16], [17], [18]. However, these methods simply give adversary the same action space as the protagonist, which is a generic design for fields such as robotics and autonomous driving, but cannot fully consider the source-load uncertainty in MG dispatch problem. What is more, the protagonists in these works only use traditional RL. As the adversary finds the worst-case scenario, it is necessary to improve the protagonist's safety by SRL."

> _[Section I, Introduction — summary of gaps]_

"In summary, the existing NMGs dispatch methods have evolved from model-driven optimization to MARL, and subsequently use SRL for safety. However, existing SRL methods assume predefined probability distributions for RESs and load, which inadequately captures source-load uncertainty and results in insufficient robustness. The adversarial training is the mainstream method for enhancing robustness, but existing adversary setup is not suitable for the robust dispatch under source-load fluctuations. Furthermore, existing MARL methods rely on global critics by sharing states and actions of agents, which cannot ensure data security and integrity."

### Cited references (resolved from the paper's bibliography)
- **[12]** Q. Zhang, K. Dehghanpour, Z. Wang, F. Qiu, D. Zhao. *Multi-agent safe policy learning for power management of networked microgrids.* IEEE Trans. Smart Grid, 2021.
- **[13]** R. Lu et al. *SMA-PDPPO: Safe multiagent primal-dual deep reinforcement learning for industrial parks energy trading.* IEEE Trans. Ind. Inform., 2025.
- **[14]** Y. Xia, Y. Xu, X. Feng. *Hierarchical coordination of networked-microgrids toward decentralized operation: A safe deep reinforcement learning method.* IEEE Trans. Sustain. Energy, 2024.
- **[15]** H. Xu, S. Mannor. *Distributionally robust Markov decision processes.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2010.
- **[16]** L. Pinto et al. *Robust adversarial reinforcement learning.* ICML 2017.
- **[17]** P. Huang et al. *Robust reinforcement learning as a Stackelberg game via adaptively-regularized adversarial training.* IJCAI 2022.
- **[18]** Z. Zhang et al. *Robust deep reinforcement learning in robotics via adaptive gradient-masked adversarial attacks.* arXiv:2503.20844, 2025.
