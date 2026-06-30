# 50. Finding the Weakest Link: Adversarial Attack against Multi-Agent Communications

## Metadata
- **Title**: Finding the Weakest Link: Adversarial Attack against Multi-Agent Communications
- **Authors**: Maxwell Standen, Junae Kim, Claudia Szabo
- **Affiliation**: The University of Adelaide (Adelaide, Australia); DST Group (Australia)
- **Venue**: Not specified (arXiv preprint, arXiv:2605.13170v1 [cs.LG], 13 May 2026)
- **Link/arXiv**: arXiv:2605.13170v1

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks — single-victim communication perturbation attacks against multi-agent communications (inter-agent message interception and L2-bounded perturbation)
- **Method paradigm**: White-box adversarial machine learning (AML); gradient-based perturbation crafting (FGM/PGD); Jacobian-based saliency (JSMA-inspired) for message/victim/timestep selection; novel adversarial loss functions; attack tempo functions
- **Keywords**: adversarial attack, multi-agent communications, MARL robustness, Jacobian saliency, attack tempo, message selection

## TL;DR
The paper proposes a single-victim communication perturbation attack framework against MARL that uses Jacobian gradient magnitudes to select which messages, which agent, and which timesteps to perturb, plus two new adversarial loss functions (weighted-loss and maximum-loss) that trade attack success for attack impact, demonstrating improved attack effectiveness against observation-sharing and RIAL communication methods.

## Problem & Motivation
Multi-agent systems rely on communication for coordination and information sharing, which exposes a vulnerability to attacks. Learnt communication protocols are increasingly applied to real-world problems, so understanding the risks of such communication is paramount, and effective attacks help expose these risks and motivate mitigations. Existing communication perturbation attacks are inefficient because they do not target vulnerable messages and timesteps: prior attacks arbitrarily select which messages to perturb, or only target systems with so few agents that message selection is moot, and "when to attack" (tempo) has only been explored against single-agent systems. The diversity of valid solutions to RL problems further complicates attacking MARL, since merely changing the action an agent takes may not impact the system if alternative actions lead to similar outcomes. Existing high-impact attacks rely on costly deep RL. The paper addresses which messages to perturb (where-to-attack), which agent to target (who-to-attack), and when to perturb (when-to-attack) without costly techniques.

