# 57. Robust Multi-Agent Coordination via Evolutionary Generation of Auxiliary Adversarial Attackers

## Metadata
- **Title**: Robust Multi-Agent Coordination via Evolutionary Generation of Auxiliary Adversarial Attackers
- **Authors**: Lei Yuan, Ziqian Zhang, Ke Xue, Hao Yin, Feng Chen, Cong Guan, Lihe Li, Chao Qian, Yang Yu
- **Affiliation**: National Key Laboratory for Novel Software Technology, Nanjing University; Polixir Technologies
- **Venue**: AAAI 2023 (Thirty-Seventh AAAI Conference on Artificial Intelligence)
- **Link/arXiv**: Code available at https://github.com/zzq-bot/ROMANCE

## Taxonomy
- **Robustness / perturbation type targeted**: Action perturbation / malicious action attacks on a limited number of cooperating agents (policy perturbation during testing); robustness of cooperative MARL coordination
- **Method paradigm**: Adversarial training; population-based training; Quality-Diversity (evolutionary) generation of attackers; minimax / worst-case optimization; value decomposition (QMIX) as the base solver
- **Keywords**: cooperative MARL, LPA-Dec-POMDP, adversarial attackers, evolutionary generation, quality-diversity, action robustness

## TL;DR
The paper formalizes robust cooperative MARL under limited malicious action attacks as a Limited Policy Adversary Dec-POMDP (LPA-Dec-POMDP) and proposes ROMANCE, which maintains and evolutionarily generates a diverse, high-quality set of auxiliary adversarial attackers (via a sparse-action quality objective plus a JSD-based diversity regularizer) against which the ego-system is alternately trained to obtain a highly robust coordination policy.

## Problem & Motivation
Cooperative MARL (CMARL) methods mainly address MARL-specific challenges (non-stationarity, credit assignment, scalability) but ignore the policy-perturbation issue that arises when a trained policy is deployed in a different environment. CMARL systems are known to be vulnerable to attacks, and unpredictable malicious action attacks on some coordinators have not been fully explored in CMARL, neither in problem formulation nor in efficient algorithm design. The paper targets the realistic setting where some coordinators on a team accidentally and unpredictably suffer a limited number of malicious action attacks while the regular coordinators must still complete the intended goal.

## Robustness Setting
- **Threat model / uncertainty set**: An adversarial attacker πadv : S × A × N → A forces some ego-agents to execute perturbed joint actions â, with a fixed total attack budget K (the number of attacks satisfies Σ_t Σ_{i∈N} I(â_i^t ≠ a_i^t) ≤ K). The attacker is "disentangled" into a victim-selection function v (which agent and when to attack) and a policy-perturbation function g (heuristic-based, e.g., forcing the victim to take the action with the minimum Q-value). The budget is limited to prevent the ego-system from being entirely destroyed.
- **Setting**: cooperative; CTDE / value-decomposition (QMIX, QPLEX, VDN); online adversarial training (alternating between attackers and ego-system).

## Method
- **Problem formulation**: Define the LPA-Dec-POMDP M̂ = ⟨N, S, A, P, K, Ω, O, R, γ⟩ and a disentangled adversarial attacker policy π_adv = v ∘ g; g is heuristic-based and deterministic.
- **Attacker optimization (quality)**: Theorem 1 shows the optimal disentangled attacker corresponds to an optimal victim policy v of a constructed MDP M̄ whose reward is the negated ego-system reward; the attacker is solved with off-the-shelf DRL. Because attacks are sparse (limited to K), Sparsity Prior Regularized Q-learning (SPRQ) is used: a KL regularizer toward a reference distribution that assigns small probability to "attack", giving the SPRQ loss L_opt(ϕ).
- **Diversity regularizer**: To avoid the ego-system overfitting to a specific attacker, a population is maintained; a Jensen-Shannon Divergence (JSD) diversity objective L_div over the population's victim policies is added. The full attacker loss is L_adv(ϕ) = (1/np)Σ L_opt(ϕ_j) − α L_div(ϕ), with α trading off quality vs. diversity.
- **Evolutionary generation (Quality-Diversity)**: An archive Arc_adv (max size na) stores attackers with a quality score (discounted cumulative attacker return) and a behavior (JSD distance to other attackers). Each generation uses fitness-based selection to pick np attackers, treats the L_adv optimization step as an implicit mutation operator, and updates the archive one-by-one, rejecting behaviorally-similar attackers and deleting the oldest when capacity is exceeded.
- **Robustness training paradigm**: Theorem 2/3 show that with a fixed (deterministic or stochastic) attacker, the LPA-Dec-POMDP reduces to a standard Dec-POMDP M̃ (with under-attack transition/reward), so any CMARL algorithm applies. QMIX is used as the solver, minimizing the standard TD loss L_ego(θ); ROMANCE alternately optimizes attackers and ego-system while updating the archive.

