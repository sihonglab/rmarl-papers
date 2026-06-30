# 94. Robust Gymnasium: A Unified Modular Benchmark for Robust Reinforcement Learning

## Metadata
- **Title**: Robust Gymnasium: A Unified Modular Benchmark for Robust Reinforcement Learning
- **Authors**: Shangding Gu, Laixi Shi (equal contribution), Muning Wen, Ming Jin, Eric Mazumdar, Yuejie Chi, Adam Wierman, Costas Spanos
- **Affiliation**: University of California, Berkeley; California Institute of Technology; Shanghai Jiao Tong University; Virginia Tech; Carnegie Mellon University
- **Venue**: ICLR 2025
- **Link/arXiv**: arXiv:2502.19652v1 [cs.LG]; project website https://robust-gym.github.io/

## Taxonomy
- **Robustness / perturbation type targeted**: Unified coverage of disruptions across all stages of the agent–environment interaction — observed state perturbation, observed reward perturbation, action perturbation, and environment (transition kernel / dynamics) shift; includes random noise, adversarial attack (incl. LLM-driven), internal dynamic shift (sim-to-real), and external disturbance. Spans standard RL, safe RL, and multi-agent RL.
- **Method paradigm**: Benchmark / evaluation framework (not a new algorithm). Formalizes a unified "MDP with disruption" (Disrupted-MDP) model with three disruptor modules; benchmarks standard, robust, safe, and MARL baselines; features a two-player zero-sum adversarial-disturbance interface, including an LLM-as-adversary.
- **Keywords**: Robust RL benchmark, Disrupted-MDP, disruptors, sim-to-real, adversarial disturbance, LLM adversary, multi-agent RL

## TL;DR
Robust-Gymnasium is a unified, highly modular open-source benchmark for robust RL that injects disruptions at every stage of the agent–environment interaction (observed state, observed reward, action, environment) across 60+ tasks spanning control/robotics, safe RL, and multi-agent RL, and shows that current standard and robust RL baselines fall short even under single-stage disruptions.

## Problem & Motivation
Policies learned in idealized training environments often fail catastrophically in the real world due to the sim-to-real gap, uncertainty, noise, and malicious attacks, yet despite many RL benchmarks there is no standardized benchmark designed for comprehensively evaluating robust RL. Existing robust RL policies typically address only one specific disruption type (e.g., observation only) and are evaluated in distinct, one-off environments that can be narrow or over-fitted to the proposed algorithms; the absence of standardized benchmarks is identified as a key bottleneck to progress. An ideal benchmark should offer diverse tasks and account for uncertainty/disruptions over multiple stages of the interaction process. The only prior robustness-focused benchmark (Zouitine et al., 2024) covers six MuJoCo tasks limited to environment shifts.

## Robustness Setting
- **Threat model / uncertainty set**: A disruption module is added to a finite-horizon MDP, producing a "Disrupted-MDP" M_dis = (S, A, T, P, r, D_s(·), D_r(·), D_a(·)). Three disruptors act on different stages: observation-disruptor perturbs the observed state (s̃_t = D_s(s_t)) and observed reward (r̃_t = D_r(r_t)); action-disruptor perturbs the executed action (ã_t = D_a(a_t)); environment-disruptor changes the actual (P, r) away from the nominal (P⁰, r⁰). Disruptors support four modes — random disturbance, adversarial disturbance (viewed as a two-player zero-sum game; any algorithm, including an LLM, can act as the adversary), internal dynamic shift, and external disturbance — and operate at flexible frequencies (step-wise, episode-wise, intermittent), during training (in-training) and/or testing (post-training).
- **Setting**: cooperative MARL (MAMuJoCo), single-agent control/robotics, and safe RL; supports centralized and decentralized MARL baselines; both online training and offline-style robust evaluation; in-training vs post-training evaluation protocols.

