# 102. Mava: a research library for distributed multi-agent reinforcement learning in JAX

## Metadata
- **Title**: Mava: a research library for distributed multi-agent reinforcement learning in JAX
- **Authors**: Ruan de Kock, Omayma Mahjoub, Sasha Abramowitz, Wiem Khlifi, Callum Rhys Tilbury, Claude Formanek, Andries Smit, Arnu Pretorius
- **Affiliation**: InstaDeep
- **Venue**: Not specified (preliminary technical report; arXiv:2107.01460v2, 15 Dec 2023)
- **Link/arXiv**: arXiv:2107.01460v2 [cs.LG]; open-source repository https://github.com/instadeepai/Mava

## Taxonomy
- **Robustness / perturbation type targeted**: Not specified (this is a software/library report; "robust" here refers to statistically robust benchmarking and reliable evaluation of MARL experiments, not adversarial/model-uncertainty robustness)
- **Method paradigm**: Research software library / engineering framework (JAX-based distributed MARL; Anakin podracer architecture; CTDE and DTDE multi-agent PPO)
- **Keywords**: MARL library, JAX, distributed training, Anakin architecture, multi-agent PPO, statistically robust evaluation

## TL;DR
Mava is an open-source research library for online MARL written purely in JAX that aims to balance simple, readable single-file code with scalable, fast distributed training (the Anakin architecture), achieving 10–100x speedups over popular MARL frameworks while integrating into a broader ecosystem (Jumanji, JaxMARL, OG-MARL, Flashbax/Vault, MARL-eval) to support statistically robust research.

## Problem & Motivation
MARL research is computationally expensive and it is often hard to obtain enough experiment samples to test hypotheses and make robust statistical claims; MARL algorithms are also complex and tricky to implement correctly. Building useful research software requires striking a balance between code that is highly performant (to run expensive experiments efficiently) and code that is easy to understand (to enable rapid conceptual and algorithmic development). Highly modular frameworks can be too slow or opaque, while overly simple ones can be too slow for meaningful enquiry. Mava aims to fill the gap for online MARL research by being simple enough to implement new ideas quickly yet scalable and fast enough to test them in a reasonable amount of time.

## Robustness Setting
- **Threat model / uncertainty set**: Not specified (the paper does not study perturbations, adversaries, or model uncertainty; "robust" is used in the sense of robust/statistically reliable evaluation and benchmarking)
- **Setting**: Cooperative MARL focus; supports both decentralised training with decentralised execution (DTDE) and centralised training with decentralised execution (CTDE); online MARL in particular (with demonstrated online-to-offline workflow integration)

## Method
- A "clean code" philosophy: core algorithmic logic is kept in a single easy-to-read file (akin to CleanRL and PureJAXRL), with some abstraction for environment initialisation, reusable type definitions, and Hydra-based configuration management, so code is easy to debug, adapt, and extend.
- Supports the Anakin podracer architecture (Hessel et al., 2021) for scalable distributed training on hardware accelerators: parameters are replicated across D devices via jax.pmap, broadcast to J update functions via jax.vmap, each rolling out experience from N environment copies; gradients are averaged across update functions and devices via jax.pmean.
- Implements both recurrent and feedforward multi-agent PPO systems following the DTDE and CTDE paradigms; supports out-of-the-box pmap over multiple devices (e.g., TPUs).
- Solves the JAX jit-compilation evaluation problem by interleaving evaluation blocks during training (training and evaluation blocks are pmap-ed and run sequentially in a normal Python for loop), enabling continual metric logging and checkpointing; logs to Tensorboard, Neptune, and JSON in a MARL-eval-compatible format.
- Integrates with an ecosystem: JAX-native environments (Matrax, Jumanji, JaxMARL), statistically robust evaluation reporting (MARL-eval), offline MARL (OG-MARL), and efficient experience storage (Flashbax Vault).

## Theoretical Contributions
None / mostly empirical (this is a software technical report; no formal theory, convergence, or guarantees are presented).

## Experiments
- **Environment/Benchmark**: Multi-Robot Warehouse (RWARE) — Jumanji's RWARE for Mava, original RWARE for EPyMARL (tiny-2ag, tiny-4ag, small-4ag); Level-Based Foraging (LBF) — Jumanji's LBF for Mava, original LBF for EPyMARL (15x15-4p-3f, 2s-8x8-2p-2f, i.e., 2- and 4-agent settings); StarCraft Multi-Agent Challenge in JAX (SMAX) scenarios 2s3z, 3s5z, 6h vs 8z; an online-to-offline demonstration on RWARE (online Mava PPO recorded via Flashbax Vault, then MAICQ trained offline in OG-MARL).
- **Baselines**: EPyMARL (PyTorch-based, extension of PyMARL) running feedforward and recurrent IPPO and MAPPO; JaxMARL's JAX-based PPO baselines (recurrent IPPO/MAPPO) on SMAX; OG-MARL's MAICQ for the offline demonstration.
- **Evaluation metrics**: Mean/evaluation episode return, win rate (%) for SMAX, steps per second (scalability), and run time in minutes (wallclock training time); evaluation follows the protocol of Gorsane et al. (2022).

