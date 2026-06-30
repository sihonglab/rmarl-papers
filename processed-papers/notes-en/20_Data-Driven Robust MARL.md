# 20. Data-Driven Robust Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Data-Driven Robust Multi-Agent Reinforcement Learning
- **Authors**: Yudan Wang, Yue Wang, Yi Zhou, Alvaro Velasquez, Shaofeng Zou
- **Affiliation**: Department of Electrical Engineering, University at Buffalo; Department of Electrical and Computer Engineering, University of Utah; Information Directorate, Air Force Research Laboratory
- **Venue**: IEEE International Workshop on Machine Learning for Signal Processing (MLSP) 2022
- **Link/arXiv**: DOI: 10.1109/MLSP55214.2022.9943500

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty in the Markov transition kernel (distributional uncertainty; sim-to-real / train-test model deviation; random perturbations, adversarial attacks, outliers in sampling)
- **Method paradigm**: Robust MDP, distributionally robust RL, robust Q-learning, R-contamination uncertainty set, decentralized/distributed optimization (average consensus), minimax worst-case optimization, finite-time / sample-complexity analysis
- **Keywords**: Distributionally robust, model-free, sample complexity, finite-time analysis, robust MDP, decentralized MARL

## TL;DR
The paper proposes MARQ, an online, model-free, fully decentralized multi-agent robust Q-learning algorithm for the collaborative setting under transition-kernel uncertainty (R-contamination set), proving almost-sure convergence to the minimax robust policy and characterizing its sample complexity at no extra computational/memory cost over vanilla multi-agent Q-learning.

## Problem & Motivation
Multi-agent systems are typically distributed, communicate over wireless channels, and are therefore vulnerable to external perturbations and adversarial attacks that cause model deviation and significant performance degradation. Existing MARL results usually assume the policy is deployed in the same environment as the one where training samples are taken, so they may not perform well when there is model deviation between training and test environments. Prior robust MDP work is mostly single-agent and either requires full knowledge of the uncertainty set, imposes stringent discount-factor conditions, or lacks provable guarantees; the only related MARL work studied reward uncertainty but ignored transition-kernel uncertainty. This paper addresses robust collaborative MARL where the transition kernel lies in an uncertainty set and the objective is worst-case performance over that set.

## Robustness Setting
- **Threat model / uncertainty set**: The transition kernel P is not fixed but lies in an (s, a)-rectangular uncertainty set P, with the time-varying choice of P_t referred to as "nature's policy" τ. Specifically, an R-contamination uncertainty set is used: P_{s,a} := {(1−R)·p̂_{s,a} + R·q | q ∈ Δ(S)}, where p̂_{s,a} is the (unknown) centroid from which samples can be obtained sequentially. The R-contamination set models state transitions being arbitrarily perturbed with small probability R (suitable for random perturbations, adversarial attacks, outliers) and connects to TV / KL-divergence / Hellinger uncertainty sets via inequalities (e.g., Pinsker's inequality).
- **Setting**: Cooperative / collaborative (maximize average accumulated reward over all agents); fully decentralized (no fusion center, local-only reward observation, neighbor-only communication over a network graph); online / model-free (single sample trajectory).

## Method
- Models a decentralized multi-agent MDP ⟨S, A, P, N, G, r, γ⟩ over a network graph G; state and joint action are fully observable to each agent, but reward r^(i) is only locally observable. Defines the robust value/Q functions as the worst case over nature's policy τ.
- Uses the strong-duality / robust Bellman recursion (Theorem 1, from robust dynamic programming): V*(s) = max_a {r̄(s,a) + γ·σ_{P_{s,a}}(V*)}, with support function σ. Under the R-contamination set, the support function reduces to (1−R)·E_{s'∼p̂}[V*(s')] + R·min_{s'} V*(s'), which avoids any explicit inner optimization over the uncertainty set.
- Designs Algorithm 1 (MARQ): each agent i keeps a local copy of its Q-table; at each step it (1) updates the Q-table via a stochastic version of the robust Bellman equation using only local reward (the update mixes the local reward, the γR·min_s V term, and γ(1−R)·V at the observed next state), then (2) performs "average consensus" by collecting neighbors' Q-table estimates and computing a weighted average via the doubly stochastic matrix G.
- The update is online, incremental, and has the same computational/memory complexity (within a constant factor) as vanilla Q-learning; greedy actions w.r.t. the local Q-estimate yield each agent's policy. The approach can be combined with deep Q-learning and double Q-learning for large/continuous problems.

