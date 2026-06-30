# 182. Robust and Diverse Multi-Agent Learning via Rational Policy Gradient

## Metadata
- **Title**: Robust and Diverse Multi-Agent Learning via Rational Policy Gradient
- **Authors**: Niklas Lauffer, Ameesh Shah, Micah Carroll, Sanjit A. Seshia, Stuart Russell, Michael Dennis
- **Affiliation**: UC Berkeley; Google DeepMind
- **Venue**: NeurIPS 2025
- **Link/arXiv**: rational-policy-gradient.github.io (code: github.com/niklaslauffer/rational-policy-gradient)

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents / partner-strategy robustness in general-sum (especially cooperative) games; robustness to differing/unseen partners, adversarial example discovery, and policy diversity. Addresses the "self-sabotage" failure mode of naive adversarial optimization in cooperative settings.
- **Method paradigm**: Adversarial optimization, opponent shaping, policy gradient with higher-order (meta-)gradients, best-response rationality constraint, auto-curriculum / population-based diversity, cross-play.
- **Keywords**: Rationality-preserving Policy Optimization (RPO), Rational Policy Gradient (RPG), opponent shaping, self-sabotage, adversarial training, cross-play diversity

## TL;DR
The paper introduces Rationality-preserving Policy Optimization (RPO) — an adversarial-optimization formalism that constrains adversarial agents to remain rational (a best response to some possible partner) — and Rational Policy Gradient (RPG), an opponent-shaping-based gradient method that solves it, thereby extending adversarial optimization from zero-sum to general-sum/cooperative settings without inducing self-sabotage.

## Problem & Motivation
Adversarial optimization (explicitly searching for flaws in agents' policies by minimizing others' rewards) is highly successful for finding robust and diverse policies in zero-sum settings via self-play, but its naive application in cooperative/general-sum settings causes a critical failure mode: agents are irrationally incentivized to self-sabotage — an adversary can simply refuse to collaborate or actively sabotage its teammate's (and its own) reward, blocking task completion and halting meaningful learning. Existing fixes for cross-play diversity algorithms (making self-play and cross-play observation distributions similar) are shown to fail in many environments. The paper aims to reap the benefits of adversarial optimization in cooperative settings while eliminating self-sabotage.

## Robustness Setting
- **Threat model / uncertainty set**: An adversarial objective minimizes another agent's reward to expose/fix policy flaws. The key restriction is that any adversarial agent's policy must be *rational*, i.e., a best response to at least one possible co-policy (∃π′_{-i} s.t. π_i ∈ BR(π′_{-i})), which prevents the adversary from playing strictly dominated/self-sabotaging actions. Robustness is measured against differing/unseen partners via cross-play.
- **Setting**: General-sum partially-observable stochastic games, with emphasis on cooperative and mixed-motive games (two-player focus in exposition); decentralized agents with stochastic Markovian (optionally history-dependent) policies; online / model-free deep RL training; manipulators used only during training and discarded at execution.

## Method
- **RPO formalism**: For each agent i with adversarial objective O_i, maximize O_i subject to the rationality constraint that π_i is a best response to some co-policy π′_{-i}. The constraint has no effect on agents with non-adversarial objectives (e.g., the victim in adversarial training).
- **RPG solution**: Introduce a *manipulator* policy π^M_{-i} for each *base* agent π_i. Base agents only optimize to be a best response against their manipulator (enforcing rationality); manipulators carry the original adversarial objective O_i and can influence it only indirectly by shaping which policy the base agents best-respond to.
- **Opponent-shaping gradients**: Base agents take a straightforward policy-gradient step; manipulators take higher-order gradients through the base agents' updates (building on LOLA-style opponent shaping). Gradients are estimated from samples using a Loaded DiCE surrogate loss that preserves higher-order dependencies (magic-box operator).
- **Partner-play regularization**: Add a small (ε-weighted) amount of rollouts of each base agent partnered with its evaluation partners to the training data, to counter the train/eval partner distribution shift and prevent manipulators from "cheating" by pushing base agents out-of-distribution.
- **Algorithm 1 (RPG update with lookahead N)**: Copy base params; perform N lookahead gradient steps on base agents against manipulators; roll out updated base agents; apply a DiCE-modified manipulator gradient step on O_i evaluated at the looked-ahead base params; apply a single base-agent gradient step. RPG is agnostic to the underlying RL algorithm.
- **Five RPG algorithms**: AP-RPG (find rational adversarial examples in fixed agents), AT-RPG (robustify a learning agent), PAIRED-RPG (regret-based robustification), PAIRED-A-RPG (find flaws maximizing regret), and XPD-RPG (cross-play diversity that produces an auto-curriculum for robust, genuinely diverse policies).

