# 70. DCT-MARL: A Dynamic Communication Topology Based MARL Algorithm for Platoon Control

## 元信息 (Metadata)
- **标题**: DCT-MARL: A Dynamic Communication Topology Based MARL Algorithm for Platoon Control
- **作者**: Yaqi Xu, Yan Shi, Jin Tian, Fanzeng Xia, Tongxin Li, Shanzhi Chen, Yuming Ge
- **机构**: Beijing University of Posts and Telecommunications (BUPT)；Chinese University of Hong Kong, Shenzhen；China Academy of Telecommunication Technology / CAICT
- **发表**: arXiv 2025（arXiv:2508.12633v2，2025年8月，eess.SY）；未明确正式 venue
- **链接/arXiv**: arXiv:2508.12633

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 非理想 V2V 通信——时变通信延迟（time-varying delay）与丢包（packet loss）
- **方法范式**: MARL (actor-critic, CTDE)、动态通信拓扑（multi-key gated network + causal inference）、状态增强/延迟补偿、Dec-POMDP
- **关键词**: connected vehicle platoon, dynamic communication topology, delay compensation, packet loss, MARL, V2V communication

## TL;DR（一句话总结）
针对车辆编队（platoon）在时变延迟与丢包的非理想 V2V 通信下控制退化问题，提出 DCT-MARL：用多键门控通信网络（基于因果推断+通信状态）动态调整通信拓扑以抗丢包，并用历史控制动作+延迟信息增广状态空间以抗延迟，提升串稳定性与驾驶舒适度。

## 问题与动机 (Problem & Motivation)
车联网编队协同控制依赖实时 V2V 信息共享，但真实环境信道衰落/遮挡/干扰导致时变延迟（信息过时）与丢包（信息缺失），损害 string stability 与驾驶舒适度。已有延迟补偿/丢包缓解方法（ZOH、插值、fallback、基于通信质量的动态拓扑）多依赖简化延迟假设、仅关注通信质量指标而忽略车辆间动态相关性，且通常孤立处理延迟或丢包之一。传统优化方法依赖精确模型、难扩展；现有 MARL 多假设理想通信。需统一框架同时处理延迟与丢包。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: V2V 通信延迟 ξ_{i,j}（车 i 在 t 收到的是 j 在 t-ξ 的信息）与丢包（通信 agent 某时刻不可用）。通信仿真采用 Rayleigh 小尺度衰落 + WINNER+ B1 路损（n=2.15 highway）+ 阴影衰落（N(0,σ²),σ=3dB）建模。非对抗性通信不完美。
- **设定**: cooperative；CTDE（集中 critic 训练、分散执行）；online。建模为 Dec-POMDP ⟨N,S,U,P,R,O,γ⟩，6 车编队（1 leader + 5 follower）。

## 方法 (Method)
- **状态增强（抗延迟）**: 状态扩展为 S_{i,t}={p,v,acc,u_{t-1},ξ_{i,t}}，纳入历史控制输入与延迟描述符，保持延迟观测下的 Markov 性，使策略能评估数据可靠性；并用条件期望修正奖励函数 R̃ 适应延迟环境。
- **多键门控动态拓扑（抗丢包）**: 通过 KL 散度做因果推断量化 agent j 对 agent i 决策的影响（causal confidence），prior 网络作二分类器；用 multi-key gating（Gumbel-Softmax 二值激活）选择 m 个通信对象，结合距离加权模块（近车权重高，体现避撞安全），聚合构造动态有向图邻接矩阵 A；限制 key 数保持输入维度稳定。
- **算法框架**: actor-critic，每个 actor 含通信网络 + 动作策略网络；集中 critic 用多头注意力聚合，TD 学习训练，仅训练用。目标含奖励 + 联合分布条件熵（鼓励探索并增强图策略 ρ）。
- **奖励设计**: r = -(ω1·errp + ω2·errv + ω3·jerk + ω4·ReLU(dsafe-d))，分别约束位置/速度跟踪误差、舒适度（jerk）、安全距离。
- **迭代训练**: 先固定 π、Q 更新图策略 ρ(A)，再用生成轨迹改进 π 与 Q。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（强调状态增强保持 Markov 性，但无收敛/稳定性理论证明）。

## 实验 (Experiments)
- **环境/Benchmark**: SUMO + Python 通信-控制联合仿真（TraCI），6 车编队，1km 高速路段；leader 轨迹取自 NGSIM I-80 真实拥堵数据；训练 100 万步，episode 600 步
- **Baselines**: 传统优化 DWOC、DRL 的 D3PG（已对齐含延迟补偿）；MARL 类 DEC-MARL（固定拓扑+状态增广）、LEB-MARL（因果推断拓扑, 即 I2C）
- **评估指标**: String Stability index S_i（越低越好）、Driving Comfort score G'_i（越高越好）、平均回报、推理时间

## 主要结果 (Key Results)
- DCT-MARL 在所有 CAV 上取得最低 string stability 指标（如 CAV5: 0.103 vs D3PG 0.221, DWOC 0.312）和最高舒适度（CAV1: 0.827 vs D3PG 0.643），对编队尾部（最易受扰）车辆改善尤其明显。
- 相对 MARL 基线：收敛更快、最终回报更高；DEC-MARL 固定拓扑在高丢包下退化，LEB-MARL 忽略通信质量时变性鲁棒性受限。
- 推理高效：600 步仿真约 3.7s，每决策步约 6ms，远低于 100ms 控制周期，适合实时部署。
- 通信热力图显示动态拓扑能自适应地利用前车为主、后车信息也显著被利用，验证动态拓扑的必要性。

## 局限与未来工作 (Limitations & Future Work)
论文局限不显式列出。可推断：仅 6 车小规模、特定高速场景验证；无理论保证；依赖通信仿真模型。未来：进一步研究非理想通信机制，探索通信与控制的联合优化，实现更自适应、资源高效的编队协同。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 的"通信鲁棒性（延迟+丢包）+ 应用（CAV 编队/智能交通）"主题线，特点是同时处理延迟与丢包，并将动态通信拓扑（因果推断的相关性 + 通信质量）结合。可与通信延迟（DACOM/CoDe）、丢包鲁棒（TMC #66）、动态拓扑通信工作对照，是面向真实 V2X 工程部署的非对抗性通信鲁棒方案。
