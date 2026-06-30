# 56. A Framework for Scalable Heterogeneous Multi-Agent Adversarial Reinforcement Learning in IsaacLab

## Metadata
- **Title**: A Framework for Scalable Heterogeneous Multi-Agent Adversarial Reinforcement Learning in IsaacLab
- **Authors**: Isaac Peterson, Christopher Allred, Jacob Morrey, Mario Harper
- **Affiliation**: Utah State University; US DEVCOM Army Research Laboratory (Allred)
- **Venue**: Not specified (arXiv preprint, 2025)
- **Link/arXiv**: arXiv:2510.01264v1 [cs.LG]; code at https://directlab.github.io/IsaacLab-HARL/

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents (competitive opponents) in zero-sum multi-agent settings; heterogeneous teaming (different agent counts, morphologies, observations, and actions); training robust policies under adversarial dynamics
- **Method paradigm**: Adversarial / self-play training, competitive HAPPO (Heterogeneous-Agent PPO) with team-specific critics, CTDE, curriculum learning, simulation framework engineering
- **Keywords**: Adversarial MARL, heterogeneous agents, HARL/HAPPO, IsaacLab, curriculum learning, high-fidelity physics simulation

## TL;DR
The paper extends the IsaacLab simulator and the HARL library into HARL-Adversarial (HARL-A), a framework that adds team-specific critics (per HAPPO) to enable scalable, high-fidelity training of heterogeneous, morphologically diverse agents in zero-sum adversarial tasks (Sumo, Soccer, 3D Galaga), and provides these as benchmarks for studying robust adversarial MARL.

## Problem & Motivation
Most MARL work in robotics has focused on cooperative settings, while adversarial interactions (pursuit-evasion, security, competitive manipulation) are equally critical for real-world deployment. A gap remains in heterogeneous adversarial learning within high-fidelity physics simulators: prior work focuses on either cooperation or simplified adversarial tasks without heterogeneous morphologies, or provides isolated implementations rather than extensible frameworks. Heterogeneous adversarial training raises specific difficulties: (i) competitive training is unstable because both agents evolve over time; (ii) heterogeneous teams need team-specific critics under CTDE since standard parameter-sharing is insufficient; and (iii) reward design in physics-based tasks must balance dense shaping with sparse success signals to prevent unintended strategies. A key technical limitation of the prior cooperative HARL-in-IsaacLab integration was a single shared critic, which in zero-sum settings collapses to the average outcome (V(s) ≈ 0), yielding vanishing advantage estimates and degenerate PPO gradients.

## Robustness Setting
- **Threat model / uncertainty set**: Robustness here is robustness to adversarial opponents in zero-sum competitive games (rewards strictly coupled, e.g. r⁽⁰⁾ₜ = −r⁽¹⁾ₜ), where both teams co-evolve via self-play. Agents must "anticipate and counter the strategies of opponents," with additional difficulty from heterogeneous morphologies (legged vs. wheeled platforms). No explicit uncertainty set or formal adversary model is defined.
- **Setting**: Competitive (zero-sum) and mixed multi-team; CTDE (centralized training with decentralized execution) using team-specific critics; online training via alternating ("leapfrog"/freezing one actor) and simultaneous self-play regimes.

