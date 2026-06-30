# 165. Robustness Evaluation of Multi-Agent Reinforcement Learning Algorithms Using GNAs

## Metadata
- **Title**: Robustness Evaluation of Multi-Agent Reinforcement Learning Algorithms Using GNAs
- **Authors**: Xusheng Zhang, Wei Zhang, Yishu Gong, Liangliang Yang, Jianyu Zhang, Zhengyu Chen, Sihong He
- **Affiliation**: Pennsylvania State University; Harvard University; Washington State University; University of Michigan; Zhejiang University; University of Connecticut (inferred from author email domains)
- **Venue**: ICLR 2023 (Tiny Papers Track)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Observation-wise and execution-wise uncertainty injected as Gaussian noise (i.i.d. noise added to the policy input/observation and to the policy output/action); measurement, model, and operation errors.
- **Method paradigm**: Empirical robustness evaluation via Gaussian noise attacks (GNAs) on a pre-trained MARL benchmark; no new robust training method proposed.
- **Keywords**: MARL, MADDPG, Gaussian noise attack (GNA), robustness evaluation, observation perturbation, execution perturbation

## TL;DR
The paper conducts the first systematic robustness evaluation of the benchmark MARL algorithm MADDPG by injecting i.i.d. Gaussian noise attacks (GNAs) into either observation (input) or execution (output) information across 8 MPE scenarios, revealing that observation-wise and execution-wise attacks induce totally different and sometimes counter-intuitive performance patterns.

## Problem & Motivation
MARL has shown strong capability in solving multi-agent sequential decision-making problems (game playing, traffic management, robotics), but uncertainties from observations and executions (measurement errors, model errors, operation errors, etc.) can undermine performance once MARL methods are deployed in the real world. Ensuring MARL algorithms are reliable, adaptable, and trustworthy requires evaluating their robustness before deployment, yet there is no systematic, universal robustness evaluation protocol for MARL algorithms. The paper addresses this gap by adopting the widely used Gaussian noise attack (GNA) approach, a universal baseline robustness evaluation for ML methods, and applying it systematically to MADDPG.

## Robustness Setting
- **Threat model / uncertainty set**: A series of i.i.d. Gaussian noise N(µ, σ) is injected into either the observation information (input of the policy) or the execution information (output/action of the policy) of well-trained MADDPG policies during testing. Parameters swept: µ ∈ {−3, −2, −1, 0.001, 0.05, 0.1, 0.25, 0.5, 1, 2, 3} and σ ∈ {3, 2, 1, 0.5, 0.25, 0.1}. Only one type of noise (observation OR execution) is applied per experiment group.
- **Setting**: cooperative / competitive / mixed (MPE scenarios cover all three); CTDE (MADDPG); evaluation is post-training (policies are pre-trained, then perturbed at test time over 10000 steps).

## Method
- Train standard MADDPG policies (CTDE + DDPG actor-critic) for agents in the Multi-Agent Particle Environments (MPE), across 8 scenarios: Mutual communication (MC), Cooperative communication (CC), Cooperative navigation (CN), Physical deception (PD), Encrypted communication (EC), Keep-away (KA), Predator-prey (PP), Complicated game (CG).
- Define the baseline as the agents' mean reward under no noise, measured over 10000 testing steps.
- Execution-wise attack: perturb the agent's action parameters by adding N(µ, σ) before the action is executed (step 1 of each iteration).
- Observation-wise attack: perturb the parameters of the observed state with N(µ, σ), so the agent perceives a different state (step 2 of each iteration).
- Sweep µ and σ over the specified grids and record agents' (and adversaries') mean rewards to characterize how the noise type and parameters affect robustness.

## Theoretical Contributions
None / mostly empirical. The paper is a tiny-paper empirical study; it provides only standard MARL/MADDPG background (Markov game tuple, deterministic policy gradient formulas) and no new theoretical guarantees.

