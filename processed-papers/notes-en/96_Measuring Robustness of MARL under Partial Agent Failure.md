# 96. Measuring the Robustness of Multi-Agent Reinforcement Learning Systems under Partial Agent Failure

## Metadata
- **Title**: Measuring the Robustness of Multi-Agent Reinforcement Learning Systems under Partial Agent Failure
- **Authors**: Zoltán Barta, Balázs Nagy, László Gulyás
- **Affiliation**: Department of Artificial Intelligence, ELTE Eötvös Loránd University, Budapest, Hungary
- **Venue**: Intelligent Robotics FAIR 2025 (IntRob '25), June 23–24, 2025, Budapest, Hungary (ACM)
- **Link/arXiv**: https://doi.org/10.1145/3759355.3759373

## Taxonomy
- **Robustness / perturbation type targeted**: Partial agent failure (sensor degradation modeled as zero-mean Gaussian observation noise applied to a subset of agents); evaluation-time fault injection on perception.
- **Method paradigm**: Empirical robustness measurement / fault-injection benchmarking of a standard CTDE algorithm (MAPPO); no specialized robust-training method is proposed.
- **Keywords**: MARL, Robustness, MAPPO, Continuous Control, TorchRL, partial agent failure, observation noise, reward shaping

## TL;DR
The paper introduces a systematic evaluation-time fault-injection framework that perturbs the observations of a fraction of agents with Gaussian noise, and uses it to benchmark MAPPO on two cooperative navigation-style tasks, finding that the dominant failure axis (fraction of faulty agents vs. noise magnitude) is dictated primarily by the reward design (collision penalties vs. collision-tolerant rewards).

## Problem & Motivation
Multi-agent systems are increasingly deployed in dynamic, unpredictable environments where partial agent failures—sensor degradation, actuator malfunctions, or communication loss—are inevitable, yet most MARL studies assume ideal operational conditions. Understanding how MARL policies perform when individual agents experience mild faults is essential for building robust, reliable robotic systems. While prior robustness work focuses heavily on worst-case, attacker-driven adversarial scenarios, how naturally occurring sensor noise and partial agent failures interact with task-level reward design is largely unaddressed; this paper addresses that gap.

## Robustness Setting
- **Threat model / uncertainty set**: Perturbations are injected only during the evaluation phase (training is clean and noise-free). A subset of agents (e.g., 10%, 30%, 50%) is selected, and zero-mean Gaussian noise N(0, σ²) is added to those agents' observations: õ_i = o_i + N(0, σ²), where σ controls noise intensity. Both σ and the proportion of affected agents are varied. No adversary/optimization; noise is naturally occurring sensor drift, not gradient-based attack.
- **Setting**: Cooperative (shared global reward); Centralized Training with Decentralized Execution (CTDE); training online in a clean environment, robustness assessed offline-style during evaluation only (perturbations not seen during training). Continuous action and observation spaces under full observability.

## Method
- Design an evaluation pipeline that separates a clean training phase from a perturbed evaluation phase; perturbations are introduced exclusively at evaluation time.
- Train MAPPO (actor-critic policy optimization extending PPO to cooperative multi-agent settings) under CTDE, with parameter sharing, implemented in TorchRL on the VMAS simulator.
- During evaluation, select a percentage of agents and corrupt their observations with zero-mean Gaussian noise (Equation 1), sweeping a full grid of noise levels σ and affected-agent percentages.
- Measure system performance via average global (shared) reward, comparing clean vs. noisy evaluation scenarios; aggregate over five independent seeds following the standardised cooperative-MARL evaluation protocol of Gorsane et al.

## Theoretical Contributions
None / mostly empirical. The paper is a purely empirical robustness measurement study; it provides no convergence, sample-complexity, equilibrium, or certified-robustness guarantees.

## Experiments
- **Environment/Benchmark**: Vectorized Multi-Agent Simulator (VMAS), two cooperative tasks — Navigation (agents reach randomly assigned goals while avoiding collisions; collisions penalized) and Sampling (agents explore a multimodal Gaussian density field collecting samples; collisions ignored). 10 agents, 5,000,000 training steps, TorchRL (v0.7).
- **Baselines**: Environment-provided heuristic solutions (Navigation: a lidar-augmented straight-line goal-direction heuristic; Sampling: a heuristic guiding agents toward highest-value regions while avoiding collisions). The clean, unperturbed MAPPO policy (0.0 noise, 0% faulty) serves as the reference baseline.
- **Evaluation metrics**: Episodic return / average global reward; mean return over the final 50% of evaluation checkpoints, with standard deviation of return reflecting performance variability. Relative change vs. unperturbed (100%) performance. Evaluation follows the protocol of Gorsane et al.

## Key Results
- Navigation (collision-penalized): robustness is ratio-bound. With ≤30% of agents affected, MAPPO retains at least 70% of clean reward even at the largest noise (σ=4.0); once ≥50% are impaired, global reward declines almost linearly, reaching a relative change of −144% when every agent is disturbed. Returns turn negative beyond ~40–50% faulty (e.g., R=−47 at 50% faulty, σ=4.0).
- Sampling (collision-tolerant): robustness is noise-bound. Reward stays high (R≳420) while σ ≲ 0.6 regardless of faulty fraction, then declines; a fully corrupted team still captures ~92% of baseline at σ=1.6. Beyond σ≥3.2 returns collapse near-synchronously across all ratios (R≈195 at σ=4.0), with column differences ≲5%.
- Whether robustness is ratio-bound or noise-bound is dictated less by the disturbance itself than by what the reward function punishes. Failures are dominated by a handful of topologically central "hub" robots: identical noise/ratio settings can differ by more than 40% in return depending on which specific (centrally located) agents are impaired.

## Limitations & Future Work
- "Free" robustness from standard training is limited: both policies share the same neural backbone that absorbs light perturbations but cannot compensate beyond task-specific breakpoints.
- Only observation (perception) noise modeled as Gaussian sensor drift; actuator faults, communication loss, and adversarial/worst-case perturbations are not directly evaluated.
- Future: use training environments and reward functions that reflect real-world constraints (explicitly penalize unsafe collisions so policies behave like the Navigation model); identify and shield "critical"/hub agents (e.g., redundant sensors, backup controllers); develop fault-isolation mechanisms that prevent error propagation when several agents fail simultaneously; further study how partial perceptual corruption of a fraction of agents impacts global performance.

## Relevance to Survey
Sits on the "agent failure / fault tolerance" and "state/observation perturbation" lines of robust MARL, but as an empirical measurement/benchmarking contribution rather than a new robust-training algorithm. It connects the adversarial-robustness-testing literature (comprehensive test suites, critical-agent attacks) and the naturally-occurring-noise / noisy-observation MARL literature, and contributes the insight that reward shaping (collision penalties) and agent centrality govern which perturbation axis is fatal. Useful as a reference point for how reward design and topological agent importance modulate robustness, and for the CTDE/MAPPO baseline behavior under partial failure.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work]_

