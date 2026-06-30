# 84. Unsupervised Partner Design Enables Robust Ad-hoc Teamwork

## Metadata
- **Title**: Unsupervised Partner Design Enables Robust Ad-hoc Teamwork
- **Authors**: Constantin Ruhdorfer, Matteo Bortoletto, Victor Oei, Anna Penzkofer, Andreas Bulling
- **Affiliation**: Collaborative Artificial Intelligence, University of Stuttgart, Stuttgart, Germany
- **Venue**: ICML 2026 (Proceedings of the 43rd International Conference on Machine Learning, PMLR 306)
- **Link/arXiv**: arXiv:2508.06336v2 [cs.LG]; project page https://git.hcics.simtech.uni-stuttgart.de/public-projects/UPD

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to unknown / unseen cooperation partners (ad-hoc teamwork), including human partners, and distribution shift between training and evaluation partner sets; jointly with robustness to unseen procedurally generated environments/levels.
- **Method paradigm**: Curriculum learning over partners (learnability-driven selection), unsupervised environment design (UED) extended to partner space, population-free online partner generation, self-play with PPO/IPPO, joint partner-environment curriculum.
- **Keywords**: Ad-hoc teamwork, zero-shot coordination, unsupervised partner design, learnability, unsupervised environment design, population-free training

## TL;DR
The paper introduces Unsupervised Partner Design (UPD), a population-free multi-agent RL method that generates training partners on-the-fly and selects them adaptively via a learnability (return-variance) criterion, eliminating pre-trained partner populations and hand-tuned mixture coefficients while producing robust ad-hoc teamwork agents that also extend to joint partner-environment curricula.

## Problem & Motivation
Robust cooperation with unknown partners (ad-hoc teamwork, AHT) is brittle when deployment partners differ from those seen in training. Existing AHT methods are costly because they typically rely on large populations of diverse partner policies or hand-crafted expert models, which become increasingly expensive as tasks and partner diversity scale. The population-free E3T method generates partners as stochastic mixtures of the ego and a random policy but still requires careful per-task tuning of the mixture coefficient ε, limiting scalability. In parallel, unsupervised environment design (UED) has shown that adaptive curricula over environment parameters improve generalisation, and recent work argues that generalising jointly across partners and environments is crucial for robust cooperation — yet existing methods struggle to scale to this joint setting. The paper asks (1) whether partners can be generated cheaply and adaptively (analogous to environment design) without explicit populations, and (2) whether such a partner-design mechanism extends naturally to joint partner-environment curricula in procedurally generated settings.

## Robustness Setting
- **Threat model / uncertainty set**: The ego agent is optimised against an unknown evaluation set of partner policies Π_eval (including humans). Since Π_eval is unknown, prior methods learn a best response to a surrogate training set Π_train; mismatch causes distribution shift. UPD instead builds an adaptive online distribution over partner behaviours via a stochastic generator (mixing parameter ε ∼ U(0,1) plus a Dirichlet bias mask over actions), and prioritises partners by learnability (return variance). In the joint setting, uncertainty also covers environment parameters θ (wall/object/agent placements) drawn from a procedural level generator.
- **Setting**: Cooperative, two-agent stochastic game (shared reward); self-play training with a fixed partner per induced environment; online; evaluated zero-shot with diverse artificial partners, held-out levels, and humans.

## Method
- Model each environment instance as an under-specified cooperative two-agent Markov game G_θ; fixing a partner policy π_p induces a single-agent training environment G_{π_p,θ} for the ego agent by marginalising the co-player over its action distribution (Eqs. 2–4).
- **Curriculum over partners**: sample candidate partners from a generator S_p, score each by a learnability function ℓ_var(π_ego, π_p, θ) = Var_τ[R(τ)] (return variance, Eq. 5). High variance indicates partners of intermediate difficulty where cooperation sometimes succeeds; these are prioritised. The paper invokes Foster et al. (2026) to argue that expected one-step policy improvement (for advantage-based PG methods like PPO) is proportional to this variance.
- **Online partner generation (S_p, Alg. 2)**: extend E3T by sampling ε ∼ U(0,1) (spanning a broad competence range) and, with probability p_bias, applying a persistent action bias mask m ∼ Dirichlet(α·1_A) to a random policy, giving π_p = ε·π_{r,m} + (1−ε)·π_ego.
- **Joint UPD (JUPD)**: extend to joint partner-level curricula by sampling (π_p, θ) ∼ S_p × Θ; to correct for differing reward ranges across levels, use a coefficient-of-variation-squared (CV²) score ℓ_CV2 = Var[R]/(E[R]+δ)² (Eq. 6).
- **Algorithm (Alg. 1)**: periodically (every R loops) generate many candidates, score by N rollouts of length L, keep top-|B| by learnability into a buffer B, then sample (π_p, θ) from B and S_p (ratio ρ) and update π_ego with PPO; single training stage, self-play.