## Experiments
- **Environment/Benchmark**: Multi-Agent Particle Environments (MPE), 8 scenarios: MC, CC, CN, PD, EC, KA, PP, CG.
- **Baselines**: MADDPG's own mean reward under no noise (the "baseline" used for comparison); no competing robustness method is compared. MADDPG is the single algorithm evaluated.
- **Evaluation metrics**: Agents' mean reward over 10000 testing steps (and adversaries' mean rewards and variance for mixed/competitive scenarios), as a function of GNA parameters µ and σ.

## Key Results
- GNA has totally different patterns for observation-wise vs. execution-wise attacks; MADDPG's behavior strongly depends on the multi-agent environment setting.
- Observation-wise GNA: in MC, CC, CN, KA, and CG there is a major decline in mean reward versus baseline, occurring even under near-baseline noise N(0, 0.1); unexpectedly, PP, EC, and PD show improvement in mean reward under GNA with certain parameters.
- Execution-wise GNA: in CN, CC, KA reward is largely insensitive to µ and robust to small σ; in PD, PP, CG, σ is the key driver — large σ even improves reward in PD, while PP and CG show an inverse σ effect (small σ raises reward, large σ lowers it).
- Counter-intuitively, in complicated environments MADDPG can achieve better performance under GNA than without attacks, providing insights that could guide future robust MARL design.

## Limitations & Future Work
- Only Gaussian noise is studied; real-world data noise sometimes follows a non-Gaussian distribution, so evaluating other types of noise/attacks is left as future work.
- Only one benchmark algorithm (MADDPG) is evaluated; no robust training method is proposed.
- Due to page limits (Tiny Paper), most experimental results are deferred to appendices.

## Relevance to Survey
This paper sits on the "observation/state perturbation" and "action/execution perturbation" lines of the robust MARL landscape, but from an evaluation rather than a method perspective: it provides a universal noise-injection benchmarking protocol (GNA) for measuring MARL robustness. It complements method-focused works on robust MARL (state uncertainty, model uncertainty, adversarial training) by highlighting the lack of systematic robustness evaluation protocols and surfacing counter-intuitive empirical phenomena that motivate the design of robust MARL algorithms.

## Related Work (verbatim excerpts from the paper)
> _[Appendix B, Related Work]_

"Since MARL recently achieved prominent performance in many decision-making applications (Dou et al., 2022c; Liu et al., 2022), researchers proposed many MARL methods, which can be generally divided into two categories: policy-based methods and value-based methods. Policy-based methods usually have an actor-critic framework, such as MADDPG (Lowe et al., 2017), COMA (Foerster & Assael, 2016) and MAAC (Iqbal & Sha, 2019). Value-based methods are usually used to solve collaborative games by factorizing the value function. For instance, VDN (Sunehag et al., 2018), QMIX (Rashid & Samvelyan, 2018), ReMIX (Mei et al., 2023a) can decompose the team value function into agent-wise value functions. Some researchers also adopt the idea of graph, such as Graph Neural Network (Li & Nabavi, 2023; Li et al., 2021; Xiao et al.; 2021; Chen et al., 2022) in developing MARL algorithms (Naderializadeh et al., 2020; Hu et al., 2021). However, without considering uncertainties from the environment, sensing, and execution, the performance of well-designed methods can be degraded when deployed in the real world (He et al., 2023b; 2020; Miao et al., 2021; Su et al., 2022; Hu et al., 2022). Adversarial training is empirically shown to improve agents' robustness to make the policies experience possible adversarial attacks (Chen et al., 2021). Pinto et al. (2017) formulate the robust RL problem as a minimax problem (Huang et al., 2023; Wu et al., 2023; Elmachtoub et al., 2023; Huang et al., 2021) then propose a method to train an agent in the presence of disturbance and obtain more robust policies. Zhang & Malkawi (2022) train the RL in real world environment with uncertainty and apply it in smart building control. There are also some robust MARL methods proposed to defend state uncertainty (Han et al., 2022; He et al., 2023a), and model uncertainty (Zhang et al., 2020). However, there is a lack of systematic and universal robustness evaluation methods and protocols for MARL algorithms."

