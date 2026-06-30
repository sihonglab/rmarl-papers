# 155. Evaluating Robustness of Cooperative MARL: A Model-Based Approach

## Metadata
- **Title**: Evaluating Robustness of Cooperative MARL: A Model-Based Approach
- **Authors**: Anonymous authors (double-blind submission)
- **Affiliation**: Not specified (anonymized)
- **Venue**: Under review as a conference paper at ICLR 2023
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial state/observation perturbation (attack on the victim agents' state input); evaluation of c-MARL robustness via adversarial attacks; victim-agent selection.
- **Method paradigm**: Model-based adversarial attack; learned dynamics model + targeted failure state; constrained nonconvex optimization solved by proximal/projected gradient (PGD); mixed-integer program relaxed to a softmax-weighted neural selector for victim choice.
- **Keywords**: c-MARL robustness, model-based adversarial attack, state perturbation, dynamics model, victim agent selection, continuous control

## TL;DR
The paper proposes c-MBA, the first model-based adversarial attack on cooperative MARL (c-MARL) that learns a dynamics model and a targeted failure state to craft observation perturbations driving the team to low reward, and shows it is consistently stronger than model-free baselines while adding a novel victim-agent selection strategy and a data-driven failure-state procedure.

## Problem & Motivation
Deep RL agents are known to be vulnerable to adversarial perturbations, but almost all existing DRL attack work targets the single-agent setting; the robustness of cooperative multi-agent RL (c-MARL) against adversarial attacks has been rarely explored. Existing c-MARL attack methods are model-free (e.g., training an adversarial policy), which is sample-expensive and impractical (it may require controlling all agents to collect "bad" trajectories), and have only been evaluated on discrete-action SMAC. The paper aims to evaluate c-MARL robustness with a more practical model-based attack on continuous action spaces, and to exploit the unique multi-agent opportunity of selecting which agents to attack.

## Robustness Setting
- **Threat model / uncertainty set**: The adversary adds a bounded state perturbation Δs to the victim agents' input, constrained by an ℓp-norm budget ε (ℓ∞ and ℓ1 evaluated) and a box constraint [ℓS, uS]. Only agents in the victim set Vt are perturbed (Δsi = 0 for i ∉ Vt). The attacker uses a pre-trained dynamics model f (a surrogate of the environment) and a targeted failure state s_fail; policy parameters are frozen and no retraining of c-MARL agents is required. White-box setting is used for fair comparison, but the approach is stated to be applicable to black-box attacks via finite-difference gradient estimation.
- **Setting**: cooperative (c-MARL, maximize total team reward), modeled as a Dec-POMDP with continuous actions; attack/evaluation phase (agents already trained via MADDPG); the dynamics model is learned offline from collected transitions.

## Method
- **Attack formulation (c-MBA, Section 3.1)**: Solve min over Δs of d(ŝ_{t+1}, s_fail) subject to ŝ_{t+1} = f(s_t, a_t), a_t^i = π^i(s_t^i + Δs^i), the budget/box constraints, and Δs^i = 0 for non-victims. This pushes the predicted next state toward a damaging failure state, lowering team reward. The constrained nonconvex problem is solved by projected gradient descent (PGD) onto the intersection of the ℓp-ball and box (Appendix A), giving a stationary point (Alg. 1).
- **Learning the dynamics model**: Train f by minimizing prediction error ‖f(s_t, a_t; ϕ) − s_{t+1}‖² over transitions D = D_train ∪ D_random, where D_train uses the pre-trained policy and D_random uses a random policy (to avoid overfitting to the trained policy). Standard supervised learning (Alg. 4).
- **Data-driven failure state (Section 3.2)**: Instead of requiring expert knowledge of the state space, sort collected transitions by ascending reward and set s_fail to the resulting state of the lowest-reward transition (Alg. 2).
- **Victim-agent selection (Section 3.3)**: A mixed-integer program (binary selectors w_i, with Σw_i = n_v) chooses the most vulnerable n_v agents; this is relaxed to a continuous weighting W(s; θ) ∈ [0,1]^n implemented as a softmax-output neural network, jointly optimized with Δs by PGD, then the top-n_v weighted agents are kept (Alg. 3). Alg. 3 can be combined with Alg. 1 for an even stronger attack.

## Theoretical Contributions
- None / mostly empirical. The only formal guarantee stated is that the perturbation found by solving the optimization problem makes the dynamics-model-predicted next state closest to the failure state under the budget constraint; PGD on the relaxed nonconvex problem converges to a stationary point. No convergence/sample-complexity or certified-robustness results for the c-MARL system itself.

## Experiments
- **Environment/Benchmark**: Multi-agent MuJoCo (MA-MuJoCo) — Ant(4x2), HalfCheetah(2x3), HalfCheetah(6x1), Walker2d(2x3); and multi-agent particle environment MPE(3x5). Agents trained with MADDPG.
- **Baselines**: Model-free attacks — Uniform noise U(−ε, ε); Gaussian noise N(0, ε); and Lin et al. (2020) + iFGSM (adversarial policy trained for 1M timesteps to minimize team reward, used as target with iterative FGSM). Two c-MBA variants: c-MBA-F (expert-defined failure state) and c-MBA-D (data-driven failure state).
- **Evaluation metrics**: Mean team reward (lower reward = stronger attack) vs. noise level / attack budget ε, under ℓ∞ and ℓ1 constraints; episode length; percentage of team-reward reduction relative to baselines.

## Key Results
- c-MBA consistently outperforms all model-free baselines across all tested environments, reducing team reward up to 8–9×; under ε = 0.05 (ℓ∞) on Ant(4x2), c-MBA's team-reward reduction is on average 66%, 503%, and 806% more than Lin et al. (2020)+iFGSM, Gaussian, and Uniform respectively.
- The data-driven variant c-MBA-D matches or outperforms the expert-defined c-MBA-F in many cases, including the particle environment where no expert failure-state knowledge is available.
- Learned victim-agent selection (Alg. 3) beats fixed/random/greedy selection (e.g., on HalfCheetah(6x1), ε=0.05, ℓ∞: 33%, 80%, 35% more reduction than fixed/random/greedy); combining Alg. 3 with Alg. 1 can further lower team reward up to 267% more on Ant(4x2). Victim selection gives up to ~80% improvement over heuristic selection.
- Attack remains effective even with a crude dynamics model: a model trained on only 0.2M samples for 1 epoch is comparable to one trained on 1M samples (100 epochs) on Ant(4x2) under ℓ∞ and ℓ1.

## Limitations & Future Work
- The method evaluates (attacks) robustness rather than providing a robust training defense; no defense/robustification is proposed.
- There is no general procedure for specifying the target/failure observation; expert-defined targets are hand-chosen per environment based on prior knowledge (the data-driven approach mitigates but does not fully solve this).
- Experiments use agents trained with MADDPG on MA-MuJoCo and MPE only; broader c-MARL algorithms/benchmarks are not covered. (Future work directions are summarized only briefly in the conclusion.)

## Relevance to Survey
This paper sits on the "adversarial attack / state-observation perturbation" line of robust MARL, specifically robustness *evaluation* of cooperative MARL. It is closely related to single-agent adversarial-RL attack work (Huang et al.; Lin et al. 2017; Kos & Song; Weng et al.; Gleave et al.) and to the few prior c-MARL attack papers (Lin et al. 2020; Hu & Zhang 2022), extending them to continuous action spaces with a model-based formulation and a multi-agent-specific victim-selection mechanism. It provides a strong attack benchmark against which defensive/robust c-MARL methods can be measured.

## Related Work (verbatim excerpts from the paper)
> _[Introduction]_

"Deep neural networks are known to be vulnerable to adversarial examples, where a small and often imperceptible adversarial perturbation can easily fool the state-of-the-art deep neural network classifiers (Szegedy et al., 2013; Nguyen et al., 2015; Goodfellow et al., 2014; Papernot et al., 2016). Since then, a wide variety of deep learning tasks have been shown to also be vulnerable to adversarial attacks, ranging from various computer vision tasks to natural language processing tasks (Jia & Liang, 2017; Zhang et al., 2020; Jin et al., 2020; Alzantot et al., 2018)."

> _[Introduction]_

"Perhaps unsurprisingly, deep reinforcement learning (DRL) agents are also vulnerable to adversarial attacks, as first shown in (Huang et al., 2017) for atari games DRL agents. (Huang et al., 2017) study the effectiveness of adversarial examples on a policy network trained on Atari games under the situation where the attacker has access to the neural network of the victim policy. In (Lin et al., 2017), the authors further investigate a strategically-timing attack when attacking victim agents on Atari games at a subset of the time-steps. Meanwhile, (Kos & Song, 2017) use the fast gradient sign method (FGSM) (Goodfellow et al., 2014) to generate adversarial perturbation on the A3C agents (Mnih et al., 2016) and explore training with random noise and FGSM perturbation to improve resilience against adversarial examples. While the above research endeavors focus on actions that take discrete values, another line of research tackles a more challenging problem on DRL with continuous action spaces (Weng et al., 2019; Gleave et al., 2019). Specifically, (Weng et al., 2019) consider a two-step algorithm which determines adversarial perturbation to be closer to a targetted failure state using a learnt dynamics model, and (Gleave et al., 2019) propose a physically realistic threat model and demonstrate the existence of adversarial policies in zero-sum simulated robotics games. However, all the above works focused on the single DRL setting."

> _[Introduction]_

"While most of the existing DRL attack algorithms focus on the single DRL agent setting, in this work we propose to study the vulnerability of multi-agent DRL, which has been widely applied in many safety-critical real-world applications including swarm robotics (Dudek et al., 1993), electricity distribution, and traffic control (OroojlooyJadid & Hajinezhad, 2019). In particular, we focus on the collaborative multi-agent reinforcement learning (c-MARL) setting, where a group of agents is trained to generate joint actions to maximize the team reward. We note that c-MARL is a more challenging yet interesting setting than the single DRL agent setting, as now one also needs to consider the interactions between agents, which makes the problem becomes more complicated."

> _[Section 2, Related Work and Background — "Related work."]_

"Most of existing adversarial attacks on DRL agents are on single agent (Huang et al., 2017; Lin et al., 2017; Kos & Song, 2017; Weng et al., 2019) while there is only two other works (Lin et al., 2020; Hu & Zhang, 2022) that focus on the c-MARL setting. Whereas (Hu & Zhang, 2022) considers a different problem than ours where they want to find an optimally ”sparse” attack by finding an attack with minimal attack steps, (Lin et al., 2020) proposes a two-step attack procedure to generate state perturbation for c-MARL setting which is the most relevant to our work. However, there are two major differences between our work and (Lin et al., 2020): (1) their attack is only evaluated under the StarCraft Multi-Agent Challenge (SMAC) environment (Samvelyan et al., 2019) where the action spaces are discrete; (2) their approach is model-free as they do not involve learning the dynamics of the environment and instead propose to train an adversarial policy for a fixed agent to minimize the the total team rewards. The requirement on training an adversarial policy is impractical and expensive compared to learning the dynamics model. To the best of our knowledge, there has not been any work considering adversarial attacks on the c-MARL setting using model-based approach on continuous action spaces. In this paper, we perform adversarial attacks on agents trained using MADDPG (Lowe et al., 2017) on two multi-agent benchmarks including multi-agent MuJoCo and multi-agent particle environments. Note that in the setting of adversarial attacks, once the agents are trained, policy parameters will be frozen and we do not require any retraining of the c-MARL agents during our attack."

> _[Section 3.1, Discussion: difference between the baseline (Lin et al., 2020)]_

"We note that the most closely related to our work is (Lin et al., 2020), where they also propose an attack algorithm to destroy c-MARL. However, there are two major differences between their approach and ours: (1) Their method is a model-free approach based on training extra adversarial policies, which could be impractical as it requires a lot of samples and it may be difficult to collect the required ”bad” trajectories to minimize the team reward (this requires the full control of all the agents in the c-MARL setting which may not be available in practice). On the other hand, our c-MBA is a model-based approach, where we only need to have a rough surrogate of the environment. This is an more practical scenario, and even very crude dynamics model could make c-MBA effective (see Experiment (III) in Section 4). (2) They did not leverage the unique setting in MARL to select most vulnerable agent to attack, while in the next section, we show that with the victim agent selection strategy, we could make c-MBA an even stronger attack algorithm (also see Experiment (IV) for more details)."

### Cited references (resolved from the paper's bibliography)
- **[Szegedy et al., 2013]** C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, R. Fergus. *Intriguing properties of neural networks.* arXiv:1312.6199, 2013.
- **[Nguyen et al., 2015]** A. Nguyen, J. Yosinski, J. Clune. *Deep neural networks are easily fooled: High confidence predictions for unrecognizable images.* CVPR 2015.
- **[Goodfellow et al., 2014]** I. J. Goodfellow, J. Shlens, C. Szegedy. *Explaining and harnessing adversarial examples.* arXiv:1412.6572, 2014.
- **[Papernot et al., 2016]** N. Papernot, P. McDaniel, S. Jha, M. Fredrikson, Z. B. Celik, A. Swami. *The limitations of deep learning in adversarial settings.* IEEE EuroS&P 2016.
- **[Jia & Liang, 2017]** R. Jia, P. Liang. *Adversarial examples for evaluating reading comprehension systems.* arXiv:1707.07328, 2017.
- **[Zhang et al., 2020]** W. E. Zhang, Q. Z. Sheng, A. Alhazmi, C. Li. *Adversarial attacks on deep-learning models in natural language processing: A survey.* ACM TIST 11(3):1–41, 2020.
- **[Jin et al., 2020]** D. Jin, Z. Jin, J. T. Zhou, P. Szolovits. *Is BERT really robust? A strong baseline for natural language attack on text classification and entailment.* AAAI 2020.
- **[Alzantot et al., 2018]** M. Alzantot, Y. Sharma, A. Elgohary, B.-J. Ho, M. Srivastava, K.-W. Chang. *Generating natural language adversarial examples.* arXiv:1804.07998, 2018.
- **[Huang et al., 2017]** S. Huang, N. Papernot, I. Goodfellow, Y. Duan, P. Abbeel. *Adversarial attacks on neural network policies.* arXiv:1702.02284, 2017.
- **[Lin et al., 2017]** Y.-C. Lin, Z.-W. Hong, Y.-H. Liao, M.-L. Shih, M.-Y. Liu, M. Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* arXiv:1703.06748, 2017.
- **[Kos & Song, 2017]** J. Kos, D. Song. *Delving into adversarial attacks on deep policies.* arXiv:1705.06452, 2017.
- **[Mnih et al., 2016]** V. Mnih, A. P. Badia, M. Mirza, A. Graves, T. Lillicrap, T. Harley, D. Silver, K. Kavukcuoglu. *Asynchronous methods for deep reinforcement learning.* ICML 2016.
- **[Weng et al., 2019]** T.-W. Weng, K. Dj Dvijotham, J. Uesato, K. Xiao, S. Gowal, R. Stanforth, P. Kohli. *Toward evaluating robustness of deep reinforcement learning with continuous control.* ICLR 2019.
- **[Gleave et al., 2019]** A. Gleave, M. Dennis, C. Wild, N. Kant, S. Levine, S. Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[Dudek et al., 1993]** G. Dudek, M. Jenkin, E. Milios, D. Wilkes. *A taxonomy for swarm robots.* IEEE/RSJ IROS 1993.
- **[OroojlooyJadid & Hajinezhad, 2019]** A. OroojlooyJadid, D. Hajinezhad. *A review of cooperative multi-agent deep reinforcement learning.* arXiv:1908.03963, 2019.
- **[Lin et al., 2020]** J. Lin, K. Dzeparoska, S. Q. Zhang, A. Leon-Garcia, N. Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[Hu & Zhang, 2022]** Y. Hu, Z. Zhang. *Sparse adversarial attack in multi-agent reinforcement learning.* arXiv:2205.09362, 2022.
- **[Samvelyan et al., 2019]** M. Samvelyan, T. Rashid, C. Schroeder de Witt, G. Farquhar, N. Nardelli, T. G. J. Rudner, C.-M. Hung, P. H. S. Torr, J. Foerster, S. Whiteson. *The StarCraft Multi-Agent Challenge.* CoRR abs/1902.04043, 2019.
- **[Lowe et al., 2017]** R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* arXiv:1706.02275, 2017.