## Theoretical Contributions
None / mostly empirical. The paper provides a formalism (RPO) and worked matrix-game examples, but states it has no theory contribution and no formal guarantee of convergence to truly rational strategies (left as future work).

## Experiments
- **Environment/Benchmark**: Matrix games (zero-sum, cooperative, mixed-motive payoffs); several Overcooked layouts (cramped room, forced coordination, counter circuit, coordination ring); a modified STORM (collect green/red coins, including "unobserved STORM" and a sabotage-incentive variant); a simplified 2-player Hanabi with 3 colors/ranks and 4 colors/ranks. Latter three use the JaxMARL implementation.
- **Baselines**: Self-play (SP, with entropy coefficients 0.01 and 0.05); adversarial policy (AP); adversarial training (AT); PAIRED; a cross-play diversity (XPD) baseline (similar to LIPO without mutual-information term / SPWR; effectively ADVERSITY in fully-observed settings); CoMeDi (prior SOTA for preventing self-sabotage in cross-play diversity).
- **Evaluation metrics**: Self-play vs. cross-play rewards; cross-play grids / intra-population cross-play reward (robustness to differing partners); reward of fixed victims under different adversarial attacks (Table 1); training curves; presence/absence of self-sabotage.

## Key Results
- XPD-RPG learns meaningfully diverse policies while avoiding self-sabotage: in STORM and Overcooked it maintains high cross-play reward, whereas CoMeDi and XPD drive cross-play reward toward zero by sabotaging (e.g., blocking the plate dispenser in Overcooked).
- RPG trains more robust policies: XPD-RPG performs nearly perfectly with arbitrary partners in cross-play grids across Overcooked and Hanabi, while SP/XPD often achieve close to zero reward with policies from other algorithms.
- RPG finds non-trivial (rational) adversarial examples: in unobserved STORM, AP-RPG and PAIRED-A-RPG expose victim weaknesses without sabotage, while PAIRED-RPG/AT-RPG victims score highly against attacks; in Overcooked, AP-RPG reduces a self-play victim's reward from 240 to 4.6 via a rational (counterclockwise) strategy. The plain AP attack trivially yields zero reward via self-sabotage, and non-RPG variants (AT, PAIRED, XPD) fail during training due to self-sabotage.
- Larger RPG lookahead stabilizes otherwise-unstable multi-agent learning dynamics, converging on (otherwise unstable) mixed equilibria in matrix games.

## Limitations & Future Work
- RPG relies on higher-order gradients through agents' learning updates, adding computational overhead (roughly linear in the number of optimizing agents; XPD-RPG is ~3x slower than XPD). Sample-based higher-order gradient estimation has high variance and needs large batch sizes; recent meta-gradient stabilization methods could be incorporated.
- No formal guarantee that RPG converges to truly rational strategies; characterizing when RPG solves RPO is left to future work.
- Future: incorporate cheaper model-free opponent shaping to improve efficiency; extend to more sophisticated RL algorithms (PPO clipping was avoided due to interference with higher-order gradients).

## Relevance to Survey
This paper sits on the "robustness to partners / adversarial agents" and "adversarial-training / opponent-shaping" method lines of robust MARL, specifically tackling robustness and diversity in cooperative and general-sum games rather than the zero-sum or model/environment-uncertainty settings of much robust MARL theory. It connects adversarial RL (adversarial policies/training), unsupervised environment design (PAIRED), and ad-hoc teamwork / zero-shot coordination literatures, and contributes a general formalism (RPO) and algorithm (RPG) that fixes the self-sabotage failure of naive adversarial optimization — a useful reference for the adversarial-training-for-robustness and population-diversity branches of the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 6, Related Works]_