## Method
- Introduces a unified robust RL framework that recasts uncertainty events as the behavior of three disruptor modules (observation, action, environment) inserted into the MDP interaction loop, abbreviated Disrupted-MDP; the goal is to maximize cumulative reward under the perturbed transition kernels and reward functions.
- Builds Robust-Gymnasium from eleven task bases (Gymnasium-Box2D, Gymnasium-MuJoCo, Maze, Fetch, Franka Kitchen, Dexterous Hand, Adroit, HumanoidBench, Robosuite, Safety MuJoCo, MAMuJoCo) totaling 60+ tasks, integrating disruptors of different types, modes, and frequencies; introduces new tasks such as MultiRobustDoor (Robosuite) with an adversarial arm impeding another arm.
- Constructs a robust RL task in three steps: select a task base, choose a disruptor and its operation mode(s), and set the interaction process/frequencies; supports advanced modes such as combining multiple disruptors and varying operation frequencies.
- Features an adversarial-disturbance interface in which an LLM is told the task and, given the current state and reward, directly outputs a disturbed result (e.g., a fake state) to attack the agent within a prescribed set.
- Benchmarks SOTA baselines across paradigms — Standard RL (PPO, SAC), Robust RL (OMPO, RSC, ATLA, DBC), Safe RL (PCRPO, CRPO), MARL (MAPPO, IPPO) — under in-training and post-training evaluation, using deployment-environment performance as the robust metric.

## Theoretical Contributions
None / mostly empirical. The paper contributes a unified formal model (MDP with disruption / Disrupted-MDP) and a benchmark, plus empirical analysis; it does not provide convergence, sample-complexity, or certified-robustness guarantees.

## Experiments
- **Environment/Benchmark**: Robust-Gymnasium itself — 60+ tasks from eleven task bases. Representative tasks used in the main paper include HalfCheetah-v4 (state/action/reward attacks), Ant-v5 / Hopper-v5 (internal dynamic shift: gravity, wind, torso/foot length), DoorCausal-v1 / LiftCausal-v1 (Robosuite external semantic shift), SafetyWalker2d-v4 (safe RL), MA-HalfCheetah-v4 / MA-HalfCheetah-2x3 (MAMuJoCo), and Ant-v4 (LLM-based and frequency attacks).
- **Baselines**: Standard RL — PPO, SAC; Robust RL — OMPO, RSC, ATLA, DBC; Safe RL — PCRPO, CRPO; MARL — MAPPO, IPPO.
- **Evaluation metrics**: Average episode reward (and average episode cost for safe RL), under In-training and Post-training evaluation processes; deployment-environment performance is the primary robust metric. Disturbance levels parameterized e.g. by Gaussian std (S=0.1/0.15, A=0.1/0.15) and attack frequency (e.g., every 50/100 steps). 3–5 random seeds (3 for single-agent, 5 for multi-agent).

## Key Results
- Standard RL (PPO, SAC) performance degrades quickly as disturbance level increases, especially under post-training attacks where training is unaware of disturbances (e.g., HalfCheetah-v4 state attack drops from 5751 to 901 / 616 at S=0.1 / 0.15).
- Robust RL baselines remain vulnerable: OMPO declines significantly under internal dynamic shifts (Ant-v5 gravity/wind, Hopper-v5 shape); among RSC, ATLA, DBC on Robosuite external semantic shifts, RSC is more robust but its training efficiency suffers from generating augmentation data.
- Safe RL: CRPO degrades quickly under action/cost disturbances while PCRPO is more robust; notably PCRPO's performance under disturbance can surpass its no-disturbance performance, suggesting appropriate training-time disturbances may enhance overall performance.
- MARL: both MAPPO and IPPO degrade as state/action/reward disruptions are applied to all agents; partial attacks on a subset of agents are less harmful than full attacks.
- LLM-based adversarial attacks cause a larger PPO performance drop than uniform-noise attacks, and higher-frequency attacks cause greater degradation — illustrating the potential of LLMs in robust RL research.

## Limitations & Future Work
- The benchmark itself does not yet include strong robust RL algorithms tailored to multi-stage disruptions; results mainly expose deficiencies and motivate new algorithm development rather than solving the problem.
- Not all task bases support every disruption type.
- Robust evaluation uses a limited number of seeds (3–5) due to compute cost; the authors intend to include additional seeds in future studies.
- The robust metric is usually deployment-environment performance; other formulations (risk-sensitive/CVaR, worst-case or average performance under shift) exist but are not the main focus.

