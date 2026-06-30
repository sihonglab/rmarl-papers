# 103. A Pilot Study of Observation Poisoning on Selective Reincarnation in Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: A Pilot Study of Observation Poisoning on Selective Reincarnation in Multi-Agent Reinforcement Learning
- **作者**: Harsha Putla, Chanakya Patibandla, Krishna Pratap Singh, P Nagabhushan
- **机构**: Indian Institute of Information Technology, Allahabad (IIITA)；Vignan's Foundation for Science, Technology & Research
- **发表**: Neural Processing Letters 2024 (vol. 56:161)
- **链接/arXiv**: https://doi.org/10.1007/s11063-024-11625-w

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 观测投毒 (observation poisoning)；对 teacher dataset 的对抗扰动（数据投毒触发器）
- **方法范式**: 鲁棒性脆弱性评估 (empirical robustness evaluation)；攻击研究而非防御；以 Kendall's tau 排序相关性量化
- **关键词**: observation poisoning, selective reincarnation, MARL, adversarial attacks, Kendall's tau

## TL;DR（一句话总结）
通过向 MARL selective reincarnation 的 teacher dataset 注入四种观测投毒触发器（高斯噪声、反转、随机打乱、缩放），实证评估了 reincarnation 决策对观测投毒的脆弱性，并用 Kendall's tau 量化排序扰动程度。

## 问题与动机 (Problem & Motivation)
selective reincarnation（复用先前计算/teacher 经验来加速 MARL 训练）虽提升效率，但引入了新的对抗脆弱性。观测投毒可微妙地操纵观测空间误导学习，但其对 reincarnation 决策（选哪些 agent 复用）的影响尚未被研究。本文系统评估该脆弱性以为更安全的 MARL 提供依据。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者篡改 teacher dataset（"Good-Medium"，约最后 40% 经验）中的观测矩阵（10×10）；四种触发器：高斯噪声 (σ=0.01)、观测行反转、随机行打乱、缩放 (α=1.1)。攻击为训练期数据投毒
- **设定**: cooperative；decentralized（IDDPG，Dec-POMDP）；offline teacher data 驱动的 reincarnation + online retraining

## 方法 (Method)
- 在 HalfCheetah (Multi-Agent MuJoCo) 上将机器人视为 6 个协作 agent（BA/BK/BH/FA/FK/FH），用 IDDPG 训练 1M 步生成 teacher dataset。
- 对 teacher dataset 施加四种观测投毒触发器，得到 poisoned dataset。
- 枚举 2^6=64 种 agent reincarnation 组合，每组在 poisoned 数据上 retrain（200k 步 + 50k 学生数据），跨 5 个 seed。
- 用 maximum return 与 average return 排序各组合，计算投毒前后排序的 Kendall's tau；并定义 "Overall Vulnerability" 指标量化各 agent 组合脆弱性。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（提供 Kendall's tau 与 Overall Vulnerability 的统计量化框架，但无收敛/认证理论）。

## 实验 (Experiments)
- **环境/Benchmark**: HalfCheetah (Multi-Agent MuJoCo / MaMuJoCo)，6 agent 协作
- **Baselines**: 基线为无投毒的 base case 与 Tabula Rasa；对比四种投毒触发器
- **评估指标**: maximum return、average return、Kendall's tau 排序相关、Overall Vulnerability 百分比

## 主要结果 (Key Results)
- reversal 攻击对 maximum return 影响最大，Kendall's tau 平均下降 38.08%；random shuffling 下降 17.66%；noise/scaling 与原排序对齐度仅 21.42%/32.66%。
- 脆弱性因 agent 组合而异：组合 {BA, FA, FK} 最脆弱（vulnerability 46%），而 BA 单独表现出韧性（负脆弱性 -10%，攻击下反而更好）。
- reversal 与 shuffling 尤其破坏 inter-agent 协作；reincarnation agent 越多投毒影响越小，但 scaling 的排序影响与 agent 数无关。

## 局限与未来工作 (Limitations & Future Work)
仅用基础、环境无关的触发器；单一环境 (HalfCheetah)、单一算法 (IDDPG)；仅为脆弱性研究，未提出防御。未来计划扩展到 Humanoid 等更多环境、cooperative/competitive/mixed 设定、更高级触发器，并据此开发防御策略。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"训练期数据/观测投毒攻击与脆弱性评估"线，特别揭示了 reincarnation/经验复用范式的新攻击面。可作为综述中攻击侧（attack-side）与鲁棒性评估方法论（Kendall's tau 排序度量）的案例，呼应 reward/action/policy poisoning 的相关工作。
