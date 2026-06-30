# 5. Distributionally Robust Cooperative Multi-Agent Reinforcement Learning via Robust Value Factorization

## Metadata
- **Title**: Distributionally Robust Cooperative Multi-Agent Reinforcement Learning via Robust Value Factorization
- **Authors**: Chengrui Qu, Christopher Yeh, Kishan Panaganti, Eric Mazumdar, Adam Wierman
- **Affiliation**: California Institute of Technology (Qu, Yeh, Mazumdar, Wierman); Tencent AI Lab (Panaganti)
- **Venue**: ICLR 2026 (Fourteenth International Conference on Learning Representations)
- **Link/arXiv**: arXiv:2602.11437v1

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental uncertainty (sim-to-real gap, model mismatch, system noise); distributionally robust, worst-case over (h,a)-rectangular uncertainty sets (ρ-contamination and TV distance)
- **Method paradigm**: Cooperative Dec-POMDP with CTDE; DrIGM principle; robust value factorization (VDN, QMIX, QTRAN); robust Bellman operators; deep learning (DRQN + mixing networks); practical/empirical + theoretical robustness guarantees
- **Keywords**: DrIGM, IGM, value factorization, VDN, QMIX, QTRAN, CTDE, cooperative MARL, Dec-POMDP, robust Bellman operator, ρ-contamination, TV uncertainty, SustainGym, SMAC

## TL;DR
Introduces Distributionally Robust IGM (DrIGM), a principled extension of the classic IGM principle to settings with environmental uncertainty, enabling robust value-factorization algorithms (Robust-VDN, Robust-QMIX, Robust-QTRAN) for cooperative CTDE MARL with provable robustness guarantees and strong empirical performance under distribution shift.

## Problem & Motivation
Cooperative MARL under CTDE relies on the Individual-Global-Maximum (IGM) principle to align decentralized greedy actions with the team-optimal joint action. However, naively applying single-agent DR-RL individual robust Q-functions to the multi-agent setting breaks IGM: the adversarial model minimizing one agent's value need not minimize the joint value. This misalignment means that robust individual greedy actions can deviate from the robust joint greedy action, preventing correct decentralized execution under uncertainty. The paper provides a counterexample demonstrating this failure and proposes a new principle (DrIGM) with a systematic fix.

## Robustness Setting
- **Threat model / uncertainty set**: (h,a)-rectangular uncertainty set P = ⊗ P_{h,a} around nominal model P^0, where each P_{h,a} ⊂ Δ(H) is a local set for each (history, action) pair. Concretely studied for: (1) ρ-contamination: P_{h,a} = {(1−ρ)P^0_{h,a} + ρν : ν ∈ Δ(H)}; (2) TV: TV(P, P^0_{h,a}) ≤ ρ.
- **Setting**: Cooperative Dec-POMDP with N agents; partial observability; single team reward; CTDE; discounted infinite-horizon; primarily empirical with theoretical robustness guarantees.

## Method
- **DrIGM principle**: Defines robust individual action values as Q^rob_i(h_i, a_i) := Q^{P^worst(h,ā)}_i(h_i, a_i), where P^worst is the global worst-case model and ā is the robust joint greedy action. By anchoring all agents to the same global adversarial model, individual greedy actions align with the robust joint greedy action.
- **Theorem 1**: If VDN/QMIX/QTRAN IGM holds for all P ∈ P, then Q^rob_i defined via eq. (6) satisfies DrIGM.
- **Theorem 2**: DrIGM holds for VDN, QMIX, and QTRAN conditions when individual Q-functions satisfy those respective structural constraints.
- **Theorem 3**: Robustness guarantee: if the test environment P^test ∈ P, then Q^P_tot(h,a) ≤ Q^{P^test}_tot(h,a) for all (h,a), i.e., the robust value lower-bounds the true value.
- **Robust Bellman operators**: Derived for ρ-contamination (eq. 8: r + γ(1−ρ)E_{P^0}[Q(h', ā')]) and TV uncertainty (eq. 10: dual form with Lagrange variable η).
- **Algorithm**: DRQN-style individual value networks + factorization mixing network, trained with robust TD loss using robust Bellman targets. Target networks for stability, ε-greedy exploration, replay buffer.
- Six total algorithm variants: {VDN, QMIX, QTRAN} × {ρ-contamination, TV}.

