# 145. Hierarchical Adversarially-Resilient Multi-Agent Reinforcement Learning for Cyber-Physical Systems Security

## Metadata
- **Title**: Hierarchical Adversarially-Resilient Multi-Agent Reinforcement Learning for Cyber-Physical Systems Security
- **Authors**: Saad Alqithami
- **Affiliation**: Computer Science Department, Al-Baha University, Albaha, Saudi Arabia
- **Venue**: AAAI Summer Symposium Series (SuSS-25) 2025
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents / adaptive (AI-driven) cyber attacks against Cyber-Physical Systems (CPS); the attacker is modeled as an explicit learning adversary that performs scanning, denial-of-service, lateral movement, and data tampering; resilience against zero-day / previously unseen attack strategies.
- **Method paradigm**: Hierarchical MARL (local defender agents + global coordinator), adversarial training loop (co-trained learning attacker), Markov game / game-theoretic equilibrium (local Nash equilibrium), minimax-style training, PPO with GAE, hierarchical multi-critic.
- **Keywords**: Hierarchical MARL, adversarial training, CPS security, intrusion detection, PPO, local Nash equilibrium

## TL;DR
The paper proposes HAMARL, a hierarchical adversarially-resilient MARL framework for CPS security that combines local subsystem defender agents with a global coordinator and an explicit co-trained adaptive attacker (modeled as a Markov game with N+2 agents), trained with PPO/GAE to proactively defend industrial IoT systems against evolving cyber threats.

## Problem & Motivation
Cyber-Physical Systems underpin critical infrastructure (manufacturing, smart grids, autonomous transportation, healthcare), but increasing interconnectivity exposes them to sophisticated, continuously evolving threats (data tampering, APTs, DDoS) and AI-driven adaptive/zero-day attacks. Traditional rule-based intrusion detection and single-agent RL struggle to adapt. Existing MARL-based security frameworks mostly use flat/decentralized architectures lacking hierarchical coordination, and most lack explicit adversarial awareness, leaving them vulnerable to adaptive attackers. A unified CPS security approach combining hierarchical coordination and adversarial resilience remains elusive; HAMARL is proposed to fill this gap.

## Robustness Setting
- **Threat model / uncertainty set**: An adaptive attacker agent (πψ) is modeled as an explicit learning player co-trained with the defenders; it dynamically evolves its attack strategies (SCAN, LATERAL, DoS, TAMPER) to compromise subsystems and remain undetected. The environment is a partially observed stochastic (Markov) game with N+2 agents (N local defenders, one global coordinator, one adversarial attacker). Resilience is formalized via an (ε, δ)-resilience condition on a bounded compromise ratio ϱ.
- **Setting**: Mixed competitive-cooperative (defenders cooperate; attacker competes); hierarchical with partial observability — local defenders act on partial subsystem observations while a global coordinator aggregates state embeddings; online adversarial/co-training; uses a hierarchical multi-critic (local critics + global critic).

## Method
- Formalizes a Markov game with an adversarial agent G = (S, {Ai}, P, {ri}, γ) over N+2 agents; factorizes the joint policy as a product of local defender policies, the global coordinator policy, and the attacker policy (Proposition 1).
- Hierarchical architecture (Figure 1): local defender agents monitor/protect individual subsystems and trigger rapid local responses; a global coordinator aggregates compressed local state embeddings and issues system-wide actions (network isolation, mass patching, node resets); an adaptive attacker persistently probes vulnerabilities.
- Adversarial training loop: the attacker is co-trained with defenders, continually refining attacks; defenders learn robust behaviors. Framed as a repeated partially observable stochastic game, shaping a minimax-style equilibrium / adversarial resilience.
- Policy optimization via PPO adapted for multi-agent settings with Generalized Advantage Estimation (GAE); hybrid local/global reward shaping (local: detection accuracy vs. false alarms; global: uptime, minimal disruption; attacker: rewarded for stealthy compromise). Local policies are 2-layer Graph Attention Networks; global coordinator is a 3-layer MLP. Hyperparameters: γ = 0.99, λ = 0.95, clip ε = 0.2.
- Additional practical considerations: partial observability with compressed/scalable communication, formal safety checks for high-risk actions (mirroring ICS safety protocols), and transferability to other CPS domains.

