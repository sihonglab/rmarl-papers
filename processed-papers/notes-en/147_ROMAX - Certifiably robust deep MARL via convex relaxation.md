# 147. ROMAX: Certifiably Robust Deep Multiagent Reinforcement Learning via Convex Relaxation

## Metadata
- **Title**: ROMAX: Certifiably Robust Deep Multiagent Reinforcement Learning via Convex Relaxation
- **Authors**: Chuangchuang Sun, Dong-Ki Kim, Jonathan P. How
- **Affiliation**: Laboratory for Information & Decision Systems (LIDS), Massachusetts Institute of Technology
- **Venue**: Not specified (arXiv:2109.06795v1, 14 Sep 2021)
- **Link/arXiv**: arXiv:2109.06795v1 [cs.LG]

## Taxonomy
- **Robustness / perturbation type targeted**: Worst-case policy changes of other (peer/opponent) agents under cyber-physical attacks (communication hijack, observation perturbations); non-stationarity caused by concurrently learning agents; action perturbations of other agents within an l_p ball
- **Method paradigm**: Minimax MARL, adversarial training, convex relaxation of neural networks (certified robustness), centralized training with decentralized execution (MADDPG-based)
- **Keywords**: certified robustness, convex relaxation, minimax optimization, robust MARL, MADDPG, worst-case opponents

## TL;DR
The paper proposes ROMAX, a minimax MARL approach that infers the worst-case policy update of other agents and approximately solves the (intractable) inner minimization via convex relaxation of neural networks, yielding a certified lower bound on the centralized Q-function and more robust policies that outperform prior robust MARL baselines on mixed cooperative-competitive tasks.

## Problem & Motivation
In multirobot systems, cyber-physical attacks (e.g., communication hijack, observation perturbations) challenge agent robustness, and this is worsened in MARL by non-stationarity from simultaneously learning agents whose changing policies alter transition and reward functions. CTDE methods partially alleviate non-stationarity but overfit other agents' current behaviors and fail against new/unseen strategies; this is especially severe in competitive settings where an opponent can exploit a brittle policy. The prior robust MARL method M3DDPG uses a single-step gradient descent to approximate the inner minimization, which can only explore the locally worst situation, is highly sensitive to a hard-to-tune step size, and only computes an upper bound of the inner problem (so maximizing it cannot guarantee maximizing the original minimax objective).

## Robustness Setting
- **Threat model / uncertainty set**: Other agents' actions a_{-i} are treated as adversarial and constrained to a compact set B_{-i} (an l_p norm ball of radius epsilon centered at the other agents' nominal actions). The worst-case (globally approximate) action of other agents is computed by minimizing the centralized Q-function over this ball; robustness is certified via a guaranteed bound from the convex relaxation.
- **Setting**: Mixed cooperative-competitive; CTDE (centralized critic, decentralized actor); online, model-free (deterministic policy gradient / MADDPG-based).

## Method
- Formulate robust learning as a minimax problem: each agent maximizes its centralized Q-value over its own policy while minimizing over the adversarial actions a_{-i} of other agents within the l_p ball B_{-i} (Equation 3).
- Since the nonconvex-nonconcave minimax is intractable and M3DDPG's one-step gradient only gives a local/upper-bound solution, convexify the centralized action-value function (assume fully connected ReLU networks) using a linear convex relaxation (Equation 6), so the inner minimization becomes a linear program solvable efficiently and yields a certified lower bound of Q (Equation 7).
- Reformulate the outer maximization as a convex combination, weighted by kappa_i in [0,1], of the original Q and the relaxed worst-case Q-bar (Equation 8), trading off training stability against the (possibly large, early-training) relaxation gap; maximizing the lower bound guarantees the original inner objective is maximized, providing robustness certificates.
- Integrate into MADDPG: actor updated by the policy gradient with the worst-case a*_{-i} from the relaxed inner minimization, critic updated with a relaxed target (Equations 9-10); the relaxation is solved automatically using the auto_LiRPA framework, optionally combining IBP and CROWN-IBP bounds via a tunable parameter beta (Equation 11). Summarized as Algorithm 1.

## Theoretical Contributions
- Provides a certified bound: the convex relaxation gives a guaranteed lower bound Q-bar of the true centralized Q, so maximizing this lower bound guarantees the original inner minimax objective is maximized, yielding robustness certificates against worst-case behavior of other learning agents. Otherwise mostly empirical (no convergence/sample-complexity analysis; the paper lists convergence analysis as future work).

