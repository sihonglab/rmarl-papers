# 55. Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula

## Metadata
- **Title**: Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula
- **Authors**: Brennen A. Hill
- **Affiliation**: Department of Computer Science, University of Wisconsin-Madison
- **Venue**: NeurIPS 2025 Workshop: Scaling Environments for Agents (SEA)
- **Link/arXiv**: arXiv:2509.03771v3 [cs.LG], 4 Nov 2025

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial environment generation / automatic curriculum; robustness to an adaptive, self-scaling adversary that procedurally generates challenges to exploit the learning team's current weaknesses (open-ended generalization / robustness via co-evolution).
- **Method paradigm**: Adversarial co-evolution / self-play, curriculum learning (learned adversarial procedural content generation), competitive multi-agent game (nearly zero-sum POMG), CTDE with PPO/MAPPO.
- **Keywords**: adversarial curriculum, co-evolution, procedural content generation, multi-agent reinforcement learning, self-play, PPO, robustness

## TL;DR
The paper frames environment generation as an adversarial game in which a generative Attacker procedurally creates increasingly difficult enemy-unit configurations against a cooperative team of Defenders, producing a self-scaling, open-ended curriculum from which complex strategies (flanking, shielding, focus-fire, spreading) emerge automatically and drive the agents toward greater robustness.

## Problem & Motivation
Scaling the complexity, diversity, and interactivity of training environments is a crucial bottleneck for developing general-purpose, robust agents. Hand-crafted environments are finite, contain implicit designer biases, and let agents overfit to fixed scenarios, while manual design of richer environments is intractable in human effort and limited by imagination. Prior procedural content generation (PCGML/PCGRL) either imitates existing data or optimizes a static hand-crafted reward, and prior adversarial PCG focused on a single solver agent solving static puzzles. The paper aims to generate a boundless, adaptive curriculum by reframing environment design as a two-player adversarial game whose challenge difficulty is derived dynamically from a learning team's performance.

