# 123. Distributionally Robust Multi-Agent Reinforcement Learning for Intelligent Traffic Control

## Metadata
- **Title**: Distributionally Robust Multi-Agent Reinforcement Learning for Intelligent Traffic Control
- **Authors**: Shuwei Pei, Joran Borger, Arda Kosay, Muhammed O. Sayin, Saeed Ahmed
- **Affiliation**: Jan C. Willems Center for Systems and Control, ENTEG, University of Groningen, the Netherlands; Department of Electrical, Electronics Engineering, Bilkent University, Ankara, Turkey
- **Venue**: Not specified (arXiv preprint, arXiv:2512.18558v1 [eess.SY], 21 Dec 2025)
- **Link/arXiv**: arXiv:2512.18558v1

## Taxonomy
- **Robustness / perturbation type targeted**: Demand/environment distribution shift in traffic signal control (worst-case over a finite set of heterogeneous traffic-demand scenarios); group-distributionally-robust optimization steering toward poorly-performing demand patterns.
- **Method paradigm**: Distributionally robust optimization (worst-case over scenario mixtures), adversarial scenario reweighting via a contextual-bandit worst-case estimator (CB-WCE), two-timescale adversarial training, PPO-based MARL with CTDE and parameter sharing.
- **Keywords**: Reinforcement Learning, Distributionally Robust Optimization, Traffic Signal Control, Intelligent Transportation Systems, MARL, contextual bandit

## TL;DR
The paper builds a distributionally robust MARL traffic-signal controller by fine-tuning a PPO-based CTDE baseline against worst-case demand mixtures selected by a contextual-bandit worst-case estimator, yielding consistently lower queues and higher speeds across eight demand scenarios plus an unseen Sioux Falls validation network (up to 51% shorter queues and 38% higher speeds on the worst-performing scenarios).

## Problem & Motivation
Learning-based traffic signal control is typically optimized for average performance under a few nominal demand patterns, which can produce poor behavior under atypical or disrupted traffic conditions. Operators care strongly about worst-case behavior across diverse demand scenarios (e.g., peak hours, incidents), but standard RL objectives provide no guarantees on tail performance. While robust and distributionally robust RL methods exist, they have mainly been tested on abstract benchmarks with simplified dynamics and unconstrained action spaces, and it is unclear how well they transfer to network-level traffic signal control where demand is highly variable and signal phases must satisfy strict safety constraints. The paper addresses this gap by biasing a MARL controller toward hard demand cases without changing the policy architecture or environment.

## Robustness Setting
- **Threat model / uncertainty set**: A finite set of K = 8 representative OD-based traffic-demand scenarios (one derived from the pNEUMA dataset, seven synthetic). A contextual-bandit worst-case estimator plays an adversarial role, selecting non-negative mixture weights over these scenarios to maximize network-wide congestion (cumulative waiting time), defining adversarial mixed demand patterns. Robustness objective targets J_worst = min over scenarios of expected return, while ideally preserving/improving J_avg.
- **Setting**: Cooperative MARL (homogeneous agents, shared policy, team reward); centralized-training-decentralized-execution (CTDE) with parameter sharing; online RL training in a SUMO/FLOW simulator. Two-timescale: signal agents act every simulation second, the estimator acts once per 600 s window.

## Method
- Train a baseline MARL controller where each of nine intersections is a PPO agent with compact lane-based observations (79-dim vector) and eight discrete non-conflicting signal phases, under a CTDE scheme with parameter sharing and a shared team reward (mean-speed term minus queue penalty); safety enforced via a fixed 5 s clearance interval.
- Construct eight heterogeneous OD-based demand scenarios (pNEUMA-derived plus seven synthetic patterns spanning uniform, inbound/outbound, corridor, and diagonal cross-town flows) to span a wide range of spatial demand patterns.
- Train a contextual-bandit worst-case estimator (CB-WCE) that, conditioned on an 18-dim window-level context (average speed and density per intersection), outputs mixture weights w over the eight scenarios; trained by a policy-gradient objective to maximize accumulated vehicle waiting time (Eq. 4), against a frozen baseline policy.
- Fine-tune the baseline MARL with the frozen CB-WCE acting as a demand scheduler: each 600 s window the estimator selects a worst-case demand mixture, and the PPO policy parameters are updated (Eq. 1/2 unchanged), gradually adapting the signal policy to adversarially chosen demand mixtures, producing the DR-MARL controller.

## Theoretical Contributions
None / mostly empirical. The paper introduces a scenario-based robustness objective (J_avg, J_worst) and two algorithms (Algorithm 1 CB-WCE training; Algorithm 2 DR-MARL training), but provides no convergence, sample-complexity, or equilibrium-existence guarantees.

## Experiments
- **Environment/Benchmark**: A 3 x 3 signalized urban grid calibrated from a contiguous 3 x 3 subarea of central Athens (pNEUMA trajectory dataset), simulated in SUMO and interfaced via FLOW; nine demand groups (groups 0–6 synthetic, group 7 pNEUMA, group 8 unseen Sioux Falls-based validation network).
- **Baselines**: PPO MARL (the expectation-maximizing multi-agent PPO controller) vs. DR-MARL (same PPO architecture retrained with the CB-WCE over eight demand scenarios).
- **Evaluation metrics**: Network-level queue length (total queued vehicles) and average speed (mean vehicle speed), horizon-averaged and averaged over 10 evaluation rollouts of length 3600 s per group; per-group improvement and worst-case (J_worst) comparison.

