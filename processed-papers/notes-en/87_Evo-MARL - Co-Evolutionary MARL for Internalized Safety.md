# 87. Evo-MARL: Co-Evolutionary Multi-Agent Reinforcement Learning for Internalized Safety

## Metadata
- **Title**: Evo-MARL: Co-Evolutionary Multi-Agent Reinforcement Learning for Internalized Safety
- **Authors**: Zhenyu Pan, Yiting Zhang, Yutong Zhang, Jianshu Zhang, Haozheng Luo, Yuwei Han, Dennis Wu, Hong-Yu Chen, Philip S. Yu, Manling Li, Han Liu
- **Affiliation**: Northwestern University; University of Illinois at Chicago
- **Venue**: Not specified (arXiv preprint)
- **Link/arXiv**: arXiv:2508.03864v2 [cs.AI], 6 Sep 2025

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial attacks on LLM/MLLM-based multi-agent systems (MAS): jailbreak, prompt injection (indirect prompt injection), malicious/compromised agents, safety contagion across the interaction graph; single-point-of-failure of external guard modules
- **Method paradigm**: Adversarial co-training (attacker–defender co-evolution), evolutionary search (mutation/crossover + fitness selection), parameter-sharing MARL with role-conditioned policies, GRPO (Group Relative Policy Optimization)
- **Keywords**: Multi-agent systems, LLM/MLLM safety, jailbreak defense, co-evolutionary adversarial training, GRPO, internalized safety

## TL;DR
Evo-MARL trains every task agent in an LLM/MLLM multi-agent system to internalize defensive capabilities (rather than relying on an external guard module) by co-evolving an evolutionary pool of attack prompts against parameter-sharing GRPO-trained defenders, jointly improving safety (ASR down by up to 22%) and task utility (accuracy up by up to 5%).

## Problem & Motivation
Multi-agent systems built on (multimodal) LLMs deliver strong collaboration but inherit foundation-model vulnerabilities and add new risks through inter-agent communication, where a single compromised agent (via manipulated roles, poisoned tools, or indirect prompt injection) can trigger cascading, system-wide failures. Existing defenses typically add an external guard module (static rules or a dedicated safety agent), which has two key limitations: (1) standalone guards offer limited protection when task agents themselves lack safety awareness, and (2) reliance on a single guard creates a single point of failure that reduces resilience. Adding more guards increases cost and complexity. The paper instead advocates internalizing defense capabilities within every task agent to foster collective safety awareness without increasing system overhead.

## Robustness Setting
- **Threat model / uncertainty set**: Attackers are external third-party adversaries that either embody malicious intent or are manipulated to attack others; they inject unsafe instructions, malicious code, or unfaithful facts into agents' outputs, tool-call results, and memory. To simulate safety contagion, a randomly chosen initial victim agent is attacked and attack prompts are sequentially injected into the responses of that agent and its downstream peers in a chain-structured MAS via indirect prompt injection. Attackers are excluded from RL optimization; their strategies evolve through an evolutionary attack-prompt pool.
- **Setting**: Cooperative defenders vs. adversarial attackers (mixed/competitive co-evolution); LLM/MLLM-based MAS with parameter sharing and role-conditioned policies; online RL training (GRPO).

## Method
- Formulates a shared MDP environment E = (S, A_a, A_d, T, R_a, R_d) where attackers learn policies π_a to induce unsafe behavior and defenders learn policies π_d to maintain system robustness; a chain-structured MAS of three specialized agents (problem analyst, solving executor, answer verifier) is used.
- During adversarial training, a subset of agents is perturbed to act as attackers (injecting harmful instructions) while the rest serve as defenders that detect, discard, or purify malicious content based on the historical interaction trajectory.
- Reward design: based on the system's final response — safe response gives +1 (unsafe gives -1); correct answer gives an additional +0.5 (incorrect gives -0.5) — jointly promoting safety and helpfulness.
- Defenders are optimized with Group Relative Policy Optimization (GRPO) under parameter sharing for efficiency (Eq. 1, with clipped surrogate objective and a KL penalty term D_KL[π_θ‖π_ref]).
- Evolving attacks: inspired by biological evolution, attackers generate diverse attack-prompt variants via random mutation and crossover; attack effectiveness (success rate) serves as a fitness signal, and successful variants are retained to seed the next generation, creating a co-evolving attacker–defender dynamic.

## Theoretical Contributions
None / mostly empirical. The paper provides a problem formulation (shared MDP for attacker/defender) and the GRPO objective but no formal convergence, equilibrium, or robustness guarantees.

