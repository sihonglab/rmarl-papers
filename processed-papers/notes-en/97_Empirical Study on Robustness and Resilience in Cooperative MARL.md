# 97. Empirical Study on Robustness and Resilience in Cooperative Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Empirical Study on Robustness and Resilience in Cooperative Multi-Agent Reinforcement Learning
- **Authors**: Simin Li, Zihao Mao, Hanxiao Li, Zonglei Jing, Zhuohang Bian, Jun Guo, Li Wang, et al.; corresponding authors Yaodong Yang, Weifeng Lv, Xianglong Liu
- **Affiliation**: State Key Laboratory of Complex & Critical Software Environment, Beihang University, China; Zhongguancun Laboratory; Institute of Artificial Intelligence, Peking University; Institute of Data Space, Hefei Comprehensive National Science Center; Nanyang Technological University, Singapore
- **Venue**: NeurIPS 2025
- **Link/arXiv**: arXiv:2510.11824v2 [cs.MA]; code at https://github.com/BUAA-TrustworthyMARL/adv_marl_benchmark

## Taxonomy
- **Robustness / perturbation type targeted**: Observation uncertainties (Gaussian noise, greedy white-box attacks, learned optimal attacks), action uncertainties (random / greedy worst-case / learned optimal policy deviations), and environment uncertainties (variations in environmental hyperparameters such as mass, velocity); perturbations applied either to all agents or to a single agent. Also studies resilience (recovery from disruptions).
- **Method paradigm**: Large-scale empirical benchmark / study (not a new algorithm); evaluation of cooperation, robustness, and resilience; hyperparameter (implementation-choice) analysis; statistical analysis (Pearson correlation, ANOVA, paired t-tests, OLS regression).
- **Keywords**: Trustworthy MARL, robustness, resilience, cooperative MARL, hyperparameters, empirical study

## TL;DR
A large-scale empirical study (over 82,620 experiments across 4 real-world environments, 13 uncertainty types, and 15 hyperparameters) that formally distinguishes robustness from resilience in cooperative MARL and shows that hyperparameter (implementation-choice) tuning alone — favoring early stopping, higher critic learning rates, and Leaky ReLU while avoiding parameter sharing, GAE, and PopArt — can substantially improve cooperation, robustness, and resilience.

## Problem & Motivation
Cooperative MARL is typically tuned in idealized simulators to maximize cooperative performance, but policies tuned this way often fail under real-world uncertainties (observation errors, action perturbations, environmental unpredictability). The paper argues for understanding two complementary properties: robustness (stability under uncertainties) and resilience (the ability to recover from disruptions). Resilience is extensively studied in control theory, ecology, and economics, but is largely overlooked in MARL, where the literature frequently conflates resilience with robustness. A second gap is the under-appreciated role of hyperparameters: as in single-agent RL where hyperparameters drive much of the empirical difference between algorithms, careful implementation choices may matter more than the algorithm itself, yet their effect on robustness and resilience is largely unexplored.

## Robustness Setting
- **Threat model / uncertainty set**: An uncertainty set U is defined over the decision process, where each u ∈ U is a perturbation on observation, action, or environment. Observation uncertainties: Gaussian noise, greedy white-box gradient-based attacks, and learned optimal (MARL-based) attacks; action uncertainties modeled as επ̂ + (1−ε)π with perturbed policy π̂ (random / greedy worst-case / learned optimal); environment uncertainties sample 50 rollouts uniformly over environmental hyperparameters and report worst case. Perturbations are applied to all agents with a small budget (ε = 0.1) or to a single agent with a large budget (ε = 0.2). Robustness is the expected return under uncertainty; resilience is the expected return when an episode is restarted from a perturbed state s_u reached after an uncertainty, then evolving without further uncertainty.
- **Setting**: cooperative; modeled as a Dec-POMDP; CTDE-style continuous-control MARL algorithms; online; evaluation only (fixed cooperative policies are stress-tested, no robust retraining for the core study).

