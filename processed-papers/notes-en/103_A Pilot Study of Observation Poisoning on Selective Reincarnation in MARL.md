# 103. A Pilot Study of Observation Poisoning on Selective Reincarnation in Multi-Agent Reinforcement Learning

## Metadata
- **Title**: A Pilot Study of Observation Poisoning on Selective Reincarnation in Multi-Agent Reinforcement Learning
- **Authors**: Harsha Putla, Chanakya Patibandla, Krishna Pratap Singh, P Nagabhushan
- **Affiliation**: Department of Information Technology, Indian Institute of Information Technology, Allahabad, Uttar Pradesh, India; Vignan's Foundation for Science, Technology & Research, Guntur, Andhra Pradesh, India
- **Venue**: Neural Processing Letters 2024 (Vol. 56:161)
- **Link/arXiv**: https://doi.org/10.1007/s11063-024-11625-w

## Taxonomy
- **Robustness / perturbation type targeted**: Observation poisoning (adversarial perturbation of the observation space via dataset/data poisoning); attacks injected into the offline "teacher dataset" used for selective reincarnation
- **Method paradigm**: Empirical robustness/vulnerability evaluation (attack-based stress testing); no defense proposed; rank-correlation analysis with Kendall's tau and an "Overall Vulnerability" metric
- **Keywords**: Observation poisoning, Selective reincarnation, Multi-agent reinforcement learning, Adversarial attacks, Kendall's tau metric

## TL;DR
This pilot study empirically evaluates how vulnerable selective reincarnation in cooperative MARL is to observation-poisoning attacks by injecting four triggers (Gaussian noise addition, observation reversal, random shuffling, scaling) into the teacher dataset of a HalfCheetah IDDPG system, and quantifies the resulting disruption to reincarnation decisions using Kendall's tau, finding that reversal and shuffling most strongly degrade the agent-combination ranking.

## Problem & Motivation
Selective reincarnation is a recent MARL technique that reuses prior computations (model weights, offline datasets) to accelerate learning, selecting which agents to reincarnate based on criteria such as maximum and average returns. While it improves efficiency and adaptability, it introduces new vulnerabilities to adversarial attacks, particularly observation poisoning, which subtly manipulates an agent's observation space and can misdirect its learning. The robustness of selective reincarnation against such poisoning attacks is an unexplored aspect, yet it is crucial for safe real-world deployment (e.g., autonomous driving, robotics). The paper aims to systematically evaluate this vulnerability to inform the development of more resilient and secure MARL systems and better-informed reincarnation decisions.

