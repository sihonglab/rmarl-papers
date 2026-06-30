# 17. Adaptive Robust Estimator for Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Adaptive Robust Estimator for Multi-Agent Reinforcement Learning
- **作者**: Zhongyi Li, Wan Tian (equal); Jingyu Chen, Kangyao Huang, Huiming Zhang, Hui Yang, Tao Ren, Jinyang Jiang, Yijie Peng, Yikun Ban, Fuzhen Zhuang 等
- **机构**: Beihang University, Peking University, Chinese Academy of Sciences, Tsinghua University
- **发表**: Preprint, 2026（arXiv:2603.21574）
- **链接/arXiv**: arXiv:2603.21574v1; 代码 https://github.com/bhai114/ARE

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 奖励噪声/污染（noisy, biased, heavy-tailed rewards，含极端 outlier、Cauchy 噪声）；奖励投毒/污染（contamination）
- **方法范式**: 鲁棒统计（Median-of-Means 改进、adaptive robust loss）、robust policy optimization（GRPO 改造）、多智能体协作推理协议
- **关键词**: robust estimator, heavy-tailed rewards, GRPO, multi-agent LLM reasoning, median-of-means, advantage normalization

## TL;DR（一句话总结）
本文针对 LLM 多智能体协作推理中奖励噪声/重尾导致 GRPO 优势归一化不稳定的问题，提出 DACR 协作协议 + ARE（自适应鲁棒估计器，改进 Median-of-Means 用自适应损失替换块内均值）来鲁棒估计 batch 均值，从而稳定多智能体策略优化。

## 问题与动机 (Problem & Motivation)
用 MARL 训练协作 LLM 推理系统面临两大脆弱性：(1) 交互层面歧义（生成/批评/修订混杂）使跨 agent 信用分配困难；(2) 奖励信号常由 verifier / reward model / 启发式打分产生，噪声大、有偏、重尾且偶有极端离群，GRPO 用 batch 经验均值方差归一化奖励，少数异常样本会扭曲 batch 统计与 advantage scaling，触发振荡甚至训练发散。多智能体交互进一步引入方差与非平稳性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 奖励分布重尾/受污染；实验注入 heavy-tailed peaked Cauchy 噪声，并测试 group-level 与 within-group 两种污染模式（不同污染组比例、组内污染率）。统计假设：有限方差或仅 (1+ϵ)-moment 重尾。
- **设定**: cooperative（双智能体协作推理）；online policy optimization（GRPO 风格）；同质与异质 agent 对

## 方法 (Method)
- DACR（Dual-Agent Answer–Critique–Rewrite）：将协作推理分解为三阶段——独立作答、互相批评（交换答案给出 critique）、基于反馈修订；评估信号外置于原推理链。
- Cross-Evaluation Reward：阶段奖励 R_ans、R_rw 加上 cross-improvement 项 Δ_i（critique 使对方修订答案提升的边际量），总回报 R_total_i = R_rw,i + γΔ_i，实现可解释的信用分配。
- ARE：改进 Median-of-Means——将样本分块，每块通过最小化 adaptive robust loss（Barron 2019）得到鲁棒位置估计（块内也鲁棒），再对块估计取中位数；用交替优化估计形状/尺度参数 (α,c)，并用 GNC + IRLS（Black-Rangarajan 对偶、outlier-process 正则）求解非凸子问题。
- 用 ARE 的鲁棒位置估计 μ̃_B 替换 GRPO 的 batch 均值，得到鲁棒 advantage A^ARE = (R_total−μ̃_B)/(σ_B+ϵ)，再做 clipped surrogate + KL 优化。

## 理论贡献 (Theoretical Contributions)
- 有限方差情形（Thm 5.3）：central-root 估计器一致且渐近正态，达经典 √m 速率。
- 重尾情形（Thm 5.5）：仅假设 (1+ϵ)-moment，单块估计器达 (log(1/δ)/m)^{ϵ/(1+ϵ)} 高概率偏差界。
- ARE 聚合渐近理论（Thm 5.6）：√n 收敛，相对样本均值的渐近相对效率为 2/π。
- Thm 5.7：重尾下 MoM 聚合的高概率偏差界。Lemma 4.1：关于 α 单调性，说明直接优化 α 病态需似然校准。

## 实验 (Experiments)
- **环境/Benchmark**: 数学推理（训练 MATH 7.5k，测试 MATH500 (ID)；AMC23、Gaokao2023en、MinervaMath、AIME24/25 (OOD)）；具身 aerial VLN（基于 FlightGPT，Qwen2-VL-2B）
- **Baselines**: 标准 GRPO（同协作设定但用 GRPO 替代 ARE/DACR）；base model；FlightGPT
- **评估指标**: 数学推理 accuracy；训练稳定性/reward 曲线；VLN 的 NE / SR / OSR / SPL

## 主要结果 (Key Results)
- 注入重尾 Cauchy 奖励噪声下，ARE 在 ID/OOD 上一致超 GRPO baseline；如 AMC23 上 Qwen2.5-1.5B 从 22.5%→32.5% (+10%)。
- 三阶段交互消融有效：AMC23 上 Qwen2.5-7B 从 47.5%→60% (+12.5%)。
- 多种污染模式下性能优雅退化，鲁棒性持续优于 baseline。
- VLN 中以 ARE 替换 GRPO，训练奖励更高，NE/SR/OSR/SPL 全面提升，未见环境增益最大（如 val-unseen NE 145.56→124.38）。

## 局限与未来工作 (Limitations & Future Work)
- VLN 实验仅验证 ARE 组件、用了较小 backbone 与降分辨率，未做完整多智能体交互（留作未来工作）；DACR 限于双智能体；理论限于 α∈(0,1] 与特定调参。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"奖励噪声/重尾鲁棒 + 鲁棒统计估计"线路，并把 robust MARL 拓展到 LLM 多智能体协作推理这一新兴场景；与 reward poisoning/contamination、robust policy optimization、credit assignment、heavy-tailed estimation（MoM）等主题相关，是连接鲁棒统计与 MARL/LLM-RL 的代表工作。
