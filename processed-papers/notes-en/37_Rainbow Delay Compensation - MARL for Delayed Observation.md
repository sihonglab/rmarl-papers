# 37. Rainbow Delay Compensation: A Multi-Agent Reinforcement Learning Framework for Mitigating Delayed Observation

## Metadata
- **Title**: Rainbow Delay Compensation: A Multi-Agent Reinforcement Learning Framework for Mitigating Delayed Observation
- **Authors**: Songchen Fu, Siang Chen, Shaojing Zhao, Letian Bai, Hong Liang, Ta Li, Yonghong Yan
- **Affiliation**: Laboratory of Speech and Intelligent Information Processing, Institute of Acoustics, CAS; University of Chinese Academy of Sciences; Department of Electronic Engineering, Tsinghua University
- **Venue**: NeurIPS 2025
- **Link/arXiv**: arXiv:2505.03586v4 [cs.MA]; code at https://github.com/linkjoker1006/RDC-pymarl

## Taxonomy
- **Robustness / perturbation type targeted**: Observation delay / delayed observation (stochastic individual delays affecting different observation components per agent); non-ideal/imperfect observation. Distinguished by the paper from robust MARL's adversarial/system-error observation inaccuracies.
- **Method paradigm**: Delay-free observation reconstruction (compensator), augmented-state POMDP modeling, delay-reconciled critic (CTDE), curriculum learning, knowledge distillation, value decomposition (VDN/QMIX)
- **Keywords**: observation delay, DSID-POMDP, MARL, delay compensation, curriculum learning, knowledge distillation

## TL;DR
The paper formalizes multi-agent delayed observation as the decentralized stochastic individual delay POMDP (DSID-POMDP) and proposes Rainbow Delay Compensation (RDC), a training framework that reconstructs delay-free observations via a compensator (Echo/Flash modes), combined with a delay-reconciled critic, curriculum learning, and knowledge distillation, achieving near delay-free performance under fixed and unfixed delays on MPE and SMAC.

