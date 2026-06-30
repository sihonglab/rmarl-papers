# Missing Candidates vs. Master List (`robust-marl-papers.xlsx`)

Checks whether the robust-MARL papers flagged as *missing from the 133 processed set* are nonetheless **already tracked in the 146-row master spreadsheet**. (The spreadsheet has 13 entries not yet processed into `processed-papers/`.)

- Candidates checked: **55**
- Already in the spreadsheet: **2**
- Possibly already in (conference/journal variant — verify): **1**
- Genuinely absent (true gaps): **52**

Full table: `data/missing_vs_xlsx.csv`. Match = token-set / token-sort fuzzy similarity on normalised titles; borderline rows were verified by hand.

## ✅ Already in the master list (no action needed)

| Cites | Candidate (from references) | → Master row | Processed? | sim (set/sort) |
|------:|------------------------------|--------------|-----------|----------------|
| 5 | Resilience enhancement of multi-agent reinforcement learning | No.119 — Resilience Enhancement of MARL Demand Resp | **not yet** | 93.8/72.6 |
| 2 | X., Chen, H., Wang, C., Xing, Y., Yang, J., Philip, S. Y., C | No.23 — Robust MARL via Bayesian Distributional Va | **not yet** | 95.3/55.0 |

## ⚠️ Possibly already in — verify (likely conference vs. journal version of a listed paper)

| Cites | Candidate (from references) | Closest master row | Processed? | sim (set/sort) |
|------:|------------------------------|--------------------|-----------|----------------|
| 2 | Learning effi- cient and robust multi-agent communication vi | No.64 — Robust MA Communication with Graph Infor | yes | 92.5/72.6 |

## ❌ Genuinely absent — true coverage gaps (52 works)

Not in the processed set **and** not in the spreadsheet. Ranked by how many of our papers cite them.

