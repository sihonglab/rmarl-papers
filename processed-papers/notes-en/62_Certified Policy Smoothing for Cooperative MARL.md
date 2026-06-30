# 62. Certified Policy Smoothing for Cooperative Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Certified Policy Smoothing for Cooperative Multi-Agent Reinforcement Learning
- **Authors**: Ronghui Mu, Wenjie Ruan, Leandro Soriano Marcolino, Gaojie Jin, Qiang Ni
- **Affiliation**: Lancaster University (School of Computing & Communication); University of Exeter (Department of Computer Science); University of Liverpool (Department of Computer Science)
- **Venue**: AAAI 2023 (The Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI-23)
- **Link/arXiv**: Tool/code available at https://github.com/TrustAI/CertifyCMARL

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation — l2-norm bounded adversarial perturbation added to each agent's observation at each time step
- **Method paradigm**: Certified robustness via randomized/policy smoothing; false discovery rate (FDR) control with multiple-hypothesis-testing correction; tree-search for global reward lower bound
- **Keywords**: Certified robustness, randomized smoothing, cooperative MARL (c-MARL), false discovery rate (FDR), QMIX/VDN, certified radius

## TL;DR
The first robustness certification method for cooperative multi-agent RL (c-MARL): it builds a smoothed policy and derives per-agent, per-state certified l2 bounds, uses an importance-factor-corrected false discovery rate (FDR) procedure to handle the multiple-test problem across agents, and a tree-search algorithm to certify a lower bound on the global team reward, yielding tighter bounds than state-of-the-art RL certification methods.

## Problem & Motivation
Cooperative multi-agent RL (c-MARL) is widely deployed in safety-critical scenarios (autonomous cars, traffic-light control, wireless communication), and DNN-based RL policies are known to be vulnerable to tiny, human-invisible perturbations of observations or environments. While robustness certification has been studied for single-agent RL, it had not been explored for c-MARL. Certifying c-MARL is harder than single-agent RL for two reasons: (i) the joint action space grows exponentially with the number of agents and all agents must be certified simultaneously, accumulating uncertainty; and (ii) changing one agent's action may not alter the team reward, so single-agent certification criteria do not transfer directly. These gaps motivate new per-state and per-trajectory certification criteria tailored to teams of agents.

## Robustness Setting
- **Threat model / uncertainty set**: Following standard adversarial attacks on c-MARLs (e.g., Lin et al. 2020), an adversarial perturbation is added to each step's observation of each agent; the policy must be provably robust against perturbations bounded by the l2-norm around each agent's observation. The certified bound ϵt ∈ R^N is the maximum perturbation applied to each agent's observation at step t; the paper focuses on value-based c-MARLs under l2-norm bounded attack (extendable to lp via different sampling distributions).
- **Setting**: cooperative (fully cooperative Dec-POMDP); centralized-training-decentralized-execution (CTDE), value-based c-MARLs (VDN, QMIX); certification is done at inference/test time (analysis of trained models).

## Method
- Defines a **smoothed policy**: at each step, each agent's observation is perturbed by i.i.d. Gaussian noise N(0, σ²I), and the joint smoothed policy selects the most frequently chosen action (estimated by Monte Carlo sampling, e.g., 10,000 samples), rather than smoothing the action-value function as in prior single-agent work.
- **Per-agent certified radius**: using a Chi-Square approximation (Goodman 1965) to bound the lower probability of the most frequent action (p_am,n) and upper probability of the runner-up (p_ar,n), each agent n gets a certified radius dn = (σ/2)(Φ⁻¹(p_am,n) − Φ⁻¹(p_ar,n)); the per-state bound is set to the least robust agent, D = min{d1,...,dN}.
- **Per-state certification with correction (CRSC, Algorithm 2)**: addresses the multiple-testing problem (N·T tests over the trajectory) by treating each agent's certification as a one-sided binomial hypothesis test, computing an importance factor IF_n from a COMA-style counterfactual advantage (comparing Q(s,a) to a baseline that alters agent n's action), multiplying each p-value by the importance factor, then running the Benjamini-Hochberg (BH) procedure to control the selective false discovery rate (FDR) and obtain the certified agent set Icert.
- **Global reward certification (T-CRGR, Algorithm 3)**: a tree-search method — when an agent's bound cannot be certified at a step, the second-most-frequent action spawns a new branch/trajectory; exploring all trajectories and taking the minimum reward over leaf nodes yields the certified lower bound of the global team reward; pruning (requiring non-negative per-step reward) controls tree size.

