# 146. MARS: A Meta-Adaptive Reinforcement Learning Framework for Risk-Aware Multi-Agent Portfolio Management

## Metadata
- **Title**: MARS: A Meta-Adaptive Reinforcement Learning Framework for Risk-Aware Multi-Agent Portfolio Management
- **Authors**: Jiayi Chen, Jing Li, Guiling Wang
- **Affiliation**: Department of Computer Science, New Jersey Institute of Technology
- **Venue**: AAAI 2026 (copyright notice "© 2026, Association for the Advancement of Artificial Intelligence"); arXiv preprint
- **Link/arXiv**: arXiv:2508.01173v2 [cs.LG], 2 Dec 2025

## Taxonomy
- **Robustness / perturbation type targeted**: Market non-stationarity / regime shift (bull vs. bear vs. volatile markets); financial tail risk and sudden market shocks. "Robustness" here means a disciplined portfolio that holds up across changing market regimes — not adversarial attacks or formal model uncertainty.
- **Method paradigm**: Risk-sensitive / risk-aware RL (Safety-Critic with safety threshold and penalty), hierarchical meta-learning controller, heterogeneous multi-agent ensemble, DDPG actor-critic, ensemble weighting (CTDE-style aggregation).
- **Keywords**: portfolio management, risk-aware RL, Safety-Critic, meta-adaptive controller, heterogeneous agent ensemble, non-stationarity

## TL;DR
MARS is a two-tier risk-aware multi-agent DRL framework for portfolio management that combines a Heterogeneous Agent Ensemble of DDPG agents with distinct risk profiles (each enforced by a Safety-Critic network) and a high-level Meta-Adaptive Controller that dynamically reweights the agents per market state, reducing maximum drawdown and volatility while maintaining competitive returns across market regimes.

## Problem & Motivation
Generic DRL applied to portfolio management faces two interconnected limitations: (1) financial markets are noisy and pervasively non-stationary, violating the stationary-MDP assumption, so models trained in one regime (e.g., a low-volatility bull market) often fail catastrophically when the regime shifts; and (2) risk is treated superficially — typically handled reactively via reward shaping (e.g., Sharpe-ratio reward or drawdown penalties) rather than proactively managed within the decision process, leaving agents vulnerable to tail risks and sudden shocks. MARS aims to explicitly address this dual challenge of non-stationarity and risk by decoupling risk preference/management from market adaptation.

## Robustness Setting
- **Threat model / uncertainty set**: No formal adversary or uncertainty set. The source of "perturbation" is the non-stationary financial environment whose statistical properties change over time (regime shifts between bull/bear/volatile markets). Risk is captured by a custom environment risk score Cenv in [0,1] (40% Simulated Volatility, 30% Portfolio Concentration, 30% Leverage) that the Safety-Critic learns to predict, plus a rule-based overlay (position-concentration limit, cash buffer, no short-selling).
- **Setting**: Cooperative ensemble of heterogeneous agents (no competition between agents); hierarchical meta-control with centralized aggregation of decentralized agent proposals; online learning from historical market interaction (single-asset-set environment, daily data).

## Method
- **Heterogeneous Agent Ensemble (HAE)**: N = 10 distinct DDPG-based Safety-Critic agents, each defined by a unique intrinsic risk profile (safety threshold θ_i, risk-aversion weight λ_i) spanning ultra-conservative to highly aggressive. Each agent has Actor, Critic, and Safety-Critic networks.
- **Safety-Critic + Conditional Safety Penalty (CSP)**: The Safety-Critic C_ξi learns to predict the environment risk Cenv of a state-action pair (trained via MSE against Cenv). The actor is updated by a policy gradient augmented with a CSP that penalizes the policy only when the predicted risk C_ξi exceeds that agent's tolerance θ_i (a ReLU(C − θ_i) hinge weighted by λ_i).
- **Meta-Adaptive Controller (MAC)**: A neural meta-policy that maps the market state s_t to a softmax weight vector w_t over the agents; the final action A_t is the weighted sum of agents' proposed actions. MAC is trained to minimize the negative of a custom utility = (mean / std of the ensemble's weighted predicted Q-values, a Sharpe-like term) minus λ_meta times the ensemble's weighted predicted risk, so it favors high, stable returns with low predicted risk and adapts reliance between conservative and aggressive agents per regime.
- **Risk Management Overlay**: A rule-based fail-safe applied to A_t before execution — enforces position-concentration limits, a cash buffer for liquidity, and a ban on short-selling — yielding a risk-compliant executed action A'_t.
- **Reward**: R_t = (V_{t+1} − V_t)/V_t − C_t − ρ_t, i.e., portfolio rate of return minus transaction cost minus a risk-aversion penalty ρ_t = w_vol·σ_30d + w_dd·DD_30d (rolling 30-day volatility and max drawdown).