## Key Results
- Mava is about 10x faster than EPyMARL for the same number (16) of parallel environments, and at 256 vectorised environments it achieves more than 100x speedups while maintaining good performance (e.g., RWARE convergence in roughly 2 minutes at scale).
- On RWARE, Mava's feedforward MAPPO shows equal or enhanced performance versus EPyMARL at significantly reduced wallclock time (from hours to minutes); reported per-task speedups include 10.6x, 8.4x, and 9.8x for 16 vmap-ed environments.
- On LBF, Mava's recurrent MAPPO achieves superior performance at ~10x the speed; using a TPU-V3 it trains to convergence in under five minutes.
- On SMAX, Mava's recurrent IPPO and MAPPO match JaxMARL's baselines (no hyperparameter tuning, using JaxMARL's hyperparameters); FF-IPPO reaches ~85% win rate on 2s3z in under a minute (54 seconds).

## Limitations & Future Work
- Experiments are explicitly preliminary and not meant as an extensive investigation; the authors suspect significant improvements are possible with proper hyperparameter tuning, and note uncertainty in interpreting reported JaxMARL speeds.
- Mava currently only supports environments written in JAX; comparing JaxMARL environment results to their non-JAX versions may be invalid due to subtle but important differences.
- Currently focuses on on-policy multi-agent PPO; the roadmap includes off-policy algorithms leveraging the Anakin architecture and both on/off-policy algorithms supporting distributed non-JAX environment training via the Sebulba architecture.
- Plans to add support for additional environments and to run Mava (on- and off-policy) across all SMAX scenarios.

## Relevance to Survey
This is an infrastructure/tooling contribution rather than a robustness-method paper. Its relevance to a Robust MARL survey is primarily as enabling software: it explicitly motivates statistically robust and reproducible MARL research (via MARL-eval and the evaluation protocol of Gorsane et al., 2022) and provides a fast, scalable JAX platform on which robust MARL algorithms and benchmarks could be implemented and reliably evaluated. It does not propose any robustness mechanism (no adversarial training, model uncertainty, or perturbation handling), so it sits at the periphery of the survey as a benchmarking/experimental-rigor enabler.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Design and core features — "A clean code philosophy."]_

"A clean code philosophy. Moving away from completely modular MARL frameworks (Samvelyan et al., 2019a; Papoudakis et al., 2021; Hu et al., 2023; Bettini et al., 2023), Mava instead adopts a code philosophy akin to recent works such as CleanRL (Huang et al., 2022) and PureJAXRL (Lu et al., 2022) where all core algorithmic logic should be contained in a single easy-to-read file. This enables researchers to debug code easily and to adapt Mava to their particular use case with little friction and overhead. A notable difference between CleanRL and Mava is that Mava has certain levels of abstraction; on environment initialisation, reusable type definitions and flexible algorithm and environment configuration management with Hydra (Yadan, 2019). This approach strikes a balance where code is easy to understand but unnecessary boilerplate code is abstracted away."

> _[Section 2, Design and core features — "Multi-device training with easy checkpointing and logging."]_

"Mava offers some core benefits over recent MARL offerings in JAX (Rutherford et al., 2023). The first of which is out-of-the-box support for code to be pmap-ed over multiple devices on hardware accelerators like TPUs for faster training times. The second is support for robust evaluation, system checkpointing and continual metric logging. It is common in MARL systems to freeze training periodically in order to evaluate current agent policies (Gorsane et al., 2022)."

> _[Section 3, Seamless integration between ecosystem libraries — "Standardised and statistically robust evaluation reporting."]_

"To ensure a high level of standardisation and statistical rigour in the evaluation of experimental outcomes, Mava can log raw experimental data in such a way that it conforms to the format expected by MARL-eval (Gorsane et al., 2022). MARL-eval implements the data aggregation and reporting proposed by Gorsane et al. (2022), based on the principles established in (Agarwal et al., 2021). This equips MARL-eval with statistically sound plotting tools, enabling robust and reliable analysis of cooperative MARL experiments."

> _[Section 3, Seamless integration between ecosystem libraries — "Offline MARL."]_