"Prior work [Cui et al., 2023, Sarkar et al., 2024] has identified the phenomenon of self-sabotage in the context of cross-play diversity algorithms and proposed fixes based on making the observation distributions of self-play and cross-play similar. Our experiments show that the approach from Sarkar et al. [2024] fails to prevent sabotage in all of our environments and that [Cui et al., 2023] fails in Overcooked and matrix games, since our XPD baseline is effectively identical to ADVERSITY in fully-observed settings. See Section C for a detailed discussion of why. Several simultaneous works [Ruhdorfer et al., 2025, Wang et al., 2025, Chaudhary et al., 2025] have explored the idea of extending the adversarial training algorithm to the cooperative setting to improve robustness against unseen partners. Specifically, Wang et al. [2025] and Chaudhary et al. [2025] encounter the problem of self-sabotage and attempt to fix it by mixing state distributions across self-play and cross-play and by limiting the adversarial search space via a generative model, respectively. However, none of these methods propose a complete framework for preventing self-sabotage across any adversarial optimization algorithm in the way that we do."

"There are several other paradigms for training more performant or robust policies in cooperative settings. Approaches based on the setting of zero-shot coordination Hu et al. [2020], Treutlein et al. [2021], Muglich et al. [2022] aim to learn policies that do not depend on arbitrary symmetries of the game. Several other methods aim make policies robust by training them against a population of agents Vinyals et al. [2019], Rahman et al. [2022] or against human-data-informed policies Carroll et al. [2019], [FAIR], Liang et al. [2024]. Our work differs from all of these by directly applying different forms of adversarial optimization and does not rely on collecting human data."

"A significant part of the technical backing of RPG is based on the line of work on opponent shaping [Foerster et al., 2017, Kim et al., 2021, Letcher et al., 2018]. To the best of the author's knowledge, RPG represents the first use of opponent shaping in the context of adversarial training. A more recent line of work [Lu et al., 2022, Khan et al., 2023] aims to achieve opponent shaping without having to explicitly compute expensive higher-order gradients. Investigating whether this type of shaping could be incorporated into RPG to improve efficiency would be an exciting line of future research."

> _[Introduction]_

"A longstanding challenge in the field of multi-agent reinforcement learning (MARL) is that of learning robust behavior: individual agents should be able to adapt to a variety of different strategies that other agents might exhibit. One way to achieve robustness is by training agents to iteratively find and fix flaws in their policy. In zero-sum settings, this can be naturally achieved through self-play [Samuel, 1959, Silver et al., 2016], where agents train against copies of themselves. Due to the adversarial nature of zero-sum self-play, agents will continually be encouraged to find new ways of attacking their opponents which will naturally lead to iterative improvement and robustification. In general-sum (especially cooperative) settings, however, self-play will explicitly avoid the weaknesses of other players, as it is harmful to the shared reward, resulting in brittle agents [Carroll et al., 2019]."

"Inspired by its success in zero-sum settings, we leverage a form of adversarial optimization (i.e., we incentivize minimizing other players' rewards) to train agents to find and fix flaws in general-sum settings. However, seeking to minimize others' rewards in cooperative settings, where all agents aim to maximize a shared reward, unsurprisingly leads to self-sabotaging behavior [Cui et al., 2023]. If an agent is solely incentivized to minimize the rewards of another player, the adversary can simply learn to refuse to collaborate with that teammate. Even worse, the adversary has an incentive to act irrationally by actively sabotaging its teammate's (and by extension, its own) reward, preventing meaningful learning."

> _[Section 3.1, Adversarial Optimization Causes Self-Sabotage]_

"We call an optimization objective adversarial when some of the agents are explicitly incentivized to minimize the reward of another agent. For example, the adversarial training (AT) optimization problem [Gleave et al., 2019] is defined for a victim πvictim and an adversary πadversary in a 2-player game. The objective for the adversary is minπadversary Uvictim(πvictim, πadversary) while the objective for the victim is non-adversarial: maxπvictim Uvictim(πvictim, πadversary). In zero-sum settings, AT has been used to train the adversary to find adversarial examples that expose robustness flaws in the victim's policy and have the victim learn to fix them."

