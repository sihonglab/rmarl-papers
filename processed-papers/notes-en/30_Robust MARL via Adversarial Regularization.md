# 30. Robust Multi-Agent Reinforcement Learning via Adversarial Regularization: Theoretical Foundation and Stable Algorithms

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning via Adversarial Regularization: Theoretical Foundation and Stable Algorithms
- **Authors**: Alexander Bukharin, Yan Li, Yue Yu, Qingru Zhang, Zhehui Chen, Simiao Zuo, Chao Zhang, Songan Zhang, Tuo Zhao
- **Affiliation**: Georgia Institute of Technology; Google; Microsoft; Ford Motor Company
- **Venue**: NeurIPS 2023
- **Link/arXiv**: https://github.com/abukharin3/ERNIE (code)

## Taxonomy
- **Robustness / perturbation type targeted**: Observation/state noise (sensor error, adversarial state perturbations), changing transition dynamics (sim-to-real gap), and malicious/changing actions of a small subset of agents
- **Method paradigm**: Adversarial training / adversarial regularization, Lipschitz (smoothness) regularization, Stackelberg (leader-follower) game reformulation, distributionally robust optimization (for the mean-field extension)
- **Keywords**: Robust MARL, adversarial regularization, Lipschitz continuity, Stackelberg game, mean-field MARL, distributionally robust optimization

## TL;DR
The paper proves that controlling a policy's Lipschitz constant yields robustness (and that a smooth, near-optimal policy exists in smooth environments), and uses this insight to propose ERNIE, a cooperative-MARL framework that enforces policy/Q-function smoothness via adversarial regularization—stabilized by reformulating the adversarial training as a Stackelberg game—giving robustness to observation noise, transition-dynamics changes, and malicious agent actions.

## Problem & Motivation
MARL policies are typically trained in a fixed environment and are sensitive to small changes at deployment time: different transition dynamics, inaccurate state information (e.g., sensor error), and a single agent acting maliciously or unexpectedly that can destabilize the whole system. Existing single-agent robust RL methods cannot be directly transferred to MARL because of three barriers: (i) theoretical—it is unclear if/when they work for MARL; (ii) methodological—they may ignore inter-agent interactions; and (iii) algorithmic—single-agent robust RL is often unstable and worsens the already-unstable MARL training. The paper addresses all three with theoretical, methodological, and algorithmic contributions.

## Robustness Setting
- **Threat model / uncertainty set**: Bounded observation perturbations δ with ‖δ‖ ≤ ε (ℓ₂ or ℓ∞ norm) adversarially chosen to maximize the change in a policy's output; changing transition dynamics (environment deviation between train and test); and malicious joint-action perturbations affecting at most K agents (measured by Hamming distance D(a,a′)). For the mean-field extension, the attack on the empirical state distribution dₛ is bounded by the Wasserstein distance (distributionally robust optimization).
- **Setting**: Cooperative MARL (agents maximize a global reward); partially observable Markov game; policy-search / actor-critic training (MAPPO, MADDPG, Q-learning); robustness evaluated by training in a non-perturbed environment and testing in a perturbed one (online training).

## Method
- **ERNIE adversarial regularizer**: For each agent's policy π_θk, add a regularizer R_π(o_k; θ_k) = max_{‖δ‖≤ε} D(π_θk(o_k+δ), π_θk(o_k)) that measures local Lipschitz smoothness and is added to the policy objective: min_θ F(θ) = L(θ) + λ Σ_n E[R_π(o_n; θ_n)]. D is the KL divergence for stochastic policies (e.g., MAPPO) and an ℓ_p norm for deterministic policies (e.g., MADDPG, Q-learning). This gives both Lipschitz continuity and data augmentation with adversarial examples.
- **Stackelberg (leader-follower) reformulation**: Vanilla adversarial regularization is a nonconvex-nonconcave zero-sum minimax problem that is unstable. The paper instead treats the perturbation δ as a K-fold composition of one-step gradient-ascent maps U_θ that depends on the model parameter θ, so the policy (leader) anticipates the attacker (follower). The resulting "Stackelberg gradient" adds a leader-follower interaction term and is computed via a Hessian-vector product (finite-difference), adding only ~O(d) overhead and two backpropagations, yielding a smoother, more stable optimization.
- **Robustness against malicious actions (ERNIE-A)**: A regularizer on the global Q-function, R_ω^A(s,a) = max_{D(a,a′)≤K} ‖Q(s,a;ω) − Q(s,a′;ω)‖²₂, encourages stable Q-values when at most K agents change their actions. Solved greedily by perturbing one agent's action at a time (top-K changes), with O(|A|·N·K) cost; K=1 already suffices empirically.
- **Mean-field extension**: ERNIE is extended to mean-field MARL by adversarially perturbing the mean-field approximation terms (empirical state distribution dₛ and average neighbor action ā_j); the attack on dₛ is bounded by the Wasserstein distance, enforced via regularization (distributionally robust optimization formulation).