## Experiments
- **Environment/Benchmark**: Mixed cooperative-competitive tasks from the multiagent particle benchmark: Predator-prey (n_a=3 predators/adversaries chasing n_c=1 prey/agent, n_L=2 landmarks) and Physical deception (n_a=1 adversary, n_c=2 agents, n_L=2 landmarks).
- **Baselines**: M3DDPG (robust MARL with one-step gradient minimax) and MADDPG (centralized critic, no minimax).
- **Evaluation metrics**: Reward per step (mean/standard error) for adversaries and agents; cross-play robustness via R_Adv (column) and R_Agent (row) where each team's policy is evaluated against a diverse set of the other team's policies (250 episodes per pair, 5x5 random-seed pairs); overall robustness R_overall = R_Adv + R_Agent; performance of a fixed robust policy against newly trained disruptive adversaries; wall-clock time per iteration relative to MADDPG.

## Key Results
- In both tasks, ROMAX trains more robust policies for both teams: its adversary achieves the highest R_Adv and its agent the highest R_Agent against diverse opponents; ROMAX attains the best overall robustness (R_overall = -0.053 vs -1.533 for M3DDPG and -2.187 for MADDPG in predator-prey; -0.805 vs -1.552 and -1.463 in physical deception).
- M3DDPG is outperformed by MADDPG in the physical deception overall results, attributed to M3DDPG's sensitive, hard-to-generalize step-size parameter; ROMAX avoids this by not needing a step size.
- The certification module is computationally efficient: the ratio of ROMAX's wall-clock time per iteration (with certification) to MADDPG's (without) is close to 1 (about 1.08 averaged over seeds).
- When disruptive adversaries are trained to exploit a fixed prey policy, the prey trained by ROMAX retains the highest return, validating its robustness advantage; M3DDPG and MADDPG perform similarly here.

## Limitations & Future Work
- The relaxation gap can be large, especially early in training, requiring the kappa_i mixing weight (and a trade-off among relaxation methods) rather than purely using the relaxed objective.
- No theoretical convergence/sample-complexity guarantees are provided.
- Future work: develop tighter but efficient convex relaxation-based neural-network robustness verification; test on more real-world robustness applications (observation perturbation, actuation fault, malicious/stealthy attack, communication delay); develop principled, general learning methods with theoretical guarantees (e.g., convergence analysis).

## Relevance to Survey
ROMAX sits on the adversarial/minimax robust MARL line, extending the M3DDPG worst-case-opponent formulation, and is notably the (claimed) first work to integrate neural-network robustness verification (certified robustness via convex relaxation) into MARL. It connects the certified-robustness / robustness-verification literature (FastLin, CROWN, IBP, CROWN-IBP, auto_LiRPA, single-agent certified RL) with cooperative-competitive CTDE MARL, bridging robust RL/robust MDP certification and robustness to other agents' policy changes.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Works — "Centralized training with decentralized execution."]_

"The standard approach for addressing non-stationarity in MARL is to consider information about other agents and reason about the effects of joint actions [12]. The recent studies regarding the centralized training with decentralized execution framework, for instance, account for the behaviors of others through a centralized critic [7, 8, 13–15]. While this body of work partially alleviates non-stationarity, converged policies generally overﬁt the current behaviors of other agents and thus show poor performance when interacting with agents with new behaviors. In contrast, our agents learn robust policies based on minimax optimization by applying convex relaxation."

> _[Section II, Related Works — "Robust MARL."]_

"Our framework is closely related to prior works that apply minimax optimization in multiagent learning settings [16, 17]. Minimax provides a game-theoretical concept that encourages an agent to learn a robust policy by maximizing its performance in a worst-case scenario [10, 18]. One of the noticeable studies in this category is [19], which computes the worst-case perturbation by taking a single gradient descent step assuming that other agents act adversarial. However, the single-step gradient approximation can only explore the locally worst situation and thus can still result in unstable learning. Our approach aims to address this drawback by computing the approximate globally worst situation based on convex relaxation. The work by [20] applies the similar linear relaxation technique in a single-agent robust RL problem to certify the robustness under uncertainties from the environments. However, in our multiagent settings, the robustness is more challenging to certify due to the concurrent policy learning amongst multiple agents."

