# 51. Adversarial Attacks on Multiagent Deep Reinforcement Learning Models in Continuous Action Space

## Metadata
- **Title**: Adversarial Attacks on Multiagent Deep Reinforcement Learning Models in Continuous Action Space
- **Authors**: Ziyuan Zhou, Guanjun Liu, Weiran Guo, MengChu Zhou
- **Affiliation**: Department of Computer Science, Tongji University, Shanghai, China; Macao Institute of Systems Engineering and Collaborative Laboratory for Intelligent Science and Systems, Macau University of Science and Technology, Macau, China; Helen and John C. Hartmann Department of Electrical and Computer Engineering, New Jersey Institute of Technology, Newark, NJ, USA
- **Venue**: IEEE Transactions on Systems, Man, and Cybernetics: Systems, Vol. 54, No. 12, December 2024
- **Link/arXiv**: DOI 10.1109/TSMC.2024.3454118; code at https://github.com/zhou-ziyuan/RTCA

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation (adversarial attacks); dynamic selection of "critical agents" as victims in cooperative MADRL
- **Method paradigm**: Adversarial attack framework; worst-case joint action search via gradient information (GI/PGD) and differential evolution (DE); SARSA-based joint action-value learning; targeted attacks (PGD, SGLD)
- **Keywords**: Adversarial attacks, continuous action space, industry 5.0, MADRL, critical agents

## TL;DR
The paper proposes AMCA, an adversarial attack framework for MADRL in continuous action space that dynamically identifies time-varying "critical agents" via gradient information or differential evolution, learns a joint action-value function with SARSA to guide the search, and then perturbs only those few agents' observations with targeted attacks, achieving stronger disruption of team cooperation than existing methods while attacking as few agents as possible.

## Problem & Motivation
MADRL models (e.g., MADDPG, FACMAC) are sensitive to perturbations in agent states arising from sensor errors or malicious attacks, which can disrupt cooperative team policies and cause severe consequences in industrial applications. Existing attacks on MADRL assume a fixed set of victim agents: methods that model the adversary as a stochastic game require all/known agents to be victims, and methods that select one victim during training must retrain when the victim changes. The paper argues that the contribution of each agent to the team differs over time, so the key open problems are (1) selecting which "critical agents" to designate as victims, (2) guiding worst-case joint actions when the victim set is uncertain, and (3) evaluating the influence of suboptimal actions on the team policy during testing when the centralized critic / joint action-value function is unavailable or trained only under optimal actions.

## Robustness Setting
- **Threat model / uncertainty set**: The adversary perturbs the observations (states) of a dynamically selected subset of victim agents. Perturbation is bounded by an ℓ∞ norm (magnitudes 0.1, 0.5, 0.02 in CMUE, MAMuJoCo, MPE respectively). The number/identity of victims M can change at every time step. The goal is to make victim agents take worst-case joint actions that minimize the team's discounted cumulative reward, while perturbing as few agents as possible to remain stealthy. Formalized via state-adversarial stochastic games (SASGs) and agent state adversarial Dec-POMDPs (SADPs).
- **Setting**: cooperative; CTDE (centralized training, decentralized execution); attack/evaluation operates at test/execution time without pretraining the adversary.

## Method
- **AMCA framework (two steps)**: Step 1 selects critical agents and their worst-case joint actions; Step 2 executes a targeted attack that generates observation perturbations from a novel loss function.
- **GI-based selection (Algorithm 1)**: When the adversary has access to the joint action-value function Qjt (FACMAC), it computes worst-case joint actions by U1-step PGD descent on Qjt (Eq. 13), then solves a combinatorial optimization selecting M of N agents to minimize Qjt (Eq. 12).
- **DE-based selection (Algorithm 2)**: Uses differential evolution (population 400/200, scaling F=0.5, crossover) to jointly search the critical-agent indices and their worst-case actions in one step; requires only inputs/outputs of Qjt (black-box), and adapts to a variable number of victims for real-time attacks.
- **SARSA-based joint action-value function SJAV (Algorithm 3)**: Trains a neural network ˜Qjt(s,a) during execution using an ε-greedy policy to explore suboptimal trajectories, minimizing a TD loss (Eq. 15), so that the value of suboptimal joint actions is estimated correctly (the FACMAC critic / MADDPG critic cannot do this); convergence is proved under GLIE.
- **Targeted attack / adversarial observation generation (Algorithm 4)**: Minimizes a loss Lsa (Eq. 16) trading off (1−β) pushing the policy toward target action âi and β pushing it away from the clean action, solved by U2-step PGD (Eq. 17) or SGLD (Eq. 18). Combining {GI, DE} × {PGD, SGLD} gives four variants: AMCA_GP, AMCA_GS, AMCA_DP, AMCA_DS.

