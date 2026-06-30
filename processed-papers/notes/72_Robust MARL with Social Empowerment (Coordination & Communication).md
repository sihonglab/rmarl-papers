# 72. Robust Multi-Agent Reinforcement Learning with Social Empowerment for Coordination and Communication

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning with Social Empowerment for Coordination and Communication
- **作者**: Tessa van der Heiden, Herke van Hoof, Efstratios Gavves, Christoph Salge
- **机构**: BMW Group；University of Amsterdam；University of Hertfordshire
- **发表**: arXiv 2020（arXiv:2012.08255v1，2020年12月，cs.MA）；未明确正式 venue
- **链接/arXiv**: arXiv:2012.08255 ；代码 https://github.com/tessavdheiden/social_empowerment

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 训练伙伴行为变化 / 对 partner 策略的过拟合（overfitting to training partners），即对队友策略扰动的鲁棒性
- **方法范式**: 内在社会动机（intrinsic social motivation）、信息论 empowerment（transfer / joint empowerment）、额外奖励项、CTDE、variational lower bound (MI 估计)
- **关键词**: social empowerment, transfer empowerment, intrinsic motivation, robust MARL, coordination, mutual information

## TL;DR（一句话总结）
针对集中式训练的 MARL agent 易对训练伙伴过拟合（假设而非反应队友行为）的脆弱性，提出将 social empowerment（量化智能体动作间潜在因果影响/信道容量）作为额外奖励项，引导学习出对队友行为保持反应性（reactive）的鲁棒协作策略。

## 问题与动机 (Problem & Motivation)
MARL（尤其集中式训练）的 agent 常采用"期望队友以特定方式行动"而非"观察并反应队友动作"的策略，导致当队友改变策略或换新伙伴时失败（缺乏鲁棒性）。希望引入一个额外奖励将学习偏向"社会反应性"策略，且需满足：(1) 普适——只需最小改动即可适配不同 sensor-actuator 配置；(2) 不损害性能——找到好策略后不干扰 exploitation。优化动作间实际互信息（如 social influence）要求策略保持一定熵，可能干扰 exploitation；empowerment 用潜在信息流可避免该限制。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非对抗性。鲁棒性定义为训练 agent 应对其他 agent 行为变化的能力（one-shot adaptation：队友改策略时能快速适应）。训练过程中所有 agent 同时改策略本身构成扰动。
- **设定**: cooperative（共享 reward）；Dec-POMDP；CTDE（训练时可用所有 agent 局部观测，执行时去中心化）；online

## 方法 (Method)
- **Transfer empowerment（成对）**: ET,k→j(st)=max_ωk I[a^j_{t+1}, a^k_t | st]，量化 agent k 动作对 agent j 后续动作的潜在因果影响（信道容量），鼓励 j 对 k 反应。本文用"对另一 agent 动作"（而非 sensor state）的 empowerment，更聚焦影响其决策。多 agent 扩展 ET,1:n→j = Σ ET,i→j，按 agent 数平方增长。
- **Joint empowerment（可扩展代理）**: EJ(st)=max_ω I[s_{t+1}, a_t | st]，所有 agent 联合动作对未来状态的因果影响；线性扩展、是各 agent self-empowerment 的上界，favor 保持群体可操作性/可控性的策略。
- **奖励修改**: R_{i,t}=r(a_t,s_t)+E(s_{t+1})，E 取 ET 或 EJ。empowerment 不关心反应"好不好"，与环境奖励结合可在解决任务的同时避免非反应性脆弱。
- **估计**: 连续动作-状态空间下用 Barber-Agakov 变分下界（源分布 ω + 规划分布 q 的变分近似 + 转移网络 p），神经网络表示并梯度上升；基于 DDPG/MADDPG 框架训练（Algorithm 1/2）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（使用 empowerment 的互信息变分下界估计，joint empowerment 为 self-empowerment 上界，但无收敛/鲁棒性形式化保证）。

## 实验 (Experiments)
- **环境/Benchmark**: OpenAI Multi-Agent Particle Environment——(I) Cooperative Communication / Speaker-Listener（L landmarks, C symbols, O obstacles）、(II) Cooperative Navigation / Cover Landmarks（3 agents）；(III) 多智能体自动驾驶模拟器（merge/避障，4 帧灰度图观测）
- **Baselines**: DDPG、MADDPG、Social Influence (SI, Jaques et al. 2019)；本文 ET、EJ
- **评估指标**: reward、平均距离、target reach %、obstacle hit %、collisions %、success %

## 主要结果 (Key Results)
- 训练曲线：加 empowerment 作额外效用后平均回报更高、学习更快。
- Speaker-Listener（L=6,C=5,O=6）：ET,k→j 取得最低障碍碰撞（31.1%）和最高 target reach（61.1%），优于 MADDPG/SI/DDPG，因 listener 学会反应消息更好地解码导航。
- Cooperative Navigation：EJ 取得最低碰撞率（13.3%）和最高成功率（95.9%，ET 89.9% 次之），显著优于 MADDPG（53.3% 碰撞 / 80.5% 成功）；EJ 避开机动性低的状态。
- Cooperative Driving：EJ 在 off-road、collisions、obstacle hit 各项均优于 MADDPG，车辆反应更快、主动让行。

## 局限与未来工作 (Limitations & Future Work)
未与训练中未见过的伙伴（如人类）协作（zero-shot 未探索）；transfer empowerment 成对计算随 agent 数平方增长（用 joint empowerment 缓解）；竞争场景可通过最小化对手 empowerment 训练（未实现）。未来：与未见伙伴/人类协作、竞争性场景的 empowerment 最小化。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"对队友/伙伴策略扰动鲁棒 + 内在动机/信息论正则"主题线，与 social influence、mutual information regularization（如 MIR2/MIR3 #31）思路相关但用 empowerment（潜在信息流/信道容量）替代实际互信息以避免干扰 exploitation。可与 population-based training、minimax MARL、zero-shot coordination（Other-Play）等"partner robustness"工作对照，提供一种通用、可扩展的协调鲁棒性内在奖励。