> _[Section II, Related Works — "Ensemble training in MARL."]_

"Another relevant approach to learning a robust policy is ensemble training, where each agent interacts with a group of agents instead of a particular agent only [7, 21, 22]. For example, the population-based training technique, which was originally proposed to ﬁnd a set of hyperparameters for optimizing a neural network [23], was applied in MARL by evolving a population of agents [24]. This approach showed robust and superhuman level performance in a competitive game. The literature on self-play, which plays against random old versions of itself to improve training stability and robustness, can also be classiﬁed into this category [25]. However, maintaining and/or evolving a population is often computationally heavy. Additionally, these methods do not employ minimax optimization, so agents may not be able to cope well with the worst scenario."

> _[Section II, Related Works — "Learning aware MARL."]_

"Our framework is also related to prior works that consider the learning of other agents in the environment to address non-stationarity. These works include [26] which attempted to discover the best response adaptation to the anticipated future policy of other agents. Our work is also related to [27, 28] that shape the learning process of others. Another relevant idea explored by [29] is to interpolate between the frameworks of [26] and [27] in a way that guarantees convergence while inﬂuencing the opponent's future policy. Recently, [6] addresses non-stationarity by considering both an agent's own non-stationary policy dynamics and the non-stationary policy dynamics of other agents within a meta-learning objective. While these approaches alleviate non-stationarity by considering the others' learning, they do not solve the minimax objective and cannot guarantee robustness when playing against a new opponent. This weakness can be exploited by a carefully trained adversary agent [9]."

> _[Section II, Related Works — "Robustness veriﬁcation and neural network relaxation."]_

"To verify the robustness of neural networks, it is important to compute the lower and upper bound of the output neurons under input perturbations. In supervised learning settings, for example, the margin between predicting the ground-truth class and other classes indicates the robustness of neural networks (i.e., measuring the chance of misclassiﬁcation). However, due to the nonconvexity in neural networks, the work by [30] proved that ﬁnding the true range of neural network's output is nonconvex and NP-complete. To address this issue, convex relaxation methods are proposed to efﬁciently compute the outer approximation (a more conservative estimate) of neural network's output range. Many prior works are based on the linear relaxation of the nonlinear units in neural networks: FastLin [31], DeepZ [32], Neurify [33], DeepPoly [34], and CROWN [35]. There are also other approaches based on semideﬁnite relaxation [36, 37], which admit tighter bounds but are more computationally expensive. See [38] for in-depth surveys on this topic."