## Theoretical Contributions
- **Theorem 1**: DrIGM is satisfied when robust individual Q-values are defined via the global worst-case model at the robust joint action.
- **Theorem 2**: Standard VDN/QMIX/QTRAN factorization structures are compatible with DrIGM.
- **Theorem 3**: Provable robustness guarantee: within the prescribed uncertainty set, the robust value lower-bounds the true value; out-of-distribution reward cannot fall below the robust Q-value.
- Counterexample (Example 1, Appendix B): Demonstrates that naive per-agent robustification (infimum over P independently per agent) violates DrIGM.

## Experiments
- **SustainGym (HVAC)**: Multi-agent building HVAC control; evaluated under climatic shifts (6 environment configurations) and seasonal shifts; our robust methods (TV and ρ-contamination) outperform non-robust baselines and GroupDR in out-of-distribution performance; 10-40% higher average reward under combined climatic and seasonal shifts.
- **SMAC (StarCraft II, 3s vs 5z)**: Observation noise perturbation; robust VDN and QMIX with ρ-contamination significantly improve out-of-distribution win rate for small ρ. Performance follows an inverted-U shape in ρ, consistent with the theory.
- **Baselines**: Non-robust VDN/QMIX/QTRAN; GroupDR (Liu et al., 2025), extended to QMIX/QTRAN.

## Key Results
- DrIGM-based algorithms consistently outperform non-robust baselines under distribution shift across all tested environments and factorization methods.
- Robust training in cooperative MARL does not necessarily reduce in-distribution performance (unlike single-agent robust RL), and can even improve it by reducing errors from partial observability.
- TV uncertainty set generally performs at least as well as ρ-contamination, especially in seasonal and combined shift scenarios.
- GroupDR baseline underperforms DrIGM methods because it relies on worst-case rewards only from training configurations.

## Limitations & Future Work
- DrIGM currently assumes a global uncertainty set; extension to agent-wise uncertainty sets (e.g., fictitious per-agent sets) is open.
- Decentralized training (beyond CTDE) under robustness constraints remains unexplored.
- The theory covers discounted Dec-POMDPs; extension to infinite-horizon average-reward settings is open.
- Computational cost of the dual variable optimization for TV uncertainty (minimizing L_dual per step) may scale poorly with large action spaces.

## Relevance to Survey
Bridges cooperative MARL (value factorization, CTDE) and distributionally robust RL; the only work in the corpus explicitly addressing cooperative Dec-POMDPs under model uncertainty with provable DrIGM guarantees; complements theoretical RMG papers (Papers 2–4) by addressing partial observability and team-reward settings; empirically demonstrates real-world robustness on energy and game benchmarks.

## Related Work (verbatim excerpts from the paper)

> _[Introduction — "Brief discussion of related work." paragraph, lines 96–107]_

"Robustness in cooperative MARL has been studied along several axes: adversarial or heterogeneous teammates (Li et al., 2019; Kannan et al., 2023; Li et al., 2024), state/observation and communication perturbations (Guo et al., 2024; Yu et al., 2024), risk-sensitive (tail-aware) objectives under a fixed model (Shen et al., 2023), and explicit model uncertainty (Kwak et al., 2010; Zhang et al., 2020b; 2021; Liu et al., 2025). Most of the works on model uncertainty adopt a distributionally robust optimization viewpoint and targets Nash solutions with provable algorithms, often assuming full observability or individual rewards (Zhang et al., 2020a; Kardeş et al., 2011; Ma et al., 2023; Blanchet et al., 2023; Shi et al., 2024; Liu et al., 2025). In this work, we focus on the cooperative CTDE regime with partial observability and a single team reward, providing a systematic framework for robustness to model uncertainty without real-time communication."

> _[Appendix A, Related Work — three subsections]_

**Single-agent Distributionally Robust RL (DR-RL).**

"The single-agent setting is typically formalized as a robust Markov decision process (MDP). A substantial literature studies finite-sample guarantees for distributionally robust RL, exploring a variety of ambiguity-set designs (Iyengar, 2005; Xu & Mannor, 2012; Wolff et al., 2012; Kaufman & Schaefer, 2013; Ho et al., 2018; Smirnova et al., 2019; Ho et al., 2021; Goyal & Grand-Clement, 2022; Derman & Mannor, 2020; Tamar et al., 2014; Panaganti & Kalathil, 2021a; Roy et al., 2017; Derman et al., 2018; Mankowitz et al., 2019). Most relevant to our work are tabular robust MDPs with (s, a)-rectangular uncertainty sets defined by total-variation balls (Yang et al., 2022; Panaganti & Kalathil, 2021b; Xu et al., 2023; Dong et al., 2022; Liu & Xu, 2024; Panaganti et al., 2022) or ρ-contamination models (Wang & Zou, 2022; Zhang et al., 2024), for which minimax dynamic programming and learning algorithms admit provable performance bounds."

