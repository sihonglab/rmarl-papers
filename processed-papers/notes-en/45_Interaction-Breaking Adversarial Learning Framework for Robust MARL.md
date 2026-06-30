# 45. Interaction-Breaking Adversarial Learning Framework for Robust Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Interaction-Breaking Adversarial Learning Framework for Robust Multi-Agent Reinforcement Learning
- **Authors**: Sunwoo Lee, Mingu Kang, Yonghyeon Jo, Seungyul Han
- **Affiliation**: Graduate School of Artificial Intelligence, UNIST, Ulsan, South Korea
- **Venue**: ICML 2026 (Proceedings of the 43rd International Conference on Machine Learning, PMLR 306, 2026)
- **Link/arXiv**: arXiv:2605.18024v2 [cs.LG]; code at https://sunwoolee0504.github.io/IBAL

## Taxonomy
- **Robustness / perturbation type targeted**: Interaction-level perturbations — adversarial attacks on observations (occlusion/masking) and actions that break inter-agent coordination; also robustness to non-parametric perturbations (agent-missing / disabled units, reduced initial health)
- **Method paradigm**: Adversarial training; information-theoretic (mutual-information) attack design; CTDE value-decomposition (QMIX); Joint-Adversarial Dec-POMDP formulation with value-equivalence to an induced perturbed Dec-POMDP
- **Keywords**: Robust MARL, interaction-breaking attack, mutual information, CTDE, observation/action attack, QMIX

## TL;DR
The paper proposes IBAL (Interaction-Breaking Adversarial Learning), a robust MARL framework that uses a mutual-information criterion to build a joint observation-and-action attacker which minimizes cross-group influence and breaks coordination, then trains CTDE policies (mainly QMIX) against it via a value-equivalent induced Dec-POMDP, yielding stronger robustness under diverse attacks and agent-missing scenarios.

## Problem & Motivation
Cooperative MARL under CTDE relies heavily on learned inter-agent coordination, which makes policies brittle when external perturbations disrupt the interaction structure itself. Prior robust MARL methods mostly consider value-oriented attacks (e.g., biasing agents toward suboptimal/low-value actions) or communication-channel corruption, and these formulations typically do not explicitly model how agents influence one another. As a result, they fail to capture breakdowns in the interaction structure underlying coordination, leaving robustness limited when agents cannot reliably interact or when coordinated attacks disrupt their dependencies—causing sharp performance degradation in tightly coupled cooperative tasks.

## Robustness Setting
- **Threat model / uncertainty set**: A joint adversary perturbs both observations and actions. Agents are partitioned into two disjoint groups G1 and G2; cross-group influence is quantified via conditional mutual information (MI), decomposed (chain rule) into an observation-level MI term and an action-level MI term. The observation attacker f_adv applies a zero-forcing mask to the L observation dimensions of G1 with the largest dimension-wise MI about G2 (motivated by the data-processing inequality); the action attacker π_adv stochastically (with probability P_act) replaces G1's intermediate actions with the MI-minimizing joint action. MI is estimated via CLUB (observation-level) and a KL/cross-entropy reconstruction model (action-level).
- **Setting**: Cooperative; CTDE (centralized training, decentralized execution); online. Primarily instantiated on value-based QMIX, but extended to policy-gradient MAPPO.

