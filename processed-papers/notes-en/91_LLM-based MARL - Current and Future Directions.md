# 91. LLM-based Multi-Agent Reinforcement Learning: Current and Future Directions

## Metadata
- **Title**: LLM-based Multi-Agent Reinforcement Learning: Current and Future Directions
- **Authors**: Chuanneng Sun, Songjun Huang, Dario Pompili
- **Affiliation**: Department of Electrical and Computer Engineering, Rutgers University–New Brunswick, NJ, USA
- **Venue**: Submitted to IEEE Robotics & Automation Letters, May 2024 (arXiv:2405.11106v1, cs.MA, 17 May 2024)
- **Link/arXiv**: arXiv:2405.11106v1

## Taxonomy
- **Robustness / perturbation type targeted**: Survey/position paper; robustness discussed mainly as a forward-looking theme — safety and security in multi-agent systems (communication manipulation/eavesdropping, malicious data injection, adversarial attacks on the language model, model-bias exploitation, agent failure/anomaly detection and rollback). Not a single concrete perturbation model.
- **Method paradigm**: Literature survey of LLM-based single-agent RL and LLM-based MARL frameworks; CTDE, value-based / policy-based MARL, learning-to-communicate; proposed future directions (personality-enabled cooperation, human-in/on-the-loop, MARL–LLM co-design via distillation, safety/security with adversarial training and secure communication).
- **Keywords**: Multi-Agent Reinforcement Learning, Large Language Models, Multi-Agent Systems, language-conditioned MARL, cooperative tasks, safety and security

## TL;DR
A short survey letter that reviews conventional MARL, LLM-based single-agent RL, and the nascent body of LLM-based MARL frameworks for cooperative tasks, then lays out four future research directions (personality-enabled cooperation, language-enabled human-in/on-the-loop, traditional MARL–LLM co-design, and safety/security in MAS), claiming to be among the first systematic overviews dedicated to LLM-based MARL.

## Problem & Motivation
MARL improves scalability and robustness for coordination in multi-agent systems, but how and what to communicate among agents remains open, and learned numerical/neural communication protocols still underperform human experts. Recent LLM advances suggest leveraging human knowledge and natural language to enable richer inter-agent communication and coordination. Extending LLM-based single-agent RL to multi-agent systems is non-trivial because coordination and communication between agents are not modeled in single-agent RL frameworks. Existing surveys cover either LLM-based multi-agent frameworks (not focused on MARL), conventional MARL, or single-agent LLM-based RL, but none is dedicated to LLM-based MARL — the gap this letter targets, focusing on cooperative tasks with a common goal and communication, plus human-in/on-the-loop scenarios.

## Robustness Setting
- **Threat model / uncertainty set**: Not a formal threat model. The paper discusses, as future work, security threats specific to integrating LLMs into MARL: manipulation of agent communication, eavesdropping, injection of malicious data, adversarial attacks during/against LLM training, exploitation of model biases, and post-deployment vulnerabilities/anomalies. Defenses suggested include secure/encrypted communication protocols, adversarial training, input validation, real-time anomaly monitoring, and isolating/rolling back affected agents.
- **Setting**: Cooperative multi-agent tasks with a common goal and communication; modeled as Dec-POMDP; CTDE discussed (e.g., LLM as a centralized critic). Both human-in-the-loop and human-on-the-loop scenarios considered. Survey scope (no single online/offline algorithm).

## Method
- Defines MARL via the Dec-POMDP (extension of the MDP), with per-agent policies/observations and individual rewards, and notes partial observability as the key difficulty motivating coordinated learning and actor–critic structures.
- Categorizes conventional (non-LLM) MARL into "learning-to-coordinate" (e.g., QMIX, QTRAN, MADDPG, MAPPO; policy-based vs. value-based; CTDE; credit-assignment problem) and "learning-to-communicate" (adjusting message content, optimizing communication network structure, differentiable inter-agent learning, emergent communication protocols/languages).
- Surveys LLM-based single-agent RL: "open-loop" frameworks that ignore environment reward (ReAct, Reflexion, ADaPT) and "closed-loop" frameworks that incorporate feedback (Refiner, LLM-feedback credit assignment, Retroformer, REX), plus multi-modal control models (PaLM-E, language grounding to actions).
- Surveys existing LLM-based MARL frameworks split into "MARL for problem solving" (γ-Bench, DyLAN, FAMA, consensus seeking, Theory-of-Mind, MetaGPT) and "MARL for embodied applications" (CoELA, SMART-LLM, RoCo, Co-NavGPT, Guo et al.), summarized in Table I.
- Proposes four future directions: personality-enabled cooperation via prompts; language-enabled human-in/on-the-loop frameworks; traditional MARL and LLM co-design (LLM as centralized critic; knowledge/in-context distillation into small onboard models; specialized communication protocols and hardware); and safety/security in MAS (continuous action spaces, secure/encrypted communication, adversarial training, input validation, reactive monitoring/rollback).

