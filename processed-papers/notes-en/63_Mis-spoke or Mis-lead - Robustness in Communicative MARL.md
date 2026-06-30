# 63. Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning

## Metadata
- **Title**: Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning
- **Authors**: Wanqi Xue, Wei Qiu, Bo An, Zinovi Rabinovich, Svetlana Obraztsova, Chai Kiat Yeo
- **Affiliation**: Nanyang Technological University, Singapore
- **Venue**: AAMAS 2022 (Proc. of the 21st International Conference on Autonomous Agents and Multiagent Systems)
- **Link/arXiv**: arXiv:2108.03803v2 [cs.LG]

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks (adversarial / malicious messages sent by compromised agents in cooperative MARL); Byzantine failure (agents do not know which peers are malicious)
- **Method paradigm**: Adversarial training, learned message attack generation, two-stage message filter (anomaly detection + reconstruction), two-player zero-sum game, game-theoretic equilibrium via Policy-Space Response Oracle (PSRO) / Double Oracle, minimax (MaxMin) defense
- **Keywords**: Multi-Agent Communicative RL, adversarial communication, message attack, message filter, PSRO, Nash equilibrium

## TL;DR
The paper systematically studies adversarial communication in multi-agent communicative RL (MACRL) by (1) learning a model that generates optimal malicious messages to attack, (2) building a two-stage message filter (anomaly detector + reconstructor) to defend, and (3) formulating attack-defense as a two-player zero-sum game solved with a PSRO-based method (ℜ-MACRL) to maximize worst-case defending performance.

## Problem & Motivation
MACRL methods greatly improve multi-agent coordination under partial observability by letting agents exchange messages, but adversarial ML shows that ML models are vulnerable to manipulation. Adversarial inter-agent communication, especially in cooperative settings, has been largely uninvestigated. Prior work either introduced only random (non-designed, inefficient) noise into communication in competitive games and merely retrained models to adapt, or proposed defenses limited to attention-based MACRL whose performance against maliciously designed attacks is unclear. The paper fills this gap by studying maliciously designed message attacks and a general defense in cooperative MACRL.

