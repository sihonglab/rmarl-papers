# 60. Robust Communicative Multi-Agent Reinforcement Learning with Active Defense

## Metadata
- **Title**: Robust Communicative Multi-Agent Reinforcement Learning with Active Defense
- **Authors**: Lebin Yu, Yunbo Qiu, Quanming Yao, Yuan Shen, Xudong Zhang, Jian Wang
- **Affiliation**: Department of Electronic Engineering, BNRist, Tsinghua University, Beijing, China
- **Venue**: AAAI 2024 (The Thirty-Eighth AAAI Conference on Artificial Intelligence)
- **Link/arXiv**: https://arxiv.org/abs/2312.11545

## Taxonomy
- **Robustness / perturbation type targeted**: Communication attacks (noises and adversarial perturbations on inter-agent messages); a subset of messages can be arbitrarily perturbed/replaced, while observations remain clean.
- **Method paradigm**: Active defense; per-message reliability estimation (supervised binary classification); decomposable message aggregation into action preference vectors with adjustable weights; compatible with adversarial training.
- **Keywords**: Robust communicative MARL, active defense, message reliability estimation, communication attacks, action preference decomposition

## TL;DR
The paper proposes an active defense strategy for robust communicative MARL — instead of passively treating all messages equally, agents estimate each received message's reliability from their own (unperturbed) observation and hidden state and reduce unreliable messages' impact on the final decision via a decomposable message-aggregation policy network (ADMAC).

## Problem & Motivation
Communication boosts cooperation in MARL, but real-world wireless channels are vulnerable to noise and adversarial attacks; perturbed (especially malicious) messages can severely degrade multi-agent performance even when observations are accurate. Existing robust communicative MARL methods predominantly adopt passive defense, where agents receive all messages equally and try to make safe decisions; since perturbed messages are mixed with useful ones, this indiscriminate reception leads to a "garbage in, garbage out" effect and makes it hard to balance robustness and performance. The paper highlights a key feature distinguishing robust communicative MARL from robust RL: attackers can only modify a part of the messages (but the modification is unbounded), so an agent can leverage its own unperturbed observations and hidden states to judge message reliability — a feature passive defense fails to exploit.

## Robustness Setting
- **Threat model / uncertainty set**: With N agents there are at most N×N messages per timestep; for each message the attacker has probability p to change it to a perturbed version, and agents receive messages without knowing which are perturbed. The perturbation strength ||m̂ − m|| is unbounded (strong attack model). Attacks may be adversarial or non-adversarial: adversarial objectives either minimize the chosen probability/preference of the best action (fA) or maximize the KL divergence between the original and perturbed action distributions (fB).
- **Setting**: Cooperative; communication-based Dec-POMDP; decentralized execution. Online (model-free, REINFORCE-based training). Observations are unperturbed; only messages are attacked.

## Method
- **Decomposable message aggregation policy net (fP)**: Restricts each message's influence to an action preference vector. It comprises a GRU module fHP (updates hidden state from observation), a base action generation module fBP (base preference vector from the hidden state), and a message-observation process module fMP (message preference vectors from observation + each received message). The total preference vector is vᵢᵗ = fBP(hᵢᵗ) + Σ_{j≠i} wᵢ(mⱼᵗ)·fMP(oᵢᵗ, mⱼᵗ), then Softmax gives the action distribution. The weight wᵢ(mⱼᵗ) defaults to 1 when no robustness is required; lowering it for malicious messages attenuates their impact.
- **Reliability estimator (fR)**: A classifier that takes (hᵢᵗ, oᵢᵗ, mⱼᵗ) and outputs a length-2 Softmax vector; its first component serves as the message weight wᵢ(mⱼᵗ) in the aggregation. Reliability is framed as binary classification.
- **Labeling criterion**: Assuming well-trained policies, a message is labeled reliable if it recommends the agent's "best action" (the action most likely chosen without perturbations), else unreliable; "recommends the kr-th action" means fMP(oᵢᵗ, mⱼᵗ)[kr] exceeds the average of the preference vector.
- **Three-stage training**: (1) Train the policy net and message encoders to maximize discounted return, with no attacks/defenses. (2) Generate a dataset by replacing 1/3 of messages with random perturbation (Attack I) and 1/3 with an L2-normed gradient-descent adversarial attack (Attack II); decisions are used only to label messages, not executed. (3) Train the MLP reliability estimator via Adam and cross-entropy loss. Uses a basic broadcast communication mechanism.

