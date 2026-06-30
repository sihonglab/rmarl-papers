# 122. Optimal Bi-Level Bidding and Dispatching Strategy Between Active Distribution Network and Virtual Alliances Using Distributed Robust Multi-Agent Deep Reinforcement Learning

## Metadata
- **Title**: Optimal Bi-Level Bidding and Dispatching Strategy Between Active Distribution Network and Virtual Alliances Using Distributed Robust Multi-Agent Deep Reinforcement Learning
- **Authors**: Ziqing Zhu, Ka Wing Chan, Shiwei Xia, Siqi Bu
- **Affiliation**: Department of Electrical Engineering, The Hong Kong Polytechnic University, Hong Kong SAR, China; State Key Laboratory of Alternate Electrical Power System With Renewable Energy Sources, North China Electric Power University, Beijing, China
- **Venue**: IEEE Transactions on Smart Grid, Vol. 13, No. 4, July 2022
- **Link/arXiv**: DOI 10.1109/TSG.2022.3164080

## Taxonomy
- **Robustness / perturbation type targeted**: Reward-function uncertainty driven by net-load (renewable distributed generation + load) prediction error; risk of financial penalty from day-ahead/real-time imbalance ("risk of misconduct"). Modeled as an uncertainty set on the net-load prediction error governed by a "nature" agent.
- **Method paradigm**: Robust Nash equilibrium (RNE), multi-agent DDPG (actor-critic), minimax / worst-case (max over policy, min over uncertainty), nature player, fully distributed training via estimated policy functions (EPF)
- **Keywords**: Active distribution network, distributed virtual alliance, bidding strategy, reinforcement learning, robust Nash equilibrium, DDPG

## TL;DR
The paper formulates the day-ahead bi-level bidding (by distributed virtual alliances) and dispatching (by the distribution system operator) problem as a stochastic dynamic program / MDP and solves it with a new Distributed Robust Multi-Agent DDPG (DRMA-DDPG) algorithm that converges to a robust Nash equilibrium, providing a fully distributed, risk-averse method that mitigates financial losses caused by net-load prediction uncertainty.

## Problem & Motivation
In a deregulated active distribution network (ADN), autonomous distributed virtual alliances (DVAs) — virtual microgrids (VMGs) and virtual power plants (VPPs) — submit available capacity and bidding prices to the distribution system operator (DSO), who performs optimal dispatching and sets the market clearing price (MCP). The uncertainty of renewable distributed generation (RDG) and load demand creates a net-load prediction error that drives real-time balancing costs and complicates both market regulation design and the energy schedule of DVAs and DSO. Prior bi-level dispatch models rely on mathematical programming (static, cannot adapt to changing conditions) or model predictive control (needs accurate net-load prediction). RL approaches based on value iteration (model-based, Q-learning, WoLF-PHC) only handle discrete state/action spaces and suffer the curse of dimensionality, while existing DDPG-based bidding/dispatching methods still require access to other DVAs' confidential bidding strategies and ignore the net-load uncertainty and its impact on decisions.