## Robustness Setting
- **Threat model / uncertainty set**: There are N_adv malicious agents, each holding a private adversarial policy ξ that generates an adversarial message δ_adv based on its action-observation history and received/intended messages. The malicious message is formed by convexly combining (or summing) the original outgoing message with the adversarial message; malicious agents otherwise follow their original action/message policies to stay covert. The attacker minimizes the joint accumulated team reward. Black-box attack is assumed (attacker has no access to the defended DNN's internals). Two assumptions: (1) Byzantine Failure — agents have imperfect information on who is malicious; (2) Concealment — malicious agents do not communicate or cooperate with each other.
- **Setting**: cooperative (shared team reward, Dec-POMDP-Com); CTDE with explicit communication during execution; the attack-defense problem is cast as a two-player zero-sum game; online RL training (PPO + PSRO).

## Method
- **Problem formulation**: Models MACRL as a Dec-POMDP-Com ⟨S, M, A, P, R, Υ, O, C, N, γ⟩. Each agent has an action policy and a message policy; malicious agents additionally have an adversarial message policy ξ that injects adversarial messages into the communication protocol, contaminating the incoming messages and Q-values of benign agents.
- **Learning the attack**: A DNN f_μ parameterizes a multivariate Gaussian adversarial policy ξ (Gaussian chosen as max-entropy prior). The attacker is trained with PPO to minimize the accumulated team reward (its reward defined as the negative team reward), subject to a regularizer constraining the distance between the original and adversarial messages (Eq. 1).
- **Defense via two-stage message filter**: A learnable defender ζ = (h_d, g_r) is cascaded onto the communication protocol. An anomaly detector h_d outputs the probability that each incoming message is malicious; a reconstructor g_r recovers the flagged messages before they are aggregated and distributed. The filter is trained with PPO to maximize the team reward under attack, with a supervised regularizer guided by ground-truth malicious labels and a reconstruction loss; benign messages are also used so the reconstructor learns an identity mapping when no attack occurs (Eq. 2).
- **Achieving robust MACRL (ℜ-MACRL)**: Because a single filter can be exploited by an adaptive attacker, the attack-defense problem is formulated as a two-player zero-sum game ⟨Π, U⟩ with the defender utility as expected team return; an NE is sought via a MaxMin objective (Eq. 3). ℜ-MACRL is built on PSRO (a deep extension of Double Oracle): it maintains populations of attacker and defender policies, computes a meta-NE over the empirical utility table, adds best-response policies each iteration, and outputs mixed strategies for both players (Algorithm 1).

## Theoretical Contributions
None / mostly empirical. The work provides a problem formulation (adversarial communication in MACRL as a Dec-POMDP-Com and as a two-player zero-sum game) and uses PSRO to approximate a Nash equilibrium, but does not prove new convergence, sample-complexity, or equilibrium-existence results.

## Experiments
- **Environment/Benchmark**: Predator Prey (PP, grid) for CommNet; Traffic Junction (TJ, easy/hard) for TarMAC; StarCraft II / SMAC scenarios (3bane_vs_hM, 4bane_vs_hM, 1o_2r_vs_4r, 1o_3r_vs_4r) for NDQ. Categorized by explicit-communication type: Communication with Delay (CD), Local Communication (LC), Communication with Cost/limited bandwidth (CC).
- **Baselines**: State-of-the-art MACRL algorithms CommNet, TarMAC, NDQ (attacked, then defended); the "vanilla" defending method (single defending policy) is compared against ℜ-MACRL.
- **Evaluation metrics**: Test return / test win rate / success rate under attack and defense; expected utility of the defender (accumulated team return) trained with ℜ-MACRL (u^ℜ_ζ) vs. vanilla (u^vn_ζ); 95% confidence intervals over five random seeds.

## Key Results
- MACRL methods are vulnerable to learned message attacks: e.g., CommNet test return drops ~40% (p=0) and ~33% (p=−0.5) on Predator Prey; TarMAC success rate and NDQ win rate also drop markedly under attack.
- The two-stage message filter recovers multi-agent coordination, restoring test return/win rate close to the original converged performance (e.g., NDQ recovers to ~60% on 3bane_vs_hM and ~55% on 1o_2r_vs_4r).
- A single message filter is brittle and can be exploited by an adaptive attacker (e.g., ~30% / ~20% return drop on CommNet after the attacker retrains against a frozen filter); ℜ-MACRL consistently yields higher defender expected utility than the vanilla method across all algorithms and environments, including multi-attacker settings.
- Ablations show both the anomaly detector and the message reconstructor are critical; disabling either degrades defense performance.

## Limitations & Future Work
- Focuses on explicit communication (implicit-communication attacks are argued to be trivial/easily detectable and are excluded); assumes black-box attacks (white-box deemed too idealistic).
- Relies on assumptions of Byzantine failure and concealment (malicious agents do not coordinate), and the defender training uses ground-truth malicious-message labels as a regularizer during learning.
- Theoretical guarantees are not provided; results are empirical. Future work directions are not explicitly enumerated in the text. ("Not specified" for explicit future-work statements.)

## Relevance to Survey
This paper is a key reference on the **communication-robustness** line of robust MARL: it targets adversarial messages exchanged between cooperative agents (rather than environment/model uncertainty, state/observation, or action perturbations). It connects the adversarial-RL and adversarial-training literature (SA-MDP, ATLA, adversarial policies) to the cooperative MACRL setting, and exemplifies the **game-theoretic / minimax defense** method line by using a two-player zero-sum formulation with PSRO to obtain worst-case-robust defenders. It complements model-uncertainty robust MARL works and sits alongside Byzantine/fault-tolerant and attack-defense MARL themes.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Preliminaries and Related Work — "Multi-Agent Communicative Reinforcement Learning"]_

"There has been extensive research on encouraging communication between agents to improve performance on cooperative or competitive tasks. Among the recent advances, some design communication mechanisms to address the problem of when to communicate [13, 14, 30]; other lines of works, e.g., TarMac [6], focus on who to communicate. These works determine the two fundamental elements in communication, i.e., the message sender and the receiver. Apart from the two elements, the message itself is another element which is crucial in communication, i.e., what to communicate: Jaques et al. propose to maximize the social influence of messages [12]. Kim et al. encode messages such that they contain the intention of agents [15]. Some other works learn to send succinct messages to meet the limitations of communication bandwidth [39, 40, 44]. Despite significant progress in MACRL, if some agents are adversarial and send maliciously designed messages, multi-agent coordination will rapidly disintegrate as these messages propagate."

> _[Section 2, Preliminaries and Related Work — "Adversarial Training"]_

"Adversarial training is a prevalent paradigm for training robust models to defend against potential attacks [9, 33]. Recent literature has considered two types of attacks [5, 26, 35]: black-box attack and white-box attack. In black-box attack, the attacker does not have access to information about the attacked deep neural network (DNN) model; whereas in white-box attack, the attacker has complete knowledge, e.g., the architecture, the parameters and potential defense mechanisms, about the DNN model. We consider the black-box attack in our problem formulation, because the setting of the white-box attack is too idealistic and may not be applicable to many realistic adversarial scenarios. In adversarial training, the attacker tries to attack a DNN by corrupting the input via ℓ𝑝-norm (𝑝∈{1, 2, ∞}) attack [9]. The attacker carefully generates artificial perturbations to manipulate the input of the model. In doing so, the DNN will be fooled into making incorrect predictions or decisions."

> _[Section 2, Preliminaries and Related Work — "Adversarial Reinforcement Learning (RL)"]_

