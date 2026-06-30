# 118. Robust Regional Coordination of Inverter-Based Volt/Var Control via Multi-Agent Deep Reinforcement Learning

## Metadata
- **Title**: Robust Regional Coordination of Inverter-Based Volt/Var Control via Multi-Agent Deep Reinforcement Learning
- **Authors**: Hangyue Liu, Cuo Zhang, Qingmian Chai, Ke Meng, Qinglai Guo, Zhao Yang Dong
- **Affiliation**: School of Electrical Engineering and Telecommunications, University of New South Wales (Sydney, Australia); Department of Electrical Engineering, Tsinghua University (Beijing, China)
- **Venue**: IEEE Transactions on Smart Grid, Vol. 12, No. 6, November 2021
- **Link/arXiv**: https://doi.org/10.1109/TSG.2021.3104139

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/operational uncertainty — spatial and temporal uncertainties of photovoltaic (PV) power generation and loads in active distribution networks (intervals/scenarios around predicted PV output and demand; not adversarial)
- **Method paradigm**: Multi-agent deep deterministic policy gradient (MADDPG) under centralized training / decentralized execution; stochastic programming (Monte Carlo scenario generation) embedded in the reward; behavior cloning + expert target Q estimation + prioritized experience replay
- **Keywords**: Active distribution network, Volt/Var control, regional coordination, MADDPG, operational uncertainty, stochastic programming

## TL;DR
The paper formulates multi-region coordinated inverter-based Volt/Var control (VVC) as a partially observable Markov Game solved by an improved MADDPG algorithm, and embeds stochastic programming (spatial and temporal uncertainty scenarios) into the reward so that the learned regional controllers minimize voltage deviations and network power losses robustly against PV/load uncertainties.

## Problem & Motivation
Conventional inverter-based VVC relies on rule-based, mathematical, or heuristic methods (e.g., QP/SOCP), which become inefficient or infeasible for large-scale systems, suffer heavy computation burdens when uncertainties are considered, and (for centralized schemes) face privacy, complexity, and scalability issues. RL/DRL approaches improve computational efficiency but most prior DRL-based VVC is centralized; existing MADDPG-based decentralized VVC does not fully consider temporal intermittencies and spatial variations of renewable generation/loads, nor exploit historical expert operation data. The paper aims to achieve real-time decision making while robustly regulating voltages and minimizing losses under spatial and temporal uncertainties.

## Robustness Setting
- **Threat model / uncertainty set**: Operational (non-adversarial) uncertainty of PV maximum power point and active/reactive power demand, bounded by predicted intervals at two scales — spatial uncertainty (locational variation, day-ahead/hour-ahead predicted bounds) and temporal uncertainty (real-time variation due to communication and inverter response delays). Uncertainty is handled by stochastic programming: Monte Carlo sampling of U scenarios per decision timestep, with scenario occurrence probabilities ξ_u; the reward averages normalized objectives over scenarios and sums voltage-constraint-violation occurrences across all scenarios. The paper notes distributional ambiguity could alternatively be handled via an ambiguity set.
- **Setting**: Cooperative (each region/sub-network is an agent minimizing voltage deviation + network loss); centralized training with decentralized execution (CTDE); model-free Markov Game; online execution after offline training.

