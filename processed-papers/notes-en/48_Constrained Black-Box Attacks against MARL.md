# 48. Constrained Black-Box Attacks Against Cooperative Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Constrained Black-Box Attacks Against Cooperative Multi-Agent Reinforcement Learning
- **Authors**: Amine Andam, Jamal Bentahar, Mustapha Hedabou
- **Affiliation**: Mohammed VI Polytechnic University; Khalifa University; Concordia University
- **Venue**: Not specified (arXiv:2508.09275v2 [cs.LG], 21 Jan 2026)
- **Link/arXiv**: arXiv:2508.09275v2; code: https://github.com/AmineAndam04/black-box-marl.git

## Taxonomy
- **Robustness / perturbation type targeted**: Test-time adversarial observation perturbation attacks against cooperative MARL (c-MARL); black-box and "free" (no-access) attacks; constrained adversary that can only collect/perturb observations of deployed agents.
- **Method paradigm**: Adversarial attacks (offensive robustness probing); misalignment-based perturbation; PGD/FGSM optimization of an alignment-prediction network; orthogonal/structured perturbations via partial Hadamard matrices; targeted agent selection.
- **Keywords**: adversarial attacks, c-MARL, black-box, observation perturbation, misalignment, Hadamard matrices

## TL;DR
The paper proposes two constrained black-box test-time attacks against cooperative MARL — the Align attack (adversary only collects/perturbs observations, no policy/action access) and the Hadamard attack (no access at all, using orthogonal partial-Hadamard perturbations) — both of which sabotage coordination by inducing misaligned agent perceptions, achieving strong damage with as few as 1,000 collected samples.

## Problem & Motivation
Cooperative MARL (c-MARL) is increasingly deployed in real-world and sensitive domains, but its vulnerabilities to adversarial attacks are under-investigated, especially at deployment. Existing work mostly focuses on training-time (poisoning) attacks or relies on unrealistic assumptions for test-time attacks — white-box access to policy weights/architecture, the ability to train surrogate policies from scratch in the same environment, or imitation learning that needs observation-action pairs or the ability to query the model. Such strong-access threat models are often infeasible and, in white-box cases, the access itself constitutes a successful attack (leaking proprietary knowledge). The paper studies weaker, more plausible threat models: an adversary that can only collect and perturb the observations of deployed ("infected") agents, and an even more constrained adversary with no access whatsoever (only the ability to add small perturbations to observations).

## Robustness Setting
- **Threat model / uncertainty set**: Test-time, black-box. (1) Align attack: adversary can only collect and perturb the observations of deployed agents (no access to actions, rewards, or policy weights); cannot directly control actions; perturbations bounded by L∞ budget ϵ. (2) Hadamard ("free") attack: no access at all (no observations, actions, or weights), only the ability to inject small perturbations into each agent's observation; perturbations bounded by L∞ ≤ ϵ. SMAC scenarios add partial and dynamic access (agents may die, so not all agents are attackable throughout an episode).
- **Setting**: cooperative (c-MARL); test-time / deployment phase (agents pre-trained, weights frozen); attacks operate on (mostly partially observable) deployed multi-agent systems.