## Method
- Formulates cooperative MARL as a Dec-POMDP and formally defines robustness (expected return under the uncertainty distribution) and resilience (expected return when recovering from a perturbed initial state distribution ρ_u after an uncertainty event), explicitly separating the two concepts.
- Runs a benchmark of 5 (seeds) × 27 (uncertainty settings: 1 cooperative baseline + 13 robustness + 13 resilience) × 18 (tasks) × 34 (implementations) = 82,620 experiments, using ~230K GPU hours (GTX 4090).
- Evaluates three continuous-control MARL backbones — MADDPG, MAPPO, HAPPO — varying one hyperparameter at a time (15 general/algorithm-specific hyperparameters → 34 implementations) to isolate each hyperparameter's effect on cooperation, robustness, and resilience.
- Analyzes results with Pearson correlations, one-/two-way ANOVA, paired t-tests, and OLS regression; then selects, per task, the best hyperparameter set maximizing combined cooperation + robustness + resilience, and tests generalization on the robust MARL method ERNIE across backbones.

## Theoretical Contributions
None / mostly empirical. The paper's contribution is a formal definitional separation of robustness vs. resilience plus a large empirical study; it cites two-timescale stochastic-approximation and maximum-entropy-RL theory to interpret findings rather than proving new results.

## Experiments
- **Environment/Benchmark**: Four real-world environments (18 tasks): Dexterous Hand Manipulation (DexHand, Isaac Gym), Quadrotor Swarm Control (Quad, OpenAI Gym), Intelligent Traffic Control (Traffic, SUMO), and Active Voltage Control (Voltage, IEEE-standard power grid).
- **Baselines**: MARL backbones MADDPG, MAPPO, HAPPO under default vs. tuned hyperparameters; robust MARL method ERNIE used to test generalization; comparisons against standard codebase defaults (e.g., EPyMARL/MAPPO save-at-final-step).
- **Evaluation metrics**: Episode reward; cooperation, robustness, and resilience (with normalization across tasks); percentage degradation/improvement; statistical significance (Pearson r, ANOVA F, paired-t).

## Key Results
- Optimizing cooperation improves robustness (Pearson r = 0.85, p < .001) and resilience (r = 0.76, p < .001) under mild uncertainty, but this correlation weakens linearly as attack severity increases. MADDPG is more robust/resilient to action uncertainties, while MAPPO and HAPPO are better under observation uncertainties.
- Robustness and resilience do not generalize across uncertainty modalities (observation vs. action vs. environment; ANOVA significant) or across agent scopes (single-agent vs. all-agent perturbations; ANOVA significant) — e.g., EIR-MAPPO trained against action uncertainties stays vulnerable to observation uncertainties, and M3DDPG robust to uniform small perturbations fails under large single-agent perturbations.
- Hyperparameter tuning alone yields average improvements of 52.60% (cooperation), 34.78% (robustness), 60.34% (resilience). Helpful: early stopping, critic LR > actor LR, Leaky ReLU, exploration (for MAPPO/HAPPO), parameter sharing only for homogeneous agents. Harmful in this benchmark: GAE, PopArt, and (often) parameter sharing. The same hyperparameter set generalizes to the robust method ERNIE, improving cooperation 89.43%, robustness 65.83%, resilience 82.96%.

## Limitations & Future Work
- The study focuses on policy-gradient-based MARL algorithms (MADDPG, MAPPO, HAPPO) because many environments require continuous control; value-based methods are not covered. The authors note this can be mitigated by integrating new algorithms into their codebase, which supports custom environments and algorithm integration.
- Findings are reported as statistically significant general trends that may not hold in every individual case.

## Relevance to Survey
A benchmark/empirical-study anchor for the robust MARL survey: it consolidates the field's uncertainty taxonomy (observation/action/environment, single- vs. all-agent), and uniquely introduces resilience as a property distinct from robustness, connecting MARL to control-theoretic, ecological, and economic notions of resilience. It links to adversarial-attack lines (observation attacks [Zhang et al.], adversarial policies, learned optimal attacks), action-robust and minimax adversarial MARL (M3DDPG, EIR-MAPPO, ERNIE), environment-uncertainty / robust-MDP lines, and robustness-benchmark efforts (RRLS, Robust Gymnasium). Its message that implementation choices can dominate algorithmic differences is a methodological caution for the whole robust-MARL literature.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Uncertainties in RL and MARL"]_