## Theoretical Contributions
- Proposition 1: factorization of the joint policy in the hierarchical-adversarial setting.
- Theorem 1 (Convergence of PPO in Hierarchical-Adversarial MARL): under standard assumptions (bounded rewards, Markov mixing, sufficient batch data and exploration, bounded trust region), PPO updates with GAE converge to a stationary point that constitutes a local Nash equilibrium.
- Definition 2 ((ε, δ)-adversarial resilience) and Theorem 2 (Bounded Compromise in Equilibrium): if the per-step cost c of a compromised subsystem is sufficiently large relative to attacker reward ra, the long-run equilibrium compromise ratio ϱ* is strictly less than 1 (sketch proof provided).

## Experiments
- **Environment/Benchmark**: A simulated industrial IoT smart-factory testbed built with the Cyber-Battle-Sim toolkit; N = 8 PLC-driven subsystems, 64 diverse sensors (temperature, vibration, flow), Modbus/TCP communication. Synthetic-yet-realistic data. Attack scenarios: DoS, data tampering, APTs.
- **Baselines**: Single-Agent RL, Non-Hierarchical (flat / PPO) MARL, Rule-Based Intrusion Detection (IDS).
- **Evaluation metrics**: Detection latency, false alarm rate (FAR), precision, recall, F1, Mean Time To Detection (MTTD), accuracy, return, operational continuity/uptime; scalability via wall-clock training time across 4, 8, 12, 24 defender agents. Reported over seeds 42, 100, 2025.

## Key Results
- Both HAMARL and Non-Hierarchical MARL substantially outperform Rule-Based IDS on all metrics (e.g., F1 ~0.80 and accuracy ~82% vs. IDS F1 ~0.44–0.53 and accuracy ~47–54%, FAR ~6.5–6.8% vs. ~50%).
- HAMARL achieves competitive performance with Non-Hierarchical MARL, matching or marginally exceeding it on precision and FAR; local defenders maintained detection rates above 90% despite mid-episode adversary behavior shifts.
- Scalability (Table 2): HAMARL incurs higher training time than Non-Hierarchical MARL (e.g., 0.204 h vs. 0.028 h at 24 agents) but the increase scales roughly linearly and remains manageable; the global coordinator improved operational continuity by isolating compromised nodes / applying global patches before cascading failures.

## Limitations & Future Work
- Substantial computational cost of training hierarchical MARL, limiting deployment on resource-constrained operational-technology networks; future work: lightweight policy distillation, transfer-learning-based initialization, federated/distributed training.
- Reward shaping and hierarchical credit assignment require careful domain-specific tuning.
- Real-world adoption needs compliance with industrial standards (e.g., IEC 62443), fail-safe validations, and field trials.
- Future directions: transfer/meta-learning across CPS domains (manufacturing → smart grid / medical IoT), explainability and formal verification for trustworthiness, and extending adversarial training to multiple or colluding attackers.

## Relevance to Survey
This paper sits on the "adversarial agents / adversarial training" line of robust MARL, applied to the cybersecurity-of-CPS domain. It connects the explicit-adversary-as-learning-agent paradigm (modeling a co-trained attacker within a Markov game, in the spirit of robust adversarial RL) with hierarchical MARL and game-theoretic equilibrium (local Nash equilibrium, minimax-style training). It also touches safety constraints (formal safety checks) and fault/compromise tolerance (bounded compromise ratio resilience). It is an applied, mostly empirical instantiation of adversarially-resilient MARL rather than a core robust-MDP/DRMG theory contribution.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Cyber-Physical Systems Security"]_

