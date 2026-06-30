# 117. Combating Uncertainties in Smart Grid Decision Networks: Multiagent Reinforcement Learning With Imperfect State Information

## Metadata
- **Title**: Combating Uncertainties in Smart Grid Decision Networks: Multiagent Reinforcement Learning With Imperfect State Information
- **Authors**: Arman Ghasemi, Amin Shojaeighadikolaei, Morteza Hashemi
- **Affiliation**: University of Kansas, Lawrence, KS, USA (Department / Graduate School of Electrical Engineering and Computer Science)
- **Venue**: IEEE Internet of Things Journal, Vol. 11, No. 13, 1 July 2024
- **Link/arXiv**: DOI 10.1109/JIOT.2024.3389653

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/state uncertainty in a smart-grid setting — imperfect and uncertain state information from renewable energy sources (wind generation uncertainty, PV generation uncertainty), locational marginal price (LMP) uncertainty, dynamic retail price fluctuation, and demand-side uncertainty. Robustness here means coping with these uncertainties (via forecasting + partial observability), not adversarial perturbation in the classic robust-MARL sense.
- **Method paradigm**: Multiagent deep RL (DDPG actor-critic) combined with LSTM time-series forecasting; two-level (bi-level) optimization; decentralized agents with partial observability; uncertainty handled by forecasting and price-history observation rather than minimax/worst-case.
- **Keywords**: Distributed energy management, reinforcement learning (RL), renewable energy uncertainty, wind power forecasting, DDPG, LSTM

## TL;DR
The paper proposes an integrated LSTM-DDPG multiagent framework for smart-grid energy management under uncertain and imperfect state information, where an LSTM forecasts day-ahead wind generation to feed a load-serving-entity DDPG agent and prosumer DDPG agents jointly optimize wholesale and retail market decisions, improving LSE profit (e.g., by 86% versus a time-of-use baseline) and reducing the peak-to-average ratio.

## Problem & Motivation
Large-scale integration of renewable energy sources (wind, solar/PV) into smart grids introduces generation, demand, and price uncertainties that challenge both electricity providers (LSEs) and prosumers. The load serving entity must (1) manage RES-induced uncertainty in both wholesale and retail markets and (2) economically distribute energy among distributed participants (residential PV units with storage). Prior work has handled these issues mostly with single-agent RL focused at the end-user level, used DL forecasting or RL decision making in isolation, and largely ignored the wholesale market and the coupling between wholesale and retail uncertainties. The authors argue that no prior work jointly investigates wind uncertainty with dynamic energy management using deep RL in a unified framework that links the wholesale and retail markets.

## Robustness Setting
- **Threat model / uncertainty set**: Uncertainty is modeled non-adversarially as (1) wind power generation uncertainty (environmental factors), (2) LMP uncertainty in day-ahead (DA) and real-time (RT) markets, (3) dynamic retail prices, and (4) demand-side uncertainty from prosumers. Each agent observes only a subset of environment states (S = SPA ∪ SLSA), i.e., imperfect/partial state information. The LSA does not know RT wind data and relies on an LSTM 24-h forecast; the PA cannot see future prices and instead observes the past N steps of electricity price to infer trends. A baseline ±10% uncertainty range around the previous 24-h generation is used when no forecasting engine is available.
- **Setting**: Mixed cooperative/competitive multiagent energy market (LSE agent vs. prosumer agents across a two-level optimization); decentralized agents each learning their own policy with local partial observations; online, model-free off-policy DDPG training (4000 episodes).

## Method
- Formulate a two-level optimization: an upper LSE level that maximizes profit by setting electricity buy/sell prices subject to generation, ramp-rate, and power-balance constraints, and a lower user level where prosumers minimize their electricity bills via battery charge/discharge actions.
- Train an LSTM forecasting engine (stacked, 100 neurons, tanh, Adam, sliding window T = 96 over 24 h to forecast h = 96 steps) on historical wind data (wind speed, direction, temperature, power) to predict next-24-h DA wind generation; performance measured by RMSE and MAPE.
- Deploy two types of DDPG agents: a load serving agent (LSA) at the LSE level whose action is the sell/buy price (Cs_t, Cb_t) and whose reward is LSE profit, and prosumer agents (PAs) whose action is battery charge/discharge b_i,t and whose reward is the negative billing cost. Each DDPG uses actor/critic plus target networks, replay buffer, Bellman critic update (eq. 16), deterministic policy gradient (eq. 17), gradient descent/ascent updates, and soft target updates with τ ≪ 1.
- Integrate the two phases (Algorithm 1): first train LSTM and generate DA predictions; then train the LSA (which observes the LSTM wind forecast plus past-M DA/RT LMPs and demand) and PAs (which observe consumption, PV, state of charge, and past price window), so forecasting reduces the DA–RT LMP mismatch and improves decision making under uncertainty. State normalization and batch normalization are used to stabilize training.