> _[Introduction]_

"However, uncertainties from observations and executions may degrade the performance of MARL algorithms and may yield unpleasant results in real-world scenarios (Tessler et al., 2019; Zhang et al., 2021; Dou et al., 2022a;b). Different sources of uncertainties, including measurement errors, model errors, operation errors, etc., need to be considered before algorithm deployments. Thus, to ensure that the MARL algorithms are reliable, adaptable, trustworthy, and suitable in a wide range of real-world applications, it is essential to evaluate robustness of MARL algorithms before their deployment (Pang et al., 2021). However, there is a lack of systematic robustness evaluations for MARL algorithms."

> _[Introduction]_

"Researchers commonly quantify the robustness of machine learning (ML) methods by testing the performance of an ML algorithm after addicting Gaussian noise (a statistical noise with a Gaussian distribution) into the input (Pezzementi et al., 2018; Rauber et al., 2017; Turchetta et al., 2020). This approach, known as Gaussian noise attack (GNA), provides a universal baseline robustness evaluation for ML methods."

### Cited references (resolved from the paper's bibliography)
- **[Chen et al., 2021]** S. Chen, Z. Chen, D. Wang. *Adaptive adversarial training for meta reinforcement learning.* IJCNN 2021.
- **[Chen et al., 2022]** Z. Chen, T. Xiao, K. Kuang. *BA-GNN: On learning bias-aware graph neural network.* ICDE 2022.
- **[Dou et al., 2022a]** J. X. Dou, M. Jia, N. Zaslavsky, et al. *Learning more effective cell representations efficiently.* NeurIPS 2022 Workshop on Learning Meaningful Representations of Life, 2022.
- **[Dou et al., 2022b]** J. X. Dou, L. Luo, R. M. Yang. *An optimal transport approach to deep metric learning (student abstract).* AAAI 2022.
- **[Dou et al., 2022c]** J. X. Dou, A. Q. Pan, R. Bao, et al. *Sampling through the lens of sequential decision making.* arXiv:2208.08056, 2022.
- **[Elmachtoub et al., 2023]** A. Elmachtoub, V. Gupta, Y. Zhao. *Balanced off-policy evaluation for personalized pricing.* AISTATS 2023.
- **[Foerster & Assael, 2016]** J. N. Foerster, Y. Assael. *Learning to communicate with deep multi-agent reinforcement learning.* NeurIPS 2016.
- **[Han et al., 2022]** S. Han, S. Su, S. He, et al. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv:2212.02705, 2022.
- **[He et al., 2020]** S. He, L. Pepin, G. Wang, D. Zhang, F. Miao. *Data-driven distributionally robust electric vehicle balancing for mobility-on-demand systems under demand and supply uncertainties.* IROS 2020.
- **[He et al., 2023a]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning considering state uncertainties.* AI4ABM Workshop at ICLR 2023.
- **[He et al., 2023b]** S. He, Z. Zhang, S. Han, et al. *Data-driven distributionally robust electric vehicle balancing for autonomous mobility-on-demand systems under demand and supply uncertainties.* IEEE Transactions on Intelligent Transportation Systems, 2023.
- **[Hu et al., 2021]** J. Hu, Z. Xu, W. Wang, G. Qu, Y. Pang, Y. Liu. *Decentralized graph-based multi-agent reinforcement learning using reward machines.* arXiv:2110.00096, 2021.
- **[Hu et al., 2022]** J. Hu, Y. Wang, Y. Pang, Y. Liu. *Optimal maintenance scheduling under uncertainties using linear programming-enhanced reinforcement learning.* Engineering Applications of Artificial Intelligence, 2022.
- **[Huang et al., 2021]** F. Huang, X. Wu, H. Huang. *Efficient mirror descent ascent methods for nonsmooth minimax problems.* NeurIPS 2021.
- **[Huang et al., 2023]** F. Huang, X. Wu, Z. Hu. *AdaGDA: Faster adaptive gradient descent ascent methods for minimax optimization.* AISTATS 2023.
- **[Iqbal & Sha, 2019]** S. Iqbal, F. Sha. *Actor-attention-critic for multi-agent reinforcement learning.* ICML 2019.
- **[Li & Nabavi, 2023]** B. Li, S. Nabavi. *A multimodal graph neural network framework for cancer molecular subtype classification.* arXiv:2302.12838, 2023.
- **[Li et al., 2021]** B. Li, T. Wang, S. Nabavi. *Cancer molecular subtype classification by graph convolutional networks on multi-omics data.* ACM BCB 2021.
- **[Liu et al., 2022]** J. Liu, D. Wang, Q. Tian, Z. Chen. *Learn goal-conditioned policy with intrinsic motivation for deep reinforcement learning.* AAAI 2022.
- **[Lowe et al., 2017]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[Mei et al., 2023a]** Y. Mei, H. Zhou, T. Lan. *ReMIX: Regret minimization for monotonic value function factorization in multiagent reinforcement learning.* arXiv:2302.05593, 2023.
- **[Miao et al., 2021]** F. Miao, S. He, L. Pepin, et al. *Data-driven distributionally robust optimization for vehicle balancing of mobility-on-demand systems.* ACM Transactions on Cyber-Physical Systems, 2021.
- **[Naderializadeh et al., 2020]** N. Naderializadeh, F. H. Hung, S. Soleyman, D. Khosla. *Graph convolutional value decomposition in multi-agent reinforcement learning.* arXiv:2010.04740, 2020.
- **[Pang et al., 2021]** Y. Pang, S. Cheng, J. Hu, Y. Liu. *Evaluating the robustness of Bayesian neural networks against different types of attacks.* 2021.
- **[Pezzementi et al., 2018]** Z. Pezzementi, T. Tabor, S. Yim, et al. *Putting image manipulations in context: robustness testing for safe perception.* SSRR 2018.
- **[Pinto et al., 2017]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Rashid & Samvelyan, 2018]** T. Rashid, M. Samvelyan, et al. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[Rauber et al., 2017]** J. Rauber, W. Brendel, M. Bethge. *Foolbox: A python toolbox to benchmark the robustness of machine learning models.* arXiv:1707.04131, 2017.
- **[Su et al., 2022]** S. Su, Y. Li, S. He, et al. *Uncertainty quantification of collaborative detection for self-driving.* arXiv:2209.08162, 2022.
- **[Sunehag et al., 2018]** P. Sunehag, G. Lever, et al. *Value-decomposition networks for cooperative multi-agent learning based on team reward.* AAMAS 2018.
- **[Tessler et al., 2019]** C. Tessler, Y. Efroni, S. Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Turchetta et al., 2020]** M. Turchetta, A. Krause, S. Trimpe. *Robust model-free reinforcement learning with multi-objective Bayesian optimization.* ICRA 2020.
- **[Wu et al., 2023]** X. Wu, Z. Hu, H. Huang. *Decentralized Riemannian algorithm for nonconvex minimax problems.* arXiv:2302.03825, 2023.
- **[Xiao et al., 2021]** T. Xiao, Z. Chen, D. Wang, S. Wang. *Learning how to propagate messages in graph neural networks.* KDD 2021.
- **[Zhang et al., 2020]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Zhang et al., 2021]** H. Zhang, H. Chen, D. Boning, C.-J. Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv:2101.08452, 2021.
- **[Zhang & Malkawi, 2022]** W. Zhang, A. Malkawi. *Simulation-based control of natural ventilation with operable windows: Transformation from predictive control into reinforcement learning control.* Building Performance Analysis Conference and SimBuild (ASHRAE/IBPSA-USA), 2022.