## Theoretical Contributions
- **Proposition 1**: For an agent deciding via the decomposable aggregation rule, if a message most/least recommends an action, incorporating it must increase/decrease the probability of choosing that action, and the magnitude varies monotonically with the message weight wᵢ(mⱼᵗ) (proof in Appendix A). Otherwise the contribution is mostly empirical.

## Experiments
- **Environment/Benchmark**: Three communication-critical cooperative tasks — Food Collector (predefined communication), Predator Prey (learned communication), and Treasure Hunt (learned communication), each with N = 5 agents.
- **Baselines**: TARMAC (attention-based communication, no robust technique), Adversarial Training (AT), and Ablated Message Ensemble (AME). All trained with an improved REINFORCE.
- **Evaluation metrics**: Average timesteps required to complete the task (lower is better), measured across attack probability p ∈ {0, 0.1, 0.2, 0.3}; mean and standard error over 500 test episodes and five seeds. Four attack types are applied: Gaussian attack (III), Monte-Carlo adversarial attack (IV), Fast Gradient Sign Method (V), and Projected Gradient Descent (VI), with adversarial objectives fA / fB. Ablation reports reliability-estimator recall/precision.

## Key Results
- ADMAC achieves the best overall performance across the three tasks and four attack types, outperforming TARMAC, AT, and AME, with the advantage attributed to the active defense strategy that judges message reliability from observations and hidden states.
- AT lowers timesteps under strong attacks versus TARMAC but has slightly worse attack-free baseline performance (the robustness–performance trade-off). AME provides some robustness but its attack-free baseline is poor because taking the consensus of all messages prevents agents from getting exclusive information.
- Ablation: the decomposable policy net (DPN) does not degrade baseline performance and sometimes adds a little robustness; the reliability estimator (RE) provides considerable robustness, especially against adversarial attacks; DPN+IRE (ideal estimator, 100% accuracy) is the best, and the gap between DPN+RE and DPN+IRE tracks the RE's classification quality (reported recall/precision: Food Collector 0.90/0.86, Predator Prey 0.87/0.84, Treasure Hunt 0.79/0.76).

## Limitations & Future Work
- In scenarios where messages are likely to carry unique information, judging whether a message is reliable is hard, leading to a decline in ADMAC's robustness.
- Future work: let agents aggregate information from a wider range of sources to better assess received messages, and extend the framework to continuous action spaces.

## Relevance to Survey
A representative work on the "communication-attack" robustness line within robust MARL. It explicitly contrasts robust communicative MARL with robust RL / robust MARL (which typically perturb observations or the environment model) and against passive-defense methods, proposing an active-defense paradigm based on per-message reliability estimation. It connects the adversarial-attack/defense theme, robust communication (e.g., TMC, R-MACRL, AME), and adversarial training, making it a useful anchor for the communication-robustness sub-area of the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section: Related Work]_

"TMC (Zhang, Zhang, and Lin 2020) is one of the earliest robust multi-agent communication frameworks. However, it only provides certain robustness against Gaussian noises and random message loss. Some recent researches have considered the existence of malicious attackers (Blumenkamp and Prorok 2021; Tu et al. 2021; Yuan et al. 2023; Sun et al. 2023), who perturb normal messages or send fake messages to disrupt normal operation of multi-agent systems. Agents within these frameworks commonly receive all messages equally and try to make robust decisions, which follows a passive defense idea conventional in robust RL (Havens, Jiang, and Sarkar 2018; Pattanaik et al. 2018). Notably, passive defense strategies fail to utilize one important feature of robust communicative MARL: unperturbed messages and hidden states can help identify fake messages to some extent. Unlike the aforementioned methods, R-MACRL (Xue et al. 2022) takes a rather proactive defense strategy, which is correcting perturbed messages. Since useful messages must contain some information unknown to the agents and attackers may replace the useful messages with manipulated ones, this strategy is not quite practical. Compared with them, while utilizing observations and hidden states, we have made corresponding preparations for the fact that it is impossible to perfectly judge received messages."