## Theoretical Contributions
- **Theorem 1**: If the ε-greedy policy satisfies GLIE (greedy in the limit with infinite exploration), the SARSA-learned joint action-value function ˜Qjt converges (proof via stochastic-approximation Lemma 1 in the Appendix).
- **Theorem 2**: Derives the training time complexity of SJAV and the run-time complexity of Algorithms 1 and 2, and of the four AMCA variants.

## Experiments
- **Environment/Benchmark**: Collaborative multi-UAV environment (CMUE / CUME, industry-related cooperative transport with two UAVs); multiagent MuJoCo (MAMuJoCo) with two-agent Humanoid and four-agent Ant; multiagent particle environments (MPE) with continuous predator-prey 3a (3 agents, 1 prey) and 6a (6 agents, 2 prey) scenarios. Victims trained by MADDPG and FACMAC for two million steps.
- **Baselines**: Random Noise (RN); FGSM, PGD, SGLD (untargeted gradient-based, single-policy); ATLA (adversary trained with PPO/MAPPO, all agents victims); PAAD (two-step director-actor adversary, requires known/fixed victims). Also attacks on defense policies FACMAC_ATLA and FACMAC_PAAD.
- **Evaluation metrics**: Average team cumulative reward (lower is better attack); in CMUE also successful rate (SR), too far rate (TFR), collide rate (CR); plus ablation on ˜Qjt vs mixing network, transferability of ˜Qjt across MADRL paradigms, scalability with victim count, and CPU/run time/memory profiling.

## Key Results
- AMCA outperforms the benchmark attacks across most scenarios; the DE+PGD variant (AMCA_DP) and DE/PGD-based variants are consistently the strongest, while AMCA can disrupt cooperation by attacking only one or two agents, confirming that agents' contributions to the team differ and that selecting critical agents beats random selection.
- RN and untargeted gradient methods (FGSM, PGD, SGLD) are weak and can even improve the victim team's reward; ATLA performs poorly due to the exponentially large joint observation space for MAPPO; PAAD requires retraining when victims change.
- On defense policies, FACMAC_ATLA and FACMAC_PAAD resist random/state perturbations but perform poorly under AMCA and suffer severe clean-performance degradation, showing existing adversarial-training defenses are ineffective against critical-agent attacks.
- ˜Qjt (SJAV) is effective for evaluating an agent's impact on team reward and shows favorable transferability between FACMAC and MADDPG; AMCA scales with victim count and resource consumption is not significantly affected by the number of victims.

## Limitations & Future Work
- AMCA is less consistently superior against MADDPG (e.g., CMUE with two victims) because MADDPG's per-agent centralized critic makes SJAV a poorer fit than for FACMAC.
- The proposed defense critique notes existing adversarial training degrades clean performance and ignores agent importance; the authors plan more general and robust training methods.
- Future work: investigate loss functions and optimization methods for targeted attacks in continuous action space; develop adaptive defenses against AMCA; bridge the sim-to-real gap (via meta-learning or domain randomization) so perturbations apply to real UAV/autonomous-driving sensors without causing significant real-world harm.

## Relevance to Survey
This paper sits on the "state/observation adversarial attack" line of robust MARL, specifically attacking cooperative CTDE MADRL (MADDPG, FACMAC) in continuous action space. Its core novelty—dynamically selecting time-varying critical agents as victims rather than a fixed victim set—connects the adversarial-attack literature (SASG, SADP, PAAD, ATLA) with robustness testing and the broader robust-MARL theme: it is an attacker/stress-test counterpart to defensive robust MARL methods (e.g., robust training against state perturbations) and motivates more robust training and defense design.

## Related Work (verbatim excerpts from the paper)

> _[Section I, Introduction]_

"However, recent studies have shown that the models trained using MADRL are sensitive to the perturbation in agent states [20], [21], [22], [23], [24]. These perturbations, stemming from sensor errors or deliberate malicious attacks, can result in severe consequences. Importantly, perturbations in the states of certain agents have the potential not only to misguide individual decisions but also to disrupt the cooperative policies in a team. Attacks on MADRL-trained models are harmful, but they are crucial to validate the reliability of industrial applications in the face of unforeseen perturbations."

> _[Section I, Introduction]_

"There are some related studies for adversarial attacks on single-agent deep reinforcement learning (SADRL) models [25], [26], [27], [28], [29], [30], [31], which do not consider which agents should be selected as victims. In the context of adversarial attacks on MADRL models, it has been demonstrated that the adversary can be effectively modeled as a stochastic game (SG). The existence of the optimal adversary is established in [23]. However, they assume that the victim agent set is ﬁxed. It cannot be modeled as SG when such a set changes. Guo et al. [20], [22], [24] only focus on the case of ﬁxed victims. As a primary focus of our work, the initial challenge we aim to address is the selection of critical agents designated as victims."