## Method
- Extends an existing cooperative HARL-in-IsaacLab integration to adversarial domains by replacing the single shared critic with team-specific critics, consistent with the HAPPO formulation: each team's critic learns a value function V⁽ⁱ⁾(s) aligned with its own reward r⁽ⁱ⁾, so heterogeneous competitive agents receive non-trivial advantage signals. This enables four actor-critic training paradigms, including single-agent and multi-agent adversarial play.
- Builds a suite of adversarial IsaacLab environments with heterogeneous robots (Anymal C quadruped, Leatherback rover), competitive objectives, and curriculum learning; the framework supports arbitrary team sizes and agent counts.
- Uses curriculum learning to decompose hard adversarial tasks into progressively harder stages (e.g., Sumo: Stage 1 Walk-To-Point, Stage 2 Block Pushing, Stage 3 Adversarial Sumo), with dense shaping plus sparse event terms, and a zero-sum elimination reward Ri(St) = τ·(Lj − Li − ϕ)·κ in the final stage.
- Maintains a consistent observation space across curriculum stages via a "zero-buffer" strategy: initial observations are padded with placeholder zeros that are later replaced with meaningful features, enabling seamless policy transfer without retraining from scratch.
- Provides two adversarial training regimes: alternating updates (freeze one team's actor while updating the other, then switch) and simultaneous training of both teams; additional environments (Soccer, 3D Galaga) demonstrate generalization beyond contact-rich pushing.

## Theoretical Contributions
None / mostly empirical (framework and benchmark contribution). The only formal argument is a motivating derivation that a single shared critic in a zero-sum setting collapses to V(s) ≈ ½(r⁽⁰⁾ₜ + r⁽¹⁾ₜ) = 0, causing vanishing advantages and degenerate PPO loss, justifying team-specific critics.

## Experiments
- **Environment/Benchmark**: Custom adversarial IsaacLab environments — Sumo (homogeneous and heterogeneous teams: Anymal C quadruped vs. Leatherback rover), Soccer (1v1 heterogeneous, anymal vs. leatherback), and 3D Galaga (aerial-ground interception: MiniTanks vs. Crazy Fly quadrotor drones). Trained on NVIDIA GeForce RTX 30- and 40-series GPUs.
- **Baselines**: Trained policies compared against their own initialization (untrained agents); simple adversarial baselines (policies deployed without opponent-aware fine-tuning). No external algorithmic baselines reported.
- **Evaluation metrics**: Win rate of the trained policy vs. its initialization (1000 environment instances per episode); convergence/learning curves with vs. without the zero-buffer; qualitative emergent behaviors.

## Key Results
- Across environments, adversarial policies consistently achieved higher win rates over time (and untrained agents' win rates decreased), confirming effective adversarial learning within HARL-A; both alternating and simultaneous training produced meaningful behaviors (with different stability profiles), suggesting robustness to multiple optimization strategies.
- Heterogeneous teams exhibited emergent role specialization without explicit role assignment: Leatherback rovers learned to destabilize Anymal robots by targeting/pulling out their legs (disruptors), while Anymals learned dragging maneuvers to pull rovers out of the arena (grapplers).
- The zero-buffer mechanism initially slowed convergence (padding ~50 unused zero-valued features) but enabled seamless state-space extension in later curriculum stages, accelerating the overall curriculum without retraining from scratch.
- In Soccer, leatherbacks learned effective strategies against initially more dominant Anymal robots; one noted exception in Sumo was trained leatherbacks vs. untrained Anymals.

## Limitations & Future Work
- 3D Galaga demonstrates adversarial interaction, not true adversarial training: policies do not adapt online to an opponent's strategy and should be interpreted as evidence of transfer and emergent competence rather than opponent-conditioned play.
- Experiments in the paper focus on two agents per team (though the framework supports arbitrary counts); no formal/theoretical robustness guarantees.
- Future work: integrate additional MARL algorithms (value-decomposition methods, graph attention networks); algorithmic innovations for adversarial domains including off-policy methods; richer evaluation (exploitability, cross-play, robustness against novel opponents); advanced curriculum strategies (value disagreement, gradual domain adaptation); and extension to new modalities (aerial, aquatic, swarm) and multi-scale interactions, with applications in security, defense, and human-robot interaction.

## Relevance to Survey
This is an applied/systems contribution on the empirical side of robust MARL: it provides a high-fidelity simulation framework and benchmark suite for adversarial, heterogeneous multi-agent competition, explicitly motivated by enabling "the development of more robust algorithms under competitive dynamics." It sits on the "adversarial agents / self-play" method line rather than the theoretical robust-MDP / distributionally-robust line, and connects robust MARL to embodied robotics (morphology asymmetry, contact dynamics). Its related work usefully bridges adversarial self-play (Bansal et al., Gleave et al.), robust adversarial RL (Pinto et al.), adversarial regularization for robust MARL (Bukharin et al.), and high-fidelity physics-based MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Works — intro and sub-groupings A/B/C, and closing gap statement]_

"Research on adversarial reinforcement learning has developed along several trajectories, from early demonstrations of self-play to large-scale competitive frameworks and physics-based multi-agent domains."

"A. Early Adversarial Self-Play
One of the first demonstrations of emergent competition in physics-based environments introduced competitive tasks in MuJoCo [9], [12]. They demonstrated that self-play can naturally induce curricula, with agents developing increasingly complex behaviors. Extension of this work [13] highlighted new aspects of adversarial training that exploited brittle policies, those which appeared robust under standard evaluation, to improve agent performance."

"B. Multi-Agent Extensions
As adversarial learning moved toward multi-agent settings, algorithmic advances became central. New work [19] introduced multi-agent deep deterministic policy gradient (MADDPG), enabling agents to condition on others' policies and improving coordination in both cooperative and competitive tasks. Large-scale competitive systems such as OpenAI Five in Dota 2 [20] and AlphaStar in StarCraft II [21] demonstrated that population-based training and league-style play could produce human-level strategies. Similarly, the MuJoCo hide-and-seek environment [15] showed emergent tool use and strategy that could come from repeated self-play. Another example proposed deep latent competition, where self-play on visual input produced competitive driving policies [16]."

"Subsequent works explored alternative objectives and domains oriented towards targeted environment tuning to guide training towards areas of low learning and performance. Procedural content generation approaches such as PAIRED [22] and adversarial PCG [23] dynamically adjusted task difficulty. Other studies focused on robustness, including adversarial perturbations [24], and adversarial regularization [25]."

"C. Toward High-Fidelity Physics
More recent work has emphasized realism and team play in continuous control environments. One method combined imitation learning, MARL, and population-based training to produce humanoid soccer players with strategies closely resembling those of human athletes [17]. In the robotics domain, [18] applied MARL in IsaacLab for robot soccer, where learned agents outperformed heuristic baselines. These advances illustrate a growing trend toward using high-fidelity simulators to bridge the gap between abstract MARL benchmarks and embodied multi-robot systems."

"Despite these advances, a unified framework for scalable, heterogeneous, adversarial MARL in high-fidelity simulators is still lacking. Many prior works focus on either cooperation or simplified adversarial tasks without heterogeneous morphologies. Others provide isolated implementations rather than extensible frameworks. As summarized in Table I, our work addresses this gap by extending IsaacLab with heterogeneous adversarial environments and providing benchmarks that support future research in robustness, scalability, and emergent multi-agent competition."

> _[Section I, Introduction — adversarial-learning challenges paragraph]_

"Adversarial learning in this setting raises several challenges. First, competitive training can be unstable, as both agents are evolving over time. Second, heterogeneous teams require team-specific critics under centralized training and decentralized execution, as standard parameter-sharing approaches are insufficient. Third, reward design in physics-based tasks must balance dense shaping with sparse success signals to prevent unintended strategies."

### Cited references (resolved from the paper's bibliography)
- **[9]** Todorov, Erez, Tassa. *MuJoCo: A physics engine for model-based control.* IEEE/RSJ IROS 2012.
- **[12]** Bansal, Pachocki, Sidor, Sutskever, Mordatch. *Emergent complexity via multi-agent competition.* ICLR 2018.
- **[13]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* ICLR 2020.
- **[15]** Baker, Kanitscheider, Markov, Wu, Powell, McGrew, Mordatch. *Emergent tool use from multi-agent autocurricula.* 2020.
- **[16]** Schwarting, Seyde, Gilitschenski, Liebenwein, Sander, Karaman, Rus. *Deep latent competition: Learning to race using visual control policies in latent space.* CoRL 2021.
- **[17]** Liu, Lever, Wang, Merel, Eslami, Hennes, Czarnecki, Tassa, et al. *From motor control to team play in simulated humanoid football.* (Preprint).
- **[18]** Li, Bjelonic, Klemm, Hutter. *MARLadona — towards cooperative team play using multi-agent reinforcement learning.* 2025.
- **[19]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[20]** Berner, Brockman, Chan, et al. (OpenAI). *Dota 2 with large scale deep reinforcement learning.* arXiv:1912.06680, 2019.
- **[21]** Vinyals, Babuschkin, Czarnecki, et al. *Grandmaster level in StarCraft II using multi-agent reinforcement learning.* Nature 2019.
- **[22]** Dennis, Jaques, Vinitsky, Bayen, Russell, Critch, Levine. *Emergent complexity and zero-shot transfer via unsupervised environment design (PAIRED).* NeurIPS 2020.
- **[23]** Gisslén, Eakins, Gordillo, Bergdahl, Tollmar. *Adversarial reinforcement learning for procedural content generation.* IEEE CoG 2021.
- **[24]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[25]** Bukharin, Li, Yu, Zhang, Chen, Zuo, Zhang, Zhang, Zhao. *Robust multi-agent reinforcement learning via adversarial regularization: theoretical foundation and stable algorithms.* NeurIPS 2023.