"Robustness against uncertainties has been extensively studied within the framework of robust RL and MARL, as summarized in [28]. In reinforcement learning, uncertainties in deployment are typically categorized into state [29, 30, 31], action [32], and environment uncertainties [33, 18]. MARL follows a similar taxonomy but incorporates the multi-agent dynamic. For observation uncertainties, noise can be introduced to each agent [34, 15, 35] or applied to specific agents [14]. Action uncertainties often arise when one or more agents deviate from their optimal policy [16, 36, 37, 17]. Environment uncertainties in MARL are typically analogous to those seen in single-agent RL [38, 19]. The primary focus of robust RL and MARL is to make algorithms robust against the worst-case adversaries chosen in the uncertainty set. In our paper, we select a set of representative methods derived from these studies for robustness evaluation. For resilience, the MARL literature often overlook its distinct role from robustness, using the term resilience and robustness interchangeably [25, 39, 26, 40]. In this paper, we draw in fields such as control theory [21], ecology [22], and economics [23] to formally define resilience in MARL."

> _[Section 2, Related Work — "The Importance of hyperparameters"]_

"It is a well-known fact that implementation matters for RL and MARL. In RL, [27] highlighted the surprising finding that variations in performance among RL algorithms often stem from hyperparameters rather than fundamental algorithmic differences. This notion was further explored by [41], who provided a comprehensive set of recommendations for RL implementation through large-scale experimentation. In MARL, Epymarl [42] introduced the first extensive benchmark suite, while MAPPO [3] significantly boosted Epymarl's performance by simply optimizing the implementation. Similarly, Pymarlv2 [43] demonstrated that state-of-the-art results in the SMAC environment can be achieved by fine-tuning QMIX [2]. [24] and [44] offer preliminary evaluations of RL/MARL under uncertainty, but are limited to simple simulation experiments in a small scale. The works most similar to ours are RRLS [45] and Robust Gymnasium [46], which provide integrated codebases for evaluating the robustness of single- and multi-agent RL. Our work differs by presenting the relations between cooperation, robustness and resilience under multiple real world environments, algorithms, and diverse uncertainties based on over 82,620 experiments."

> _[Section 3, Robustness and Resilience — definitions of Robustness and Resilience]_

"Robustness has been a central concept in control systems, which refers to the stability of the algorithm under uncertainties [48]. In MARL, the study of robustness relies on defining an uncertainty set U in the decision process. During the deployment of MARL policies, such uncertainty set U can be defined as a distribution over uncertainty realizations, where each u ∈ U represents a perturbation on observation [14], action [34, 40] or environments [38]."

"When uncertainties cannot be handled by algorithms alone, robustness alone may become insufficient. In such cases, resilience—i.e., the ability of systems to recover from external shocks [49]—becomes crucial. As illustrated in Fig. 2, resilience and robustness are complementary: while robustness allows a system to maintain functionality under small perturbations, resilience ensures recovery when perturbations exceed the limits of robustness [50]. This complementary relationship has been extensively explored across various fields, including control theory [21], ecology [22], economics [23], and complex networks [51]."

"Despite this, the MARL literature often conflates resilience with robustness, overlooking their distinct roles. For instance, [24] frame resilience as an inherent feature of robustness, while [25, 39] label their approaches as resilient MARL but ground their methodologies in robust RL. Similarly, [26] and [40] use the terms resilience and robustness interchangeably, failing to distinguish between the two."