## Theoretical Contributions
None / mostly empirical (survey and position paper; no theorems, convergence, or sample-complexity results).

## Experiments
- **Environment/Benchmark**: Not specified (survey; no experiments conducted). Table I catalogs benchmarks/simulators used by surveyed works (e.g., MATH, MMLU, HumanEval, MBPP, BabyAI-Text, Traffic Junction, TDW-MAT, C-WAH, RoCoBench, Habitat-Matterport 3D, VirtualHome-Social).
- **Baselines**: Not specified (no comparative evaluation performed).
- **Evaluation metrics**: Not specified.

## Key Results
- Provides a systematic overview that the authors claim is among the first dedicated to LLM-based MARL, distinguishing it from prior surveys on LLM-based multi-agent frameworks, conventional MARL, and single-agent LLM-based RL.
- Organizes existing LLM-based MARL work into "problem solving" vs. "embodied applications," with Table I detailing application, dataset/simulator, whether training is used, and the LLM's role (decision, communication, memory, planning, ToM, etc.).
- Identifies four concrete future research directions and argues that, with LLMs, designing MARL becomes more analogous to modeling the group learning of animals/humans, where knowledge is exchanged via natural language.

## Limitations & Future Work
- It is a short letter/survey: no new algorithm, theory, or empirical evaluation; conclusions are qualitative.
- Continuous action spaces remain hard for LLM-based control; existing methods replace the LLM's last layers and require in-environment training that may be inaccessible — alternatives without substantial retraining are needed.
- On-board LLM inference is impractical for small robots; PEFT + quantization still require inference through the large network, motivating co-design and (in-context) distillation into compact onboard models, specialized communication protocols, and specialized hardware.
- Safety/security challenges (biased personalized language, communication manipulation/eavesdropping, adversarial attacks, anomaly detection and rollback) are open. Future work also includes personality-driven negotiation, benign competitive agents, context-aware human–agent dialogue, and new metrics for communication quality.

## Relevance to Survey
This paper sits at the intersection of MARL and large language models rather than on the formal robust-MARL theory line. Its relevance to a robust MARL survey comes primarily from Section IV-D ("Safety and Security in MAS"), which frames robustness, safety, and security concerns for LLM-augmented multi-agent systems: secure/encrypted communication against eavesdropping and malicious-data injection, adversarial training against attack vectors, input validation, and reactive anomaly detection with state rollback (fault tolerance). It also touches communication robustness (the "learning-to-communicate" line) and human-on-the-loop oversight for safety. Useful as a pointer to the LLM-based MARL research frontier and to where robustness/security challenges arise when language models mediate agent coordination.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Multi-Agent Reinforcement Learning (MARL) has emerged as a popular approach to address the coordination problem in Multi-Agent Systems (MAS). As opposed to Individual Reinforcement Learning (IRL)-based or traditional optimization-based solutions, MARL has shown a significant improvement in scalability and robustness to uncertainty and dynamicity [1]–[4]. This improvement is largely attributed to the communication and coordination among agents inherent in MARL, where multiple agents learn and adapt their policies simultaneously while interacting within a shared environment and communicating with others. However, how and what to communicate among the agents in the MAS remains to be explored. Representative examples include MARL frameworks that learn to generate numerical messages using neural networks, formulate neural communication protocols, and learn targeted ad hoc communications. Despite the decent performance of the MARL frameworks achieved in various applications, they still underperform human experts. As a result, it is reasonable to think why not leveraging human knowledge and human languages in MARL?"

> _[Introduction — positioning vs. prior surveys]_

"Guo et al. [20] reviewed LLM-based multi-agent frameworks, but the emphasis of that paper was not on MARL. Unlike their paper, this letter focuses more on the MAS that tries to accomplish a task cooperatively. In addition to that, there are several surveys on the topic of MARL [21]–[23] and single agent LLM-based RL [24], [25], but none of them is dedicated to LLM-based MARL. Therefore, we claim that we are among the first to provide a systematic overview of the LLM-based MARL problem and provide potential future research directions."

