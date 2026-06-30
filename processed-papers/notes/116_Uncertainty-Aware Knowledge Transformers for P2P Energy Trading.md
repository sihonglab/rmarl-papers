# 116. Uncertainty-Aware Knowledge Transformers for Peer-to-Peer Energy Trading with Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Uncertainty-Aware Knowledge Transformers for Peer-to-Peer Energy Trading with Multi-Agent Reinforcement Learning
- **作者**: Mian Ibad Ali Shah, Enda Barrett, Karl Mason
- **机构**: School of Computer Science, University of Galway, Ireland
- **发表**: ECAI 2025（European Conference on Artificial Intelligence, Main Track）
- **链接/arXiv**: arXiv:2507.16796v1 [cs.AI]（2025-07-22）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境/预测不确定性（renewable 发电与负荷的随机性，aleatoric/heteroscedastic uncertainty）
- **方法范式**: 不确定性感知预测（probabilistic transformer）+ MARL（DQN）、风险敏感决策；偏实证
- **关键词**: P2P Energy Trading, Probabilistic Forecasting, Transformer, Uncertainty Quantification, MARL, DQN, Double Auction

## TL;DR（一句话总结）
提出 Knowledge Transformer with Uncertainty (KTU) 的异方差概率预测模型，把负荷/PV 预测的不确定性显式注入多智能体 DQN 的状态与奖励，实现对随机 P2P 能源交易环境的风险敏感、鲁棒决策，显著降低购电成本与峰时电网需求。

## 问题与动机 (Problem & Motivation)
P2P 能源交易中可再生发电与负荷高度随机，传统确定性预测无法刻画未来情景全貌，导致次优或高风险的交易/调度决策。现有 MARL P2P 工作多依赖确定性预测，或有概率预测但未与多智能体学习结合。需要将不确定性量化整合进 MARL，以提升交易系统的适应性与鲁棒性（尤其在高可再生渗透与碳约束下）。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自可再生发电与负荷的随机波动，由 KTU 输出每个预测的均值 µ 与方差 σ²（Gaussian，Softplus）显式量化（aleatoric uncertainty），并构造置信区间。非对抗设定。
- **设定**: competitive / mixed（10 个自利 prosumer agent，独立训练最大化自身效用，去中心化竞争）；centralized auctioneer 做市场清算（仅共享发电/负荷/价格数据，保隐私）；online 仿真训练

## 方法 (Method)
- KTU：基于 transformer encoder（multi-head self-attention、可学习位置编码）的异方差概率预测，双输出头预测 µ 与 σ²，PV 均值受 daylight/季节物理约束调制；复合损失 = 高斯负对数似然 + 时间平滑正则 + 夜间 PV 惩罚。
- 将预测的均值与不确定性 (FL, FG, UL, UG) 连同当前负荷/发电/电池状态构成状态向量，输入每个 agent 的 DQN 策略选择离散动作（buy/sell/charge/discharge/self-consume 等）。
- 奖励函数显式纳入预测置信度 αi、tariff 时段、电池约束（SoC），鼓励峰前预充电、峰时少依赖电网。
- 市场用 double auction（DA）机制清算，按 Supply-Demand Ratio (SDR) 计算内部买/卖价 (IBP/ISP)；Optuna 自动超参优化。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（作者明言收敛性理论保证为未来工作）。

## 实验 (Experiments)
- **环境/Benchmark**: 10 个芬兰乡村 prosumer（4 奶牛场 + 6 家庭，2 家有 EV），各配 PV+电池；PettingZoo 框架，约 2M timesteps 仿真。
- **Baselines**: Rule-Based、RB+QL（ensemble）、标准 DQN（无预测）、DQN Forecasting（本文）；另评估 PPO 等。
- **评估指标**: 购电成本、售电收入、峰时电网需求；预测质量用 PICP、MPIW、CRPS；收敛速度、电池 SoC 行为。

## 主要结果 (Key Results)
- 不确定性感知 DQN 相对标准 DQN：购电成本降低约 5.7%（无 P2P）/3.2%（有 P2P）；售电收入提升 6.4%（无 P2P）/44.7%（有 P2P）；峰时电网需求下降 38.8%（无 P2P）/45.6%（有 P2P）。
- 收敛速度约快 50%、所需 timesteps 减少约 25%（概率预测缩小探索空间）。
- 电池管理更具前瞻性：峰前预充电、峰时放电，优于 reactive 的标准 DQN 与规则方法；P2P 交易是降本/降峰/增收的最大单一因素，DQN 优于 PPO。

## 局限与未来工作 (Limitations & Future Work)
缺乏收敛性理论保证；仅 10 agent 小社区仿真、无真实部署。未来：纳入更多市场机制、真实试点、优化预测时域、给出收敛性理论分析。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中“环境/预测不确定性 + 不确定性感知（risk-aware）决策”一线，区别于对抗/minimax 路线：通过显式不确定性量化（probabilistic forecasting）将风险信息融入状态与奖励来获得鲁棒性。是 robust MARL 在能源市场（P2P trading）应用、且竞争性多智能体设定的实证案例。