## Theoretical Contributions
- **Theorem 3.1**: If the environment is (L_r, L_P)-smooth, then any policy's Q-function is Lipschitz in the state (L_Q = L_r + γL_P/(1−γ)), and for an L_π-smooth policy the value function is Lipschitz (L_V = L_π/(1−γ) + L_Q).
- **Theorem 3.2 (existence of smooth, near-optimal policy)**: For any ε > 0, in a smooth environment there exists an ε-optimal policy that is O(L_Q/ε)-smooth (feeding a smooth Q into a softmax operator induces a smooth policy).
- **Theorem 3.3 (robustness to observation noise)**: For an L_π-smooth policy and perturbations with ‖δ_s^t‖ ≤ ε, the perturbed-observation value satisfies |V^π(s) − V^{π̃}(s)| ≤ 2L_π ε/(1−γ)², with an analogous bound for Q; this holds with no smoothness assumption on the transition or reward.
- The discussion is shown to carry over to cooperative MARL (Remark 3.1) by setting S/A as the joint state/action spaces; large neural networks can approximate the target policy/Q with smoothness guarantees (deferred to appendix).

## Experiments
- **Environment/Benchmark**: Traffic light control (Flow framework, two-by-two grid of four agents; evaluated under different car speeds, traffic flows, network topologies/sizes, and observation noise) and particle environments (cooperative navigation, predator-prey, tag, cooperative/covert communication); mean-field cooperative navigation with N = 3, 6, 15 agents; additional multi-agent drone control (Appendix E.1).
- **Baselines**: QCOMBO and COMA (traffic); MADDPG, M3DDPG, RMA3C, and a Baseline-Gaussian (Gaussian random perturbation); mean-field MADDPG (mean-field setting).
- **Evaluation metrics**: Reward / cumulative reward under increasing environment deviation and observation noise level ε; percentile (worst-case) reward across 10 initializations; sensitivity to hyperparameters K (attack steps) and ε; robustness vs. network width.

## Key Results
- Baseline MARL algorithms are vulnerable to small environment changes (speed, traffic flow, topology, observation noise), while ERNIE maintains more stable reward across all these changes; the Gaussian baseline only helps for Gaussian-like perturbations.
- ERNIE-A maintains higher reward when a randomly selected agent's action is adversarially changed 3% or 5% of the time, where both baselines degrade.
- In particle environments ERNIE matches or beats MADDPG across noise levels; M3DDPG surprisingly gives some observation-noise robustness; ERNIE is also compared against RMA3C.
- The mean-field ERNIE extension shows higher reward and slower performance decay across noise levels for N = 3, 6, 15. Ablations show the Stackelberg formulation improves stability/worst-case (percentile) robustness, adversarial training (K>0, ε>0) consistently beats the K=0/ε=0 baseline, and sufficiently wide networks (128/256 units) are needed for robust ERNIE policies.

## Limitations & Future Work
- ERNIE is motivated by smoothness, but real-world environments are not always smooth; the paper relies on a (partial) smoothness assumption as prior knowledge.
- λ is a fixed global hyperparameter; future work could adaptively select λ per state to allow state-dependent smoothness.
- Robustness against changes in the transition kernel (vs. observation noise) is largely deferred as future investigation in the theory.

## Relevance to Survey
A representative "state/observation perturbation + adversarial training" entry in robust MARL that bridges single-agent smoothness/adversarial-regularization ideas to the cooperative multi-agent setting with theoretical backing (Lipschitz-continuity ⇒ robustness). It connects the perturbation-based robust RL line (smoothing, adversarial regularization), the robust-Markov-game / model-uncertainty line (Zhang et al., M3DDPG), the state-adversarial robust-equilibrium line (He et al., Han et al.), and—via its mean-field extension—the distributionally robust optimization line. Its Stackelberg-game reformulation contributes a stable-optimization angle relevant to the broader minimax/adversarial-training methodology.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Background — "Robust RL." bullet]_

"In recent years many single agent robust RL techniques have been proposed. Most of these methods use information about the underlying simulator to train agents over a variety of relevant environment settings [7; 8; 9; 10; 11]. Although these methods can provide robustness against a wide range of environment changes, they suffer from long training times and require expert knowledge of the underlying simulator, which is not practical. Another direction of research focuses on perturbation based methods [3; 12]. Perturbation based methods train the policy to be robust to input perturbations, encouraging the policy to act reasonably in perturbed or previously unseen states. [13] certify robustness by adding smoothing noise to the state; it is not clear how this affects the learned policy's optimality. Another related line of work [14; 15; 16; 17] studies robust markov decision processes and provides a principled way to learn robust policies. However, such methods often require strict assumptions on the perturbation/uncertainty. Inspiring our work, [3] proposes to learn a smooth policy in single agent RL, but they do so to reduce training complexity rather than increase robustness and provide no theoretical justiﬁcation for their method. Instead, we theoretically connect smoothness to robustness, extend perturbation based methods to MARL, and develop a more stable perturbation computation technique, and develop an extension to mean-ﬁeld MARL."

