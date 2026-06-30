# 100. SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning

## Metadata
- **Title**: SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning
- **Authors**: Benjamin Ellis, Jonathan Cook, Skander Moalla, Mikayel Samvelyan, Mingfei Sun, Anuj Mahajan, Jakob N. Foerster, Shimon Whiteson
- **Affiliation**: University of Oxford; University College London; Meta AI; University of Manchester; EPFL
- **Venue**: NeurIPS 2023 (Track on Datasets and Benchmarks)
- **Link/arXiv**: Code at https://github.com/oxwhirl/smacv2

## Taxonomy
- **Robustness / perturbation type targeted**: Generalisation to unseen scenarios / stochasticity (procedurally generated team compositions and start positions); meaningful partial observability (stochastic enemy-observation masking in the EPO challenge). No adversarial/attack threat model in the classic robust-MARL sense.
- **Method paradigm**: Benchmark design / procedural content generation (PCG); analysis of open-loop vs closed-loop policies; Q-value inferrability regression analysis; not a robust-training algorithm.
- **Keywords**: Cooperative MARL, CTDE, SMAC benchmark, procedural content generation, partial observability (Dec-POMDP), generalisation

## TL;DR
The paper shows that the widely used SMAC benchmark lacks the stochasticity and meaningful partial observability needed to require closed-loop policies (an open-loop, timestep-only policy reaches non-trivial win rates), and introduces SMACv2 — using procedural generation of team compositions and start positions plus the Extended Partial Observability (EPO) challenge — to force agents to generalise and condition on their observations.

## Problem & Motivation
SMAC has become the most popular testbed for cooperative MARL under the CTDE paradigm, but after years of improvement algorithms now achieve near-perfect win rates on most scenarios, causing ceiling effects. The authors present a more fundamental problem: SMAC's fixed starting positions and unit types let agents memorise fixed action sequences, and its large fields-of-view make most relevant observations common across agents, so it is not stochastic enough to require closed-loop (observation-conditioned) policies and provides little meaningful partial observability. Because meaningful partial observability is essential to the difficulty (and NEXP-completeness) of Dec-POMDPs and to true decentralisation, and because generalising to new settings at test time is crucial for real-world MARL, a new benchmark is needed.

## Robustness Setting
- **Threat model / uncertainty set**: No adversary. "Uncertainty" arises from procedural randomisation: per-episode random team compositions (unit types drawn with fixed probabilities), random start positions (reflect and surround flavours), and true SC2 sight/attack ranges. In the EPO challenge, enemy observations are stochastically masked per agent with a tunable success probability p (recommended p = 0), and the available-actions mask is removed, requiring agents to infer or implicitly communicate enemy information.
- **Setting**: cooperative; centralised training with decentralised execution (CTDE); online; Dec-POMDP formulation.

## Method
- Diagnoses SMAC's deficiency by training open-loop policies (conditioned only on agent ID and timestep) vs closed-loop policies (full observation history) using MAPPO and QMIX; open-loop policies still succeed on many scenarios, revealing insufficient stochasticity.
- A second diagnostic masks ("zeros out") observation/state features and regresses to a trained QMIX joint Q-function; even masking everything yields low RMSE (≈5–15% of mean Q), showing observation features barely inform the Q-value.
- Proposes SMACv2: procedural content generation (PCG) of team compositions (3 unit types per race with fixed spawn probabilities, special units at 10%), random start positions (reflect / surround), and use of true unit sight/attack ranges (with a minimum attack range of 2 for melee units).
- Introduces the Extended Partial Observability (EPO) challenge: only the first ally to spot an enemy is guaranteed to see it; other allies get a binary draw (probability p) deciding whether they can ever observe that enemy; the available-actions mask is removed; uses a 6-vs-5 setting to widen the gap between p = 1 and p = 0.

## Theoretical Contributions
None / mostly empirical. The paper invokes existing theory (open-loop optimality under deterministic dynamics; NEXP-completeness of Dec-POMDPs) as motivation but contributes a benchmark and empirical analysis rather than new theorems.

