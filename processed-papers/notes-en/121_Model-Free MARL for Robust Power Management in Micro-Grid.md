# 121. A Model-Free Multi-Agent Reinforcement Learning Approach to Reach a Robust, Optimal, and Environment-Friendly Power Management in a Micro-Grid

## Metadata
- **Title**: A Model-Free Multi-Agent Reinforcement Learning Approach to Reach a Robust, Optimal, and Environment-Friendly Power Management in a Micro-Grid
- **Authors**: M. Nasir Uddin (Fellow, IEEE), Yazdan H. Tabrizi
- **Affiliation**: Dept. of Electrical Engineering, Lakehead University, LU-GC program, Barrie, ON, Canada
- **Venue**: 2023 IEEE Industry Applications Society Annual Meeting (IAS), 2023 (DOI: 10.1109/IAS54024.2023.10406423)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Renewable-resource and load uncertainty in micro-grid energy management (uncertainty/variability in wind and solar generation and demand). "Robust" is used informally to mean a reliable, economical, environment-friendly power-management system; no formal adversarial / distributional / model-uncertainty robustness setting is defined.
- **Method paradigm**: Data-driven forecasting (multi-layer recurrent neural network) + model-free value-based MARL (stochastic game, Q-learning); not an adversarial/minimax robust-MARL formulation.
- **Keywords**: Power management, multi-layer recurrent neural network, renewable resources power prediction, multi-agent reinforcement learning, energy storage

## TL;DR
The paper proposes a two-stage data-driven scheme for micro-grid power management — a grid-search-tuned multi-layer recurrent neural network (MLRNN) to forecast 24-hour wind/PV output, feeding a model-free multi-agent Q-learning controller that dispatches CCHP, renewables, and battery storage to minimize a combined fuel + CO2-emission cost function.

## Problem & Motivation
Micro-grids (MGs) integrating distributed/renewable energy resources need an energy management strategy (EMS) that balances supply and demand while minimizing cost and CO2 emissions. Classical model-based EMS approaches (quadratic/mixed-integer programming, PSO, genetic algorithms, MDP-based, stochastic optimization, MPC, gravitational/bee-colony search, fuzzy/ANFIS, ANN-BPSO) suffer from heavy computation, dependence on day-ahead forecast accuracy, slow or non-guaranteed convergence, parameter-tuning difficulty, and limited applicability to complex real-world constraints. The authors argue data-driven AI approaches (RNN forecasting + model-free RL) are a more appealing substitute, and that single-agent RL becomes less effective as MG power-management systems grow, motivating a multi-agent solution that decomposes the hard optimization into simpler per-agent tasks.

## Robustness Setting
- **Threat model / uncertainty set**: No formal uncertainty set or adversary is defined. The uncertainty addressed is the natural unpredictability/variability of renewable wind and solar generation and of loads; it is handled by accurate day-ahead MLRNN forecasting rather than by a worst-case or distributionally robust formulation. "Robust" denotes a dependable, economical, environment-friendly MG operation.
- **Setting**: Cooperative multi-agent (four agents jointly minimizing one MG cost function); model-free, value-based MARL (Q-learning) over a stochastic game; online decision-making over a 24-hour dispatch horizon. Centralized/decentralized training-execution split is not specified.

