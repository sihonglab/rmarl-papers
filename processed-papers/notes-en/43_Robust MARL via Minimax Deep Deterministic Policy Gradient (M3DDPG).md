# 43. Robust Multi-Agent Reinforcement Learning via Minimax Deep Deterministic Policy Gradient

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning via Minimax Deep Deterministic Policy Gradient
- **Authors**: Shihui Li, Yi Wu, Xinyue Cui, Honghua Dong, Fei Fang, Stuart Russell
- **Affiliation**: Carnegie Mellon University; University of California, Berkeley; Tsinghua University
- **Venue**: AAAI 2019 (The Thirty-Third AAAI Conference on Artificial Intelligence, AAAI-19)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to changes in opponents' (other agents') policies between training and testing; adversarial worst-case perturbation of other agents' actions (interpreted as adversarial noise on the dynamics).
- **Method paradigm**: Minimax / worst-case (maximin), adversarial training, deterministic policy gradient (MADDPG extension), centralized critic with decentralized actors, game-theoretic minimax.
- **Keywords**: M3DDPG, MADDPG, minimax, robust policy learning, multi-agent adversarial learning (MAAL), continuous action spaces.

## TL;DR
The paper proposes M3DDPG, a minimax (maximin) extension of MADDPG that trains each agent to perform well when all other agents act adversarially, and introduces Multi-Agent Adversarial Learning (MAAL) — a single-gradient-step linearization to make the otherwise intractable continuous-action minimax objective efficient.

## Problem & Motivation
DRL agents are brittle and sensitive to their training environment, and in multi-agent settings a learned policy can get stuck in a poor local optimum that is only locally optimal w.r.t. its training partners' current policies. This is especially severe in competitive environments: when opponents alter their policies at test time, performance can degrade drastically. Although a centralized critic (as in MADDPG) stabilizes training and mitigates non-stationarity, it does not make policies robust to opponents using strategies different from those seen during training. The paper aims to learn robust multi-agent policies with continuous action spaces that generalize when opponents' policies change.

## Robustness Setting
- **Threat model / uncertainty set**: During training, each agent optimizes its accumulative reward under the assumption that all other agents act adversarially (worst case). The minimax objective places a minimization over the other agents' actions inside the centralized Q function. From a single agent's perspective, perturbations on opponents' actions can be viewed as a special adversarial noise on the dynamics. The worst-case perturbation magnitude is controlled by a tunable perturbation rate α.
- **Setting**: Mixed cooperative and competitive Markov games; centralized critic with decentralized execution (CTDE, built on MADDPG); model-free / online; continuous action spaces.

## Method
- **Minimax objective**: Extend MADDPG by defining each agent's objective as a maximin — maximize agent i's return assuming all other agents take the worst-case (reward-minimizing) actions, yielding a modified centralized Q function Q^μ_{M,i} with an embedded minimization over other agents' actions (Eqs. 6–8). This Q function admits a recursive Bellman form and supports off-policy temporal-difference learning.
- **Gradients and updates**: Because the adversarial actions do not depend on agent i's own parameters θ_i, the deterministic policy gradient theorem applies directly; the resulting actor gradient (Eq. 9) and critic loss/target (Eq. 10) simply inject a minimization over other agents' actions into the standard MADDPG updates.
- **Multi-Agent Adversarial Learning (MAAL)**: Solving the inner minimization exactly is intractable for continuous, non-linear Q functions. MAAL (1) locally linearizes the Q function and (2) replaces the inner-loop minimization with a single gradient-descent step, approximating each worst-case perturbation ε̂_j by a scaled negative gradient of Q w.r.t. action a_j (Eqs. 11–14). This requires only one extra gradient computation and is fully end-to-end.
- **Perturbation scaling**: To stabilize learning given changing gradient/action norms, the perturbation is computed with normalized forms ε̂_j = -α_j g/||g|| or ε̂_j = -α_j ||a_j|| g/||g|| (Eqs. 16–17). With α = 0, M3DDPG degenerates to MADDPG; larger α increases robustness but makes optimization harder. In mixed environments, adding (smaller) perturbations to collaborators in addition to competitors empirically improves learned policies.

## Theoretical Contributions
None / mostly empirical. The paper provides derivations of the minimax Q-function recursion and the corresponding gradient/critic updates, and draws formal connections to adversarial training and to single-agent robust RL, but offers no convergence, equilibrium-existence, or sample-complexity guarantees.

## Experiments
- **Environment/Benchmark**: The same particle-world environments and training configurations as the MADDPG paper; four mixed cooperative and competitive scenarios — Covert communication, Keep-away, Physical deception, and Predator-prey. A fixed set of 2500 environment configurations is used for testing. α selected via grid search over 0.1, 0.01, 0.001.
- **Baselines**: MADDPG (classical, "MA"); also DDPG used to train "disruptive adversaries" from scratch under a zero-sum reward for the worst-case evaluation.
- **Evaluation metrics**: Normalized (0–1) agent score / reward of the normal agents across role cross-combinations (e.g., MA vs MA, MA vs Minimax, Minimax vs MA, Minimax vs Minimax); reward of the fixed normal agents as disruptive adversaries are trained to convergence.

