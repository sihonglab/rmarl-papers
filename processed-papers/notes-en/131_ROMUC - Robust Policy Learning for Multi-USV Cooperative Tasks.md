# 131. ROMUC: A Robust Policy Learning Method for Multi-USV Cooperative Tasks

## Metadata
- **Title**: ROMUC: A Robust Policy Learning Method for Multi-USV Cooperative Tasks
- **Authors**: Peng Li, Shaofei Chen, Ao Ma, Jing Chen (corresponding author)
- **Affiliation**: College of Intelligence Science and Technology, National University of Defense Technology, Changsha, China
- **Venue**: 2025 Asian Conference on Artificial Intelligence Technology (ACAIT) (IEEE)
- **Link/arXiv**: DOI: 10.1109/ACAIT67930.2025.11522108

## Taxonomy
- **Robustness / perturbation type targeted**: Environmental uncertainties (ocean currents, wind, reefs, exploration risk, noisy/stochastic teammate) and risks from inherent decision-making method errors (overestimation error in value-based MARL)
- **Method paradigm**: Distributional MARL (quantile / implicit quantile networks), value decomposition (QMIX-style monotonic mixing), value averaging, operator switching (Max ↔ Mellowmax), CTDE
- **Keywords**: multi-USV, distributional reinforcement learning, robustness, cooperative policies, overestimation error, value averaging

## TL;DR
ROMUC is a robust cooperative MARL method for multi-USV tasks that learns the full action-value distribution (via implicit quantile networks under a QMIX-style mixing network) to capture environmental uncertainty, and combines value averaging with Max/Mellowmax operator switching to reduce overestimation errors, jointly improving the robustness of cooperative policies.

## Problem & Motivation
In open waters, multi-USV systems face dual risks: environmental uncertainties (ocean currents, wind speeds, reefs) and uncertainties in their own cooperative policies, making robust cooperation under risk extremely challenging. Existing MARL methods for multi-USV (target tracking, path planning, pursuit) perform well but do not consider the impact of risks on the cooperative policy learning process. Perturbation-based robust approaches that add noise to actions/inputs have evident limitations: (1) they cannot fully capture the variety of environmental uncertainties, and (2) they fail to address risks caused by inherent errors of MARL methods themselves (e.g., overestimation). Prior error-reduction work (VAOS) addressed methodological-error risk but not environmental risk. ROMUC aims to handle both risk types simultaneously.

## Robustness Setting
- **Threat model / uncertainty set**: Two coupled sources of risk — (a) environmental uncertainty modeled by learning the complete action-value distribution and conditioning policies on a randomly sampled environmental risk level ω ~ U(0,1); (b) methodological error (overestimation) mitigated via value averaging and Max/Mellowmax operator switching. Test-time risk factors: an "exploration" risk (reduced exploration-rate decay, prolonged high-level exploration) and a "noise" risk (a stochastic teammate that selects random actions with 30% probability).
- **Setting**: Cooperative (with competitive Red-vs-Blue task structure); centralized training with decentralized execution (CTDE); modeled as a Dec-POMDP; online value-based MARL.

## Method
- **Distributional representation**: Replace the scalar expected Q-value with an action-value distribution Z_i (E[Z_i] = Q_i), approximated by an implicit quantile function F⁻¹_Z(s,u|ω) = f(φ(o) ⊙ ϕ(ω))_u; observation o and risk level ω are encoded by MLPs and combined by element-wise product (consistent with IQN), enabling risk-aware policies.
- **Mixing / credit assignment**: Use a QMIX-style monotonic mixing network to decompose the joint policy value distribution Z_tot into individual agents' distributions, satisfying a distributional IGM principle (arg max over the joint matches the per-agent arg max of expected distributions).
- **Value averaging**: Maintain L target policy networks and average their outputs (Z_i^ave = (1/L) Σ Z_i^l) feeding the target mixing network, and average the K target-mixing-network outputs (Z_tot^ave = (1/K) Σ Z_tot^k), reducing variance from parameter randomness (inspired by Averaged-DQN).
- **Operator switching**: When forming the TD target, alternate at a fixed frequency between the Max operator (strong exploration) and the Mellowmax operator (mitigates overestimation), per the VAOS mechanism, where mellowmax_ρ Z_i = (1/ρ) log((1/c) Σ_{a'} exp[ρ Z_i(a')]).
- **Optimization**: Train with the quantile-regression Huber loss L1 over TD loss δ = y_tot − Z_tot, plus a regularization term L2 = λ|E(Z_tot) − Σ γ^v r_{t+v}| that penalizes deviation from the discounted-return baseline to control overestimation; total objective L = L1 + L2 within the standard CTDE framework.

