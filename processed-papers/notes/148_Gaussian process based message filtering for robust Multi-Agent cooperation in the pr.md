# 148. Gaussian Process Based Message Filtering for Robust Multi-Agent Cooperation in the Presence of Adversarial Communication

## 元信息 (Metadata)
- **标题**: Gaussian Process Based Message Filtering for Robust Multi-Agent Cooperation in the Presence of Adversarial Communication
- **作者**: Rupert Mitchell, Jan Blumenkamp, Amanda Prorok
- **机构**: University of Cambridge
- **发表**: arXiv 2020（arXiv:2012.00508）
- **链接/arXiv**: arXiv:2012.00508

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗/非合作通信（匿名智能体发送 faulty/misleading/manipulative 信息）
- **方法范式**: GNN 通信、Gaussian Process 概率建模、消息过滤（置信度加权）
- **关键词**: adversarial communication, GNN, Gaussian Process, message filtering, robust cooperation

## TL;DR（一句话总结）
在基于 GNN 的去中心化通信架构上提出一个 Gaussian Process 概率模型，利用智能体物理邻近与相对位置刻画不同智能体同时通信间的互信息，使每个智能体本地估计各通信伙伴"是否诚实"的后验置信度，并据此对消息加权过滤，抑制可疑通信对决策的影响。

## 问题与动机 (Problem & Motivation)
多智能体协作高度依赖通信，但为最优协作设计的通信协议对任一智能体的异常行为天然脆弱（故障、对抗攻击、Byzantine 串谋）。已有 GNN 通信工作几乎都假设完全合作、共享全局奖励，鲜有研究如何让学习到的通信策略对邻居的非合作/对抗通信鲁棒。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 匿名 non-cooperative agents 发送虚假/误导消息；论文按"对抗者可获得的信息量"建立非合作智能体 taxonomy（从弱到最强 informed）
- **设定**: cooperative；fully decentralized（GNN 多跳局部通信）；online

## 方法 (Method)
- GNN 通信架构：智能体为节点、连接为边、内部状态为图信号，多跳局部通信得到去中心化策略
- 提出 GP 概率模型刻画"因物理邻近/相对位置而产生的不同智能体同时通信之间的互信息"
- 由该模型本地计算各通信伙伴诚实的近似后验概率（confidence）
- 将 confidence 作为权重做 message filtering，压制可疑消息影响；对无对抗时性能影响可忽略

## 理论贡献 (Theoretical Contributions)
偏方法/概率建模：用 GP 给出可解析的"诚实度"后验作为过滤权重；无样本复杂度类形式化保证。

## 实验 (Experiments)
- **环境/Benchmark**: 两个不同的多智能体协作实验（覆盖所提非合作智能体 taxonomy）
- **Baselines**: 其它鲁棒通信/过滤方法
- **评估指标**: 不同 informed 程度对抗者下的任务性能、过滤对干净环境性能的开销

## 主要结果 (Key Results)
- 除"信息最充分"的对抗者外，过滤方法能把非合作智能体的影响降到几乎可忽略
- 在无对抗者时几乎不损失性能，体现"低开销"的实用性

## 局限与未来工作 (Limitations & Future Work)
对最强（fully informed）对抗者仍有残余影响；GP 互信息模型依赖物理邻近/位置假设，迁移到非几何拓扑场景需调整。

## 与综述的关联 (Relevance to Survey)
属 §4 通信鲁棒线中"基于置信度/可信度的消息过滤"代表作，被本语料 9× 引用，是 certified message / mutual-information 防御之外的概率推断式防御范式；与 [[blumenkamp2021emergence]]（同组对抗通信攻击）互补。
