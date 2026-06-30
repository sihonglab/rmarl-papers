# 184. A Survey on Fault Tolerant Multi Agent System

## Metadata
- **Title**: A Survey on Fault Tolerant Multi Agent System
- **Authors**: Yasir Arfat, Fathy Elbouraey Eassa
- **Affiliation**: Department of Computer Science, King Abdul Aziz University, Jeddah, Saudi Arabia
- **Venue**: International Journal of Information Technology and Computer Science (IJITCS), Vol.8, No.9, pp.39-48, 2016 (MECS Press)
- **Link/arXiv**: DOI: 10.5815/ijitcs.2016.09.06

## Taxonomy
- **Robustness / perturbation type targeted**: Agent failure / fault tolerance in multi-agent systems (MAS) — machine crashes, process failure, software failure, communication failure, hardware failure; faults classified as "fail silent" (crash-type) and "fail uncontrolled". Not an RL / robust-MARL learning paper; robustness here means classical distributed-systems fault tolerance.
- **Method paradigm**: Survey / taxonomy of fault tolerance techniques — replication-based (active, passive, adaptive), non-replication-based (architecture-oriented and mathematical/algorithmic), and hybrid approaches; qualitative comparison and evaluation. (No learning/RL algorithm; not minimax, certified robustness, or game-theoretic equilibrium.)
- **Keywords**: Multi Agent System, Fault Tolerance, Agents, Adaptive Replication, Redundancy

## TL;DR
A survey that classifies fault-tolerant multi-agent systems (FTMAS) by recovery technique, presents a taxonomy of both faults and techniques, and gives a qualitative comparison and evaluation of existing approaches, concluding that most existing schemes are inefficient due to high computation cost, costly replication, and large communication overheads.

## Problem & Motivation
Multi-agent systems operate in distributed environments and are prone to failure (agent failure, machine crashes, process failure, software/communication/hardware failure), which makes resources unavailable and delays goal achievement, decreasing performance and reliability. To increase reliability, a MAS should be fault tolerant and able to mask failures so it can keep providing services. Many researchers have proposed fault tolerance approaches, so the paper surveys them to provide a taxonomy, qualitative comparison, and evaluation, and to identify which technique is most appropriate (efficient, low overhead, low cost) for masking faults in MAS.

## Robustness Setting
- **Threat model / uncertainty set**: Faults/failures in a distributed MAS, divided into "fail silent" (crash-type) and "fail uncontrolled" (any type of fault/failure). Specific failure types surveyed include machine crashes, end of broker process, network breakdown, host failure, process failure, software entity failure, physical component failure, partial agent failure, and actuator faults. No probabilistic uncertainty set or adversary model (not an RL formulation).
- **Setting**: Cooperative multi-agent systems in distributed environments; both centralized and decentralized architectures are discussed. Not framed as CTDE / online / offline learning. Not specified in RL terms.

## Method
- Surveys ten existing FTMAS works (Kumar et al., Marin et al., Almeida et al., Khan et al., Almeida et al. plane-based, Singh et al., Koppensteiner et al., Bora et al., Mirian et al., Khalili et al.) describing each technique's assumptions, objectives, methodology, and key approach.
- Presents a taxonomy of faults (fail silent vs. fail uncontrolled, further subdivided) and a taxonomy of techniques: replication-based (active, passive, adaptive), non-replication-based (architecture-oriented; mathematical/algorithmic), and hybrid.
- Provides a qualitative comparison (Table 1) along eight parameters: agent type, fault tolerance technique, objectives, language, type of failure, replication protocol, characteristics, and environment.
- Summarizes pros and cons of each surveyed technique (Table 2) and conducts an evaluation discussion of the schemes' effectiveness, overheads, reliability, and computational cost.

## Theoretical Contributions
None / mostly survey. No convergence, sample complexity, equilibrium, or certified-robustness results. The contribution is a threefold survey: taxonomy of faults and techniques, qualitative comparison, and evaluation of existing approaches.

## Experiments
- **Environment/Benchmark**: Not specified (survey paper; no original experiments). Surveyed works use frameworks such as DARX and DIMA and languages such as KQML and ACL, but the survey itself runs no benchmark.
- **Baselines**: Not specified (the surveyed FTMAS approaches are compared against each other qualitatively rather than via an empirical baseline).
- **Evaluation metrics**: Qualitative comparison parameters: agent type, fault tolerance technique, objectives, language, type of failure, replication protocol, characteristics, environment; pros/cons assessed by overheads of fault recovery, reliability, performance improvement, and computational cost.

