# 156. SoK: Adversarial Machine Learning Attacks and Defences in Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: SoK: Adversarial Machine Learning Attacks and Defences in Multi-Agent Reinforcement Learning
- **作者**: Maxwell Standen, Junae Kim, Claudia Szabo
- **机构**: Defence Science and Technology Group（澳大利亚国防科技集团）；The University of Adelaide
- **发表**: ACM Computing Surveys 2025；arXiv:2301.04299 (2023)
- **链接/arXiv**: arXiv:2301.04299；doi:10.1145/3708320

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: execution-time（执行期）对抗机器学习攻击——观测扰动、动作扰动、通信攻击、对抗智能体等；涵盖攻击与防御两侧
- **方法范式**: SoK / 综述与分类学（taxonomy）、Attack Vector 框架、对抗训练等防御范式梳理
- **关键词**: adversarial machine learning, MARL, attack vector, taxonomy, execution-time attack, defence

## TL;DR（一句话总结）
这是首篇系统梳理 MARL 执行期对抗机器学习（AML）攻击与防御的 SoK/综述，提出受网络安全启发的 "Attack Vector" 新视角与两套建模框架（刻画攻击的手段、强度、节奏 tempo 与位置 location），并对攻击与防御给出分类学，指出研究空白与未来方向。

## 问题与动机 (Problem & Motivation)
DRL 已从单智能体走向部分可观测的多智能体，并应用到自动驾驶、电网、网络防御等安全攸关场景，但深度学习固有的 AML 脆弱性（如人眼难辨的输入扰动即可改变网络输出）尚未在 MARL 语境下被系统研究。已有 AML 综述只覆盖 DRL/MAL，缺少针对 MARL 的统一视角；同时 DRL 中对抗训练只能得到对特定攻击的"窄鲁棒"，难以泛化到未见攻击。作者主张 MARL 从业者亟需理解可用的攻击与防御谱系。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 聚焦执行期（训练后部署阶段）攻击；用 Attack Vector 刻画攻击如何被实施、使用何种信息、攻击目标为何；两套框架进一步描述攻击的 magnitude、tempo（节奏/时机）与 location（位置）
- **设定**: 覆盖 cooperative / competitive / mixed；涉及 centralised/decentralised 训练与执行（CTDE、IQL、CommNet、DIAL 等）；online 执行期

## 方法 (Method)
- 对 MARL、DRL、MAL 三类领域的 AML 工作做系统化综述（Systematization of Knowledge）
- 提出 **Attack Vector** 视角：以网络安全思路描述攻击的实施方式、所需信息与目标
- 给出攻击分类学（如何部署、利用什么信息、攻击目标）与改进的防御分类学（防御类型、可对抗的 Attack Vector、部署时机、所需先验信息）
- 提出两套新建模框架，刻画 Attack Vector 组合与攻击的强度/节奏/位置
- 总结知识空白并展望未来研究方向

## 理论贡献 (Theoretical Contributions)
无 / 偏综述与概念框架（提出 Attack Vector 视角与两套攻击建模框架、攻击与防御分类学），非定理型贡献。

## 实验 (Experiments)
- **环境/Benchmark**: 无（综述类，无独立实验）
- **Baselines**: 无
- **评估指标**: 无（以文献归类与框架适用性进行定性分析）

## 主要结果 (Key Results)
- 指出此前无专门针对 MARL 的 AML 攻防综述，本文填补该空白
- Attack Vector 视角能统一刻画 MARL 中多样攻击的实施途径；强调攻击时机（tempo）与位置对攻击有效性的重要性
- 现有防御（尤其对抗训练）泛化性差，难以抵御未见攻击，是关键开放问题

## 局限与未来工作 (Limitations & Future Work)
作为 SoK 受限于已有文献覆盖面；MARL 专属（区别于单智能体）的攻击与防御仍稀缺；防御对未见攻击的泛化、跨 Attack Vector 的统一防御、训练期攻击等方向有待深入。

## 与综述的关联 (Relevance to Survey)
本文是 robust MARL 中"对抗攻击与防御谱系"线的导航性综述，为 [[观测扰动]]、[[动作扰动]]、[[通信攻击]]、[[对抗智能体]] 等威胁模型提供统一分类与术语；其 Attack Vector / tempo / location 框架可作为本综述组织攻击章节的参照，并与 [[对抗训练]] 防御线直接呼应。