## Experiments
- **Environment/Benchmark**: SMAC (14 micromanagement scenarios) for the diagnostic analysis; SMACv2 (Protoss / Terran / Zerg, with 5v5, 10v10, 20v20 symmetric and 10v11, 20v23 asymmetric scenarios) and the EPO challenge (6v5 per race) for the new evaluations.
- **Baselines**: QMIX, MAPPO, IPPO, QPLEX, and an open-loop policy based on MAPPO.
- **Evaluation metrics**: Mean test win rate (over 3 seeds, 10M training steps); Q-value regression RMSE under different feature masks (and RMSE as a proportion of mean Q-value, ϵrmse/Q̄, and the everything-minus-nothing gap).

## Key Results
- On SMAC, open-loop policies perform well on a wide range of scenarios; only four maps (3s5z_vs_3s6z, corridor, 6h_vs_8z, 5m_vs_6m) cannot be learned at all open-loop, evidencing a lack of stochasticity.
- Q-value regression with the everything mask reaches only ≈15% of mean Q at peak and 5–10% for most of the episode (below 0.12 for all scenarios except 5m_vs_6m), close to the nothing baseline — confirming limited stochasticity/meaningful partial observability in SMAC.
- On SMACv2, the open-loop policy cannot learn any map, while QMIX/MAPPO/IPPO/QPLEX struggle (low win rates on asymmetric, especially 20_vs_23, scenarios; Zerg hardest); the everything-minus-nothing Q gap is higher for every SMACv2 map than any SMAC map (e.g., 0.12 for 5_gen_protoss vs 0.07 for 5m_vs_6m), showing SMACv2 is significantly more stochastic.
- In EPO, p = 0 attains only modest performance while p = 1 nearly solves several tasks, leaving a large gap for methods using implicit communication; ablations show random start positions and unit-type diversity contribute most to difficulty, with the true-range change contributing little.

## Limitations & Future Work
- SMACv2 is confined to StarCraft II, which cannot represent the dynamics of all multi-agent tasks; the authors recommend evaluating on multiple benchmarks.
- Only one side can be controlled by RL agents; controlling both armies (e.g., via self-play across two clients) is left as future work.
- Future inference capabilities could be improved via better sequence models (e.g., specialised transformers, upside-down RL); expanding such work to more diverse scenarios is an open avenue.

## Relevance to Survey
SMACv2 is not a robust-MARL method but a benchmark that operationalises two robustness-adjacent challenges for cooperative MARL: (i) generalisation to procedurally varied, previously unseen scenarios (stochasticity) and (ii) meaningful partial observability requiring implicit communication. It connects to the "generalisation / environment stochasticity" and "partial-observability robustness" themes and provides an evaluation substrate against which robustness/generalisation claims of CTDE algorithms (QMIX, MAPPO, IPPO, QPLEX) can be stress-tested, exposing the brittleness of memorised, open-loop behaviour.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work]_

"The MARL community has made signiﬁcant use of games for benchmarking cooperative MARL algorithms. The Hanabi Learning Environment [2] tasks agents with learning to cooperate in the card-game Hanabi. Here, each agent observes the cards of its teammates but not its own, which must be implicitly communicated via gameplay. Hanabi is partially observable and stochastic, but only features teams of 2 to 5 players, which is fewer than all but the smallest SMACv2 scenarios. Kurach et al. [20] propose Google Football as a complex and stochastic benchmark, and also have a multi-agent setting. However, it assumes fully observable states, which simpliﬁes coordination. Peng et al. [31] propose a multi-agent adaptation of the MuJoCo environment featuring a complex continuous action space. Multi-Particle Environments (MPE) [25] feature simple communication-oriented challenges where particle agents can move and interact with each other using continuous actions. In contrast to both multi-agent MuJoCo and MPE, SMACv2 has a discrete action space, but challenges agents to handle a wide range of scenarios using procedural content generation. A plethora of work in MARL uses grid-worlds [25, 23, 54, 4, 48, 35, 24] where agents move and perform a small number of discrete actions on a 2D grid, but these tasks have much lower dimensional observations than SMACv2. OpenSpiel [22] and PettingZoo [46] provide collections of cooperative, competitive, and mixed sum games, such as grid-worlds and board games. However, the cooperative testbeds in either of these suites feature only simple environments with deterministic dynamics or a small number of agents. Neural MMO [41] provides a massively multi-agent game environment with open-ended tasks. However, it focuses on emergent behaviour within a large population of agents, rather than the ﬁne-grained coordination of fully cooperative agents. Furthermore, none of these environments combines meaningful partial observability, complex dynamics, and high-dimensional observation spaces, whilst also featuring more than a few agents that need to coordinate to solve a common goal."