## Theoretical Contributions
- **Theorem 1**: Existence of a constructed MDP M̄ whose optimal policy v*, combined with g, yields the optimal disentangled adversarial attacker for the LPA-Dec-POMDP.
- **Theorem 2**: For a fixed deterministic attacker, there exists an equivalent Dec-POMDP M̃ whose optimal policy is optimal for the LPA-Dec-POMDP given π_adv (and extends to a population version).
- **Theorem 3**: For a stochastic attacker, the value function in the constructed Dec-POMDP lower-bounds the value of the same joint policy in the original LPA-Dec-POMDP. (Proofs are in the Appendix.)

## Experiments
- **Environment/Benchmark**: SMAC (StarCraft II unit micromanagement), maps 2s3z, 3m, 3s_vs_3z, 8m, MMM, 1c3s5z; five random seeds, 95% confidence intervals.
- **Baselines**: vanilla QMIX, RANDOM (random attacks during training), RARL (Pinto et al. 2017), RAP (Vinitsky et al. 2020). Integration also tested on QPLEX and VDN. Attacker ablations: EGA, EGA w/o sa, PBA (Population-Based Attackers), ATA (Alternating Training Attackers), RANDOM.
- **Evaluation metrics**: Average test win rate under three settings — "Natural" (no attack), "Random Attack", and "EGA" (out-of-distribution evolutionary-generation-based attackers); generalization across varying attack budgets K; significance via Wilcoxon rank-sum test (confidence level 0.05).

## Key Results
- ROMANCE achieves comparable or better performance than baselines in the "Natural" setting, and clearly superior robustness in the "Random Attack" and especially the strong "EGA" out-of-distribution attack settings (e.g., on 2s3z under EGA: 81.6% vs. RAP 64.1%, vanilla QMIX 26.7%).
- ROMANCE generalizes better than baselines when the test attack budget K differs from training (trained at K=8 on 2s3z, it stays strongest as K increases up to K=14), while vanilla QMIX and RANDOM degrade sharply.
- ROMANCE-generated EGA attackers have higher attack quality and behavior diversity (t-SNE) than PBA/ATA/RANDOM; ablations show the sparse-action regularizer and the diverse population (vs. RARL/RAP) are each necessary; ROMANCE acts as a plug-in that boosts robustness of QMIX, QPLEX, and VDN.

## Limitations & Future Work
- The method learns a disentangled attacker that relies on a heuristic-based policy-perturbation function g; future work could explore more reasonable/efficient perturbations such as observation perturbation and automatic search for the best attack budget for different tasks.
- Designing efficient and effective robust MARL algorithms for the open-environment setting is highlighted as a valuable future direction.

## Relevance to Survey
This paper sits on the action-perturbation / adversarial-attack line of robust cooperative MARL. It introduces a new problem formulation (LPA-Dec-POMDP) for limited malicious action attacks and connects the adversarial-training paradigm of single-agent robust RL (RARL, RAP) with population-based and Quality-Diversity evolutionary methods. It explicitly relates to and contrasts with prior robust MARL works on opponent-policy robustness (M3DDPG), model uncertainty (R-MADDPG), observation perturbation, value-decomposition resilience (RADAR), and communication robustness, making it a useful bridge between adversarial-attack robustness and population/evolutionary diversity methods.

## Related Work (verbatim excerpts from the paper)

> _[Section 2, Related Work — Adversarial training]_