## Relevance to Survey
A central infrastructure paper for the robust MARL / robust RL landscape: it provides the first unified, modular, multi-stage benchmark that standardizes evaluation across observation, reward, action, and environment disruptions, and explicitly includes a multi-agent RL track (MAMuJoCo, MAPPO/IPPO, partial-agent attacks) plus safe RL. Its Disrupted-MDP taxonomy ties together the major robust-RL threat models (state-adversarial RL, action-robust RL, robust MDP / environment shift, distributionally robust RL) and connects to the survey's themes of state-perturbation robustness, adversarial training, sim-to-real, safety, and multi-agent robustness. The LLM-as-adversary feature links robust RL to emerging LLM-based attack/defense lines.

## Related Work (verbatim excerpts from the paper)
> _[Appendix A, Related Works — "Related RL benchmarks." and "RL works involving tasks for robust evaluation."]_

"To the best of our knowledge, Zouitine et al. (2024) is the only existing benchmark designed specifically for robustness evaluations, with the same goal of this work. It introduced six continuous control tasks in Gymnasium-MuJoCo, designed to address environmental shifts. A clear lack of standardized benchmarks is present that offer a wide range of diverse tasks and account for uncertainty and disruptions over multiple stages throughout the interaction process, (not only the environment). Such a comprehensive evaluation platform is essential for the community to evaluate existing efforts and inspire new algorithms. Robust-Gymnaisum fills the gaps for robust evaluation of RL as a unified modular benchmark that supports over sixty diverse tasks in robotics and control for comprehensive evaluation, and accounting for different types of uncertainty and disruptions across multiple stages of the interaction process."

"Although not primarily focusing on building a benchmark for robust RL, there exists a lot of prior works or benchmarks that involves tasks for robust evaluation. While they typically support a few robust evaluation tasks associated with only one disruption type, which is not sufficient for comprehensive evaluations for robustness in real-world applications. Specifically, there exists a lot of benchmarks for different RL problems, such as standard RL, safe RL, multi-agent RL, offline RL, and etc. These benchmarks either don't have robust evaluation tasks, or only have a narrow range of tasks for robust evaluation (since robust evaluation is not their primary goals), such as Duan et al. (2016) support 5 tasks with robust evaluations in control. Besides, there are many existing robust RL works that involve tasks for robust evaluations, while they often evaluate one-off and a narrow range of tasks in specific domains, such as 8 tasks for robotics and control (Ding et al., 2023a), 9 robot and control tasks in StateAdvRL (Zhang et al., 2020), 5 robust RL tasks in RARL (Pinto et al., 2017), a 3D bin-packing task (Pan et al., 2023). Since their primary goal is to design robust RL algorithms, but not a platform to evaluate the algorithms."

> _[Appendix A, Related Works — "Robustness in single-agent RL."]_

"Robustness is a key principle in designing RL algorithms, as training processes are often idealized and limited in data and scenarios, while real-world environments are changeable, unpredictable, and highly diverse. An emerging body of work focuses on developing robust RL algorithms that can withstand potential uncertainties, perturbations, and attacks during real-world execution. These efforts can largely be categorized under our unified robust RL framework (Sec. 2), which formulates uncertainty events affecting the agent-environment interaction as behaviors of three types of disruptors. Our proposed Robust-Gymnasium encompasses all types of robust RL tasks within this framework, providing a flexible and comprehensive platform for evaluating and developing robust RL algorithms."

"Specifically, prior works typically involve one type of disruptors: Zhang et al. (2020; 2021b); Han et al. (2022); Qiaoben et al. (2021); Sun et al. (2021); Xiong et al. (2022) studied the uncertainty of agent's observed state, controlled by the observation-disruptor who can add restricted noise or perform adversarial attack; Tessler et al. (2019); Tan et al. (2020) considered the robustness w.r.t. the uncertainty of the action, where the action is possibly distorted by the action-disruptor abruptly or smoothly before forwarding to the environment to be executed; A large amount of prior works focus on dealing with the perturbation/shift on the environmental controlled by the environment-disruptor — includes the reward function, the dynamics, or the task itself, ranging from theory (Iyengar, 2005; Xu & Mannor, 2012; Wolff et al., 2012; Kaufman & Schaefer, 2013; Ho et al., 2018; Smirnova et al., 2019; Ho et al., 2021; Goyal & Grand-Clement, 2022; Derman & Mannor, 2020; Tamar et al., 2014; Badrinath & Kalathil, 2021) to applications (Pinto et al., 2017; Pattanaik et al., 2017; Tanabe et al., 2022; Ding et al., 2023a). Besides them, only a few works consider more complex scenarios that more than one disruptors are involved (Mandlekar et al., 2017). See Moos et al. (2022) for a recent review."

