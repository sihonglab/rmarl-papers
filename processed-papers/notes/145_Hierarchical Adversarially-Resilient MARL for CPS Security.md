# 145. Hierarchical Adversarially-Resilient Multi-Agent Reinforcement Learning for Cyber-Physical Systems Security

## 元信息 (Metadata)
- **标题**: Hierarchical Adversarially-Resilient Multi-Agent Reinforcement Learning for Cyber-Physical Systems Security
- **作者**: Saad Alqithami
- **机构**: Computer Science Department, Al-Baha University, Albaha, Saudi Arabia
- **发表**: AAAI Summer Symposium Series (SuSS-25), 2025
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体（自适应/zero-day 网络攻击：DoS、data tampering、APT、lateral movement、scan）、CPS 安全
- **方法范式**: hierarchical MARL、对抗训练（adversarial training loop / red-team attacker as learning agent）、minimax 博弈、PPO + GAE、multi-critic、博弈论均衡（local Nash）
- **关键词**: Cyber-Physical Systems, hierarchical MARL, adversarial training, CPS security, PPO, industrial IoT

## TL;DR（一句话总结）
提出 HAMARL：将局部防御 agent（子系统级）与全局协调者（系统级）组织为分层结构，并嵌入一个与防御方协同进化的自适应 attacker（对抗训练循环），用 PPO 在 Markov game 中训练，使工业 CPS 对自适应/zero-day 攻击具备主动、可扩展的对抗韧性。

## 问题与动机 (Problem & Motivation)
CPS（制造、智能电网、自动交通等）互联性增强使其暴露于复杂演化的网络威胁（APT、DDoS、data tampering）。传统 rule-based IDS 与单智能体 RL 难以适应 AI 驱动的自适应/zero-day 攻击。现有 MARL 安全框架多为扁平/去中心化结构，缺乏分层协调与显式对抗意识，对不断变招的攻击者脆弱。需要统一结合分层协调与对抗韧性的 CPS 安全方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 自适应 attacker（学习型 agent πψ），动作含 SCAN/LATERAL/DOS/TAMPER，与防御方同步训练、持续演化策略（含 zero-day/未见过攻击）；防御方部分可观测。
- **设定**: competitive-cooperative mixed（N 个 local defender + 1 global coordinator 合作，vs 1 attacker 竞争）；分层 + CTDE 思想（local 部分观测 + global 聚合）；建模为 (N+2)-agent partially observable Markov game；online 对抗训练。

## 方法 (Method)
- **分层架构**: 底层 local defender agent 监控各子系统（部分观测 ω_i），做轻量实时异常检测与本地响应（ALERT/QUARANTINE/PATCH）；顶层 global coordinator 聚合 local embedding（g），做系统级响应（ISOLATE-SEG/ROLL-PATCH/RESET-NODE）。
- **联合策略分解**: π = ∏ π_θi(a_i|ω_i) · π_ϕ(a_global|g) · π_ψ(a_att|ω_att)（Proposition 1）。
- **对抗训练循环**: attacker 与 defender 同步用 PPO 训练，attacker 因成功/隐蔽攻陷获正奖励、defender 因漏检/被攻陷受负奖励，形成 minimax 式均衡 → 对抗韧性。
- **PPO + GAE + multi-critic**: 各 agent 用 PPO（γ=0.99, λ=0.95, clip=0.2）+ GAE；local critic 评估检测性能，global critic 评估系统级指标；local 策略用 2 层 Graph Attention Network，global 用 3 层 MLP。
- **混合 reward**: local r_i=+1(TP)/−0.2(FP)/−1(miss)；global R=−0.1|Comp(t)|−0.01·DOWNTIME+0.2·UPTIME；含 formal safety checks（高风险动作触发域特定安全检查）。

## 理论贡献 (Theoretical Contributions)
- Theorem 1: 在标准假设（有界奖励、Markov mixing、充分探索、衰减步长）下，(N+2)-agent PPO+GAE 更新收敛到 stationary point，构成 local Nash equilibrium。
- Definition 2 + Theorem 2: 定义 (ϵ,δ)-adversarial resilience（compromise ratio ϱ）；证明若 defender 每步被攻陷代价 c 相对 attacker 奖励 r_a 足够大，则均衡下 compromise ratio ϱ* < 1（有界攻陷，部分容纳防止全面失效）。

## 实验 (Experiments)
- **环境/Benchmark**: 基于 Cyber-Battle-Sim 扩展的仿真工业 IoT 智能工厂——8 个 PLC 子系统、64 传感器、Modbus/TCP；合成但真实的数据。攻击场景含 DoS、data tampering、APT。
- **Baselines**: Single-Agent RL、Non-Hierarchical (flat) MARL、Rule-Based IDS。
- **评估指标**: Return、F1、Precision、Recall、FAR、MTTD、Accuracy、operational continuity；可扩展性（4/8/12/24 agent 训练时间）。

## 主要结果 (Key Results)
- HAMARL 与 Non-Hier MARL 在所有指标上远超 Rule-Based IDS（F1≈0.80 vs 0.44–0.52，Accuracy≈82.9% vs ~50%，FAR≈6.6% vs ~50%）。
- HAMARL 与 Non-Hier MARL 性能相当（precision/FAR 略优或持平），但 HAMARL 提供分层战略监督，对大规模/复杂环境与未见过攻击的韧性与全局协调更优。
- 对抗训练中 local defender 检测率持续 >90%，即使攻击者中途变招；global coordinator 通过及时隔离/打补丁降低 MTTD、保障运营连续性。
- 可扩展性：HAMARL 训练时间随 agent 数线性增长（4→24 agent: 0.036→0.204h），高于 Non-Hier 但仍可控。

## 局限与未来工作 (Limitations & Future Work)
分层 MARL 训练计算成本高（不利于资源受限 OT 网络）；reward shaping 与分层 credit assignment 需域特定调参；缺乏工业标准合规(IEC 62443)与现场验证。未来：lightweight policy distillation、transfer/meta-learning 初始化、federated/分布式训练降本；加入 explainability 与 formal verification 提升可信；扩展到多攻击者/合谋攻击场景。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗智能体 + 对抗训练 + 博弈论均衡"主线，并结合 hierarchical MARL 与 CPS 安全应用。将 attacker 显式建模为学习型 agent 进行 minimax 对抗训练，并提供 local Nash 收敛与 bounded compromise 的理论结果，是 adversarial-resilient hierarchical MARL 在工业 IoT/CPS 安全的代表性工作，与对抗训练、安全应用、分层方法、形式化保证等主题相关。