"Adversarial training plays a promising role for the RL robustness (Moos et al. 2022), which involves the perturbations occurring in different cases, such as state, reward, policy, etc. These methods then train the RL policy in an adversarial way to acquire a robust policy in the worst-case situation. Robust adversarial reinforcement learning (RARL) (Pinto et al. 2017) picks out specific robot joints that the adversary acts on to find an equilibrium of the minimax objective using an alternative learning adversary. RARARL (Pan et al. 2019) takes a further step by introducing risk-averse robust adversarial reinforcement learning to train a risk-averse protagonist and a risk-seeking adversary, this approach shows substantially fewer crashes compared to agents trained without an adversary on a self-driving vehicle controller. The mentioned methods only learn a single adversary, and this approach does not consistently yield robustness to dynamics variations under standard parametrizations of the adversary. RAP (Vinitsky et al. 2020) and GC (Song and Schneider 2022) then learn population-based augmentation to the Robust RL formulation. See (Ilahi et al. 2021; Moos et al. 2022) for detailed reviews, and (Smirnova, Dohmatob, and Mary 2019; Zhang et al. 2020a,b; Oikarinen et al. 2021; Xie et al. 2022) for some recent advances."

> _[Section 2, Related Work — Robust MARL]_

"Robust MARL has attracted widespread attention recently (Guo et al. 2022). M3DDPG (Li et al. 2019) learns a minimax extension of MADDPG (Lowe et al. 2017) and trains the MARL policy in an adversarial way, which shows potential in solving the poor local optima caused by opponents' policy altering. In order to model the uncertainty caused by the inaccurate knowledge of the model, R-MADDPG (Zhang et al. 2020c) introduces the concept of robust Nash equilibrium, and treats the uncertainty as a natural agent, demonstrating high superiority when facing reward uncertainty. For the observation perturbation of CMARL, Lin et al. (2020) learn an adversarial observation policy to attack the system, showing that the ego-system is highly vulnerable to observational perturbations. RADAR (Phan et al. 2021) learns resilient MARL policy via adversarial value decomposition. Hu and Zhang (2022) further design an action regularizer to attack the CMARL system efficiently. Xue et al. (2022c) recently consider the multi-agent adversarial communication, learning robust communication policy when some message senders are poisoned. To our knowledge, no previous work has explored CMARL under LPA-Dec-POMDP, neither in problem formulation nor efficient algorithm design."

> _[Section 2, Related Work — ad-hoc teamwork / zero-shot coordination]_

"Furthermore, some other works focus on the robustness when coordinating with different teammates, referring to ad-hoc teamwork (Stone et al. 2010; Gu et al. 2022; Mirsky et al. 2022), or zero-shot coordination (ZSC) (Hu et al. 2020; Lupu et al. 2021; Xue et al. 2022a). The former methods aim at creating an autonomous agent that can efficiently and robustly collaborate with previously unknown teammates on tasks to which they are all individually capable of contributing as team members. While in the ZSC setting, a special case of ad-hoc teamwork, agents work toward a common goal and share identical rewards at each step. The introduction of adversarial attacks makes the victim an unknown teammate with regard to regular agents, while it is even more challenging because the unknown teammate might execute destructive actions. Our proposed method takes a further step toward this direction for robust CMARL."

> _[Introduction — single-agent robust RL background and MARL vulnerability]_

"Training a robust policy before deployment plays a promising role for the mentioned problem and makes excellent progress in single-agent reinforcement learning (SARL) (Moos et al. 2022; Xu et al. 2022). Previous works typically employ an adversarial training paradigm to obtain a robust policy. These methods generally model the process of policy learning as a minimax problem from the perspective of game theory (Yu et al. 2021) and optimize the policy under the worst-case situation (Pinto et al. 2017; Zhang et al. 2020a; Zhang, Wang, and Boedecker 2022). Nevertheless, the multi-agent problem is much more complex (Zhang, Yang, and Bas¸ar 2021), as multiple agents are making decisions simultaneously in the environment. Also, recent works indicate that a MARL system is usually vulnerable to any attack (Guo et al. 2022). Some MARL works study the robustness from various aspects, including the uncertainty in local observation (Lin et al. 2020), model function (Zhang et al. 2020a), and message sending (Xue et al. 2022c). The mentioned methods either focus on investigating the robustness from different aspects, or apply techniques such as heuristic rules and regularizers used in SARL to train a robust coordination policy. However, how unpredictable malicious action attacks cause policy perturbation has not been fully explored in CMARL."