## Key Results
- In direct competition across all four environments, the highest normal-agent score occurs when M3DDPG agents play as the normal agents against a MADDPG adversary, and the lowest when MADDPG agents play against an M3DDPG adversary — indicating M3DDPG policies are of higher quality than MADDPG.
- Under the worst-case evaluation against disruptive (zero-sum, trained-from-scratch) adversaries, M3DDPG (Minimax) agents achieve higher reward than MADDPG agents in all scenarios, implying better robustness even in the worst situation.

## Limitations & Future Work
- Because MAAL uses a single-step gradient approximation, an M3DDPG agent only explores the locally worst situation during training, which can still yield unsatisfying behavior when test opponents adopt drastically different strategies.
- Using a fixed α throughout training can cause unstable learning due to changing gradient/action scales (motivating the normalized-perturbation variants).
- Future work: re-examine the robustness–efficiency trade-off in MAAL and improve policy learning by placing more computation on the minimax optimization.

## Relevance to Survey
A foundational adversarial-training line of robust MARL: M3DDPG introduces the minimax/maximin worst-case objective into continuous-action multi-agent deep RL and connects multi-agent robustness to single-agent robust/adversarial RL by treating opponents' worst-case action perturbations as adversarial noise on the dynamics. It is frequently cited as a baseline and reference point for later robust MARL work (e.g., the robust Markov game / model-uncertainty line), and sits on the "robustness to opponent/agent policy changes" theme combined with the "minimax + adversarial training" method line.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — MARL / DRL multi-agent learning]_

"Multi-agent reinforcement learning (Littman 1994) has been a long-standing ﬁeld in AI (Hu, Wellman, and others 1998; Busoniu, Babuska, and De Schutter 2008). Recent works in DRL use deep neural networks to approximately represent policy and value functions. Inspired by the success of DRL in single-agent settings, many DRL-based multi-agent learning algorithms have been proposed. Forester et al. (2016b) and He et al. (2016) extended the deep Q-learning to multi-agent setting; Peng et al. (2017a) proposed a centralized policy learning algorithm based on actor-critic policy gradient; Forester et al. (2016a) developed a decentralized multi-agent policy gradient algorithm with centralized baseline; Lowe et al. (2017) extended DDPG to multi-agent setting with a centralized Q function; Wei et al. (2018) and Grau-Moya (2018) proposed multi-agent variants of the soft-Q-learning algorithm (Haarnoja et al. 2017); Yang et al. (2018) focused on multi-agent reinforcement learning on a very large population of agents. Our M3DDPG algorithm is built on top of MADDPG and inherits the decentralized policy and centralized critic framework."

> _[Section 2, Related Work — Minimax in MARL]_

"Minimax is a fundamental concept in game theory and can be applied to general decision-making under uncertainty, prescribing a strategy that minimizes the possible loss for a worst case scenario (Osborne and others 2004). Minimax was ﬁrstly introduced to multi-agent reinforcement learning as minimax Q-learning by Littman (1994). More recently, some works combine the minimax framework and the DRL techniques to ﬁnd Nash equilibrium in two player zero-sum games (Foerster et al. 2018; P´erolat et al. 2016; Grau-Moya, Leibfried, and Bou-Ammar 2018). In our work, we utilize the minimax idea for the purpose of robust policy learning."

> _[Section 2, Related Work — Robust / adversarial RL]_

"Robust reinforcement learning was originally introduced by Morimoto et al. (2005) considering the generalization ability of the learned policy in the single-agent setting. This problem is also studied recently with deep neural networks, such as adding random noise to input (Tobin et al. 2017) or dynamics (Peng et al. 2017b) during training. Besides adding random noise, some other works implicitly adopt the minimax idea by utilizing the “worst noise” (Pinto et al. 2017; Mandlekar et al. 2017). These works force the learned policy to work well even under the worst case perturbations and are typically under the name of “adversarial reinforcement learning”, despite the fact that the original adversarial reinforcement learning problem was introduced in the setting of multi-agent learning (Uther and Veloso 1997). In our M3DDPG algorithm, we focus on the problem of learning polices that is robust to opponents with different strategies."

> _[Section 2, Related Work — finding the worst case scenario]_