"StarCraft has been frequently used as a testbed for RL algorithms. Most work focuses on the full game whereby a centralised controller serves as a puppeteer issuing commands for the two elements of the game: macromanagement, i.e., the high-level strategies for resource management and economy, and micromanagement, i.e., the ﬁne-grained control of army units. TorchCraft [45] and TorchCraftAI [1] provide interfaces for training agents on StarCraft: BroodWar. The StarCraft II Learning Environment (SC2LE) [49] provides a Python interface for communicating with the game of StarCraft II and has been used to train AlphaStar [50], a grandmaster-level but fully centralised agent that is able to beat professional human players. SMAC and SMACv2 are built on top of SC2LE and concentrate only on decentralised unit micromanagement for the CTDE setting."

"One limitation of SMAC is the constant starting positions and types of units, allowing methods to memorise action sequences for solving individual scenarios (as we show in Section 5.1), while also lacking the ability to generalise to new settings at test time, which is crucial for real-world applications of MARL [28]. To address these issues, SMACv2 relies on procedural content generation [PCG; 36, 18] whereby inﬁnite game levels are generated algorithmically and differ across episodes. PCG environments have recently gained popularity in single-agent domains [7, 6, 17, 21, 38] for improving generalisation in RL [19] and we believe the next generation of MARL benchmarks should follow suit. Iqbal et al. [15] and Mahajan et al. [28] consider updated versions of SMAC by randomising the number and types of the units, respectively, to assess the generalisation in MARL. However, these works do not include the random start positions explored in SMACv2, analyse the properties of SMAC to motivate these changes, or address SMAC's lack of meaningful partial observability. They also do not change the agents' ﬁeld-of-view and attack ranges or provide a convenient interface to generate new distributions over these features."

> _[Introduction]_

"Together these results suggest that SMAC is not stochastic enough to necessitate complex closed-loop (i.e. conditioned on the observation) control policies on many scenarios. Therefore, although SMAC scenarios may require difﬁcult to discover action sequences such as focus ﬁre, agents do not need to adapt to a diverse range of situations, but can largely repeat a ﬁxed action sequence with little deviation. Additionally, meaningful partial observability (see Section 4) is minimal in SMAC due to large ﬁelds-of-view. For partial observability to be meaningful, one agent must observe information that is relevant to the current or future action selection of another agent, unknown to that other agent, and uninferrable from the other agent's observation. Meaningful partial observability is crucial to decentralisation and the NEXP-completeness of Dec-POMDPs [3]."

