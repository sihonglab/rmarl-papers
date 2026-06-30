# 116. Uncertainty-Aware Knowledge Transformers for Peer-to-Peer Energy Trading with Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Uncertainty-Aware Knowledge Transformers for Peer-to-Peer Energy Trading with Multi-Agent Reinforcement Learning
- **Authors**: Mian Ibad Ali Shah, Enda Barrett, Karl Mason
- **Affiliation**: School of Computer Science, University of Galway, Ireland
- **Venue**: ECAI 2025 (European Conference on Artificial Intelligence, Main Track)
- **Link/arXiv**: arXiv:2507.16796v1 [cs.AI], 22 Jul 2025

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty (stochastic renewable generation and dynamic load); aleatoric prediction uncertainty in forecasts; risk-sensitive decision-making under variability. (Not adversarial; "robustness" is empirical resilience of trading decisions to forecast/renewable uncertainty.)
- **Method paradigm**: Uncertainty-aware probabilistic forecasting (heteroscedastic transformer) combined with multi-agent reinforcement learning (independent DQN); double-auction market mechanism; uncertainty quantification injected into state and reward.
- **Keywords**: P2P energy trading, MARL, DQN, probabilistic transformer forecasting, uncertainty quantification, carbon trading

## TL;DR
The paper proposes a framework that couples a heteroscedastic probabilistic transformer (Knowledge Transformer with Uncertainty, KTU) with a multi-agent DQN system so that energy-trading agents make risk-sensitive decisions using forecast uncertainty, yielding faster convergence, lower purchase costs, higher sales revenue, and reduced peak-hour grid demand in a simulated P2P prosumer community.

## Problem & Motivation
P2P energy markets face inherent uncertainty from variable solar/wind generation and stochastic consumer demand, which undermines economic efficiency and reliability if not properly managed. Traditional deterministic forecasting cannot capture the full spectrum of future scenarios, leading to suboptimal or risk-prone trading and dispatch decisions. Most prior MARL-for-P2P implementations rely on deterministic forecasts and do not integrate uncertainty quantification with multi-agent learning. The paper aims to fill this gap by explicitly quantifying prediction uncertainty and propagating it into the MARL trading framework, while also incorporating carbon accounting as peak-tariff management.

## Robustness Setting
- **Threat model / uncertainty set**: Uncertainty is modeled probabilistically (not adversarially). The KTU predicts a mean μ and variance σ² (Gaussian) for both prosumer load and PV generation, capturing aleatoric uncertainty. These uncertainty estimates are included in each agent's state vector and influence the reward function (via a confidence score αᵗⁱ). No explicit adversary or worst-case uncertainty set is defined.
- **Setting**: Competitive / decentralized P2P trading; 10 self-interested prosumer agents trained independently (no explicit coordination, communication-free) via DQN; centralized auctioneer for market clearing; online simulation over 2 million timesteps in PettingZoo.

## Method
- **Probabilistic forecasting (KTU)**: A transformer encoder with learnable positional encodings and multi-head self-attention produces dual output heads predicting mean μ and variance σ² (Softplus activation) for load L and PV generation P, giving Gaussian probabilistic forecasts at horizon t+k. PV mean is modulated by physics-informed daylight/seasonality constraints.
- **Custom loss**: A composite loss combining Gaussian negative log-likelihood with a temporal-smoothness regularization term (α) and a penalty (β) for physically impossible nighttime PV generation; hyperparameters tuned via Optuna. Forecast quality assessed with PICP, MPIW, and CRPS.
- **MARL trading (DQN)**: Each agent's state vector includes current and forecasted load/generation, battery state, and forecast uncertainty estimates [Li,t, Gi,t, Bi,t, FLi,t, FGi,t, UL,i,t, UG,i,t]. Discrete actions cover buy, sell, charge, discharge, self-consumption (and combinations). DQN approximates Q-values via a neural network updated by TD error with a periodically updated target network.
- **Uncertainty-aware rewards**: Per-action reward functions incorporate the confidence score αᵗⁱ, tariff periods (N/NP/P/D), state-of-charge, and peak-deficit prediction, encouraging anticipatory charging before peak hours and risk-informed trading.
- **Market mechanism**: A double-auction (DA) clears the market each timestep; Internal Selling Price (ISP) and Internal Buying Price (IBP) are set by the Supply and Demand Ratio (SDR) method; buyers and sellers are matched by price priority before resorting to grid transactions.