## Robustness Setting
- **Threat model / uncertainty set**: The "perturbation" is an actively hostile, learned Attacker that procedurally generates sequences of hostile units (worlds/challenges) over a combinatorially large parameter space (lane, health, damage, speed, range, regeneration, leech, physical/magic defense, penetration, type) to defeat the Defenders. Unit-generation cost is a superlinear, multiplicative function of parameters, forcing the Attacker toward challenges at the frontier of the Defenders' current capability (too-easy yields no reward; truly impossible is prohibitively expensive). The Attacker functions as an automated red-teaming agent finding edge cases and blind spots in the Defenders' policy.
- **Setting**: Mixed-motive — the Defender team (N = 4) is fully cooperative; the Defender-vs-Attacker relationship is fully competitive, forming a nearly zero-sum game (R_A ≈ −Σ R_Dj). Formalized as a Partially Observable Markov Game (POMG); CTDE with shared Defender policy and decentralized execution; online RL via PPO. Defenders have partial observability (do not see the Attacker's energy/policy); the Attacker observes the full state.

## Method
- Formalizes the system as a two-team, nearly zero-sum, partially observable Markov game (POMG) ⟨I, S, {Ai}, T, R, {Ωi}, O⟩ on a discrete 2D grid (10 lanes × 30 tiles); Team D = 4 cooperative Defenders constrained to the first four rows, Team A = 1 generative Attacker at the far end. Defenders win by surviving; the Attacker wins if a unit reaches the baseline or any Defender's health reaches zero.
- The Attacker's action is to generate a unit with a parameter vector θ (13-dimensional multi-branched output with independent softmax heads) or do nothing; generated units follow hard-coded forward-moving behavior so challenge complexity arises from the Attacker's generative choices, not unit AI. The energy cost of a unit is superlinear/multiplicative in θ, enforcing quantity-vs-quality trade-offs.
- Defenders are heterogeneous: each of the four agents holds a unique role (Mage, Healer, Tank, Sharpshooter) with distinct stats and a role-specific special ability (200 energy), choosing from a discrete action space (move, shoot, heal, special, do nothing) with energy costs.
- Reward structure is nearly symmetric/zero-sum: Defenders get −1.0 for losing, +0.001 per tick survived, +0.05 per kill; the Attacker gets +1.0 for winning, −0.001 per tick, −0.03 for failed spawns. Both teams trained simultaneously with PPO (on-policy actor-critic); the four Defenders share a policy to encourage cooperation; policies updated concurrently. MLP with two 128-unit hidden layers, ReLU; implemented in Unity ML-Agents.
- The adversarial dynamic acts as a co-evolutionary arms race: as Defenders improve, the Attacker is incentivized to generate harder challenges, transforming the environment generator into a learned, adaptive loss function that searches the vast world space for maximally informative configurations.

## Theoretical Contributions
None / mostly empirical. The contribution is a system architecture and empirical demonstration; no convergence, equilibrium-existence, or certified-robustness results are proven (the paper notes the system navigates continuous cycles of strategies/counter-strategies rather than reaching a stable Nash equilibrium).

## Experiments
- **Environment/Benchmark**: Custom 2D grid "tower-defense-like" game (10 lanes × 30 tiles) implemented in the Unity engine with the ML-Agents Toolkit; 4 heterogeneous cooperative Defenders vs. 1 generative Attacker. 100 training runs of 500 episodes each on a consumer-grade laptop (Intel Core i5-1035G7 CPU).
- **Baselines**: A random baseline where both sides select actions uniformly at random; plus two ablation conditions — Trained Defender vs. Random Attacker, and Trained Attacker vs. Random Defender — to isolate the effect of co-evolution.
- **Evaluation metrics**: Average episode length (Defender survival time in ticks/steps); frequency of four signature emergent strategies (Cooperative Spreading, Cooperative Focusing, Flanking, Tandem) measured as average uses per episode and usage rate (%), averaged across 100 independent runs.

## Key Results
- Trained agents survived over four times longer than the random baseline (avg. episode length 83 steps vs. 19), demonstrating substantially improved survival.
- The trained Attacker used Tandem in 98.2% and Flanking in 94.0% of episodes; the Defender team used Cooperative Spreading in 92.6% and Cooperative Focusing in 81.4% of episodes, versus below ~11% for the random baseline — indicating deliberate, recognizable multi-agent tactics rather than chance.
- Ablations show co-evolution is the primary driver: a Defender trained against a random Attacker survived longer (216 steps) but rarely used cooperative strategies (Spreading 13.2%, Focusing 9.30%) and barely improved over baseline; an Attacker trained against random Defenders saw episode length collapse to 14 steps with Flanking/Tandem at only 13.7%/21.2%, failing to develop strategic depth.
- The Defender survival curve is non-monotonic with oscillations characteristic of a co-evolutionary arms race (Red Queen dynamic): dips correspond to the Attacker discovering a new effective strategy, after which the Defenders adapt and survival climbs again.

## Limitations & Future Work
- Training was limited to 500 episodes on consumer hardware; longer training would likely reveal more sophisticated, multi-layered strategies.
- Quantitative results are largely qualitative/emergent-behavior based; a deeper analysis of the learned policies (e.g., via explainable AI) is warranted.
- Future work: integrate LLMs as the generative Attacker (formulating high-level strategic goals) and/or for Defender high-level planning and explicit communication; scale the generator (modify environment topology, place obstacles, design new unit types) and richer compositional tool-use; explore population-based training with multiple co-evolving species of Attackers and Defender teams.

## Relevance to Survey
This paper sits on the "adversarial / open-ended environment generation" line of robust MARL, where robustness and generalization are pursued not by an explicit worst-case uncertainty set but by an adaptive learned adversary that continually red-teams the cooperative team. It connects adversarial self-play, automatic curriculum learning, and procedural content generation to the goal of training robust cooperative MARL agents, and explicitly positions PPO/MAPPO as the cooperative learner. It complements the model-uncertainty and minimax adversarial-training lines (e.g., robust MARL with a nature player) by treating the environment generator itself as the adaptive adversary, and it ties to communication/coordination robustness through emergent implicitly-coordinated Defender tactics.

## Related Work (verbatim excerpts from the paper)

> _[Section 2.1, Related Work — Multi-Agent Reinforcement Learning (MARL)]_

"MARL extends reinforcement learning to scenarios with multiple interacting agents. A central challenge in MARL is non-stationarity: from any single agent's perspective, the environment is constantly changing as other agents adapt their policies [Bușoniu et al., 2008]. This makes learning unstable. Our system embraces this non-stationarity, leveraging it as the primary driver of learning for both the Attacker and the Defenders.

MARL problems can be categorized as cooperative, competitive, or mixed-motive [Zhang et al., 2019]. Our work features a mixed structure: the Defender team is fully cooperative, while the relationship between the Defender team and the Attacker is fully competitive, forming a game that is close to zero-sum. The formal framework for such interactions is the Partially Observable Markov Game (POMG), where agents must make decisions based on incomplete information about the true game state [Hansen et al., 2004, Liu et al., 2022]. In our setup, the Defenders have only partial observability of the Attacker's internal state, not seeing the Attacker's energy reserves and policy.

A dominant paradigm in modern MARL is Centralized Training with Decentralized Execution (CTDE) [de Witt et al., 2020]. In CTDE, agents use global information (e.g., a shared value function) during training to stabilize learning but act based only on their local observations during execution. Proximal Policy Optimization (PPO) [Schulman et al., 2017] has proven surprisingly effective in cooperative MARL settings when adapted to this paradigm (e.g., MAPPO), challenging the notion that on-policy methods are too sample-inefficient [Yu et al., 2022]. This body of work provides strong justification for our choice of PPO as the learning algorithm for the cooperative Defender team and the competitive Attacker."

> _[Section 2.2, Related Work — Procedural Content Generation (PCG)]_

"Procedural Content Generation refers to the algorithmic creation of game content. Traditional PCG methods are often constructive or search-based. A more recent paradigm is PCG via Machine Learning (PCGML), where models are trained on existing content to generate new, similar content [Summerville et al., 2018]. For example, models can learn to blend existing levels to create novel combinations [Guzdial and Riedl, 2016]. However, PCGML is fundamentally imitative and its creative potential is bounded by its training data.

To overcome this limitation, PCG via Reinforcement Learning (PCGRL) was introduced, framing content generation as an RL problem where an agent learns to iteratively modify a level to maximize a reward function based on desired properties like playability [Khalifa et al., 2020]. This approach is inventive rather than imitative, as it can discover novel content through exploration. Our work builds directly upon this idea, but instead of using a static, hand-crafted reward function, the reward signal for our generative Attacker is derived dynamically from the performance of another learning agent (the Defender team)."

> _[Section 2.3, Related Work — Adversarial Learning and Automatic Curricula]_

"The core mechanism of our system is the adversarial dynamic between the generator and the solvers. This concept has deep roots in machine learning, most notably in Generative Adversarial Networks (GANs). In the context of RL, adversarial self-play has been shown to be a powerful engine for generating complexity and achieving superhuman performance without human data, as exemplified by AlphaGo and AlphaZero [Silver et al., 2016, 2017]. Similarly, competitive multi-agent environments have been shown to produce a natural curriculum, leading to the emergence of complex skills and strategies as agents continually adapt to one another [Bansal et al., 2018, Tampuu et al., 2017, Narvekar et al., 2020].

The explicit use of an adversary for PCG was explored by Volz et al. [Volz et al., 2021] and Gisslén et al. [Gisslén et al., 2021], who proposed a Generator-Solver framework where the generator is rewarded for creating challenging but solvable levels for a single solver agent. Our work extends this adversarial PCG paradigm in several critical dimensions. We transition from a single-solver setting to a multi-agent cooperative team, elevating the task from solving static puzzles to developing dynamic, coordinated strategies against a learning adversary. Second, our generator operates at a more fundamental level with fine-grained control over the challenge. We shift the focus from generating solvable static environments to orchestrating a dynamic, self-scaling curriculum.

This process of co-evolution, where agents and their environments develop in tandem, has been identified as a powerful method for open-ended learning. The POET algorithm, for instance, co-evolves a population of environments and agent policies, leading to the continual generation of novel and complex challenges [Wang et al., 2019]. Other work has explored co-evolving an agent's morphology alongside its environment [Ao et al., 2023]. Our system can be seen as a specific instantiation of this broader principle, using a competitive game to drive the co-evolution of environmental challenges (from the Attacker) and solving policies (from the Defenders). This dynamic automatically generates goals of appropriate difficulty, a key principle in automatic curriculum generation [Florensa et al., 2018]. Finally, our use of PPO is further supported by its extensibility for training policies robust to adversarial perturbations [Wu et al., 2021, Zhang et al., 2020]."

### Cited references (resolved from the paper's bibliography)
- **[Ao et al., 2023]** Ao, He, Zhou, Liu, Sun. *Curriculum reinforcement learning via morphology-environment co-evolution.* arXiv preprint arXiv:2309.12529, 2023.
- **[Bansal et al., 2018]** Bansal, Pachocki, Sidor, Sutskever, Mordatch. *Emergent complexity via multi-agent competition.* ICLR 2018.
- **[Bușoniu et al., 2008]** Bușoniu, Babuška, De Schutter. *A comprehensive survey of multi-agent reinforcement learning.* IEEE Transactions on Systems, Man, and Cybernetics, Part C, 38(2):156–172, 2008.
- **[de Witt et al., 2020]** Schroeder de Witt, Gupta, Makoviichuk, Makar, Farquhar, Torr, Sun, Whiteson. *Is independent learning all you need in the StarCraft multi-agent challenge?* Deep RL Workshop, NeurIPS 2020.
- **[Florensa et al., 2018]** Florensa, Held, Geng, Abbeel. *Automatic goal generation for reinforcement learning agents.* ICML 2018.
- **[Gisslén et al., 2021]** Gisslén, Eakins, Gordillo, Bergdahl, Tollmar. *Adversarial reinforcement learning for procedural content generation.* IEEE Conference on Games (CoG) 2021.
- **[Guzdial and Riedl, 2016]** Guzdial, Riedl. *Learning to blend computer game levels.* Foundations of Digital Games (FDG) 2016.
- **[Hansen et al., 2004]** Hansen, Bernstein, Zilberstein. *Dynamic programming for partially observable stochastic games.* 19th National Conference on Artificial Intelligence (AAAI) 2004.
- **[Khalifa et al., 2020]** Khalifa, Earle, Bȧk, Togelius. *PCGRL: Procedural content generation via reinforcement learning.* AAAI Conference on AI and Interactive Digital Entertainment (AIIDE), vol. 16, 2020.
- **[Liu et al., 2022]** Liu, Szepesvári, Jin. *Sample-efficient reinforcement learning of partially observable Markov games.* NeurIPS 2022.
- **[Narvekar et al., 2020]** Narvekar, Sinapov, Leonetti, Stone. *Curriculum learning for reinforcement learning agents.* Autonomous Agents and Multi-Agent Systems, 34(2):32, 2020.
- **[Schulman et al., 2017]** Schulman, Wolski, Dhariwal, Radford, Klimov. *Proximal policy optimization algorithms.* arXiv preprint arXiv:1707.06347, 2017.
- **[Silver et al., 2016]** Silver, Huang, Maddison, Guez, Sifre, van den Driessche, et al. *Mastering the game of Go with deep neural networks and tree search.* Nature, 529(7587):484–489, 2016.
- **[Silver et al., 2017]** Silver, Schrittwieser, Simonyan, Antonoglou, Huang, Guez, et al. *Mastering the game of Go without human knowledge.* Nature, 550(7676):354–359, 2017.
- **[Summerville et al., 2018]** Summerville, Snodgrass, Guzdial, Holmgård, Hoover, Isaksen, Nealen, Togelius. *Procedural content generation via machine learning (PCGML).* IEEE Transactions on Games, 10(3):257–270, 2018.
- **[Tampuu et al., 2017]** Tampuu, Matiisen, Kodelja, Kuzovkin, Korjus, Aru, Aru, Vicente. *Multiagent cooperation and competition with deep reinforcement learning.* PLoS ONE, 12(4):e0172395, 2017.
- **[Volz et al., 2021]** Volz, Schrum, Liu, Lucas, Smith, Risi. *Evolving Mario levels in the latent space of a deep convolutional generative adversarial network.* IEEE Congress on Evolutionary Computation (CEC) 2021.
- **[Wang et al., 2019]** Wang, Lehman, Clune, Stanley. *Paired Open-Ended Trailblazer (POET): Endlessly generating increasingly complex and diverse learning environments and their solvers.* arXiv preprint arXiv:1901.01753, 2019.
- **[Wu et al., 2021]** Wu, Guo, Wei, Xing. *Adversarial policy training against deep reinforcement learning.* 30th USENIX Security Symposium (USENIX Security 21), 2021.
- **[Yu et al., 2022]** Yu, Velu, Vinitsky, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative, multi-agent games.* NeurIPS 2022.
- **[Zhang et al., 2019]** Zhang, Yang, Başar. *Multi-agent reinforcement learning: A selective overview of theories and algorithms.* arXiv preprint arXiv:1911.10635, 2019.
- **[Zhang et al., 2020]** Zhang, Chen, Xiao, Li, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