> _[Section II-B, Traditional MARL]_

"To solve the problem of Dec-POMDP, many frameworks have been proposed. These frameworks can be roughly categorized into two classes: learning-to-cooperate and learning-to-communicate.
Learning to coordinate: The first kind of approach, such as QMIX [27], QTRAN [28], MADDPG [29], MAPPO [30], and many others [31]–[36], assumes that through centralized training with ideal communication, agents can learn to work with each other during the centralized training; therefore, communication is not needed during execution. In other words, these approaches expect the agents to learn to adapt to other agents' behavior patterns. These approaches can also be classified as policy-based and value-based approaches. Policy-based approaches typically adopt the actor-critic architecture where actors are trained to make decisions, and critics approximate the long-term return and provide feedback to the actors. Value-based approaches learn optimized joint Q values given the team's observations and actions. A problem that often happens in this situation is the credit assignment problem, where the critic needs to determine the contribution of each agent to the performance.
Learning to communicate: In communication-based approaches, agents are equipped with the capability to share information through various means, such as adjusting the content of the shared messages [37] or optimizing the structure of the communication network [38]. This explicit inter-agent communication facilitates coordinated strategies and is crucial in dynamic environments where conditions and objectives may frequently change [39], [40]. Effective communication enables agents to form coalitions to achieve common goals, adapt to peers' actions, and optimize collective outcomes, improving system performance in tasks ranging from cooperative manipulation to competitive strategic games [37]. Protocols for communication, often learned during training, leverage advanced techniques such as differentiable interagent learning algorithms, which refine communication patterns based on environmental feedback [41]–[43]. In addition, frameworks for learning emergent communication protocols/languages have also been proposed [44], [45]. These frameworks encourage the agents to learn a certain "language" that is understandable by other agents and encodes certain information."

> _[Section IV-D, Safety and Security in MAS]_

"Ensuring the safety and security of MAS is critical, especially as these systems are increasingly deployed in diverse and potentially high-stakes environments. The integration of language models into MARL introduces unique challenges and vulnerabilities, from the manipulation of agent communication to the exploitation of model biases.
Many robotic operations have continuous action spaces, where the output of each agent's policy is a set of continuous values. Unlike discrete action spaces, which can be reformulated as multi-choice problems and solved by prompting the multi-choice question to the LLM, continuous action space is more tricky, especially in high-stake environments, for example, operation robots. Existing methods replace the last few layers of the LLMs with new layers that map the observation in languages to continuous action spaces. However, this kind of approach requires training the new layers in the desired environment, which might be inaccessible. Therefore, exploring alternative methods for integrating LLMs into the control loop of robots operating in continuous action spaces without the need for substantial retraining or modification of the LLMs is promising.
In addition to safety in actions, safety and security against potential attacks are also crucial in MAS. One way towards safety is through proactive measures. This includes the development of secure communication protocols between agents to prevent eavesdropping or the injection of malicious data that could lead to compromised decision-making. Communications encryption can be a fundamental aspect of this, ensuring that even if data transmissions are intercepted, the information remains protected. In addition, securing the language model training process against adversarial attacks is crucial. Adversarial training, which involves exposing the system to a wide range of attack vectors during the training phase, can help models learn to resist or mitigate these attacks in deployment. In addition, input validation techniques can be employed to filter out potentially harmful or misleading inputs that could cause the system to behave unpredictably. This is particularly important in scenarios where agents interact with humans or systems outside the controlled environment and are exposed to a broader range of language inputs and behaviors.
Despite the best proactive defenses, systems may still encounter unforeseen vulnerabilities post-deployment. Thus, reactive strategies are necessary to quickly address any breaches or failures. This can involve real-time monitoring of agent behaviors and communications to detect anomalies that may indicate a security breach or a failure in safety protocols. Once an anomaly is detected, the systems should be able to isolate affected agents and roll back their states to secure configurations."

