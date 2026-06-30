# 182. Robust and Diverse Multi-Agent Learning via Rational Policy Gradient

## 元信息 (Metadata)
- **标题**: Robust and Diverse Multi-Agent Learning via Rational Policy Gradient
- **作者**: Niklas Lauffer, Ameesh Shah, Micah Carroll, Sanjit A. Seshia, Stuart Russell, Michael Dennis
- **机构**: UC Berkeley；Google DeepMind
- **发表**: NeurIPS 2025
- **链接/arXiv**: rational-policy-gradient.github.io；github.com/niklaslauffer/rational-policy-gradient

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对队友/对手策略多样性的脆弱性（partner/strategy 不确定）、对抗优化下的 self-sabotage；目标是 robust + diverse policy
- **方法范式**: adversarial optimization、rational policy gradient、opponent shaping、博弈论理性约束 (best-response)
- **关键词**: rational policy gradient, adversarial optimization, self-sabotage, opponent shaping, cooperative MARL, policy diversity

## TL;DR（一句话总结）
针对 adversarial optimization 在合作/general-sum 场景下因激励最小化他人收益而导致 self-sabotage（智能体非理性破坏任务）的失败模式，提出 Rationality-preserving Policy Optimization (RPO) 形式化与求解算法 Rational Policy Gradient (RPG)，通过引入 manipulator 智能体与 opponent shaping，使智能体在保持 rational（对某个可能队友策略最优）的前提下优化对抗目标，从而在合作环境中安全地获得 robust 与 diverse 策略。

## 问题与动机 (Problem & Motivation)
对抗优化（显式搜索策略缺陷）在 zero-sum 下通过 self-play 能自然带来鲁棒化，但在合作/general-sum 下天真应用会失败：若智能体仅被激励最小化队友收益，adversary 会直接拒绝合作甚至主动破坏队友（及自身）收益，阻断有意义的学习——即 self-sabotage。这使对抗优化无法直接用于合作设定下寻找鲁棒、可适应、diverse 的策略，cross-play 多样性算法也受此困扰（公开难题）。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 队友/对手可能采取多种策略；对抗目标显式最小化他人收益以暴露缺陷，但要求 adversary 策略必须 rational（对至少一个可能 co-policy 是 best-response），排除非理性 self-sabotage
- **设定**: general-sum partially-observable stochastic game（含 cooperative 与 general-sum）；两玩家为主；策略梯度 / 深度学习；含 base agents 与训练后丢弃的 manipulators

## 方法 (Method)
- 提出 RPO 形式化：在对抗优化目标 O_i 上加 rationality 约束——存在某个 co-policy 使 π_i 为 best-response
- RPG 求解：为每个 base agent 引入一个 manipulator，base agent 只在其 manipulator environment 中最大化自身收益（确保 rational）
- 每个 manipulator 用 opponent shaping 操纵 base agent 的学习，引导其走向优化对抗目标（如在原 base 环境中与队友取得低收益）的策略
- 训练后丢弃 manipulators，训练好的 base agents 即为 RPO 版对抗目标的解；用 RPG 扩展出 5 种新的对抗优化算法（找 rational adversarial examples、训练鲁棒策略、学习多样策略）

## 理论贡献 (Theoretical Contributions)
形式化 self-sabotage 与 RPO（rationality 即 best-response 约束）；给出将难以直接整合的 rationality 约束转化为可用梯度优化的 RPG 构造。偏方法/形式化，配合实证验证。

## 实验 (Experiments)
- **环境/Benchmark**: 多个常用 cooperative 与 general-sum 环境（含矩阵博弈示例、Overcooked 类协作任务等）
- **Baselines**: 既有 adversarial training / cross-play diversity 算法（受 self-sabotage 困扰者）
- **评估指标**: 是否避免 self-sabotage、鲁棒性、可适应性、策略多样性、与既有 baseline 的性能比较

## 主要结果 (Key Results)
- RPG 彻底消除既有 cross-play 多样性算法中的 self-sabotaging 行为，解决该公开难题
- 在多个流行合作环境中性能超越既有 baseline，同时能找到 rational adversarial examples、训练更鲁棒的策略并学习 diverse 策略
- 证明对抗优化的好处可在不引发 self-sabotage 的前提下迁移到 general-sum / cooperative 设定

## 局限与未来工作 (Limitations & Future Work)
形式化与实验主要限于两玩家；引入 manipulator 带来额外训练成本；opponent shaping 的稳定性与可扩展到更多智能体 / 更大环境仍待验证。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[对抗智能体 / adversarial optimization]] 与 [[策略多样性 / population-based robustness]] 交叉的代表性工作，把 zero-sum 对抗鲁棒化方法安全推广到合作设定，与 ad-hoc teamwork、partner robustness、[[opponent shaping]] 主题相关，是合作 MARL 鲁棒性与多样性的统一框架。
