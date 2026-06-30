# 19. Scalable Robust Multi-Agent Reinforcement Learning for Model Uncertainty

## Metadata
- **Title**: Scalable Robust Multi-Agent Reinforcement Learning for Model Uncertainty
- **Authors**: Younkyung Jwa, Minseon Gwak, Jiin Kwak, Chang Wook Ahn, PooGyeon Park
- **Affiliation**: Gwangju Institute of Science and Technology (GIST); Pohang University of Science and Technology (POSTECH); Ulsan National Institute of Science and Technology (UNIST), Korea
- **Venue**: 2023 62nd IEEE Conference on Decision and Control (CDC)
- **Link/arXiv**: DOI: 10.1109/CDC49753.2023.10383458

## Taxonomy
- **Robustness / perturbation type targeted**: Model uncertainty, specifically reward-function uncertainty (noisy rewards drawn from a truncated Gaussian), combined with scalability to many agents
- **Method paradigm**: Robust Markov game with nature actor, actor-critic (MADDPG-style), attention-based architecture, evolutionary population curriculum learning, minimax / worst-case robust Nash equilibrium
- **Keywords**: scalable MARL, robust Nash equilibrium, model uncertainty, nature actor, attention mechanism, population curriculum, evolutionary learning

## TL;DR
The paper proposes the Evolutionary Diversity-maintaining Population Curriculum (EDPC) framework combined with a Robust Attention-based MADDPG (RA-MADDPG) algorithm to scale robust MARL under model (reward) uncertainty, using attention-based nature actors and diversity-preserving evolutionary operators to find robust Nash equilibria efficiently as the number of agents grows.

## Problem & Motivation
Robust MARL methods such as R-MADDPG can find a robust Nash equilibrium of a Markov game with model uncertainty by treating uncertainty as an additional (nature) agent, but as the system scales up the search space required to find robust NEs expands dramatically, weakening the robustness property in environments with many agents. Conversely, existing scalable MARL frameworks (e.g., the Evolutionary Population Curriculum, EPC) have been developed only in uncertainty-ignorant environments, and the EPC's rule-based population generation restricts population diversity, with no clear extension to settings involving model uncertainty. The paper addresses the gap of achieving both robustness and scalability simultaneously in MARL.

## Robustness Setting
- **Threat model / uncertainty set**: Model uncertainty defined as uncertainty in each agent's reward function. A reward r̄ⁱ_{t,σ} is drawn from a truncated Gaussian distribution with mean equal to the original reward rⁱ_t, standard deviation σ (noise rate), and truncation threshold [−θ, θ]. The robust Markov game Ḡ_σ defines uncertainty sets R̄ⁱ for rewards (and a corresponding set T̄ of transition probabilities). Uncertainty is treated as a virtual adversarial "nature" agent acting against each agent.
- **Setting**: Cooperative (fully-cooperative food-collection environment); centralized critic with decentralized actors (MADDPG-style CTDE); online, model-free actor-critic.