## Problem & Motivation
In real-world multi-agent systems (MASs), observation delays are ubiquitous, preventing agents from acting on the environment's true state. An agent's local observation comprises multiple components (self-state, other agents' states, environmental states) that experience varying delays, which is challenging for MARL. Prior work on delays is rooted in single-agent control theory and RL (augmented states, model-based estimation) and typically handles only fixed/deterministic delays; multi-agent extensions remain superficial and overlook the asynchronicity and stochasticity of delayed observations. Unfixed delays violate the Markov assumption and exacerbate non-stationarity and credit assignment, making the unfixed-delayed-observation problem in MARL an urgent and unresolved gap.

## Robustness Setting
- **Threat model / uncertainty set**: Each agent's observation is decomposed into components from "entities" (other agents, environment), each with an individual delay value drawn from a user-defined probability distribution Dij (e.g., uniform, binomial, Gaussian, Poisson; possibly distance-correlated). Delay values satisfy a temporal-consistency constraint (dij_t < min(dij_{t-1}+1, T); information at step t cannot be older than at step t-1). The framework assumes no prior knowledge of the delay distribution. Modes: no delay, fixed, partially fixed, unfixed (random delay values and which contents are delayed).
- **Setting**: cooperative and competitive/mixed (MPE simple-tag is competitive but converted to cooperative by fixing the prey policy; simple-spread/reference cooperative; SMAC cooperative-vs-enemy); centralized-training-decentralized-execution (CTDE); online (compensator trained synchronously with RL).

## Method
- **DSID-POMDP**: extends Dec-POMDP with an augmented state x = {s(−T),…,s(−1),s} containing the delay-free state and previous T states, individual delay distributions Dij, and a factorized delayed observation function; proves the transition reduces to POMDP transition when historical-sequence transitions are fixed.
- **Delay compensator** (core component): reconstructs delay-free observation from history. Two modes — **Flash** (single-pass, fast, low resource) and **Echo** (autoregressive, T-step, adapts to variable/unknown delays). Implemented with GRU and Transformer networks; uses a dual-head residual design with cross-entropy loss for discrete (classification) features and MSE for continuous (regression) features; inputs include observation history and past-T action sequences; trained online alongside RL.
- **Delay-reconciled critic**: feeds the critic with delay-free global states during centralized training (critic not needed at inference), integrating with CTDE to mitigate delay impact.
- **Curriculum learning actor**: initially provides the actor delay-free (ground-truth) observations and linearly anneals the probability of using them until the actor relies entirely on compensated observations; important for complex tasks (SMAC), not strictly needed for simpler ones (MPE).
- **Knowledge distillation**: a teacher trained under low-delay conditions guides the student's hidden representations and output decisions (loss combines action CE, Q-value MSE, and critic-parameter MSE), accelerating convergence; distillation is not applied to the compensator.
- Integrates two value-decomposition algorithms, VDN and QMIX, as baselines (code-level optimized FT-VDN/FT-QMIX in experiments).

## Theoretical Contributions
- Defines the DSID-POMDP as a universal mathematical model for MASs with delayed observation (Definition 1), extending Dec-POMDP.
- Provides proofs (Appendix A) of the correctness of the DSID-POMDP state transition function and observation function under the assumption that observations from different entities are mutually independent.
- Notes the delay equivalence theorem (from single-agent work) cannot hold in MASs due to mutually independent action delays; otherwise the contributions are mostly empirical/algorithmic.

## Experiments
- **Environment/Benchmark**: MPE (simple-tag/TAG, simple-spread/SPREAD, simple-reference/REFERENCE) and SMAC (3s_vs_5z, 5m_vs_6m, 6h_vs_8z), with delay filters simulating none/fixed/partially-fixed/unfixed delays; evaluated under in-distribution and half-out-of-distribution delay ranges and different delay distributions (uniform, binomial, Gaussian, Poisson).
- **Baselines**: Oracle (baseline algorithm in delay-free environment, ideal upper bound), Base (FT-QMIX/FT-VDN under delay), and ablation variants combining DR (delay-reconciled critic), H (history input), C (curriculum learning actor), KD (knowledge distillation); compensator modes Echo and Flash with GRU/Transformer networks.
- **Evaluation metrics**: episode reward (MPE; also reported for SMAC) and win rate (SMAC, the more critical metric); compensator inference time; observation/compensation loss.

## Key Results
- Baseline MARL methods suffer severe performance degradation under fixed and unfixed delays (e.g., win rates approach zero on 5m_vs_6m and 6h_vs_8z); curriculum learning alone or a delay-reconciled critic alone cannot satisfactorily counteract delays in complex scenarios.
- RDC-enhanced models maintain superior, robust performance across all scenarios and can match or slightly exceed the delay-free Oracle in some settings (attributed to extra teacher-model training steps within the same horizon, validated by an additional-10M-step experiment).
- RDC generalizes to out-of-distribution delay ranges and to delay distributions unseen in training (binomial/normal/Poisson), since compensation needs no prior knowledge of the delay distribution.
- Echo (autoregressive) generalizes better than Flash at large/OOD delays; Flash is much faster (≈0.004 s vs ≈0.02 s inference in TAG at delay 6) and benefits more from history inputs. RDC remains compatible with non-actor-critic methods (e.g., FT-VDN); Transformer compensators generally outperform GRU.

## Limitations & Future Work
- A crucial assumption is that each entity exposes only its own state, giving independent observation components; this fails in environments with information relaying/hopping (multi-hop communication) or single-channel interference, and the authors argue extending DSID-POMDP to such cases would not be optimal.
- Both Echo and Flash show poor generalizability on SMAC, with win rates declining rapidly as delay grows; the compensator only processes the agent's own perspective and ignores other agents' influence on the environment.
- Resource overhead grows with the number of agents/entities (increased observation dimensionality), a common MARL challenge; mitigated by parameter sharing under CTDE.
- Future work: design more effective compensator architectures and knowledge-distillation techniques, and develop theoretical frameworks with weaker assumptions.

## Relevance to Survey
This paper addresses robustness to non-ideal observations from the angle of stochastic observation delays, an under-explored axis adjacent to the survey's "state/observation perturbation" and "communication robustness" themes. The authors explicitly contrast their delay-induced observation lag with robust MARL (citing robust MARL with state uncertainty), which targets observation inaccuracies from system errors or adversarial attacks. It connects the delayed-observation / asynchronous-communication line (DAMARL, DACom/TimeNet, reward-delay V-learning) to value-decomposition MARL and CTDE, and provides a reusable training framework (compensation + delay-reconciled critic + curriculum + distillation) relevant to building delay/communication-robust multi-agent systems.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Works]_

"Recent studies have explored Deep Reinforcement Learning (DRL) approaches to address delay issues in single-agent systems. Walsh et al. [32] introduced the constant delay Markov decision process (CDMDP), which extends action sequences to incorporate fixed delays in observation and reward. However, the resulting state space expansion suffers from exponential growth, limiting the feasibility of pure state-based solutions. To overcome this, they proposed Model-Based Simulation (MBS) for discrete environments and Model Parameter Approximation (MPA) for continuous environments, pioneering model-based methods for delay-free state estimation. Firoiu et al. [9] employed environment prediction models to reduce performance degradation from fixed action delays in gaming scenarios. Bouteiller et al. [4] developed a partial trajectory resampling method to resolve credit assignment challenges in stochastic delay environments. Liotet et al. [20] implemented imitation learning to align delayed agents with expert action distributions, but only for fixed delays. Wang et al. [34] combined state augmentation and state prediction with delay-reconciled training for separate actor-critic optimization, demonstrating significant improvements in stochastic delay scenarios."

"Significant progress has also been made in addressing the challenges of delay in MARL. Chen et al. [6] developed the Delay-Aware Multi-Agent Reinforcement Learning (DAMARL) framework, which mitigates fixed observation delays through centralized training with auxiliary information. Subsequent work by Yuan et al. [36] introduced TimeNet to dynamically optimize agents' waiting time for delayed communications, thereby enhancing collaborative efficiency. For reward delay scenarios, Zhang et al. [39] proposed Delay-Adaptive Multi-Agent V-Learning (DAMAVL) with proven convergence under finite and infinite delay conditions. Practical applications have shown promise, as demonstrated by Liu et al. [21]'s successful implementation of DAMARL in cooperative adaptive cruise control (CACC) systems. While Wang et al. [33] advanced the field by predicting action effects through state prediction. Still, current approaches remain limited to fixed delay scenarios and typically overlook the asynchronicity of delayed observations. It is worth noting that research on robust MARL [15] also aims to address the challenges of non-ideal observations. Unlike the observation lag caused by delays, this line of work focuses more on inaccuracies in observations resulting from system errors or adversarial attacks."

> _[Introduction — prior-work background paragraph]_

"Early studies on system delay problems were primarily rooted in control theory [1, 23], where solutions relied heavily on fixed transition models—an assumption often violated in complex MASs [25]. The introduction of augmented state spaces [2, 32] marked a pivotal shift, enabling reinforcement learning methods to handle deterministic delays through model-based state estimation [9, 7]. While these approaches advanced single-agent systems, their extension to multi-agent settings remained superficial, typically limited to fixed delay scenarios [7, 33, 21]. Recent progress in delayed-observation Markov decision processes (DOMDPs) [34] formalized stochastic delay modeling, yet existing work concentrates overwhelmingly on single-agent domains. Multi-agent solutions [36, 35] established theoretical foundations and algorithmic innovations at the levels of communication and feedback. Yet, a critical gap remains: the fundamental challenge of stochastic partial observability in MASs remains unresolved. This oversight is particularly significant given the inherent asynchrony and network-induced uncertainties in real-world multi-agent applications."

### Cited references (resolved from the paper's bibliography)
- **[1]** Z. Artstein. *Linear systems with delayed controls: A reduction.* IEEE Transactions on Automatic Control, 1982.
- **[2]** J. L. Bander, C. C. White III. *Markov decision processes with noise-corrupted and delayed state observations.* Journal of the Operational Research Society, 1999.
- **[4]** Y. Bouteiller, S. Ramstedt, G. Beltrame, C. Pal, J. Binas. *Reinforcement learning with random delays.* ICLR 2020.
- **[6]** B. Chen, M. Xu, Z. Liu, L. Li, D. Zhao. *Delay-aware multi-agent reinforcement learning for cooperative and competitive environments.* arXiv 2020.
- **[7]** B. Chen, M. Xu, L. Li, D. Zhao. *Delay-aware model-based reinforcement learning for continuous control.* Neurocomputing, 2021.
- **[9]** V. Firoiu, T. Ju, J. Tenenbaum. *At human speed: Deep reinforcement learning with action delay.* arXiv 2018.
- **[15]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* arXiv 2023.
- **[20]** P. Liotet, D. Maran, L. Bisi, M. Restelli. *Delayed reinforcement learning by imitation.* ICML 2022.
- **[21]** J. Liu, Z. Wang, P. Hang, J. Sun. *Delay-aware multi-agent reinforcement learning for cooperative adaptive cruise control with model-based stability enhancement.* arXiv 2024.
- **[23]** M. R. Matausek, A. D. Micic. *On the modified smith predictor for controlling a process with an integrator and long dead-time.* IEEE Transactions on Automatic Control, 1999.
- **[25]** S.-I. Niculescu. *Delay effects on stability: a robust control approach.* Springer, 2003.
- **[32]** T. J. Walsh, A. Nouri, L. Li, M. L. Littman. *Learning and planning in environments with delayed feedback.* Autonomous Agents and Multi-Agent Systems, 2009.
- **[33]** F. Wang, H. Zhang, Y. Zhang. *Resolving action delay: Multi-agent reinforcement learning based on state prediction.* Chinese Intelligent Systems Conference, Springer 2024.
- **[34]** W. Wang, D. Han, X. Luo, D. Li. *Addressing signal delay in deep reinforcement learning.* ICLR 2023.
- **[35]** Y. Yang, H. Zhong, T. Wu, B. Liu, L. Wang, S. S. Du. *A reduction-based framework for sequential decision making with delayed feedback.* NeurIPS 2023.
- **[36]** T. Yuan, H.-M. Chung, J. Yuan, X. Fu. *DACom: Learning delay-aware communication for multi-agent reinforcement learning.* AAAI 2023.
- **[39]** Y. Zhang, R. Zhang, Y. Gu, N. Li. *Multi-agent reinforcement learning with reward delays.* Learning for Dynamics and Control Conference (L4DC), PMLR 2023.