## Theoretical Contributions
Mostly empirical, with a conceptual analysis rather than new convergence/sample-complexity proofs. The paper provides: (i) a "UPD and Convention Selection" analysis on a 2×2 coordination matrix game showing that learnability biases UPD toward partners that break the current self-play convention (ℓ_var maximised at p = 0.5), encouraging convention-breaking without hand-engineered mechanisms (Sec. 4.4, Appendix C); (ii) an argument, via Foster et al. (2026), that expected policy improvement is proportional to return variance, motivating learnability as the selection signal; (iii) a computational-cost analysis deriving a break-even population size n⋆ below which UPD is cheaper than population-based two-stage methods (Appendix F).

## Experiments
- **Environment/Benchmark**: Level-Based Foraging (LBF, 7×7 grid, two agents, three foods); Overcooked-AI (five standard layouts: Cramped Room, Asymmetric Advantages, Coordination Ring, Counter Circuit, Forced Coordination); Overcooked Generalisation Challenge (OGC, 5×5 procedurally generated version). A human-AI user study with 12 participants and 144 games. In total 282 trained policies are evaluated.
- **Baselines**: Self-play (SP / IPPO), FCP, MEP, E3T (population-free), and ROTATE (additional comparison in Appendix D); ablations UPD w/o bias and UPD w/o ℓ. For the OGC: DR-DR, Cross-Environment-Cooperation (CEC), and SFLE3T, compared against JUPD.
- **Evaluation metrics**: Average episodic return when paired with diverse unseen evaluation populations Π_eval (and held-out level-partner combinations for OGC); % gain relative to E3T; human-study subjective survey ratings (frustration, adaptiveness, human-likeness, coordination) and returns, with Wilcoxon signed-rank / paired t-tests and Holm-Bonferroni correction.

