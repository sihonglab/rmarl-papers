# 50. Finding the Weakest Link: Adversarial Attack against Multi-Agent Communications

## 元信息 (Metadata)
- **标题**: Finding the Weakest Link: Adversarial Attack against Multi-Agent Communications
- **作者**: Maxwell Standen, Junae Kim, Claudia Szabo
- **机构**: The University of Adelaide, Australia; DST Group (Defence Science and Technology), Australia
- **发表**: 未明确（arXiv preprint，arXiv:2605.13170v1, 2026）
- **链接/arXiv**: arXiv:2605.13170v1 [cs.LG]

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击（communication perturbation attack，扰动 agent 间传递的消息）
- **方法范式**: 白盒梯度攻击、Jacobian saliency（JSMA 扩展）、attack tempo（何时攻击）、victim/message 选择、新型对抗损失函数
- **关键词**: adversarial attack, multi-agent communications, MARL robustness, Jacobian saliency, attack tempo, single-victim attack

## TL;DR（一句话总结）
研究针对 MARL 通信的单受害者扰动攻击，提出用基于 Jacobian 的梯度幅值识别"最薄弱环节"——最易受攻击且影响最大的消息、agent 和时步（where/who/when），并设计 weighted-loss 与 maximum-loss 两种对抗损失在攻击成功率与影响间权衡，从而显著增强攻击有效性。

## 问题与动机 (Problem & Motivation)
多智能体系统依赖通信协调，学习到的通信协议（MARL-Comms）在带宽/噪声上更高效但暴露攻击面。现有通信扰动攻击效率低：(1) 任意选择要扰动的消息（where）或只针对少 agent 系统；(2) "何时攻击"（tempo）仅在单智能体系统研究过；(3) "攻击谁"（who）在 MARL AML 攻击中从未被研究；(4) 高影响攻击常依赖昂贵的深度 RL。本文系统填补 where/who/when 三个空白以理解并评估通信鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: single-victim communication attack——攻击者拦截并扰动单个 agent 收到的消息；白盒（已知目标系统/可计算梯度）；受 attack rate / tempo 约束。区别于注入恶意新消息的攻击。
- **设定**: cooperative MARL with learnt communication；针对已训练系统的测试/攻击阶段

## 方法 (Method)
1. **Where-to-attack（消息选择）**: 扩展 JSMA，将 Jacobian 对自定义损失求梯度，用梯度幅值做 ranked message selection 选 top-k 最具影响力的消息扰动。
2. **Who-to-attack（victim 选择）**: 用消息梯度幅值识别最易受攻击的 agent；并把单智能体 tempo 方法扩展为 victim 选择函数。
3. **When-to-attack（tempo）**: 利用白盒知识扩展现有 tempo 方法（CBTS、MMR、ML、NS、VL、ST）到多智能体域，决定攻击时机。
4. **两种损失**: weighted-loss 同时优化攻击影响与成功概率；maximum-loss 牺牲成功率换取更大系统影响；二者均改进基础 untargeted loss 的缺陷。无需训练深度 RL。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证

## 实验 (Experiments)
- **环境/Benchmark**: navigation、PredatorPrey（PP-O / PP-D）、TrafficJunction（small / large）；攻击两种通信方法（RIAL、CommNet 类）
- **Baselines**: 不使用本文方法的 baseline 攻击，采用 tempo 方法 CBTS、MMR、ML、NS、VL、ST 作 tempo 与 victim 选择 + 随机消息选择
- **评估指标**: 任务指标（navigation 完成比例、TrafficJunction 碰撞数等）随 attack rate 的下降幅度；clean 性能对照；共 30 个场景

## 主要结果 (Key Results)
1. ranked message selection 在 30 个场景中的 29 个达到与随机消息选择相当或更大的影响。
2. victim/message 选择、tempo、损失函数组合在约半数（30 个中 15 个）场景显著提升攻击有效性，尤其在更复杂环境和更鲁棒通信方法上。
3. 不同环境/通信方法下最优组合不同（如 navigation 用 ranked + weighted/maximum loss；TrafficJunction 用 maximum/weighted loss），并据此揭示通信方法与环境属性如何影响 c-MARL 鲁棒性。

## 局限与未来工作 (Limitations & Future Work)
白盒假设较强；结论可能不适用于其他环境配置；攻击效果依赖 tempo 函数表现；为攻击/评估工作而非防御。未来可深化对 tempo 函数的理解并发展相应防御缓解措施。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"通信攻击 / 通信鲁棒性"主线，首次系统处理通信攻击的 where/who/when 三要素，可作为评估学习型多智能体通信脆弱性的攻击基准；与 inter-agent communication 攻击、attack tempo、saliency-based 对抗攻击等工作相关。