## Experiments
- **Environment/Benchmark**: 3 red-team datasets — JailBreakV-28K (official 280 mini split), HarmBench (multimodal split), MultiJail (English split) — plus 2 helpfulness benchmarks — MATH (100 randomly sampled points) and Creative Writing. Two MAS settings: (1) chain-structured three-agent system used in training, and (2) a hierarchical setup where a jailbreak-prone multimodal agent responds first, then three benign agents sequentially decide whether to agree.
- **Baselines**: Untrained MAS counterparts at 1.5B and 3B scales (MAS-1.5B, MAS-3B), and a larger untrained MAS-7B; agents instantiated with Qwen2.5-1.5B-Instruct and Qwen2.5-3B-Instruct.
- **Evaluation metrics**: Attack Success Rate (ASR) on the red-teaming benchmarks with harmfulness judged by LLaMA-Guard-3-8B; answer accuracy vs. gold solutions for MATH; protocol-following score for Creative Writing.

## Key Results
- When the MAS is composed of trained 1.5B models, ASR on HarmBench drops by up to 22%; safety improves consistently across tasks and model scales.
- MAS built on trained 1.5B models consistently outperform their 3B counterparts in safety and even surpass the untrained 7B-based MAS on JailBreakV and MultiJail, suggesting larger base models are not inherently safer in multi-agent configurations and that adversarial training can match or exceed model scaling for safety.
- Helpfulness improves: the trained 1.5B MAS achieves accuracy gains of up to 5 percentage points on mathematical reasoning and creative writing without compromising safety, addressing the common safety–helpfulness trade-off.

## Limitations & Future Work
- Stabilizing training with adaptive attackers remains challenging.
- Scaling to larger or more complex multi-agent systems is an open issue.
- Incorporating memory or external knowledge to boost long-term robustness in dynamic adversarial environments is left for future work.

## Relevance to Survey
This paper sits at the intersection of robust MARL and LLM/MLLM multi-agent safety. It applies an adversarial co-training / minimax-style paradigm (attacker vs. defender), augmented with evolutionary search, to the emerging setting of robustness against jailbreak and prompt-injection attacks in LLM-based MAS. It connects the survey's "adversarial training," "adversarial agents / malicious agents," "communication robustness," and "safety" themes to the modern LLM-agent regime, and illustrates the shift from external guard modules toward internalized, jointly-optimized defensive policies via parameter-sharing MARL (GRPO).

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Works — "Safety in Multi-Agent Systems"]_

"Safety in Multi-Agent Systems. Large Language Models and Multi-modal LLMs are known to exhibit significant safety vulnerabilities, particularly susceptibility to prompt injection attacks [7, 16, 20, 29, 33] and adversarial manipulations [17, 18, 45]. As LLM-based agents are increasingly augmented with external modules such as tools and memory systems, they become even more exposed to security threats through these interfaces [2, 5, 36, 47]."

"While MAS offers promising capabilities through agent collaboration, it also introduces unique safety concerns. Adversaries can compromise MAS via two main avenues: (1) hijacking individual agents to propagate malicious content throughout the system [13, 15, 48], and (2) manipulating inter-agent communication and workflow execution [8, 9, 38, 44]. To address these safety issues, prior work has primarily relied on external safety modules or explicit defense protocols. For example, tse Huang et al. [39] introduces a dedicated safety inspection agent to monitor and sanitize message streams. Wang et al. [41] leverages Graph Neural Networks (GNNs) to model communication topologies and detect unsafe message propagation, further applying supervised fine-tuning to enhance detection performance. Fan and Li [6] proposes a peer-review mechanism, where agents serve as inspectors of each other's outputs and collectively reject unsafe responses."

"Although effective to some extent, these approaches do not improve the agents' intrinsic safety mechanisms. Moreover, reliance on external modules often results in scalability bottlenecks and fragility. In contrast, we advocate for embedding safety awareness directly into agents via reinforcement learning, allowing the entire system to become more robust through internalized safety capabilities."

> _[Section 2, Related Works — "Reinforcement Learning for Agent Training"]_

"Reinforcement Learning for Agent Training. RL has proven effective in LLM post-training, with methods such as Proximal Policy Optimization (PPO) [32] and Group Relative Policy Optimization (GRPO) [3] yielding substantial performance improvements. Recent works have applied RL to enhance agentic behavior: Search-R1 [12] teaches LLMs to incorporate web search into reasoning, while Wei et al. [43] and Team et al. [37] demonstrate large-scale RL training on real-world agentic and software engineering tasks. Multi-agent reinforcement learning methods—such as MAPPO [46], QMIX [31], and HATRPO [14]—serve as foundational algorithms for learning coordinated multi-agent policies. Building on this, LLM-based MARL seeks to leverage these coordination capabilities to further enhance system performance. Park et al. [28] uses MAPPO to enhance collaborative reasoning across agents. Wan et al. [40] trains a meta-agent and an execution agent with distinct roles and parameter-sharing schemes to achieve advanced meta-reasoning. Chen et al. [1] treats each Retrieval-Augmented Generation (RAG) component as an autonomous agent, collectively improving system capabilities. Inspired by these, our work aim to utilize MARL to embed safety awareness into each agent. Through adversarial co-training between attacker and defender agents, we enable both enhanced individual safety awareness and improved overall system reliability."