> _[Section II-A, Related Work — Adversarial Attacks on SADRL Models]_

"In the context of adversarial attacks on SADRL models, the studies [25] and [26] utilize gradient-based adversary attacks like deep neural network (DNN) to generate adversarial-state perturbations. However, they only mislead an agent to do a wrong action and may not lead to the minimal expected reward. In [27], the adversary is modeled as a Markov decision process (MDP), and DRL is employed to address it, which can work well in low-dimension state space. To extend this method to high-dimension one, the work [28] proposes a two-step attack framework consisting of a director component for advising the worst-case action and an actor component for generating perturbations based on the guidance of the director. These studies do not consider which agents should be selected as victims which is important in adversarial attacks on MADRL models."

> _[Section II-B, Related Work — Adversarial Attacks on MADRL Models]_

"In the ﬁeld of adversarial attacks on MADRL models, Lin et al. [22] used a two-step framework like [28] to generate adversarial observations, where an agent is selected as a victim during the training process. When the victim changes, the model has to retrain. Studies [20], [23], [33] model the adversarial attacks as an SG and use MADRL to solve it, but they view all agents as victims. In this work, we propose an adversarial attack framework to ﬁnd deﬁciencies in MADRL models by generating perturbation with a high impact on the team while interfering with the minimum number of agents. Building upon our previous work [32], where we introduced a framework known as robustness testing based on critical agents (RTCAs) for MADRL in discrete action space, this work extends the framework to the case of continuous one."

> _[Section III-C, SASG]_

"The properties of SASG, such as the existence and contraction of the joint optimal adversarial perturbation, are discussed in [23]. It is highlighted that the problem of solving the joint optimal adversarial perturbation can be modeled as an SG well-addressed by MADRL. Consequently, studies [22], [33], [37] have solved this problem via MADRL. However, during the training process, victim agents are assumed to be ﬁxed. If the set of victims changes, retraining is required for MADRL models. Addressing this limitation is the focus of our work."

### Cited references (resolved from the paper's bibliography)
- **[20]** J. Guo, Y. Chen, Y. Hao, Z. Yin, Y. Yu, S. Li. *Towards comprehensive testing on the robustness of cooperative multi-agent reinforcement learning.* IEEE/CVF CVPR Workshops 2022.
- **[21]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research (TMLR) 2023.
- **[22]** J. Lin, K. Dzeparoska, S. Q. Zhang, A. Leon-Garcia, N. Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[23]** Z. Zhou, G. Liu, M. Zhou. *A robust mean-field actor-critic reinforcement learning against adversarial perturbations on agent states.* IEEE Transactions on Neural Networks and Learning Systems (early access) 2023.
- **[24]** W. Guo, G. Liu, Z. Zhou, L. Wang, J. Wang. *Enhancing the robustness of QMIX against state-adversarial attacks.* Neurocomputing 2024.
- **[25]** S. Huang, N. Papernot, I. Goodfellow, Y. Duan, P. Abbeel. *Adversarial attacks on neural network policies.* arXiv 2017.
- **[26]** H. Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[27]** H. Zhang, H. Chen, D. S. Boning, C. Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[28]** Y. Sun, R. Zheng, Y. Liang, F. Huang. *Who is the strongest enemy? Towards optimal and efficient evasion attacks in deep RL.* ICLR 2022.
- **[29]** T. Franzmeyer et al. *Illusory attacks: Information-theoretic detectability matters in adversarial attacks.* ICLR 2024.
- **[30]** X. Liu, S. Chakraborty, Y. Sun, F. Huang. *Rethinking adversarial policies: A generalized attack formulation and provable defense in RL.* ICLR 2024.
- **[31]** M. Yang, G. Liu, Z. Zhou, J. Wang. *Probabilistic automata-based method for enhancing performance of deep reinforcement learning systems.* IEEE/CAA Journal of Automatica Sinica (submitted).
- **[32]** Z. Zhou, G. Liu. *Robustness testing for multi-agent reinforcement learning: State perturbations on critical agents.* European Conference on Artificial Intelligence (ECAI) 2023.
- **[33]** S. Han et al. *What is the solution for state-adversarial multi-agent reinforcement learning?* Transactions on Machine Learning Research (TMLR) 2024.
- **[37]** S. Li et al. *Attacking cooperative multi-agent reinforcement learning by adversarial minority influence.* arXiv 2023.