### Cited references (resolved from the paper's bibliography)
- **[Moos et al. 2022]** Moos, Hansel, Abdulsamad, Stark, Clever, Peters. *Robust reinforcement learning: A review of foundations and recent advances.* Machine Learning and Knowledge Extraction, 2022.
- **[Pinto et al. 2017]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Pan et al. 2019]** Pan, Seita, Gao, Canny. *Risk averse robust adversarial reinforcement learning.* ICRA 2019.
- **[Vinitsky et al. 2020]** Vinitsky, Du, Parvate, Jang, Abbeel, Bayen. *Robust reinforcement learning using adversarial populations.* arXiv 2020.
- **[Song and Schneider 2022]** Song, Schneider. *Robust reinforcement learning via genetic curriculum.* ICRA 2022.
- **[Ilahi et al. 2021]** Ilahi, Usama, Qadir, Janjua, Al-Fuqaha, Hoang, Niyato. *Challenges and countermeasures for adversarial attacks on deep reinforcement learning.* IEEE Transactions on Artificial Intelligence, 2021.
- **[Smirnova, Dohmatob, and Mary 2019]** Smirnova, Dohmatob, Mary. *Distributionally robust reinforcement learning.* arXiv 2019.
- **[Zhang et al. 2020a]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* ICLR 2020.
- **[Zhang et al. 2020b]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Oikarinen et al. 2021]** Oikarinen, Zhang, Megretski, Daniel, Weng. *Robust deep reinforcement learning through adversarial loss.* NeurIPS 2021.
- **[Xie et al. 2022]** Xie, Sodhani, Finn, Pineau, Zhang. *Robust policy learning over multiple uncertainty sets.* arXiv 2022.
- **[Guo et al. 2022]** Guo, Chen, Hao, Yin, Yu, Li. *Towards comprehensive testing on the robustness of cooperative multi-agent reinforcement learning.* arXiv 2022.
- **[Li et al. 2019]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019.
- **[Lowe et al. 2017]** Lowe, Wu, Tamar, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[Zhang et al. 2020c]** Zhang, Sun, Tao, Genc, Mallya, Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Lin et al. 2020]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* SPW 2020.
- **[Phan et al. 2021]** Phan, Belzner, Gabor, Sedlmeier, Ritz, Linnhoff-Popien. *Resilient multi-agent reinforcement learning with adversarial value decomposition (RADAR).* AAAI 2021.
- **[Hu and Zhang 2022]** Hu, Zhang. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv 2022.
- **[Xue et al. 2022c]** Xue, Qiu, An, Rabinovich, Obraztsova, Yeo. *Mis-spoke or mis-lead: Achieving robustness in multi-agent communicative reinforcement learning.* AAMAS 2022.
- **[Stone et al. 2010]** Stone, Kaminka, Kraus, Rosenschein. *Ad hoc autonomous agent teams: Collaboration without pre-coordination.* AAAI 2010.
- **[Gu et al. 2022]** Gu, Zhao, Hao, An. *Online ad hoc teamwork under partial observability.* ICLR 2022.
- **[Mirsky et al. 2022]** Mirsky, Carlucho, Rahman, Fosong, Macke, Sridharan, Stone, Albrecht. *A survey of ad hoc teamwork: Definitions, methods, and open problems.* arXiv 2022.
- **[Hu et al. 2020]** Hu, Lerer, Peysakhovich, Foerster. *"Other-Play" for zero-shot coordination.* ICML 2020.
- **[Lupu et al. 2021]** Lupu, Cui, Hu, Foerster. *Trajectory diversity for zero-shot coordination.* ICML 2021.
- **[Xue et al. 2022a]** Xue, Wang, Yuan, Guan, Qian, Yu. *Heterogeneous multi-agent zero-shot coordination by coevolution.* arXiv 2022.
- **[Xu et al. 2022]** Xu, Liu, Huang, Ding, Cen, Li, Zhao. *Trustworthy reinforcement learning against intrinsic vulnerabilities: Robustness, safety, and generalizability.* arXiv 2022.
- **[Yu et al. 2021]** Yu, Gehring, Schäfer, Anandkumar. *Robust reinforcement learning: A constrained game-theoretic approach.* L4DC 2021.
- **[Zhang, Wang, and Boedecker 2022]** Zhang, Wang, Boedecker. *Robust reinforcement learning in continuous control tasks with uncertainty set regularization.* arXiv 2022.
- **[Zhang, Yang, and Bas¸ar 2021]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* Handbook of Reinforcement Learning and Control, 2021.