### Cited references (resolved from the paper's bibliography)
- **[1]** Sun, Huang, Pompili. *HMAAC: Hierarchical multi-agent actor-critic for aerial search with explicit coordination modeling.* IEEE ICRA 2023.
- **[2]** Shalev-Shwartz, Shammah, Shashua. *Safe, multi-agent, reinforcement learning for autonomous driving.* arXiv:1610.03295, 2016.
- **[3]** Sadhu, Sun, Karimian, Tron, Pompili. *Aerial-DeepSearch: Distributed multi-agent deep reinforcement learning for search missions.* IEEE MASS 2020.
- **[4]** Calvo, Dusparic. *Heterogeneous multi-agent deep reinforcement learning for traffic lights control.* AICS 2018.
- **[20]** Guo, Chen, Wang, Chang, Pei, Chawla, Wiest, Zhang. *Large language model based multi-agents: A survey of progress and challenges.* arXiv:2402.01680, 2024.
- **[21]** Nguyen, Nguyen, Nahavandi. *Deep reinforcement learning for multiagent systems: A review of challenges, solutions, and applications.* IEEE Transactions on Cybernetics 2020.
- **[22]** Hernandez-Leal, Kartal, Taylor. *A survey and critique of multiagent deep reinforcement learning.* Autonomous Agents and Multi-Agent Systems 2019.
- **[23]** Gronauer, Diepold. *Multi-agent deep reinforcement learning: a survey.* Artificial Intelligence Review 2022.
- **[24]** Luketina, Nardelli, Farquhar, Foerster, Andreas, Grefenstette, Whiteson, Rocktäschel. *A survey of reinforcement learning informed by natural language.* arXiv:1906.03926, 2019.
- **[25]** Cao, Zhao, Cheng, Shu, Liu, Liang, Zhao, Li. *Survey on large language model-enhanced reinforcement learning: Concept, taxonomy, and methods.* arXiv:2404.00282, 2024.
- **[27]** Rashid, Samvelyan, De Witt, Farquhar, Foerster, Whiteson. *Monotonic value function factorisation for deep multi-agent reinforcement learning (QMIX).* JMLR 2020.
- **[28]** Son, Kim, Kang, Hostallero, Yi. *QTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning.* ICML 2019.
- **[29]** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments (MADDPG).* NeurIPS 2017.
- **[30]** Yu, Velu, Vinitsky, Gao, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative multi-agent games (MAPPO).* NeurIPS 2022.
- **[31]** Sunehag, Lever, Gruslys, Czarnecki, Zambaldi, et al. *Value-decomposition networks for cooperative multi-agent learning based on team reward.* AAMAS 2018.
- **[32]** Rashid, Farquhar, Peng, Whiteson. *Weighted QMIX: Expanding monotonic value function factorisation for deep multi-agent reinforcement learning.* NeurIPS 2020.
- **[33]** Wang, Ren, Liu, Yu, Zhang. *QPLEX: Duplex dueling multi-agent Q-learning.* ICLR 2021.
- **[34]** Ackermann, Gabler, Osa, Sugiyama. *Reducing overestimation bias in multi-agent domains using double centralized critics.* arXiv:1910.01465, 2019.
- **[35]** Wang, Han, Wang, Dong, Zhang. *DOP: Off-policy multi-agent decomposed policy gradients.* ICLR 2020.
- **[36]** Zhang, Li, Wang, Xie, Lu. *FOP: Factorizing optimal joint policy of maximum-entropy multi-agent reinforcement learning.* ICML 2021.
- **[37]** Foerster, Assael, De Freitas, Whiteson. *Learning to communicate with deep multi-agent reinforcement learning.* NeurIPS 2016.
- **[38]** Das, Gervet, Romoff, Batra, Parikh, Rabbat, Pineau. *TarMAC: Targeted multi-agent communication.* ICML 2019.
- **[39]** Sukhbaatar, Fergus, et al. *Learning multiagent communication with backpropagation.* NeurIPS 2016.
- **[40]** Hoshen. *VAIN: Attentional multi-agent predictive modeling.* NeurIPS 2017.
- **[41]** Jiang, Lu. *Learning attentional communication for multi-agent cooperation.* NeurIPS 2018.
- **[42]** Mordatch, Abbeel. *Emergence of grounded compositional language in multi-agent populations.* AAAI 2018.
- **[43]** Shen, Fu, Su, Pan, Qiao, Dou, Wang. *GraphComm: A graph neural network based method for multi-agent reinforcement learning.* IEEE ICASSP 2021.
- **[44]** Gupta, Hazra, Dukkipati. *Networked multi-agent reinforcement learning with emergent communication.* arXiv:2004.02780, 2020.
- **[45]** Lazaridou, Baroni. *Emergent multi-agent communication in the deep learning era.* arXiv:2006.02419, 2020.