| Cites | Candidate work | Year | Cited by | Closest master row (sim) |
|------:|----------------|------|----------|----------------------|
| 10 | ROMAX: Certifiably robust deep multiagent reinforcement learning via convex relaxation · arXiv:2109.06795 | 2022 | #10, #16, #28, #29, #31, #46, #65, #73, #79, #97 | No.61 (60.8/56.6) |
| 9 | Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication · arXiv:2012.00508 | 2020 | #60, #61, #63, #64, #65, #67, #68, #80, #96 | No.67 (70.8/53.6) |
| 8 | Decentralized robust v-learning for solving markov games with model un- certainty | 2023 | #2, #3, #4, #5, #6, #8, #9, #93 | No.1 (66.7/58.8) |
| 7 | Adversarial Attacks On Multi-Agent Communication · arXiv:2101.06560 | 2021 | #44, #45, #50, #61, #63, #65, #68 | No.47 (73.3/69.8) |
| 7 | Learning and testing resilience in cooperative multi- agent systems | 2020 | #16, #29, #31, #41, #73, #74, #97 | No.97 (67.7/64.6) |
| 5 | Safe and robust multi-agent reinforcement learning for connected autonomous vehicles under state perturbations · arXiv:2309.11057 | 2023 | #2, #5, #44, #51, #94 | No.114 (69.7/54.8) |
| 5 | Attacking cooperative multi-agent reinforcement learning by adversarial minority influence · arXiv:2302.03322 | 2023 | #31, #51, #97, #98, #103 | No.52 (63.9/60.4) |
| 5 | A robust and constrained multi-agent reinforcement learning electric vehicle rebalancing method in amod systems · arXiv:2209.08230 | 2022 | #18, #28, #31, #44, #137 | No.26 (58.1/48.6) |
| 5 | Evaluating robustness of cooperative marl: A model-based approach · arXiv:2202.03558 | 2022 | #32, #33, #49, #62, #98 | No.59 (89.6/62.5) |
| 3 | Efficient adversarial attacks on online multi-agent reinforcement learning · arXiv:2307.07670 | 2023 | #47, #48, #103 | No.47 (73.3/60.2) |
| 3 | One4all: Manipulate one agent to poison the cooperative multi-agent reinforcement learning | 2023 | #48, #76, #103 | No.131 (60.5/53.6) |
| 3 | J., Artiglio, G., and Xie, Q. Roping in uncer- tainty: Robustness and regularization in markov games | 2024 | #9, #11, #12 | No.30 (55.6/52.8) |
| 2 | Robust co- operative multi-agent reinforcement learning via multi-view message certification | 2024 | #44, #67 | No.65 (83.5/64.9) |
| 2 | Sok: Adversarial machine learning attacks and defences in multi-agent reinforcement learning · arXiv:2301.04299 | 2023 | #52, #103 | No.47 (66.7/56.0) |
| 2 | Adversarial machine learning attacks and defences in multi-agent reinforcement learning | 2025 | #50, #67 | No.47 (66.7/56.2) |
| 2 | Adversarial attacks in consensus-based multi-agent reinforce- ment learning | 2021 | #78, #103 | No.47 (66.7/57.4) |
| 1 | Marnet: Backdoor attacks against cooperative multi-agent reinforcement learning | 2022 | #103 | No.131 (60.5/56.7) |
| 1 | Communication-efficient and resilient distributed deep reinforcement learning for multi-agent systems | 2024 | #78 | No.67 (78.3/55.3) |
| 1 | Security analysis of poisoning attacks against multi-agent reinforcement learning | 2021 | #103 | No.54 (59.6/51.9) |
| 1 | Robustness evaluation of multi-agent reinforcement learning algorithms using gnas | 2023 | #103 | No.15 (61.9/56.9) |
| 1 | Adversarial attacks on multi-agent communication | 2021 | #64 | No.47 (73.3/69.8) |
| 1 | Safe multi-agent reinforcement learning for wireless applications against adversarial communications | 2024 | #67 | No.61 (60.1/58.9) |
| 1 | Towards resilience for multi-agent qd-learning | 2021 | #78 | No.78 (59.8/57.7) |
| 1 | Attacking cooperative multi-agent reinforcement learning by adversarial minority influence | 2025 | #49 | No.52 (63.9/60.4) |
| 1 | The emergence of ad- versarial communication in multi-agent reinforcement learn- ing | 2020 | #60 | No.4 (55.6/53.9) |
| 1 | Adversarial attacks on multi-agent com- munication | 1992 | #60 | No.47 (73.3/69.0) |
| 1 | Communication-robust multi-agent learning by adaptable auxiliary multi-agent adversary generation | 2024 | #67 | No.61 (67.6/62.5) |
| 1 | Resilient multiagent reinforcement learning with function approxi- mation | 2024 | #78 | No.7 (60.6/59.1) |
| 1 | Toward resilient multi-agent actor-critic algorithms for distributed reinforcement learning | 2020 | #78 | No.78 (74.1/56.3) |
| 1 | Robust reward-free actor-critic for cooperative multiagent reinforcement learning | 2024 | #78 | No.131 (68.1/56.7) |
| 1 | Robust lane change decision for autonomous vehicles in mixed traffic: A safety-aware multi-agent adversarial reinforcement learning approach | 2022 | #53 | No.58 (73.3/48.5) |
| 1 | Robust multi-agent Q-learning in cooperative games with adversaries | 2021 | #31 | No.74 (74.0/66.1) |
| 1 | An overview on multi-agent consensus under adversarial attacks | 2019 | #60 | No.47 (73.3/59.5) |
| 1 | Adversarial Ma- chine Learning Attacks and Defences in Multi-Agent Rein- forcement Learning | 2018 | #145 | No.47 (66.7/59.0) |
| 1 | Less is more: Robust robot learning via partially observable multi-agent reinforcement learning · arXiv:2309.1479 | 2023 | #51 | No.40 (60.0/57.7) |
| 1 | Adaptive fault-tolerant tracking control for discrete-time multiagent systems via reinforcement learning algorithm | 2021 | #135 | No.76 (56.6/50.9) |
| 1 | Byzantine- resilient multiagent distributed optimization under redundancy | 2025 | #78 | No.78 (75.6/65.0) |
| 1 | Distributed resilience-aware control in multi-robot networks | 2025 | #78 | No.134 (63.9/60.5) |
| 1 | Towards a fault-tolerant multi-agent system architecture | 2000 | #77 | No.77 (62.1/57.5) |
| 1 | Distributed robust optimization for multi-agent systems with guaranteed finite-time convergence · arXiv:2309.01201 | 2023 | #126 | No.26 (58.1/53.4) |
| 1 | N., Shah, A., Carroll, M., Seshia, S., Russell, S. J., and Dennis, M. Robust and diverse multi-agent learning via rational policy gradient | 2026 | #13 | No.131 (63.6/54.4) |
| 1 | Adaptive frequency and delay compen- sation in multi-agent systems: Enhancing communication efficiency and robustness | 2024 | #67 | No.67 (64.5/50.6) |
| 1 | A survey on fault tolerant multi agent system | 2016 | #77 | No.35 (55.2/51.9) |
| 1 | On the hard- ness of decentralized multi-agent policy evaluation under byzantine attacks | 2024 | #78 | No.15 (60.9/55.9) |
| 1 | Adversarial policy gradient for alternating markov games | 2014 | #43 | No.58 (60.2/60.2) |
| 1 | Large-scale mean-field federated learning for detection and defense: A byzantine robustness approach in IoT | 2024 | #142 | No.75 (58.5/53.6) |
| 1 | Fault-tolerant consensus of leader-following multi-agent systems with jointly connected topologies | 2023 | #77 | No.4 (48.8/47.6) |
| 1 | Byzantine-resilient multiagent optimization | 2021 | #78 | No.78 (61.3/57.4) |
| 1 | Learn- ing markov games with adversarial opponents: Effi- cient algorithms and fundamental limits · arXiv:2203.06803 | 2022 | #20 | No.14 (55.0/53.4) |
| 1 | Fault-tolerant cooperative control of multiagent systems: A survey of trends and methodologies | 2020 | #77 | No.59 (54.9/49.7) |
| 1 | Data poisoning to fake a nash equilibria for markov games | 2024 | #3 | No.8 (53.3/50.0) |
| 1 | Resilient dis- tributed optimization for multiagent cyberphysical systems | 2025 | #78 | No.145 (52.3/52.3) |