# 35. Fault-Tolerant MARL for CAVs under Observation Perturbations for Highway On-Ramp Merging

## 元信息 (Metadata)
- **标题**: Fault-Tolerant MARL for CAVs under Observation Perturbations for Highway On-Ramp Merging
- **作者**: Yuchen Shi, Huaxin Pei, Yi Zhang, Danya Yao
- **机构**: Department of Automation, Tsinghua University；BNRist, Tsinghua University, Beijing, China
- **发表**: arXiv:2511.23193v1 (2025)（cs.RO；venue 未明确，疑投 IEEE）
- **链接/arXiv**: arXiv:2511.23193

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 观测/感知与通信故障扰动 (observation faults / perturbations)，容错 (fault tolerance)
- **方法范式**: 对抗训练（co-trained fault injection agent）、自诊断/异常检测 + 观测重构（时空相关性、temporal network/GRU）、防御-进攻协同
- **关键词**: cooperative driving, CAV, fault tolerance, observation perturbation, adversarial fault injection, on-ramp merging

## TL;DR（一句话总结）
针对 CAV 协同驾驶中 MARL 对观测故障容错不足的问题，提出 OFT-MARL：一个全局对抗 fault injection agent 在训练中生成最具破坏性的观测扰动以硬化策略，配合具备自诊断能力的容错车辆 agent（利用车辆状态序列的时空相关性检测故障并重构可信观测），在高速公路匝道汇入场景下实现接近无故障水平的安全与效率。

## 问题与动机 (Problem & Motivation)
CAV 协同驾驶依赖实时信息交换，但通信/感知故障使观测偏离真值，错误观测会误导决策并在车队中传播，破坏协同能力甚至引发安全事故。现有 MARL 协同驾驶研究很少考虑感知/通信故障的影响机制，容错不足成为落地瓶颈。两大挑战：(1) 如何生成训练中能有效压力测试策略的扰动（随机/手工注入幅度不当、影响可忽略）；(2) 如何让车辆缓解被污染观测的影响（车辆无法判断自身观测是否被扰动，盲信不安全、过度不信任又过保守）。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 观测扰动作用于车辆感知到的他车位置、速度等关键状态；由全局 fault injection agent 聚合所有车辆观测与故障信息、基于全局态势计算最具破坏性的扰动策略，与车辆策略协同训练。M 个车辆可被攻击。
- **设定**: cooperative（多车协同）；基于 MADDPG（连续动作）；online，对抗协同训练

## 方法 (Method)
1. **对抗 fault injection agent**: 全局 agent 聚合全车观测/故障信息，生成最优对抗观测扰动，与车辆策略并发协同训练，通过对抗学习持续暴露使车辆策略容错能力增强（进攻方）。
2. **容错车辆 agent（自诊断）**: 基于车辆运行数据固有的时空相关性（轨迹连续平滑、无频繁急加减速），用 temporal network (含 GRU) 分析状态序列时序特征，检测显著偏离正常动态的数据并重构可信的真实观测估计（防御方）。
3. **防御-进攻协同**: fault injection 硬化策略 + 容错 agent 屏蔽错误输入，共同构成容错系统。
4. 基于 MADDPG 增强容错以实现精确速度控制。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（方法与系统设计为主，无收敛性/均衡证明）。

## 实验 (Experiments)
- **环境/Benchmark**: 仿真高速公路匝道汇入 (on-ramp merging) 场景，多车协同。
- **Baselines**: MADDPG (fault-free)、Vanilla MADDPG、OFT-MARL w/o GRU（消融）、OFT-MARL；并在 fault-free / random fault / 多种 fault injection agent 生成的故障 / retrained fault 等条件下测试泛化。
- **评估指标**: Reward、Collision Rate、Timesteps；故障诊断的准确率/精确率/召回率；观测重构的 MAE/MSE recovery。

## 主要结果 (Key Results)
1. 对抗故障训练下，OFT-MARL (reward −0.38, 碰撞率 12.5%) 显著优于 Vanilla MADDPG (reward −2.36, 碰撞率 22.9%)，接近无故障水平 (MADDPG fault-free 碰撞率 11.3%)。
2. 跨多种故障模式（含针对固定策略 retrained 的对抗故障）泛化良好，性能退化轻微，明显优于 baseline。
3. 自诊断时序网络故障检测准确率 99.3%、精确率 99.6%、召回率 95.8%；观测重构将位置 MAE 从 9.10m 降至 3.36m（63.1% 纠正），速度等指标 recovery 亦超 50%。
4. 消融显示 GRU/时序自诊断模块对容错贡献关键。

## 局限与未来工作 (Limitations & Future Work)
聚焦匝道汇入单一场景与 MADDPG；偏实证无理论保证；未来可扩展到更多驾驶场景、更复杂故障/攻击模型与真实部署（论文末提出后续方向，具体细节未明确）。

## 与综述的关联 (Relevance to Survey)
应用驱动的观测扰动容错 MARL（自动驾驶/CAV 领域），结合对抗训练（attacker co-training）与检测-重构式防御，代表 robust MARL 在安全攸关协同控制中的落地。与状态/观测扰动鲁棒主线、对抗训练、容错/fault-tolerant 分支相关。
