# 126. Distributionally Robust Multi-Agent Reinforcement Learning for Dynamic Chute Mapping

## Metadata
- **Title**: Distributionally Robust Multi-Agent Reinforcement Learning for Dynamic Chute Mapping
- **Authors**: Guangyi Liu, Suzan Iloglu, Michael Caldara, Joseph W. Durham, Michael M. Zavlanos
- **Affiliation**: Amazon Robotics; Department of Mechanical Engineering and Materials Science, Duke University
- **Venue**: Not specified (arXiv preprint, 2025)
- **Link/arXiv**: arXiv:2503.09755v1 [cs.LG], 12 Mar 2025

## Taxonomy
- **Robustness / perturbation type targeted**: Distribution shift / distributional uncertainty in the reward function (specifically uncertain and dynamic package induction-rate distributions); out-of-distribution (OOD) robustness; adversarial variations in induction distributions
- **Method paradigm**: Group distributionally robust optimization (group DRO), distributionally robust Bellman operator, worst-case (minimax over distribution groups) optimization, value decomposition (VDN), DQN, contextual bandit-based worst-case predictor
- **Keywords**: Distributionally Robust MARL, group DRO, dynamic chute mapping, contextual bandit, worst-case reward prediction, robotic sortation warehouse

## TL;DR
The paper introduces DRMARL, a framework that integrates group distributionally robust optimization into multi-agent reinforcement learning to learn destination-to-chute mapping policies robust to adversarial/uncertain package induction-rate distributions, and proposes a contextual-bandit-based worst-case reward predictor that cuts the cost of worst-case group identification from O(m) to O(1).

## Problem & Motivation
In Amazon robotic sortation warehouses, the destination-to-chute mapping policy critically determines package throughput, but uncertain and dynamic package induction rates can cause increased package recirculation. The authors' prior MARL chute-mapping policy assumes the deployment induction distribution matches the training distribution and that the daily induction rate stays near its average; in practice induction patterns vary significantly over time, degrading the MARL policy under unexpected distribution shifts (out-of-distribution induction data). Prior destination-assignment and MARL-for-resource-allocation approaches do not account for distributional uncertainty in demand/system dynamics, and traditional distributionally robust RL primarily addresses transition-probability ambiguity rather than induction (reward) distribution changes. The paper aims to make the learned chute-mapping policy robust to distribution shifts in package induction.

## Robustness Setting
- **Threat model / uncertainty set**: Distribution shift in package induction patterns, modeled via a group DRO ambiguity set M defined as convex combinations of m known empirical induction-generating distributions {P_1, ..., P_m} (multinomial distributions estimated via Sample Average Approximation from historical data, clustered by week). The distribution shift affects only the reward function (recirculation), so robustness is sought against worst-case induction distributions within (and demonstrated even beyond) the ambiguity set. The framework optimizes for the worst-case distribution group across G.
- **Setting**: cooperative MARL (each destination is an agent; objectives aligned with the global goal of minimizing recirculation while maintaining throughput); centralized value decomposition with independent execution (π = ∏ πi) and budget-constrained joint actions; online / model-free RL (DQN-based).