"Cyber-Physical Systems are characterized by tightly integrated computational and physical processes, where embedded sensors and actuators interact in real-time to enable autonomous decision-making (Baheti and Gill 2011). The security of these systems involves protecting both the network infrastructure and physical components from malicious disruptions (Lee 2008). However, the complexity of CPS architectures—often spanning legacy industrial protocols, wireless sensor networks, and cloud-connected services—poses significant challenges for designing unified security solutions. Furthermore, the requirement for continuous operation, where downtime can lead to severe economic and safety consequences, necessitates the adoption of automated and adaptive security mechanisms to ensure resilience against cyber threats."

> _[Section 2, Related Work — "Multi-Agent Reinforcement Learning"]_

"Reinforcement learning is a machine learning paradigm where agents learn optimal behaviors by interacting with an environment and receiving feedback in the form of rewards or penalties(Sutton and Barto 2018). Multi-Agent Reinforcement Learning extends this concept to multi-agent environments, where multiple agents simultaneously learn and optimize their policies while considering interactions with others(Bus¸oniu, Babuˇska, and Schutter 2010). MARL approaches can be broadly categorized into: (a) Fully decentralized methods, where each agent learns independently without centralized coordination (Matignon, Laurent, and Fort-Piat 2012). (b) Centralized training with decentralized execution (CTDE), allowing agents to coordinate effectively during training but act independently at runtime (Lowe et al. 2017). (c) Hierarchical MARL, which decomposes decision-making into higher-level and lower-level policies, thereby improving both sample efficiency and scalability in complex environments (Kulkarni et al. 2016). While MARL has demonstrated success in robotics, autonomous systems, and network optimization, its application in cybersecurity for CPS remains underexplored. Furthermore, existing MARL-based intrusion detection and defense mechanisms often lack adversarial robustness, making them susceptible to sophisticated cyber threats."

> _[Section 2, Related Work — "Adversarial Learning and Game Theory"]_

"In the context of cybersecurity, adversarial learning involves modeling malicious actors who attempt to evade detection or manipulate system behavior(Goodfellow, Shlens, and Szegedy 2015). This aligns well with game-theoretic security models, where defenders and attackers can be represented as players with conflicting objectives(Shapley 1953). Incorporating adversarial learning into security systems enables proactive defense strategies, where defenders are trained against worst-case attack scenarios to enhance system resilience (Standen, Kim, and Szabo 2025). In CPS security, adversarial learning is particularly relevant because attackers can leverage AI-driven techniques to continuously adapt their strategies. Integrating adversarial learning into MARL-based defense mechanisms allows security agents to anticipate and counteract adaptive cyber threats. Additionally, the competitive-cooperative nature of multi-agent environments makes game-theoretic approaches particularly useful, as defenders must coordinate responses while mitigating attacks from intelligent adversaries (Conti et al. 2018)."

> _[Section 2, Related Work — "Positioning of This Work"]_

"Although there have been several investigations into MARL for intrusion detection(Louati, Ktata, and Amous 2024) and adversarial learning for robust classification(Goodfellow, Shlens, and Szegedy 2015), there is a lack of research that integrates hierarchical MARL with adversarial training specifically for CPS security. Addressing this gap, our work introduces a Hierarchical Adversarially-Resilient Multi-Agent Reinforcement Learning framework that: (a) Structures multiple defender agents under a hierarchical coordinator, ensuring efficient and scalable threat mitigation. (b) Incorporates an adaptive adversarial training loop, where the system continuously learns from evolving attack strategies to enhance resilience. By bridging hierarchical MARL and adversarial learning, our approach extends prior work and contributes to the growing field of AI-driven cybersecurity for CPS (Rashid et al. 2020). The proposed framework is designed to improve real-time intrusion detection, response efficiency, and adaptability, making it a novel and practical solution for securing modern CPS environments."

> _[Introduction — prior-work motivation paragraph]_

