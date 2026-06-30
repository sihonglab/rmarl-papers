# 169. Communication-Robust Multi-Agent Learning by Adaptable Auxiliary Multi-Agent Adversary Generation

## 元信息 (Metadata)
- **标题**: Communication-robust multi-agent learning by adaptable auxiliary multi-agent adversary generation
- **作者**: Lei Yuan, Feng Chen, Zongzhang Zhang, Yang Yu（Lei Yuan 与 Feng Chen 同等贡献）
- **机构**: Nanjing University（National Key Laboratory for Novel Software Technology）；Polixir Technologies
- **发表**: Frontiers of Computer Science 2023（2024, 18(6): 186331）
- **链接/arXiv**: doi:10.1007/s11704-023-2733-5

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信消息攻击（message perturbation / noise / hostile attack）作用于每条信息信道
- **方法范式**: 对抗训练、auxiliary adversary generation、把攻击者建模为 cooperative MARL、进化学习的 attacker population、交替训练
- **关键词**: multi-agent communication, adversarial training, attacker population, evolutionary learning, robustness validation

## TL;DR（一句话总结）
针对通信型协作 MARL 在噪声/攻击下脆弱的问题，提出 MA3C：把对每条消息信道的攻击建模为一个共享目标（最小化 ego system 协调能力）的 cooperative MARL 问题，再用进化学习生成具备攻击质量与行为多样性的 attacker population，与 ego system 交替对抗训练，从而得到对各信道、不同程度扰动都鲁棒的通信策略。

## 问题与动机 (Problem & Motivation)
通信能促进协作 MARL 的协调，但现有工作多聚焦通信效率，假设训练/测试环境相同，忽视真实世界通信存在噪声或攻击者。深度网络对微小对抗扰动极其敏感，会令 MARL 通信系统崩溃。MARL 通信的鲁棒性尤其复杂：N 个全连接智能体共有 N×(N−1) 条消息信道，直接训练攻击者会使其动作空间随智能体数急剧膨胀；以往工作只能做强假设（如所有信道同一扰动、或仅少数智能体注入启发式噪声）。单一攻击者的对抗训练又易过拟合、损害泛化。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 每条消息信道在任意时刻都可能被不同程度地扰动；每个 adversary 获取一个消息发送者的局部状态，对其发往各队友的消息输出随机扰动动作；存在 N 个 adversary 协同最小化 ego system 回报
- **设定**: cooperative（ego system 协作）；CTDE 式通信策略；online；对抗训练框架

## 方法 (Method)
- 新颖的 message-attacking 建模：将 auxiliary attacker 的学习视为共享目标的 cooperative MARL 问题——每个 adversary 对一个发送者发出的每条消息施加扰动，整体协同最小化 ego system 的协调能力，故可用任意 cooperative MARL 算法训练攻击者系统
- attacker population generation：基于 evolutionary learning 生成一组兼具高攻击质量与行为多样性的攻击者，缓解单一攻击者导致的过拟合、保护 ego system 泛化能力
- 交替/对抗训练：ego system 与持续进化的 attacker population 配对，交替训练，使双方均"可适应"(adaptable)，最终得到鲁棒的通信策略

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。主要为方法学贡献（把消息攻击转写为 cooperative MARL + 进化攻击者种群 + 交替训练），借鉴博弈论"最坏情况性能保证"的动机但不以形式化定理为核心。

## 实验 (Experiments)
- **环境/Benchmark**: Hallway、StarCraft Multi-Agent Challenge (SMAC) 两张地图、新建环境 Gold Panner (GP)、Traffic Junction (TJ)——均为需通信协调的协作任务
- **Baselines**: 多种通信型 MARL 及对抗训练/鲁棒通信方法
- **评估指标**: 受攻击下的回报/胜率（鲁棒性）、泛化能力、向复杂任务的迁移能力

## 主要结果 (Key Results)
- MA3C 在多个 benchmark 上提供与基线相当或更优的鲁棒性与泛化能力
- 将攻击建模为 cooperative MARL，使每条信道可遭受不同的消息攻击，攻击更贴近真实威胁
- attacker population（进化生成的多样化攻击者）缓解单一攻击者的过拟合，提升 ego system 的泛化与迁移能力

## 局限与未来工作 (Limitations & Future Work)
对抗 + 进化种群的交替训练计算开销较大；鲁棒性以实证为主、缺乏形式化保证；攻击者建模与种群规模等超参对结果有影响；在更大规模/真实通信场景的验证仍有限。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[通信攻击]] 防御侧的代表性工作，与 168（对抗通信涌现的威胁建模）形成"攻击—防御"呼应；方法上结合 [[对抗训练]] 与 [[population-based/进化学习]]，把单智能体鲁棒 RL 的 auxiliary adversary 思路扩展到多信道通信 MARL；与 [[CTDE]]、[[SMAC benchmark]] 主题相关。
