# 75. IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems

## 元信息 (Metadata)
- **标题**: IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems
- **作者**: Yihuan Mao*, Yipeng Kang*, Peilun Li, Ning Zhang, Wei Xu, Chongjie Zhang
- **机构**: Tsinghua University; BIGAI; Shanghai Tree-Graph Blockchain Research Institute; Washington University in St. Louis
- **发表**: AAMAS 2025 (under review)
- **链接/arXiv**: arXiv:2410.16237v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击（恶意/被攻陷 agent 发送虚假消息）、Byzantine 容错；LLM agent 的 hallucination 导致的消息异常
- **方法范式**: 共识协议（Byzantine consensus / 随机化多轮广播）、博弈论一致性、与 MARL（Q-learning）集成、认证式鲁棒（理论保证）
- **关键词**: Multi-agent systems, zero-shot robustness, Byzantine Generals Problem, consensus protocol, communicative MARL, partial coordination

## TL;DR（一句话总结）
提出经典 BGP 的松弛版本 Imperfect BGP（IBGP，只需 k 个 benign agent 达成局部共识），设计带全局随机器的多轮 (k,λ)-共识协议并集成进 MARL，提供对通信攻击的可证明 zero-shot 鲁棒性，且容忍恶意比例可达 50%。

## 问题与动机 (Problem & Motivation)
随着 LLM agent 进入基础设施，异构 agent 间的消息同步至关重要。消息与动作可能因 hallucination 或被攻陷而异常，导致 V2V 等场景的危险误协调。经典 BGP 要求全局共识、冗余大且在恶意比例超 33% 时不可行；但 MAS 中往往只需局部/部分协调（如 predator-prey 只需部分捕食者）。现有 MAS 共识研究很少关注对抗攻击，且缺乏对攻击者和环境的 zero-shot 适应能力。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: n 个 benign agent + t 个攻击者，攻击者可在完全通信网络中发送任意虚假消息扰乱协调（攻击通信信道而非动作）；agent 不知他人身份。目标是避免误协调（mis-coordination），关注鲁棒性而非期望回报。
- **设定**: cooperative；decentralized（Dec-POMDP）；零样本（zero-shot，测试时面对未见攻击）

## 方法 (Method)
1. 定义 IBGP：成功协调只需 ≥k 个观测 M0=1 的 agent 合作（Agreement: #(M0=1,a=1)∈{0}∪[k,n]），重新定义 Agreement/Consistency 以匹配部分协调。
2. 指出单轮阈值决策不足（didactic 反例），提出多轮广播 (k,λ)-协议：全局随机器从分布 R 采样总轮数 r_tot（攻击者不知），各轮 active agent 按收到消息数是否 ≥k+λ 广播，最后一轮按 ≥k 决策。
3. 取 λ=t 时给出鲁棒性定理：临时误协调最多持续一轮，且由于 r_tot 对攻击者未知，攻击成功概率极低。
4. 将共识协议作为 Dec-POMDP 的协调子模块集成进 Q-learning：agent 学习何时选择 "propose to catch"（置 M0=1 参与共识），由协议决定是否真正协同行动；通过 prompt 指令即可集成进 LLM agent。

## 理论贡献 (Theoretical Contributions)
- Theorem 1: (k,t)-协议在任意攻击下以置信度 1−max_r{p(r_tot=r)} 鲁棒求解 IBGP(t,k)。
- 协议相比 BGP 需更少冗余、容忍更高恶意比例（最高 50% vs BGP 的 33%）。

## 实验 (Experiments)
- **环境/Benchmark**: Predator-prey（单/多目标/大规模, 如 (4,1,2,1)、(20,4,2,2)）、Hallway((3,1,2,1)、(10,1,5,2))、SMAC 改造的 4bane_vs_1hM、自建 3z_vs_1r；以及 Sensor Network 案例研究
- **Baselines**: Recursive training、AME、ADMAC
- **评估指标**: robustness percentage（有攻击者测试性能 / 无攻击者训练性能），zero-shot 通信攻击下的鲁棒性

## 主要结果 (Key Results)
1. IBGP 协议在多数环境中 robustness percentage 接近或达 100%（如 Predator-prey(20,4,2,2)、Hallway(10,1,5,2) 为 100%），显著优于 AME、ADMAC、Recursive training。
2. 在大规模和更高协调阈值场景下仍保持鲁棒，可扩展性好；多个 baseline 在部分环境训练不收敛（'/'）。
3. 在 3z_vs_1r 这类需兼顾效率与鲁棒的挑战任务上仍领先（51.5%），凸显效率-鲁棒权衡。

## 局限与未来工作 (Limitations & Future Work)
- 关注布尔型 {0,1} 提案的协调一致性，目标偏向避免误协调而非最大化回报；3z_vs_1r 显示效率仍有改进空间。
- 鲁棒性依赖全局随机器和随机轮数机制；恶意比例需保持在阈值（≤50%）以下。
- 未来可扩展到更复杂的 LLM agent 协调与真实异构系统。

## 与综述的关联 (Relevance to Survey)
代表 robust MARL 中“通信攻击 / Byzantine 容错”分支，独特之处是把分布式系统的 Byzantine 共识协议（带可证明保证、zero-shot）引入通信式 MARL 与 LLM multi-agent 系统，松弛为部分协调（IBGP）。与认证鲁棒、容错 MARL 主题相关，桥接共识协议理论与学习型多智能体协调。
