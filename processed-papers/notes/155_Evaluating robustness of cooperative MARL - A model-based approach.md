# 155. Evaluating Robustness of Cooperative MARL: A Model-Based Approach

## 元信息 (Metadata)
- **标题**: Evaluating Robustness of Cooperative MARL: A Model-Based Approach (c-MBA)
- **作者**: Nhan H. Pham, Lam M. Nguyen, Jie Chen, Hoang Thanh Lam, Subhro Das, Tsui-Wei Weng
- **机构**: IBM Research / UNC；MIT-IBM Watson AI Lab；UC San Diego 等
- **发表**: arXiv:2202.03558（ICLR 2023 投稿版）
- **链接/arXiv**: arXiv:2202.03558

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗状态扰动（评估 c-MARL 鲁棒性的攻击）
- **方法范式**: model-based 对抗攻击、victim-agent 选择、data-driven targeted failure state
- **关键词**: c-MARL robustness evaluation, model-based attack, state perturbation, victim selection, targeted failure

## TL;DR（一句话总结）
提出用 **model-based** 方法 c-MBA 评估合作 MARL 的对抗鲁棒性，能比已有 model-free 方法构造更强的对抗状态扰动以降低团队总回报，并首次给出 victim-agent 选择策略与 data-driven 的目标失败状态定义，无需环境专家知识即可发动更强攻击。

## 问题与动机 (Problem & Motivation)
合作 MARL (c-MARL) 方法激增，但其对对抗攻击的鲁棒性鲜被探究。已有 DRL 攻击多针对单智能体、且多为 model-free；如何系统、强力地评估 c-MARL 在对抗状态扰动下的最坏团队表现仍缺方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对（部分）智能体观测/状态施加对抗扰动，目标是最小化团队总回报
- **设定**: cooperative；test-time 评估性攻击；model-based（用学到的动力学模型）

## 方法 (Method)
- **c-MBA**：基于学习到的环境动力学模型构造对抗状态扰动，比 model-free 攻击更强
- **Victim-agent 选择**：首个选择攻击哪个/哪些智能体的策略，以最大化破坏
- **Data-driven targeted failure state**：用数据定义目标失败状态，引导扰动方向，无需环境专家知识
- 在两个代表性 MARL benchmark 上对比 model-free 基线

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（攻击/评估方法），提供更紧的"最坏团队表现"评估手段。

## 实验 (Experiments)
- **环境/Benchmark**: 两个代表性 MARL benchmark（合作任务）
- **Baselines**: model-free 对抗攻击方法
- **评估指标**: 团队总回报下降幅度、攻击强度、跨环境一致性

## 主要结果 (Key Results)
- c-MBA 在所有测试环境上一致优于 model-free 基线，造成更大团队回报下降
- victim 选择 + 目标失败状态进一步增强攻击，且不依赖环境专家知识

## 局限与未来工作 (Limitations & Future Work)
依赖学习动力学模型的质量；聚焦攻击/评估，未提供配套鲁棒训练防御；benchmark 规模有限。

## 与综述的关联 (Relevance to Survey)
属 §8 Benchmark/测评（兼 §3 攻击）中"以更强攻击度量 c-MARL 鲁棒性"的代表（被本语料 5× 引用），为 robust c-MARL 提供 model-based 评估基线；与 [[59_On the Robustness of Cooperative MARL]]、[[99_Towards Comprehensive Testing on the Robustness of Cooperative MARL]] 等鲁棒性测评工作对照。