## Method
- **Forecasting stage (MLRNN)**: A multi-layer recurrent neural network with tanh activations and backpropagation-through-time predicts 24-hour WT and PV output power. Inputs are historical wind/solar features (Northern California weather data from NREL's System Advisor Model, SAM); data are standardized (z-score scaling) and the network is trained with mini-batch stochastic gradient descent (MGD). Performance is measured by normalized RMSE (nRMSE).
- **Hyperparameter tuning**: Number of hidden layers and MGD step size are auto-tuned by grid-search (domains [1, 8] layers and [10^-3, 10] step size), using 10% of samples as a validation set, instead of Bayesian/trial-and-error tuning.
- **Problem formulation**: MG operation is cast as constrained optimization with supply/demand balance equations and a total cost function CF_total = CF1 (natural-gas fuel cost of MT and boiler) + CF2 (CO2 emission cost), subject to capacity/SoC/charge-discharge constraints for CCHP units, micro-turbine, PV, WT, and BESS.
- **MARL stage**: The dispatch is modeled as a stochastic game with N agents sharing the state space; agents maximize discounted cumulative reward (discount factor 0.9). State includes BESS SoC, MT/WT/PV output power, and time of day h(t); action space has three states: idle (0), increase/charge (1), decrease/discharge (2). A value-based Q-learning update is used, where each agent's evaluation accounts for itself and all other agents' interests (an "eval/Solve" operator yields each agent's policy). Four agents are used in the experiments.

## Theoretical Contributions
None / mostly empirical. No convergence, sample-complexity, equilibrium-existence, or certified-robustness results are provided.

## Experiments
- **Environment/Benchmark**: Simulated micro-grid (Fig. 1) with CCHP (micro-turbine, absorption chiller, gas boiler, heat recovery), PV, WT, and BESS; CCHP/BESS parameters in Tables I–II; Northern California NREL SAM weather data for forecasting; 24-hour electrical/heating/cooling load profiles.
- **Baselines**: For forecasting, comparison is qualitative ("over previously researched methods"). For power management, a tabular comparison (TABLE VI) of prior RL-based strategies — Q-Learning [24], Bayesian-RL [25], DQN [26], Actor-critic RL [27], Transfer RL [28] — against the proposed MARL, summarizing strengths/deficiencies (not head-to-head numeric results).
- **Evaluation metrics**: Forecasting test accuracy (and nRMSE); dispatch correctness (generation-unit output power over 24 h, BESS charge/discharge behavior); total operating cost (fuel + CO2 emission).

## Key Results
- MLRNN test accuracy: 96.06% for WT and 98.32% for PV output-power prediction; optimal hyperparameters were 4 hidden layers / step size 0.03 (WT) and 3 layers / step size 0.48 (PV).
- The MARL controller dispatched MT mainly to serve heating/cooling demand (operating at its 10 kW minimum, i.e., 10% of rated capacity, in low-demand hours), while WT and PV ran near maximum capacity in high-demand periods.
- Total cost of the obtained power management was about $241; BESS discharged to the load (max 6 kW step) when generation could not meet electrical demand and recharged at the earliest opportunity, validating proper operation under both light and heavy load conditions.

## Limitations & Future Work
- The proposed MARL's noted deficiencies (TABLE VI) are communication overhead and challenging training.
- "Robustness" is asserted qualitatively (economical, environment-friendly operation) rather than demonstrated against any defined perturbation, adversary, or uncertainty set; no stress-test under forecast errors or worst-case conditions is reported.
- No quantitative comparison against the listed RL baselines on the same MG; results are from a single simulated case. Future-work directions are not explicitly stated in the text.

## Relevance to Survey
This is an application paper on micro-grid energy management; it uses "robust" colloquially to mean reliable/economical operation and adopts a cooperative model-free multi-agent Q-learning controller fed by RNN forecasts. It does not address robust MARL in the formal sense (no adversarial training, robust MDP/Markov game, distributional robustness, or perturbation/uncertainty-set guarantees). Its relevance to a Robust MARL survey is peripheral: it illustrates MARL applied to an uncertain, renewable-driven energy domain and how forecasting is used to cope with renewable variability, but it is not a methodological contribution to robustness. Useful mainly as an applications/energy-systems data point rather than a core robust-MARL reference.

## Related Work (verbatim excerpts from the paper)
The paper has no dedicated Related Work section and no discussion of robust MARL, robust RL / robust MDP, adversarial RL, or distributionally robust RL. The Introduction reviews prior energy-management-strategy (EMS) methods; the most relevant verbatim passages (covering MDP-, stochastic-optimization-, MPC-, and AI-based EMS approaches, i.e., the closest "prior work" content) are quoted below.

> _[Introduction]_

"In MGs, EMS is frequently described as a nonlinear optimization issue. Numerous approaches, such as quadratic and mixed integer programming, particle swarm optimization, and genetic algorithm [5]-[7], have been suggested in the studies to tackle the EMS problems with different objective functions. Nevertheless, since the renewable energy sources and loads are unpredictable in real world problems, the mentioned methods rely on the day-ahead forecast's accuracy, and this has a negative impact on how the system operates with these algorithms, in real time [8]."

> _[Introduction]_

"Depending on the Markov decision process (MDP), alternative types of EMS are available. An MDP includes a number of states, a sequence of operations, and reward functions. Though, in a practical case, the operator can just select the appropriate day type rather than assessing the generated power and load for the day, which could lead to a substandard solution. Reference [9], derived a near-optimal EMS for an MG, using a finite MDP-based supplemented by deep neural network learning. The approach, meanwhile, required a lot of calculation because the state space was large."

> _[Introduction]_

"The stochastic optimization (SO) based EMS is an option, as well. A finite collection of alternative situations is used by SO to explore the search area and makes decisions derived from empirical average of such possibilities. To reduce the real-time electricity cost, a SO-based EMS strategy for stand-alone grids was reported in [10]. With the same objective function, a real-time SO for EMS in domestic system contains WT, PV, and energy storage systems was suggested in [11]. But inherently, the SO is an iterative problem-solving approach. The iterative technique has two drawbacks: first, its convergence cannot always be assured, and secondly, implementation in real-world situations may not always be feasible [12]."

> _[Introduction]_

"Model predictive control (MPC) is another comprehensive approach that makes it through an explicit concept to forecast how the structure will respond in the upcoming and adapt the control plan over time. MPC has a proven track record of offering real-time solutions for multi-variable operations that are delayed and chaotic [13]. To reduce operating costs and carbon dioxide emission, an MPC-based EMS in an MG was provided in [14]. According to [15], an island MG was considered to analyze MPC-based, in order to lessen the negative consequences of unforeseen renewable energy units' outputs. Conversely, MPC suffers from sophisticated calculation, high maintenance cost and lack of flexibility."

> _[Introduction]_

"Each of the techniques discussed above falls under the category of model-based solutions, in which the resources and the consumers are reflected by mathematical formulas. This will lead to a computationally expensive solution. The power management improvement is being treated by gravitational search algorithm [16], and artificial bee colony search algorithm [17] to highlight important mentioned issues. Although, for the highest fitness fulfillment, these algorithms have complicated parameter calculations, restrictions, coding challenges, and formulations. Furthermore, the adaptive neuro-fuzzy inference system and fuzzy-logic controller still have drawbacks in power management problems, according to the literature [18]. In order to achieve consistent resolution forecasts and controller refinement, artificial neural network (ANN) based optimization approaches are a useful choice in this regard. Consequently, to get around the limitations of the aforementioned techniques, an ANN based binary particle swarm optimization controller was suggested in [19]. However, the method was a relatively complex approach, and the number of hyperparameters which should be precisely tuned increased."

### Cited references (resolved from the paper's bibliography)
- **[5]** C. Cecati, C. Citro, P. Siano. *Combined Operations of Renewable Energy Systems and Responsive Demand in a Smart Grid.* IEEE Transactions on Sustainable Energy, 2011.
- **[6]** S. A. Pourmousavi, M. H. Nehrir, C. M. Colson, C. Wang. *Real-Time Energy Management of a Stand-Alone Hybrid Wind-Microturbine Energy System Using Particle Swarm Optimization.* IEEE Transactions on Sustainable Energy, 2010.
- **[7]** P. Siano, C. Cecati, H. Yu, J. Kolbusz. *Real Time Operation of Smart Grids via FCN Networks and Optimal Power Flow.* IEEE Transactions on Industrial Informatics, 2012.
- **[8]** G. Mohy-ud-din, K. M. Muttaqi, D. Sutanto. *Adaptive and Predictive Energy Management Strategy for Real-Time Optimal Power Dispatch From VPPs Integrated With Renewable Energy and Energy Storage.* IEEE Transactions on Industry Applications, 2021.
- **[9]** P. Zeng, H. Li, H. He, S. Li. *Dynamic Energy Management of a Microgrid Using Approximate Dynamic Programming and Deep Recurrent Neural Network Learning.* IEEE Transactions on Smart Grid, 2019.
- **[10]** C. Liu, C. Lee, H. Chen, S. Mehrotra. *Stochastic Robust Mathematical Programming Model for Power System Optimization.* IEEE Transactions on Power Systems, 2016.
- **[11]** F. Hafiz, M. A. Awal, A. R. d. Queiroz, I. Husain. *Real-Time Stochastic Optimization of Energy Storage Management Using Deep Learning-Based Forecasts for Residential PV Applications.* IEEE Transactions on Industry Applications, 2020.
- **[12]** Y. Du, F. Li. *Intelligent Multi-Microgrid Energy Management Based on Deep Neural Network and Model-Free Reinforcement Learning.* IEEE Transactions on Smart Grid, 2020.
- **[13]** Y. Zheng, S. Li, R. Tan. *Distributed Model Predictive Control for On-Connected Microgrid Power Management.* IEEE Transactions on Control Systems Technology, 2018.
- **[14]** F. Delfino, G. Ferro, M. Robba, M. Rossi. *An Energy Management Platform for the Optimal Control of Active and Reactive Powers in Sustainable Microgrids.* IEEE Transactions on Industry Applications, 2019.
- **[15]** Z. Zhao et al. *Distributed Robust Model Predictive Control-Based Energy Management Strategy for Islanded Multi-Microgrids Considering Uncertainty.* IEEE Transactions on Smart Grid, 2022.
- **[16]** M. Marzband, M. Ghadimi, A. Sumper, J. L. Domínguez-García. *Experimental validation of a real-time energy management system using multi-period gravitational search algorithm for microgrids.* Applied Energy, 2014.
- **[17]** K. Roy, K. K. Mandal, A. C. Mandal. *Modeling and managing of micro grid connected system using improved artificial bee colony algorithm.* International Journal of Electrical Power & Energy Systems, 2016.
- **[18]** T. Sadeq, M. Rezkallah, A. Chandra, Z. Feger, H. Ibrahim, J.-F. Savard. *Real-Time Power Management Strategy based on Fuzzy Logic Controller and Human-Computer Interface for DC Off-Grid System.* IEEE Industry Applications Society Annual Meeting, 2020.
- **[19]** M. G. M. Abdolrasol, R. Mohamed, M. A. Hannan, A. Q. Al-Shetwi, M. Mansor, F. Blaabjerg. *Artificial Neural Network Based Particle Swarm Optimization for Microgrid Optimal Energy Scheduling.* IEEE Transactions on Power Electronics, 2021.