## Theoretical Contributions
None / mostly empirical. The paper relies on standard DDPG formulations (Bellman equation, deterministic policy gradient) and a two-level optimization formulation; no new convergence, sample-complexity, or equilibrium-existence results are proven.

## Experiments
- **Environment/Benchmark**: Modified IEEE five-bus system; two gas-turbine generators (G1 base, G2 reserve) with quadratic cost curves, a WPP at bus A, an LSE serving buses B/C/D, and a network of five prosumers on bus D. Real wind data from a 14 MW wind farm in Zhangye, China (Kaggle, Jan 2018–Mar 2020); load/PV curves mimicking California ISO patterns. Implemented in Python with PyTorch 1.12.1; 4000 episodes, 24-h cycles, 15-min sampling.
- **Baselines**: Case 1 — no forecasting engine, LSA uses a ±10% uncertainty range around the past 24-h real data (as in [12]); pricing-scheme comparisons including a fixed price and two time-of-use (TOU) waveforms (Kansas/Evergy and California/SCE).
- **Evaluation metrics**: Forecasting accuracy (RMSE, MAPE); LSE profit; prosumer electricity bills; peak-to-average ratio (PAR); episodic accumulative return; battery arbitrage behavior.

## Key Results
- The LSTM achieves RMSE = 1.235 and ~8% MAPE for DA wind power forecasting, within the acceptable range for 24-h wind prediction.
- LSA and PA agents learn stable near-optimal policies within roughly the first 2000 episodes.
- Integrating the LSTM forecast with DDPG (Case 2) lets the LSA better anticipate RT/DA LMPs, dynamically adjust prices, incentivize prosumers to use full battery capacity, lower electricity bills, and reduce PAR versus the uncertainty-range baseline (Case 1).
- The proposed dynamic pricing framework increases LSE profit by 86% compared with a TOU pricing scenario and yields higher profit and smaller PAR than fixed and TOU schemes (Table II).

## Limitations & Future Work
- Evaluation is limited to a single modified IEEE five-bus system with five prosumers and one wind farm dataset; scalability to larger networks is not assessed.
- The framework assumes buy and sell prices are equal (Cb_t = Cs_t, net-metering) and forgoes transmission-system limits; LMP calculation details are omitted for exposition.
- "Robustness" is addressed via forecasting and partial-observation heuristics rather than formal worst-case/adversarial guarantees.
- Future work: extend the framework to include other electricity-market factors such as the LSE's bidding strategies and the associated uncertainties.

## Relevance to Survey
This is an application-driven smart-grid paper rather than a core robust-MARL theory paper, but it is relevant to the survey's "state/observation uncertainty" and "partial observability / imperfect state information" themes in multi-agent settings. It explicitly motivates its work by citing core robust-RL and robust-MARL literature (robust DRL against state-observation perturbations, robust RL as a constrained game, robust MARL with state uncertainty, adversarial regularization, mutual-information regularization), positioning the smart-grid uncertainty problem alongside those lines. It illustrates how the MARL state-uncertainty challenge — where one agent's decision under uncertain state affects others' returns — arises in a real cyber-physical system, and connects the forecasting-plus-RL methodology to robustness against environmental/exogenous uncertainty.

## Related Work (verbatim excerpts from the paper)
> _[Section II.A, Related Work — "Combating Uncertainties With Forecasting"]_