## Theoretical Contributions
None / mostly empirical. The paper relies on existing distributional RL, IGM, and operator definitions; no new convergence or sample-complexity results are proven.

## Experiments
- **Environment/Benchmark**: Modified MPE environment simulating two multi-USV maritime combat scenarios — Pursuit mission (three Red USVs encircle one faster Blue USV among island reefs/obstacles) and Denial mission (four Red USVs intercept two Blue USVs breaching a warning line, with obstacles, detection blind zones, and oil supply points). USVs treated as point masses with identical kinematics; collisions add a reward penalty. Evaluated under standard settings and under two risk factors (exploration risk, noise risk). Three random seeds (mean and variance curves); NVIDIA RTX 2080Ti GPU, 32-core CPU; ~10–13 h training per task.
- **Baselines**: QMIX (pymarl), VAOS, Sub-Avg (error-reduction methods), and DRIMA (risk-sensitive distributional MARL), each with default configurations.
- **Evaluation metrics**: Testing reward (return) curves under standard, exploration-risk, and noise-risk settings; plus ablations varying the number of quantiles and number of networks.

## Key Results
- Under standard settings (risk mainly from methodological errors), ROMUC achieves higher testing rewards than all baselines in both pursuit and denial tasks, stabilizing training and yielding more robust cooperative policies.
- Under exploration-risk and noise-risk settings, ROMUC attains the best performance because it is the only method that simultaneously addresses decision-making error reduction and environmental risk mitigation.
- Ablations: ROMUC outperforms VAOS under risk settings (VAOS reduces only methodological error, not environmental risk); performance is fairly stable across different numbers of quantiles, and improves moderately with more networks but at higher computational cost.

## Limitations & Future Work
- Increasing the number of networks improves performance only moderately while raising computational load and reducing algorithmic efficiency.
- No theoretical robustness guarantees; validation is limited to simulated MPE-based maritime scenarios rather than real USVs.
- Future work may address algorithmic efficiency to enhance execution capability during deployment.

## Relevance to Survey
ROMUC sits on the intersection of the "environmental/model uncertainty" robustness line and the "risk-sensitive / distributional MARL" method line, applied to a cooperative multi-agent (multi-USV) domain. It is representative of robustness-via-distributional-value-learning plus overestimation-error reduction (value averaging + operator switching), contrasting with adversarial/perturbation-injection approaches. It connects to value-decomposition MARL (QMIX, VDN), distributional RL (C51, IQN), and risk-sensitive multi-agent RL (DRIMA), and exemplifies application-driven robust MARL for safety-critical maritime cooperation.

## Related Work (verbatim excerpts from the paper)
> _[Introduction — multi-USV MARL prior work]_

"In recent years, multi-agent reinforcement learning (MARL) has shown great potential by modeling the cooperative decision-making problem of multi-USV as a partially observable Markov decision model [5]–[9], and has received widespread attention from researchers. For example, QMIX decomposes the global value function into local value functions for each agent through nonlinear mapping relationships under the assumption of monotonicity. It can learn good policies in complex environments and achieve excellent multi-agent cooperation performance in complex game scenarios such as Starcraft. The decomposition method of VDN is different from QMIX, as it uses a simple linear summation to represent the global value function, which can also play a good role in simple cooperative scenarios. Wang et al. [10] proposed an adaptive adjustment method based on MADDPG to solve the cooperative target intrusion problem in multi-USV. Li et al. [11] achieved the target tracking task of multi-USV through probabilistic data extraction and action constraint methods. Gan et al. [12] proposed a MARL method based on MA-POCA and constructed an obstacle assisted pursuit framework to improve the collaborative pursuit efﬁciency of multi-USV. Wei et al. [13] proposed a multi-USV formation path planning algorithm based on target based hierarchical reinforcement learning to solve the planning conﬂicts within the formation, and designed an improved artiﬁcial potential ﬁeld algorithm during the training process to obtain the optimal path planning and obstacle avoidance learning scheme for multi-USV."

> _[Introduction — robust MARL prior work]_