## Method
- **Misalignment intuition**: Effective cooperation depends on agents having aligned perceptions/beliefs about the environment (e.g., agreement on target health/position for focus-fire in SMAC). The attack uses a divide-and-conquer idea — make each agent perceive the environment differently to break coordination and degrade team performance. For partially observable settings with little observation overlap, the goal is to induce misalignment in common beliefs.
- **Align attack**: Train a neural network fθ to predict an agent's observation oi from the other agents' observations o−i (fθ(o−i) ≈ oi), minimizing mean squared error J(o; θ). Aligned observations are correlated and predictable, so a trained fθ gives high loss on misaligned inputs and thus measures misalignment. The attack finds small perturbations δ (∥δ∥∞ ≤ ϵ) that maximize J(o + δ; θ) via PGD. This is black-box, needs no policy/value access, and (unlike Eq. 1) adds perturbation to both fθ's input and output. Two phases: (1) collect observations of deployed agents for a period T^c and train fθ (no attack); (2) intercept current observations, generate and inject perturbations.
- **Targeted Align attack**: To reduce cost/improve stealth, attack only a subset M ⊂ N of size m, choosing the most mutually aligned agents (those most likely to coordinate) by minimizing J over candidate subsets (Eq. 7).
- **Free / Hadamard attack**: Without observation access, induce misalignment by pushing agents in orthogonal directions. Generate a perturbation matrix δ ∈ R^{n×d} whose rows are mutually orthogonal (Condition 1) and respect the budget (Condition 2). Partial Hadamard matrices H̃ (rows of a full Hadamard matrix, entries ±1, orthogonal rows) satisfy both via δ = ϵ × H̃. Since Hadamard matrices exist only when d is a multiple of 4, generate a full matrix of size d̃ = 2^⌊log2 d⌋ (largest power of two ≤ d) via Sylvester's construction and zero-pad the remaining columns (does not affect orthogonality or budget).
- **Targeted/combined attack**: Use the Align network fθ to identify critical agents (profiling) and inject Hadamard perturbations for fast generation — combining Align's selection capability with Hadamard's lightweight efficiency.