## Theoretical Contributions
None / mostly empirical. The paper contributes architectural design and loss/penalty formulations (CSP, environment risk score, MAC utility) but provides no convergence, sample-complexity, or equilibrium analysis.

## Experiments
- **Environment/Benchmark**: Historical daily data from two major global indices — Dow Jones Industrial Average (DJI) and Hang Seng Index (HSI), from Yahoo Finance; portfolios of 50 representative US stocks (vs. DJI) and 50 HSI constituents. Two test regimes: 2022 (volatile bear market) and 2024 (recent bull market), each with rolling training/validation/testing spans.
- **Baselines**: Market Index (buy-and-hold), DeepTrader (Wang et al. 2021b), HRPM (Wang et al. 2021a), AlphaStock (Wang et al. 2019); plus ablation variants MARS-Static (uniform fixed weights, no MAC), MARS-Homogeneous (identical risk profiles, different seeds), MARS-Div5 / MARS-Div15 (5 or 15 agents).
- **Evaluation metrics**: Cumulative Return (CR%), Annualized Return (AR%), Sharpe Ratio (SR), Annualized Volatility (AVol%), Maximum Drawdown (MDD%).

## Key Results
- On DJI 2024 (bull), MARS achieved the best across-the-board metrics: CR 29.50%, AR 31.19%, SR 2.84, MDD -5.39%; relative SR improvements of 70.6% (DJI 2022) and 101.4% (DJI 2024) over the best baseline.
- On HSI, MARS excelled at capital preservation in the 2022 bear market (best CR -14.50%, lowest AVol 22.56%, smallest MDD -32.72%); in 2024 it had the highest Sharpe Ratio among all models (35.5% relative improvement), though the passive HSI index had a higher raw return.
- Ablations confirm both components matter: removing MAC (MARS-Static) drops DJI-2024 CR from 29.50% to 17.10% and SR from 2.84 to 1.71; removing heterogeneity (MARS-Homogeneous) gives CR 22.21%, SR 1.85, worse MDD -7.81%. Ensemble size of 10 beats 5 and 15.
- Qualitatively, MAC adapts: in the 2022 bear market it is highly reactive/defensive (Aggressive-group allocation volatility >70% higher than 2024), while in 2024 it is stable and coordinated (Conservative–Aggressive allocation correlation deepens from -0.788 to -0.968).

