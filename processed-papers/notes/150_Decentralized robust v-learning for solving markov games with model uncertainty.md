# 150. Decentralized Robust V-learning for Solving Markov Games with Model Uncertainty

## 元信息 (Metadata)
- **标题**: Decentralized Robust V-learning for Solving Markov Games with Model Uncertainty
- **作者**: Shaocong Ma, Ziyi Chen, Shaofeng Zou, Yi Zhou
- **机构**: University of Utah；Cornell University；University at Buffalo (SUNY)
- **发表**: Journal of Machine Learning Research (JMLR) 24, 2023
- **链接/arXiv**: jmlr.org/papers/v24/23-0310.html

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境/模型不确定性（state transition kernel uncertainty）
- **方法范式**: 鲁棒马尔可夫博弈理论、robust correlated equilibrium、全分散随机算法 (V-learning)
- **关键词**: robust Markov games, model uncertainty, robust correlated equilibrium, decentralized, sample complexity

## TL;DR（一句话总结）
首次为带环境模型不确定性的 Markov game 提出可解的新解概念 **robust correlated equilibrium (robust CE)**，证明其相对非鲁棒 CE 具有简单的修正结构且依赖不确定性水平，并给出首个全分散随机算法计算近似 robust CE，附多项式 episode 复杂度 Õ(SA²H⁵ε⁻²)。

## 问题与动机 (Problem & Motivation)
多数 Markov game 工作只计算给定模型下的某种均衡，忽略实际中普遍存在的环境模型不确定性（训练/测试环境失配）。把模型不确定性纳入博弈解概念既能提升部署鲁棒性，又带来"如何定义可解且可分散计算的鲁棒均衡"的挑战。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 环境转移模型落在不确定性集内，求最坏情况下的均衡（distributionally/robust）
- **设定**: competitive（general Markov game，多玩家）；fully decentralized；有限步 (finite-horizon) 理论设定

## 方法 (Method)
- 定义 robust correlated equilibrium：在模型不确定性下每个玩家对其鲁棒（最坏情况）收益无单方偏离动机
- 证明 robust CE 相对普通 CE 只需"简单修正结构"，其均衡刻画关键依赖不确定性水平
- 设计首个 **fully-decentralized stochastic algorithm**（robust V-learning 式）计算近似 robust CE，玩家仅用本地信息

## 理论贡献 (Theoretical Contributions)
- 提出 robust CE 解概念并给出其存在性/结构刻画
- 全分散算法的收敛与 episode 复杂度 Õ(SA²H⁵ε⁻²) 上界（达近似 robust CE，精度 ε）

## 实验 (Experiments)
- **环境/Benchmark**: 偏理论；以小规模 Markov game 数值验证为主
- **Baselines**: 非鲁棒 CE / 标准 V-learning
- **评估指标**: 收敛性、模型扰动下的鲁棒收益、复杂度验证

## 主要结果 (Key Results)
- robust CE 在模型扰动下保持均衡性质，且可由分散算法多项式样本高效计算
- 均衡的修正量随不确定性水平显式变化，给出可解释的"鲁棒性—保守性"关系

## 局限与未来工作 (Limitations & Future Work)
理论以 tabular、有限步、特定不确定性集为主；向函数逼近/大状态空间与在线探索扩展仍待研究。

## 与综述的关联 (Relevance to Survey)
属 §1 DRMG/理论主线的去中心化均衡计算分支，被本语料 8× 引用；与 [[2_Sample-Efficient Robust MARL in Face of Environmental Uncertainty]]、[[3_Breaking the Curse of Multiagency in Robust MARL]] 等鲁棒 Markov game 理论互为补充（correlated equilibrium 视角 + 全分散算法）。