## Theoretical Contributions
- **Proposition 1**: with probability at least (1−α), the smoothed policy chooses action set am for all perturbations ||ϵt||2 ≤ D (intuitive per-state certification).
- **Corollary 1 / Corollary 2**: per-agent and per-state certified bounds dn = (σ/2)(Φ⁻¹(p_am,n) − Φ⁻¹(p_ar,n)) under the condition P(π̃n(zn)=am,n) ≥ 0.5.
- **Theorem 2**: for each certified agent in Icert, the action satisfies π̃n(zn+ϵn)=π̃n(zn) for ||ϵn||2 ≤ D = min(dn), after applying the importance-factor-corrected BH/FDR procedure.
- Builds on Theorem 1 (Cohen, Rosenfeld, and Kolter 2019) randomized smoothing for classification. (Full proofs in appendices.)

## Experiments
- **Environment/Benchmark**: Single-agent — "Freeway" (OpenAI Gym). c-MARL — "Checkers" (2 agents) and "Switch/Switches" (4 agents) from ma-gym; extra experiments in "Traffic Junction" (4 and 10 agents) in appendix.
- **Baselines**: Single-agent — CROP-LORE (Wu et al. 2021), with the same setting for fair comparison. c-MARL — no existing certification solution, so PGD attack (Kurakin, Goodfellow, and Bengio 2018) is used to demonstrate validity of the certified bounds. RL algorithms certified: DQN trained by SA-MDP (PGD) and SA-MDP (CVX) (Zhang et al. 2020a) for single agent; VDN and QMIX for c-MARL.
- **Evaluation metrics**: Certified radius/bound ϵ (per-agent, per-state, global), certified lower bound of total/global reward vs. empirical reward under PGD attack, across smoothing variances σ = 0.03, 0.06, 0.1; α = 0.05 (single-agent), α = 0.01 (c-MARL); 10,000 smoothing samples; γ = 1.0.

## Key Results
- On single-agent Freeway, the proposed method obtains a **tighter certified lower bound of total reward** than the CROP-LORE baseline (Wu et al. 2021), because it uses the probability of selecting the most frequent action (excluding never-chosen actions) rather than a Lipschitz-bounded action-value function.
- For c-MARL, the method certifies the robustness of all c-MARL models (VDN, QMIX) across environments; e.g., on Checkers (2 agents) VDN reward 79.84 and QMIX reward 19.96 across σ values, with certified ϵ increasing as σ increases.
- **VDN achieves higher reward but is less robust (lower ϵ_cert) than QMIX**: VDN simply adds the two agents' rewards for centralization, letting one agent adopt a lazier strategy once another learns a useful one, whereas QMIX's more complex mixing network captures richer inter-agent relationships and encourages each agent to learn.
- The importance-factor-corrected p-value method means the per-state certified bound does not always take the minimum among all agents, correctly ignoring low-impact agents (observed in Switch with four agents).

## Limitations & Future Work
- Pruning in the global-reward tree search requires per-step rewards to be non-negative; when this fails (e.g., QMIX on Switch with rewards below zero), the trajectory must be run to the end without pruning, increasing cost.
- The work focuses on value-based c-MARLs and l2-norm bounded attacks; extension to other lp norms (via generalized Gaussian / different sampling distributions per Hayes 2020) is noted as possible but not fully demonstrated.
- The smoothing-based certification relies on Monte Carlo sampling (10,000 samples) with confidence (1−α), and accumulated uncertainty across N·T tests remains a scalability challenge that the FDR correction mitigates rather than eliminates.

## Relevance to Survey
This is a cornerstone of the **certified-robustness line** within robust MARL and, by the authors' claim, the first robustness-certification method for cooperative MARL. It connects the single-agent certified-RL line (policy smoothing / randomized smoothing: CROP-LORE, Kumar-Levine-Feizi, Lütjens et al.) and SA-MDP observation-robust RL (Zhang et al. 2020a) to the multi-agent cooperative (CTDE / VDN / QMIX) setting, and sits adjacent to the adversarial-attack-on-c-MARL line (Lin et al. 2020; Pham et al. 2022) and certified-communication robustness (Sun et al. 2022). It exemplifies the "observation/state perturbation + certified bound" theme, distinct from model-uncertainty / minimax adversarial-training lines.

## Related Work (verbatim excerpts from the paper)