"Besides the research works that are focused on uncertainties in smart grid systems, there is a multitude of related works that are focused on investigating the impacts of uncertainties in the general RL frameworks [9], [10]. Dealing with state uncertainty becomes even more challenging in the context of MARL, as the decisions of an agent with uncertain state information affect not only its own returns but also those of other agents [11], [36], [37]. However, these solutions are not specifically designed to address uncertainties in smart grid decision-making scenarios. Given the distinct nature of uncertainties in smart grid networks and complex market structures (i.e., wholesale and retail markets, with DA and RT pricing), actions taken with uncertain state information in the wholesale market impact the decisions made by the retail market agents, and vice versa. In this article, we investigate the uncertainties in the wholesale and retail markets and the associated impacts on distributed energy management."

> _[Section I, Introduction — prior-work overview]_

"Over the past few years, extensive research have focused on addressing these challenges, covering topics like predicting RES generation, optimizing energy distribution, and addressing uncertainties in demand response and energy management. To address uncertainties, two primary research approaches have gained prominence: deep learning (DL) forecasting [3], [4], [5], [6], [7] and reinforcement learning (RL) for decision making [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22]. From a wholesale market perspective, researchers have explored DL and RL techniques to tackle uncertainties like LMP prediction and bidding strategies [3], [4], [8]. On the other hand, in the retail market, RL and DL are extensively utilized to address uncertainties in solving demand response and energy management problems [6], [7], [13], [14]. Notably, some recent studies have employed a combined approach integrating RL-based decision making and DL-based forecasting frameworks [23], [24], [25], [26], [27], [28], [29], [30], [31], [32]. However, these works primarily focused on addressing price and PV uncertainties solely at the end-user level, utilizing a single-agent RL framework, without considering the wholesale market. To the best of our knowledge, no prior work has investigated the impacts of uncertainty with dynamic energy management utilizing deep RL (DRL) techniques."