## Theoretical Contributions
None / mostly empirical. The work gives constructive arguments (orthogonality/budget conditions, partial-Hadamard construction with Sylvester's method, padding preserving orthogonality and budget) but no formal convergence, sample-complexity, or certified-robustness theorems.

## Experiments
- **Environment/Benchmark**: Three c-MARL benchmarks, 22 tasks: Level-Based Foraging (LBF, 10 environments, fully observable / highly cooperative / partially observable variants, obs dim 15–18, up to 4 agents), Multi-Robot Warehouse (RWARE, partially observable, sensory ranges 3×3/5×5/7×7, obs dim 71–351, 4 agents), and StarCraft Multi-Agent Challenge (SMAC, six partially observable games, obs dim 82–285, 5/10/27 agents). Agents trained with QMIX and MAPPO via the Epymarl library; weights frozen for attacks.
- **Baselines**: White-box attack (minimizes probability/Q-value of the optimal action, used as an upper bound and to choose meaningful ϵ); random attacks (uniform, normal, plus a non-symmetric exponential Exp(λ) distribution and temporally correlated Ornstein–Uhlenbeck noise; best random attack reported).
- **Evaluation metrics**: Episodic return reported as interquartile mean (IQM) over 50 independent episodes with 95% confidence intervals; percentage drop in return relative to benign reward; episode-length increase (%). PGD fixed at K = 10 with step size α = ϵ/K; fθ trained with feedforward (MLP), recurrent (RNN), and encoder-only Transformer architectures (default: MAPPO agents, 5,000 transitions, RNN fθ).

## Key Results
- Both Align and Hadamard attacks are effective across fully and partially observable tasks; attacks are substantially more effective in highly cooperative ("-coop") settings. In several partially observable scenarios the free Hadamard attack matches or outperforms Align; on SMAC, Align is consistent across games while Hadamard struggles to beat random noise in some scenarios.
- The attack is highly sample-efficient: strong performance is achieved with as few as 1,000 collected samples (vs. millions for prior methods), with no observable gains from larger datasets; a single PGD step (K=1) is often sufficient for strong, real-time attacks.
- Targeted attacks: Align maintains strong performance when ≥50% of agents are targeted and is less sensitive than Hadamard to targeting fewer agents. Using fθ to select agents and injecting Hadamard perturbations gives consistent additional return drops (up to −57%; average additional drop −11.5% on LBF, −6.18% on RWARE, −6.28% on SMAC), confirming fθ's value for target selection.
- Beyond return, the Align attack can substantially increase episode length on LBF (often double-digit percentages, up to 226% in the worst case), highlighting an overlooked metric for constrained adversaries.

## Limitations & Future Work
- The attack faces the same core challenges as any MARL training procedure, notably partial observability; handling heterogeneous agents and multi-modal observations may further reduce effectiveness.
- The study considers realistic attacks only from the perspective of the adversary's access and capabilities; other perspectives — system-level constraints, attack deployment, and detectability in real-world settings — are left to future work.

## Relevance to Survey
This paper sits on the adversarial-attack / test-time robustness line of cooperative MARL, characterizing c-MARL vulnerability under realistic, constrained (black-box and no-access) threat models. It connects the survey's themes of observation-perturbation attacks, communication/coordination robustness (exploiting reliance on aligned perceptions/common beliefs), and the white-box-vs-black-box and training-time-vs-test-time taxonomy of adversarial c-MARL. As an attack-side contribution, it motivates the defensive/robust-training literature by exposing how cheaply (1,000 samples, single-step PGD) coordination can be sabotaged.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related works]_

"Adversarial c-MARL can be classified according to several criteria: Does the attack occur during training or deployment? Are we considering a white-box or black-box scenario? What system components does the attacker have access to, and which does it target?"

"Training-time vs Test-time attacks. Training-time attacks, also called data poisoning attacks [Rakhsha et al., 2020], occur when an adversary is present during the training and aim to manipulate the agent into a target policy. This can involve reward poisoning [Liu and Lai, 2023; Zhang et al., 2020], environment poisoning [Rakhsha et al., 2021], or altering observations or actions [Hu and Zhang, 2022; Chen et al., 2024; Zheng et al., 2023]. However, interfering with training is not always feasible. MARL systems are arguably more vulnerable when deployed. Test-time attacks occur during deployment and aim to degrade agent performance. This is achieved by exploiting the known vulnerabilities of neural networks to adversarial inputs [Huang et al., 2017; Szegedy, 2013], mainly through observation manipulation [Pham et al., 2023; Lin et al., 2020], or action manipulation [Nisioti et al., 2021]."

"White-box vs Black-box. In white-box scenarios, the attacker knows the learning algorithm and has access to the policy weights and its architecture [Chen et al., 2024; Hu and Zhang, 2022; Nisioti et al., 2021; Lin et al., 2020; Pham et al., 2023; Huang et al., 2017]. While these attacks tend to be the most effective, it is impractical for the attacker to have the complete knowledge of the deployed policies. Conversely, black box settings allow for more relaxed assumptions [Huang et al., 2017]. Most existing work relies on learning a surrogate policy to exploit the transferability of adversarial examples [Papernot et al., 2016]. This surrogate policy can be learned by training the model from scratch [Huang et al., 2017], but doing so requires access to the training environment. Alternatively, imitation learning can be used to approximate the policy [Wu et al., 2021; Inkawhich et al., 2020], which would necessitate access to observation-action pairs or the ability to query the policy. Table 1 provides a comprehensive comparison between our work and previous work. Prior work on test-time attacks often assumes white-box adversaries and access to multiple elements simultaneously, which is not always feasible during deployment. We instead focus on more practical scenarios: deployed c-MARL in a black-box setting with limited access."

> _[Introduction]_

"Collaborative multi-agent reinforcement learning (c-MARL) algorithms have demonstrated state-of-the-art performances in complex cooperative tasks [Rashid et al., 2018; Yu et al., 2022], making them well-suited for solving real-world problems across various domains [Lv et al., 2025; Park et al., 2024; Zhang et al., 2024]. However, a critical prerequisite for the widespread adoption of c-MARL is a full understanding of its vulnerabilities to adversarial attacks [Huang et al., 2017; Kos and Song, 2017], particularly when deployed. While much of the literature on adversarial c-MARL focuses on training-time attacks [Zheng et al., 2023; Liu and Lai, 2023; Chen et al., 2024; Hu and Zhang, 2022], we focus instead on test-time attacks, where the adversary is present during deployment. Prior work on test-time attacks [Pham et al., 2023; Lin et al., 2020; Nisioti et al., 2021] has primarily considered white-box threat models, in which the adversary has access to the policy architecture and weights. This scenario is not always feasible. Moreover, such access can itself be considered a successful attack, as it typically involves proprietary knowledge with significant financial implications if leaked. In contrast, black-box threat models [Huang et al., 2017] do not assume access to the policy's weights or architecture; instead, they often involve learning a surrogate policy network either by training from scratch in the same environment [Huang et al., 2017] or through imitation learning [Wu et al., 2021; Inkawhich et al., 2020]. The former requires access to the training environment, while the latter relies on collecting both observations and actions or the ability to query the model (see Figure 1)."

### Cited references (resolved from the paper's bibliography)
- **[Rakhsha et al., 2020]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching via environment poisoning: Training-time adversarial attacks against reinforcement learning.* ICML 2020.
- **[Rakhsha et al., 2021]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching in reinforcement learning via environment poisoning attacks.* JMLR 22(210):1–45, 2021.
- **[Liu and Lai, 2023]** Liu, Lai. *Efficient adversarial attacks on online multi-agent reinforcement learning.* NeurIPS 2023.
- **[Zhang et al., 2020]** Zhang, Ma, Singla, Zhu. *Adaptive reward-poisoning attacks against reinforcement learning.* ICML 2020.
- **[Hu and Zhang, 2022]** Hu, Zhang. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv:2205.09362, 2022.
- **[Chen et al., 2024]** Chen, Liao, Zhao, Dai, Zhao. *Cuda2: An approach for incorporating traitor agents into cooperative multi-agent systems.* arXiv:2406.17425, 2024.
- **[Zheng et al., 2023]** Zheng, Li, Chen, Dong, Zhang, Lin. *One4all: Manipulate one agent to poison the cooperative multi-agent reinforcement learning.* Computers & Security 124:103005, 2023.
- **[Huang et al., 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv:1702.02284, 2017.
- **[Szegedy, 2013]** Szegedy. *Intriguing properties of neural networks.* arXiv:1312.6199, 2013.
- **[Pham et al., 2023]** Pham, Nguyen, Chen, Lam, Das, Weng. *Attacking c-marl more effectively: A data driven approach.* IEEE ICDM 2023.
- **[Lin et al., 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[Nisioti et al., 2021]** Nisioti, Bloembergen, Kaisers. *Robust multi-agent Q-learning in cooperative games with adversaries.* AAAI 2021.
- **[Papernot et al., 2016]** Papernot, McDaniel, Goodfellow. *Transferability in machine learning: from phenomena to black-box attacks using adversarial samples.* arXiv:1605.07277, 2016.
- **[Wu et al., 2021]** Wu, Guo, Wei, Xing. *Adversarial policy training against deep reinforcement learning.* USENIX Security 2021.
- **[Inkawhich et al., 2020]** Inkawhich, Chen, Li. *Snooping attacks on deep reinforcement learning.* AAMAS 2020.
- **[Rashid et al., 2018]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[Yu et al., 2022]** Yu, Velu, Vinitsky, Gao, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative multi-agent games.* NeurIPS 2022.
- **[Lv et al., 2025]** Lv, Lei, Yi. *A local information aggregation-based multiagent reinforcement learning for robot swarm dynamic task allocation.* IEEE Transactions on Neural Networks and Learning Systems 36(6):10437–10449, 2025.
- **[Park et al., 2024]** Park, Jung, Eom, Lee. *Uncertainty-aware portfolio management with risk-sensitive multiagent network.* IEEE Trans. Neural Networks Learn. Syst. 35(1):362–375, 2024.
- **[Zhang et al., 2024]** Zhang, Yue, Wang, Yoo. *Multi-agent graph-attention deep reinforcement learning for post-contingency grid emergency voltage control.* IEEE Transactions on Neural Networks and Learning Systems 35(3):3340–3350, 2024.
- **[Kos and Song, 2017]** Kos, Song. *Delving into adversarial attacks on deep policies.* arXiv:1705.06452, 2017.
