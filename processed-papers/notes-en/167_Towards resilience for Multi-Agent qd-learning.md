# 167. Towards Resilience for Multi-Agent QD-Learning

## Metadata
- **Title**: Towards Resilience for Multi-Agent QD-Learning
- **Authors**: Yijing Xie, Shaoshuai Mou, Shreyas Sundaram
- **Affiliation**: Purdue University, West Lafayette, IN (College of Engineering; School of Aeronautics and Astronautics; School of Electrical and Computer Engineering)
- **Venue**: Not specified (arXiv preprint; eess.SY)
- **Link/arXiv**: arXiv:2104.03153v1 [eess.SY] 7 Apr 2021

## Taxonomy
- **Robustness / perturbation type targeted**: Byzantine/fault tolerance — adversarial (Byzantine) agents in a networked peer-to-peer MARL system that can behave arbitrarily and send conflicting/incorrect values to neighbors.
- **Method paradigm**: Resilient distributed Q-learning (QD-learning) with consensus + innovations; trimmed-mean / value-filtering (removing F highest and F lowest neighbor values); robust network topology ((2F+1)-robust graphs); almost-sure convergence analysis.
- **Keywords**: Byzantine agents, resilient MARL, distributed QD-learning, F-local adversary model, (2F+1)-robust graph, consensus

## TL;DR
The paper proposes a resilient distributed QD-learning algorithm for networked (peer-to-peer) MARL that tolerates Byzantine agents by filtering out the F highest and F lowest neighbor Q-value estimates, proving almost-sure convergence of every regular agent's value function to a neighborhood of the optimal value function of all regular agents when the network is (2F+1)-robust and adversaries form an F-local set.

## Problem & Motivation
Distributed MARL algorithms (e.g., QD-learning) rely on local coordination among neighbors, which makes them vulnerable: even a single malicious/compromised agent under cyberattack can corrupt the entire learning process. The authors show that the standard QD-learning algorithm generally fails in the presence of even a single adversarial agent (a fixed-value adversary can drive all regular agents to an arbitrary value, and any optimality-guaranteeing algorithm can be arbitrarily co-opted and remain undetected). This motivates a resilient algorithm that, accepting that exact optimality is impossible under adversaries, instead approximately learns the optimal value function and policy of the regular agents.

## Robustness Setting
- **Threat model / uncertainty set**: Byzantine agents (Definition 2) that may behave arbitrarily, send conflicting/incorrect values to different neighbors at each time-step, and know the network topology and private information of all other agents. Adversaries form an F-local set (Definition 5): each regular agent has at most F adversarial neighbors. The agent network is time-invariant and (2F+1)-robust (Assumption 4). The node set V is partitioned into regular nodes R and adversarial nodes A = V \ R, unknown a priori to regular nodes.
- **Setting**: Fully cooperative; decentralized / networked peer-to-peer (no central coordinator), but assuming a global controller whose actions are visible to all agents (to focus on resilient learning); online model-free distributed Q-learning.

## Method
- Extends the undirected-network distributed QD-learning of [1] to time-varying directed (rooted) networks; each agent maintains Q-value estimates for all state-action pairs, updated via a consensus term (driving agreement with neighbors) plus an innovation term (the local Q-learning portion).
- Establishes for the (non-adversarial) directed/time-varying case: boundedness of Q-value estimates (Proposition 1), asymptotic consensus (Proposition 2), and convergence to a neighborhood of the optimal value function within radius R (Proposition 3).
- Characterizes adversarial vulnerability: a fixed-value adversary drags all regular agents to its arbitrary value (Proposition 4), and any algorithm that is optimal without adversaries can be co-opted to an arbitrary value undetected (Proposition 5) — "the price for resilience is a loss of optimality (in general)."
- Resilient QD-learning (Algorithm 1): each regular agent receives neighbors' Q-values, removes the F largest values above and F smallest values below its own estimate, and runs the consensus + innovation update only over the retained neighbor set J^n_{i,u}(t).
- Uses the F-local adversary model and (2F+1)-robust topology so that, after trimming, the regular-agent subgraph remains rooted, enabling the convergence proof to carry over.

## Theoretical Contributions
- **Theorem 1**: Under Assumptions 1, 2, 4, Algorithm 1 guarantees for each regular agent vn ∈ R that lim sup ‖Qⁿ_t − Q^{R*}‖∞ ≤ R and lim sup ‖Vⁿ_t − V^{R*}‖∞ ≤ R almost surely, where R = max_{vn,vl∈R} ‖Qⁿ* − Q^{l*}‖∞. If |Q^{R*}_{i,u} − Q^{R*}_{i,v}| ≥ 2R for all actions, each regular agent learns the optimal policy π^{R*} of all regular agents.
- Bounds on each regular agent's Q-values: lim sup Qⁿ_{i,u}(t) ≤ M^R and lim inf Qⁿ_{i,u}(t) ≥ m^R a.s. (Eqs. 13–14), with M^R, m^R the max/min local optimal Q-values over regular agents.
- Negative results (Propositions 4 and 5) proving impossibility of exact optimality under a single adversary.
- Supporting analysis: Proposition 1 (boundedness), Proposition 2 (consensus), Proposition 3 (convergence for time-varying directed networks), Lemma 1 (equivalent trimmed update using [5], [18]), plus preliminary Lemmas 2–4 in the appendix; Remark 4 gives a further bound R ≤ max_{vn,vl∈R} (1/(1−γ)) ‖E[cn] − E[cl]‖∞, with R = 0 when all regular agents share the same local optimal value functions/costs.