## Theoretical Contributions
None / mostly empirical. The authors explicitly note that theoretical analysis or guarantees regarding convergence properties are left to future work.

## Experiments
- **Environment/Benchmark**: Simulated P2P energy trading community of 10 rural Finnish prosumers (4 dairy farms with data from Uski et al.; 6 households with synthetic Finnish-profile loads, 2 owning EVs), each with PV and battery; PV simulated with SAM (NREL); renewable capacity set to 40% of annual load; PettingZoo framework; 2 million timesteps.
- **Baselines**: Rule-Based, RB+QL (rule-based + Q-learning ensemble), standard DQN, and DQN with uncertainty-aware Forecasting (proposed); PPO was also evaluated. Scenarios with and without P2P trading.
- **Evaluation metrics**: Electricity purchase cost (€), electricity sales revenue (€), peak-hour grid demand (kW), reward convergence/training efficiency; forecast metrics PICP, MPIW, CRPS.

## Key Results
- Uncertainty-aware DQN reduces energy purchase costs by ~5.7% without P2P (€105,000 → €99,100) and 3.2% with P2P (€102,100 → €96,800) vs standard DQN.
- Electricity sales revenue increases 6.4% without P2P (€7,850 → €8,350) and 44.7% with P2P (€14,450 → €20,900).
- Peak-hour grid demand falls 38.8% without P2P (23,200 kW → 14,200 kW) and 45.6% with P2P (21,850 kW → 11,900 kW).
- The uncertainty-aware forecasting DQN converges ~50% faster (about 25% fewer timesteps) than standard DQN; improvements are more pronounced with P2P trading enabled, and DQN consistently outperformed PPO.

## Limitations & Future Work
- No theoretical convergence guarantees are provided (acknowledged as future work).
- Evaluation is simulation-based on a small 10-prosumer community; scaling to larger populations is argued for but not demonstrated (future work mentions distributed/federated learning).
- Uncertainty is treated probabilistically (aleatoric) rather than via adversarial/worst-case robustness.
- Future work: integrate additional market mechanisms, real-world pilot deployments, optimize the forecasting horizon, and develop theoretical convergence analysis.

## Relevance to Survey
This paper sits on the periphery of robust MARL: it addresses robustness in the sense of resilience and risk-sensitive decision-making under environment/model uncertainty (stochastic renewables and demand), achieved by injecting probabilistic forecast uncertainty into a decentralized multi-agent DQN system. It connects the "uncertainty quantification / risk-aware MARL" theme to an applied energy-systems domain, and to the literature on robust optimization and uncertainty-aware forecasting for P2P trading. It is not a theoretical robust-MARL contribution (no minimax/DRMG/adversary), but exemplifies how uncertainty-awareness is used to enhance robustness of cooperative-competitive multi-agent systems in practice.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work]_

"P2P energy trading in microgrids has emerged as a decentralized approach to sustainable energy distribution, facing challenges in scalability, privacy, pricing, and uncertainty. Zhou et al. demonstrated that early community market mechanisms apply uniform prices, limiting individualized incentives [41]. While Zheng et al. introduced auction-based methods for trader-specific pricing [38], these approaches struggle with real-world uncertainties in trader behavior and energy supply."

"May et al. presented MARL as a promising solution, showing how agents can learn optimal strategies in dynamic environments [19]. Bhavana et al. identified persistent technical challenges regarding scalability and uncertainty management [3], while Bassey et al. investigated AI applications in trading strategy optimization [2]. However, most implementations rely on deterministic forecasts, inadequately capturing the inherent variability in renewable systems. Zhang et al. demonstrated that forecasting errors significantly impact market efficiency [37], highlighting the need for uncertainty-aware forecasting models."

"In transformer architectures, Liu et al. have shown promising results in energy forecasting [17], but the approach primarily addresses single-agent settings or deterministic outputs. Chen et al. developed a DQN-based approach for price prediction [5], though without uncertainty quantification. El et al. investigated uncertainty-aware prosumer coalitional games [9], but did not integrate probabilistic forecasting with multi-agent learning."

"Recent work by Yazdani et al. proposed robust optimization for real-time trading [36], while Uthayansuthi et al. combined clustering, forecasting, and deep reinforcement learning [32]. However, these approaches either lack advanced neural forecasting integration or focus primarily on economic optimization without considering uncertainty impact."

> _[Introduction — motivation on uncertainty and robustness]_

