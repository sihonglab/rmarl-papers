# 117. Combating Uncertainties in Smart Grid Decision Networks: Multiagent Reinforcement Learning With Imperfect State Information

## 元信息 (Metadata)
- **标题**: Combating Uncertainties in Smart Grid Decision Networks: Multiagent Reinforcement Learning With Imperfect State Information
- **作者**: Arman Ghasemi, Amin Shojaeighadikolaei, Morteza Hashemi（前两位同等贡献）
- **机构**: University of Kansas（EECS）
- **发表**: IEEE Internet of Things Journal, Vol. 11, No. 13, 1 July 2024（DOI: 10.1109/JIOT.2024.3389653）
- **链接/arXiv**: 未明确（IEEE Xplore）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境/可再生能源不确定性（风电生成、LMP 价格、需求侧/PV 不确定性）、imperfect/uncertain state information
- **方法范式**: 时间序列预测（LSTM）+ MARL（DDPG）、两层优化、weather-aware；偏实证
- **关键词**: Distributed Energy Management, Reinforcement Learning, Renewable Energy Uncertainty, Wind Power Forecasting, LSTM, DDPG

## TL;DR（一句话总结）
提出 LSTM-DDPG 统一框架，用 LSTM 时序预测应对风电生成不确定性、用多智能体 DDPG 在不完美/不确定状态信息下做分布式能源管理决策，同时建模批发与零售市场，提升 LSE 与 prosumer 的经济收益并降低峰均比（PAR）。

## 问题与动机 (Problem & Motivation)
风光等可再生能源大规模并网带来发电、需求与电价的多重不确定性。批发市场风电不确定性导致 DA/RT LMP 不确定，影响零售市场（反之亦然）。已有工作多只在终端用户层、用单智能体 RL 处理价格/PV 不确定性，不考虑批发市场；预测与决策很少联合；且很少同时在批发（风电）与零售（分布式 PV）联合建模可再生不确定性。需要一个统一框架联合处理风电不确定性、LMP 不确定性、动态零售价与需求侧不确定性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非对抗。不确定性来自风电生成（环境因素）、LMP 价格、PV 生成与用户行为；agent 面对 imperfect/uncertain state information（无 RT 真值，仅历史数据 + LSTM 预测）。基线对照用 ±10% 风电不确定区间。
- **设定**: cooperative/mixed（LSE agent 与多个 prosumer agent，两层优化）；distributed decision-making；online（DDPG 训练）

## 方法 (Method)
- 建模为两层优化：LSE 在 DA/RT 批发市场参与并动态定零售价；prosumer 控制电池充放电以最小化电费。
- LSTM 时序预测引擎：滑动窗口（24h，15min 间隔，T=96）预测未来 24h（h=96）DA 风电生成，缓解风电不确定性。
- DDPG RL agents（连续动作）：LSE agent（LSA）动作为售电价格；prosumer agent（PA）动作为电池充放电，观察过去 20 步电价应对价格不确定性。
- weather-aware 机制：将 DA 标记为 {Cloudy, Sunny} 提前观测，调整 PA 决策，实现 battery arbitrage（低谷充、高峰放/卖）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。

## 实验 (Experiments)
- **环境/Benchmark**: IEEE 五总线系统模型；真实风电场数据集；LSTM（stacked，100 神经元，tanh，Adam lr=0.001，batch 64，100 epochs）。
- **Baselines**: 无预测、用 ±10% 不确定区间的方法；TOU 定价（Kansas、California 两种波形）、固定价格场景。
- **评估指标**: LSE 利润、prosumer 电费、峰均比（PAR）；LSTM 预测的 RMSE/MAPE；episodic return 收敛。

## 主要结果 (Key Results)
- LSTM 风电预测 RMSE=1.235、MAPE≈8%（24h 窗口可接受范围）；LSA/PA agent 约 2000 episode 收敛到稳定策略。
- 相比 TOU 定价，所提动态定价框架将 LSE 利润提升约 86%；同时降低 PAR。
- 集成预测引擎（Case 2）相比仅用不确定区间（Case 1）能让 LSA 更准估 DA/RT LMP、动态调价，促 prosumer 在峰时支撑电网，进而降低 PAR、prosumer 用满电池容量降电费。
- 风电模式日间变化越大，DA/RT LMP 失配越大，凸显预测对决策的重要性。

## 局限与未来工作 (Limitations & Future Work)
未考虑 LSE 竞价（bidding）策略及其不确定性；规模仅五总线系统。未来拟纳入 LSE 竞价策略等更多电力市场因素及其不确定性。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中“环境/可再生不确定性 + imperfect state information”一线的电力系统应用，采用预测（LSTM forecasting）而非对抗/minimax 来获得对不确定性的鲁棒决策。论文相关工作明确引用了 robust RL against state perturbations（Zhang et al. 2020）、constrained game-theoretic robust RL、robust MARL with state uncertainty（He et al. 2023）等鲁棒 MARL 主线，是“以不确定性建模/预测提升鲁棒性”的代表案例。