## Method
- Partition an N-bus distribution network into M interconnected sub-networks; model each sub-network's control center as an agent and reformulate the multi-objective regionally coordinated VVC optimization as a partially observable Markov Game (POMG). Observations cover local bus voltage, active/reactive demand, and PV maximum power; actions are continuous inverter reactive-power setpoints; the reward is the negative weighted sum of normalized voltage deviation, normalized network loss, and a voltage-violation penalty.
- Solve the POMG with a modified MADDPG algorithm (centralized critic over all agents' observations and actions, decentralized deterministic policies), so trained controllers act using only local measurements without inter-agent communication at execution.
- Embed stochastic programming for robustness: generate spatial uncertainty scenarios before each operation period and temporal uncertainty scenarios (in time sequence, preserving temporal correlation) within each period; compute rewards as scenario-probability-weighted normalized objectives and sum voltage violations over all scenarios.
- Improve training performance with: (i) behavior cloning to pre-train policy networks from an expert dataset; (ii) expert target Q value estimation to pre-train the Q networks; (iii) proportional prioritized experience replay (with a prioritized "flash" replay buffer to avoid excessive priority recalculation).

## Theoretical Contributions
None / mostly empirical. The paper provides an appendix derivation of the Bellman optimality equation (decomposition from Eq. (17) to Eq. (19)) under a deterministic power-flow transition, but offers no convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: IEEE 123-node feeder system, partitioned into 4 interconnected sub-networks; 100% PV penetration, inverter apparent power oversized to 110% of installed PV capacity. Two operating cases: PV-peak (50% load, 100% PV) and load-peak (100% load, 0% PV). Also tested under three network reconfiguration topologies (Case-NR1/NR2/NR3 via switches SW1/SW2). AC power flow solved with PYPOWER; conventional baseline solved with GUROBI.
- **Baselines**: Conventional scenario-based stochastic optimization (branch-flow SOCP model, "Math"); two conventional MADDPG variants with different initialization — random initialization (Rand. Init.) and self-training initialization (Self. Init.).
- **Evaluation metrics**: Maximum bus voltage deviation (Vmax), mean of absolute bus voltage deviations (Vmean), network power loss (Ploss), weighted sum of normalized objectives, number of constraint-violation scenarios (robustness), training time, and optimization (decision) time.

## Key Results
- The proposed method converges much faster than the Rand. Init. and Self. Init. MADDPG variants; e.g., in the PV-peak case mean absolute voltage deviation and network loss converge to about 0.011 p.u. and 0.005 p.u. (load-peak: about 0.016 p.u. and 0.012 p.u.).
- MADDPG-based methods have an optimization (decision) time of around 0.014 second, far faster than the mathematical stochastic optimization, making them suitable for online use; the proposed method achieves lower network power loss than the mathematical method.
- Robustness check on 5000 additional Monte Carlo uncertainty-realization scenarios: both the proposed method and the mathematical method achieve no operating violations, while the proposed method gives better network-loss reduction and comparable voltage deviations.
- Under network reconfiguration (Case-NR2/NR3) the proposed method remains applicable and outperforms the conventional data-driven baselines on both convergence and optimization performance.

## Limitations & Future Work
- Only continuous Var resources (inverter reactive-power setpoints) are controlled; discrete-variable VVC resources (OLTCs, switching capacitor banks, soft open points) are not yet incorporated — listed as future work.
- Probability distributions of uncertainties are assumed known (uniform used); distributional ambiguity is only mentioned as a possible extension (ambiguity set), not implemented — future work plans to consider distributional ambiguity in the MADDPG algorithm.
- Future work also includes handling multiple conflicting objectives with multi-task machine learning.

## Relevance to Survey
This is an application-oriented robust MARL paper in the power-systems (smart-grid) domain. Its notion of "robustness" is robustness to environment/operational uncertainty (renewable and load uncertainty) achieved by embedding stochastic programming into a cooperative MADDPG (CTDE) pipeline, rather than adversarial or worst-case minimax robustness. It connects the robust-MARL survey to the "model/environment uncertainty" line and to distributionally robust optimization (referenced but not adopted), and serves as an example of scenario-based / stochastic-programming robustness within deep MARL for real-world coordinated control.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction — robust optimization / distributionally robust optimization prior work]_

"In [11], a two-stage dynamic optimal power flow model for multiple microgrids is developed, where a distributionally robust optimization method is applied to address uncertainties with an ambiguity set. Distributionally robust optimization is advanced in dealing with distributional ambiguity and improving out-of-sample performance [12]. Authors in [13] propose a hierarchically-coordinated VVC structure combining centralized control dispatching reactive power setpoints as well as droop functions for PV inverters, and decentralized droop control that responds to local voltage variations during each central dispatch period. Similarly, a dual time-scale coordination of robust reactive power optimization and voltage control method is proposed in [3], working with ULTCs and CBs on a slow timescale, DG units and static Var compensators (SVCs) on a fast timescale. In [4], a three-stage VVC method is proposed with the first stage coordinating OLTC and CBs, the second stage dispatching inverter reactive power setpoints, and the third stage implementing decentralized droop control. In most of the above literature, VVC optimization problems are formulated as mathematical problems such as quadratic programming (QP) or second-order cone programming (SOCP) problems, then solved mathematically. It is worth noting that although some mathematic hybrid control methods have been proposed, these methods suffer from heavy computation burdens when systems become large and complex, or when uncertainties are considered [14]."

> _[Section I, Introduction — RL / DRL / multi-agent RL prior work]_