## Method
- Formulates dynamic chute mapping as a Markov game over N agents (destinations), using a Value Decomposition Network (VDN) that expresses the joint Q-network as a sum of local Q-networks (a single shared Q' network for all agents), with budget-constrained joint actions solved as an integer program (via OR-Tools / Xpress).
- Introduces group DRO into MARL: rather than minimizing the worst-case Bellman error (which does not yield a policy optimal under worst-case rewards), it defines a distributionally robust Bellman operator T̃_G(Q̃)(s,a) = inf_{g∈G} E_{X∼P_g}[r(s,a;X)] + γ max_{a'} Q̃(s',a'), and the corresponding distributionally robust loss, so the policy selects actions optimal w.r.t. worst-case reward functions.
- Uses Lemma 3.1 to reduce the infinite-dimensional DRO problem to a finite minimization over m groups (worst-case over the ambiguity set equals worst-case over the group vertices).
- Proposes a contextual bandit (CB)-based worst-case reward predictor: an independent DQN Q_CB(s,a,g;ψ) ≈ E_{X∼P_g}[r(s,a;X)] is trained (Algorithm 1) to predict, for each state-action pair, the worst-case distribution group g' = arg min_{g∈G} Q_CB(s,a,g). DRMARL training (Algorithm 2) then uses this predicted g' instead of exhaustive search, reducing worst-case identification complexity from O(m) to O(1).
- In the large-scale setting where the transition probability also depends on X (violating the Lemma 3.2 assumption), an upper-bounding operator Ũ_R is used as a tractable approximation, with Q_CB approximating both immediate-reward and transition components.

## Theoretical Contributions
- **Lemma 3.1**: For an ambiguity set M of convex combinations of groups, the worst-case expected reward over M equals the infimum over the finite group set G (optimum of a linear program over the simplex is attained at a vertex), making group DRO finite-dimensional and tractable.
- **Lemma 3.2**: Derives the distributionally robust Bellman operator T̃_G for MARL (reduces to the reward-ambiguity case since the distribution shift in X affects only the reward), and proves it is a γ-contraction under the ℓ∞ norm, so Q-learning converges to Q̃*.
- (Appendix C.1) Shows the approximating operator Ũ_R provides an upper bound on the distributionally robust Bellman operator T̃_R for the large-scale case where transitions also depend on X.

## Experiments
- **Environment/Benchmark**: (1) A simplified robotic sortation warehouse simulation (10 eject chutes, 1 recirculation chute, 20 destinations; 5-hour episodes, 30-min steps; m = 9 induction groups, normal-distribution-based ambiguity set). (2) A large-scale Amazon robotic sortation warehouse simulation (187 eject chutes, 1 recirculation chute, 120 destinations; 11-hour episodes, 5-min steps; m = 21 induction groups spanning Years 1-4).
- **Baselines**: Regular MARL (trained on a single distribution / Year 4); DRMARL with random group selection; DRMARL with exhaustive worst-case search; and MARL (group-specific) trained and tested on the same group as a theoretical-optimal reference.
- **Evaluation metrics**: Recirculation rate, throughput, recirculation amount; relative improvement over MARL baseline; training time / convergence (training efficiency); CB prediction loss; OOD performance and performance on distributions outside the ambiguity set M.

## Key Results
- In the simplified warehouse (Table 1, averaged over m = 9 groups), DRMARL with Q_CB achieves a 0.56% ± 0.18% recirculation rate vs 2.16% ± 2.35% for MARL, nearly matching exhaustive search (0.55%) and the group-specific MARL optimum (0.53%), while converging in under ~300 seconds vs at least ~2900 seconds for exhaustive search.
- In the large-scale warehouse (Table 2, averaged over m = 21 groups), DRMARL improves over the MARL baseline by 79.97% recirculation-rate reduction, 5.62% throughput increase, and 33.64% recirculation-amount reduction; the abstract and Appendix D report an average ~80% reduction in package recirculation.
- The Q_CB predictor reduces worst-case-group identification complexity from O(m) to O(1); exhaustive evaluation over G required approximately 924 hours on a 64-vCPU cloud instance, and Q_CB achieves prediction errors below 1% of the recirculation rate. DRMARL also generalizes to induction distributions P' outside the ambiguity set M.

## Limitations & Future Work
- Due to industry confidentiality, the specific large-scale data source cannot be disclosed and only relative performance improvements are reported.
- In the large-scale setting the transition probability also depends on the induction variable X, violating the Lemma 3.2 assumption; the method relies on an upper-bound approximation Ũ_R (reported relative approximation error < 0.57%) rather than the exact operator.
- The approach assumes historical operational data provide sufficiently rich induction patterns so that any future induction pattern is representable as a combination of basis distributions P_g.
- The authors note broad applicability beyond sortation (resource allocation, collaborative robotics, warehouse automation) and that the design principles can be extended to other MARL applications where distributional robustness is crucial.

## Relevance to Survey
A distributionally robust MARL contribution that targets robustness to reward-distribution (demand/induction) shifts via group DRO, distinct from the dominant robust-MDP / transition-uncertainty and adversarial-policy lines. It connects the distributionally robust RL line (DR Bellman operator, worst-case over ambiguity sets) with cooperative MARL value decomposition, and adds a contextual-bandit mechanism to address the well-known computational cost of distributionally robust RL. It is a strong industrial application case (Amazon robotic sortation) and explicitly situates itself relative to recent (Distributionally) Robust MARL frameworks (RMGs, ERNIE, DRNVI), making it a useful pointer for the "reward/demand distribution shift" sub-theme of robust MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.1, Literature Review — "Robust and Distributionally Robust RL"]_

"Robust and Distributionally Robust RL: Robust Reinforcement Learning (Robust RL) [20, 21, 22, 23, 24, 25] develops policies that maintain performance under worst-case conditions through adversarial perturbations. Distributionally Robust Reinforcement Learning (DRRL) [26, 27, 28, 29, 30, 31, 32] extends this by optimizing across environment distributions rather than single worst-case scenarios. While traditional DRRL primarily addresses ambiguity in MDP transition probabilities, this approach inadequately captures induction distribution changes in Amazon robotic sortation warehouses. Our problem requires focus on distributionally robust optimization of reward function distributions, building on [33, 34]. Recent advances in (Distributionally) Robust Multi-Agent RL [35, 36, 37, 38] have introduced frameworks like RMGs, ERNIE, and DRNVI to address environmental uncertainties, adversarial dynamics, and model uncertainties. While existing methods primarily focus on robustness in transition dynamics, adversarial interactions, and general environmental uncertainties, they do not explicitly address distributional shifts in package induction, which is a critical challenge in sortation warehouses. Our approach extends DRMARL to explicitly model and optimize against uncertainties in induction distributions, ensuring robust and consistent performance under varying operational conditions."

> _[Section 1.1, Literature Review — "MARL for Resource Allocation"]_

"MARL for Resource Allocation: MARL has previously been applied to address resource allocation problems [16, 17, 18]. For example, a MARL framework for ocean transportation networks was proposed in [19]. This framework develops a multi-agent Q-learning algorithm where the local Q-networks depend on the joint states (including the limited shared resources) and the joint actions. However, since the joint state-action space grows exponentially with the number of agents, the local Q-networks are hard to learn and this approach does not scale well in practice. This limitation was addressed in our previous work [6], where the local Q-networks are only loosely coupled, enhancing the scalability while still being interconnected enough to capture the impact of robot congestion on the sortation floor. Compared to [19], the method proposed in [6] models resources explicitly as actions and considers budget constraints when taking joint actions. However, these MARL-based approaches do not incorporate distributional robustness, making them sensitive to demand fluctuations and uncertainty, which our DRMARL framework explicitly addresses to ensure reliable performance in dynamic sorting environments."

> _[Section 1.1, Literature Review — "Group DRO"]_

"Group DRO: Group Distributionally Robust Optimization aims to enhance model robustness across diverse subpopulations by optimizing for the worst-performing groups rather than average performance [39]. This approach ensures fairness and resilience to distribution shifts, particularly for underrepresented groups. While initial work focused on single-agent supervised learning [40, 41], recent advances have extended these principles to more complex settings. Notably, [42] provided a soft-weighting method on distribution groups with convergence guarantees, while [43] and [44] demonstrated the applicability of group DRO in multi-agent systems and reinforcement learning, respectively. Our work bridges a critical gap by introducing group DRO principles to DRMARL. We begin by formulating the distributionally robust Bellman operator and addressing the computational challenges of exploring all distribution groups during the training. To tackle these challenges, we provide a DR Bellman operator specifically designed for MARL and introduce a contextual bandit (CB)-based worst-case distribution group predictor. This predictor enables efficient training by adaptively identifying the worst-case distribution groups."

### Cited references (resolved from the paper's bibliography)
- **[6]** Y. Shen, B. McClosky, J. W. Durham, M. M. Zavlanos. *Multi-Agent Reinforcement Learning for Resource Allocation in Large-Scale Robotic Warehouse Sortation Centers.* IEEE CDC 2023.
- **[16]** H. Nie, S. Li, Y. Liu. *Multi-agent deep reinforcement learning for resource allocation in the multi-objective HetNet.* IWCMC 2021.
- **[17]** R. Mei, Z. Wang. *Multi-Agent Deep Reinforcement Learning-Based Resource Allocation for Cognitive Radio Networks.* IEEE Transactions on Vehicular Technology 2024.
- **[18]** W. Jun-Han, H. He, J. Cha, I. Jeong, A. Chang-Jun. *Multi-Agent Reinforcement Learning for Efficient Resource Allocation in Internet of Vehicles.* Electronics 2025.
- **[19]** X. Li, J. Zhang, J. Bian, Y. Tong, T.-Y. Liu. *A cooperative multi-agent reinforcement learning framework for resource balancing in complex logistics network.* arXiv 2019.
- **[20]** J. Morimoto, K. Doya. *Robust reinforcement learning.* Neural Computation 2005.
- **[21]** W. Wiesemann, D. Kuhn, B. Rustem. *Robust Markov decision processes.* Mathematics of Operations Research 2013.
- **[22]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[23]** J. Moos, K. Hansel, H. Abdulsamad, S. Stark, D. Clever, J. Peters. *Robust reinforcement learning: A review of foundations and recent advances.* Machine Learning and Knowledge Extraction 2022.
- **[24]** V. Goyal, J. Grand-Clement. *Robust Markov decision processes: Beyond rectangularity.* Mathematics of Operations Research 2023.
- **[25]** T. Yamagata, R. Santos-Rodriguez. *Safe and Robust Reinforcement-Learning: Principles and Practice.* arXiv 2024.
- **[26]** H. Xu, S. Mannor. *Distributionally robust Markov decision processes.* NeurIPS 2010.
- **[27]** E. Smirnova, E. Dohmatob, J. Mary. *Distributionally robust reinforcement learning.* arXiv 2019.
- **[28]** L. Hou, L. Pang, X. Hong, Y. Lan, Z. Ma, D. Yin. *Robust reinforcement learning with Wasserstein constraint.* arXiv 2020.
- **[29]** S. Wang, N. Si, J. Blanchet, Z. Zhou. *On the foundation of distributionally robust reinforcement learning.* arXiv 2023.
- **[30]** S. S. Ramesh, P. G. Sessa, Y. Hu, A. Krause, I. Bogunovic. *Distributionally robust model-based reinforcement learning with large state spaces.* AISTATS 2024.
- **[31]** Z. Zhang, K. Panaganti, L. Shi, Y. Sui, A. Wierman, Y. Yue. *Distributionally Robust Constrained Reinforcement Learning under Strong Duality.* arXiv 2024.
- **[32]** M. Lu, H. Zhong, T. Zhang, J. Blanchet. *Distributionally Robust Reinforcement Learning with Interactive Data Collection: Fundamental Hardness and Near-Optimal Algorithm.* arXiv 2024.
- **[33]** A. Z. Ren, A. Majumdar. *Distributionally robust policy learning via adversarial environment generation.* IEEE Robotics and Automation Letters 2022.
- **[34]** Z. Liu, Q. Bai, J. Blanchet, P. Dong, W. Xu, Z. Zhou, Z. Zhou. *Distributionally Robust Q-Learning.* ICML 2022.
- **[35]** K. Zhang, T. Sun, Y. Tao, S. Genc, S. Mallya, T. Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[36]** A. Bukharin, Y. Li, Y. Yu, Q. Zhang, Z. Chen, S. Zuo, C. Zhang, S. Zhang, T. Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* NeurIPS 2024.
- **[37]** L. Shi, E. Mazumdar, Y. Chi, A. Wierman. *Sample-Efficient Robust Multi-Agent Reinforcement Learning in the Face of Environmental Uncertainty.* arXiv 2024.
- **[38]** L. Shi, J. Gai, E. Mazumdar, Y. Chi, A. Wierman. *Breaking the Curse of Multiagency in Robust Multi-Agent Reinforcement Learning.* arXiv 2024.
- **[39]** S. Sagawa, P. W. Koh, T. B. Hashimoto, P. Liang. *Distributionally robust neural networks for group shifts: On the importance of regularization for worst-case generalization.* arXiv 2019.
- **[40]** W. Hu, G. Niu, I. Sato, M. Sugiyama. *Does distributionally robust supervised learning give robust classifiers?* ICML 2018.
- **[41]** Y. Oren, S. Sagawa, T. B. Hashimoto, P. Liang. *Distributionally robust language modeling.* arXiv 2019.
- **[42]** T. Soma, K. Gatmiry, S. Jegelka. *Optimal algorithms for group distributionally robust optimization and beyond.* arXiv 2022.
- **[43]** X. Wu, J. Fu. *Distributed robust optimization for multi-agent systems with guaranteed finite-time convergence.* arXiv 2023.
- **[44]** M. Xu, P. Huang, Y. Niu, V. Kumar, J. Qiu, C. Fang, K.-H. Lee, X. Qi, H. Lam, B. Li, et al. *Group distributionally robust reinforcement learning with hierarchical latent variables.* AISTATS 2023.
