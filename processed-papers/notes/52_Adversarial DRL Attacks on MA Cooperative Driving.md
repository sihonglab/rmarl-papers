# 52. Adversarial Deep Reinforcement Learning Attacks on Multi-Agent Autonomous Cooperative Driving Policies

## 元信息 (Metadata)
- **标题**: Adversarial Deep Reinforcement Learning Attacks on Multi-Agent Autonomous Cooperative Driving Policies
- **作者**: Ahmed Alzubaidi, Ameena S. Al-Sumaiti, Majid Khonji
- **机构**: Khalifa University, Abu Dhabi, UAE（Smart OR Lab / KUCARS Center）
- **发表**: IET Intelligent Transport Systems 2025（Vol. 19, e70066）
- **链接/arXiv**: https://doi.org/10.1049/itr2.70066

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体（环境操纵型 environment manipulation，对抗 CAV 注入到合作车队中）
- **方法范式**: 对抗策略训练（A-DRL）+ 对抗训练防御（同质 / 异质 / 课程学习）
- **关键词**: MARL, connected autonomous vehicles, adversarial attack, cooperative driving, adversarial training

## TL;DR（一句话总结）
针对 MARL 训练的合作自动驾驶（CD-MARL）策略，作者训练了两个对抗 CAV（碰撞型 advc 与降速型 advs）暴露其脆弱性，并用多种对抗训练方法提升受害策略的鲁棒性。

## 问题与动机 (Problem & Motivation)
MARL 已广泛用于连接自动车（CAV）合作驾驶，但继承了深度学习模型对对抗攻击的脆弱性。已有文献尚未探究 MARL 训练的合作驾驶策略在部署中遭遇对抗行为时的鲁棒性。论文围绕两个研究问题：RQ-1 CD-MARL 策略是否易受对抗攻击；RQ-2 若是，何种防御可提升鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击方式为环境操纵（environment manipulation）——一辆对抗 CAV 与正常 CAV 共存于 on-ramp merging 场景，常规车无法区分对抗车与正常车；black-box 攻击（攻击者不知受害模型权重）；攻击者仅能在共享环境中执行动作，无法访问他车传感/执行器。两类对抗目标：safety-attacker (advc, 最大化碰撞) 与 speed-attacker (advs, 最小化邻车平均速度)。
- **设定**: cooperative；CTDE（受害策略用 parameter-sharing MA2C 训练）；对抗策略为单智能体 A2C；online

## 方法 (Method)
- 受害策略 πvc：复现 Chen et al. 的 on-ramp merging 合作 MARL 策略（MA2C + priority-based safety supervisor，POMDP 建模）。
- 攻击：将攻击建模为单智能体 MDP，用 A2C 训练对抗 CAV；状态含邻车 presence/position/speed 向量，动作为 5 个高层决策（变道/加减速/idle），advc 奖励为邻车碰撞数，advs 奖励为邻车速度效率的负值。
- 防御——对抗训练三种方案：(1) Homogeneous（仅对单一对抗体重训，得 πhmc/πhms）；(2) Heterogeneous（每回合随机选 advc 或 advs，得 πht）；(3) Curriculum learning（两阶段依次暴露不同对抗体，得 πclc/πcls）。
- 环境用 Highway-env 模拟，6 辆车其中 1 辆为对抗体。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。

## 实验 (Experiments)
- **环境/Benchmark**: Highway-env on-ramp merging；三个环境：adv-fr-env（无对抗）、adv-co-env（含 advc）、adv-sp-env（含 advs）。
- **Baselines**: 原始受害策略 πvc 与各对抗训练变体相互对照。
- **评估指标**: cumulative global reward (cg)、cumulative regional reward (cr)、collision-free rate (co)、time to collision (tc)、average speed (avg)。

## 主要结果 (Key Results)
- 攻击有效：advc 将碰撞率从 0% 升至 62%、cg 从约 74 降至 26；advs 将平均速度从 25 m/s 降至 21.73 m/s，cg 降至 47.58。证实 CD-MARL 策略脆弱（RQ-1 成立）。
- 同质对抗训练对已见对抗体有效：πhmc 将对 advc 的碰撞率减半（62%→28%），πhms 面对 advs 实现 0% 碰撞，且在无对抗场景几乎不损失性能。
- 泛化失败：πhmc/πhms 无法应对未见过的另一类对抗体；异质（πht）与课程学习策略均未得到可靠的通用鲁棒策略，πht 表现最差，甚至在无对抗场景也退化。

## 局限与未来工作 (Limitations & Future Work)
未能训练出对未见类型对抗体鲁棒的策略；advc 可制造不可避免的碰撞场景；通用化（异质/课程）方法效果不佳。未来方向为 CAV 安全中更强的可泛化防御。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗智能体 / adversarial policy 攻击 + 对抗训练防御"主题，应用领域为自动驾驶合作驾驶；与 Gleave et al. 对抗策略、Sharif et al. MARL 驾驶攻击等工作同线，体现攻击-防御实证范式而非理论鲁棒。
