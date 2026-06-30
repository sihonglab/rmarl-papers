# 83. Modeling Trust and Deception in Multi-Agent Reinforcement Learning Using the Werewolf Game

## Metadata
- **Title**: Modeling Trust and Deception in Multi-Agent Reinforcement Learning Using the Werewolf Game
- **Authors**: Pathikkumar D. Patel (advisor: Dr. Manfred Huber)
- **Affiliation**: The University of Texas at Arlington (Computer Science and Engineering)
- **Venue**: M.S. Thesis, The University of Texas at Arlington, May 2025
- **Link/arXiv**: https://mavmatrix.uta.edu/cse_theses/529

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial/deceptive agents and hidden-role partial observability; robustness to environmental shifts (varying population sizes and role distributions); social misinformation / trust manipulation
- **Method paradigm**: Symbolic heuristic + probabilistic trust modeling (Agent vA) vs. modular phase-specific Q-learning (Agent vB); self-play; emergent deception
- **Keywords**: social deduction games, Werewolf, trust modeling, deception, multi-agent reinforcement learning, Q-learning, belief modeling

## TL;DR
The thesis builds a Werewolf social-deduction simulation and compares two agent designs—a symbolic, memory-based trust-modeling agent (vA) and a modular role-conditioned Q-learning agent (vB)—showing that trust and deception emerge as learned behaviors, with the symbolic agent more robust to environmental shifts and the Q-learning agent more scalable and adaptive.

## Problem & Motivation
As autonomous agents increasingly operate under uncertainty, incomplete information, and potentially deceptive collaborators or adversaries, they must reason about the beliefs, intentions, and trustworthiness of others. Social deduction games such as Werewolf are a compelling testbed for emergent trust-building, alliance formation, and strategic misinformation, requiring agents to reason from evolving social dynamics rather than only environmental feedback. The thesis asks whether RL agents can learn to build trust or deceive in a partially observable, role-based environment; what behavioral patterns emerge over repeated play; and whether deception can emerge organically through reinforcement learning alone without being hardcoded.

## Robustness Setting
- **Threat model / uncertainty set**: Hidden roles and asymmetric information—an informed minority (Werewolves) versus an uninformed majority (Villagers, plus Seer and Medic). Agents face deceptive opponents, partial observability, and "environmental shifts" induced by varying population sizes (7–49 agents) and re-randomized role distributions each episode. No formal uncertainty set; robustness is evaluated empirically as performance stability across these shifts.
- **Setting**: Mixed cooperative–competitive (team-based factions); decentralized agents with per-agent memory/Q-tables; online self-play training, persistent across episodes (10,000–150,000+ games).

## Method
- Simulates a simplified Werewolf game (four roles: Werewolf, Seer, Medic, Villager) with alternating night (private special-role actions) and day (symbolic communication + plurality voting) phases; structured messages include accuse, reveal, support, agree.
- **Agent vA (heuristic memory-based)**: a handcrafted, uniformly-initialized probabilistic trust/belief model over each player's role, updated by confidence-weighted heuristics scaled by speaker reputation; a bounded memory window (~5 rounds); votes against the least-trusted alive player with role-specific overrides (e.g., Seer prioritizes known Werewolves); lightweight role-conditioned strategy Q-values updated by Q_new = Q_old + α(R − Q_old).
- **Agent vB (modular Q-learning)**: three independent phase-specific Q-tables (night, day conversation, day vote), each updated by the temporal-difference rule Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') − Q(s,a)] with α=0.1, γ=0.95; symbolic compressed state strings (phase, num alive, role, accused flag, werewolves discovered, max suspicion) mapped to integer IDs; ε-greedy exploration with ε decaying from 1.0 to 0.1 over 50,000 episodes; role-specific reward shaping (e.g., Seer correctly reveals Werewolf +10, Medic protects +5, Werewolf deception believed +1, talk +0.05 / silent −0.05) plus terminal team win/loss reward (+1/−1).
- Trains agents independently via self-play, then runs head-to-head hybrid simulations (21 agents: 7 Werewolves, 3 Seer, 3 Medic, 8 Villagers) to compare paradigms.

## Theoretical Contributions
None / mostly empirical. The work includes a theoretical attrition-based heatmap of the minimum number of rounds required for a Werewolf victory as a function of player count (7–100) and Werewolf ratio, used only as a baseline for comparison; there are no convergence proofs, sample-complexity bounds, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: A custom Python Werewolf social-deduction simulator; populations of 7, 14, 21, 35, and 49 agents (default and most-analyzed = 21); randomized roles per episode; alternating night/day phases with symbolic communication and voting.
- **Baselines**: The two agent architectures are compared against each other (Agent vA vs. Agent vB), with the theoretical attrition heatmap serving as a theoretical baseline; no external/published baselines.
- **Evaluation metrics**: Win rate by role, voting accuracy, deception success, survival duration, trust alignment (belief vs. ground-truth roles), unique-state-space growth, and convergence curves.

## Key Results
- Agent vA was trained over 500,000 episodes with a continually growing symbolic state space; Agent vB converged much earlier (typically within ~100,000 episodes) with a smaller state space; the Werewolf win-rate curve flattened around 0.69, indicating convergence.
- Role-based comparison: Agent vA wins more as Seer (74.2% vs. 62.5%) and Werewolf (66.1% vs. 63.3%); Agent vB wins more as Medic (69.0% vs. 58.7%) and Villager (67.8% vs. 55.4%).
- In hybrid play, Agent vA initially led, but Agent vB adapted and largely closed the gap after ~5,000 episodes; in vA self-play the Werewolf team won 284,109 vs. 215,891 games (56.8% Werewolf win rate), and deceptive behaviors (minimal communication, mirroring, reactive voting) emerged without explicit rules.
- Simulated games take roughly 20–50% more rounds than the theoretical attrition minimum, indicating emergent disruption via Seer reveals, Medic protections, and false voting chains.