### Cited references (resolved from the paper's bibliography)
- **[2]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[3]** Yu, Velu, Vinitsky, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative, multi-agent games.* arXiv 2021.
- **[14]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[15]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* arXiv 2023.
- **[16]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv 2019.
- **[17]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game.* arXiv 2023.
- **[18]** Xie, Sodhani, Finn, Pineau, Zhang. *Robust policy learning over multiple uncertainty sets.* ICML 2022.
- **[19]** Shi, Mazumdar, Chi, Wierman. *Sample-efficient robust multi-agent reinforcement learning in the face of environmental uncertainty.* arXiv 2024.
- **[21]** Zhu, Başar. *Robust and resilient control design for cyber-physical systems with an application to power systems.* IEEE CDC-ECC 2011.
- **[22]** Holling et al. *Resilience and stability of ecological systems.* 1973.
- **[23]** Di Caro, Fratesi. *Regional determinants of economic resilience.* The Annals of Regional Science 2018.
- **[24]** Behzadan, Hsu. *RL-based method for benchmarking the adversarial resilience and robustness of deep reinforcement learning policies.* SAFECOMP 2019 Workshops (Springer).
- **[25]** Phan, Gabor, Sedlmeier, Ritz, Kempter, Klein, Sauer, Schmid, Wieghardt, Zeller, et al. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
- **[26]** Zeng, Qiu, Sun. *Resilience enhancement of multi-agent reinforcement learning-based demand response against adversarial attacks.* Applied Energy 2022.
- **[27]** Engstrom, Ilyas, Santurkar, Tsipras, Janoos, Rudolph, Madry. *Implementation matters in deep policy gradients: A case study on PPO and TRPO.* arXiv 2020.
- **[28]** Ilahi, Usama, Qadir, Janjua, Al-Fuqaha, Hoang, Niyato. *Challenges and countermeasures for adversarial attacks on deep reinforcement learning.* IEEE Transactions on Artificial Intelligence 2021.
- **[29]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[30]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[31]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv 2021.
- **[32]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[33]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[34]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[35]** Sun, Kim, How. *ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* ICRA 2022.
- **[36]** Nisioti, Bloembergen, Kaisers. *Robust multi-agent Q-learning in cooperative games with adversaries.* AAAI 2021.
- **[37]** Yuan, Zhang, Xue, Yin, Chen, Guan, Li, Qian, Yu. *Robust multi-agent coordination via evolutionary generation of auxiliary adversarial attackers.* AAAI 2023.
- **[38]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[39]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[40]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game.* arXiv 2023.
- **[41]** Andrychowicz, Raichuk, Stańczyk, Orsini, Girgin, Marinier, Hussenot, Geist, Pietquin, Michalski, et al. *What matters in on-policy reinforcement learning? A large-scale empirical study.* arXiv 2020.
- **[42]** Papoudakis, Christianos, Schäfer, Albrecht. *Benchmarking multi-agent deep reinforcement learning algorithms in cooperative tasks.* arXiv 2020.
- **[43]** Hu, Jiang, Harding, Wu, Liao. *Rethinking the implementation tricks and monotonicity constraint in cooperative multi-agent reinforcement learning.* arXiv 2021.
- **[44]** Guo, Chen, Hao, Yin, Yu, Li. *Towards comprehensive testing on the robustness of cooperative multi-agent reinforcement learning.* CVPR (Workshops) 2022.
- **[45]** Zouitine, Bertoin, Clavier, Geist, Rachelson. *RRLS: Robust reinforcement learning suite.* arXiv 2024.
- **[46]** Gu, Shi, Wen, Jin, Mazumdar, Chi, Wierman, Spanos. *Robust Gymnasium: A unified modular benchmark for robust reinforcement learning.* GitHub 2024.
- **[48]** Gu, Petkov, Konstantinov. *Robust control design with MATLAB.* Springer 2005.
- **[49]** Capano, Woo. *Resilience and robustness in policy design: A critical appraisal.* Policy Sciences 2017.
- **[50]** Zhu, Başar. *Disentangling resilience from robustness: Contextual dualism, interactionism, and game-theoretic paradigms.* IEEE Control Systems Magazine 2024.
- **[51]** Artime, Grassia, De Domenico, Gleeson, Makse, Mangioni, Perc, Radicchi. *Robustness and resilience of complex networks.* Nature Reviews Physics 2024.