## Robustness Setting
- **Threat model / uncertainty set**: The net-load prediction error of DVAs is treated as uncertain. A "nature" agent draws a random net-load prediction error from an uncertainty set Ẽᵏ_t according to a distribution μ⁰,ᵏ, inducing a penalty Lᵏ_t that corrects each agent's reward Rᵏ_t. The robust solution maximizes reward under the worst-case realization (max over agent/opponent policies, min over the uncertainty distribution).
- **Setting**: Mixed (competitive bidding among DVAs plus DSO dispatching, a bi-level/hierarchical interaction); multi-agent; fully distributed training and execution (no access to other agents' policies); online deep RL.

## Method
- Formulates the bi-level optimal bidding and dispatching strategy (OBDS) model: each DVA (CDG/VPP/VMG) maximizes revenue minus generation cost and misconduct penalty, while the DSO minimizes purchasing cost minus selling revenue plus a total-prediction-error term, subject to capacity, ramping, line, and curtailment constraints. The model is recast as a stochastic dynamic program and then an MDP τ = ⟨S, A, P, R⟩.
- Builds on the baseline DDPG actor-critic (online/target networks, experience replay buffer, soft update) to handle continuous state/action spaces, then extends to the multi-agent setting where each agent's expected reward depends on all agents' policies (Nash equilibrium).
- Incorporates the Robust Nash Equilibrium (RNE): a robust value function defined as Maxμ Min over the worst-case reward set, with policy gradients derived for the agent policy μᵏ, opponent policies μ⁻ᵏ, and the nature policy μ⁰,ᵏ; gradients are estimated by Monte Carlo over mini-batches from the replay buffer.
- Makes training fully distributed via an estimated policy function (EPF) #μᵏ that replaces the unavailable opponent policies μ⁻ᵏ when updating the critic, refreshed by minimizing a cross-entropy penalty — so each agent trains without other agents' confidential bidding strategies.
- Adds practical tricks inherited from DDPG fixes: double critic networks (take the smaller Q-value) against Q-value overestimation, delayed critic update (every two steps), and delayed soft target update (every four steps).

## Theoretical Contributions
- Defines the robust MDP and the robust Nash equilibrium (RNE) condition (Eqs. 17–20) and a robust value-function Bellman recursion; derives the policy-gradient expressions for the agent, opponent, and nature policies (Eqs. 23–24). The paper claims the algorithm "would converge to RNE" but provides no formal convergence proof or sample-complexity analysis. Mostly empirical.

## Experiments
- **Environment/Benchmark**: A test market of 5 distributed DVAs built on a modified IEEE 33-Bus (33-Node) network; network/line parameters from [33], renewable output, load profile, and prediction-error scenarios from [34]; real-time dispatching and penalty calculation from [32]. Implemented in TensorFlow (Python) on a laptop with Intel i7-4870HQ 2.5 GHz CPU, 32 GB RAM. Bidding price limit [1, 1.5] (kWh/RMB).
- **Baselines**: MA-DDPG, DDPG, Deep Q-Learning.
- **Evaluation metrics**: Convergence speed (episodes to converge), average reward and worst-case (lowest) reward under uncertainty, total 24-hour reward of DVAs, MCP behavior, DSO dispatching/capacity-allocation results and rewards.

## Key Results
- DRMA-DDPG converges within about 8000 episodes, while MA-DDPG, DDPG, and Deep Q-Learning fail to converge under reward and bidding-strategy uncertainty.
- Both the total reward and the lowest (worst-case) reward of DRMA-DDPG are apparently higher than the baselines, attributed to effective risk mitigation by converging to the RNE.
- Strategic analysis shows DVAs uplift bids to deliberately let bids fail when the misconduct penalty would yield negative reward; reducing the penalty to ~30% of the rated value lowers bidding prices off-peak (better social welfare) but discourages prediction-accuracy improvement.
- The DSO with DRMA-DDPG dispatches more conservatively (less from high-renewable VPP1/VPP2, more from controllable VPP3/VPP4/VMG1), slightly lowering reward in some slots but mitigating large real-time imbalance penalties and raising DSO reward overall.

## Limitations & Future Work
- Inherits DDPG drawbacks, especially Q-value overestimation that can accumulate and trap the agent in local optima, and limited exploration from deterministic policy gradients (addressed only heuristically via double critics and delayed updates).
- No formal convergence guarantee for the claimed RNE convergence; results are empirical on a single 5-DVA modified IEEE 33-bus testbed.
- The proper setting of the misconduct penalty is unresolved and "still requires further in-depth investigations." Future work focuses on using the algorithm to simulate emerging market paradigms and provide theoretical/practical support for market operation.

## Relevance to Survey
A domain (power-market) application of robust MARL that directly adopts the robust Nash equilibrium and nature-player paradigm from the M3DDPG line ([30] = Li et al., AAAI 2019) and the multi-agent actor-critic / estimated-policy-function ideas from MADDPG ([31] = Lowe et al.). It connects the "model/reward uncertainty" robustness theme with practical multi-agent deep RL (R-MADDPG-style minimax), and adds a fully distributed training variant (privacy-preserving EPF). Useful as an example of how robust Markov game / RNE concepts transfer to competitive cooperative real-world multi-agent systems.

## Related Work (verbatim excerpts from the paper)
> _[Section I.B, Literature Review]_

"A considerable amount of literature has been published on downstream DVA dispatching in the ADN with uncertainties. In [9], a bi-level robust economic dispatch model for microgrids (MGs) in the ADN was proposed, in which the upper level is a two-stage robust economic dispatch model of ADN, and the self-dispatch of MGs based on MCP prediction is formulated in the lower level. A similar bi-level dispatching model between VPP and ADN was developed in [10], and solved by using Karush-Kuhn-Tucker (KKT) optimality conditions, Fortuny-Amat transformation and the strong duality theorem. The demand response (DR) was incorporated into ADN in [11] and [12] with participation of MGs, while multiple objective functions were simultaneously considered. However, these works are based on mathematical programming methods to re-formulate the problem to a single-level convex optimization model. Hence, the decision making is static and cannot respond to change of conditions, such as variation of available capacities, RDG outputs, load demand. As a remedy, model prediction control (MPC) was adopted in [13] and [14], in which accurate net load prediction is required but hard to archive in practice."

> _[Section I.B, Literature Review]_

"With the emergence of AI techniques, Reinforcement Learning (RL) in the multi-agent interaction environment provides potential solutions for dynamic bidding simulation and market equilibrium computation. However, algorithms, such as conventional model-based method [15], Q-learning [16], WoLF-PHC algorithm [17], adopted the value function iteration method can only deal with the discrete state and action space. Hence, for scalability, the “curse of dimensionality” [18] will render such algorithms intractable. In addition, the conventional model-based RL requires detailed modeling of environment, which is not applicable considering the uncertainty of both the reward function and state transition probability."

> _[Section I.B, Literature Review]_

"The emerging deep deterministic policy gradient (DDPG) [18] is the state-of-the-art tool to deal with the continuous states and actions by updating the parameterized neural network using the policy gradient descent method instead of value function iteration, and has been successfully applied to solve the dynamic dispatching of DVAs in ADN in [19]–[21]. In [20], a cooperative DRL algorithm for distributed economic dispatch of MGs was proposed, in which a diffusion strategy is incorporated to coordinate the actions of distributed generating units and energy storage systems. In [21], two modiﬁcations of the DDPG algorithm were proposed to facilitate the dispatching of MGs considering the non-observable state information. However, this method still has the following limitations: ﬁrstly, the update of neural network still requires the availability of other DVA’s bidding strategies, which is conﬁdential and therefore cannot be accessed; secondly, the uncertainties of net load and the energy trading between DVAs and DSO were not incorporated; lastly, the impact of such uncertainty to their decisions is not considered, which is an important indicator while simulating the bidding and dispatching procedure."

> _[Section I.B, Literature Review]_

"The optimal bidding strategy for DVAs is well-investigated in previous literature [22]–[26]. While the net load uncertainty of DVAs is considered in [21]–[23] using stochastic and robust optimization, the more promising DDPG algorithm for dynamic bidding strategy modiﬁcation was adopted in [24]–[26] without consideration of uncertainty. However, DDPG still requires the bidding information of other DVAs, which would not be available in the competitive electricity market."

> _[Section III.B, Robust MA-DDPG Under Uncertainty — definition of RNE]_

"However, the optimal decision μᵏ∗ should be robust to any risk of penalty resulted from the uncertainty of DVA net load. Hence, based on the MDP for multi-agent environment, the robust MDP is deﬁned as follows: ... where Rᵏt ∈ R denotes reward considering potential risks. Let μ0,k ∈ Ẽᵏt be the probability distribution of uncertainty set of net load prediction error, and the resulted penalty is denoted as Lᵏt, the robust Nash equilibrium (RNE) [30] can be deﬁned as: ..."

> _[Section III.C, Fully-Distributed Robust MA-DDPG — estimated policy function]_

"As shown in (26) and (27), the availability of other agents’ policies is required while updating the critic network. However, such assumption cannot be held in the deregulated and competitive electricity market, as the policy of each involved stakeholder including DVAs and DSO is conﬁdential. In this paper, this issue is tackled by the estimated policy function (EPF) [31] of other agents. Each agent will use the EPF #μᵏ ϑ−kt instead of μ−k to update the critic network, while the EPF is refreshed by minimizing the penalty function: ..."

### Cited references (resolved from the paper's bibliography)
- **[9]** Z. Yi, Y. Xu, J. Zhou, W. Wu, H. Sun. *Bi-level programming for optimal operation of an active distribution network with multiple virtual power plants.* IEEE Trans. Sustainable Energy 2020.
- **[10]** H. Haddadian, R. Noroozian. *Multi-microgrid-based operation of active distribution networks considering demand response programs.* IEEE Trans. Sustainable Energy 2019.
- **[11]** X. Zhou, Q. Ai, M. Yousif. *Two kinds of decentralized robust economic dispatch framework combined distribution network and multi-microgrids.* Applied Energy 2019.
- **[12]** M. Xie, X. Ji, X. Hu, P. Cheng, Y. Du, M. Liu. *Autonomous optimized economic dispatch of active distribution system with multi-microgrids.* Energy 2018.
- **[13]** Y. Du, F. Li. *Intelligent multi-microgrid energy management based on deep neural network and model-free reinforcement learning.* IEEE Trans. Smart Grid 2020.
- **[14]** C. A. Hans, P. Sopasakis, J. Raisch, C. Reincke-Collon, P. Patrinos. *Risk-averse model predictive operation control of islanded microgrids.* IEEE Trans. Control Systems Technology 2020.
- **[15]** S. Totaro, I. Boukas, A. Jonsson, B. Cornélusse. *Lifelong control of off-grid microgrid with model-based reinforcement learning.* Energy 2021.
- **[16]** J. Viehmann, S. Lorenczik, R. Malischek. *Multi-unit multiple bid auctions in balancing markets: An agent-based Q-learning approach.* Energy Economics 2021.
- **[17]** X. Gao, K. W. Chan, S. Xia, X. Zhang, K. Zhang, J. Zhou. *A multiagent competitive bidding strategy in a pool-based electricity market with price-maker participants of WPPs and EV aggregators.* IEEE Trans. Industrial Informatics 2021.
- **[18]** Y. Ye, D. Qiu, M. Sun, D. Papadaskalopoulos, G. Strbac. *Deep reinforcement learning for strategic bidding in electricity markets.* IEEE Trans. Smart Grid 2020.
- **[19]** P. Kou, D. Liang, C. Wang, Z. Wu, L. Gao. *Safe deep reinforcement learning-based constrained optimal control scheme for active distribution networks.* Applied Energy 2020.
- **[20]** W. Liu, P. Zhuang, H. Liang, J. Peng, Z. Huang. *Distributed economic dispatch in microgrids based on cooperative reinforcement learning.* IEEE Trans. Neural Networks and Learning Systems 2018.
- **[21]** L. Lei, Y. Tan, G. Dahlenburg, W. Xiang, K. Zheng. *Dynamic energy dispatch based on deep reinforcement learning in IoT-driven smart isolated microgrids.* IEEE Internet of Things Journal 2021.
- **[22]** X. Lu et al. *Optimal bidding strategy of DER aggregator considering dual uncertainty via information gap decision theory.* IEEE Trans. Industry Applications 2021.
- **[23]** G. Liu, Y. Xu, K. Tomsovic. *Bidding strategy for microgrid in day-ahead market based on hybrid stochastic/robust optimization.* IEEE Trans. Smart Grid 2016.
- **[24]** N. Rezaei, A. Ahmadi, A. Khazali, J. Aghaei. *Multiobjective risk-constrained optimal bidding strategy of smart microgrids: An IGDT-based normal boundary intersection approach.* IEEE Trans. Industrial Informatics 2019.
- **[25]** Y. Liang, C. Guo, Z. Ding, H. Hua. *Agent-based modeling in electricity market using deep deterministic policy gradient algorithm.* IEEE Trans. Power Systems 2020.
- **[26]** Y. Du, F. Li, H. Zandi, Y. Xue. *Approximating Nash equilibrium in day-ahead electricity market bidding with multi-agent deep reinforcement learning.* J. Modern Power Systems and Clean Energy 2021.
- **[30]** S. Li, Y. Wu, X. Cui, H. Dong, F. Fang, S. J. Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[31]** R. Lowe, Y. Wu, A. Tamar, J. Harb, J. Abbeel. *Multi-agent actor-critic for mixed cooperative-competitive environments.* arXiv:1706.02275, 2020.