## Experiments
- **Environment/Benchmark**: Not specified (the paper is theoretical; no empirical experiments are reported).
- **Baselines**: Not specified.
- **Evaluation metrics**: Not specified.

## Key Results
- Standard QD-learning is not resilient: a single fixed-value Byzantine agent forces all regular agents' Q-values and value functions to converge to the adversary's arbitrary value (Proposition 4); any non-resilient optimal algorithm can be co-opted to an arbitrary value and remain undetected (Proposition 5).
- The proposed resilient QD-learning algorithm guarantees almost-sure convergence of each regular agent's value function to within radius R of the optimal value function of all regular agents, regardless of Byzantine behavior (Theorem 1).
- The convergence radius R shrinks as regular agents' local optimal value functions/costs become closer, reaching R = 0 when all regular agents share identical local optimal value functions/costs (Remark 4).
- The adopted F-local adversary model is more general than the F-total model of [17]: up to F Byzantine nodes are allowed in the neighborhood of every regular node, rather than F in the entire network (Remark 6).

## Limitations & Future Work
- Exact optimality is provably unattainable under adversaries; only approximate (within-R) optimality is guaranteed, and the bound R can be nonzero whenever regular agents' local optimal values/costs differ.
- Assumes a global controller whose actions are visible to all agents (to sidestep the issue of agents applying inputs that are not visible to others); the more general case where agents apply their own inputs that may be invisible to others is left as a noted challenge.
- Requires a time-invariant (2F+1)-robust network and an F-local adversary set.
- No empirical evaluation is provided.
- Future work is not explicitly stated in the text.

## Relevance to Survey
This paper is a core entry in the Byzantine / fault-tolerant line of robust MARL: rather than environment/model uncertainty or state/action perturbations, it targets resilience against arbitrarily-behaving (Byzantine) agents in a decentralized networked-MARL setting. It connects the consensus + innovations distributed RL line ([1]–[4]) with the resilient distributed optimization / consensus literature ([5]–[10]) and Byzantine-robust distributed learning ([11]–[15]), and complements concurrent resilient-MARL works [16] (client-server actor-critic) and [17] (P2P policy evaluation, F-total model). It exemplifies the "topology-based robustness ((2F+1)-robust graphs) + value trimming" methodological sub-line for fault-tolerant cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section I, Introduction — networked/distributed MARL background]_

"In multi-agent reinforcement learning (MARL), multiple agents observe the outcome of interactions with an environment, and use those observations to learn optimal control policies to achieve long-term goals. By working cooperatively, agents are able to optimize a common long-term reward which is an aggregate of all agents' private rewards [1]–[4]. The authors of [1] approach the MARL problem by a distributed Q-learning algorithm, in which each agent maintains a Q-value estimate for every state-action pair. The convergence of the Q-value estimates to the optimal Q values is guaranteed. Subsequently, [2] proposes actor-critic algorithms with convergence guarantees using linear functions to parameterize Q-value estimates. Each agent shares its parameter instead of Q-value estimates to its neighbors. By exploiting the network structure, [3] proposes a scalable actor-critic algorithm where each agent maintains Q-value estimates only for state-action pairs within its multi-hop neighbors. This result has been further extended in [4] to the case of time-varying networks."

> _[Section I, Introduction — resilience and adversarial / Byzantine robustness background]_

"Algorithms for multi-agent systems are typically robust against benign failures of individual agents as long as the underlying network is connected. However, the dependence of these algorithms on local coordination among neighbors also raises a major security concern that the presence of one or more malicious agents under cyberattacks could compromise the entire algorithm [5]. It is thus imperative to develop algorithms that are resilient, which refers to algorithms' ability to withstand the compromise of a subset of the agents and still ensure some notion of correctness [6]. Resilient algorithms against various types of attackers for networked systems have been proposed for different problems such as consensus [6]–[8], distributed optimization [5], [9], [10] and distributed learning [11]–[15]. Within the class of resilient distributed learning algorithms, some papers assume a client-server architecture where a central agent collects information from all other agents and broadcasts new information back to other agents [11]–[13]. Other algorithms such as ByRDiE in [14] and BRIDGE in [15] are designed based on the peer-to-peer (P2P) architecture, where there is no central agent to coordinate all other agents, and all agents exchange information with neighbors. Very recently, resilient algorithms for MARL in the presence of Byzantine agents are proposed in [16] and [17]. Specifically, [16] considers the fully cooperative MARL problem for a networked system in the client-server architecture with a reliable central agent. The paper [17] considers the policy evaluation problem in the P2P architecture. By assuming a bounded reward variation between the local reward of each agent and the global averaged reward of all agents, they obtain a learning error, which is related to the bound of the reward variation, network structure and discounting factor."