## Key Results
- DR-MARL substantially reduces average queue length and increases average speed for every one of the nine demand groups; queue length decreases by roughly 21–69% across groups (largest in group 7, −68.68%), average speed increases by roughly 16–77% (largest in groups 6 and 7, about +76.7%).
- On worst-case performance: DR-MARL reduces the worst observed average queue length by about 51.2% (baseline group 7 vs. DR-MARL group 5) and increases the worst observed average speed by about 38.4% (baseline group 6 vs. DR-MARL group 5).
- On the unseen Sioux Falls group (group 8), DR-MARL reduces queues by about 41.6% and increases speed by about 22.9%, indicating better generalization than the baseline to an unseen demand distribution.
- Some rollout-level overlap between the two controllers remains (a few rollouts perform similarly to or marginally worse than the baseline), expected given simulation stochasticity and the finite set of training demand groups.

## Limitations & Future Work
- Robustness is assessed on a finite set of hand-crafted demand scenarios on a stylized 3 x 3 grid, restricting the diversity of operating conditions and network structures represented.
- The worst-case estimator is trained only against the baseline MARL controller and then kept fixed during DR-MARL fine-tuning, so its selected demand patterns reflect worst cases of the baseline rather than of the improved controller.
- Future work: extend to larger and more heterogeneous networks, and allow the worst-case estimator to adapt to the evolving DR-MARL policy.

## Relevance to Survey
An applied distributionally-robust MARL paper sitting on the "environment/distribution-shift robustness" main line, instantiated for intelligent traffic signal control. It connects the group-DRO line (Sagawa et al., 2020; Hashimoto et al., 2018) and adversarial scenario-reweighting (contextual-bandit worst-case estimation, Liu et al., 2025) to cooperative CTDE MARL. Useful as an example of the "adversarial/worst-case training via a slower-timescale adversary that perturbs the environment distribution" method line applied to a safety-constrained, real-data-calibrated systems-and-control domain, contrasting with the robust-Markov-game/minimax theory line.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Reinforcement learning (RL) offers a data-driven alternative that can adapt signal timing directly from interaction with traffic (Sutton and Barto, 1998). For single intersections, deep RL controllers with compact lane- or image-based encodings, discrete phase-switching actions, and delay-oriented rewards, have demonstrated improvements over fixed-time baselines in simulation (Huang et al., 2023). To handle networks, multi-agent reinforcement learning (MARL) assigns an agent to each intersection and coordinates them via local observations and limited neighborhood context, achieving promising results on grid and arterial networks (Zhang et al., 2023). These methods, however, are typically trained on a small set of nominal demand patterns and optimized for expected return, with evaluation focused on average performance."

> _[Introduction]_

"In practice, operators care strongly about worst-case behaviour across diverse traffic demand scenarios (e.g., peak-hours or disrupted conditions), not only average delay. Standard RL objectives provide no guarantees on tail performance, motivating robust and distributionally robust formulations that bias learning toward hard cases by upweighting poorly performing scenario groups (Sagawa et al., 2020). To address this, in this paper, we adopt a contextual-bandit worst-case estimator (CB-WCE) (Liu et al., 2025), which adaptively reweights traffic scenarios during training and thus steers a standard MARL controller trained with proximal policy optimization (PPO) towards improved worst-case performance, while keeping the policy architecture and environment unchanged. While robust and distributionally robust RL methods have been developed and tested mainly on abstract benchmarks with simplified dynamics and unconstrained action spaces (Sagawa et al., 2020; Hashimoto et al., 2018), it is still unclear how well these techniques transfer to network-level traffic signal control, where demand is highly variable and signal phases must satisfy strict safety constraints."

### Cited references (resolved from the paper's bibliography)
- **(Sutton and Barto, 1998)** Sutton, Barto. *Reinforcement learning: An introduction.* MIT Press 1998.
- **(Huang et al., 2023)** Huang, Lin, Kuo, Lin, Sayin, Lin. *Reinforcement-learning-based job-shop scheduling for intelligent intersection management.* DATE 2023.
- **(Zhang et al., 2023)** Zhang, Yu, Zhang, Wang, Luan, Guo, Yuen. *Learning decentralized traffic signal controllers with multi-agent graph reinforcement learning.* IEEE Transactions on Mobile Computing 2023.
- **(Sagawa et al., 2020)** Sagawa, Koh, Hashimoto, Liang. *Distributionally robust neural networks for group shifts: On the importance of regularization for worst-case generalization.* ICLR 2020.
- **(Liu et al., 2025)** Liu, Iloglu, Caldara, Durham, Zavlanos. *Distributionally robust multi-agent reinforcement learning for dynamic chute mapping.* ICML 2025.
- **(Hashimoto et al., 2018)** Hashimoto, Srivastava, Namkoong, Liang. *Fairness without demographics in repeated loss minimization.* ICML 2018.
