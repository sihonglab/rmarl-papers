# 31. Robust Multi-Agent Reinforcement Learning by Mutual Information Regularization

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning by Mutual Information Regularization
- **Authors**: Simin Li, Ruixiao Xu, Jingqiao Xiu, Yuwei Zheng, Pu Feng, Yuqing Ma, Bo An, Yaodong Yang, Xianglong Liu
- **Affiliation**: Beihang University (State Key Laboratory of Complex and Critical Software Environment / Software Development Environment); Nanyang Technological University; National University of Singapore; Peking University; Zhongguancun Laboratory
- **Venue**: IEEE Transactions on Neural Networks and Learning Systems (TNNLS), Vol. 36, No. 10, October 2025
- **Link/arXiv**: https://doi.org/10.1109/TNNLS.2025.3577259 ; code: https://github.com/DIG-Beihang/MIR3

## Taxonomy
- **Robustness / perturbation type targeted**: Action uncertainty / action perturbation — an unknown subset of cooperative agents takes unpredictable or worst-case adversarial actions (compromised/hacked agents, software/hardware failures); exponentially many threat scenarios from which agents may be perturbed.
- **Method paradigm**: Control-as-inference, mutual information regularization (information bottleneck / robust action prior), regularization-as-robustness (robustness without adversarial training), off-policy evaluation, zero-sum worst-case adversary modeling.
- **Keywords**: robust MARL, mutual information regularization, control-as-inference, information bottleneck, action adversarial Dec-POMDP, worst-case adversary

## TL;DR
MIR3 (mutual information regularization as robust regularization) frames robust cooperative MARL as a control-as-inference problem and proves that penalizing the mutual information between joint histories and actions maximizes a lower bound on worst-case robustness, yielding provably robust policies trained without ever exposing agents to adversaries.

## Problem & Motivation
In cooperative MARL, deployed agents often deviate from their intended policies due to uncertainties, malfunctions, or being hacked into worst-case adversarial behavior. Because each of N agents may independently be perturbed or unperturbed, the number of potential threat scenarios grows exponentially, making per-scenario max-min optimization intractable. Existing robust MARL methods either treat all agents as adversaries (overly pessimistic, agents stop cooperating) or enumerate threat scenarios (insufficiently explored, leaving defenders vulnerable), both at high computational cost. Inspired by human "situational awareness" — maintaining a general level of caution rather than preparing for every threat — the paper seeks implicit worst-case robustness without modeling specific adversaries.

## Robustness Setting
- **Threat model / uncertainty set**: Action uncertainty modeled as an Action Adversarial Dec-POMDP (A2Dec-POMDP). A partition φ ∈ {0,1}^N splits agents into defenders (φ_i = 0, original policy) and adversaries (φ_i = 1, original policy replaced by a worst-case adversarial policy π_α). The attacker acts at test time with the defender's policy fixed, shares the defender's partial observation and action space, and learns a zero-sum worst-case policy that minimizes cumulative reward. Defenders do not know who is the adversary and the perturbed-partition distribution is p(Φ_α).
- **Setting**: Cooperative MARL; CTDE; trained without attacks (only partition φ = 0^N) yet provably robust at test time. Theory leans on the offline-RL uniform coverage assumption for off-policy evaluation.