## Method
- Formalize the joint attack as a Joint-Adversarial Dec-POMDP (JA-Dec-POMDP) M_J = ⟨N, S, A, P, Ω, O, R, γ, f_adv, π_adv⟩: at each step the observation attacker perturbs o_t → õ_t, the ego policy samples an intermediate action â_t ~ π(·|õ_t), and the action attacker outputs the executed ã_t ~ π_adv(·|s_t, â_t).
- Prove value-equivalence (Theorem 4.2): the JA-Dec-POMDP value V_{π_adv∘π∘f_adv} equals the state value of an induced Dec-POMDP M̃ with perturbed dynamics, so standard MARL algorithms can optimize π in M̃ and preserve performance under the attack.
- Design the interaction-breaking attack: partition N into G1/G2, quantify cross-group influence by conditional MI, with f_adv targeting observation-level MI and π_adv targeting action-level MI to break interaction by minimizing them separately.
- Observation attacker: upper-bound group-wise MI by a sum of dimension-wise MI terms plus a fast-decaying group-redundancy term (Lemma 4.3), then mask the L dimensions with the largest dimension-wise MI; precomputed scores are aggregated when the partition changes to avoid repeated MI estimation.
- Training (IBAL): randomly sample group partitions each episode (k ~ Unif{0,…,K}, K ≤ n/2), apply symmetric mutual occlusion, and use an adaptive action-attack probability schedule (grown by factor α when average success rate exceeds threshold η), then learn Qtot via the QMIX TD loss on data from M̃.

## Theoretical Contributions
- **Theorem 4.2**: existence of an induced Dec-POMDP M̃ whose state value of π equals the JA-Dec-POMDP value V_{π_adv∘π∘f_adv} (proof via a Bellman-equation form, Lemma A.1, and uniqueness of the fixed point).
- **Lemma 4.3**: an upper bound decomposing group-wise observation-level MI into a sum of dimension-wise MI terms plus a group-redundancy term R(G1;G2) (proof via the Möbius expansion of multivariate MI and the conditioning-relaxation property), justifying the efficient dimension-wise masking criterion.

## Experiments
- **Environment/Benchmark**: StarCraft II Multi-Agent Challenge (SMAC) — 3m, 3s vs 3z, 2s3z, 8m, 1c3s5z, MMM; also Level-Based Foraging (LBF) and SMACv2 (terran/zerg/protoss 5 vs 5).
- **Baselines**: Robust MARL methods (all QMIX-based unless noted): Vanilla QMIX, Rand-Obs, Rand-Act, FGSM, ATLA, ERNIE, ROMANCE (trained vs EGA), WALL (trained vs Wolfpack). Attacker baselines used at evaluation: Natural (Nat.), Random (Rand.), FGSM, EGA, Wolfpack (Wolf.), and the proposed interaction-breaking attack (Ours). Non-parametric perturbations: Dis-ℓ (disable ℓ ally units) and HP-h (reduce ally initial health by h%).
- **Evaluation metrics**: Mean test win rate / success rate (%) over 5 random seeds (with standard deviation), under unseen attacks and non-parametric perturbations; policies trained for 10M timesteps from a 1M-timestep QMIX pretrain.

