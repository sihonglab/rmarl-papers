# 149. Adversarial Attacks On Multi-Agent Communication

## 元信息 (Metadata)
- **标题**: Adversarial Attacks On Multi-Agent Communication
- **作者**: James Tu, Tsunhsuan Wang, Jingkang Wang, Sivabalan Manivasagam, Mengye Ren, Raquel Urtasun
- **机构**: Waabi；University of Toronto；MIT（工作完成于 Uber ATG）
- **发表**: ICCV 2021；arXiv:2101.06560
- **链接/arXiv**: arXiv:2101.06560；doi:10.1109/ICCV48922.2021.00767

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗通信攻击（对学习到的中间表示 learned intermediate representations 施加不可察觉扰动）
- **方法范式**: 对抗攻击、神经网络表示扰动、黑盒迁移攻击 + 域适配
- **关键词**: adversarial attack, learned communication, intermediate representation, black-box transfer, autonomous driving

## TL;DR（一句话总结）
研究"以共享神经网络中间表示进行通信"的协作多智能体（如自动驾驶 V2X 感知）在表示级的对抗脆弱性，证明一个不可分辨的对抗消息即可严重降级性能，但随良性智能体增多而减弱；并指出此设定下黑盒迁移攻击更难，需用域适配对齐表示分布。

## 问题与动机 (Problem & Motivation)
现代自治系统大规模部署后将形成协作多智能体系统，通过共享信息提升感知/效率（如车队多视角感知提升安全）。但通信依赖使共享信息可被恶意篡改，而其底层深度网络本就易受对抗攻击；攻击者即便能发任意消息，最危险的是与良性消息不可分辨的微小扰动。需在神经网络层面评估并增强这类系统的鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者篡改某智能体发送的 learned representation 消息，注入不可察觉的对抗扰动；含白盒与黑盒迁移两种
- **设定**: cooperative（共享中间表示通信）；以自动驾驶协作感知为应用；评估期攻击（test-time）

## 方法 (Method)
- 形式化"以共享中间表示通信"这一新颖设定下的对抗攻击
- 构造与良性消息不可分辨的对抗消息，扰动接收方网络输出
- 分析黑盒迁移攻击：直接扰动输入更易，扰动学习表示需用 **domain adaptation** 对齐受害者表示分布才能迁移
- 探讨良性智能体数量对攻击强度的削弱作用，提出在 NN 层面增加容错的安全视角

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（系统性攻击实验与分析），给出"表示级攻击随良性体增多而减弱""黑盒迁移需域适配"等经验性结论。

## 实验 (Experiments)
- **环境/Benchmark**: 协作自动驾驶感知（多智能体共享中间表示，V2X/车队多视角）
- **Baselines**: 直接输入扰动攻击、无攻击
- **评估指标**: 任务性能降级幅度、攻击不可分辨性、随智能体数变化、黑盒迁移成功率

## 主要结果 (Key Results)
- 单个不可分辨对抗消息即可显著降级协作感知性能
- 攻击强度随良性智能体数增多而下降；黑盒迁移在表示级显著更难，需域适配
- 倡导在神经网络层面为多智能体系统增加一层容错/安全防护

## 局限与未来工作 (Limitations & Future Work)
聚焦攻击与脆弱性揭示，未提供完善防御；评估集中于自动驾驶感知任务；防御（认证/过滤）留作后续。

## 与综述的关联 (Relevance to Survey)
属 §4 通信鲁棒/§3 对抗攻击交叉的奠基性攻击工作（被本语料 7× 引用），把"learned communication 的表示级对抗脆弱性"引入 MARL/协作感知，是后续 certified message / message filtering 防御（[[mitchell2020gaussian]] 等）的威胁模型来源之一。
