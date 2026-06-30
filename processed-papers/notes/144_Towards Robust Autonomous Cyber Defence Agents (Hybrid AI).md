# 144. Towards Robust Autonomous Cyber Defence Agents using Hybrid AI models

## 元信息 (Metadata)
- **标题**: Towards Robust Autonomous Cyber Defence Agents using Hybrid AI models
- **作者**: Laurin Holz, Johannes Loevenich, Roberto Rigolin F. Lopes
- **机构**: Secure Communications & Information (SIX), Thales Deutschland, Ditzingen, Germany
- **发表**: IEEE International Conference on Network Softwarization (NetSoft) 2025（PhD thesis/方向性论文，DOI 10.1109/NETSOFT64993.2025.11080605）
- **链接/arXiv**: 未明确（IEEE Xplore）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体（cyber 攻击）、状态/观测扰动（输入扰动）、部分可观测与不确定性、安全约束（safety/liveness）
- **方法范式**: 形式化验证（Formal Verification: reachability、model checking、temporal logic、theorem proving、abstract interpretation、fuzz testing）、hybrid AI（MARL + symbolic AI/知识图谱 + LLM）、CTDE/课程学习、认证鲁棒
- **关键词**: Software-Defined Defence, Autonomous Cyber Defence, MARL, Formal Verification, LLM, trustworthy AI

## TL;DR（一句话总结）
一篇 PhD thesis 方向性论文，提出将 Formal Verification (FV) 应用于 ACD 的 MARL 系统，结合 hybrid AI（MARL + 知识图谱 + 增强 LLM）与 human-in-the-loop 接口，为军事关键网络基础设施中的自治网络防御 agent 提供数学化的正确性、安全性与对抗鲁棒性保证。

## 问题与动机 (Problem & Motivation)
Software-Defined Defence (SDD) 提供多层监控/控制接口实现 ACD，但缺乏对这些 hybrid AI agent 鲁棒性与安全性的评估。MARL 学得的策略不透明、随机，在军事网络等关键环境难以建立信任与部署。FV 在传统软硬件正确性验证中成熟，并逐渐应用于神经网络，但在 MARL 中仍严重欠探索。需用 FV 量化并提升 hybrid AI ACD 方案的鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 演化的网络攻击、输入空间的意外/对抗扰动（fuzz testing 注入）、部分可观测与噪声/不完整信息；目标是验证不可达 unsafe 状态、满足时序逻辑(LTL/CTL)的 safety/liveness。
- **设定**: cooperative（多 blue agent 协防 user hosts/operational servers）；建模为 POMDP；训练支持 CTDE / Independent Learning / CTCE / hierarchical MARL；simulated/emulated（CybORG/BRETAGNE）。

## 方法 (Method)
- **三阶段方法论**: (A) 在 ACO gym 环境用课程学习 + 多种范式(CTDE/IL/CTCE/hierarchical) 训练 MARL agent 并实证评估鲁棒性；(B) 将训练好的 agent + 环境 + 待验证属性送入 FV 框架；(C) 将验证结果集成入 human-machine 接口。
- **FV 技术组合**: reachability analysis（不安全状态可达性）、model checking（时序逻辑全路径验证）、fuzz testing（对抗输入容错）、temporal logic (LTL/CTL)、theorem proving（数学正确性证明）、abstract interpretation（高层静态分析/异常检测）。
- **LLM 集成**: 验证失败时生成 counterexample，由 fine-tuned LLM 翻译为自然语言解释并给出修正建议，形成 human-in-the-loop 反馈回路（重训练/改环境/精化规约）。
- **POMDP 建模**: 7 元组 (S,A,T,R,Ω,O,γ)，状态含拓扑/主机/漏洞/被攻陷程度，动作含扫描/阻断/恢复/部署诱饵，观测含其他 agent 的消息以缓解部分可观测。

## 理论贡献 (Theoretical Contributions)
无 / 偏方向性（research proposal/thesis outline）。本身不提供新定理，而是规划应用 FV 提供正确性/安全/鲁棒性的形式化保证；综述了相关工作中具收敛/正确性保证的方法（如 ALMANAC、MILP reachability）。

## 实验 (Experiments)
- **环境/Benchmark**: 计划使用 CybORG (Cyber Operations Research Gym) 与 BRETAGNE 仿真/仿真器环境（尚为 outlook，未给出实验结果）。
- **Baselines**: 未明确（方向性论文）。
- **评估指标**: 计划评估 agent 性能、适应性、对抗鲁棒性；FV 输出（正确性证明、counterexamples、coverage metrics）。

## 主要结果 (Key Results)
- 本文为 thesis 方向性论文，尚无实验结果；核心为提出研究空白（FV + MARL + LLM 三者结合在 cybersecurity 中未被探索）与方法论框架。
- 通过 Table I 对比指出本工作是唯一同时涵盖 cybersecurity + hybrid AI + MARL + FV + user interface 的方案。
- 假设：FV 可显著提升 MARL ACD agent 的鲁棒性/安全性/可信度，LLM 接口可将 FV 结果转为可解释洞见支持人工监督。

## 局限与未来工作 (Limitations & Future Work)
处于研究早期（outlook 阶段），无落地实现与定量验证；FV 在 MARL 上的可扩展性与部分可观测处理是核心挑战。未来：在 CybORG/BRETAGNE 上实现 FV 改进的 CTDE 训练，将 FV 结果提供给 LLM agent 自动优化实验与训练过程，面向军事网络需求构建完整验证框架。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"认证鲁棒/形式化验证"主线与网络安全(ACD)应用线，强调可信、可验证的鲁棒性保证（safety/correctness/adversarial resilience），并引入 hybrid AI（MARL + symbolic + LLM）。是少见的将 Formal Verification 系统性引入 MARL 鲁棒性评估的方向性工作，与认证鲁棒、temporal logic 约束、LLM-based MARL 主题相关。