## Robustness Setting
- **Threat model / uncertainty set**: The attacker poisons the offline "teacher dataset" (the 'Good-Medium' dataset, ~final 40% of teachers' experiences from the Off-the-Grid MARL framework) that is later provided to the reincarnating agents. Four environment-independent perturbation triggers are applied to the d×d observation matrix s (d=10): Gaussian noise addition (s'_ij = s_ij + ε_ij, ε ~ N(0, σ²), σ=0.01), observation reversal (row order inverted), random shuffling (rows randomly permuted by a bijection), and scaling (s'_ij = α·s_ij, α=1.1). The perturbations are described as subtle yet significantly impactful on learning.
- **Setting**: Cooperative (fully cooperative, shared-reward Dec-POMDP); decentralized execution with Independent DDPG (IDDPG); uses offline teacher data for reincarnation (offline-to-online / reincarnation), then retrained online.

## Method
- Train six cooperative HalfCheetah (MaMujoco) agents — back ankle (BA), back knee (BK), back hip (BH), front ankle (FA), front knee (FK), front hip (FH) — with IDDPG over 1 million steps and save experiences as the teacher dataset.
- Poison the teacher dataset with one of four triggers (Gaussian noise, reversal, shuffling, scaling), then provide this poisoned dataset to reincarnating agents.
- Enumerate all 2^6 = 64 subsets of agent combinations for reincarnation; for each combination retrain for 200k timesteps after teacher-data removal plus an additional 50k timesteps on student data alone, repeated over five seeds (0–4).
- Evaluate using 'maximum return' (Rmax, peak return averaged over seeds) and 'average return' (Ravg, averaged over all timesteps and seeds); group and sort reincarnating agents by metric value.
- Quantify the impact of poisoning on the agent-combination ranking with Kendall's tau correlation coefficient (τ near 1 = minimal ranking change; near −1 = strong disruption), and assess per-combination susceptibility via an "Overall Vulnerability" formula Vc averaging normalized return drops across the four attacks for combination c.

## Theoretical Contributions
None / mostly empirical. The paper introduces an "Overall Vulnerability" quantification formula and uses Kendall's tau for rank-correlation analysis, but provides no convergence, sample-complexity, or certified-robustness guarantees.

## Experiments
- **Environment/Benchmark**: HalfCheetah (MuJoCo / Multi-Agent MuJoco, MaMujoco) as six cooperative agents; 'Good-Medium' teacher dataset from the Off-the-Grid MARL framework.
- **Baselines**: Base case (no poisoning) and Tabula Rasa (training from scratch) as reference points; comparison is across the four poisoning triggers and across the 64 agent combinations (no external robust-MARL baseline algorithms).
- **Evaluation metrics**: Maximum return (Rmax), average return (Ravg), Kendall's tau correlation coefficient on performance rankings, and the Overall Vulnerability score Vc.

## Key Results
- The reversal technique showed the most pronounced negative effect for maximum returns, with an average decrease of 38.08% in Kendall's tau values across all agent combinations; random shuffling decreased Kendall's tau by 17.66%; noise addition and scaling aligned with the original ranking by only 21.42% and 32.66%, respectively.
- Vulnerability varies markedly across agent combinations: 'BA, FA, FK' is the most vulnerable (overall vulnerability score 46%), while 'BA' alone exhibits the lowest vulnerability (a 10% negative vulnerability score, i.e., performing better under attack than baseline).
- The fully reincarnated configuration performed well under base case and noise addition but struggled against reversal and random shuffling, suggesting these attacks particularly disrupt inter-agent cooperation and coordination. The impact of noise/reversal on rankings is strongest with a single reincarnating agent and lessens as the number of reincarnating agents increases, while scaling consistently influences rankings regardless of count.

## Limitations & Future Work
- A pilot study limited to basic, environment-independent triggers in a single environment (HalfCheetah) with IDDPG; only cooperative shared-reward setting is studied; no defense mechanism is proposed.
- Future work: test more poisoning methods and advanced triggers across a variety of environments (e.g., multi-agent Humanoid and HumanoidStandup); study cooperative, competitive, and mixed settings; assess resilience to advanced poisoning attacks; and contribute to developing more effective defense strategies.

## Relevance to Survey
This paper sits on the adversarial-attack / data-poisoning line of robust MARL, specifically observation poisoning targeting the offline data used for reincarnation. Rather than proposing a robust algorithm, it provides an empirical robustness/vulnerability evaluation that complements work on robust deep RL against state-observation perturbations and on reward/action/policy poisoning in (multi-agent) RL. It connects the themes of adversarial robustness, offline/reincarnating RL, and cooperative MARL coordination fragility, motivating future defenses for the survey's "robustness evaluation and adversarial attacks in MARL" theme.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — opening]_

"Our research intersects three primary areas of prior work: "Selective Reincarnation in MARL" [10], "Adversarial Attacks in Deep RL, specifically Observation Poisoning", and "Robustness Evaluation in MARL"."

> _[Section 2.1, Selective Reincarnation in MARL]_

"MARL has garnered attention due to its ability to model complex interactions between multiple agents. Recent literature has explored the concept of reincarnation in MARL which involves reusing prior computations based on past performances. This approach has shown significant benefits, such as improved computational efficiency and adaptability, as discussed in a work by [11]. Transfer learning has been another area of interest in MARL. Study [41] introduce an ontology-based approach to facilitate knowledge transfer across agents, which aligns with the broader theme of reusing knowledge. Moreover, [42] proposes methods to transfer knowledge from trained agents to newer ones, resulting in improved training efficiency and performance. Selective reincarnation, a form of reincarnation in which we can select which agents to reincarnate, in MARL has been found to improve learning efficiency by reusing previous computations across selected agents [10]. In a cooperative, heterogeneous HalfCheetah MARL setup, it shows faster convergence and better returns than starting anew or complete reincarnation. However, careful selection of agents to reincarnate is crucial as incorrect selection can yield inferior results. Our research focuses on the unexplored aspect of the robustness of selective reincarnation in MARL against susceptibility to poisoning attacks, specifically observation poisoning."

> _[Section 2.2, Adversarial Attacks in Deep RL: Observation Poisoning]_

"The vulnerability of MARL systems, especially in the face of adversarial attacks, has been a pressing concern. The paper [43] discusses the challenges posed by dynamic environments and the need for continuous coordination among agents. This work underscores the importance of our research, which focuses on the vulnerabilities introduced by observation poisoning.
Observation poisoning, an adversarial tactic, can majorly derail an agent's learning by manipulating its observation space, thereby threatening RL system robustness. Research shows that even slight disruptions can significantly affect Deep RL agents, inducing them to adopt sub-optimal policies [44]. A two-stage optimization-based attack can efficiently introduce adversarial noise into RL, heavily impacting performance [45]. Backdoors attack using triggers in deep RL agents hamper their performance [46]. Notably, a small amount of poisoned training data can lead to successful backdoor attacks, highlighting system vulnerabilities [47]."

> _[Section 2.3, Robustness Evaluation in MARL]_

"Ensuring that MARL systems are robust, especially as they are deployed in diverse and challenging environments, is crucial. Due to the varied landscape of adversarial attacks on MARL, particularly on input observations, it is essential to understand these threats and develop appropriate evaluation metrics and defense strategies.
Like other domains in machine learning [48–50], one standard attack on MARL systems is the Gaussian noise addition (GNA), which introduces subtle yet effective adversarial strategies by adding noise to agents' observations. Attackers can mislead agents and adversely affect their learning trajectories through this manipulation. The significance of defending against Gaussian noise addition is emphasized in research such as [51], showcasing the profound impact of such a seemingly simple attack on MARL systems.
Shuffling and reversal attacks are also potent adversarial tactics that can drastically alter an agent's perception of the environment without changing the actual state of the environment. These manipulations lead to sub-optimal learning outcomes. Multiple works, such as [16, 45, 52–56], highlight the importance of understanding and mitigating the risks associated with these shuffling-based attacks in MARL.
Although scaling attacks have been extensively studied in broader machine learning contexts [45, 48, 57–59], their impact on MARL systems remains less explored. These attacks manipulate the magnitude of agents' observations, leading to skewed perceptions and decisions. Our work assesses the robustness of selective reincarnation in the face of diverse poisoning attacks in MARL, including scaling attacks."

> _[Introduction — prior-work context on safety, robustness, and poisoning attacks]_

"Selective reincarnation has brought improvements, but it also introduces new vulnerabilities in the face of adversarial attacks. Observation poisoning is one such attack that can degrade the performance of well-trained neural network policies by perturbing the observation space [15]. This issue extends to crowdsensing systems where false data can be injected to interfere with analysis results [16]. With the increasing prevalence of these attacks, it is urgent to develop robust models that can withstand such threats [17]. The safety of MARL systems is critical for their successful deployment in real-world scenarios like autonomous driving and robotics [18]. Ignoring safety in RL can lead to catastrophic outcomes [19]. Recent studies [20–23] highlight the potential of safe RL to enhance the reliability of AI systems. This is particularly relevant in the context of MARL, where action [24], policy [25], and reward [26] poisoning attacks pose significant threats to system performance. Therefore, it is necessary [27–29] to test and evaluate the susceptibility of selective reincarnation to adversarial attacks, which aids in the essential step of development of robust defenses and resilient algorithms [30–36]."

### Cited references (resolved from the paper's bibliography)
- **[10]** Formanek, Tilbury, Shock, Tessera, Pretorius. *Reduce, reuse, recycle: Selective reincarnation in multi-agent reinforcement learning.* Workshop on Reincarnating Reinforcement Learning at ICLR 2023.
- **[11]** Agarwal, Schwarzer, Castro, Courville, Bellemare. *Reincarnating reinforcement learning: Reusing prior computation to accelerate progress.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2022.
- **[15]** Xiong, Eappen, Zhu, Jagannathan. *Defending observation attacks in deep reinforcement learning via detection and denoising.* ECML PKDD (Machine Learning and Knowledge Discovery in Databases), Springer, 2023.
- **[16]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2020.
- **[17]** Li, Sun, Lu, Maharjan, Tian. *Deep reinforcement learning for partially observable data poisoning attack in crowdsensing systems.* IEEE Internet of Things Journal, 2019.
- **[18]** Gu, Yang, Du, Chen, Walter, Wang, Yang, Knoll. *A review of safe reinforcement learning: Methods, theory and applications.* arXiv:2205.10330, 2022.
- **[19]** Schmidt, Kontes, Plinge, Mutschler. *Can you trust your autonomous car? Interpretable and verifiably safe reinforcement learning.* IEEE Intelligent Vehicles Symposium (IV) 2021.
- **[20]** Amani, Thrampoulidis, Yang. *Safe reinforcement learning with linear function approximation.* ICML 2021.
- **[21]** Thomas, Luo, Ma. *Safe reinforcement learning by imagining the near future.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2021.
- **[22]** Pfrommer, Gautam, Zhou, Sojoudi. *Safe reinforcement learning with chance-constrained model predictive control.* Learning for Dynamics and Control Conference (L4DC) 2022.
- **[23]** Bastani, Li, Xu. *Safe reinforcement learning via statistical model predictive shielding.* Robotics: Science and Systems (RSS) 2021.
- **[24]** Liu, Lai. *Provably efficient black-box action poisoning attacks against reinforcement learning.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2021.
- **[25]** Ma, Zhang, Sun, Zhu. *Policy poisoning in batch reinforcement learning and control.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2019.
- **[26]** Wu, McMahan, Zhu, Xie. *Reward poisoning attacks on offline multi-agent reinforcement learning.* Proc. AAAI Conf. on Artificial Intelligence, 2023.
- **[27]** Liu, Lai. *Efficient adversarial attacks on online multi-agent reinforcement learning.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2023.
- **[28]** Li, Guo, Xiu, Feng, Yu, Liu, Wu, Liu. *Attacking Cooperative Multi-Agent Reinforcement Learning by Adversarial Minority Influence.* 2023.
- **[29]** Lu, Liu, Lai, Xu. *Camouflage Adversarial Attacks on Multiple Agent Systems.* 2024.
- **[30]** Figura, Kosaraju, Gupta. *Adversarial attacks in consensus-based multi-agent reinforcement learning.* American Control Conference (ACC) 2021.
- **[31]** Rakhsha, Radanovic, Devidze, Zhu, Singla. *Policy teaching via environment poisoning: training-time adversarial attacks against reinforcement learning.* ICML 2020.
- **[32]** Guo, Chen, Hao, Yin, Yu, Li. *Towards comprehensive testing on the robustness of cooperative multi-agent reinforcement learning.* IEEE/CVF CVPR 2022.
- **[33]** Xu, Wang, Raizman, Rabinovich. *Transferable environment poisoning: training-time attack on reinforcement learning.* AAMAS 2021.
- **[34]** Chen, Zheng, Gong. *Marnet: Backdoor attacks against cooperative multi-agent reinforcement learning.* IEEE Trans. Dependable and Secure Computing, 2022.
- **[35]** Xie, Xiang, Li, Zhao, Tong, Niu, Liu, Wang. *Security analysis of poisoning attacks against multi-agent reinforcement learning.* ICA3PP 2021, Springer.
- **[36]** Zheng, Li, Chen, Dong, Zhang, Lin. *One4all: Manipulate one agent to poison the cooperative multi-agent reinforcement learning.* Computers & Security, 2023.
- **[41]** Kono, Kamimura, Tomita, Murata, Suzuki. *Transfer learning method using ontology for heterogeneous multi-agent reinforcement learning.* Int. J. Advanced Computer Science and Applications, 2014.
- **[42]** Gao, Xu, Ding, Wang. *Knowru: Knowledge reuse via knowledge distillation in multi-agent reinforcement learning.* Entropy, 2021.
- **[43]** Nekoei, Badrinaaraayanan, Courville, Chandar. *Continuous coordination as a realistic scenario for lifelong learning.* ICML 2021.
- **[44]** Hussenot, Geist, Pietquin. *Targeted attacks on deep reinforcement learning agents through adversarial observations.* arXiv:1905.12282, 2019.
- **[45]** Qiaoben, Ying, Zhou, Su, Zhu, Zhang. *Understanding adversarial attacks on observations in deep reinforcement learning.* Science China Information Sciences, 2021.
- **[46]** Ashcraft, Karra. *Poisoning deep reinforcement learning agents with in-distribution triggers.* ICLR 2021 Workshop on Security and Safety in Machine Learning Systems.
- **[47]** Kiourti, Wardega, Jha, Li. *Trojdrl: evaluation of backdoor attacks on deep reinforcement learning.* ACM/IEEE Design Automation Conference (DAC) 2020.
- **[48]** Rauber, Brendel, Bethge. *Foolbox: A python toolbox to benchmark the robustness of machine learning models.* Reliable Machine Learning in the Wild Workshop, ICML 2017 (arXiv:1707.04131).
- **[49]** Adeyemo, Khalid, Odetola, Hasan. *Security analysis of capsule network inference using horizontal collaboration.* IEEE MWSCAS 2021.
- **[50]** Voss, Rademacher, Belkin. *Fast algorithms for gaussian noise invariant independent component analysis.* NeurIPS (Adv. Neural Inf. Process. Syst.) 2013.
- **[51]** Zhang, Zhang, Gong, Yang, Zhang, Chen, He. *Robustness evaluation of multi-agent reinforcement learning algorithms using gnas.* 2023.
- **[52]** Tekgul, Wang, Marchal, Asokan. *Real-time adversarial perturbations against deep reinforcement learning policies: attacks and defenses.* ESORICS 2022, Springer.
- **[53]** Korkmaz. *Non-robust feature mapping in deep reinforcement learning.* ICML 2021 Workshop on Adversarial Machine Learning.
- **[54]** Standen, Kim, Szabo. *Sok: Adversarial machine learning attacks and defences in multi-agent reinforcement learning.* arXiv:2301.04299, 2023.
- **[55]** Korkmaz. *Investigating vulnerabilities of deep neural policies.* Uncertainty in Artificial Intelligence (UAI) 2021.
- **[56]** Korkmaz. *Adversarial training blocks generalization in neural policies.* NeurIPS 2021 Workshop on Distribution Shifts.
- **[57]** Quiring, Rieck. *Backdooring and poisoning neural networks with image-scaling attacks.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[58]** Hu, Shi. *Impact of scaled image on robustness of deep neural networks.* arXiv:2209.02132, 2022.
- **[59]** Wang, Zhang, Li, Pan. *Dba: downsampling-based adversarial attack in medical image analysis.* Third International Conference on Computer Vision and Pattern Analysis (ICCPA 2023), SPIE.