> _[Section 2, Background — "Robust MARL." bullet]_

"Recently, some works have studied the robustness of MARL systems. Lin et al. [18] studies how to attack MARL systems and ﬁnds that MARL systems are vulnerable to attacks on even a single agent. Zhang et al. [19] develop a framework to handle MARL with model uncertainty by formulating MARL as a robust Markov game. However, their proposed method only considers uncertainty in the reward function, while this article focuses on robustness to observation noise and changing transition dynamics. Li et al. [20] modify the MADDPG algorithm to consider the worst-case actions of the other agents in continuous action spaces with the M3DDPG algorithm. M3DDPG aims to grant robustness against the actions of other agents, which is less general than the robustness against observation noise, changing transition dynamics, and malicious agents that our method aims for. Wang et al. [21] consider robustness against uncertain transition dynamics, but their algorithm is not applied to deep MARL. More recently, He et al. [22]; Han et al. [23] introduces the concept of robust equilibrium and proposes to learn an adversarial policy to perturb each agent's observations. Finally Zhou et al. [24] propose to learn robust policies by minimizing the cross-entropy loss between agent's actions in non-perturbed states and perturbed states."

> _[Section 2, Background — closing paragraph on adversarial-training relatives]_

"The ERNIE framework is also related to several existing works which use similar adversarial training methods but target different domains such as trajectory optimization [25], semi-supervised learning [26; 27; 28], ﬁne-tuning language models [29; 30], and generalization in supervised learning [31]."

### Cited references (resolved from the paper's bibliography)
- **[3]** Shen, Li, Jiang, Wang, Zhao. *Deep reinforcement learning with robust and smooth policy.* ICML 2020.
- **[7]** Morimoto, Doya. *Robust reinforcement learning.* Neural Computation 2005.
- **[8]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[9]** Abdullah, Ren, Bou Ammar, Milenkovic, Luo, Zhang, Wang. *Wasserstein robust reinforcement learning.* arXiv 2019.
- **[10]** Pan, Seita, Gao, Canny. *Risk averse robust adversarial reinforcement learning.* ICRA 2019.
- **[11]** Wang, Zou. *Policy gradient method for robust reinforcement learning.* ICML 2022.
- **[12]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[13]** Kumar, Levine, Feizi. *Policy smoothing for provably robust reinforcement learning.* ICLR 2022.
- **[14]** Iyengar. *Robust dynamic programming.* Mathematics of Operations Research 2005.
- **[15]** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research 2005.
- **[16]** Panaganti, Xu, Kalathil, Ghavamzadeh. *Robust reinforcement learning using offline data.* NeurIPS 2022.
- **[17]** Li, Zhao, Lan. *First-order policy optimization for robust Markov decision process.* arXiv 2022.
- **[18]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE SPW 2020.
- **[19]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2021.
- **[20]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[21]** Wang, Wang, Zhou, Velasquez, Zou. *Data-driven robust multi-agent reinforcement learning.* IEEE MLSP 2022.
- **[22]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* TMLR 2023.
- **[23]** Han, Su, He, Han, Yang, Miao. *What is the solution for state adversarial multi-agent reinforcement learning?* arXiv 2022.
- **[24]** Zhou, Liu, Zhou. *A robust mean-field actor-critic reinforcement learning against adversarial perturbations on agent states.* IEEE TNNLS 2023.
- **[25]** Zhao, Zuo, Zhao, Zhao. *Adversarially regularized policy learning guided by trajectory optimization.* L4DC 2022.
- **[26]** Miyato, Maeda, Koyama, Ishii. *Virtual adversarial training: a regularization method for supervised and semi-supervised learning.* IEEE TPAMI 2018.
- **[27]** Hendrycks, Mazeika, Kadavath, Song. *Using self-supervised learning can improve model robustness and uncertainty.* NeurIPS 2019.
- **[28]** Zuo, Yu, Liang, Jiang, Er, Zhang, Zhao, Zha. *Self-training with differentiable teacher.* Findings of NAACL 2022.
- **[29]** Jiang, He, Chen, Liu, Gao, Zhao. *SMART: Robust and efficient fine-tuning for pre-trained natural language models through principled regularized optimization.* ACL 2020.
- **[30]** Yu, Zuo, Jiang, Ren, Zhao, Zhang. *Fine-tuning pre-trained language model with weak supervision: A contrastive-regularized self-training approach.* NAACL-HLT 2021.
- **[31]** Zuo, Liang, Jiang, Liu, He, Gao, Chen, Zhao. *Adversarial regularization as Stackelberg game: An unrolled optimization approach.* EMNLP 2021.