"There have been many attempts to improve the computational efficiency, including applications of reinforcement learning (RL) algorithms in solving power system operation optimization problems, e.g., [16], [17]. However, the conventional RL algorithms suffer from scalability issues and the 'curse of dimensionality' for both state and action spaces [18]. Consequently, system model accuracy is often sacrificed, or system state and action spaces are usually simplified and discretized. To overcome these issues, and with advancements in deep (D-) RL in the recent decade, many DRL-based algorithms have been developed to solve VVC problems. In [19], discrete voltage setpoints are optimized with a deep Q network (DQN) algorithm for a VVC model including switching shunt elements, OLTC tap ratios, and generator terminal voltage setpoints in a transmission system. Similarly, [20] applies a batch reinforcement learning algorithm for optimizing OLTC tap ratio settings. A constrained soft actor-critic algorithm has been proposed in [21], to solve a VVC problem containing OLTCs, CBs, and voltage regulators. Reference [22] proposes a two-timescale VVC method, in which the slow responsive CB switching control is based on DQN, while the fast responsive inverter reactive power control is achieved with the SOCP algorithm. Moreover, [23] proposes an autonomous voltage control method based on DQN for OLTC tap ratios and switching shunt elements, as well as a deep deterministic policy gradient (DDPG) algorithm for voltage setpoints of distributed generators. However, most of the above DRL-based methods are applied for centralized control frameworks, which are computationally expensive and suffer from privacy issues. Recently, [24] applies a multi-agent DDPG (MADDPG) algorithm [25] to solve fully decentralized inverter-based VVC, with each inverter modeled as an agent. The algorithm outperforms conventional programming based centralized and decentralized droop control methods. Further, an attention enabled MADDPG algorithm for decentralized inverter-based VVC has been proposed in [26], where a multi-agent twin delayed DDPG algorithm (MATD3) is developed for voltage regulation with unsupervised clustering based network partition. The simulations in this wok indicate advances over conventional centralized control methods."

> _[Section I, Introduction — gap identification motivating this work]_

"Nonetheless, temporal intermittencies and spatial variations of renewable power generation and loads are still not fully considered or addressed in the existing methods. Furthermore, most of the above works do not consider the usage of historical expert operation data or equivalent which could further improve the performance of DRL agents in the training process."

### Cited references (resolved from the paper's bibliography)
- **[3]** W. Zheng, W. Wu, B. Zhang, Y. Wang. *Robust reactive power optimisation and voltage control method for active distribution networks via dual time-scale coordination.* IET Gener. Transm. Distrib., 2017.
- **[4]** C. Zhang, Y. Xu, Z. Dong, J. Ravishankar. *Three-stage robust inverter-based voltage/var control for distribution networks with high-level PV.* IEEE Trans. Smart Grid, 2019.
- **[11]** W. Huang, W. Zheng, D. J. Hill. *Distributionally robust optimal power flow in multi-microgrids with decomposition and guaranteed convergence.* IEEE Trans. Smart Grid, 2021.
- **[12]** H. Saberi, C. Zhang, Z. Y. Dong. *Data-driven distributionally robust hierarchical coordination for home energy management.* IEEE Trans. Smart Grid (early access), 2021.
- **[13]** C. Zhang, Y. Xu. *Hierarchically-coordinated voltage/VAR control of distribution networks using PV inverters.* IEEE Trans. Smart Grid, 2020.
- **[14]** T. Ding, Q. Yang, Y. Yang, C. Li, Z. Bie, F. Blaabjerg. *A data-driven stochastic reactive power optimization considering uncertainties in active distribution networks and decomposition method.* IEEE Trans. Smart Grid, 2018.
- **[16]** J. G. Vlachogiannis, N. D. Hatziargyriou. *Reinforcement learning for reactive power control.* IEEE Trans. Power Syst., 2004.
- **[17]** Y. Xu, W. Zhang, W. Liu, F. Ferrese. *Multiagent-based reinforcement learning for optimal reactive power dispatch.* IEEE Trans. Syst., Man, Cybern. C, 2012.
- **[18]** Y. Li. *Deep reinforcement learning: An overview.* arXiv 2017.
- **[19]** R. Diao, Z. Wang, D. Shi, Q. Chang, J. Duan, X. Zhang. *Autonomous voltage control for grid operation using deep reinforcement learning.* IEEE PES General Meeting (PESGM), 2019.
- **[20]** H. Xu, A. D. Domínguez-García, P. W. Sauer. *Optimal tap setting of voltage regulation transformers using batch reinforcement learning.* IEEE Trans. Power Syst., 2020.
- **[21]** W. Wang, N. Yu, Y. Gao, J. Shi. *Safe off-policy deep reinforcement learning algorithm for volt-VAR control in power distribution systems.* IEEE Trans. Smart Grid, 2020.
- **[22]** Q. Yang, G. Wang, A. Sadeghi, G. B. Giannakis, J. Sun. *Two-timescale voltage control in distribution grids using deep reinforcement learning.* IEEE Trans. Smart Grid, 2020.
- **[23]** J. Duan et al. *Deep-reinforcement-learning-based autonomous voltage control for power grid operations.* IEEE Trans. Power Syst., 2020.
- **[24]** D. Cao, W. Hu, J. Zhao, Q. Huang, Z. Chen, F. Blaabjerg. *A multi-agent deep reinforcement learning based voltage regulation using coordinated PV inverters.* IEEE Trans. Power Syst., 2020.
- **[25]** R. Lowe, Y. I. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[26]** D. Cao, J. Zhao, W. Hu, F. Ding, Q. Huang, Z. Chen. *Attention enabled multi-agent DRL for decentralized volt-VAR control of active distribution system using PV inverters and SVCs.* IEEE Trans. Sustain. Energy, 2021.