## Theoretical Contributions
- **Asymptotic convergence (Theorem 2)**: Under Assumptions 1–3 (doubly stochastic weight matrix with spectral gap, Robbins–Monro learning-rate conditions, bounded reward), each agent's estimate Q^(i)_T → Q* almost surely as T → ∞, via a novel generalization of stochastic-approximation convergence analysis to the decentralized setting.
- **Finite-time error bound and sample complexity (Theorem 3)**: Under Assumptions 1–4 (adding uniform ergodicity of the behavior-policy Markov chain), with probability ≥ 1−6δ, ‖Q_T − Q*‖_∞ < 5ε for the stated T, learning rate, and ε range. The overall sample size is O( 1/((1−γ)^5 ε^2) + t_mix/(1−γ) + log(√N)/(ε(1−γ)) ), which matches the single-agent / centralized tabular settings within a constant factor (for a large range of N); as N grows, more samples are needed to drive down the average-consensus error.
- Provides a proof sketch decomposing the error into a one-step average-consensus error (part I) and a Q-learning error (part II) via a D-norm, combining distributed optimization with robust RL analysis.

## Experiments
- **Environment/Benchmark**: A synthetic multi-agent MDP with N = 5 agents and |S| = 24 states; per-agent action space A^(i) = {0,1} (joint action space |A| = 32); a "23-point game" over states S = {0,...,23} with an action-mapping matrix n(a) and a designed reward structure (e.g., reaching state 23 gives agents 2,3,4 rewards 1,4,5; a step reward of −0.2). Policies are evaluated in a perturbed environment that, with probability p, transits to the worst-case state arg min_s V*(s).
- **Baselines**: Vanilla (non-robust) decentralized multi-agent Q-learning (i.e., Algorithm 1 with R = 0).
- **Evaluation metrics**: Average reward over 100 test episodes per evaluation step (evaluated every 40 steps), with 10th/90th-percentile envelopes, under perturbation settings (R=0.2, p=0.2), (R=0.3, p=0.2), (R=0.3, p=0.3).

## Key Results
- MARQ achieves higher reward than the vanilla algorithm in the perturbed environment, demonstrating robustness to distributional uncertainty and adversarial perturbations.
- When the perturbation parameters R, p are small (small model mismatch), MARQ performs similarly to the non-robust algorithm; when the parameters are larger, MARQ performs much better.
- Empirically confirms the algorithm's convergence and robustness consistent with the theoretical guarantees.

## Limitations & Future Work
- Experiments are on a small synthetic tabular MDP (N=5, |S|=24); no large-scale or real-world / deep-network evaluation.
- Restricted to the R-contamination uncertainty set; other uncertainty sets (KL-divergence, Wasserstein distance) are left for future work.
- Future: extend the idea to make SARSA and other RL algorithms robust; combine with deep Q-learning and double Q-learning for large/continuous state/action spaces; generalize the robust policy gradient approach to the decentralized multi-agent setting.

## Relevance to Survey
A core data-driven / distributionally robust MARL contribution: it extends single-agent online robust Q-learning under the R-contamination model to a fully decentralized, networked cooperative MARL setting with provable convergence and sample complexity. It sits on the "model/transition uncertainty" main line and the "robust MDP + decentralized/distributed optimization" method line, complementing reward-uncertainty robust MARL (Zhang et al., NeurIPS 2020 [16]) by handling transition-kernel uncertainty, and connecting robust RL theory (Nilim & El Ghaoui, Iyengar) with distributed average-consensus MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 1, Introduction]_