> _[Section I, Introduction — positioning of this work]_

"In this paper, we propose a resilient QD-learning algorithm for a networked system in the presence of Byzantine agents. The main motivation is that the QD-learning algorithm generally fails even in the presence of a single adversarial agent. We first extend the distributed Q-learning algorithm for undirected networks [1] to time-varying directed networks. We then build on that to create a resilient QD-learning that is capable of tolerating Byzantine attacks. For each regular agent, we establish the almost sure convergence of the value function to the neighborhood of the optimal value function of all regular agents under certain conditions on the graph topology. For each state, we show that if the optimal Q-values corresponding to different actions are sufficiently separated, each regular agent can learn the optimal policy for all regular agents."

> _[Section IV, Resilient QD-Learning — Remark 6, F-local vs F-total adversary model]_

"The adversary model we consider is the F-local model, which is more general than the F-total model considered in [17]. In particular, the F-total model indicates that there are no more than F Byzantine nodes in the entire network, whereas we allow up to F Byzantine nodes in the neighborhood of every regular node."

### Cited references (resolved from the paper's bibliography)
- **[1]** S. Kar, J. M. Moura, H. V. Poor. *QD-learning: A collaborative distributed strategy for multi-agent reinforcement learning through consensus + innovations.* IEEE Transactions on Signal Processing, 2013.
- **[2]** K. Zhang, Z. Yang, H. Liu, T. Zhang, T. Basar. *Fully decentralized multi-agent reinforcement learning with networked agents.* ICML (PMLR) 2018.
- **[3]** G. Qu, A. Wierman, N. Li. *Scalable reinforcement learning of localized policies for multi-agent networked systems.* Learning for Dynamics and Control (PMLR) 2020.
- **[4]** Y. Lin, G. Qu, L. Huang, A. Wierman. *Distributed reinforcement learning in multi-agent networked systems.* arXiv:2006.06555, 2020.
- **[5]** S. Sundaram, B. Gharesifard. *Distributed optimization under adversarial nodes.* IEEE Transactions on Automatic Control, 2018.
- **[6]** H. J. LeBlanc, H. Zhang, X. Koutsoukos, S. Sundaram. *Resilient asymptotic consensus in robust networks.* IEEE Journal on Selected Areas in Communications, 2013.
- **[7]** F. Pasqualetti, A. Bicchi, F. Bullo. *Consensus computation in unreliable networks: A system theoretic approach.* IEEE Transactions on Automatic Control, 2012.
- **[8]** X. Wang, S. Mou, S. Sundaram. *A resilient convex combination for consensus-based distributed algorithms.* Numerical Algebra, Control & Optimization, 2019.
- **[9]** C. Zhao, J. He, Q.-G. Wang. *Resilient distributed optimization algorithm against adversarial attacks.* IEEE Transactions on Automatic Control, 2019.
- **[10]** K. Kuwaranancharoen, L. Xin, S. Sundaram. *Byzantine-resilient distributed optimization of multi-dimensional functions.* American Control Conference (ACC) 2020.
- **[11]** Y. Chen, L. Su, J. Xu. *Distributed statistical machine learning in adversarial settings: Byzantine gradient descent.* Proceedings of the ACM on Measurement and Analysis of Computing Systems, 2017.
- **[12]** P. Blanchard, E. M. E. Mhamdi, R. Guerraoui, J. Stainer. *Byzantine-tolerant machine learning.* arXiv:1703.02757, 2017.
- **[13]** D. Yin, Y. Chen, R. Kannan, P. Bartlett. *Byzantine-robust distributed learning: Towards optimal statistical rates.* ICML (PMLR) 2018.
- **[14]** Z. Yang, W. U. Bajwa. *ByRDiE: Byzantine-resilient distributed coordinate descent for decentralized learning.* IEEE Transactions on Signal and Information Processing over Networks, 2019.
- **[15]** Z. Yang, W. U. Bajwa. *BRIDGE: Byzantine-resilient decentralized gradient descent.* arXiv:1908.08098, 2019.
- **[16]** Y. Lin, S. Gade, R. Sandhu, J. Liu. *Toward resilient multi-agent actor-critic algorithms for distributed reinforcement learning.* American Control Conference (ACC) 2020.
- **[17]** Z. Wu, H. Shen, T. Chen, Q. Ling. *Byzantine-resilient decentralized TD learning with linear function approximation.* arXiv:2009.11146, 2020.
