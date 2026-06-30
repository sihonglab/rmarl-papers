# 69. Towards Robust Multi-UAV Collaboration: MARL with Noise-Resilient Communication and Attention Mechanisms

## 元信息 (Metadata)
- **标题**: Towards Robust Multi-UAV Collaboration: MARL with Noise-Resilient Communication and Attention Mechanisms
- **作者**: Zilin Zhao, Chishui Chen, Haotian Shi, Jiale Chen, Xuanlin Yue, Zhejian Yang, Yang Liu（后两位通讯）
- **机构**: Jilin University（吉林大学，多学院）；China University of Mining and Technology
- **发表**: IROS 2025（arXiv:2503.02913v1，2025年3月；补充材料 github iros25-supp）
- **链接/arXiv**: arXiv:2503.02913 ；https://github.com/zilin-zhao/iros25-supp

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信噪声 / 传感器数据噪声（距离相关乘性衰减 + 加性高斯白噪声）
- **方法范式**: MARL (COMA, CTDE)、denoising autoencoder、attention（CBAM + 空间/通道注意力融合）、信息论 IPP
- **关键词**: multi-UAV, informative path planning (IPP), noise-resilient communication, sensor fusion/denoising, attention, COMA

## TL;DR（一句话总结）
针对噪声环境下多无人机协同信息采集（informative path planning），提出基于 COMA 的 MARL 框架，核心是 SenDFuse 多传感器去噪融合网络（denoising autoencoder + 注意力融合）与 CBAM 注意力 Actor-Critic，显著提升噪声通信下的协同鲁棒性与决策能力。

## 问题与动机 (Problem & Motivation)
多无人机在 3D 空间协同执行 informative path planning (IPP) 可提升信息采集效率，但噪声环境下的鲁棒通信与协同决策仍是难题。传统非自适应/自适应 IPP 方法分别存在路径固定或评估候选路径耗时指数增长的问题；GNN-IPP 依赖专家示范的监督模仿学习。现有 MARL-IPP 工作（如 Westheider 首次将其引入 full-3D）聚焦 credit assignment，但无人针对多无人机通信协议设计，尤其在传感器融合与通信噪声条件下，也未将复合注意力机制整合进框架。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 通信/传感噪声建模为 Ir(x,y)=α(x,y)I(x,y)+n(x,y)，α 为距离相关衰减因子、n~N(0,σ²) 高斯白噪声。moderate noise: α~U(0.8,1), σ=0.02；loud noise: α~U(0.6,1), σ=0.06。本地 UAV(UAV0) 自身数据不受噪声影响，仅接收的其他 UAV 数据含噪。非对抗性环境噪声。
- **设定**: cooperative；CTDE（COMA 集中训练、分散执行）；online（含离线预训练 SenDFuse + 部署）

## 方法 (Method)
- **问题建模**: full-3D 多 UAV 协同导航/IPP，目标最大化信息增益（belief map 的 Shannon 熵减少），受通信/采样预算 B 约束。状态=全局 belief map+各 UAV 位置+预算；动作=6 个坐标轴方向；奖励=地图熵的相对减少。
- **SenDFuse Network**: 扩展 NestFusion，从"同模不同模态融合"扩展到"同模态不同视角的 n 路融合"。采用 denoising autoencoder 范式：训练时禁用融合、向输入加人工噪声并回归到无噪图像（loss = MSE+MAE+SSIM 组合）；部署时启用基于通道注意力 C(Φ) 与空间注意力 S(Φ) 加权和的融合策略 F(Φ)=αC(Φ)+βS(Φ)。
- **Actor-Critic + CBAM**: 所有 UAV 共享 Actor，输入为 8 通道 11×11 子图（剩余预算/ID/高度/足迹/本地传感/本地 belief/本地熵/去噪融合图），采用 CBAM（通道+空间注意力）；Critic 额外含 4 维全局信息（全局 belief/全局熵/全局足迹/所有 UAV 动作）。
- **训练**: COMA 用反事实基线计算每个 agent 的 advantage 进行 credit assignment，Critic 用 TD(λ) 估计回报。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（采用信息论 IPP 目标与 COMA 反事实基线，但无新收敛/鲁棒理论分析）。

## 实验 (Experiments)
- **环境/Benchmark**: 三类环境——Env1 合成星形数据、Env2 热成像(HIT-UAV 数据集)、Env3 可见光(吉林大学地质宫航拍)；4 架 UAV，通信预算 b=15，1200 episodes
- **Baselines**: AG (Adaptive Gain 自适应 IPP)、NL (Non-adaptive Lawnmower)、Random；消融：Base(无 SenDFuse 无 CBAM)、仅 Fusion、仅 CBAM、两者皆有
- **评估指标**: F1-Score（像素价值二分类）、全局 belief map 的 Shannon 熵（越低越好）；no/moderate/loud 三种噪声水平；10 次试验均值±标准差

## 主要结果 (Key Results)
- 同时含 SenDFuse + CBAM 的完整模型收敛速度与最终收敛值最佳；噪声越大，两模块的重要性越明显。
- Fusion 模块单独优于 CBAM 单独，但 CBAM 也能在 RL 过程中学到一定去噪/融合能力，优于 naive 基线。
- 较 AG/NL/Random 基线在 F1 与熵指标上取得最佳性能与稳定性，宣称在噪声环境下熵减少提升约 78%。
- 噪声增大时各方法方差增大（不稳定），Fusion 模块能一定程度缓解。

## 局限与未来工作 (Limitations & Future Work)
论文未设独立局限/未来工作章节。可推断局限：仅在小规模（4 UAV）与有限环境验证；本地 UAV 数据假设无噪；噪声为非对抗性高斯模型，未考虑对抗攻击或丢包；SenDFuse 需离线预训练数据；无理论保证。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 的"通信/感知噪声鲁棒性 + 应用（多 UAV）"主题线，强调用 denoising autoencoder 与注意力机制在表征层抵御传感/通信噪声（区别于对抗通信攻击防御与认证鲁棒）。可与其他通信鲁棒（TMC #66、噪声信道 #71）及 UAV 应用类 robust MARL 工作对照，是面向真实 IPP 部署的工程化噪声鲁棒方案。