## Method
- **Robust actor-critic with nature actors (RA-MADDPG)**: Introduces a set of nature actor policies π0 = {π0,i(·|s)}, each constrained within the reward uncertainty set R̄ⁱ_s, acting as virtual adversaries. The nature actor's parameters are updated to reduce both the gap between predicted and observed reward and the predicted reward value itself (a conservative reward estimate). The critic is trained using the nature actor's reward instead of the received reward, producing a robust Q-value; the loss is a TD-style mean-squared error with target y_t computed from the nature actor and target critic.
- **Attention-based networks**: To handle varying numbers of agents across curriculum stages with a fixed parameter count, the nature actor, critic, and policy networks use self-attention modules. The nature actor network produces a global attention embedding vⁱ as a softmax-weighted sum of observation-action encodings of other agents; policy networks process only observations while critic and nature actor networks process both observations and actions.
- **EDPC curriculum (Algorithm 1)**: MARL is divided into S stages, starting with few agents and doubling them at each stage by merging two parent agent sets. A population of K individuals (agent sets) is trained in parallel with RA-MADDPG; reward serves as a fitness metric (genetic-algorithm view: stage = generation, agent set = individual, agent = gene).
- **Reward-proportionate parent selection (Sec. IV-B)**: Two parents per next-generation individual are chosen with probability proportional to scaled average reward r′_A = e^{α|r_A|/r_max}, so even low-reward individuals can be selected, maintaining diversity (vs. EPC's top-n selection).
- **Reward-guided mutation (Algorithm 2)**: With probability µ, each agent (gene) is replaced by a randomly chosen agent from a candidate set restricted to (i) cooperating agents in the same individual and (ii) agents with higher mean episode reward, preserving cooperation while increasing diversity and reward.

## Theoretical Contributions
None / mostly empirical. The paper builds on the robust Markov game formulation and robust NE definition from prior work [18] and contributes algorithmic and architectural designs; no new convergence or sample-complexity proofs are provided.

## Experiments
- **Environment/Benchmark**: Food collection environment (from [21], based on the environment in [24]); N cooperative agents must occupy N foods, maximizing foods consumed while avoiding collisions. Reward +6/N when food is eaten, −6/N penalty per collision, plus a navigation reward (negative distance to nearest food). Target system is 12 agents; EPC/EDPC use 3 stages with 3, 6, and 12 agents.
- **Baselines**: MADDPG [16], R-MADDPG [18], EPC [21], and the proposed EDPC.
- **Evaluation metrics**: Average reward over all agents (fully-cooperative setting) after To = 10⁴ test episodes, evaluated under noise rates σ = 1, 2, 3, 6 with θ = 2, for 6- and 12-agent systems; learning curves and an ablation study on the two diversity-maintaining components.

## Key Results
- EDPC achieves the highest average reward across all noise rates and agent counts; e.g., in the 12-agent system at noise rate σ = 6, EDPC reaches 54.151 vs. EPC 7.751, R-MADDPG −1.754, and MADDPG 0.507 (Table I).
- MADDPG and R-MADDPG reward tends to decrease as noise rate increases; despite being designed for model uncertainty, R-MADDPG fails to find robust NEs well under scaling. EPC beats MADDPG/R-MADDPG at low noise but degrades rapidly as uncertainty grows.
- Ablation (Table II, 12-agent): adding reward-guided mutation and then reward-proportionate parent selection on top of the EPC baseline consistently improves reward, indicating diversity maintenance promotes discovery of optimal robust NEs.
- EDPC performance increases as stages evolve despite the growing number of agents, demonstrating scalable robustness.

## Limitations & Future Work
- Evaluated only in a fully-cooperative environment; behavior with non-cooperative agents is not studied. The authors note future work to verify EDPC where non-cooperative agents exist and to develop more general and versatile MARL algorithms.
- Model uncertainty is limited to reward-function uncertainty; transition uncertainty is included in the formulation but not separately evaluated.
- No theoretical guarantees on convergence to robust NEs are provided.

## Relevance to Survey
This paper sits on the "model/environment uncertainty" main line of robust MARL and directly extends the robust Markov game / nature-player paradigm of Zhang et al.'s R-MADDPG ([18] here; the survey's paper #1) toward the scalability dimension. It connects the robust-MARL line to scalable MARL (evolutionary population curriculum, attention-based architectures) and to evolutionary / curriculum learning method lines, making it a key reference for the intersection of robustness and scalability in cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction]_

"In reinforcement learning (RL) research, robustness has been explored with the concern of various uncertain factors, such as observations [9], [10], actions [11], and models [12]–[15]. In multi-agent environments where agents influence each other, uncertainty makes it more difficult for an agent to predict what other agents will do, which may lead to performance degradation [16], [17]. In [18], a robust MADDPG (R-MADDPG) algorithm is proposed considering uncertainty in the rewards given to agents. To address the problem of model uncertainty in MARL, the algorithm leverages the idea of a zero-sum game between agents and uncertainty, treating the uncertainty as an additional agent [19]. The R-MADDPG achieves robust policies by reaching a robust Nash equilibrium (NE) of the game. However, as the system scales up, the expansion of the search space required to find robust NEs increases accordingly."

> _[Section I, Introduction]_

"The scaling problem in MARL has been handled in uncertainty-ignorant environments [8], [20]–[22]. One notable scalable MARL framework is an evolutionary population curriculum (EPC) [21]. In the EPC, the learning process is divided into multiple stages, starting from an environment with fewer agents and gradually increasing the number of agents at each stage. Although the scaling method of the EPC contributes to a structured search space expansion, the population generated from the previous stage is formed according to some specified rules, which restricts the population diversity. Furthermore, it remains unclear how this approach can be extended to environments that involve model uncertainty."

### Cited references (resolved from the paper's bibliography)
- **[8]** G. Qu et al. *Scalable multi-agent reinforcement learning for networked systems with average reward.* Advances in Neural Information Processing Systems, 33:2074–2086, 2020.
- **[9]** H. Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* Advances in Neural Information Processing Systems, 33:21024–21037, 2020.
- **[10]** Z. Lu et al. *Decentralized fault tolerant control for modular robot manipulators via integral terminal sliding mode and disturbance observer.* Int. J. Control Autom. Syst., 20(10):3274–3284, 2022.
- **[11]** C. Tessler et al. *Action robust reinforcement learning and applications in continuous control.* ICML 2019 (PMLR), pages 6215–6224.
- **[12]** L. Pinto et al. *Robust adversarial reinforcement learning.* ICML 2017 (PMLR), pages 2817–2826.
- **[13]** D. Mankowitz et al. *Learning robust options.* Proceedings of the AAAI Conference on Artificial Intelligence, vol. 32, 2018.
- **[14]** Y. Wang and S. Zou. *Online robust reinforcement learning with model uncertainty.* Advances in Neural Information Processing Systems, 34:7193–7206, 2021.
- **[15]** V. T. Vu et al. *Online actor-critic reinforcement learning control for uncertain surface vessel systems with external disturbances.* Int. J. Control Autom. Syst., 20(3):1029–1040, 2022.
- **[16]** R. Lowe et al. *Multi-agent actor-critic for mixed cooperative-competitive environments.* Advances in Neural Information Processing Systems, 30, 2017.
- **[17]** S. Li et al. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* Proceedings of the AAAI Conference on Artificial Intelligence, vol. 33, pages 4213–4220, 2019.
- **[18]** K. Zhang et al. *Robust multi-agent reinforcement learning with model uncertainty.* Advances in Neural Information Processing Systems, 33:10571–10583, 2020.
- **[19]** X. Zhu et al. *Data-driven multiplayer mixed-zero-sum game control of modular robot manipulators with uncertain disturbance.* Int. J. Control Autom. Syst., 21(2):645–657, 2023.
- **[20]** G. Qu et al. *Scalable reinforcement learning of localized policies for multi-agent networked systems.* Learning for Dynamics and Control, pages 256–266, PMLR, 2020.
- **[21]** Q. Long et al. *Evolutionary population curriculum for scaling multi-agent reinforcement learning.* arXiv preprint arXiv:2003.10423, 2020.
- **[22]** C. D. Hsu et al. *Scalable reinforcement learning policies for multi-agent control.* 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 4785–4791, IEEE, 2021.