> _[Appendix A, Related Works — "Robustness in safe RL and multi-agent RL."]_

"Besides the class of standard single-agent RL, robustness in RL algorithms are ubiquitously demanded and has emerges a growing line of works for other RL problems such as partially observable Markov decision processes (POMDPs) (Cubuktepe et al., 2021), safe RL (Liu et al., 2022; Sun et al., 2024; Zhang et al., 2024; Gu et al., 2024a;c) and multi-agent RL (Vial et al., 2022; Han et al., 2022; He et al., 2023; Zhou & Liu, 2023; Zhang et al., 2023; 2021b). Additional challenges arise when combining robustness requirements with issues such as safety constraints and strategic interactions, which are often understudied and lack standardized benchmarks for evaluation. Our Robust-Gymnasium not only provides single-agent RL tasks but also encompasses a broader range of RL paradigms, including safe RL and multi-agent RL. This enables a faster and more comprehensive process for designing and evaluating robust RL algorithms across a wider array of RL tasks."

> _[Introduction — robustness motivation and disruption-stage prior work]_

"Disruptions or interventions can occur at various stages of the agent-environment interaction, affecting the agent's observed state (Zhang et al., 2020; 2021b; Han et al., 2022; Sun et al., 2021; Xiong et al., 2022), observed reward (Xu & Mannor, 2006), action (Huang et al., 2017), and the environment (transition kernel) (Iyengar, 2005; Pinto et al., 2017) and existing robust RL policies are vulnerable to such real-world failures (Mandlekar et al., 2017). This vulnerability is, in part, a result of the fact that policies are designed to address only one specific type of disruption (e.g., over the observed state), among other technical limitations (Ding et al., 2024). More critically, robust RL policies are often evaluated in distinct, one-off environments that can be narrow or over-fitted to the proposed algorithms. The absence of standardized benchmarks is a key bottleneck to progress in robust RL."

