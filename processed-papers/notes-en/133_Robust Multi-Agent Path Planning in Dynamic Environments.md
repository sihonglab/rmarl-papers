# 133. Path Planning Through Multi-Agent Reinforcement Learning in Dynamic Environments

## Metadata
- **Title**: Path Planning Through Multi-Agent Reinforcement Learning in Dynamic Environments
- **Authors**: Jonas De Maeyer, Hossein Yarahmadi, Moharram Challenger
- **Affiliation**: University of Antwerp (UA) and Flanders Make (Dept. of Computer Science); Ayatollah Boroujerdi University, Boroujerd, Iran (Dept. of Computer Engineering)
- **Venue**: Not specified (technical report; arXiv preprint)
- **Link/arXiv**: arXiv:2511.15284v1 [cs.RO], 19 Nov 2025; code: https://github.com/micss-lab/MARL4DynaPath

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty from dynamic obstacles (obstacles change over time, introducing uncertainty); robustness here means reliable adaptation/replanning when the maze layout changes, not adversarial or distributionally-robust MARL.
- **Method paradigm**: Hierarchical (quadtree) decomposition of the environment, tabular Q-learning, federated Q-learning (FedAsynQ), success-rate-based conditional retraining; DTDE (single-agent) and CTDE (federated within a sub-environment).
- **Keywords**: Path Planning, Multi-Agent Reinforcement Learning, Dynamic Environment, Federated Q-learning, Hierarchical Planning

## TL;DR
A scalable, region-aware MARL framework that recursively decomposes a dynamic maze into a tree of sub-environments and adapts to moving obstacles by selectively retraining (escalating up the hierarchy when needed) using single-agent or federated asynchronous Q-learning, with the two federated variants (fedAsynQ_EqAvg, fedAsynQ_ImAvg) achieving accuracy close to an A* Oracle upper bound while keeping adaptation time low.

## Problem & Motivation
Path planning in dynamic environments (where obstacles change over time, introducing uncertainty) is essential for mobile robots, but classical planners like A* require full, up-to-date knowledge of the environment and replan poorly/inefficiently when changes occur. Most MARL approaches assume environmental changes are unlocalizable, causing unnecessary global replanning. Yarahmadi et al. proposed a region-aware approach that localizes changes and replans only affected sub-environments, but it (1) relies on a global path planner (unusable in unknown environments and poorly scalable), (2) triggers RL replanning on every change regardless of impact, (3) confines each agent to an isolated sub-environment with no fallback when a charging station is absent/unreachable, and (4) is evaluated only in overly simplistic environments with a single obstacle change per time step. This work addresses these gaps.

## Robustness Setting
- **Threat model / uncertainty set**: Uncertainty arises from dynamic obstacles that can move (and appear/disappear) over time, modeled by modifying the MDP's reward function and grid positions. Up to 10 simultaneous obstacle changes per time step are sampled from a skewed distribution (smaller numbers of changes far more probable). A "region-aware dynamicity assumption" holds: changes can be detected and localized to specific leaf sub-environments.
- **Setting**: Cooperative/distributed multi-robot navigation; single-agent variants follow DTDE, federated variants follow CTDE within each sub-environment; online tabular RL; environment assumed initially unknown for the RL methods (global planner unavailable).

## Method
- **Hierarchical decomposition (quadtree)**: Recursively bisect the environment along both dimensions into four children until sub-environments are at most 20×20, forming a tree (root = whole environment, leaves = smallest regions). Each node holds a Q-table; each leaf gets one (or, in federated mode, multiple) agent(s) trained independently and in parallel across CPU cores.
- **Region-aware retraining + hierarchical escalation**: When changes are localized to leaf nodes, only those are considered. If local leaf retraining is insufficient (e.g., no reachable charging station), retraining escalates one level up (covering siblings, expanding scope by 4×), in the worst case up to the root.
- **Retraining condition (success rate)**: Success rate = (number of states with a valid greedy path to a charging station) / (number of states). Retraining is triggered when the success rate drops by more than a threshold (0.01) between consecutive time steps, or falls below a minimum acceptable level (0.9). Q-tables are propagated upward and downward to keep policies consistent across the hierarchy (a consolidated root Q-table stores the most up-to-date policy).
- **Four approaches**: (1) onlyTrainLeafNodes — single-agent Q-learning, leaf-level only (mirrors Yarahmadi et al.); (2) singleAgent — single-agent Q-learning with the full tree strategy; (3) fedAsynQ_EqAvg — federated asynchronous Q-learning with equal averaging + tree strategy; (4) fedAsynQ_ImAvg — federated asynchronous Q-learning with importance (visit-count) weighted averaging + tree strategy. Federated Q-learning (after Woo et al.) lets K=12 agents collect trajectories asynchronously, update local Q-values, and periodically aggregate into a shared Q-table. Single-agent methods also use an experience replay buffer, prioritized starting-position sampling, and convergence-based stopping; federated methods use a fixed iteration budget T = r×c×200.

