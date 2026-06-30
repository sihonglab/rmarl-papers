# 87. Evo-MARL: Co-Evolutionary Multi-Agent Reinforcement Learning for Internalized Safety

## 元信息 (Metadata)
- **标题**: Evo-MARL: Co-Evolutionary Multi-Agent Reinforcement Learning for Internalized Safety
- **作者**: Zhenyu Pan, Yiting Zhang, Yutong Zhang, Jianshu Zhang, Haozheng Luo, Yuwei Han, et al. (Philip S. Yu, Manling Li, Han Liu 等)
- **机构**: Northwestern University; University of Illinois at Chicago
- **发表**: 未明确（arXiv 预印本）
- **链接/arXiv**: arXiv:2508.03864v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: jailbreak / 对抗攻击、prompt injection（间接提示注入）、恶意智能体、安全风险传染 (safety contagion)、单点失效；LLM/MLLM 多智能体系统安全
- **方法范式**: 对抗训练、co-evolution（进化搜索：mutation/crossover）、parameter-sharing MARL、GRPO、内化安全 (internalized safety)
- **关键词**: MAS safety, LLM agents, co-evolution, adversarial training, GRPO, jailbreak defense

## TL;DR（一句话总结）
提出 Evo-MARL，一种把安全防御能力"内化"到每个任务智能体中的 MARL 框架，通过进化搜索演化攻击 prompt 池与 GRPO 参数共享训练 defender 协同对抗，使 LLM/MLLM 多智能体系统在不增加外部 guard 模块的前提下提升对 jailbreak 攻击的鲁棒性，同时还略微提升任务性能。

## 问题与动机 (Problem & Motivation)
基于 LLM/MLLM 的多智能体系统 (MAS) 协作能力强，但开放性与交互复杂性带来 jailbreak、对抗攻击、prompt injection 等安全风险，单个被攻陷的智能体可经交互图级联破坏全系统。现有防御依赖外部 guard 模块（专用安全智能体），存在两大缺陷：(1) 独立 guard 在任务智能体缺乏安全意识时保护有限；(2) 单 guard 是单点失效，被攻陷则系统级安全崩溃；naive 增加 guard 数量又抬高成本与复杂度。因此作者主张把防御能力内化到每个任务智能体，培养集体安全意识。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 链式结构 MAS（problem analyst、solving executor、answer verifier 三个角色）；随机选一个 agent 作为初始受害者，通过间接 prompt injection 把攻击 prompt 顺序注入该 agent 及其下游 peer 的响应，模拟安全传染。攻击者被当作外部第三方对手，不纳入 RL 优化；攻击 prompt 通过进化搜索持续演化。
- **设定**: cooperative defenders vs 演化的 attacker（mixed/对抗）；MARL，attacker 与 defender 在共享 MDP E=(S,Aa,Ad,T,Ra,Rd) 中；defender 参数共享、role-conditioned 策略；online 对抗训练

## 方法 (Method)
- 内化安全：用 MARL 把安全意识训进每个任务智能体；defender 必须检测、丢弃或净化被攻陷智能体引入的恶意内容，基于历史交互轨迹协同决策。
- 奖励设计：基于系统最终响应——safe +1 / unsafe −1；correct +0.5 / incorrect −0.5；联合促进 safety 与 helpfulness。
- defender 训练用 parameter sharing + GRPO（Group Relative Policy Optimization），含 clip 与 KL 惩罚（式1）。
- 进化攻击 (co-evolution)：为避免训练目标冲突，attacker 排除在 RL loop 外，但用生物进化思想——对攻击 prompt/策略做 mutation 与 crossover 生成变体，以攻击成功率为 fitness 做自然选择，成功变体保留并 seed 下一代，形成 attacker-defender 协同进化。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（基于 GRPO 的对抗-进化训练框架，无收敛/均衡理论证明）。

## 实验 (Experiments)
- **环境/Benchmark**: 红队数据集 JailBreakV-28K（280 mini）、HarmBench（multimodal split）、MultiJail（English split）；helpfulness：MATH（采样100）、Creative Writing；两种 MAS 设置：训练用链式三智能体、评估含层级式（jailbreak-prone 多模态 agent + 三个 benign 顺序判断）
- **Baselines**: 未训练的 MAS-1.5B / MAS-3B / MAS-7B（Qwen2.5-Instruct 系列）对比训练后的 1.5B / 3B
- **评估指标**: Attack Success Rate (ASR)（由 LLaMA-Guard-3-8B 判定 harmfulness）、MATH 准确率、Creative Writing 得分

## 主要结果 (Key Results)
- 训练后 MAS 在所有红队任务、各模型规模上安全性一致提升：1.5B 模型在 HarmBench 上 ASR 最多下降 22%。
- 训练后的 1.5B MAS 在安全性上持续优于 3B 对应版本，甚至在 JailBreakV 与 MultiJail 上超过未训练的 7B MAS——说明更大模型在 MAS 中并非天然更安全，原则性防御训练可媲美/超过模型放大。
- helpfulness 不降反升：trained 1.5B 在数学推理与创意写作上准确率最多提升 5 个百分点，缓解 safety-helpfulness 权衡。

## 局限与未来工作 (Limitations & Future Work)
- 自适应攻击者下训练稳定性问题。
- 向更大/更复杂系统扩展。
- 引入 memory 或外部知识以提升动态对抗环境下的长期鲁棒性。
- 攻击者不纳入 RL 优化，仅靠进化搜索，演化能力受限。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 在 LLM/MLLM 多智能体系统安全这一新兴方向，针对 jailbreak/prompt injection/恶意智能体传染等威胁，采用对抗训练 + co-evolution 范式，与"对抗智能体""通信攻击""安全约束""单点失效/容错"等主题相关。其"把防御内化到每个 agent 而非依赖外部 guard"的去中心化鲁棒性思路，是综述中 LLM-agent 安全分支的代表性工作。