"Multi-agent reinforcement learning (MARL) [1] finds a wide range of applications in modern artificial intelligence applications, where multiple autonomous agents interact with a common stochastic environment [2, 3, 4]. Multi-agent systems are usually distributed, and agents communicate through wireless channel, and therefore, they are vulnerable to external perturbations and adversarial attacks, which may result in a model deviation, and further lead to a significant performance degradation. However, existing results typically assume that the policy will be deployed in the same environment as the one where training samples are taken [5], and thus may not perform well when there is model deviation between the training and test environments. In this paper, we develop a robust MARL approach, where the Markov decision process (MDP) model is not fixed but lies in an uncertainty set, and the goal is to optimize the worst-case performance over the uncertainty set."

> _[Section 1, Introduction — prior work on robust RL and MARL]_

"The framework of robust MDP was developed in [6, 7, 8] for the single-agent setting. A robust dynamic programming approach was developed, and was shown to be minimax optimal. This approach, however, requires full knowledge of the uncertainty set, and does not scale well to large or continuous problems. Following this framework, model-free approaches with function approximation are developed, e.g., [9, 10], but the convergence results require a stringent condition on the discount factor. There are also heuristic approaches on robust RL, e.g., [11, 12, 13, 14, 15], but they lack in provable performance guarantee. More importantly, the above studies are mostly focused on the single-agent case. Recently, the work [16] studied reward uncertainty in MARL, but did not take into consideration the Markov transition kernel uncertainty. There are also studies on MARL, e.g., [17, 18, 19, 20, 1], but they are limited to the non-robust case."

> _[Section 1, Introduction — positioning of this work]_

"In this paper, we investigate the problem of robust MARL in the collaborative setting with uncertainty in the Markov transition kernel, where the agents aim to maximize the accumulative average reward over all the agents under the worst-case Markov transition kernel in the uncertainty set. We generalize the single-agent robust Q-learning algorithm in [21] to the decentralized multi-agent setting, where there is no fusion center, each agent's reward information is only locally observable, and each agent may only communicate with its neighbors in the network."

### Cited references (resolved from the paper's bibliography)
- **[1]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, 2021.
- **[2]** Shalev-Shwartz, Shammah, Shashua. *Safe, multi-agent, reinforcement learning for autonomous driving.* arXiv:1610.03295, 2016.
- **[3]** Leibo, Zambaldi, Lanctot, Marecki, Graepel. *Multi-agent reinforcement learning in sequential social dilemmas.* AAMAS 2017.
- **[4]** Wang, Wan, Zhang, Li, Zhang. *Towards smart factory for industry 4.0: a self-organized multi-agent system with big data based feedback and coordination.* Computer Networks, 2016.
- **[5]** Sutton, Barto. *Reinforcement Learning: An Introduction.* MIT Press, 2018.
- **[6]** Bagnell, Ng, Schneider. *Solving uncertain Markov decision processes.* 2001.
- **[7]** Nilim, El Ghaoui. *Robustness in Markov decision problems with uncertain transition matrices.* NIPS 2004.
- **[8]** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research, 2005.
- **[9]** Roy, Xu, Pokutta. *Reinforcement learning under model mismatch.* NIPS 2017.
- **[10]** Panaganti Badrinath, Kalathil. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML 2021.
- **[11]** Vinitsky, Du, Parvate, Jang, Abbeel, Bayen. *Robust reinforcement learning using adversarial populations.* arXiv:2008.01825, 2020.
- **[12]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[13]** Hou, Pang, Hong, Lan, Ma, Yin. *Robust reinforcement learning with Wasserstein constraint.* arXiv:2006.00945, 2020.
- **[14]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* IJCAI 2017.
- **[15]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* AAMAS 2018.
- **[16]** Zhang, Sun, Tao, Genc, Mallya, Başar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[17]** Zhang, Yang, Liu, Zhang, Başar. *Fully decentralized multi-agent reinforcement learning with networked agents.* ICML 2018.
- **[18]** Liu, Wang, Jin. *Learning Markov games with adversarial opponents: Efficient algorithms and fundamental limits.* arXiv:2203.06803, 2022.
- **[19]** Chen, Zhou, Chen, Zou. *Sample and communication-efficient decentralized actor-critic algorithms with finite-time analysis.* arXiv:2109.03699, 2021.
- **[20]** Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994, Elsevier.
- **[21]** Wang, Zou. *Online robust reinforcement learning with model uncertainty.* NeurIPS 2021.
