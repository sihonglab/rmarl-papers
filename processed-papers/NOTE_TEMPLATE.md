# 标准化论文笔记模板（Robust MARL Survey）

> 每篇论文一个笔记文件，文件名与文本文件同名（`<编号>_<标题>.md`），存于 `processed-papers/notes/`。
> 严格按以下结构填写。无法从全文确定的字段填 `未明确`，不要编造。技术术语保留英文。

---

```markdown
# <编号>. <论文标题>

## 元信息 (Metadata)
- **标题**: 
- **作者**: （前几位 + et al.）
- **机构**: 
- **发表**: <venue> <年份>（无法确定填 `未明确`）
- **链接/arXiv**: （正文中若有则填，否则 `未明确`）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: （如：环境/模型不确定性、状态/观测扰动、动作扰动、对抗智能体、通信攻击、Byzantine/容错、奖励投毒、智能体失效、安全约束 等）
- **方法范式**: （如：DRMG 理论、对抗训练、minimax、价值分解、认证鲁棒、风险敏感、课程学习、博弈论均衡 等）
- **关键词**: 3–6 个

## TL;DR（一句话总结）
（一句中文概括论文做了什么、最核心的贡献）

## 问题与动机 (Problem & Motivation)
（要解决什么问题，为什么重要，已有工作的不足）

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: （扰动作用在哪、攻击者能力、不确定性如何建模）
- **设定**: cooperative / competitive / mixed；CTDE / decentralized / centralized；online / offline

## 方法 (Method)
（核心思想与算法步骤，2–5 条要点。如有关键公式/损失/约束，用文字描述）

## 理论贡献 (Theoretical Contributions)
（收敛性、样本复杂度、均衡存在性、认证半径等；无则填 `无 / 偏实证`）

## 实验 (Experiments)
- **环境/Benchmark**: 
- **Baselines**: 
- **评估指标**: 

## 主要结果 (Key Results)
（量化结论与最重要发现，2–4 条）

## 局限与未来工作 (Limitations & Future Work)

## 与综述的关联 (Relevance to Survey)
（这篇在 robust MARL 全景中的定位；与哪些主题/方法线相关）
```