## Key Results
- Researchers apply replication and non-replication based fault recovery approaches for FTMAS; techniques can be grouped into replication-based, non-replication-based, and hybrid.
- Most existing schemes are not very efficient due to high computation costs, costly replication, and large communication overheads.
- When proposing fault tolerance techniques, researchers often ignored other aspects (overheads, expensive computation), which decreased system reliability and MAS performance.
- For example, Singh et al. [16] report that fifty percent actively replicated agents can remove system complexity; decentralized architectures (Khan et al. [14]) are reported less faulty, more reliable, and faster than centralized ones.

## Limitations & Future Work
- Most existing fault tolerance approaches do not provide basic fault recovery features in MAS such as reliability, scalability, adaptability, and robustness.
- The distributed nature of MAS, prone to failure at any time, makes designing fault-tolerant architecture a complex challenge.
- There is no standard evaluation framework for FTMAS for comparison purposes; each researcher uses their own criteria.
- MAS lacks reliable programming tools and specialized debugging tools, and skills are needed to move from analysis/design to coding, plus difficulties in understanding the environment and methodology.
- Need for an appropriate technique that provides fault tolerance with fewer overheads and lower computational cost.

## Relevance to Survey
This is a 2016 survey of classical fault-tolerance techniques (replication, redundancy, heartbeat, adaptive recovery) for multi-agent systems, predating the robust-MARL literature and containing no reinforcement learning. For a Robust MARL survey it is relevant as background on the "agent failure / fault tolerance / Byzantine-style robustness" theme in MAS — it motivates why agent and communication failures matter in cooperative multi-agent settings and provides a taxonomy of fault types and recovery strategies that can frame later learning-based robustness work. It connects to the fault-tolerance and communication-robustness sub-lines rather than to robust MDP / adversarial / distributionally robust RL methods.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Background]_

"In multi agent systems (MAS), several agents are working together to achieve task-oriented goals on behalf of the user or human ref. Maciel et al.[6] Successful interaction is required among agents in MAS to negotiate, coordinate and cooperate with each agent in the environment ref. Gerrard et al.[7] The best examples of MAS are Internet agents and as used in Spacecraft control ref. Li et al.[8] Nowadays, researchers and developers alike are using the agent in the distributed environment, such as those used as environment agents who need co-ordination, co-operation, and negotiation. These are the basic issues that MAS has in each environment ref. Davoodi et al.[9]. As the failure rate increases when there is less co-ordination, co-operation and communication among the agents, this leads to the failure of the system. Hence, these types of failures are subject to the host, machine and exception set ref. Wang al.[10]. There are several fault tolerance MAS techniques that have been proposed to mask the faults in MAS. Each technique differs in its ability to mask failure in MAS."

> _[Section III, Literature Review — A. Towards FTMAS Architecture]_

"Kumar et al. [11] describe that there were many possibilities that failure could happen at any time in MAS of any distributed system. Many agents were not available due to process failure, exceptions and breakdown of communication. There were many faults that existed ranging from database recovery, TS monitoring, resource manager and fault tolerance distributive systems up to application server. There were many issues in these techniques, such as using replication schemes as a critical system for monitoring. However, when it increases the reliability of the system it duplicates the data and services. Moreover, many systems saved the application state but it also created many problems during recovery. To overcome this traditional fault tolerance technique they proposed Adaptive Agent Architecture (AAA) for the multi-agent system (MAS). Whereby, AAA overcomes a problem like a broker failure without incurring undue overheads. There may be more than one of many such brokers in the large multi-agent system. In the case of sudden unavailability of a broker in AAA, they used the team based approach for automatic recovery of MAS. Furthermore for the recovery, they assumed three different recovery schemes, namely logical characterization, recovery scheme and recovery scenario. In these assumptions, they described different steps, theorems and characterizations of performance. Their results show that autonomous agents can make a multi-agent system more robust."

> _[Section III, Literature Review — B. Towards Adaptive FTDMAS]_

"Marin et al. [12] have also proposed an adaptive architecture for the multi-agent system (MAS). It deals with existing problems in MAS using new methodologies. MAS as a distributed system may by its very nature accrue failure at any time in the system. Moreover, due to it being a distributed system, computations of dynamic applications were often changed, during execution. Nevertheless, they tried to make it more flexible to overcome the flaws of the conventional system. On the proposed architecture, we can either replicate or replicate the software element on the spot. The advantage of this approach is that we can change replication tactics in a matter of a few seconds. The main objective of selected architecture is to make fault tolerance more efficient for MAS, using selective replication techniques. An outcome of this approach is to develop architecture, which is suitable for dynamic fault tolerance for applications. They used the selective replication scheme as many problems existed for approaches to dynamic applications. Moreover, they also introduced a framework namely, (dynamic adaptive replication extension) DARX, which uses both active and passive replication, specially designed for the distributed application."