**Value factorization methods for cooperative MARL.**

"Value factorization is the standard mechanism for scalable cooperative MARL under CTDE. Early work adopts simple additivity (VDN (Sunehag et al., 2017)), while QMIX (Rashid et al., 2020) learn a state-conditioned monotone combiner to enlarge the function class without violating the IGM requirement. QTRAN (Son et al., 2019) further relax the monotonicity assumption with consistency constraints. Other approaches include attention-based mixers (e.g., QAtten (Yang et al., 2020), REFIL (Iqbal et al., 2021)), dueling-style decompositions (QPlex (Wang et al., 2021)) and residual designs (ResQ (Shen et al., 2022)). Building on this body of work, we develop robust value-factorization algorithms with provable robustness guarantees under model uncertainty, enabling robust decentralized execution in partially observable cooperative settings."

**Robustness in MARL.**

"In general MARL, robustness is typically studied within Markov games, where uncertainty can be modeled in different components, such as the state space (Han et al., 2022; He et al., 2023; Zhou & Liu, 2023; Zhang et al., 2023), other agents (Li et al., 2019; Kannan et al., 2023), and environmental dynamics (Zhang et al., 2020a; Liu et al., 2025). We refer readers to Vial et al. (2022) for an overview. This work considers robustness to model uncertainty, primarily studied via distributionally robust optimization (DRO) (Rahimian & Mehrotra, 2019; Gao, 2020; Bertsimas et al., 2018; Duchi & Namkoong, 2018; Blanchet & Murthy, 2019; Fonseca & Junca, 2023; Qu et al., 2025; Mohajerin Esfahani & Kuhn, 2018; Noyan et al., 2022), where most prior efforts target Nash equilibria and provide provable (actor–critic / Q-learning) algorithms (Zhang et al., 2020a; Kardeş et al., 2011; Ma et al., 2023; Blanchet et al., 2023; Shi et al., 2024; Liu et al., 2025), often under full observability or individually rewarded settings. We complement this line by addressing the cooperative, partially observable CTDE regime, where agents receive a single joint reward and act only local observations.

In cooperative MARL, robustness has been modeled along several complementary axes, including adversarial (Byzantine) teammates (Li et al., 2024), state/observation disturbances (Guo et al., 2024), communication errors (Yu et al., 2024), risk-sensitive objectives that guard against tail events under a fixed model (Shen et al., 2023), and explicit model uncertainty Kwak et al. (2010); Zhang et al. (2020b). Focusing on the last category, Kwak et al. (2010) address model uncertainty with sparse, execution-time communication, whereas Zhang et al. (2020b) study settings in which each agent observes the full state and receives individual reward. Similarly, Bukharin et al. (2023) also considers settings where each agent receives individual reward, and they achieve robustness by controlling the Lipschitz constant of each agent's policy. In contrast, our work targets robustness to model uncertainty in the cooperative CTDE setting, complementing prior approaches by providing a systematic framework that does not require real-time communication and operates under partial observability with a single team reward."

