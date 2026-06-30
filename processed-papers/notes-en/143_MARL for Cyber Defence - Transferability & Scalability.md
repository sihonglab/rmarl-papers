# 143. Multi-Agent Reinforcement Learning for Cyber Defence: Transferability and Scalability

## Metadata
- **Title**: Multi-Agent Reinforcement Learning for Cyber Defence: Transferability and Scalability
- **Authors**: Andrew Thomas, Matthew Yates, Oliver Osborne
- **Affiliation**: Raytheon Strategic Research Group, Raytheon UK, Harlow, Essex, UK
- **Venue**: Applied AI Letters 2026 (Letter; received 14 March 2025, accepted 26 October 2025)
- **Link/arXiv**: https://doi.org/10.1002/ail2.70015

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to changes in the environment/task (network scale, attack scenario, and level of network activity); transferability across action/observation space scales. Not adversarial/worst-case robustness — robustness here means generalization stability under distribution shift (IID and OOD context shifts) of the cyber-defence task.
- **Method paradigm**: Cooperative MARL with CTDE; zero-shot transfer learning; task partitioning into node-level POMDPs; network-invariant local agents; PPO-based actor-critic (IPPO/MAPPO/HAPPO); Spatial Pyramidal Pooling for fixed-length observations.
- **Keywords**: autonomous cyber defence (ACD), multi-agent RL, zero-shot transfer, scalability, CTDE, MAPPO

## TL;DR
The paper proposes a zero-shot transfer method for autonomous cyber defence that partitions a network-defence task into scale-independent node-level POMDP subtasks solved by cooperative CTDE MARL (MAPPO) local agents, which can be remapped to larger/different networks without retraining and remain robust to changes in network scale, attack scenario, and activity level.

## Problem & Motivation
RL has proven effective for simple automated cyber defence (ACD) tasks, but several limitations block real-world deployment: trained policies have limited transferability (even minor environment changes require retraining from scratch), training is sample inefficient, and as the network scales the action/observation spaces grow, hurting single-agent stability and optimization. Existing transfer-learning approaches (task mapping, reward shaping, representation learning, policy transfer) are generally confined to a fixed action/state space — i.e., a fixed network scale. The paper addresses these limitations with a MARL-based zero-shot transfer approach designed to defend a varied set of networks across scales without retraining, noting MARL has been highlighted as an underdeveloped area in RL for ACD research.

## Robustness Setting
- **Threat model / uncertainty set**: The "robustness" is to task/environment variation rather than to an adversary attacking the agent. Tasks are formulated as a Contextual-MDP (CMDP) with a context space C and context distribution p(c); training/testing task sets are subsets of contexts. Two test regimes: IID (train/test contexts drawn i.i.d. from the full distribution) and out-of-distribution (OOD). Robustness is assessed by transferring small-network local agents to medium/large networks and to varied red (malicious) and green (legitimate) activity scenarios.
- **Setting**: Cooperative MARL; Centralised Training with Decentralised Execution (CTDE); online training in simulation, zero-shot (and limited few-shot) transfer at inference.

## Method
- Partition the global network-defence task into per-machine (node) management POMDPs; each "local" agent observes only one node's properties plus local link/region information, so its action/observation spaces are independent of overall network scale.
- Train local agents on a small network with MAPPO (shared critic for full-network context during CTDE training) using the same global reward R as the single-agent setup, encouraging collaborative behaviour.
- At inference, map the trained local actors to nodes in novel/larger networks (one-to-many mapping, possibly duplicating an agent across nodes) based on similarity of node type and number of links — no additional training required (zero-shot).
- Handle variable-length link information with two observation variants: a "padded" observation (supports up to M=8 links, zero-padded) and a "pooled" observation using a 1D Spatial Pyramidal Pooling (SPP) layer (windows pooling into 6, 4, 2 components → length-12 vector) that can theoretically handle any number of links.
- Develop MA-PrimAITE, an extension of DSTL's PrimAITE that accepts a collection of simultaneous node-level actions per timestep and maps the global observation/action spaces to node-level equivalents.

## Theoretical Contributions
None / mostly empirical. The paper uses standard formalisms (MDP, POMDP, CMDP, PPO clipped objective) but provides no new convergence, sample-complexity, or equilibrium guarantees; it notes that with independent multi-agent setups the single-agent convergence guarantee no longer holds.

