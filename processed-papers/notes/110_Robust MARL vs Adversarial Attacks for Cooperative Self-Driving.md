# 110. Robust Multi-Agent Reinforcement Learning Against Adversarial Attacks for Cooperative Self-Driving Vehicles

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning Against Adversarial Attacks for Cooperative Self-Driving Vehicles
- **作者**: Chuyao Wang, Ziwei Wang, Nabil Aouf
- **机构**: Department of Engineering, City St George's, University of London, UK
- **发表**: IET Radar, Sonar & Navigation, 2025; 19:e70033（Open Access）
- **链接/arXiv**: https://doi.org/10.1049/rsn2.70033

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（white-box 对抗攻击，亦涵盖传感器误差/域转移），属安全关键的对抗攻击
- **方法范式**: 对抗训练 (FGSM 迭代)、Mean-Field theory、risk 估计网络、constrained optimization (CBF 思路) + 散度正则、Stochastic Game with perturbation
- **关键词**: cooperative self-driving, adversarial attack, observation perturbation, mean-field, risk minimisation, constrained MARL

## TL;DR（一句话总结）
针对协作自动驾驶 MARL 易受观测扰动攻击的问题，提出 R-CCMARL（robust constrained cooperative MARL）：用 universal policy + Mean-Field 共享观测建模交互，配合风险估计网络与带正则的约束优化目标，在最坏情况下最小化长期碰撞风险并最大化回报，在 CARLA 路口场景下对状态扰动保持鲁棒。

## 问题与动机 (Problem & Motivation)
MARL 提升了自动驾驶多车协调与性能，但对未预料的对抗攻击脆弱：被扰动的观测会使一辆或多辆车做出关键错误决策，引发连锁碰撞。现有方法多基于局部观测训练、缺乏全局系统意识；CTDE 可能退化为多个单智能体；且多采用 task-specific 策略（如只会左转），不适合需要通用驾驶能力的自动驾驶。同时安全攸关，需要对对抗攻击及不可避免的传感器误差/域转移都鲁棒。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: white-box 对抗者，完全访问 RL 模型参数，基于 FGSM 并结合 collision-risk 最大化生成扰动；用迭代 FGSM（而非单纯增大 ε）降低对抗样本可见性（如 ε=0.1, iter=20）；将多智能体路口通行建模为 Stochastic Game with perturbation。
- **设定**: cooperative；共享观测 + Mean-Field（全局状态与交互意识）；universal policy（非 task-oriented）；对抗训练 online

## 方法 (Method)
1. 构造 white-box 最优对抗生成器（FGSM 迭代 + collision risk 最大化）产生扰动观测作为鲁棒训练样本。
2. 每个 agent 使用 universal policy，并用 Mean-Field theory 支持的信息共享结构整合共享观测，建模 MARL 交互、获得全局意识。
3. 提出 risk formulation 与 risk estimation network，最小化定义的长期风险；该 risk estimator 同时作为 control barrier function 容忍有界扰动并以 safety reward 反馈塑形策略。
4. 用风险估计构建带 regulariser 的约束优化目标，在最坏情况下最大化长期回报；散度型正则项模拟非对抗状态与对抗状态间的性能差距。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（将问题形式化为 Stochastic Game with perturbation，并用 CBF 思路容忍有界扰动，但无收敛/认证半径等新定理）

## 实验 (Experiments)
- **环境/Benchmark**: CARLA simulator，多车 intersection（路口通行/协商）场景
- **Baselines**: MAPPO（非鲁棒）、risk-only 模型（去约束的消融）、ERNIE 等鲁棒方法
- **评估指标**: 长期/累计 team reward、collision risk（team risk per agent），在 normal 与多种 attack 场景（含 attack on 指定 agent）对比

## 主要结果 (Key Results)
- R-CCMARL 在无攻击与有攻击下均保持高性能，累计回报显著优于 MAPPO（如某场景 168.6 vs MAPPO 116.4，约 +44.8%）。
- 团队回报在攻击下比 ERNIE 高约 25%（159.90 vs 127.85）；R-CCMARL 在各攻击场景下风险最低（如把 Agent 风险从 MAPPO 的 -9.89 降到约 -6.97）。
- 消融显示 risk-only 模型在重攻击下也优于 MAPPO，但完整的约束优化 R-CCMARL 最鲁棒，验证风险最小化模块与约束优化的作用。

## 局限与未来工作 (Limitations & Future Work)
评估限于 CARLA 路口场景与 FGSM 类白盒攻击；Mean-Field 近似与 universal policy 假设。未来可扩展到更多样攻击类型、更复杂交通与真实部署（正文未详尽列出）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的"状态/观测对抗扰动 + 安全约束"应用线（cooperative 自动驾驶），结合对抗训练 (FGSM)、Mean-Field 交互建模与风险敏感约束优化，关联 state-adversarial robust RL、risk-sensitive/constrained MARL 与自动驾驶鲁棒决策主题。