## Method
- Formalizes robust MARL as an A2Dec-POMDP; the defender objective maximizes both cooperative value V_π(s) and the expected worst-case value under the partition distribution, E_{φ∼p(Φ_α)}[min_{π_α} V_{π,π_α}(s, φ)].
- Adopts control-as-inference (Levine): writes the cooperative and the under-attack objectives, and uses importance sampling / off-policy evaluation to express the worst-case term using only on-policy (no-attack) trajectories τ^0.
- Proves (Proposition 1) that, under a uniform-coverage assumption and using the fact that defender and zero-sum adversary log-policies differ by a constant, J(π) ≥ Σ_t E[r_t − λ I(h_t; a_t)] — i.e., minimizing the mutual information between joint histories and actions maximizes a lower bound on robustness.
- Adds −λ I(h_t; a_t) as a reward-shaping regularizer, so MIR3 is backbone-agnostic (MADDPG, QMIX, MAPPO). MI is intractable, so its upper bound is estimated with CLUB (an off-the-shelf contrastive log-ratio MI upper-bound estimator); for scalability under CTDE, I(h_t; a_t) is approximated by I(s_t; a_t) (one estimator call per training step).
- Two interpretations are given: an information bottleneck (suppressing spurious agent-to-agent correlations, preventing overreaction to failed agents) and a robust action prior (constraining the policy near a learned task-favored marginal p(a), replacing max-entropy RL's uniform prior).

## Theoretical Contributions
- **Proposition 1 (robustness lower bound)**: J(π) ≥ Σ_t E_{τ^0}[r_t − λ I(h_t; a_t)]; minimizing history–action mutual information maximizes a lower bound on worst-case robustness (three-step proof: zero-sum log-policy constant, lower bound over all attack trajectories/partitions under uniform coverage, identification with mutual information).
- **Proposition 2 (convergence)**: Because MIR3 only shapes the reward (without altering policy space, transition dynamics, or observation structure), the MI-augmented Bellman operator is a γ-contraction; by Banach's fixed-point theorem, value iteration converges to the optimal value in the tabular case with finite state/action spaces and infinitely-often visitation.
- Computational-complexity analysis: MIR3 adds only one MI-estimator call per step (vs. multiple gradient backward steps for worst-case-action methods) and zero overhead at test time.

## Experiments
- **Environment/Benchmark**: StarCraft Multi-Agent Challenge (SMAC, six tasks), quadrotor swarm control (Quads), and a continuous ten-agent robot-swarm rendezvous task (simulation + real-world e-puck2 robots in a 2×2 m arena).
- **Baselines**: M3DDPG, ROMAX, ERNIE (treat all other agents as adversaries), ROM-Q (one or more agents as adversaries), and EIR (added on the MAPPO/Quads continuous-control setting). Implemented on MADDPG, QMIX, and MAPPO backbones (M3DDPG/ROMAX not run on QMIX due to reliance on the MADDPG central critic).
- **Evaluation metrics**: Cooperative performance (no attack) and robust performance under worst-case adversaries (one or two adversaries), with 95% confidence intervals; per-epoch training time; ablations over λ and over MI estimators (VUB, L1Out, CLUB, CLUB-Sample); robustness against nonadversarial disturbances (observation noise, action repetition, harder opponents); real-world reward.

## Key Results
- Despite never training against adversaries, MIR3 consistently outperforms all baselines (including those trained with adversaries) in robustness under worst-case one-adversary attacks across six SMAC tasks and two backbones, while maintaining (and slightly improving) cooperative performance at small λ.
- Robustness holds with two adversaries (SMAC 5v3m) and on continuous control with stochastic policies (Quads, MAPPO), and MIR3 better handles nonadversarial disturbances (observation/action failures, stronger opponents) than max-min methods.
- MIR3 adds only moderate training cost over non-robust backbones (e.g., +10.71% MADDPG 4v3m) versus much larger overheads for explicit threat-scenario methods (up to +149.21% on rendezvous).
- In real-world robot-swarm rendezvous deployment, MIR3 achieves +14.29% average reward over the best-performing baseline; an emergent pursuit-evade behavior is observed when an adversary runs away.

## Limitations & Future Work
- The theory relies on the offline-RL uniform coverage assumption, which the authors acknowledge "might not hold" in real-world settings (Remark 3), though it is indispensable in many offline-RL works and favorable for robustness; evaluation under one/two-adversary scenarios violates uniform coverage yet still shows gains.
- Convergence guarantees hold only in the tabular case; practical implementations use nonconvex-nonconcave neural networks.
- Hyperparameter λ requires careful tuning: too large (> 5×10⁻⁴) collapses both cooperative and robust performance.
- For SMAC, an adversary controlling one agent can make the environment unsolvable, so algorithms are given control over additional agents for fair evaluation.

## Relevance to Survey
A representative "robustness without an adversary" / regularization line within action-robust cooperative MARL. It connects the control-as-inference and information-theoretic (mutual information / information bottleneck, max-entropy-as-robustness) threads to the zero-sum worst-case adversary formulation, contrasting itself against enumeration/approximation-based max-min MARL (M3DDPG, ROMAX, ERNIE, ROM-Q, EIR). It complements model-uncertainty robust MARL (e.g., Zhang et al. robust Markov games) and state-adversarial MARL, and is notable for theoretical robustness guarantees plus real-world sim2real validation.

## Related Work (verbatim excerpts from the paper)

> _[Section II-B, Robust MARL]_

"Robust MARL aims to fortify against uncertainties in actions [10], states [35], [36], and rewards/environment [17], [37], [38]. Among these factors, action robustness have become a main focus due to the propensity for multiple agents to act unpredictably during deployment. Algorithms such as M3DDPG [10] and ROMAX [11] treat each agent as an adversary that deviates toward jointly worst-case actions [12]. However, in real world, since not all other agents are adversaries, such a policy can likely be overly pessimistic and make agents not cooperate at all. Later approaches attempt to directly train policies against these worst-case adversaries [18], [19], [22], [39]. However, as these methods must explore numerous distinct adversarial scenarios, each scenario may left insuﬃciently examined. As a consequence, attackers can be less powerful comparing with worst-case adversary, and defenders trained with such weaker attackers can still be vulnerable to worst-case adversaries at test time."

> _[Section II-C, Robustness Without an Adversary]_

"While it is tempting to directly train MARL policy against adversaries via max-min optimization, such process can be overly pessimistic [10], unbalanced across threat scenarios [18], [19], and computationally demanding [23]. A parallel line of research in RL aims to achieve robustness without relying on adversaries. A2PD [40] shows a certain modiﬁcation of policy distillation can be inherently robust against state adversaries. Through the use of convex conjugate, [41] has shown that max-entropy RL can be provably robust against uncertainty in reward and environment transitions. Derman et al. [23] further extended regularization to uncertainties in reward and transition dynamics under rectangular and ball constraints. The work most similar to ours is ERNIE [21], which minimize the Lipshitz constant of value function under worst-case perturbations in MARL. However, the method considers all agents as potential adversaries, thus inherits the drawback of M3DDPG, learning policy that can either be pessimistic or insuﬃciently robust."

> _[Section I, Introduction]_

"In real-world applications, however, MARL algorithms often fall short when the actions of cooperative agents deviate from their intended policies due to numerous uncertainties during deployment. In such cases, cooperative agents may exhibit unpredictable behavior or even perform worst-case actions if being hacked by adversaries, [10], [11], [12], [13], [14], [15]. This vulnerability greatly limits the practical applicability of MARL in real-world scenarios, such as robot swarm control [16]. Research on robust MARL against action uncertainties primarily focuses on max-min optimization against worst-case adversaries [10], [11], [17], [18], [19]. This approach can be framed as a zero-sum game [17], [20], where defenders with ﬁxed parameters during deployment aim to maximize performance despite unknown proportions of adversaries employing the worst-case, nonoblivious adversarial policies [12], [14]. However, in multi-agent scenario, each agent can be either perturbed or unperturbed, leading to an exponential increase in the number of potential threat scenarios, making max-min optimization against each threat intractable. To address this complexity, some methods [10], [11], [21] approximate the problem by treating all agents as adversaries. However, since not all agents are perturbed in reality, the learned policy can be overly pessimistic, making agents not cooperate at all. Others attempt to enumerate all threat scenarios [18], [19], [22], but often struggle to explore each threat scenario suﬃciently during training, leaving defenders still vulnerable to worst-case adversaries. Consequently, max-min optimization provides limited defense capabilities in MARL and incurs high computational cost [23]."

> _[Section II-E, Mutual Information Estimation — MARL with MI regularization]_

"Since mutual information (MI) captures agent correlations, many MARL methods use MI regularization to promote collaboration. Existing approaches can be grouped into three categories: 1) social inﬂuence [50] and EITI [51] maximize MI between pairs of agents to enhance mutual inﬂuence; 2) MAVEN [52], SIC [53], and VM3-ac [54] maximize MI between each agent and a shared latent variable to improve coordination; and 3) PMIC [55] maximizes MI between states and joint actions to promote diverse yet predictable behaviors. However, these methods do not account for robustness against action perturbations—higher coordination in such cases may amplify cascading failures when individual agents falter."

### Cited references (resolved from the paper's bibliography)
- **[10]** S. Li, Y. Wu, X. Cui, H. Dong, F. Fang, S. Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[11]** C. Sun, D. K. Kim, J. P. How. *ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* ICRA 2022.
- **[12]** A. Gleave, M. Dennis, C. Wild, N. Kant, S. Levine, S. Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv 2019.
- **[13]** B. Ly, R. Ly. *Cybersecurity in unmanned aerial vehicles (UAVs).* Journal of Cyber Security Technology 2021.
- **[14]** L. C. Dinh, D. Mguni, T. A. Han, J. Wang, Y. Yang. *Online Markov decision processes with non-oblivious strategic adversary.* Autonomous Agents and Multi-Agent Systems 2023.
- **[15]** S. Li et al. *Attacking cooperative multi-agent reinforcement learning by adversarial minority influence.* arXiv 2023.
- **[16]** M. Hüttenrauch, S. Adrian, G. Neumann. *Deep reinforcement learning for swarm systems.* JMLR 2019.
- **[17]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Başar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[18]** E. Nisioti, D. Bloembergen, M. Kaisers. *Robust multi-agent Q-learning in cooperative games with adversaries.* AAAI Workshop on Reinforcement Learning in Games 2021.
- **[19]** S. Li et al. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game.* arXiv 2023.
- **[20]** C. Tessler, Y. Efroni, S. Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[21]** A. Bukharin et al. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms (ERNIE).* NeurIPS 2023.
- **[22]** L. Yuan et al. *Robust multi-agent coordination via evolutionary generation of auxiliary adversarial attackers.* AAAI 2023.
- **[23]** E. Derman, M. Geist, S. Mannor. *Twice regularized MDPs and the equivalence between robustness and regularization.* NeurIPS 2021.
- **[35]** S. Han et al. *What is the solution for state-adversarial multi-agent reinforcement learning?* arXiv 2022.
- **[36]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* TMLR 2023.
- **[37]** E. Kardeş, F. Ordóñez, R. W. Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research 2011.
- **[38]** S. He, Y. Wang, S. Han, S. Zou, F. Miao. *A robust and constrained multi-agent reinforcement learning electric vehicle rebalancing method in AMoD systems.* arXiv 2022.
- **[39]** T. Phan et al. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
- **[40]** X. Qu, A. Gupta, Y.-S. Ong, Z. Sun. *Adversary agnostic robust deep reinforcement learning (A2PD).* IEEE TNNLS 2023.
- **[41]** B. Eysenbach, S. Levine. *Maximum entropy RL (provably) solves some robust RL problems.* arXiv 2021.
- **[50]** N. Jaques et al. *Social influence as intrinsic motivation for multi-agent deep reinforcement learning.* ICML 2018.
- **[51]** T. Wang, J. Wang, Y. Wu, C. Zhang. *Influence-based multi-agent exploration (EITI).* arXiv 2019.
- **[52]** A. Mahajan, T. Rashid, M. Samvelyan, S. Whiteson. *MAVEN: Multi-agent variational exploration.* NeurIPS 2019.
- **[53]** L. Chen et al. *Signal instructed coordination in cooperative multi-agent reinforcement learning (SIC).* ICDAI 2021.
- **[54]** W. Kim, W. Jung, M. Cho, Y. Sung. *A maximum mutual information framework for multi-agent reinforcement learning (VM3-ac).* arXiv 2020.
- **[55]** P. Li et al. *PMIC: Improving multi-agent reinforcement learning with progressive mutual information collaboration.* arXiv 2022.