## Theoretical Contributions
- Time complexity analysis: Recursive decomposition (Algorithm 1) runs in Θ(N) = Θ(RC) with recursion depth Θ(log max{R,C}) (via the Master Theorem); initial training Tinit = Θ(N); incremental retraining cost Tincr = O(min{N, K log M}) where K is the number of affected leaves and M = max{R,C}.
- Otherwise mostly empirical; convergence guarantees for the underlying methods are cited from prior work (Q-learning convergence; FedAsynQ finite-time convergence of Woo et al.).

## Experiments
- **Environment/Benchmark**: Randomly generated 2D maze grids (free space, dynamic obstacles, charging stations) modeled as MDPs; 8 cardinal/diagonal actions; deterministic transitions; γ=0.9; reward +100 (charging station), −10 (obstacle), −1 (other move). Sizes: 20×20, 50×50, 100×100, 200×200, 300×300. Difficulties: easy/medium/hard (varying obstacle, charging-station, and free-space densities). Up to 10 simultaneous obstacle changes per step; 2×r time steps for an r×r maze. A 50×50 "edge case" maze where the top-left 25×25 quadrant has no charging stations.
- **Baselines**: A* Static (plans once, never updates) and A* Oracle (full knowledge each step, replans entire grid). The four RL approaches are also compared against each other.
- **Evaluation metrics**: Accuracy (success rate), adaptation time, cumulative adaptation time, average path length, initial training time.

## Key Results
- The two federated Q-learning approaches (fedAsynQ_EqAvg, fedAsynQ_ImAvg) consistently perform best, achieving accuracy close to A* Oracle across all sizes and difficulties while keeping adaptation times low; fedAsynQ_EqAvg has a slight edge (lower cumulative adaptation time, slightly shorter paths, simpler aggregation).
- onlyTrainLeafNodes matches A* Oracle in easy environments but degrades badly in medium/hard settings (below 90% accuracy on several sizes, sometimes worse than A* Static), confirming leaf-only retraining is insufficient; the hierarchical methods recover this.
- Federated Q-learning substantially reduces initial training time vs single-agent (e.g., ~150–200 s vs ~350–600 s for single-agent at 300×300 in medium/hard), and A* Oracle's adaptation time grows steeply with size (≈6 s/step easy, ≈9 s/step hard at 300×300), showing the RL methods' scalability advantage. Paths are slightly longer than A* Oracle but acceptable.

## Limitations & Future Work
- **Suboptimal path lengths**: learned policies give longer paths than A* Oracle; a trade-off between path optimality and adaptation speed (the work prioritizes fast adaptation).
- **Initial training overhead**: tabular RL needs extensive exploration; initial training is time-intensive in large unknown environments despite parallelization.
- **Hierarchical decomposition constraints**: only supports environments with known dimensions and rectangular/square shapes (grid-like), not arbitrary/irregular shapes.
- **Simplified MDP abstraction**: agents occupy abstract states, ignore collisions with each other and sensor noise; best viewed as a software solution, not directly deployable to real robots.
- **Future work**: integrate Deep RL (DQN/actor-critic) for generalization; action masking for path optimality; transfer learning to cut initial training time; scale to larger maps (500×500, 1000×1000); extend to 3D (UAVs) and irregular shapes; alternative aggregation strategies; real-world robotic implementation with perception and collision avoidance.

## Relevance to Survey
This paper sits on the "environment/model uncertainty" line of robust MARL, but interprets robustness as reliable, efficient adaptation to dynamic (time-varying) environments rather than adversarial perturbation or distributionally-robust formulations. Its methodological contributions — hierarchical/region-aware decomposition, conditional (success-rate-triggered) retraining, and federated Q-learning for parallel knowledge sharing — connect to the scalability/fault-tolerance and distributed-learning themes of MARL. It is an applied (path-planning / robotics) data point illustrating how MARL achieves robust adaptation under environmental uncertainty, and is useful as a contrast to theory-driven robust-MARL/robust-MDP works.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.1, Introduction — Problem Context]_

"The dynamic nature of real-world environments can lead to situations where the environment is partially or entirely unknown, making it difficult, or even impossible, to solve the path planning problem using traditional techniques alone. Classical algorithms such as Dijkstra's or A* become inadequate under such uncertainty, as they require a complete representation or model of the environment. This limitation creates a pressing need for new algorithms, or adaptations of existing ones, that can handle dynamicity while still producing accurate and efficient paths."