## Limitations & Future Work
Not specified. (The paper states no explicit limitations or future-work section; it notes only that some baselines' performance is contingent on factors such as predictive-model accuracy, and that diminishing returns appear beyond a moderate ensemble size.)

## Relevance to Survey
This paper sits at the periphery of the Robust MARL landscape: it is a cooperative multi-agent (ensemble) RL system whose "robustness" goal is resilience to non-stationary market regimes and tail risk rather than adversarial perturbations or formal model/transition uncertainty. It connects to the risk-sensitive / safety-constrained RL theme (Safety-Critic, risk penalties) and to hierarchical / meta-controlled multi-agent design (a meta-policy orchestrating heterogeneous agents), and is an applied example of using behavioral diversity for cross-regime robustness. It does not engage the robust-MDP, minimax, or distributionally robust lines, so it is best cited as an application-domain instance of risk-aware multi-agent RL.

## Related Work (verbatim excerpts from the paper)
> _[Section: Related Work — opening paragraph]_

"Recent research in quantitative finance reveals a significant methodological evolution from supervised prediction to end-to-end Reinforcement Learning (RL). This shift is motivated by the “prediction-profitability gap,” where higher prediction accuracy does not reliably translate to better trading returns (Jiang, Zhu, and Hu 2024), and by RL’s inherent suitability for sequential decision-making. Researchers are applying increasingly sophisticated RL paradigms to tackle financial challenges like market non-stationarity and low signal-to-noise ratios (Liu et al. 2022; Wang et al. 2025), leading to a diverse ecosystem of approaches. Concurrently, the development of standardized benchmarks like FinRL-Meta (Liu et al. 2022) and TradeMaster (Sun et al. 2023) signifies a community-wide push for greater scientific rigor."

> _[Section: Related Work — "Model-Free Approaches"]_

"Model-free RL approaches learn trading policies directly from market interaction without an explicit market model. Recent advancements focus on augmenting standard RL agents with domain-specific architectures. For instance, DeepTrader is a risk-aware agent using a dual-module architecture to balance return with risk by embedding market conditions and penalizing high portfolio drawdown, allowing it to adapt its strategy to different market regimes (Wang et al. 2021b). Addressing a different challenge, Logic-Q is a knowledge-guided system that injects human-like trading logic into a DRL agent via program sketching. This helps the agent identify major market trends and prevent catastrophic errors during trend shifts, thereby improving robustness (Li et al. 2025)."

> _[Section: Related Work — "Model-Based and Hybrid Approaches"]_

"Model-based and hybrid approaches integrate predictive components to provide the RL agent with a richer understanding of the market, aiming to improve sample efficiency. A prime example is StockFormer, which fuses a predictive coding module with an RL agent, using specialized Transformer branches to learn latent representations of future dynamics for a Soft Actor-Critic (SAC) agent (Gao, Wang, and Yang 2023). This end-to-end system tackles the low signal-to-noise problem by extracting predictive signals, though its performance can be contingent on the accuracy of the underlying predictive model. Other hybrid methods, like “Ambiguous” Mean-Variance RL, fuse RL with classical financial theory, using RL to learn unknown statistical parameters required by traditional risk models (Huang and Li 2020)."

> _[Section: Related Work — "Hierarchical and Multi-Agent RL Approaches"]_

"Hierarchical and Multi-Agent RL approaches decompose complex financial problems into more manageable sub-tasks. Hierarchical Reinforcement Learning (HRL) is particularly effective for multi-scale decision-making. For example, HRPM uses a two-level hierarchy where a high-level agent sets strategic portfolio allocations and a low-level agent minimizes trade execution costs, directly addressing frictions like slippage (Wang et al. 2021a). EarnHFT applies a more complex three-tier hierarchy to high-frequency trading, using a meta-controller to dynamically select the best-specialized agent for current market conditions (Qin et al. 2024). Separately, Multi-Agent RL (MARL) models strategic interactions. The MAPS framework, for instance, uses cooperative agents with a diversification penalty to encourage varied strategies, creating a more robust “portfolio of portfolios” (Lee et al. 2020). These approaches acknowledge that a single agent may be insufficient to capture multifaceted market dynamics."

### Cited references (resolved from the paper's bibliography)
- **(Jiang, Zhu, and Hu 2024)** Jiang, Zhu, Hu. *Benchmarking Machine Learning Methods for Stock Prediction.* Under review at ICLR 2025.
- **(Liu et al. 2022)** Liu, Xia, Rui, Gao, Yang, Zhu, Wang, Wang, Guo. *FinRL-Meta: Market Environments and Benchmarks for Data-Driven Financial Reinforcement Learning.* NeurIPS 2022.
- **(Wang et al. 2025)** Wang, Kong, Guo, Hua, Qi, Zhou, Zheng, Wang, Ni, Guo. *QuantBench: Benchmarking AI Methods for Quantitative Investment.* arXiv preprint arXiv:2504.18600, 2025.
- **(Sun et al. 2023)** Sun, Qin, Zhang, Xia, Zong, Ying, Xie, Zhao, Wang, An. *TradeMaster: A Holistic Quantitative Trading Platform Empowered by Reinforcement Learning.* NeurIPS 2023.
- **(Wang et al. 2021b)** Wang, Huang, Tu, Zhang, Xu. *DeepTrader: A Deep Reinforcement Learning Approach for Risk-Return Balanced Portfolio Management with Market Conditions Embedding.* AAAI 2021 (vol. 35), 643–650.
- **(Li et al. 2025)** Li, Jiang, Cao, Cui, Wu, Li, Liu, Sun. *Logic-Q: Improving Deep Reinforcement Learning-based Quantitative Trading via Program Sketch-based Tuning.* AAAI 2025 (vol. 39), 18584–18592.
- **(Gao, Wang, and Yang 2023)** Gao, Wang, Yang. *StockFormer: Learning Hybrid Trading Machines with Predictive Coding.* IJCAI 2023, 4766–4774.
- **(Huang and Li 2020)** Huang, Li. *A Two-level Reinforcement Learning Algorithm for Ambiguous Mean-variance Portfolio Selection Problem.* IJCAI 2020, 4527–4533.
- **(Wang et al. 2021a)** Wang, Wei, An, Feng, Yao. *Commission Fee is not Enough: A Hierarchical Reinforced Framework for Portfolio Management.* AAAI 2021 (vol. 35), 626–633.
- **(Qin et al. 2024)** Qin, Sun, Zhang, Xia, Wang, An. *EarnHFT: Efficient Hierarchical Reinforcement Learning for High Frequency Trading.* AAAI 2024 (vol. 38), 14669–14676.
- **(Lee et al. 2020)** Lee, Kim, Yi, Kang. *MAPS: Multi-Agent Reinforcement Learning-based Portfolio Management System.* IJCAI 2020, 4520–4526.