### Cited references (resolved from the paper's bibliography)
- **[1]** Chen, Yan, Sun, Ma, Zhang, Wang, Yin, Yang, Mao. *Improving retrieval-augmented generation through multi-agent reinforcement learning.* 2025.
- **[2]** Chen, Xiang, Xiao, Song, Li. *AgentPoison: Red-teaming LLM agents via poisoning memory or knowledge bases.* 2024.
- **[3]** DeepSeek-AI. *DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning.* 2025.
- **[5]** Dong, Xu, He, Li, Tang, Liu, Liu, Xiang. *A practical memory injection attack against LLM agents.* 2025.
- **[6]** Fan, Li. *PeerGuard: Defending multi-agent systems against backdoor attacks through mutual reasoning.* 2025.
- **[7]** Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz. *Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection.* 2023.
- **[8]** Han, Zhang, Yao, Jin, Xu. *LLM multi-agent systems: Challenges and open problems.* 2025.
- **[9]** He, Lin, Dong, Xu, Xing, Liu. *Red-teaming LLM multi-agent systems via communication attacks.* 2025.
- **[12]** Jin, Zeng, Yue, Yoon, Arik, Wang, Zamani, Han. *Search-R1: Training LLMs to reason and leverage search engines with reinforcement learning.* 2025.
- **[13]** Khan, Tan, Yun, Flemming, Chen. *Agents Under Siege: Breaking pragmatic multi-agent LLM systems with optimized prompt attacks.* 2025.
- **[14]** Kuba, Chen, Wen, Wen, Sun, Wang, Yang. *Trust region policy optimisation in multi-agent reinforcement learning (HATRPO).* 2022.
- **[15]** Lee, Tiwari. *Prompt infection: LLM-to-LLM prompt injection within multi-agent systems.* 2024.
- **[16]** Li, Zhou, Zhu, Yao, Liu, Han. *DeepInception: Hypnotize large language model to be jailbreaker.* 2024.
- **[17]** Li, Chen, Liu, Bai, Yang, Xiang, Zhang. *TF-Attack: Transferable and fast adversarial attacks on large language models.* 2024.
- **[18]** Liu, Xu, Chen, Xiao. *AutoDAN: Generating stealthy jailbreak prompts on aligned large language models.* 2024.
- **[20]** Lv, Wang, Zhang, Huang, Dou, Ye, Gui, Zhang, Huang. *CodeChameleon: Personalized encryption framework for jailbreaking large language models.* 2024.
- **[28]** Park, Han, Guo, Ozdaglar, Zhang, Kim. *MAPoRL: Multi-agent post-co-training for collaborative large language models with reinforcement learning.* 2025.
- **[29]** Pathade. *Red teaming the mind of the machine: A systematic evaluation of prompt injection and jailbreak vulnerabilities in LLMs.* 2025.
- **[31]** Rashid, Samvelyan, Schroeder de Witt, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* 2018.
- **[32]** Schulman, Wolski, Dhariwal, Radford, Klimov. *Proximal policy optimization algorithms.* 2017.
- **[33]** Schwartzman. *Exfiltration of personal information from ChatGPT via prompt injection.* 2024.
- **[36]** Shi, Yuan, Tie, Zhou, Gong, Sun. *Prompt injection attack to tool selection in LLM agents.* 2025.
- **[37]** Kimi Team et al. *Kimi K2: Open agentic intelligence.* 2025.
- **[38]** Triedman, Jha, Shmatikov. *Multi-agent systems execute arbitrary malicious code.* 2025.
- **[39]** Jen-tse Huang, Zhou, Jin, Zhou, Chen, Wang, Yuan, Lyu, Sap. *On the resilience of LLM-based multi-agent collaboration with faulty agents.* 2025.
- **[40]** Wan, Li, Wen, Song, Wang, Yang, Schmidt, Wang, Zhang, Hu, Wen. *ReMA: Learning to meta-think for LLMs with multi-agent reinforcement learning.* 2025.
- **[41]** Wang, Zhang, Yu, Wan, Meng, Guo, Wang, Wang. *G-Safeguard: A topology-guided security lens and treatment on LLM-based multi-agent systems.* 2025.
- **[43]** Wei, Duchenne, Copet, Carbonneaux, Zhang, Fried, Synnaeve, Singh, Wang. *SWE-RL: Advancing LLM reasoning via reinforcement learning on open software evolution.* 2025.
- **[44]** Yan, Zhou, Zhang, Zhang, Zhou, Miao, Li, Li, Zhang. *Beyond self-talk: A communication-centric survey of LLM-based multi-agent systems.* 2025.
- **[45]** Yi, Liu, Sun, Cong, He, Song, Xu, Li. *Jailbreak attacks and defenses against large language models: A survey.* 2024.
- **[46]** Yu, Velu, Vinitsky, Gao, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative, multi-agent games (MAPPO).* 2022.
- **[47]** Zhang, Huang, Mei, Yao, Wang, Zhan, Wang, Zhang. *Agent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents.* 2025.
- **[48]** Zhou, Li, Zhang, Zhang, Wang, Liu, Guo. *CORBA: Contagious recursive blocking attacks on multi-agent systems based on large language models.* 2025.
