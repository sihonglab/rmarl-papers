# 184. A Survey on Fault Tolerant Multi Agent System

## 元信息 (Metadata)
- **标题**: A Survey on Fault Tolerant Multi Agent System
- **作者**: Yasir Arfat, Fathy Elbouraey Eassa
- **机构**: Department of Computer Science, King Abdulaziz University, Jeddah, Saudi Arabia
- **发表**: International Journal of Information Technology and Computer Science (IJITCS) 2016, Vol. 9, pp. 39–48
- **链接/arXiv**: doi:10.5815/ijitcs.2016.09.06

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 智能体失效、机器/进程/软件/硬件/通信失败（fault tolerance），非对抗性故障
- **方法范式**: 综述 / taxonomy；replication-based 与 non-replication-based fault recovery、redundancy、adaptive replication
- **关键词**: multi-agent system, fault tolerance, adaptive replication, redundancy, fault recovery, taxonomy

## TL;DR（一句话总结）
一篇关于 fault tolerant multi-agent system (FTMAS) 的综述，提供 faults 与容错技术的 taxonomy、对现有容错方法的定性比较与评估，指出多数现有方案因高计算代价、昂贵的 replication 与大通信开销而效率不高。

## 问题与动机 (Problem & Motivation)
MAS 在分布式环境中容易失效——智能体失效、机器崩溃、进程/软件/硬件/通信故障都会导致资源不可用、延迟达成目标。为提高 MAS 可靠性，系统需具备容错能力以 mask 失败、持续提供服务。已有大量容错方法被提出但缺乏系统梳理，本文动机即对这些方法做分类、比较与评估。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非恶意的系统故障（agent failure、machine crash、process/software/hardware/communication failure）；通过 replication / redundancy 等使系统在故障下继续运行
- **设定**: cooperative MAS；分布式环境；面向通用 agent 系统（非 RL）；综述视角

## 方法 (Method)
- 提出 faults 与容错 techniques 的 taxonomy，将 FTMAS 按 recovery 技术分类
- 区分 replication-based 与 non-replication-based fault recovery 方法
- 从特征、failure 类型、agent 类型、environment、replication protocol 等属性对现有技术做定性比较
- 对既有容错技术进行评估并总结其优缺点，讨论未来挑战

## 理论贡献 (Theoretical Contributions)
无 / 偏综述与分类（taxonomy、定性比较、评估），不含算法收敛性或形式化保证。

## 实验 (Experiments)
- **环境/Benchmark**: 无（文献综述）
- **Baselines**: 现有 FTMAS 容错方法（replication / non-replication）
- **评估指标**: 计算代价、replication 成本、通信开销、可靠性 / 性能等定性维度

## 主要结果 (Key Results)
- 现有容错方案多数效率不高，主要受制于高计算代价、昂贵的 replication 与大通信开销
- 给出 FTMAS 的 faults / techniques 分类框架与方法间的定性比较，指出容错与开销之间的权衡

## 局限与未来工作 (Limitations & Future Work)
为 2016 年综述，未涵盖近年学习型 / RL 容错；以定性比较为主，缺乏统一定量 benchmark；关注非恶意故障，未深入 Byzantine / 对抗攻击模型。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 的 [[fault-tolerance / 容错]] 背景文献，提供 MAS 故障类型与 replication / redundancy 容错技术的分类视角，是理解 [[Byzantine]]、agent-failure resilience 等主题在传统 MAS 中起源的背景参考，与去中心化 MARL 的容错设计动机相承接。