"Within the minimax framework, ﬁnding the worst case scenario is a critical component. Lanctot et al. (2017) proposed an iterative approach that alternatively computes the best response policy while ﬁxes the other. Gao et al. (Gao, Mueller, and Hayward 2018) replace “mean” in the temporal difference learning rule with “minimum”. In our work, we proposed MAAL, which is a general, efﬁcient and fully end-to-end learning approach. MAAL is motivated by adversarial training (Goodfellow, Shlens, and Szegedy 2014) and suitable for arbitrary number of agents. The core idea of MAAL is approximating the minimization in our minmax objective by a single gradient descent step. The idea of one-step-gradient approximation was also explored in meta-learning (Finn, Abbeel, and Levine 2017)."

### Cited references (resolved from the paper's bibliography)
- **Littman 1994** Littman. *Markov games as a framework for multi-agent reinforcement learning.* ICML 1994.
- **Hu, Wellman, and others 1998** Hu, Wellman, et al. *Multiagent reinforcement learning: theoretical framework and an algorithm.* ICML 1998.
- **Busoniu, Babuska, and De Schutter 2008** Busoniu, Babuska, De Schutter. *A comprehensive survey of multiagent reinforcement learning.* IEEE Transactions on Systems, Man, and Cybernetics, Part C, 2008.
- **Forester et al. (2016b)** Foerster, Assael, de Freitas, Whiteson. *Learning to Communicate to Solve Riddles with Deep Distributed Recurrent Q-Networks.* 2016.
- **He et al. (2016)** He, Boyd-Graber, Kwok, Daumé III. *Opponent modeling in deep reinforcement learning.* ICML 2016.
- **Peng et al. (2017a)** Peng, Yuan, Wen, Yang, Tang, Long, Wang. *Multiagent bidirectionally-coordinated nets for learning to play StarCraft combat games.* CoRR abs/1703.10069, 2017.
- **Forester et al. (2016a)** Foerster, Assael, de Freitas, Whiteson. *Learning to communicate with deep multi-agent reinforcement learning.* CoRR abs/1605.06676, 2016.
- **Lowe et al. (2017)** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **Wei et al. (2018)** Wei, Wicke, Freelan, Luke. *Multiagent soft Q-learning.* arXiv:1804.09817, 2018.
- **Grau-Moya (2018) / Grau-Moya, Leibfried, and Bou-Ammar 2018** Grau-Moya, Leibfried, Bou-Ammar. *Balancing two-player stochastic games with soft Q-learning.* arXiv:1802.03216, 2018.
- **Haarnoja et al. 2017** Haarnoja, Tang, Abbeel, Levine. *Reinforcement learning with deep energy-based policies.* arXiv:1702.08165, 2017.
- **Yang et al. (2018)** Yang, Luo, Li, Zhou, Zhang, Wang. *Mean field multi-agent reinforcement learning.* arXiv:1802.05438, 2018.
- **Osborne and others 2004** Osborne, et al. *An introduction to game theory.* Oxford University Press, 2004.
- **Foerster et al. 2018** Foerster, Chen, Al-Shedivat, Whiteson, Abbeel, Mordatch. *Learning with opponent-learning awareness.* AAMAS 2018.
- **Pérolat et al. 2016** Pérolat, Strub, Piot, Pietquin. *Learning Nash equilibrium for general-sum Markov games from batch data.* arXiv:1606.08718, 2016.
- **Morimoto et al. (2005) / Morimoto and Doya 2005** Morimoto, Doya. *Robust reinforcement learning.* Neural Computation 17(2):335–359, 2005.
- **Tobin et al. 2017** Tobin, Fong, Ray, Schneider, Zaremba, Abbeel. *Domain randomization for transferring deep neural networks from simulation to the real world.* IROS 2017.
- **Peng et al. 2017b** Peng, Andrychowicz, Zaremba, Abbeel. *Sim-to-real transfer of robotic control with dynamics randomization.* arXiv:1710.06537, 2017.
- **Pinto et al. 2017** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* arXiv:1703.02702, 2017.
- **Mandlekar et al. 2017** Mandlekar, Zhu, Garg, Fei-Fei, Savarese. *Adversarially robust policy learning: Active construction of physically-plausible perturbations.* IROS 2017.
- **Uther and Veloso 1997** Uther, Veloso. *Generalizing adversarial reinforcement learning.* AAAI Fall Symposium on Model Directed Autonomous Systems, 1997.
- **Lanctot et al. (2017)** Lanctot, Zambaldi, Gruslys, Lazaridou, Perolat, Silver, Graepel, et al. *A unified game-theoretic approach to multiagent reinforcement learning.* NeurIPS 2017.
- **Gao, Mueller, and Hayward 2018** Gao, Mueller, Hayward. *Adversarial policy gradient for alternating Markov games.* 2018.
- **Goodfellow, Shlens, and Szegedy 2014** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* arXiv:1412.6572, 2014.
- **Finn, Abbeel, and Levine 2017** Finn, Abbeel, Levine. *Model-agnostic meta-learning for fast adaptation of deep networks.* arXiv:1703.03400, 2017.