"A growing body of research probes the fragility of cooperative multi-agent reinforcement learning under intentionally crafted disturbances. Most existing studies focus on targeted, gradient-based attacks that perturb the local state of agents so as to maximise team-level disruption. Comprehensive test suites [8] systematically inject adversarial perturbations into observation and reward channels, while other works [9, 17] demonstrate that corrupting only a few strategically chosen agents can trigger group-wide failure."

"Agent drop-outs and communication losses are modelled in some approaches [16], while others [6] crafts Gaussian noise with predefined distribution profiles to mimic sensor drift. Although earlier studies [5, 11] acknowledge stochastic disturbances, their coverage of noise types and magnitudes remains limited."

"The understanding of worst-case, attacker-driven scenarios is advanced, but how naturally occurring sensor noise and partial agent failures interact with task-level reward design is largely unaddressed. This paper addresses this question."

> _[Introduction]_

"While multi-agent reinforcement learning (MARL) has demonstrated impressive success in training coordinated behaviors [14], most existing studies assume ideal operational conditions. However, the real world is far from perfect, and understanding how MARL policies perform when individual agents experience mild faults is essential for building robust and reliable robotic systems [12]."

### Cited references (resolved from the paper's bibliography)
- **[5]** Chen, Liu, Luo, Yin. *Robust multi-agent reinforcement learning for noisy environments.* Peer-to-Peer Networking and Applications, 2022.
- **[6]** Geng, Xiao, Li, Wei, Wang, Zhao. *Noise Distribution Decomposition based Multi-Agent Distributional Reinforcement Learning.* arXiv 2024.
- **[8]** Guo, Chen, Hao, Yin, Yu, Li. *Towards Comprehensive Testing on the Robustness of Cooperative Multi-agent Reinforcement Learning.* arXiv 2022.
- **[9]** He, Han, Su, Han, Zou, Miao. *Robust Multi-Agent Reinforcement Learning with State Uncertainty.* arXiv 2023.
- **[11]** Kilinc, Montana. *Multi-agent Deep Reinforcement Learning with Extremely Noisy Observations.* arXiv 2018.
- **[12]** Moos, Hansel, Abdulsamad, Stark, Clever, Peters. *Robust Reinforcement Learning: A Review of Foundations and Recent Advances.* Machine Learning and Knowledge Extraction, 2022.
- **[14]** Papadopoulos, Kontogiannis, Papadopoulou, Poulianou, Koumentis, Vouros. *An Extended Benchmarking of Multi-Agent Reinforcement Learning Algorithms in Complex Fully Cooperative Tasks.* arXiv 2025.
- **[16]** Zhao, Zhao, Wang, Yang, Hu, Zhou, Hao, Li. *Coach-assisted Multi-Agent Reinforcement Learning Framework for Unexpected Crashed Agents.* arXiv 2022.
- **[17]** Zhou, Liu. *Robustness Testing for Multi-Agent Reinforcement Learning: State Perturbations on Critical Agents.* IOS Press 2023.