> _[Section III, Literature Review — C. Towards Automatic FTMAS]_

"Almeida et al. [13] presented an automated fault tolerance (FT) MAS scenario. They described that there are many possibilities whereby an exception or failure can occur at any time in the system. These failures occur when recovery and fault tolerance approaches are defined at the design level. Indeed, it is very difficult to decide at the design level when and where to apply the FT approach (i.e. replication). But conventional approaches are out of order when it comes to dynamic systems (i.e. MAS). These applications could be ambient intelligence systems, related to e-commerce, crisis management systems or the air traffic control system. According to the situation and nature of interdependencies in these applications, an agent can change their role during the computation stage. Therefore, to overcome all difficulties and to make the FT management automatic and dynamic, they considered a self-adaptation FT approach."

> _[Section III, Literature Review — D. Decentralized Architecture for FTMAS]_

"Khan et al. [14] presented fault tolerant decentralized architecture for the multi-agent system. Most applications have a lack of fault tolerance. There is an expectation that usage of MAS in different distributed applications will increase. However, there are many faults existing within the agent platform, causing a multitude of problems. To overcome all these problems they introduced decentralized architecture, as an alternative to the centralized architecture of the agent platform (AP). Figure 2 shows the working of decentralized architecture, namely Virtual Agent Cluster (VAC). When a single agent platform is deployed it includes all machines. A similarity exists between virtual agent cluster and cluster computing, where the front processor distributes the load among the machines."

> _[Section III, Literature Review — E. Plane-Based Replication for FTMAS]_

"Almeida et al. [15] presented a plane-based replication of the fault tolerant multi-agent system. In their proposed scheme, they used this method for stipulating the dependability for MAS through replication. This method is different from others cited above, here they focus on predictive and adaptive replication whereby the critical agents are replicated to overcome failures. As some of the application uses static replication, in contrast here they use dynamic replication. The latter has advantages over static replication i.e. re-allocation of tasks, changing the role of an agent, flexible organization etc. Moreover, it is very important to replicate an agent through dynamic and automatic means. Here, they are more focused on building reliable MAS. ... They also validated their approach on the DARX framework and DIMA."

> _[Section III, Literature Review — F. Adaptive and Automated FTMAS]_

"Singh et al. [16] have proposed this framework for a critical agent in the multi-agent system (MAS), based on the cardinality of an agent. Sometimes replication can become very costly due to the complexity of the system; moreover, dynamic replication is also a need of all agents in fault tolerance MAS. Hence, to overcome these issues they proposed this particular framework. They mixed two techniques namely, active and passive replication. Thereby, critical agents will actively replicate, more focused relatively to other agents."

> _[Section III, Literature Review — G. Hybrid Based Approach for FTMAS]_

"Koppensteiner et al. [17] have proposed a hybrid fault tolerance multi-agent system using the heartbeat mechanism. They used this mechanism to detect failure in MAS. They found three different types of failures here, namely: 1) System disturbance 2) Physical Component Failure and 3) Software Entity Failure. To recover from physical component failure i.e. a failure in tangible hardware or failure in block base application controlling function, they introduced the heartbeat mechanism. Using the heartbeat between the LLC (Low-Level Control layer) and HLC (High-Level Control layer) they minimized messages to maintain the system's stability."

> _[Section III, Literature Review — H. Choice of Sampling Rates in FTMAS]_

"Bora et al. [18] proposed fault tolerance in a multi-agent system based on the sampling period. To increase the fault tolerance in distributed and dynamic systems, adaptive replication techniques were very useful. But there is one disadvantage of this approach; it increases the cost due to adaptive replication. To overcome this drawback, a sampling period was introduced to minimize the cost. This technique whereby it monitors critical agents, properly chooses the appropriate replication for the agent based on its criticality."

> _[Section III, Literature Review — I. A Decision-making based approach for Fault Handing in Multi-Agent System]_