> _[Section 1, Introduction]_

"Deep neural networks (DNNs) are known to be vulnerable to tiny, non-random, ideally human-invisible perturbations of the input, which can lead to incorrect predictions (Szegedy et al. 2013; Xu, Ruan, and Huang 2022; Jin et al. 2022; Wang et al. 2022; Mu et al. 2022; Yin, Ruan, and Fieldsend 2022; Ruan et al. 2019; Zhang et al. 2020b). RL has also been shown to be susceptible to perturbation in the observations of an RL agent (Huang et al. 2017; Behzadan and Munir 2017) or in environments (Gleave et al. 2019). Some adversarial defence works for RL are proposed (Donti et al. 2020; Eysenbach and Levine 2021; Shen et al. 2020; Sun et al. 2022) and then towards these defences, stronger attacks are proposed (Salman et al. 2019; Russo and Proutiere 2019). To end this repeated game, Wu et al. (2021) and Kumar, Levine, and Feizi (2021) proposed to use probabilistic approaches to provide robustness certification for RLs. Concerning c-MARL, Lin et al. (2020) addressed the challenges of attacking such systems and proposed adding perturbations to the state space. To date, the robustness certification on c-MARL has not been touched upon by the community."

> _[Section 7, Related work — "Adversarial Attacks on DRLs"]_

"Adversarial Attacks on DRLs Existing attack solutions mainly focused on attacking single-agent RL systems, such as Huang et al. (2017); Lin et al. (2017); Kos and Song (2017); Weng et al. (2019). For attacking c-MARLs, there are notably two existing works. Lin et al. (2020) proposed to train a policy network to find a wrong action that the victim agent is expected to take and set it as the targeted adversarial example. Pham et al. (2022) then proposed to craft a stronger adversary by using a model-based approach."

> _[Section 7, Related work — "Robustness Certification of DRLs"]_

"Robustness Certification of DRLs Majority research on robustness certification concentrated on DNNs (Wang et al. 2023; Zhang, Ruan, and Xu 2023; Ruan, Huang, and Kwiatkowska 2018; Wu et al. 2020; Zhang, Ruan, and Fieldsend 2022; Wang and Ruan 2022). Certification on DRLs is still in its infancy. Lütjens, Everett, and How (2020) first proposed a certified defence on the observations of DRLs. Zhang et al. (2020a) then provided empirically provable certificates to ensure that the action does not change at each state. However, this method cannot certify the robustness of the reward if the action is changed under attacks. To tackle this problem, Kumar, Levine, and Feizi (2021) proposed to directly certify the total reward via randomised smoothing-based defence, but it cannot certify the robustness at action level. Recently, Wu et al. (2021) proposed a policy smoothing method based on the randomised smoothing of the action-value function. However, all existing methods can only work on single-agent systems. To the best of our knowledge, this paper is the first work to certify the robustness of cooperative multi-agent RL systems."