### Cited references (resolved from the paper's bibliography)
- **[Samuel, 1959]** A. L. Samuel. *Some studies in machine learning using the game of checkers.* IBM Journal of Research and Development, 1959.
- **[Silver et al., 2016]** Silver, Huang, Maddison, Guez, Sifre, et al. *Mastering the game of Go with deep neural networks and tree search.* Nature 2016.
- **[Carroll et al., 2019]** Carroll, Shah, Ho, Griffiths, Seshia, Abbeel, Dragan. *On the utility of learning about humans for human-AI coordination.* NeurIPS 2019.
- **[Cui et al., 2023]** Cui, Lupu, Sokota, Hu, Wu, Foerster. *Adversarial diversity in Hanabi.* ICLR 2023.
- **[Sarkar et al., 2024]** Sarkar, Shih, Sadigh. *Diverse conventions for human-AI collaboration.* NeurIPS 2024 (Advances in Neural Information Processing Systems 36).
- **[Gleave et al., 2019]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv 2019.
- **[Foerster et al., 2017]** Foerster, Chen, Al-Shedivat, Whiteson, Abbeel, Mordatch. *Learning with opponent-learning awareness.* arXiv 2017.
- **[Ruhdorfer et al., 2025]** Ruhdorfer, Bortoletto, Oei, Penzkofer, Bulling. *Unsupervised partner design enables robust ad-hoc teamwork.* arXiv 2025.
- **[Wang et al., 2025]** Wang, Rahman, Cui, Sung, Stone. *ROTATE: Regret-driven open-ended training for ad hoc teamwork.* arXiv 2025.
- **[Chaudhary et al., 2025]** Chaudhary, Liang, Chen, Du, Jaques. *Improving human-AI coordination through adversarial training and generative models.* arXiv 2025.
- **[Hu et al., 2020]** Hu, Lerer, Peysakhovich, Foerster. *"Other-play" for zero-shot coordination.* ICML 2020.
- **[Treutlein et al., 2021]** Treutlein, Dennis, Oesterheld, Foerster. *A new formalism, method and open issues for zero-shot coordination.* ICML 2021.
- **[Muglich et al., 2022]** Muglich, Schroeder de Witt, van der Pol, Whiteson, Foerster. *Equivariant networks for zero-shot coordination.* NeurIPS 2022.
- **[Vinyals et al., 2019]** Vinyals, Babuschkin, Czarnecki, Mathieu, Dudzik, et al. *Grandmaster level in StarCraft II using multi-agent reinforcement learning.* Nature 2019.
- **[Rahman et al., 2022]** Rahman, Fosong, Carlucho, Albrecht. *Generating teammates for training robust ad hoc teamwork agents via best-response diversity.* arXiv 2022.
- **[FAIR]** Meta Fundamental AI Research Diplomacy Team (FAIR), Bakhtin, Brown, Dinan, Farina, et al. *Human-level play in the game of Diplomacy by combining language models with strategic reasoning.* Science 2022.
- **[Liang et al., 2024]** Liang, Chen, Gupta, Du, Jaques. *Learning to cooperate with humans using generative agents.* arXiv 2024.
- **[Kim et al., 2021]** Kim, Liu, Riemer, Sun, Abdulhai, Habibi, Lopez-Cot, Tesauro, How. *A policy gradient algorithm for learning to learn in multiagent reinforcement learning.* ICML 2021.
- **[Letcher et al., 2018]** Letcher, Foerster, Balduzzi, Rocktäschel, Whiteson. *Stable opponent shaping in differentiable games.* arXiv 2018.
- **[Lu et al., 2022]** Lu, Willi, Schroeder de Witt, Foerster. *Model-free opponent shaping.* ICML 2022.
- **[Khan et al., 2023]** Khan, Willi, Kwan, Tacchetti, Lu, Grefenstette, Rocktäschel, Foerster. *Scaling opponent shaping to high dimensional games.* arXiv 2023.