"Mirian, Maryam S. et al. [19] introduced a new decision-based technique for fault handling in the multi-agent system. They described the multi-agent system more like a distributed system where fault can occur at any time in the system. In the paper, they focused on the faulty agent and their recovery in the multi-agent system. In the presented technique, if a fault agent requests its other agents or its team agents come to know that this agent is faulty and needs help, then there are several help requests that exist. ... For this methodology there is no central agent, all agents are decentralized. Each agent has knowledge about the environment and existing agents in the environment. They all also have the ability to perform the task of other agents. If an agent fails in the system another agent can help based on the decision-making phase."

> _[Section III, Literature Review — J. Distributed Adaptive Fault-Tolerant Consensus Control of Multi-Agent System with Actuator Faults]_

"Khalili et al. [20] presented a distributed FT consensus control of MAS with actuator faults. This FTMAS is based on three different assumptions. In this distributed system an FT control component was developed to perform a two-step process between the agents. The first would diagnose the fault in the MAS while the second would provide an opportunity to recover in an adaptive manner. These assumptions are constructed using mathematical equations and in particular, vectors. Using the assumptions, it can check the system's stability with the closed-loop mechanism. The main objective of this system is to develop an algorithm that diagnoses and recovers faults. A unique feature of this algorithm is that it takes an information-neighboring algorithm and applies its actions."

### Cited references (resolved from the paper's bibliography)
- **[6]** Maciel, Souza, Viterbo, Mendes, El Fallah Seghrouchni. *A Multi-agent Architecture to Support Ubiquitous Applications in Smart Environments.* In Agent Technology for Intelligent Mobile Services and Smart Societies, pp. 106-116, Springer 2015.
- **[7]** Gerrard, McCall, Macleod, Coghill. *Applications and design of cooperative multi-agent ARN-based systems.* Soft Computing 2015.
- **[8]** Li, Li, Shen, Bi, Sun. *Risk assessment model based on multi-agent systems for complex product design.* Information Systems Frontiers 17(2):363-385, 2015.
- **[9]** Davoodi, Khorasani, Talebi, Momeni. *Distributed fault detection and isolation filter design for a network of heterogeneous multiagent systems.* IEEE Transactions on Control Systems Technology 22(3):1061-1069, 2014.
- **[10]** Wang, Song, Lewis. *Robust Adaptive Fault-tolerant Control of Multi-agent Systems with Uncertain Non-identical Dynamics and Undetectable Actuation Failures.* 2015.
- **[11]** Kumar, Cohen. *Towards fault-tolerant multi-agent system architecture.* Proceedings of the fourth international conference on Autonomous Agents, ACM 2000.
- **[12]** Marin, Sens, Briot, Guessoum. *Towards adaptive fault tolerance for distributed multi-agent systems.* Proceedings of ERSADS, pp. 195-201, 2001.
- **[13]** Almeida, Briot, Aknine, Guessoum, Marin. *Towards autonomic fault-tolerant multi-agent systems.* 2nd Latin American Autonomic Computing Symposium (LAACS'2007), Petropolis, Brazil, 2007.
- **[14]** Khan, Shahid, Ahmad, Ali, Suguri. *Decentralized architecture for fault tolerant multi agent system.* Autonomous Decentralized Systems (ISADS 2005), pp. 167-174, IEEE 2005.
- **[15]** Almeida, Aknine, Briot, Malenfant. *Plan-based replication for fault-tolerant multi-agent systems.* Proceedings of the 20th International Conference on Parallel and Distributed Processing, p. 347, Rhodes Island, Greece, April 2006.
- **[16]** Singh, Juneja, Sharma. *Adaptive and automated fault-tolerance for multi-agent systems.* Computer Science and Automation Engineering (CSAE), vol. 1, pp. 53-57, IEEE 2011.
- **[17]** Koppensteiner, Merdan, Lepuschitz, Hegny. *Hybrid based approach for fault tolerance in a multi-agent system.* Advanced Intelligent Mechatronics (AIM 2009), pp. 679-684, IEEE/ASME 2009.
- **[18]** Bora, Dikenelli. *On the choice of sampling rates in a fault-tolerant multi-agent system.* 2012 International Symposium on Innovations in Intelligent Systems and Applications, 2012.
- **[19]** Mirian, Nili Ahmadabadi, Navabi. *A decision-making based approach for fault-handling in multi-agent systems.* Neural Information Processing (ICONIP'02), vol. 4, pp. 1905-1909, IEEE 2002.
- **[20]** Khalili, Zhang, Cao, Muse. *Distributed Adaptive Fault-Tolerant Consensus Control of Multi-Agent Systems with Actuator Faults.* (Year not specified in bibliography.)