## Key Results
- In LBF, no swept E3T value of ε (over {0.2,…,0.8}) matches UPD; UPD consistently yields higher average returns with the ten-partner evaluation population, with only marginal extra runtime (<10%).
- In Overcooked-AI (Table 1), UPD attains the best average return (94.4) vs. E3T (78.8), MEP (75.3), FCP (70.0), and SP (41.4), a +18.0% gain over E3T; ablations UPD w/o bias (+10.9%) and UPD w/o ℓ (+14.1%) are also strong, but full UPD is best on average (other methods only beat UPD on CRoom).
- UPD selects different average ε per layout/time and exhibits emergent convention breaking (directional action biases that switch over training) without explicit convention-breaking components; learnability is highest for rare intermediate-difficulty partners.
- In the human-AI study, UPD achieves higher returns and is rated significantly more adaptive, more human-like, a better collaborator, and less frustrating than SP, MEP, and E3T (composite Cronbach's α = 0.916).
- On the OGC (Table 2), JUPD attains the best average return (58.9) vs. DR-DR (49.9), SFLE3T (44.0), and CEC (23.9), demonstrating the joint partner-environment curriculum.

## Limitations & Future Work
- UPD avoids explicit population pretraining but shifts computation toward large-scale online partner evaluation; this tradeoff is favourable in highly vectorised (e.g., JAX) simulators but may be less advantageous where environment interaction is expensive.
- UPD w/o ℓ already performs strongly, implying much of the gain comes from large-scale partner generation/biasing rather than learnability per se; a practical implication is that E3T extended with randomised mixture coefficients plus large-scale parallel generation may already be a stronger population-free baseline.
- The framework is instantiated with SFL and a stochastic generator; exploring richer partner spaces (other UED methods, partner populations, or latent partner spaces, e.g., Liang et al., 2024) is left for future work.
- The human study is small (12 participants), so results demonstrate effectiveness at collaborating with humans rather than establishing UPD as the best method overall. An earlier version had baseline implementation/configuration issues that were corrected (conclusions unchanged).

## Relevance to Survey
This paper sits in the cooperative robustness line of robust MARL — robustness to unknown/unseen partners (ad-hoc teamwork and zero-shot human-AI coordination) and to distribution shift between training and deployment partner sets — rather than the model/transition-uncertainty or adversarial-attack lines. Its key conceptual move is to transplant unsupervised environment design (UED) and learnability-based curricula from the environment/level space into the partner space, and to combine the two into a joint partner-environment curriculum. It connects the AHT/zero-shot-coordination literature (FCP, MEP, E3T, ROTATE) with the UED/open-ended curriculum literature, offering a population-free, generation-and-selection approach to robust cooperation that complements adversarial-training and population-diversity methods in the survey.

## Related Work (verbatim excerpts from the paper)

> _[Section 2.1, Related Work — Ad-hoc Teamwork]_

"AHT was explored in a wide range of multi-agent reinforcement learning (RL) environments (Carroll et al., 2019; Bard et al., 2020; Kurach et al., 2020; Ruhdorfer et al., 2025a). Popular AHT methods, such as fictitious co-play (FCP) (Strouse et al., 2021) or maximum entropy population-based training (MEP) (Zhao et al., 2023), rely on pretraining diverse partner populations and optimising best-response policies for these (Yu et al., 2023; Lou et al., 2023; Rahman et al., 2023; Erlebach & Cook, 2024; You et al., 2025). Recent works incorporated open-ended learning objectives to dynamically expand partner diversity (Li et al., 2023b; Wang et al., 2025), but still involved growing partner populations over time or used curricula over pretrained populations (Erlebach & Cook, 2024) or over a partner model learned from offline data (Chaudhary et al., 2025). A notable exception is E3T (Yan et al., 2023), which generates partners on the fly as mixtures of the ego and a random policy. E3T demonstrated strong performance, outperforming prior population-based approaches such as FCP and MEP in human-AI coordination settings. While this approach does not require any partner population and thus significantly reduces the computational overhead, it still requires careful tuning of mixture coefficients between the ego and random policy for each task and evaluation scenario, limiting robustness across settings. In contrast, we propose a lightweight population-free approach that adaptively generates diverse partner behaviour without fixed parameters or pre-trained populations, and is compatible with existing curriculum learning frameworks."

> _[Section 2.2, Related Work — Unsupervised Environment Design]_

"UED (Dennis et al., 2020) adaptively generates training environments tailored to an agent's capabilities and has proven effective for improving generalisation. Unlike domain randomisation (DR) (Tobin et al., 2017), UED generates environments to target an agent's learning frontier. Existing UED methods mainly focus on single-agent settings and rely on regret-based objectives to guide environment generation (Wang et al., 2019; 2020; Dennis et al., 2020; Jiang et al., 2021b;a; Parker-Holder et al., 2022; Li et al., 2023a; Beukman et al., 2024). Extensions to multi-agent settings are limited: Samvelyan et al. (2023) focused on competitive settings, Ruhdorfer et al. (2025b) proposed a cooperative multi-agent UED benchmark, but no method, while You et al. (2025) trains only with past self-play checkpoints. Recent works reframed UED as a learnability-driven problem, replacing regret-based objectives with scoring functions that directly measure an environment's learning potential (Rutherford et al., 2024; Monette et al., 2025). However, prior work has focused on environment parametrisation only and does not consider partner policies as part of the curriculum space. We extend unsupervised design to partner policies, introducing adaptive partner generation as a population-free curriculum mechanism. When combined with existing UED approaches, this enables joint partner-environment selection in procedurally generated settings for zero-shot cooperation."

> _[Section 3.3, Preliminaries — Unsupervised Environment Design]_

"In single-agent RL, UED algorithms use the free parameters of an environment θ ∈ Θ to create a curriculum using a utility function U. Many algorithms use regret as the UED objective (Dennis et al., 2020; Samvelyan et al., 2023), where θ is selected based on the performance difference between the current and an optimal policy: U(π, θ) = REGRET_θ(π, π*_θ). However, this assumes access to the optimal policy π*_θ. Recent work has thus moved away from regret as utility. Sampling for learnability (SFL) (Rutherford et al., 2024) scores levels using a learnability function that prioritises instances near the agent's learning frontier. For binary outcomes in which R(τ, θ) ∈ {0, 1}, learnability is defined as ℓ_sr(π, θ) = p(1 − p), where p = E_τ∼p(τ|π,θ)[R(τ, θ)] is the success rate on a level. Monette et al. (2025) extended this idea to continuous rewards by weighting return variance around the mean performance. In this work, we apply this idea to partners rather than levels, treating them as training instances that can be generated and selected based on learnability."

### Cited references (resolved from the paper's bibliography)
- **[Bard et al., 2020]** Bard, Foerster, Chandar, Burch, Lanctot, Song, et al. *The Hanabi challenge: A new frontier for AI research.* Artificial Intelligence, 2020.
- **[Beukman et al., 2024]** Beukman, Coward, Matthews, Fellows, Jiang, Dennis, Foerster. *Refining minimax regret for unsupervised environment design.* ICML 2024.
- **[Carroll et al., 2019]** Carroll, Shah, Ho, Griffiths, Seshia, Abbeel, Dragan. *On the utility of learning about humans for human-AI coordination.* NeurIPS 2019.
- **[Chaudhary et al., 2025]** Chaudhary, Liang, Chen, Du, Jaques. *Improving human-AI coordination through adversarial training and generative models.* CoRR abs/2504.15457, 2025.
- **[Dennis et al., 2020]** Dennis, Jaques, Vinitsky, Bayen, Russell, Critch, Levine. *Emergent complexity and zero-shot transfer via unsupervised environment design.* NeurIPS 2020.
- **[Erlebach & Cook, 2024]** Erlebach, Cook. *RACCOON: Regret-based adaptive curricula for cooperation.* Coordination and Cooperation for Multi-Agent RL Methods Workshop, 2024.
- **[Jiang et al., 2021a]** Jiang, Dennis, Parker-Holder, Foerster, Grefenstette, Rocktäschel. *Replay-guided adversarial environment design.* NeurIPS 2021.
- **[Jiang et al., 2021b]** Jiang, Grefenstette, Rocktäschel. *Prioritized level replay.* ICML 2021.
- **[Kurach et al., 2020]** Kurach, Raichuk, Stanczyk, Zajac, Bachem, Espeholt, et al. *Google research football: A novel reinforcement learning environment.* AAAI 2020.
- **[Li et al., 2023a]** Li, Varakantham, Li. *Generalization through diversity: improving unsupervised environment design.* IJCAI 2023.
- **[Li et al., 2023b]** Li, Zhang, Sun, Du, Wen, Wang, Pan. *Cooperative open-ended learning framework for zero-shot coordination.* ICML 2023.
- **[Lou et al., 2023]** Lou, Guo, Zhang, Wang, Huang, Du. *PECAN: leveraging policy ensemble for context-aware zero-shot human-AI coordination.* AAMAS 2023.
- **[Monette et al., 2025]** Monette, Letcher, Beukman, Jackson, Rutherford, Goldie, Foerster. *An optimisation framework for unsupervised environment design.* Reinforcement Learning Journal, 2025.
- **[Parker-Holder et al., 2022]** Parker-Holder, Jiang, Dennis, Samvelyan, Foerster, Grefenstette, Rocktäschel. *Evolving curricula with regret-based environment design.* ICML 2022.
- **[Rahman et al., 2023]** Rahman, Fosong, Carlucho, Albrecht. *Generating teammates for training robust ad hoc teamwork agents via best-response diversity (BRDiv).* TMLR 2023.
- **[Ruhdorfer et al., 2025a]** Ruhdorfer, Bortoletto, Bulling. *The Yokai learning environment: Tracking beliefs over space and time.* arXiv:2508.12480, 2025.
- **[Ruhdorfer et al., 2025b]** Ruhdorfer, Bortoletto, Penzkofer, Bulling. *The Overcooked Generalisation Challenge: Evaluating cooperation with novel partners in unknown environments using unsupervised environment design.* TMLR 2025.
- **[Rutherford et al., 2024]** Rutherford, Beukman, Willi, Lacerda, Hawes, Foerster. *No regrets: Investigating and improving regret approximations for curriculum discovery (Sampling for Learnability, SFL).* NeurIPS 2024.
- **[Samvelyan et al., 2023]** Samvelyan, Khan, Dennis, Jiang, Parker-Holder, Foerster, Raileanu, Rocktäschel. *MAESTRO: Open-ended environment design for multi-agent reinforcement learning.* ICLR 2023.
- **[Strouse et al., 2021]** Strouse, McKee, Botvinick, Hughes, Everett. *Collaborating with humans without human data (FCP).* NeurIPS 2021.
- **[Tobin et al., 2017]** Tobin, Fong, Ray, Schneider, Zaremba, Abbeel. *Domain randomization for transferring deep neural networks from simulation to the real world.* IROS 2017.
- **[Wang et al., 2019]** Wang, Lehman, Clune, Stanley. *Paired Open-Ended Trailblazer (POET): endlessly generating increasingly complex and diverse learning environments and their solutions.* CoRR abs/1901.01753, 2019.
- **[Wang et al., 2020]** Wang, Lehman, Rawal, Zhi, Li, Clune, Stanley. *Enhanced POET: open-ended reinforcement learning through unbounded invention of learning challenges and their solutions.* ICML 2020.
- **[Wang et al., 2025]** Wang, Rahman, Cui, Sung, Stone. *ROTATE: Regret-driven open-ended training for ad hoc teamwork.* arXiv:2505.23686, 2025.
- **[Yan et al., 2023]** Yan, Guo, Lou, Wang, Zhang, Du. *An efficient end-to-end training approach for zero-shot human-AI coordination (E3T).* NeurIPS 2023.
- **[You et al., 2025]** You, Ha, Lee, Kim. *Automatic curriculum design for zero-shot human-AI coordination.* IEEE Access, 2025.
- **[Yu et al., 2023]** Yu, Gao, Liu, Xu, Tang, Yang, Wang, Wu. *Learning zero-shot cooperation with humans, assuming humans are biased.* ICLR 2023.
- **[Zhao et al., 2023]** Zhao, Song, Yuan, Hu, Gao, Wu, Sun, Yang. *Maximum entropy population-based training for zero-shot human-AI coordination (MEP).* AAAI 2023.