### Cited references (resolved from the paper's bibliography)
- **[Badrinath & Kalathil, 2021]** Badrinath, Kalathil. *Robust reinforcement learning using least squares policy iteration with provable performance guarantees.* ICML 2021.
- **[Cubuktepe et al., 2021]** Cubuktepe, Jansen, Junges, Marandi, Suilen, Topcu. *Robust finite-state controllers for uncertain POMDPs.* AAAI 2021.
- **[Derman & Mannor, 2020]** Derman, Mannor. *Distributional robustness and regularization in reinforcement learning.* arXiv 2020.
- **[Ding et al., 2023a]** Ding, Shi, Chi, Zhao. *Seeing is not believing: Robust reinforcement learning against spurious correlation.* NeurIPS 2023.
- **[Ding et al., 2024]** Ding, Shi, Chi, Zhao. *Seeing is not believing: Robust reinforcement learning against spurious correlation.* Advances in Neural Information Processing Systems 36, 2024.
- **[Duan et al., 2016]** Duan, Chen, Houthooft, Schulman, Abbeel. *Benchmarking deep reinforcement learning for continuous control.* ICML 2016.
- **[Goyal & Grand-Clement, 2022]** Goyal, Grand-Clement. *Robust Markov decision processes: Beyond rectangularity.* Mathematics of Operations Research 2022.
- **[Gu et al., 2024a]** Gu, Liu, Kshirsagar, Chen, Peters, Knoll. *RoSCom: Robust safe reinforcement learning on stochastic constraint manifolds.* IEEE Transactions on Automation Science and Engineering 2024.
- **[Gu et al., 2024c]** Gu, Yang, Du, Chen, Walter, Wang, Knoll. *A review of safe reinforcement learning: Methods, theories and applications.* IEEE TPAMI 2024.
- **[Han et al., 2022]** Han, Su, He, Han, Yang, Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv 2022.
- **[He et al., 2023]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* TMLR 2023.
- **[Ho et al., 2018]** Ho, Petrik, Wiesemann. *Fast Bellman updates for robust MDPs.* ICML 2018.
- **[Ho et al., 2021]** Ho, Petrik, Wiesemann. *Partial policy iteration for L1-robust Markov decision processes.* JMLR 2021.
- **[Huang et al., 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[Iyengar, 2005]** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research 2005.
- **[Kaufman & Schaefer, 2013]** Kaufman, Schaefer. *Robust modified policy iteration.* INFORMS Journal on Computing 2013.
- **[Liu et al., 2022]** Liu, Guo, Cen, Zhang, Tan, Li, Zhao. *On the robustness of safe reinforcement learning under observational perturbations.* arXiv 2022.
- **[Mandlekar et al., 2017]** Mandlekar, Zhu, Garg, Fei-Fei, Savarese. *Adversarially robust policy learning: Active construction of physically-plausible perturbations.* IROS 2017.
- **[Moos et al., 2022]** Moos, Hansel, Abdulsamad, Stark, Clever, Peters. *Robust reinforcement learning: A review of foundations and recent advances.* Machine Learning and Knowledge Extraction 2022.
- **[Pan et al., 2023]** Pan, Chen, Lin. *Adjustable robust reinforcement learning for online 3D bin packing.* arXiv 2023.
- **[Pattanaik et al., 2017]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* arXiv 2017.
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Qiaoben et al., 2021]** Qiaoben, Zhou, Ying, Zhu. *Strategically-timed state-observation attacks on deep reinforcement learning agents.* ICML 2021 Workshop on Adversarial Machine Learning.
- **[Smirnova et al., 2019]** Smirnova, Dohmatob, Mary. *Distributionally robust reinforcement learning.* arXiv 2019.
- **[Sun et al., 2021]** Sun, Liu, Zhao, Yao, Jui, Kong. *Exploring the training robustness of distributional reinforcement learning against noisy state observations.* arXiv 2021.
- **[Sun et al., 2024]** Sun, He, Miao, Zou. *Constrained reinforcement learning under model mismatch.* arXiv 2024.
- **[Tamar et al., 2014]** Tamar, Mannor, Xu. *Scaling up robust MDPs using function approximation.* ICML 2014.
- **[Tan et al., 2020]** Tan, Esfandiari, Lee, Sarkar. *Robustifying reinforcement learning agents via action space adversarial training.* ACC 2020.
- **[Tanabe et al., 2022]** Tanabe, Sato, Fukuchi, Sakuma, Akimoto. *Max-min off-policy actor-critic method focusing on worst-case robustness to model misspecification.* NeurIPS 2022.
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Vial et al., 2022]** Vial, Shakkottai, Srikant. *Robust multi-agent bandits over undirected graphs.* Proceedings of the ACM on Measurement and Analysis of Computing Systems 2022.
- **[Wolff et al., 2012]** Wolff, Topcu, Murray. *Robust control of uncertain Markov decision processes with temporal logic specifications.* IEEE CDC 2012.
- **[Xiong et al., 2022]** Xiong, Eappen, Zhu, Jagannathan. *Defending observation attacks in deep reinforcement learning via detection and denoising.* arXiv 2022.
- **[Xu & Mannor, 2006]** Xu, Mannor. *The robustness-performance tradeoff in Markov decision processes.* NeurIPS 2006.
- **[Xu & Mannor, 2012]** Xu, Mannor. *Distributionally robust Markov decision processes.* Mathematics of Operations Research 2012.
- **[Zhang et al., 2020]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Zhang et al., 2021b]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[Zhang et al., 2023]** Zhang, Sun, Huang, Miao. *Safe and robust multi-agent reinforcement learning for connected autonomous vehicles under state perturbations.* arXiv 2023.
- **[Zhang et al., 2024]** Zhang, Panaganti, Shi, Sui, Wierman, Yue. *Distributionally robust constrained reinforcement learning under strong duality.* arXiv 2024.
- **[Zhou & Liu, 2023]** Zhou, Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* arXiv 2023.
- **[Zouitine et al., 2024]** Zouitine, Bertoin, Clavier, Geist, Rachelson. *RRLS: Robust reinforcement learning suite.* arXiv 2024.