"Recent advances in adversarial machine learning motivate researchers to investigate the adversarial problem in RL [8, 20, 41]. SA-MDP [43] characterizes the problem of decision making under adversarial attacks on state observations. Lin et al. propose two tactics of attacks, i.e., the strategically-timed attack and the enchanting attack, which attack by injecting noise to states and luring the agent to a designated target [20]. Gleave et al. consider the problem of taking adversarial actions that change the environment and consequentially change the observation of agents [8]. ATLA [42] propose to train the optimal adversary to perturb state observations and improve the worst-case agent reward. The settings of these works are different from ours: we consider the multi-agent scenario and restrict the attacking approach to adversarial messages, which makes the detection of anomalies difficult. Tu et al. propose to attack on multi-agent communication [36]. However, their focus is on the representation-level, whereas we focus on the policy-level. Recently, there are some works considering a similar setting as ours [3, 22]. However, they either focus on random attacks in specific competitive games or the defence of specific communication methods."

> _[Introduction — discussion of prior adversarial-communication work]_

"Unfortunately, despite great importance, adversarial problems, especially adversarial inter-agent communication problems, remain largely uninvestigated in MACRL. Blumenkamp et al. show that, by introducing random noise in communication, agents are able to deceive their opponents in competitive games [3]. However, the attacks are not artificially designed and therefore inefficient. Besides, cooperative cases, where communication is more crucial, are neglected. They also fail to propose an effective defence, but merely retrain the models to adapt to the attacks. Mitchell et al. propose to generate weights of Attention models [37] through Gaussian process for defending against random attacks in attention-based MACRL [22]. However, the applicability of this approach is unsatisfactory, being limited to attention-based MACRL, and its performance on maliciously designed attacks is unclear."

### Cited references (resolved from the paper's bibliography)
- **[3]** Blumenkamp, Prorok. *The emergence of adversarial communication in multi-agent reinforcement learning.* CoRL 2020.
- **[5]** Carlini, Wagner. *Towards evaluating the robustness of neural networks.* IEEE Symposium on Security and Privacy (SP) 2017.
- **[6]** Das, Gervet, Romoff, Batra, Parikh, Rabbat, Pineau. *TarMAC: Targeted multi-agent communication.* ICML 2019.
- **[8]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial Policies: Attacking Deep Reinforcement Learning.* ICLR 2020.
- **[9]** Goodfellow, Papernot, Huang, Duan, Abbeel, Clark. *Attacking machine learning with adversarial examples.* OpenAI 2017.
- **[12]** Jaques, Lazaridou, Hughes, Gulcehre, Ortega, Strouse, Leibo, De Freitas. *Social influence as intrinsic motivation for multi-agent deep reinforcement learning.* ICML 2019.
- **[13]** Jiang, Lu. *Learning attentional communication for multi-agent cooperation.* NeurIPS 2018.
- **[14]** Kim, Moon, Hostallero, Kang, Lee, Son, Yi. *Learning to schedule communication in multi-agent reinforcement learning.* ICLR 2019.
- **[15]** Kim, Park, Sung. *Communication in multi-agent reinforcement learning: Intention Sharing.* ICLR 2021.
- **[20]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* IJCAI 2017.
- **[22]** Mitchell, Blumenkamp, Prorok. *Gaussian Process Based Message Filtering for Robust Multi-Agent Cooperation in the Presence of Adversarial Communication.* arXiv 2020.
- **[26]** Papernot, McDaniel, Goodfellow, Jha, Celik, Swami. *Practical black-box attacks against machine learning.* ACM Asia Conference on Computer and Communications Security 2017.
- **[30]** Singh, Jain, Sukhbaatar. *Learning when to communicate at scale in multiagent cooperative and competitive tasks.* ICLR 2018.
- **[33]** Szegedy, Zaremba, Sutskever, Bruna, Erhan, Goodfellow, Fergus. *Intriguing properties of neural networks.* ICLR 2014.
- **[35]** Tramèr, Kurakin, Papernot, Goodfellow, Boneh, McDaniel. *Ensemble adversarial training: attacks and defenses.* ICLR 2018.
- **[36]** Tu, Wang, Wang, Manivasagam, Ren, Urtasun. *Adversarial attacks on multi-agent communication.* arXiv 2021.
- **[37]** Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin. *Attention is all you need.* NeurIPS 2017.
- **[39]** Wang, He, Yu, Qiu, An, Rabinovich. *Learning efficient multi-agent communication: An information bottleneck approach.* ICML 2020.
- **[40]** Wang, Wang, Zheng, Zhang. *Learning Nearly Decomposable Value Functions Via Communication Minimization (NDQ).* ICLR 2019.
- **[41]** Xu, Wang, Raizman, Rabinovich. *Transferable environment poisoning: Training-time attack on reinforcement learning.* AAMAS 2021.
- **[42]** Zhang, Chen, Boning, Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary (ATLA).* ICLR 2021.
- **[43]** Zhang, Chen, Xiao, Li, Liu, Boning, Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations (SA-MDP).* NeurIPS 2020.
- **[44]** Zhang, Lin, Zhang. *Succinct and robust multi-agent communication with temporal message control.* arXiv 2020.