## Experiments
- **Environment/Benchmark**: MA-PrimAITE (a multi-agent extension of the PrimAITE network simulation from the ARCD programme). Three network scales — small (6 nodes), medium (15 nodes), large (30 nodes); episode length 256 timesteps. Activity-scaling variants: proportional red/green activity, plus low/medium/high activity, red-activity-only (RAO), green-activity-only (GAO).
- **Baselines**: Natively trained MARL local agents (trained directly on the target medium/large network); multi-action single-agent PPO; single-action PPO (small network only, as reference).
- **Evaluation metrics**: Average episode reward (closer to 0 is better; negative rewards from successful red IERs / failed green IERs and node health), reported as the mean across 50 episodes; percentage change in reward between medium and large networks; distribution of average episode rewards.

## Key Results
- Transferred agents significantly outperform natively trained equivalents: Transfer Padded reward was 39% lower (better) than native on medium and 64% lower on large; Transfer Pooled improved 56% (medium) and 78% (large).
- Transferred agents are less susceptible to network scale: the reward drop between medium and large networks was 125% (native) / 137% (native pooled) vs only 34% (Transfer Padded) and 13% (Transfer Pooled).
- The method is robust to changing activity/attack scenarios: transfer outperformed native in nearly all activity-scaling tasks (uplifts ~7%–27%), with the exception of red-activity-only (RAO), where transfer was 21% worse — indicating limits on how far OOD the scenario can deviate from training.
- MAPPO best among MARL methods, roughly matching single-action PPO (with more training instability); multi-action PPO failed to learn due to its combinatorially large action space; pooled agents generally beat padded but with greater variance and sensitivity to node mapping.

## Limitations & Future Work
- Agents acting in parallel can take unnecessary actions; performance depends on an effective agent-to-node mapping (pooled agents especially sensitive). Future: action masking and additional local context to suppress harmful actions; learned/automated optimal mappings (e.g., grid-wise control encoder-decoder assignment).
- Future: hierarchical setups (separate detection/recommendation/action agents, or a manager agent) to abstract local tasks and improve transfer/generalization; learned observation representations and bisimulation-metric representations to standardize observations.
- PrimAITE, though high-fidelity, is still abstracted from real-world network defence; applying the approach to an emulated network (e.g., Imaginary YAK) would give a more realistic test.

## Relevance to Survey
This paper sits on the periphery of robust MARL: it is a cooperative MARL transfer-learning study where "robustness" denotes empirical generalization stability under task distribution shift (network scale, attack scenario, activity level; IID and OOD contexts) rather than worst-case/adversarial robustness or model-uncertainty (robust-MDP/DRMG) robustness. It connects to the survey's themes of scalability and generalization in MARL and to CTDE cooperative methods (MAPPO/HAPPO), and provides a real-world-motivated cyber-defence application where robustness-to-shift is the practical concern. It does not engage the robust-MDP, distributionally robust, minimax, or adversarial-agent literature.

## Related Work (verbatim excerpts from the paper)
> _[Section 1, Introduction]_

"Reinforcement learning (RL), is one such ML method of interest. RL is able to learn control tasks for simple games/simulations beyond the level of human performance. Applications to ACD type tasks have shown it to be an effective method for coordinating network defence [2–4]. Previous work has demonstrated RL agents' ability to learn flexible defensive strategies against network attacks in several simulated settings [5, 6]. However, there are a number of limitations to these RL approaches that prevent them from being deployed onto real-world hardware. Training new RL policies is sample inefficient, requiring a large number of interactions with the task environment to explore and learn the underlying task dynamics [7, 8]. These trained policies will often have limited transferability, such that even minor changes to the environment setup require the policy to be retrained from scratch [9]. Furthermore, as the environment scales so does the complexity and size of the action and observation spaces [10]. This scaling presents a challenge to single-agent setups, where increasingly longer training times are required, with agents often failing to fully optimise or suffering from a lack of stability whilst training [11]."

> _[Section 1, Introduction]_

"Transfer learning for RL aims to improve the efficiency with which RL policies can be adapted to new tasks. Transfer is achieved by the application of knowledge learned in one task domain to new unseen tasks [12]. There are a number of different approaches for encoding or applying previously learned knowledge such as task mapping [13], reward shaping [14], representation learning [15] or policy transfer [16]. However, these still have hard limitations. They are generally confined to transference between tasks in an environment with a fixed action state space. In the ACD space this means the scale of the simulated network must be consistent across tasks."

> _[Section 1, Introduction]_

"MARL trains multiple agents simultaneously within the same environment instance. It can potentially address the scaling challenges presented by enterprise systems where the network environments are highly complex [17]. A combination of MARL, multi-task and transfer learning paradigms has been proposed as the basis for a fully task-agnostic learning process [18, 19]. MARL agents have also demonstrated learning effective cyber defence strategies [20–22]. Despite this, MARL has been highlighted as an underdeveloped area in RL for ACD research [17]."

> _[Section 2.1.1, IPPO]_