"Besides, we would like to differentiate our research from robust MARL. Following Sun et al., we make two important assumptions: 1) only a part of the messages might be perturbed; 2) the perturbation power is unlimited and the perturbed messages can be completely different from the original ones. As a comparison, robust MARL commonly assumes the observations of agents (Li et al. 2019) or the environment model (Zhang et al. 2020b) is perturbed. Some robust MARL techniques can be used in robust communicative MARL (e.g. adversarial training), but an active defense strategy can better utilize the features of this problem."

> _[Introduction]_

"Adversarial attacks and defenses in communicative MARL receive much less attention when compared to their counterparts in reinforcement learning (Mu et al. 2022). Current frameworks in this area (Ishii, Wang, and Feng 2022; Yuan et al. 2023) commonly follow the principle of passive defense, where agents treat all received messages equally and try to make relative safe decisions. Since perturbed messages are mixed with useful messages, this indiscriminate reception may lead to the result of “garbage in, garbage out”. We notice that robust communicative MARL has an important feature compared with robust RL: The attackers are only allowed to modify a part of the messages, while the modification is unlimited and perturbed messages can be quite different from the original ones. Inspired by noisy learning (Han et al. 2018), we propose an active defense strategy to utilize this feature: agents actively judge the reliability of messages based on their own unperturbed observations and hidden states (which contain history information) and reduce unreliable messages’ impact on the final decision."

> _[Section: Attack against Communication]_

"Attack against multi-agent communication has been a hot topic (Xue et al. 2022; Sun et al. 2023) recently since wireless communication is vulnerable to distractions and noises. These works commonly follow the setting that attackers only interfere a part of messages in the multi-agent system to disrupt collaboration. Based on them, we consider the following attack model."

### Cited references (resolved from the paper's bibliography)
- **[Zhang, Zhang, and Lin 2020]** Zhang, S. Q., Zhang, Q., Lin, J. *Succinct and robust multi-agent communication with temporal message control.* NeurIPS 2020.
- **[Blumenkamp and Prorok 2021]** Blumenkamp, J., Prorok, A. *The emergence of adversarial communication in multi-agent reinforcement learning.* Conference on Robot Learning (PMLR) 2021.
- **[Tu et al. 2021]** Tu, J., Wang, T., Wang, J., Manivasagam, S., Ren, M., Urtasun, R. *Adversarial attacks on multi-agent communication.* ICCV 2021.
- **[Yuan et al. 2023]** Yuan, L., Chen, F., Zhang, Z., Yu, Y. *Communication-Robust Multi-Agent Learning by Adaptable Auxiliary Multi-Agent Adversary Generation.* arXiv preprint arXiv:2305.05116, 2023.
- **[Sun et al. 2023]** Sun, Y., Zheng, R., Hassanzadeh, P., Liang, Y., Feizi, S., Ganesh, S., Huang, F. *Certifiably Robust Policy Learning against Adversarial Multi-Agent Communication.* ICLR 2023.
- **[Havens, Jiang, and Sarkar 2018]** Havens, A., Jiang, Z., Sarkar, S. *Online robust policy learning in the presence of unknown adversaries.* NeurIPS 2018.
- **[Pattanaik et al. 2018]** Pattanaik, A., Tang, Z., Liu, S., Bommannan, G., Chowdhary, G. *Robust Deep Reinforcement Learning with Adversarial Attacks.* AAMAS 2018.
- **[Xue et al. 2022]** Xue, W., Qiu, W., An, B., Rabinovich, Z., Obraztsova, S., Yeo, C. K. *Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning.* AAMAS 2022.
- **[Li et al. 2019]** Li, S., Wu, Y., Cui, X., Dong, H., Fang, F., Russell, S. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Zhang et al. 2020b]** Zhang, K., Sun, T., Tao, Y., Genc, S., Mallya, S., Basar, T. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Mu et al. 2022]** Mu, R., Ruan, W., Marcolino, L. S., Jin, G., Ni, Q. *Certified Policy Smoothing for Cooperative Multi-Agent Reinforcement Learning.* arXiv preprint arXiv:2212.11746, 2022.
- **[Ishii, Wang, and Feng 2022]** Ishii, H., Wang, Y., Feng, S. *An overview on multi-agent consensus under adversarial attacks.* Annual Reviews in Control, 2022.
- **[Han et al. 2018]** Han, B., Yao, Q., Yu, X., Niu, G., Xu, M., Hu, W., Tsang, I., Sugiyama, M. *Co-teaching: Robust training of deep neural networks with extremely noisy labels.* NeurIPS 2018.