"However, the aforementioned MARL algorithms, while demonstrating excellent performance in multi-USV tasks such as target tracking and path planning, do not consider the impact of risks on the multi-agent cooperative policy learning process. To address the problem of robust multi-agent policy learning under risk conditions, some researchers have conducted studies from the perspective of robust MARL. For instance, Zhao et al. [14] proposed a MARL method with random stopping mechanisms, achieving path tracking for underactuated multi-USV formations. Literatures [15], [16] simulated output perturbations by adding noise to action outputs, enabling agents to access other states in the environment with a certain probability. Zhang et al. [17] addressed safety challenges in multi-USV mission planning by developing a method that employs deep neural networks to map the state spaces of task allocation and autonomous collision avoidance subproblems to each USV's action space, while evaluating the generated policies through corresponding reward functions. Meanwhile, Ren et al. [18] proposed a novel noise-added multi-agent proximal policy pptimization method by injecting perturbations into the input of advantage functions to enhance their generalization capability, thereby improving the exploration efﬁciency of cooperative policies for multi-USV systems."

> _[Introduction — limitations of perturbation-based robustness and motivation]_

"Nevertheless, the approach of enhancing the robustness of MARL methods by adding perturbations has evident limitations: (1) it is difﬁcult to fully consider the risks brought by various uncertainties in the environment; (2) it fails to address risks caused by inherent errors in MARL methods themselves. Previous work like the VAOS [19] method employed value averaging and operator switching to mitigate risks from methodological errors, which achieved signiﬁcant effectiveness in gaming scenarios. However, it only addressed methodological error risks without countering environmental risks. Perturbation-based approaches can only handle speciﬁc disturbances while lacking capability to address other environmental risks and risks stemming from decision-making method errors themselves."

### Cited references (resolved from the paper's bibliography)
- **[5]** Nguyen, Nguyen, Nahavandi. *Deep reinforcement learning for multiagent systems: a review of challenges, solutions, and applications.* IEEE Transactions on Cybernetics, 2020.
- **[6]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[7]** Sunehag, Lever, Gruslys, Czarnecki, Zambaldi, Jaderberg, Lanctot, Sonnerat, Leibo, Tuyls, Graepel. *Value-decomposition networks for cooperative multi-agent learning based on team reward.* AAMAS 2018.
- **[8]** Sun, Liu, Dong. *Reinforcement learning with task decomposition for cooperative multiagent systems.* IEEE Transactions on Neural Networks and Learning Systems, 2021.
- **[9]** Pan, Rashid, Peng, Huang, Whiteson. *Regularized softmax deep multi-agent Q-learning.* NeurIPS 2021.
- **[10]** Wang, Wang, Shi, Wang. *Scalable-MADDPG-based cooperative target invasion for a multi-USV system.* IEEE Transactions on Neural Networks and Learning Systems, 2024.
- **[11]** Li, Yin, Wang, Huang, Yang, Gui. *Distributed pursuit-evasion game of limited perception USV swarm based on multiagent proximal policy optimization.* IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2024.
- **[12]** Gan, Qu, Song, Yao. *Multi-USV cooperative chasing strategy based on obstacles assistance and deep reinforcement learning.* IEEE Transactions on Automation Science and Engineering, 2024.
- **[13]** Wei, Wang, Tang. *Deep hierarchical reinforcement learning based formation planning for multiple unmanned surface vehicles with experimental results.* Ocean Engineering, 2023.
- **[14]** Zhao, Ma, Hu. *USV formation and path-following control via deep reinforcement learning with random braking.* IEEE Transactions on Neural Networks and Learning Systems, 2021.
- **[15]** Eberhard, Hollenstein, Pinneri, Martius. *Pink noise is all you need: colored noise exploration in deep reinforcement learning.* ICLR 2023.
- **[16]** Raffin, Hill, Gleave, Kanervisto, Ernestus, Dormann. *Stable-Baselines3: reliable reinforcement learning implementations.* Journal of Machine Learning Research, 2021.
- **[17]** Zhang, Ren, Cui, Fu, Cong. *Multi-USV task planning method based on improved deep reinforcement learning.* IEEE Internet of Things Journal, 2024.
- **[18]** Ren, Ke (et al.). *Multi-USVs cooperative policy optimization method based on disturbed input of advantage function.* Acta Automatica Sinica, 2025.
- **[19]** Li, Chen, Yuan, Hu, Chen. *VAOS: enhancing the stability of cooperative multi-agent policy learning.* Knowledge-Based Systems, 2024.