### Cited references (resolved from the paper's bibliography)
- **Li et al. (2019)** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **Kannan et al. (2023)** Kannan, Venkatesh, Min. *Smart-LLM: Smart multi-agent robot task planning using large language models.* arXiv:2309.10062, 2023.
- **Li et al. (2024)** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game.* ICLR 2024.
- **Guo et al. (2024)** Guo, Liu, Zhou, Wang, Wang. *Enhancing the robustness of QMIX against state-adversarial attacks.* Neurocomputing, 2024.
- **Yu et al. (2024)** Yu, Qiu, Yao, Shen, Zhang, Wang. *Robust communicative multi-agent reinforcement learning with active defense.* AAAI 2024.
- **Shen et al. (2023)** Shen, Ma, Li, Liu, Fu, Mei, Liu, Wang. *RiskQ: risk-sensitive multi-agent reinforcement learning value factorization.* NeurIPS 2023.
- **Kwak et al. (2010)** Kwak, Yang, Yin, Taylor, Tambe. *Teamwork and coordination under model uncertainty in Dec-POMDPs.* AAAI Workshop 2010.
- **Zhang et al. (2020b)** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **Zhang et al. (2021)** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **Liu et al. (2025)** Liu, Iloglu, Caldara, Durham, Zavlanos. *Distributionally robust multi-agent reinforcement learning for dynamic chute mapping.* ICML 2025.
- **Zhang et al. (2020a)** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **Kardeş et al. (2011)** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 2011.
- **Ma et al. (2023)** Ma, Chen, Zou, Zhou. *Decentralized robust V-learning for solving Markov games with model uncertainty.* JMLR, 2023.
- **Blanchet et al. (2023)** Blanchet, Lu, Zhang, Zhong. *Double pessimism is provably efficient for distributionally robust offline reinforcement learning.* NeurIPS 2024.
- **Shi et al. (2024)** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* arXiv:2404.18909, 2024.
- **Iyengar (2005)** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **Xu & Mannor (2012)** Xu, Mannor. *Distributionally robust Markov decision processes.* Mathematics of Operations Research, 2012.
- **Yang et al. (2022)** Yang, Zhang, Zhang. *Toward theoretical understandings of robust Markov decision processes: Sample complexity and asymptotics.* Annals of Statistics, 2022.
- **Panaganti & Kalathil (2021b)** Panaganti, Kalathil. *Sample complexity of model-based robust reinforcement learning.* CDC 2021.
- **Xu et al. (2023)** Xu, Panaganti, Kalathil. *Improved sample complexity bounds for distributionally robust reinforcement learning.* arXiv:2303.02783, 2023.
- **Dong et al. (2022)** Dong, Li, Wang, Zhang. *Online policy optimization for robust MDP.* arXiv:2209.13841, 2022.
- **Liu & Xu (2024)** Liu, Xu. *Distributionally robust off-dynamics reinforcement learning: Provable efficiency with linear function approximation.* arXiv:2402.15399, 2024.
- **Panaganti et al. (2022)** Panaganti, Xu, Kalathil, Ghavamzadeh. *Robust reinforcement learning using offline data.* NeurIPS 2022.
- **Wang & Zou (2022)** Wang, Zou. *Policy gradient method for robust reinforcement learning.* ICML 2022.
- **Zhang et al. (2024)** Zhang, Panaganti, Shi, Sui, Wierman, Yue. *Distributionally robust constrained reinforcement learning under strong duality.* arXiv:2406.15788, 2024.
- **Sunehag et al. (2017)** Sunehag et al. *Value-decomposition networks for cooperative multi-agent learning.* arXiv:1706.05296, 2017.
- **Rashid et al. (2020)** Rashid, Samvelyan, De Witt, Farquhar, Foerster, Whiteson. *Monotonic value function factorisation for deep multi-agent reinforcement learning.* JMLR, 2020.
- **Son et al. (2019)** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to factorize with transformation for cooperative multi-agent RL.* ICML 2019.
- **Yang et al. (2020)** Yang, Hao, Liao, Shao, Chen, Liu, Tang. *QATTEN: A general framework for cooperative multiagent reinforcement learning.* arXiv:2002.03939, 2020.
- **Iqbal et al. (2021)** Iqbal, Schröder de Witt, Peng, Boehmer, Whiteson, Sha. *Randomized entity-wise factorization for multi-agent reinforcement learning.* ICML 2021.
- **Wang et al. (2021)** Wang, Ren, Liu, Yu, Zhang. *QPLEX: Duplex dueling multi-agent Q-learning.* ICLR 2021.
- **Shen et al. (2022)** Shen, Qiu, Liu, Liu, Fu, Liu, Wang. *ResQ: A residual Q function-based approach for multi-agent reinforcement learning value factorization.* NeurIPS 2022.
- **Han et al. (2022)** Han, Su, He, Han, Yang, Miao. *What is the solution for state-adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **He et al. (2023)** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* TMLR, 2023.
- **Zhou & Liu (2023)** Zhou, Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv:2306.06136, 2023.
- **Zhang et al. (2023)** Zhang, Sun, Huang, Miao. *Safe and robust multi-agent reinforcement learning for connected autonomous vehicles under state perturbations.* arXiv:2309.11057, 2023.
- **Vial et al. (2022)** Vial, Shakkottai, Srikant. *Robust multi-agent bandits over undirected graphs.* ACM MACS, 2022.
- **Bukharin et al. (2023)** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* NeurIPS 2023.
