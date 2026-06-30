# 88. AdvEvo-MARL: Shaping Internalized Safety Through Adversarial Co-Evolution in Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: AdvEvo-MARL: Shaping Internalized Safety Through Adversarial Co-Evolution in Multi-Agent Reinforcement Learning
- **作者**: Zhenyu Pan, Yiting Zhang, Zhuo Liu, Yolo Yunlong Tang, et al.；Han Liu（通讯）
- **机构**: Northwestern University；University of Illinois at Chicago；University of Rochester；Carnegie Mellon University
- **发表**: arXiv preprint 2025（未明确正式 venue）
- **链接/arXiv**: arXiv:2510.01586v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / jailbreak 与 prompt-injection 攻击、通信消息篡改、用户指令劫持（LLM-based MAS 安全）
- **方法范式**: 对抗训练（adversarial co-evolution）、MARL、minimax 博弈、REINFORCE++、public baseline advantage 估计
- **关键词**: LLM multi-agent safety, adversarial co-evolution, MARL, jailbreak defense, internalized safety

## TL;DR（一句话总结）
提出 AdvEvo-MARL，通过让 attacker 与 defender 在 MARL 中协同进化，将安全意识内化进任务智能体本身，无需外部 guard，即可在保持任务性能的同时把攻击成功率压到 20% 以下。

## 问题与动机 (Problem & Motivation)
LLM 多智能体系统（MAS）因开放性和交互复杂性易受 jailbreak、prompt-injection 和对抗协作攻击。现有防御分两类：(i) 自验证（self-verification），单 agent 能力有限，难以检测跨 agent 的不安全链条；(ii) 外部 guard 模块，引入单点失效、成本高、扩展性差。需要一种把安全内化到 task agent 的方法，且能抵抗自适应对手而非对静态数据集过拟合。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: attacker 生成不断演化的 jailbreak prompt；三种攻击场景——NetSafe（注入 dark trait 操纵 agent）、AutoInject（消息中注入对抗 prompt）、UserHijack（篡改用户指令）。攻击者能力随训练进化。
- **设定**: mixed（attacker vs defender 对抗，组内合作）；建模为 partially observable Markov game；online RL 训练；多 backbone 模型协同（非参数共享）

## 方法 (Method)
- 形式化为 partially observable Markov game，agent 分为 attacker 集 A 与 defender 集 D，目标为 max-min 博弈（defender 最大化、attacker 最小化净回报）。
- **Attacker warm-up**: 用 1000 个有害行为生成约 4000 条 (behavior, attack) 配对及推理轨迹，经 LLM-as-judge 过滤，SFT 注入 jailbreak 先验知识。
- **Co-evolutionary RL**: attacker 与 defender 用 REINFORCE++ 联合优化，attacker 不断改写更强 prompt，defender 同时抵抗攻击并完成任务。
- **Public baseline**: 同一功能组（attacker 或 defender）共享组内 mean return 作为 advantage baseline，降低方差、增强组内协作。
- **奖励建模**: attacker 奖励基于全局恶意目标是否达成；defender 奖励结合 local + global 的安全(s)、任务(t)、格式(f)三项；训练前半段重安全、后半段重任务。

## 理论贡献 (Theoretical Contributions)
偏实证。给出 max-min 博弈目标公式与 public baseline advantage 估计，但无收敛性/均衡存在性的形式化证明。

## 实验 (Experiments)
- **环境/Benchmark**: 三种 MAS 拓扑（chain/tree/complete），三种攻击（NetSafe/AutoInject/UserHijack）；任务 benchmark：AIME'24&'25、GPQA-diamond、LiveCodeBench；训练数据 MATH-500（lv3-5）；攻击 prompt 来自 JailbreakBench/Wild Jailbreak/Strong Reject。
- **Baselines**: Vanilla QWen2.5-3B/7B、Challenger（self-verification）、Inspector（外部 guard）、GPT-3.5、GPT-4o-mini。
- **评估指标**: Attack Success Rate (ASR)、Contagion Rate (CR)、任务 Accuracy / Pass@1。

## 主要结果 (Key Results)
- AdvEvo-MARL 在几乎所有配置下取得最低 ASR/CR；chain/tree 拓扑 ASR 常近零，complete 拓扑最高 17.68%，而 baseline 在 UserHijack 下 Challenger-7B 达 38.33%。
- 任务性能基本不退化甚至提升：7B 变体在 OOD 任务上超越 vanilla，最高 +3.67%（reasoning），LiveCodeBench 最高 +4%。
- 动态 attacker 相比静态 attacker 在 NetSafe 下降低约 12% ASR；attacker prompt diversity 训练后期上升，证明协同进化驱动泛化。
- Public baseline 带来更稳定训练，避免 defender 响应长度退化（无 baseline 时后期下降约 13.3%）。

## 局限与未来工作 (Limitations & Future Work)
实验仅 3 个 agent、QWen2.5 3B/7B backbone；complete 拓扑下 CR 仍较高（最高约 50%）；缺乏理论保证；对更大规模 MAS 与更广攻击类型的泛化未充分验证。

## 与综述的关联 (Relevance to Survey)
属于 LLM-based MARL 安全方向，将对抗训练/co-evolution 与 minimax 博弈用于内化安全，连接「对抗智能体/通信攻击」与「对抗训练范式」两条主线，是 robust MARL 在大模型智能体系统上的最新代表。