"IPPO is the simplest extension of PPO to a multi-agent setting, shown in Figure 1. It is made up of N independent PPO policies that train simultaneously. As the policies are completely independent of each other it can be applied to either cooperative or competitive tasks [26]. The overall problem is broken down into N single-agent problems. As agent's actions are affecting the environment in parallel with each other, to an individual agent, the environment is no longer stationary. Therefore the theoretical convergence guarantee of single-agent RL no longer holds [27], limiting the stability of independent multi-agent setups."

### Cited references (resolved from the paper's bibliography)
- **[2]** Nguyen, Reddi. *Deep Reinforcement Learning for Cyber Security.* IEEE Transactions on Neural Networks and Learning Systems 34(8), 2021.
- **[3]** Adawadkar, Kulkarni. *Cyber-Security and Reinforcement Learning—A Brief Survey.* Engineering Applications of Artificial Intelligence 114, 2022.
- **[4]** Thompson, Caron, Hicks, Mavroudis. *Entity-Based Reinforcement Learning for Autonomous Cyber Defence.* arXiv:2410.17647, 2024.
- **[5]** Kiely, Bowman, Standen, Moir. *On Autonomous Agents in a Cyber Defence Environment.* arXiv:2309.07388, 2023.
- **[6]** Alavizadeh, Alavizadeh, Jang-Jaccard. *Deep Q-Learning Based Reinforcement Learning Approach for Network Intrusion Detection.* Computers 11(3), 2022.
- **[7]** Dulac-Arnold, Mankowitz, Hester. *Challenges of Real-World Reinforcement Learning.* arXiv:1904.12901, 2019.
- **[8]** Miles, Farmer, Foster, et al. *Reinforcement Learning for Autonomous Resilient Cyber Defence.* Black Hat USA 2024.
- **[9]** Oh, Kim, Nah, Park. *Employing Deep Reinforcement Learning to Cyber-Attack Simulation for Enhancing Cybersecurity.* Electronics 13(3), 2024.
- **[10]** Liu, Ren, Yan, Su, Gu, Kato. *Scaling up Multi-Agent Reinforcement Learning: An Extensive Survey on Scalability Issues.* IEEE Access 12, 2024.
- **[11]** Chan, Fishman, Canny, Korattikara, Guadarrama. *Measuring the Reliability of Reinforcement Learning Algorithms.* arXiv:1912.05663, 2019.
- **[12]** Taylor, Stone. *Transfer Learning for Reinforcement Learning Domains: A Survey.* Journal of Machine Learning Research 10(7), 2009.
- **[13]** Taylor, Whiteson, Stone. *Transfer via Inter-Task Mappings in Policy Search Reinforcement Learning.* AAMAS 2007.
- **[14]** Bates, Mavroudis, Hicks. *Reward Shaping for Happier Autonomous Cyber Security Agents.* ACM Workshop on Artificial Intelligence and Security (AISec '23), 2023.
- **[15]** Wang, Jian, Tan, Wu, Huang. *Representation Learning-Based Network Intrusion Detection System by Capturing Explicit and Implicit Feature Interactions.* Computers & Security 112, 2022.
- **[16]** Zhu, Lin, Jain, Zhou. *Transfer Learning in Deep Reinforcement Learning: A Survey.* IEEE Transactions on Pattern Analysis and Machine Intelligence 45, 2023.
- **[17]** Vyas, Hannay, Bolton, Burnap. *Automated Cyber Defence: A Review.* arXiv:2303.04926, 2023.
- **[18]** Upadhyay, Phlypo, Saini, Liwicki. *Sharing to Learn and Learning to Share; Fitting Together Meta, Multi-Task, and Transfer Learning: A Meta Review.* IEEE Access 12, 2024.
- **[19]** Soltoggio, Ben-Iwhiwhu, Braverman, et al. *A Collective AI via Lifelong Learning and Sharing at the Edge.* Nature Machine Intelligence 6, 2024.
- **[20]** Wilson, Menzies, Morarji, et al. *Multi-Agent Reinforcement Learning for Maritime Operational Technology Cyber Security.* arXiv:2401.10149, 2024.
- **[21]** Wang, Dechene. *Multi-Agent Actor-Critics in Autonomous Cyber Defense.* arXiv:2410.09134, 2024.
- **[22]** Singh, Rathbun, Graham, et al. *Hierarchical Multi-Agent Reinforcement Learning for Cyber Network Defense.* arXiv:2410.17351, 2024.
- **[26]** Papoudakis, Christianos, Schäfer, Albrecht. *Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks.* arXiv:2006.07869, 2020.
- **[27]** Huh, Mohapatra. *Multi-Agent Reinforcement Learning: A Comprehensive Survey.* arXiv:2312.10256, 2024.