### Cited references (resolved from the paper's bibliography)
- **[1]** TorchCraftAI. *TorchCraftAI: A bot platform for machine learning research on StarCraft: Brood War.* GitHub repository, 2018.
- **[2]** Bard, Foerster, Chandar, Burch, Lanctot, Song, et al. *The Hanabi challenge: A new frontier for AI research.* Artificial Intelligence, 2020.
- **[3]** Bernstein, Givan, Immerman, Zilberstein. *The complexity of decentralized control of Markov decision processes.* Mathematics of Operations Research, 2002.
- **[4]** Carroll, Shah, Ho, Griffiths, Seshia, Abbeel, Dragan. *On the utility of learning about humans for human-AI coordination.* NeurIPS 2019.
- **[6]** Chevalier-Boisvert, Willems, Pal. *Minimalistic gridworld environment for OpenAI Gym (gym-minigrid).* GitHub repository, 2018.
- **[7]** Cobbe, Hesse, Hilton, Schulman. *Leveraging procedural generation to benchmark reinforcement learning.* ICML 2020.
- **[15]** Iqbal, Schroeder De Witt, Peng, Boehmer, Whiteson, Sha. *Randomized entity-wise factorization for multi-agent reinforcement learning.* ICML 2021.
- **[17]** Juliani, Khalifa, Berges, Harper, Teng, Henry, Crespi, Togelius, Lange. *Obstacle Tower: A generalization challenge in vision, control, and planning.* IJCAI 2019.
- **[18]** Justesen, Torrado, Bontrager, Khalifa, Togelius, Risi. *Procedural level generation improves generality of deep reinforcement learning.* CoRR abs/1806.10729, 2018.
- **[19]** Kirk, Zhang, Grefenstette, Rocktäschel. *A survey of generalisation in deep reinforcement learning.* arXiv:2111 (preprint), 2021.
- **[20]** Kurach, Raichuk, Stańczyk, Zając, Bachem, Espeholt, et al. *Google research football: A novel reinforcement learning environment.* AAAI 2020.
- **[21]** Küttler, Nardelli, Miller, Raileanu, Selvatici, Grefenstette, Rocktäschel. *The NetHack Learning Environment.* NeurIPS 2020.
- **[22]** Lanctot, Lockhart, Lespiau, Zambaldi, Upadhyay, Pérolat, et al. *OpenSpiel: A framework for reinforcement learning in games.* CoRR abs/1908.09453, 2019.
- **[23]** Leibo, Zambaldi, Lanctot, Marecki, Graepel. *Multi-agent reinforcement learning in sequential social dilemmas.* arXiv:1702.03037, 2017.
- **[24]** Leibo, Dueñez-Guzmán, Vezhnevets, Agapiou, Sunehag, Koster, et al. *Scalable evaluation of multi-agent reinforcement learning with Melting Pot.* PMLR 2021.
- **[25]** Lowe, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[28]** Mahajan, Samvelyan, Gupta, Ellis, Sun, Rocktäschel, Whiteson. *Generalization in cooperative multi-agent systems.* arXiv:2202.00104, 2022.
- **[31]** Peng, Rashid, Schroeder de Witt, Kamienny, Torr, Boehmer, Whiteson. *FACMAC: Factored multi-agent centralised policy gradients.* NeurIPS 2021.
- **[35]** Resnick, Eldridge, Ha, Britz, Foerster, Togelius, Cho, Bruna. *Pommerman: A multi-agent playground.* arXiv:1809.07124, 2018.
- **[36]** Risi, Togelius. *Increasing generality in machine learning through procedural content generation.* Nature Machine Intelligence, 2020.
- **[38]** Samvelyan, Kirk, Kurin, Parker-Holder, Jiang, Hambro, Petroni, Kuttler, Grefenstette, Rocktäschel. *MiniHack the planet: A sandbox for open-ended reinforcement learning research.* NeurIPS 2021 Datasets and Benchmarks Track.
- **[41]** Suarez, Du, Isola, Mordatch. *Neural MMO: A massively multiagent game environment for training and evaluating intelligent agents.* arXiv:1903.00784, 2019.
- **[45]** Synnaeve, Nardelli, Auvolat, Chintala, Lacroix, Lin, Richoux, Usunier. *TorchCraft: A library for machine learning research on real-time strategy games.* arXiv:1611.00625, 2016.
- **[46]** Terry, Black, Grammel, Jayakumar, Hari, Sullivan, et al. *PettingZoo: Gym for multi-agent reinforcement learning.* NeurIPS 2021.
- **[48]** Vinitsky, Jaques, Leibo, Castenada, Hughes. *An open source implementation of sequential social dilemma games.* GitHub repository, 2019.
- **[49]** Vinyals, Ewalds, Bartunov, Georgiev, Vezhnevets, Yeo, et al. *StarCraft II: A new challenge for reinforcement learning.* arXiv:1708.04782, 2017.
- **[50]** Vinyals, Babuschkin, Czarnecki, Mathieu, Dudzik, Chung, et al. *Grandmaster level in StarCraft II using multi-agent reinforcement learning.* Nature, 575(7782):350–354, 2019.
- **[54]** Yang, Luo, Li, Zhou, Zhang, Wang. *Mean field multi-agent reinforcement learning.* ICML 2018.