"A promising and increasingly popular research direction in MARL is offline training (Yang et al., 2021; Tseng et al., 2022; Meng et al., 2023; Tian et al., 2023; Wang et al., 2023). In offline MARL, agents are trained on a static dataset of experience without any additional online interactions in the environment. Offline MARL is an appealing paradigm because it avoids online environment interactions which can be slow, expensive and dangerous if a simulator is not readily available. Another promising approach is combining offline with online training to make online training significantly more sample efficient (Nair et al., 2020; Wagenmaker and Pacchiano, 2023; Ball et al., 2023). Formanek et al. (2023b) demonstrated that a similar approach can significantly speed up online training in MARL. Recently, Off-the-Grid MARL (Formanek et al., 2023a) was proposed as a framework for offline MARL research."

### Cited references (resolved from the paper's bibliography)
- **(Agarwal et al., 2021)** Agarwal, Schwarzer, Castro, Courville, Bellemare. *Deep reinforcement learning at the edge of the statistical precipice.* NeurIPS 2021.
- **(Ball et al., 2023)** Ball, Smith, Kostrikov, Levine. *Efficient online reinforcement learning with offline data.* ICML (PMLR) 2023.
- **(Bettini et al., 2023)** Bettini, Prorok, Moens. *BenchMARL: Benchmarking multi-agent reinforcement learning.* arXiv:2312.01472, 2023.
- **(Formanek et al., 2023a)** Formanek, Jeewa, Shock, Pretorius. *Off-the-grid MARL: Datasets and baselines for offline multi-agent reinforcement learning.* Extended Abstract at AAMAS 2023.
- **(Formanek et al., 2023b)** Formanek, Tilbury, Shock, Pretorius, et al. *Reduce, reuse, recycle: Selective reincarnation in multi-agent reinforcement learning.* Workshop on Reincarnating Reinforcement Learning at ICLR 2023.
- **(Gorsane et al., 2022)** Gorsane, Mahjoub, de Kock, Dubb, Singh, Pretorius. *Towards a standardised performance evaluation protocol for cooperative MARL.* NeurIPS 2022.
- **(Hu et al., 2023)** Hu, Zhong, Gao, Wang, Dong, Liang, Li, Chang, Yang. *MARLlib: A scalable and efficient multi-agent reinforcement learning library.* JMLR 2023.
- **(Huang et al., 2022)** Huang, Dossa, Ye, Braga, Chakraborty, Mehta, Araújo. *CleanRL: High-quality single-file implementations of deep reinforcement learning algorithms.* JMLR 2022.
- **(Lu et al., 2022)** Lu, Kuba, Letcher, Metz, Schroeder de Witt, Foerster. *Discovered policy optimisation.* NeurIPS 2022.
- **(Meng et al., 2023)** Meng, Wen, Le, Li, Xing, Zhang, Wen, Zhang, Wang, Yang, et al. *Offline pre-trained multi-agent decision transformer.* Machine Intelligence Research 2023.
- **(Nair et al., 2020)** Nair, Gupta, Dalal, Levine. *AWAC: Accelerating online reinforcement learning with offline datasets.* arXiv:2006.09359, 2020.
- **(Papoudakis et al., 2021)** Papoudakis, Christianos, Schäfer, Albrecht. *Benchmarking multi-agent deep reinforcement learning algorithms in cooperative tasks.* NeurIPS Datasets and Benchmarks Track 2021.
- **(Rutherford et al., 2023)** Rutherford, Ellis, Gallici, Cook, Lupu, Ingvarsson, Willi, Khan, Schroeder de Witt, Souly, et al. *JaxMARL: Multi-agent RL environments in JAX.* arXiv:2311.10090, 2023.
- **(Samvelyan et al., 2019a)** Samvelyan, Rashid, Schroeder de Witt, Farquhar, Nardelli, Rudner, Hung, Torr, Foerster, Whiteson. *The StarCraft Multi-Agent Challenge.* CoRR abs/1902.04043, 2019.
- **(Tian et al., 2023)** Tian, Kuang, Liu, Wang. *Learning from good trajectories in offline multi-agent reinforcement learning.* AAAI 2023.
- **(Tseng et al., 2022)** Tseng, Wang, Lin, Isola. *Offline multi-agent reinforcement learning with knowledge distillation.* NeurIPS 2022.
- **(Wagenmaker and Pacchiano, 2023)** Wagenmaker, Pacchiano. *Leveraging offline data in online reinforcement learning.* ICML (PMLR) 2023.
- **(Wang et al., 2023)** Wang, Xu, Zheng, Zhan. *Offline multi-agent reinforcement learning with implicit global-to-local value regularization.* NeurIPS 2023.
- **(Yadan, 2019)** Yadan. *Hydra - a framework for elegantly configuring complex applications.* GitHub, 2019.
- **(Yang et al., 2021)** Yang, Ma, Li, Zheng, Zhang, Huang, Yang, Zhao. *Believe what you see: Implicit constraint approach for offline multi-agent reinforcement learning.* NeurIPS 2021.