## Key Results
- Under adversarial attacks, IBAL consistently outperforms prior robust MARL methods and generalizes across observation and action attacks; baselines such as FGSM and WALL perform well against their own attacks but drop sharply under the interaction-breaking attack (e.g., on 8m the "Ours" attack column: WALL 13.5% vs IBAL 88.4%; on MMM: WALL 13.5% vs IBAL 88.7%).
- Under non-parametric perturbations (Dis-ℓ, HP-h), IBAL shows a clear advantage: most methods degrade sharply when ally units are disabled, while IBAL remains effective (e.g., on 8m under Dis-1, IBAL 87.0% vs the next-best WALL 25.4%).
- IBAL generalizes to LBF and SMACv2 (achieving stronger natural performance under SMACv2's increased stochasticity) and, because it does not rely on value information or the IGM property, also improves robustness for the policy-gradient CTDE method MAPPO.
- Ablations show every component matters: removing the observation or action attack causes substantial drops, and MI-guided masking plus the adaptive schedule outperform random masking / fixed probability; zero-masking is more effective than Gaussian-noise or FGSM variants on the selected dimensions.

## Limitations & Future Work
- IBAL introduces additional hyperparameters—the maximum group size K and the masking budget L—though guideline ranges from hyperparameter search are provided and performance is reported as not overly sensitive within them.
- IBAL incurs extra computational overhead due to MI estimation; the authors characterize this overhead as moderate and reasonable given the performance gains.

## Relevance to Survey
This paper extends the adversarial-training line of robust MARL beyond value-oriented and communication attacks to attacks that explicitly target the interaction/coordination structure, using an information-theoretic (mutual-information) criterion. It connects the "adversarial attacks on observations/actions" theme, the "robust CTDE / value decomposition" theme (QMIX, building on Phan et al.'s adversarial value decomposition), and the "information-theoretic MARL" theme. Methodologically it sits alongside ROMANCE (EGA) and WALL (Wolfpack) as a robust-training-against-an-attacker approach, while its JA-Dec-POMDP value-equivalence result links it to the robust-RL-as-perturbed-dynamics formulation.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Works — "Robust Multi-Agent RL."]_

"Robust MARL addresses perturbations in multi-agent environments. One common direction improves robustness through regularization-based objectives (Lin et al., 2020; Li et al., 2023b; Wang et al., 2023; Bukharin et al., 2023; Li et al., 2025) and distributional RL methods that explicitly model uncertainty (Li et al., 2020; Xu et al., 2021; Du et al., 2024; Geng et al., 2024). Another line of work revisits equilibrium concepts, developing robust variants of Nash equilibria tailored to multi-agent systems (Zhang et al., 2020b; Li et al., 2023a). In addition, max-min robust optimization (Chinchuluun et al., 2008; Han & Sung, 2021) has been integrated into MARL formulations to learn policies resilient to worst-case perturbations (Li et al., 2019; Wang et al., 2022)."

> _[Section 2, Related Works — "Adversarial Learning Frameworks."]_

"A substantial line of research in RL improves robustness (Nilim & El Ghaoui, 2005; Moos et al., 2022; Lee et al., 2026) by training agents to withstand adversarial perturbations. In single-agent MDPs, attacks commonly target states or observations (Pattanaik et al., 2017; Zhang et al., 2020a; 2021a; Qiaoben et al., 2024), actions (Pinto et al., 2017; Tessler et al., 2019; Tan et al., 2020; Lee et al., 2021; Liu et al., 2024), rewards (Bouhaddi & Adi, 2023; Rakhsha et al., 2021; Xu et al., 2024), or environment dynamics (Chae et al., 2022). These threat models extend to multi-agent settings via state or observation uncertainties (Han et al., 2022; He et al., 2023; Zhou et al., 2025), action attacks (Yuan et al., 2023), and reward perturbations (Kardes¸ et al., 2011). Prior work also studies adversarial effects in value-decomposition frameworks (Phan et al., 2021), attacks on critical agents (Yuan et al., 2023; Zhou et al., 2024b; Lee et al., 2025), and vulnerabilities in inter-agent communication (Xue et al., 2021; Tu et al., 2021; Sun et al., 2023). Adversarially shaped frameworks have also been used to improve zero-shot human-AI coordination (Yan et al., 2023; Kang et al., 2026)."

> _[Section 2, Related Works — "Information-Theoretic Approaches for MARL."]_

"Mutual information has been widely used in MARL to estimate and exploit inter-agent influence (Jaques et al., 2019; Li et al., 2022; Ye & Lu, 2023; Zhou et al., 2024a; Park et al., 2026). Building on this idea, prior work leverages MI for structured exploration and role diversity under parameter sharing (Mahajan et al., 2019; Li et al., 2021; Jo et al., 2024), and uses influence-based signals to guide and stabilize inter-agent communication (Wang et al., 2020b; Guan et al., 2022; Ding et al., 2024; Bae et al., 2026). In contrast, we use MI to quantify cross-group influence and design an attacker that disrupts coordination by minimizing this influence, rather than targeting values."

> _[Introduction — prior-work discussion]_

"A growing body of work has investigated robustness in MARL (Lin et al., 2020; Li et al., 2019; He et al., 2023). Existing approaches typically pursue robustness by modeling uncertainty and perturbations during policy learning (Zhang et al., 2021b; Goodfellow et al., 2014), or by considering adversarial manipulations that degrade agent behavior, for example by biasing agents toward suboptimal actions (Bukharin et al., 2023; Yuan et al., 2023; Lee et al., 2025) or by corrupting communication channels (Xue et al., 2021) used for coordination. While effective under their targeted perturbation models, these methods often fail to capture breakdowns in the interaction structure underlying coordination. As a result, robustness against interaction-level failures can remain limited when agents cannot reliably interact or when coordinated attacks disrupt their dependencies, causing substantial performance degradation in tightly coupled cooperative tasks."

> _[Section 3.2, Adversarial Attacks for MARL]_

"To improve robustness against external perturbations, prior work in MARL has considered a range of adversarial attacks. A basic approach perturbs the state or observation by injecting noise, e.g., s̃_t = s_t + ϵ or õ_t = o_t + ϵ (Lin et al., 2020), where the key design choice is how to construct ϵ. Action attacks have also been widely studied. Under CTDE, a common formulation defines an attacker policy π_adv that selects perturbed actions to minimize learned utility estimates, e.g., ã_i_t ~ π_i_adv := arg min_{a_i∈A_i} Q_i(τ_i_t, a_i). For example, EGA (Yuan et al., 2023) diversifies value-minimizing attacks by learning critical timesteps for multiple random seeds, whereas the Wolfpack adversarial attack (Lee et al., 2025) sequentially targets agents to amplify disruption. In this paper, we consider both observation and action perturbations, but adopt an information-theoretic criterion that differs fundamentally from value-based objectives."

### Cited references (resolved from the paper's bibliography)
- **[Lin et al., 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[Li et al., 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Li et al., 2023a]** Li, Guo, Xiu, Xu, Yu, Wang, Liu, Yang, Liu. *Byzantine robust cooperative multi-agent reinforcement learning as a Bayesian game.* arXiv preprint arXiv:2305.12872, 2023.
- **[Li et al., 2023b]** Li, Xu, Guo, Feng, Wang, Liu, Yang, Liu, Lv. *MIR2: Towards provably robust multi-agent reinforcement learning by mutual information regularization.* arXiv preprint arXiv:2310.09833, 2023.
- **[Li et al., 2025]** Li, Xu, Xiu, Zheng, Feng, Ma, An, Yang, Liu. *Robust multi-agent reinforcement learning by mutual information regularization.* IEEE Transactions on Neural Networks and Learning Systems, 2025.
- **[Li et al., 2020]** Li, Wang, Tian, Jia, Zheng. *Multi-agent reinforcement learning based on value distribution.* Journal of Physics: Conference Series, vol. 1651, 012017, IOP Publishing, 2020.
- **[Li et al., 2021]** Li, Wang, Wu, Zhao, Yang, Zhang. *Celebrating diversity in shared multi-agent reinforcement learning.* NeurIPS 2021.
- **[Li et al., 2022]** Li, Tang, Yang, Hao, Sang, Zheng, Hao, Taylor, Tao, Wang, et al. *PMIC: Improving multi-agent reinforcement learning with progressive mutual information collaboration.* arXiv preprint arXiv:2203.08553, 2022.
- **[Wang et al., 2023]** Wang, Chen, Huang, Zhang, Zhao, Qu. *Regularization-adapted Anderson acceleration for multi-agent reinforcement learning.* Knowledge-Based Systems, 275:110709, 2023.
- **[Wang et al., 2022]** Wang, Wang, Zhou, Velasquez, Zou. *Data-driven robust multi-agent reinforcement learning.* IEEE 32nd International Workshop on Machine Learning for Signal Processing (MLSP) 2022.
- **[Wang et al., 2020b]** Wang, He, Yu, Qiu, An, Rabinovich. *Learning efficient multi-agent communication: An information bottleneck approach.* ICML 2020.
- **[Bukharin et al., 2023]** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* NeurIPS 2023.
- **[Xu et al., 2021]** Xu, Li, Bai, Fan. *MMD-MIX: Value function factorisation with maximum mean discrepancy for cooperative multi-agent reinforcement learning.* IJCNN 2021.
- **[Du et al., 2024]** Du, Chen, Wang, Xing, Yang, Philip, Chang, He. *Robust multi-agent reinforcement learning via Bayesian distributional value estimation.* Pattern Recognition, 145:109917, 2024.
- **[Geng et al., 2024]** Geng, Xiao, Li, Wei, Wang, Zhao. *Noise distribution decomposition based multi-agent distributional reinforcement learning.* IEEE Transactions on Mobile Computing, 2024.
- **[Zhang et al., 2020b]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Zhang et al., 2020a]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Zhang et al., 2021a]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv preprint arXiv:2101.08452, 2021.
- **[Zhang et al., 2021b]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, pp. 321–384, 2021.
- **[Chinchuluun et al., 2008]** Chinchuluun, Migdalas, Pardalos, Pitsoulis. *Pareto optimality, game theory and equilibria*, vol. 17. Springer, 2008.
- **[Han & Sung, 2021]** Han, Sung. *A max-min entropy framework for reinforcement learning.* NeurIPS 2021.
- **[Nilim & El Ghaoui, 2005]** Nilim, El Ghaoui. *Robust control of Markov decision processes with uncertain transition matrices.* Operations Research, 53(5):780–798, 2005.
- **[Moos et al., 2022]** Moos, Hansel, Abdulsamad, Stark, Clever, Peters. *Robust reinforcement learning: A review of foundations and recent advances.* Machine Learning and Knowledge Extraction, 4(1):276–315, 2022.
- **[Lee et al., 2026]** Lee, Bae, Park, Han. *Self-improving skill learning for robust skill-based meta-reinforcement learning.* ICLR 2026.
- **[Pattanaik et al., 2017]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* arXiv preprint arXiv:1712.03632, 2017.
- **[Qiaoben et al., 2024]** Qiaoben, Ying, Zhou, Su, Zhu, Zhang. *Understanding adversarial attacks on observations in deep reinforcement learning.* Science China Information Sciences, 67(5):1–15, 2024.
- **[Pinto et al., 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Tessler et al., 2019]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* ICML 2019.
- **[Tan et al., 2020]** Tan, Esfandiari, Lee, Sarkar, et al. *Robustifying reinforcement learning agents via action space adversarial training.* American Control Conference (ACC) 2020.
- **[Lee et al., 2021]** Lee, Esfandiari, Tan, Sarkar. *Query-based targeted action-space adversarial policies on deep reinforcement learning agents.* ACM/IEEE 12th International Conference on Cyber-Physical Systems 2021.
- **[Liu et al., 2024]** Liu, Kuang, Wang. *Robust deep reinforcement learning with adaptive adversarial perturbations in action space.* arXiv preprint arXiv:2405.11982, 2024.
- **[Bouhaddi & Adi, 2023]** Bouhaddi, Adi. *Multi-environment training against reward poisoning attacks on deep reinforcement learning.* SECRYPT, pp. 870–875, 2023.
- **[Rakhsha et al., 2021]** Rakhsha, Zhang, Zhu, Singla. *Reward poisoning in reinforcement learning: Attacks against unknown learners in unknown environments.* arXiv preprint arXiv:2102.08492, 2021.
- **[Xu et al., 2024]** Xu, Gumaste, Singh. *Reward poisoning attack against offline reinforcement learning.* arXiv preprint arXiv:2402.09695, 2024.
- **[Chae et al., 2022]** Chae, Han, Jung, Cho, Choi, Sung. *Robust imitation learning against variations in environment dynamics.* ICML 2022.
- **[Han et al., 2022]** Han, Su, He, Han, Yang, Zou, Miao. *What is the solution for state-adversarial multi-agent reinforcement learning?* arXiv preprint arXiv:2212.02705, 2022.
- **[He et al., 2023]** He, Han, Su, Han, Zou, Miao. *Robust multi-agent reinforcement learning with state uncertainty.* arXiv preprint arXiv:2307.16212, 2023.
- **[Zhou et al., 2025]** Zhou, Liu, Zhou, Guo. *Robust multi-agent reinforcement learning with stochastic adversary.* ICML 2025.
- **[Yuan et al., 2023]** Yuan, Zhang, Xue, Yin, Chen, Guan, Li, Qian, Yu. *Robust multi-agent coordination via evolutionary generation of auxiliary adversarial attackers.* AAAI 2023.
- **[Kardes¸ et al., 2011]** Kardeş, Ordóñez, Hall. *Discounted robust stochastic games and an application to queueing control.* Operations Research, 59(2):365–382, 2011.
- **[Phan et al., 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition.* AAAI 2021.
- **[Zhou et al., 2024b]** Zhou, Liu, Guo, Zhou. *Adversarial attacks on multiagent deep reinforcement learning models in continuous action space.* IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2024.
- **[Lee et al., 2025]** Lee, Hwang, Jo, Han. *Wolfpack adversarial attack for robust multi-agent reinforcement learning.* ICML 2025.
- **[Xue et al., 2021]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* arXiv preprint arXiv:2108.03803, 2021.
- **[Tu et al., 2021]** Tu, Wang, Wang, Manivasagam, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[Sun et al., 2023]** Sun, Zheng, Hassanzadeh, Liang, Feizi, Ganesh, Huang. *Certifiably robust policy learning against adversarial multi-agent communication.* ICLR 2023.
- **[Yan et al., 2023]** Yan, Guo, Lou, Wang, Zhang, Du. *An efficient end-to-end training approach for zero-shot human-AI coordination.* NeurIPS 2023.
- **[Kang et al., 2026]** Kang, Lee, Jo, Han. *Shaping zero-shot coordination via state blocking.* arXiv preprint arXiv:2605.11688, 2026.
- **[Jaques et al., 2019]** Jaques, Lazaridou, Hughes, Gulcehre, Ortega, Strouse, Leibo, De Freitas. *Social influence as intrinsic motivation for multi-agent deep reinforcement learning.* ICML 2019.
- **[Ye & Lu, 2023]** Ye, Lu. *Mutual-information regularized multi-agent policy iteration.* NeurIPS 2023.
- **[Zhou et al., 2024a]** Zhou, Hong, Kao. *Reciprocal reward influence encourages cooperation from self-interested agents.* NeurIPS 2024.
- **[Park et al., 2026]** Park, Lee, Han. *Focusing influence mechanism for multi-agent reinforcement learning.* arXiv preprint arXiv:2506.19417, 2026.
- **[Mahajan et al., 2019]** Mahajan, Rashid, Samvelyan, Whiteson. *MAVEN: Multi-agent variational exploration.* NeurIPS 2019.
- **[Jo et al., 2024]** Jo, Lee, Yeom, Han. *FOX: Formation-aware exploration in multi-agent reinforcement learning.* AAAI 2024.
- **[Guan et al., 2022]** Guan, Chen, Yuan, Wang, Yin, Zhang, Yu. *Efficient multi-agent communication via self-supervised information aggregation.* NeurIPS 2022.
- **[Ding et al., 2024]** Ding, Du, Ding, Guo, Zhang. *Learning efficient and robust multi-agent communication via graph information bottleneck.* AAAI 2024.
- **[Bae et al., 2026]** Bae, Park, Lee, Han. *LLM-guided communication for cooperative multi-agent reinforcement learning.* ICML 2026.
- **[Goodfellow et al., 2014]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* arXiv preprint arXiv:1412.6572, 2014.