"Many RL-based approaches have already been proposed to address dynamic environments, and several notable contributions are discussed in Section 3. However, a specific research direction remains underexplored. Most MARL-based solutions assume that changes in the environment, such as moving obstacles, are unlocalizable. That is, agents are expected to adapt to environmental changes without knowing where those changes occurred. This often leads to inefficient and unnecessary re-planning: agents may revise their strategies even when no relevant changes have occurred within their operational region."

"To address this inefficiency, Yarahmadi et al. [13] proposed a novel MARL-based approach that introduces a localized change detection assumption. Their method assumes that changes in the environment can be detected and localized to specific regions, allowing replanning to occur only where it is needed. If no changes are detected in the environment, a global path planner (e.g., A*) is used to navigate to a charging station. If changes are detected, the environment is divided into sub-environments, each managed by an agent responsible for finding paths to a charging station using Q-learning. This targeted replanning strategy greatly reduces unnecessary computation."

> _[Section 3.2.1, Literature Review — Perception-Driven Approaches]_

"Liu et al. [28] introduced the Multi-Agent Path Planning with Evolutionary Reinforcement Learning (MAPPER) method, which also uses an image-based representation to model dynamic obstacle behavior. The approach is decentralized, meaning agents learn optimal actions on their own using local observations without using any form of communication. It employs evolutionary RL in a decentralized setting to train agents. Advantage Actor-Critic (A2C) is used to update the model parameters of the actor-critic network. The authors acknowledge that collisions with dynamic obstacles in complex environments may still occur."

"Guan et al. [29] proposed Attention and BicNet-based Multi-agent path planning with effective reinforcement (AB-Mapper), which builds upon MAPPER and introduces agent communication via a BicNet (bidirectional LSTM). It operates within an actor-critic framework and is designed for dynamic environments. It also operates an attention mechanism in the critic network that allows agents to focus on the actions and states of the most relevant neighboring agents. The approach aligns with the CTDE paradigm, allowing decentralized execution. Its reliance on DNNs makes it computationally intensive, however."

> _[Section 3.2.4, Literature Review — Fully Decentralized MARL]_

"Guo et al. [35] proposed the Decentralized Path Planning model using Deep Reinforcement Learning (DPPDRL), a decentralized approach for coordinating Automated Guided Vehicless (AGVs) in dynamic Robotic Mobile Fulfillment System (RMFS) environments. Following the DTDE paradigm, the method enables agents to make real-time decisions based solely on local observations. A carefully designed reward function and state space allow the system to remain robust under dynamic conditions, with each agent learning and acting independently."

> _[Section 3.3.1, Literature Review — Region-Aware MARL Methodology of Yarahmadi et al.]_

"Yarahmadi et al. [13] identify a critical limitation in classical path planning algorithms such as A*, which, while effective in static environments, become inefficient in dynamic settings where obstacles change over time. These algorithms lack incremental update mechanisms and instead require full replanning whenever the environment changes, leading to substantial computational overhead."

"To address this inefficiency, the authors introduce a key assumption: although the environment is dynamic, the locations of changes can be detected and localized with reasonable precision. Based on this assumption, they propose a region-aware replanning strategy that confines path updates to only the affected parts of the environment, avoiding unnecessary global recomputation. This perspective is rarely considered in the MARL literature."

> _[Section 4.5, Methodology — Multi-Agent Reinforcement Learning, on federated Q-learning]_

"To align with these objectives, we draw on the work of Woo et al. [44], which analyzes federated Q-learning. This approach enhances Q-learning by enabling multiple agents to learn policies and periodically aggregate their Q-tables. Woo et al. explore both synchronous and asynchronous variants of federated Q-learning. This technical report focuses on the asynchronous variant, as its experiments demonstrate superior performance, requiring fewer samples to estimate the optimal action-value function."

### Cited references (resolved from the paper's bibliography)
- **[13]** Yarahmadi, Marah, Challenger. *Comparative analysis of classic and reinforcement learning approaches for robot navigation in dynamic environments.* University of Antwerp and Flanders Make Strategic Research Center, 2024.
- **[28]** Liu, Chen, Zhou, Koushik, Hebert, Zhao. *Mapper: Multi-agent path planning with evolutionary reinforcement learning in mixed dynamic environments.* IEEE/RSJ IROS 2020.
- **[29]** Guan, Gao, Zhao, Yang, Deng, Lam. *Ab-mapper: Attention and bicnet based multi-agent path planning for dynamic environment.* IEEE/RSJ IROS 2022.
- **[35]** Guo, Ji, Yao, Chen. *A decentralized path planning model based on deep reinforcement learning.* Computers and Electrical Engineering, 2024.
- **[44]** Woo, Joshi, Chi. *The blessing of heterogeneity in federated q-learning: Linear speedup and beyond.* Journal of Machine Learning Research, 2025.