## Robustness Setting
- **Threat model / uncertainty set**: Strong attacker with full white-box knowledge of the victim system, able to intercept and alter inter-agent messages. Single-victim scenario: the adversary alters only a subset of messages received by a single agent. Attack effectiveness = attack success (changing the victim's action) × attack impact (effect on system performance); detectability is governed by perturbation magnitude (max L2 distance Δ_m), tempo, and number of changed messages k per attacked timestep. Modeled as a Single-Victim Communication Perturbation APOSG (SVCP-APOSG), a 14-tuple variant of the Adversarial Partially Observable Stochastic Game (APOSG) with six adversarial elements {v_m, Θ_m, Δ_m, Σ_a, Σ_m, k}.
- **Setting**: cooperative MARL; agents trained with Q-learning approaches (assumed well-trained, accurately predicting Q-values); evaluation is essentially online attack at execution time; the attacker is external (not a learning agent).

## Method
- Proposes two novel loss functions to combine with gradient-based crafting (FGM/PGD): **maximum loss** (L_m), which encourages the victim to select the action originally considered worst, maximizing impact at the cost of success probability; and **weighted loss** (L_w), a mean Q-difference-weighted cross-entropy across actions that balances impact and success. Both improve over the standard **untargeted loss** (L_u), which only minimizes the probability of the original action and can yield low-impact alternative actions.
- Defines the Jacobian of a chosen loss with respect to the received messages, J(o_i) = ∇L(o_i), and uses the element-wise sum of absolute values of each message's Jacobian as a proxy P(o_i, j) = Σ_k |J_m(o_i, j)_k| for that message's attack effectiveness.
- **Ranked message selection** (where-to-attack, Σ_m): ranks received messages by Jacobian magnitude and selects the top-k. **Victim selection** (who-to-attack, Σ_a): selects the agent with the largest total Jacobian-proxy value over its top-k messages. **Tempo function** (when-to-attack, Θ): attacks timesteps where the total top-k Jacobian magnitude for the selected victim exceeds a threshold φ.
- Perturbations are crafted with PGD (20 iterations, step size 0.1) under L2 magnitude Δ_m = 1, using the respective loss function; the Jacobian-proxy thus measures attack success (untargeted loss) or attack effectiveness (maximum/weighted loss).

## Theoretical Contributions
None / mostly empirical. The paper contributes a formal problem model (the SVCP-APOSG 14-tuple) and defines loss functions and selection criteria, but provides no convergence, sample-complexity, equilibrium, or certified-robustness guarantees.

## Experiments
- **Environment/Benchmark**: Five environments — a simple grid-world navigation game (Nav); two PredatorPrey variants, orthogonal (PP-O) and diagonal (PP-D); and two TrafficJunction variants, small (TJ-S, up to 5 agents) and large (TJ-L, up to 20 agents). Three agents control Nav and PredatorPrey. Two communication methods are attacked: full observation sharing (OBS) and RIAL (vocabulary size 4, message length 2).
- **Baselines**: Tempo/victim-selection methods used with random message selection and PGD + untargeted loss — CBTS, MMR, ML, NS, VL, and ST. Ablation compares maximum / weighted / untargeted loss with random vs. ranked message selection (Rand-M/W/U, Rank-M/W/U). The paper's attacks are denoted J-W and J-M (Jacobian tempo/victim/message selection with weighted or maximum loss respectively).
- **Evaluation metrics**: Total episode reward; a task metric (proportion of agents reaching the goal for Nav; proportion of caught prey for PredatorPrey; number of collisions for TrafficJunction); and attack success rate Δ_a (proportion of attacked steps where the victim's action changed). Tukey's honest significance test (α = 0.05) is used; attack frequency is controlled via a binning method (bins 0.25, 0.5, 0.75, width 0.125).

## Key Results
- Ranked message selection achieves a similar or greater impact than random message selection in 29 of the 30 tested scenarios.
- The J-M and J-W attacks are most effective in the orthogonal PredatorPrey environment across all attack rates (against OBS), and J-W is most effective in diagonal PredatorPrey (significant improvement at high attack rates); against TrafficJunction (OBS), J-W and J-M are most effective except at high attack rates against the large environment, where ST dominates.
- RIAL is markedly more robust than observation sharing: attack success rates are low across environments, impacts on PredatorPrey/TrafficJunction are much smaller, and no attack significantly affects the task metric of PredatorPrey and small TrafficJunction.
- Local optima can cause adversarially induced actions to improve system performance, observed in OBS navigation and all RIAL systems, undermining the assumption that the system is well trained.

## Limitations & Future Work
- A key assumption is that the system is well trained and accurately approximates the Q-function, but this is not well supported since some attacks improve system performance (local optima phenomenon).
- Conclusions are constrained by the two communication methods and the environments used; aspects such as network topology, delayed messages, and noisy channels were not considered, and the environments have relatively small observation spaces (larger observations may reduce attack effectiveness).
- Threshold-based attack-rate control derived from clean episodes is less effective than expected because attacks change the system dynamics and thus the distribution used by tempo functions, introducing a feedback loop; the binning method mitigates this efficiently but a more expensive approach running the attacks could find better thresholds.
- The study focuses on undefended agents. Future work could evaluate defences (e.g., input-correction snapping messages to the nearest valid message for discrete message sets, and adversarial training) and additional communication algorithms and environments.

## Relevance to Survey
This paper sits on the "communication robustness / adversarial attacks against MARL" line of the robust MARL landscape, complementing certified-defence and robust-communication works (e.g., Sun et al. certifiably robust communication, Xue et al. mis-spoke/mis-lead). It contributes the attacker's perspective — exposing the weakest links in inter-agent communication — and connects adversarial-RL tempo/timing work (single-agent) to the multi-agent communication setting, while motivating future defence research (adversarial training, input correction). It is an attack/red-team counterpart to the defensive robust-MARL methods catalogued in the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Background and Related Work]_

"MARL extends deep RL to multi-agent problems and a unique aspect of multi-agent problems is communication, which is necessary for coordination and information sharing between agents. A common approach to communication allows agents to share their observations [28–30]. However, this may be impractical in real-world scenarios due to bandwidth or Size Weight And Power (SWAP) constraints. Instead, more efficient communication protocols can be learnt using MARL (MARL-Comms) [31]. The key properties of these algorithms for an attacker are the frequency of communication and the structure of the messages sent between agents. Reinforced Inter-Agent Learning (RIAL) [4] is a MARL-Comms algorithm that treats communication as an auxiliary reinforcement learning task and uses Deep Q-Networks (DQN) [32] to simultaneously learn action and message policies. This communication occurs once between timesteps, and the message is selected from a discrete set of possible messages. This contrasts with an approach such as CommNet [33], which features multiple rounds of communication during a timestep with a continuous set of messages."

> _[Section 2, Background and Related Work]_

"There have been a variety of AML attacks targeting MARL [34], but relatively few communication perturbation attacks, which occur when an adversary intercepts and perturbs the messages sent between agents. We consider communication perturbation attacks separate to malicious communication attacks as identified by Standen et al. [34], in which an adversary can inject new malicious messages into the system. Previous communication perturbations attacks targeted both MARL [8–10] and non-RL multi-agent [7] systems. The messages the adversary intercepts is a unique aspect of these attacks and there have been two approaches to selecting these messages, namely: broadcast and single victim. Broadcast attacks perturb a subset of messages that are broadcast to all agents in the system [7, 9, 10]. Single-victim attacks perturb a subset of messages received by a single agent in the system [8]. However, none of these works address which messages an adversary should perturb to maximise the effectiveness of an attack. Instead, they either preselect messages [7–9] without consideration of attack effectiveness, or attacked small multi-agent systems where there is only a single message to perturb [10]."

> _[Section 2, Background and Related Work]_

"Communication perturbation attacks rely on cleverly crafted perturbations that affect behaviour of a system. An adversary with white-box knowledge of the victim may use gradient-based methods to craft these perturbations. Single-step gradient methods, such as Fast Gradient Method (FGM) [17], uses the gradient of the input with respect to a particular loss function, and assumes a linear response from the network to find an effective perturbation. Another gradient-method Projected Gradient Descent (PGD) [18], iteratively applies FGM, allowing perturbations to correct for the non-linear response of the network. The default loss function used in these attacks is called the untargeted loss and aims to minimise the probability that the agent will output the same action as it would with unperturbed input. However, for RL systems, these untargeted attacks may cause the victim to select an alternate action with similar outcomes, thus the attack causes minimal impact against the system [19]. Instead, two-stage attacks first learn an adversarial policy which minimises the system reward and then uses a gradient method to cause the victim to output the actions selected by the adversarial policy [19–22]. Extending on this idea, RL-based attacks use deep RL to directly learn effective perturbations [8, 9, 23–26], forgoing the need of gradient-based perturbation crafting methods. However, RL can require significantly more time and computation than the original untargeted perturbation and the learnt functions can only target a specific environment or system."

> _[Section 2, Background and Related Work]_

"Adversarial attacks against MARL need to consider when to attack. Selecting an effective tempo allows an adversary to minimise the number of attacked timesteps without compromising attack effectiveness. Current tempo methods all target single-agent systems, and no published work, to the best of our knowledge, has considered the tempo of attacks against MARL. Fixed tempos do not consider the attack effectiveness and include tempos that attack every timestep [35] or attack a contiguous set of timesteps [11]. To improve attack effectiveness, counterfactual tempos simulate an attack [12], and learnt tempos train a deep RL agent to learn when to attack [12]. However, these methods can be costly due to the simulation and training time respectively. Threshold tempos measure certain properties of an agent's logits, and attack when that metric exceeds a hyperparameter threshold [11, 13–16]. Criticality-Based Timing Selection (CBTS) [15] uses the difference between the first and second highest logits, max(Q) − max2(Q). Max-Min Ratio (MMR) [16] uses the ratio between the maximum and minimum logits, max(Q) / (1 + min(Q)). Maximum Logit (ML) [16] uses the maximum logit, max(Q). Negative Skew (NS) [16] uses the negative skew in the logit distribution, 3×(mean(Q)−median(Q))/σ(Q). Variance of Logits (VL) [16] uses the variance of the logits, σ(Q). Strategically-Timed (ST) [11] uses the difference between largest and smallest logits, max(Q) − min(Q). A drawback of threshold tempos is the requirement to specify the attack tempo as a hyperparameter."

> _[Section 2, Background and Related Work — summary paragraph]_

"In summary, while there has been some work looking at communication perturbation attacks [7–10], these attacks do not address the key question of which messages an adversary should perturb to maximise attack effectiveness. The crafting of communication perturbations against MARL has heavily relied on deep RL-based methods which are costly to train. The question of when to attack has also not been addressed in previous communication perturbation attacks. In this work, we address these gaps by proposing a message selection method that identifies which messages should be perturbed to maximise the effectiveness of the attack, proposing new loss functions to improve the effectiveness of gradient-based perturbation crafting methods, and exploring victim selection methods by extending existing tempo functions and proposing a new tempo function."

> _[Introduction]_

"However, just changing the action taken by an agent may not be sufficient to impact the system because alternative actions may lead to similar outcomes. To overcome this problem, many approaches train a neural network using deep RL that can identify the actions with the highest impact that are then induced by gradient-based observation perturbations [19–22] or the network can directly perturb observations [23–26] and messages [8, 9] to cause high-impact actions. The limitation of these attacks is their reliance on high-compute resources and narrow application to a specific target."

### Cited references (resolved from the paper's bibliography)
- **[4]** J. Foerster, Y. Assael, N. de Freitas, S. Whiteson. *Learning to Communicate with Deep Multi-Agent Reinforcement Learning.* NeurIPS 2016.
- **[7]** J. Tu, T. Wang, J. Wang, S. Manivasagam, M. Ren, R. Urtasun. *Adversarial Attacks On Multi-Agent Communication.* IEEE/CVF ICCV 2021.
- **[8]** Y. Sun, R. Zheng, P. Hassanzadeh, Y. Liang, S. Feizi, S. Ganesh, F. Huang. *Certifiably Robust Policy Learning against Adversarial Multi-agent Communication.* ICLR 2023.
- **[9]** W. Xue, W. Qiu, B. An, Z. Rabinovich, S. Obraztsova, C. K. Yeo. *Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning.* AAMAS 2022.
- **[10]** X. Ma, W.-J. Li. *Grey-box Adversarial Attack on Communication in Multi-agent Reinforcement Learning.* AAMAS 2023.
- **[11]** Y.-C. Lin, Z.-W. Hong, Y.-H. Liao, M.-L. Shih, M.-Y. Liu, M. Sun. *Tactics of Adversarial Attack on Deep Reinforcement Learning Agents.* IJCAI 2017.
- **[12]** J. Sun, T. Zhang, X. Xie, L. Ma, Y. Zheng, K. Chen, Y. Liu. *Stealthy and Efficient Adversarial Attacks against Deep Reinforcement Learning.* AAAI 2020.
- **[13]** J. Kos, D. Song. *Delving into adversarial attacks on deep policies.* ICLR 2017.
- **[14]** Y. Qiaoben, X. Zhou, C. Ying, J. Zhu. *Strategically-timed State-Observation Attacks on Deep Reinforcement Learning Agents.* ICML Workshop on Adversarial Machine Learning 2021.
- **[15]** Y. Zheng, Z. Yan, K. Chen, J. Sun, Y. Xu, Y. Liu. *Vulnerability Assessment of Deep Reinforcement Learning Models for Power System Topology Optimization.* IEEE Transactions on Smart Grid 2021.
- **[16]** R. Praveen Kumar, I. Niranjan Kumar, S. Sivasankaran, A. Mohan Vamsi, V. Vijayaraghavan. *Critical State Detection for Adversarial Attacks in Deep Reinforcement Learning.* IEEE ICMLA 2021.
- **[17]** I. J. Goodfellow, J. Shlens, C. Szegedy. *Explaining and Harnessing Adversarial Examples.* ICLR 2015.
- **[18]** A. Madry, A. Makelov, L. Schmidt, D. Tsipras, A. Vladu. *Towards Deep Learning Models Resistant to Adversarial Attacks.* ICLR 2018.
- **[19]** J. Lin, K. Dzeparoska, S. Q. Zhang, A. Leon-Garcia, N. Papernot. *On the Robustness of Cooperative Multi-Agent Reinforcement Learning.* IEEE Security and Privacy Workshops 2020.
- **[20]** Y. Sun, R. Zheng, Y. Liang, F. Huang. *Who Is the Strongest Enemy? Towards Optimal and Efficient Evasion Attacks in Deep RL.* ICLR 2022.
- **[21]** X. Wan, L. Zeng, M. Sun. *Exploring the Vulnerability of Deep Reinforcement Learning-based Emergency Control for Low Carbon Power Systems.* IJCAI 2022.
- **[22]** Y. Qiaoben, C. Ying, X. Zhou, H. Su, J. Zhu, B. Zhang. *Understanding adversarial attacks on observations in deep reinforcement learning.* Science China Information Sciences 2024.
- **[23]** A. Russo, A. Proutiere. *Towards Optimal Attacks on Reinforcement Learning Policies.* American Control Conference 2021.
- **[24]** J. García, R. Majadas, F. Fernández. *Learning adversarial attack policies through multi-objective reinforcement learning.* Engineering Applications of Artificial Intelligence 2020.
- **[25]** A. Pattanaik, Z. Tang, S. Liu, G. Bommannan, G. Chowdhary. *Robust Deep Reinforcement Learning with adversarial attacks.* AAMAS 2018.
- **[26]** H. Zhang, H. Chen, C. Xiao, B. Li, M. Liu, D. Boning, C.-J. Hsieh. *Robust Deep Reinforcement Learning against Adversarial Perturbations on State Observations.* NeurIPS 2020.
- **[28]** O. Kilinc, G. Montana. *Multi-agent Deep Reinforcement Learning with Extremely Noisy Observations.* 2018.
- **[29]** N. Gupta, G. Srinivasaraghavan, S. Mohalik, N. Kumar, M. Taylor. *HAMMER: Multi-level coordination of reinforcement learning agents via learned messaging.* Neural Computing and Applications 2023.
- **[30]** X. Kong, B. Xin, F. Liu, Y. Wang. *Revisiting the Master-Slave Architecture in Multi-Agent Deep Reinforcement Learning.* 2017.
- **[31]** C. Zhu, M. Dastani, S. Wang. *A Survey of Multi-Agent Deep Reinforcement Learning with Communication.* Autonomous Agents and Multi-Agent Systems 2024.
- **[32]** V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wierstra, M. Riedmiller. *Playing Atari with Deep Reinforcement Learning.* Deep Learning Workshop 2013.
- **[33]** S. Sukhbaatar, A. Szlam, R. Fergus. *Learning Multiagent Communication with Backpropagation.* NeurIPS 2016.
- **[34]** M. Standen, J. Kim, C. Szabo. *Adversarial Machine Learning Attacks and Defences in Multi-Agent Reinforcement Learning.* ACM Computing Surveys 2025.
- **[35]** S. Huang, N. Papernot, I. Goodfellow, Y. Duan, P. Abbeel. *Adversarial Attacks on Neural Network Policies.* ICLR 2017.