## Limitations & Future Work
- Simplified, purely symbolic, turn-based mechanics with no non-verbal cues, emotion, or linguistic ambiguity; future work could add multimodal communication.
- Limited role diversity (four roles); adding Hunter, Witch, Alpha Werewolf, Masons could enable richer strategies.
- Equal agent-skill assumption; curriculum/transfer learning or dynamic role assignment could model asymmetry.
- Rule-bound symbolic communication; could be replaced by natural-language generation or learned grammar.
- Finite sampling of game configurations; meta-RL or curriculum-based scenario generation could improve generalization and reduce overfitting.
- Exploration bias in early agent versions; intrinsic curiosity, entropy regularization, or novelty rewards could help.
- Agent vA's partially hardcoded trust system (manually calibrated decay/suspicion); learned embeddings/attention/neural memory could replace fixed rules.
- Game-specific evaluation metrics; domain-agnostic metrics (KL divergence, trust-distribution entropy) would generalize better.
- No human-in-the-loop evaluation; user studies could assess believability and persuasiveness.
- Manual reward shaping introduces human bias; IRL, preference learning, or RLHF could derive reward signals from data.

## Relevance to Survey
This thesis sits on the "adversarial / deceptive agents" and "social robustness under hidden-role partial observability" lines of robust MARL, contrasting a symbolic trust-modeling paradigm with a learning-based Q-learning paradigm. Its explicit framing of robustness as stability to environmental shifts (population/role distribution changes) and its study of emergent deception connect to the survey's themes of adversarial agents, trust/belief modeling, and robustness to non-stationary social opponents. It is primarily an applied/empirical contribution rather than a theoretical robust-MARL result, useful as an example of trustworthy-AI and social-deception modeling in MARL.

## Related Work (verbatim excerpts from the paper)

> _[Chapter 2, Related Work — 2.1 Multi-Agent Reinforcement Learning in Hidden-Role Games]_

"Social deduction games like Mafia, Werewolf, and The Resistance: Avalon pose a unique multi-agent challenge: players must identify allies vs. adversaries under hidden roles and partial information. Foundational work includes equilibrium analysis in hidden-role games. Carminati et al. (2024) introduced a formal equilibrium model for such games and proved tractable strategies in Avalon [6]. Serrino et al. (2019) developed DeepRole, a deep RL + CFR agent that achieved superhuman performance in Avalon by learning effective strategies through belief modeling and self-play training [7]."

> _[Chapter 2, Related Work — 2.2 Deception and Trust Modeling in MARL]_

"Deception and trust modeling are central to these environments. Aitchison et al. (2021) introduced Rescue The General (RTG), a testbed for deception-focused MARL, and proposed Bayesian Belief Manipulation (BBM) to reward misleading behaviors [8]. Jin et al. (2024) extended this by training agents that strategically choose between truth and lies in One Night Ultimate Werewolf. Their RL-instructed language agents optimized discussion tactics for improved voting outcomes [9]."

> _[Chapter 2, Related Work — 2.3 Strategic Communication and Language-Based Agents]_

"Recent works combine natural language processing and MARL. Xu et al. (2023) used GPT-based LLMs to generate candidate statements in Werewolf, with RL policies selecting the most strategic ones [10]. These agents achieved human-level performance. Sarkar et al. (2025) applied a similar approach in Among Us, with agents learning to speak, listen, and infer impostors through conversation [11]. Auxiliary prediction objectives encouraged belief modeling and deception detection."

> "Other systems explore constrained communication. The AIWolf competition began with limited utterance formats and later expanded to free chat [12]. Tsang et al. (2024) trained agents to reason using only voting behavior, showing implicit communication through vote patterns and confirming that rules like sequential elimination shape emergent strategies [13]."

> _[Chapter 2, Related Work — 2.4 Summary]_

"This body of work shows that MARL agents can learn trust, deception, and communication strategies in hidden-role settings. From symbolic belief modeling to deep RL with natural language, each study advances our understanding of social reasoning in AI. Together, these results inform the design of multi-agent systems that can compete with and outperform humans in socially complex environments."

### Cited references (resolved from the paper's bibliography)
- **[6]** Carminati, Burch, Holte, Bowling. *Hidden role games: Equilibria and algorithms.* arXiv preprint arXiv:2402.10894, 2024.
- **[7]** Serrino, Iyyer, Boyd-Graber. *Finding your allies in multiplayer games: Agent modeling for the game of Avalon.* AAAI 2019.
- **[8]** Aitchison, Benke, Sweetser. *Learning to deceive with attention-based message passing.* AAMAS 2021.
- **[9]** Jin, Wang, Zettlemoyer. *Strategic communication in One Night Ultimate Werewolf using reinforcement learning.* NAACL 2024.
- **[10]** Xu, Liu, Sun. *Language-guided multi-agent reinforcement learning for the Werewolf game.* NeurIPS Workshop on Multi-Agent Learning, 2023.
- **[11]** Sarkar, Bai, Lee, Liu. *Emergent strategic communication for deception detection in Among Us.* AAAI 2025.
- **[12]** *AIWolf Project: Werewolf intelligence agent platform.* https://aiwolf.org, 2023.
- **[13]** Tsang, Singh, Rabinowitz. *Voting as implicit communication in multi-agent deduction games.* ICLR 2024.