"Recent advances in multi-agent reinforcement learning (MARL) offer promising solutions to the security challenges faced by CPS. By distributing decision-making responsibilities among multiple agents, MARL facilitates scalable, coordinated, and adaptive defense strategies that are particularly effective in decentralized and complex environments (Bus¸oniu, Babuˇska, and Schutter 2010). Hierarchical reinforcement learning further extends this concept, introducing a multi-tier control structure where higher-level policies guide lower-level agents, thereby enhancing scalability, adaptability, and strategic coherence across large-scale CPS deployments (Vezhnevets et al. 2017). Nevertheless, most existing MARL-based security frameworks lack explicit adversarial awareness, rendering them vulnerable to adaptive, AI-driven cyber threats. Purely reactive defensive strategies fall short in environments where adversaries consistently evolve tactics to evade detection (Goodfellow, Shlens, and Szegedy 2015). Hence, incorporating adversarial training—where defensive agents explicitly learn against evolving attacker strategies—emerges as crucial for proactively enhancing MARL-based defense resilience."

### Cited references (resolved from the paper's bibliography)
- **[Baheti and Gill 2011]** Baheti, R.; Gill, H. *Cyber-physical systems.* The Impact of Control Technology, 12(1):161–166, 2011.
- **[Bus¸oniu, Babuˇska, and Schutter 2010]** Buşoniu, L.; Babuška, R.; Schutter, B. D. *Multi-agent reinforcement learning: An overview.* In Innovations in Multi-Agent Systems and Applications – 1, Springer, 2010.
- **[Conti et al. 2018]** Conti, M.; Dehghantanha, A.; Franke, K.; Watson, S. *Internet of Things security and forensics: Challenges and opportunities.* Future Generation Computer Systems, 2018.
- **[Goodfellow, Shlens, and Szegedy 2015]** Goodfellow, I.; Shlens, J.; Szegedy, C. *Explaining and Harnessing Adversarial Examples.* ICLR 2015.
- **[Kulkarni et al. 2016]** Kulkarni, T. D.; Narasimhan, K.; Saeedi, A.; Tenenbaum, J. *Hierarchical Deep Reinforcement Learning: Integrating Temporal Abstraction and Intrinsic Motivation.* NIPS 2016.
- **[Lee 2008]** Lee, E. A. *Cyber physical systems: Design challenges.* 11th IEEE International Symposium on Object Oriented Real-Time Distributed Computing, 2008.
- **[Louati, Ktata, and Amous 2024]** Louati, F.; Ktata, F. B.; Amous, I. *Big-IDS: a decentralized multi agent reinforcement learning approach for distributed intrusion detection in big data networks.* Cluster Computing, 27(5):6823–6841, 2024.
- **[Lowe et al. 2017]** Lowe, R.; Wu, Y. I.; Tamar, A.; Harb, J.; Pieter Abbeel, O.; Mordatch, I. *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments.* NeurIPS 2017.
- **[Matignon, Laurent, and Fort-Piat 2012]** Matignon, L.; Laurent, G. J.; Fort-Piat, N. L. *Independent Reinforcement Learners in Cooperative Markov Games: a Survey regarding Coordination Problems.* The Knowledge Engineering Review, 2012.
- **[Rashid et al. 2020]** Rashid, T.; Samvelyan, M.; De Witt, C. S.; Farquhar, G.; Foerster, J.; Whiteson, S. *Monotonic value function factorisation for deep multi-agent reinforcement learning.* Journal of Machine Learning Research, 21(178):1–51, 2020.
- **[Shapley 1953]** Shapley, L. *Stochastic Games.* Proceedings of the National Academy of Sciences, 1953.
- **[Standen, Kim, and Szabo 2025]** Standen, M.; Kim, J.; Szabo, C. *Adversarial Machine Learning Attacks and Defences in Multi-Agent Reinforcement Learning.* ACM Computing Surveys, 57(5):1–35, 2025.
- **[Sutton and Barto 2018]** Sutton, R. S.; Barto, A. G. *Reinforcement Learning: An Introduction.* MIT Press, 2nd edition, 2018.
- **[Vezhnevets et al. 2017]** Vezhnevets, A. S.; Osindero, S.; Schaul, T.; Heess, N.; Jaderberg, M.; Silver, D.; Kavukcuoglu, K. *FeUdal Networks for Hierarchical Reinforcement Learning.* ICML 2017.