### Cited references (resolved from the paper's bibliography)
- **[Szegedy et al. 2013]** Szegedy, Zaremba, Sutskever, Bruna, Erhan, Goodfellow, Fergus. *Intriguing properties of neural networks.* arXiv preprint arXiv:1312.6199, 2013.
- **[Xu, Ruan, and Huang 2022]** Xu, Ruan, Huang. *Quantifying safety risks of deep neural networks.* Complex & Intelligent Systems, 2022.
- **[Jin et al. 2022]** Jin, Yi, Huang, Schewe, Huang. *Enhancing Adversarial Training with Second-Order Statistics of Weights.* CVPR 2022.
- **[Wang et al. 2022]** Wang, Zhang, Xu, Ruan. *Deep learning and its adversarial robustness: A brief introduction.* Handbook on Computer Learning and Intelligence, Vol. 2, 2022.
- **[Mu et al. 2022]** Mu, Ruan, Marcolino, Ni. *3DVerifier: efficient robustness verification for 3D point cloud models.* Machine Learning, 2022.
- **[Yin, Ruan, and Fieldsend 2022]** Yin, Ruan, Fieldsend. *DIMBA: discretely masked black-box attack in single object tracking.* Machine Learning, 2022.
- **[Ruan et al. 2019]** Ruan, Wu, Sun, Huang, Kroening, Kwiatkowska. *Global Robustness Evaluation of Deep Neural Networks with Provable Guarantees for the Hamming Distance.* IJCAI 2019.
- **[Zhang et al. 2020b]** Zhang, Ruan, Wang, Huang. *Generalizing universal adversarial attacks beyond additive perturbations.* IEEE ICDM 2020.
- **[Huang et al. 2017]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv preprint arXiv:1702.02284, 2017.
- **[Behzadan and Munir 2017]** Behzadan, Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* International Conference on Machine Learning and Data Mining in Pattern Recognition, Springer, 2017.
- **[Gleave et al. 2019]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv preprint arXiv:1905.10615, 2019.
- **[Donti et al. 2020]** Donti, Roderick, Fazlyab, Kolter. *Enforcing robust control guarantees within neural network policies.* arXiv preprint arXiv:2011.08105, 2020.
- **[Eysenbach and Levine 2021]** Eysenbach, Levine. *Maximum entropy RL (provably) solves some robust RL problems.* arXiv preprint arXiv:2103.06257, 2021.
- **[Shen et al. 2020]** Shen, Li, Jiang, Wang, Zhao. *Deep reinforcement learning with robust and smooth policy.* ICML 2020.
- **[Sun et al. 2022]** Sun, Zheng, Hassanzadeh, Liang, Feizi, Ganesh, Huang. *Certifiably Robust Policy Learning against Adversarial Communication in Multi-agent Systems.* arXiv preprint arXiv:2206.10158, 2022.
- **[Salman et al. 2019]** Salman, Li, Razenshteyn, Zhang, Zhang, Bubeck, Yang. *Provably robust deep learning via adversarially trained smoothed classifiers.* NeurIPS 2019.
- **[Russo and Proutiere 2019]** Russo, Proutiere. *Optimal attacks on reinforcement learning policies.* arXiv preprint arXiv:1907.13548, 2019.
- **[Wu et al. 2021]** Wu, Li, Huang, Vorobeychik, Zhao, Li. *Crop: Certifying robust policies for reinforcement learning through functional smoothing.* arXiv preprint arXiv:2106.09292, 2021.
- **[Kumar, Levine, and Feizi 2021]** Kumar, Levine, Feizi. *Policy smoothing for provably robust reinforcement learning.* arXiv preprint arXiv:2106.11420, 2021.
- **[Lin et al. 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* 2020 IEEE Security and Privacy Workshops (SPW), 2020.
- **[Lin et al. 2017]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* arXiv preprint arXiv:1703.06748, 2017.
- **[Kos and Song 2017]** Kos, Song. *Delving into adversarial attacks on deep policies.* arXiv preprint arXiv:1705.06452, 2017.
- **[Weng et al. 2019]** Weng, Dvijotham, Uesato, Xiao, Gowal, Stanforth, Kohli. *Toward evaluating robustness of deep reinforcement learning with continuous control.* ICLR 2019.
- **[Pham et al. 2022]** Pham, Nguyen, Chen, Lam, Das, Weng. *Evaluating Robustness of Cooperative MARL: A Model-based Approach.* arXiv preprint arXiv:2202.03558, 2022.
- **[Wang et al. 2023]** Wang, Xu, Ruan, Huang. *Towards Verifying the Geometric Robustness of Large-scale Neural Networks.* AAAI 2023.
- **[Zhang, Ruan, and Xu 2023]** Zhang, Ruan, Xu. *Reachability Analysis of Neural Network Control Systems.* AAAI 2023.
- **[Ruan, Huang, and Kwiatkowska 2018]** Ruan, Huang, Kwiatkowska. *Reachability analysis of deep neural networks with provable guarantees.* IJCAI 2018.
- **[Wu et al. 2020]** Wu, Wicker, Ruan, Huang, Kwiatkowska. *A game-based approximate verification of deep neural networks with provable guarantees.* Theoretical Computer Science, 807, 2020.
- **[Zhang, Ruan, and Fieldsend 2022]** Zhang, Ruan, Fieldsend. *PRoA: A Probabilistic Robustness Assessment against Functional Perturbations.* ECML/PKDD 2022.
- **[Wang and Ruan 2022]** Wang, Ruan. *Understanding Adversarial Robustness of Vision Transformers via Cauchy Problem.* ECML/PKDD 2022.
- **[Lütjens, Everett, and How 2020]** Lütjens, Everett, How. *Certified adversarial robustness for deep reinforcement learning.* Conference on Robot Learning (CoRL), 2020.
- **[Zhang et al. 2020a]** Zhang, Chen, Xiao, Li, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on observations.* arXiv preprint arXiv:2003.08938, 2020.