### Cited references (resolved from the paper's bibliography)
- **[9]** H. Zhang et al. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS (34th Adv. Neural Inf. Process. Syst.) 2020.
- **[10]** J. Yu, C. Gehring, F. Schäfer, A. Anandkumar. *Robust reinforcement learning: A constrained game-theoretic approach.* Learning for Dynamics and Control (L4DC) 2021.
- **[11]** S. He, S. Han, S. Su, S. Han, S. Zou, F. Miao. *Robust multi-agent reinforcement learning with state uncertainty.* Transactions on Machine Learning Research (TMLR) 2023.
- **[36]** A. Bukharin et al. *Robust multi-agent reinforcement learning via adversarial regularization: Theoretical foundation and stable algorithms.* arXiv:2310.10810, 2023.
- **[37]** S. Li et al. *MIR2: Towards provably robust multi-agent reinforcement learning by mutual information regularization.* arXiv:2310.09833, 2023.
- **[3]** Z. Zhao, Y. Liu, L. Guo, L. Bai, Z. Wang, C. Wang. *Distribution locational marginal pricing under uncertainty considering coordination of distribution and wholesale markets.* IEEE Trans. Smart Grid 2023.
- **[4]** Z. Zhang, M. Wu. *Predicting real-time locational marginal prices: A GAN-based approach.* IEEE Trans. Power Syst. 2022.
- **[5]** M. Xia, H. Shao, X. Ma, C. W. De Silva. *A stacked GRU-RNN-based approach for predicting renewable energy and electricity load for smart grid operation.* IEEE Trans. Ind. Informat. 2021.
- **[6]** W. Kong, Z. Y. Dong, Y. Jia, D. J. Hill, Y. Xu, Y. Zhang. *Short-term residential load forecasting based on LSTM recurrent neural network.* IEEE Trans. Smart Grid 2019.
- **[7]** H. Jahangir, H. Tayarani, S. S. Gougheri, M. A. Golkar, A. Ahmadian, A. Elkamel. *Deep learning-based forecasting approach in smart grids with microclustering and bidirectional LSTM network.* IEEE Trans. Ind. Electron. 2021.
- **[8]** X. Gao, K. W. Chan, S. Xia, X. Zhang, K. Zhang, J. Zhou. *A multiagent competitive bidding strategy in a pool-based electricity market with price-maker participants of WPPs and EV aggregators.* IEEE Trans. Ind. Informat. 2021.
- **[12]** V.-H. Bui, A. Hussain, H.-M. Kim. *Double deep Q-learning-based distributed operation of battery energy storage system considering uncertainties.* IEEE Trans. Smart Grid 2020.
- **[13]** H. Li, Z. Wan, H. He. *Real-time residential demand response.* IEEE Trans. Smart Grid 2020.
- **[14]** E. Samadi, A. Badri, R. Ebrahimpour. *Decentralized multi-agent based energy management of microgrid using reinforcement learning.* Int. J. Elect. Power Energy Syst. 2020.
- **[15]** H. Xiao, X. Pu, W. Pei, L. Ma, T. Ma. *A novel energy management method for networked multi-energy microgrids based on improved DQN.* IEEE Trans. Smart Grid 2023.
- **[16]** J. Qi, L. Lei, K. Zheng, S. X. Yang, X. Shen. *Optimal scheduling in IoT-driven smart isolated microgrids based on deep reinforcement learning.* IEEE Internet Things J. 2023.
- **[17]** C. Guo, X. Wang, Y. Zheng, F. Zhang. *Real-time optimal energy management of microgrid with uncertainties based on deep reinforcement learning.* Energy 2022.
- **[18]** Y. Liang, C. Guo, Z. Ding, H. Hua. *Agent-based modeling in electricity market using deep deterministic policy gradient algorithm.* IEEE Trans. Power Syst. 2020.
- **[19]** E. Foruzan, L.-K. Soh, S. Asgarpoor. *Reinforcement learning approach for optimal distributed energy management in a microgrid.* IEEE Trans. Power Syst. 2018.
- **[20]** A. Dolatabadi, H. Abdeltawab, Y. A.-R. I. Mohamed. *A novel model-free deep reinforcement learning framework for energy management of a PV integrated energy hub.* IEEE Trans. Power Syst. 2023.
- **[21]** L. Lei, Y. Tan, G. Dahlenburg, W. Xiang, K. Zheng. *Dynamic energy dispatch based on deep reinforcement learning in IoT-driven smart isolated microgrids.* IEEE Internet Things J. 2021.
- **[22]** Z. Zhu, K. W. Chan, S. Xia, S. Bu. *Optimal bi-level bidding and dispatching strategy between active distribution network and virtual alliances using distributed robust multi-agent deep reinforcement learning.* IEEE Trans. Smart Grid 2022.
- **[23]** A. A. Amer, K. Shaban, A. M. Massoud. *DRL-HEMS: Deep reinforcement learning agent for demand response in home energy management systems considering customers and operators perspectives.* IEEE Trans. Smart Grid 2023.
- **[24]** R. Lu, S. H. Hong, M. Yu. *Demand response for home energy management using reinforcement learning and artificial neural network.* IEEE Trans. Smart Grid 2019.
- **[25]** L. Xiong et al. *A two-level energy management strategy for multi-microgrid systems with interval prediction and reinforcement learning.* IEEE Trans. Circuits Syst. I, Reg. Papers 2022.
- **[26]** X. Xu, Y. Jia, Y. Xu, Z. Xu, S. Chai, C. S. Lai. *A multi-agent reinforcement learning-based data-driven method for home energy management.* IEEE Trans. Smart Grid 2020.
- **[27]** J. Cao, D. Harrold, Z. Fan, T. Morstyn, D. Healey, K. Li. *Deep reinforcement learning-based energy storage arbitrage with accurate lithium-ion battery degradation model.* IEEE Trans. Smart Grid 2020.
- **[28]** Z. Wan, H. Li, H. He, D. Prokhorov. *Model-free real-time EV charging scheduling based on deep reinforcement learning.* IEEE Trans. Smart Grid 2019.
- **[29]** F. Zhang, Q. Yang, D. An. *CDDPG: A deep-reinforcement-learning-based approach for electric vehicle charging control.* IEEE Internet Things J. 2021.
- **[30]** L. Xiong et al. *Meta-reinforcement learning-based transferable scheduling strategy for energy management.* IEEE Trans. Circuits Syst. I, Reg. Papers 2023.
- **[31]** Y. Ye, H. Wang, P. Chen, Y. Tang, G. Strbac. *Safe deep reinforcement learning for microgrid energy management in distribution networks with leveraged spatial–temporal perception.* IEEE Trans. Smart Grid 2023.
- **[32]** D. A. Khan, A. Arshad, M. Lehtonen, K. Mahmoud. *Combined DR pricing and voltage control using reinforcement learning based multi-agents and load forecasting.* IEEE Access 2022.