"Complex and dispersed, modern real-world systems have many parts, nonlinear processes, and uncertain environments ([7]). A central challenge in the operation of P2P energy markets is the inherent uncertainty associated with renewable generation and dynamic load profiles. The variability of solar and wind resources, as well as the stochastic nature of consumer demand, introduce significant risks that can undermine both economic efficiency and system reliability if not properly managed [12] [13]. Traditional deterministic forecasting approaches are insufficient in this context, as they fail to capture the full spectrum of possible future scenarios, leading to suboptimal or risk-prone trading and dispatch decisions."

"To address these challenges, recent research has emphasized the importance of robust and uncertainty-aware forecasting methods. Probabilistic forecasting, which provides not only point estimates but also confidence intervals or probability distributions, enables market participants to make risk-informed decisions and supports the design of resilient trading mechanisms [12]. Furthermore, the integration of uncertainty quantification into multi-agent optimization and reinforcement learning frameworks has been shown to enhance the adaptability and robustness of P2P trading systems, particularly in the presence of high renewable penetration and carbon constraints [28]."

### Cited references (resolved from the paper's bibliography)
- **[2]** K. E. Bassey, S. A. Rajput, K. Oyewale. *Peer-to-peer energy trading: Innovations, regulatory challenges, and the future of decentralized energy systems.* World Journal of Advanced Research and Reviews, 2024.
- **[3]** G. Bhavana, R. Anand, J. Ramprabhakar, V. Meena, V. K. Jadoun, F. Benedetto. *Applications of blockchain technology in peer-to-peer energy markets and green hydrogen supply chains: a topical review.* Scientific Reports, 2024.
- **[5]** T. Chen, S. Bu. *Realistic peer-to-peer energy trading model for microgrids using deep reinforcement learning.* IEEE PES ISGT-Europe 2019.
- **[7]** A. Dorri, S. S. Kanhere, R. Jurdak. *Multi-agent systems: A survey.* IEEE Access, 2018.
- **[9]** G. El Rahi, S. R. Etesami, W. Saad, N. B. Mandayam, H. V. Poor. *Managing price uncertainty in prosumer-centric energy trading: A prospect-theoretic Stackelberg game approach.* IEEE Transactions on Smart Grid, 2017.
- **[12]** Z. Guo, P. Pinson, S. Chen, Q. Yang, Z. Yang. *Chance-constrained peer-to-peer joint energy and reserve market considering renewable generation uncertainty.* IEEE Transactions on Smart Grid, 2020.
- **[13]** Z. Hu, Y. Xu, M. Korkali, X. Chen, L. Mili, J. Valinejad. *A Bayesian approach for estimating uncertainty in stochastic economic dispatch considering wind power penetration.* IEEE Transactions on Sustainable Energy, 2020.
- **[17]** Y. Liu, T. Hu, H. Zhang, H. Wu, S. Wang, L. Ma, M. Long. *iTransformer: Inverted transformers are effective for time series forecasting.* arXiv preprint arXiv:2310.06625, 2023.
- **[19]** R. May, P. Huang. *A multi-agent reinforcement learning approach for investigating and optimising peer-to-peer prosumer energy markets.* Applied Energy, 2023.
- **[28]** M. Song, C. Gao, M. Yan, Y. Yao, T. Chen. *Robust peer-to-peer multi-energy trading considering carbon emission.* In Local Energy Markets: Paving the Path Toward the Low-Carbon Digital Power Distribution System, Springer, 2025.
- **[32]** N. Uthayansuthi, P. Vateekul. *Optimization of peer-to-peer energy trading with a model-based deep reinforcement learning in a non-sharing information scenario.* IEEE Access, 2024.
- **[36]** H. Yazdani, M. Doostizadeh, F. Aminifar. *Forecast-aided power and flexibility trading of prosumers in peer to peer markets.* IET Renewable Power Generation, 2023.
- **[37]** B. Zhang, G. He, Y. Du, H. Wen, X. Huan, B. Xing, J. Huang. *Assessment of the economic impact of forecasting errors in peer-to-peer energy trading.* Applied Energy, 2024.
- **[38]** J. Zheng, Z.-T. Liang, Y. Li, Z. Li, Q.-H. Wu. *Multi-agent reinforcement learning with privacy preservation for continuous double auction-based p2p energy trading.* IEEE Transactions on Industrial Informatics, 2024.
- **[41]** Y. Zhou, J. Wu, C. Long. *Evaluation of peer-to-peer energy sharing mechanisms based on a multiagent simulation framework.* Applied Energy, 2018.