### Cited references (resolved from the paper's bibliography)
- **[6]** D.-K. Kim, M. Liu, M. Riemer, C. Sun, M. Abdulhai, G. Habibi, S. Lopez-Cot, G. Tesauro, J. How. *A policy gradient algorithm for learning to learn in multiagent reinforcement learning.* ICML 2021.
- **[7]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* arXiv:1706.02275, 2017.
- **[8]** J. Foerster, G. Farquhar, T. Afouras, N. Nardelli, S. Whiteson. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[9]** A. Gleave, M. Dennis, C. Wild, N. Kant, S. Levine, S. Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[10]** M. L. Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994.
- **[12]** P. Hernandez-Leal, M. Kaisers, T. Baarslag, E. M. de Cote. *A survey of learning in multiagent environments: Dealing with non-stationarity.* CoRR abs/1707.09183, 2017.
- **[13]** Y. Yang, R. Luo, M. Li, M. Zhou, W. Zhang, J. Wang. *Mean field multi-agent reinforcement learning.* ICML 2018.
- **[14]** Y. Wen, Y. Yang, R. Luo, J. Wang, W. Pan. *Probabilistic recursive reasoning for multi-agent reinforcement learning.* ICLR 2019.
- **[15]** D.-K. Kim, M. Liu, S. Omidshafiei, S. Lopez-Cot, M. Riemer, G. Habibi, G. Tesauro, S. Mourad, M. Campbell, J. P. How. *Learning hierarchical teaching policies for cooperative agents.* AAMAS 2020.
- **[16]** J. Perolat, F. Strub, B. Piot, O. Pietquin. *Learning Nash Equilibrium for General-Sum Markov Games from Batch Data.* AISTATS 2017.
- **[17]** J. Grau-Moya, F. Leibfried, H. Bou-Ammar. *Balancing two-player stochastic games with soft Q-learning.* IJCAI 2018.
- **[18]** M. Osborne. *An introduction to game theory.* Oxford Univ. Press, 2004.
- **[19]** S. Li, Y. Wu, X. Cui, H. Dong, F. Fang, S. Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[20]** B. Lütjens, M. Everett, J. P. How. *Certified adversarial robustness for deep reinforcement learning.* Conference on Robot Learning (CoRL), PMLR 2020.
- **[21]** M. Shen, J. P. How. *Robust opponent modeling via adversarial ensemble reinforcement learning.* ICAPS 2021.
- **[22]** J. Schrittwieser, I. Antonoglou, T. Hubert, K. Simonyan, L. Sifre, S. Schmitt, A. Guez, E. Lockhart, D. Hassabis, T. Graepel, T. Lillicrap, D. Silver. *Mastering Atari, Go, chess and shogi by planning with a learned model.* Nature 2020.
- **[23]** M. Jaderberg, V. Dalibard, S. Osindero, W. M. Czarnecki, J. Donahue, A. Razavi, O. Vinyals, T. Green, I. Dunning, K. Simonyan, C. Fernando, K. Kavukcuoglu. *Population based training of neural networks.* CoRR abs/1711.09846, 2017.
- **[24]** M. Jaderberg, W. M. Czarnecki, I. Dunning, L. Marris, G. Lever, A. G. Castañeda, C. Beattie, N. C. Rabinowitz, A. S. Morcos, A. Ruderman, et al. *Human-level performance in 3D multiplayer games with population-based reinforcement learning.* Science 2019.
- **[25]** T. Bansal, J. Pachocki, S. Sidor, I. Sutskever, I. Mordatch. *Emergent complexity via multi-agent competition.* ICLR 2018.
- **[26]** C. Zhang, V. R. Lesser. *Multi-agent learning with policy prediction.* AAAI 2010.
- **[27]** J. Foerster, R. Y. Chen, M. Al-Shedivat, S. Whiteson, P. Abbeel, I. Mordatch. *Learning with opponent-learning awareness.* AAMAS 2018.
- **[28]** J. Foerster, G. Farquhar, M. Al-Shedivat, T. Rocktäschel, E. Xing, S. Whiteson. *DiCE: The infinitely differentiable Monte Carlo estimator.* ICML 2018.
- **[29]** A. Letcher, J. Foerster, D. Balduzzi, T. Rocktäschel, S. Whiteson. *Stable opponent shaping in differentiable games.* ICLR 2019.
- **[30]** G. Katz, C. Barrett, D. L. Dill, K. Julian, M. J. Kochenderfer. *Reluplex: An efficient SMT solver for verifying deep neural networks.* CAV 2017.
- **[31]** L. Weng, H. Zhang, H. Chen, Z. Song, C.-J. Hsieh, L. Daniel, D. Boning, I. Dhillon. *Towards fast computation of certified robustness for ReLU networks.* ICML 2018.
- **[32]** G. Singh, T. Gehr, M. Mirman, M. Püschel, M. T. Vechev. *Fast and effective robustness certification.* NeurIPS 2018.
- **[33]** S. Wang, K. Pei, J. Whitehouse, J. Yang, S. Jana. *Efficient formal safety analysis of neural networks.* arXiv:1809.08098, 2018.
- **[34]** G. Singh, T. Gehr, M. Püschel, M. T. Vechev. *Boosting robustness certification of neural networks.* ICLR (Poster) 2019.
- **[35]** H. Zhang, T.-W. Weng, P.-Y. Chen, C.-J. Hsieh, L. Daniel. *Efficient neural network robustness certification with general activation functions.* arXiv:1811.00866, 2018.
- **[36]** A. Raghunathan, J. Steinhardt, P. Liang. *Semidefinite relaxations for certifying robustness to adversarial examples.* arXiv:1811.01057, 2018.
- **[37]** K. D. Dvijotham, R. Stanforth, S. Gowal, C. Qin, S. De, P. Kohli. *Efficient neural network verification with exactness characterization.* UAI 2020.
- **[38]** H. Salman, G. Yang, H. Zhang, C.-J. Hsieh, P. Zhang. *A convex relaxation barrier to tight robust verification of neural networks.* arXiv:1902.08722, 2019.
