# 91. LLM-based Multi-Agent Reinforcement Learning: Current and Future Directions

## 元信息 (Metadata)
- **标题**: LLM-based Multi-Agent Reinforcement Learning: Current and Future Directions
- **作者**: Chuanneng Sun, Songjun Huang, Dario Pompili
- **机构**: Department of Electrical and Computer Engineering, Rutgers University–New Brunswick
- **发表**: arXiv 2024（submitted to IEEE Robotics & Automation Letters）
- **链接/arXiv**: arXiv:2405.11106v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 综述性，涉及通信篡改/恶意数据注入、模型偏见利用、安全约束（作为「safety and security in MAS」研究方向之一）
- **方法范式**: 综述（survey/letter）；涉及 CTDE、learning-to-cooperate / learning-to-communicate、LLM-as-agent、对抗训练、知识蒸馏
- **关键词**: LLM-based MARL, language-conditioned MARL, multi-agent systems, communication, safety and security

## TL;DR（一句话总结）
一篇综述短文，系统梳理传统 MARL、LLM-based 单智能体 RL 与现有 LLM-based MARL 框架，并提出四个未来方向（个性化协作、human-in/on-the-loop、传统 MARL 与 LLM 协同设计、MAS 的安全与安全防护）。

## 问题与动机 (Problem & Motivation)
传统 MARL 在协调/通信上仍逊于人类专家，自然引出「为何不利用人类知识与语言」。LLM 含通用世界知识、可少样本泛化，将其引入 MARS 协调与通信有巨大潜力，但单智能体 RL 框架不直接考虑多智能体协调/通信。现有综述均未专门聚焦 LLM-based MARL，本文填补该空白。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 作为未来方向讨论——agent 通信被操纵、恶意数据注入、模型偏见被利用；连续动作空间下的高风险操作安全。建模基础为 Dec-POMDP。
- **设定**: 主要 cooperative（共同目标 + 通信）；涵盖 CTDE 与 human-in/on-the-loop；非具体算法（综述）

## 方法 (Method)
- 综述传统 MARL：分 learning-to-cooperate（QMIX/QTRAN/MADDPG/MAPPO 等，CTDE）与 learning-to-communicate（学习消息内容/通信网络结构/涌现语言）。
- 综述 LLM-based 单智能体 RL：open-loop（ReAct、Reflexion、ADaPT）与 closed-loop（Refiner、Retroformer、REX、LLM 反馈做 credit assignment）。
- 综述现有 LLM-based MARL：问题求解类（DyLAN、FAMA、consensus seeking、ToM、MetaGPT）与具身应用类（CoELA、SMART-LLM、RoCo、Co-NavGPT 等），并给出对比表。
- 提出四个未来方向，其中「Safety and Security in MAS」涉及安全通信协议、加密、对抗训练、输入验证、实时异常监测与回滚等鲁棒性机制。

## 理论贡献 (Theoretical Contributions)
无（综述/展望性 letter），无新理论结果。

## 实验 (Experiments)
- **环境/Benchmark**: 无原创实验；综述涉及的 benchmark 包括 MATH、MMLU、HumanEval、BabyAI-Text、TDW-MAT/C-WAH、RoCoBench、HM3D、VirtualHome-Social 等。
- **Baselines**: 无（综述）
- **评估指标**: 无（综述）

## 主要结果 (Key Results)
- 指出 language-conditioned MARL 尚处早期但前景广阔，语言可提升协调、谈判、人机交互与可解释性。
- 提出 LLM 作为 centralized critic 指导 actor 训练、再蒸馏到小模型上板执行的协同设计思路（in-context distillation）。
- 把 MAS 的安全与安全防护列为关键开放问题，强调 proactive（安全通信/对抗训练/输入验证）+ reactive（监测/隔离/回滚）双重策略。

## 局限与未来工作 (Limitations & Future Work)
本身为简短 letter，覆盖面有限、无实验验证；指出 LLM-based MARL 整体仍属未充分探索领域，连续动作空间集成、安全防护、资源高效部署等均待研究。

## 与综述的关联 (Relevance to Survey)
作为 LLM-based MARL 的方向性综述，为本 robust MARL 综述提供背景与未来方向；其「Safety and Security in MAS」一节直接对应对抗训练、通信攻击防御、安全约束等鲁棒性主题，可作为相关工作与动机引用。
