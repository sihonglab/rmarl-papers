# 99. Towards Comprehensive Testing on the Robustness of Cooperative Multi-agent Reinforcement Learning

## Metadata
- **Title**: Towards Comprehensive Testing on the Robustness of Cooperative Multi-agent Reinforcement Learning
- **Authors**: Jun Guo, Yonghong Chen, Yihang Hao, Zixin Yin, Yin Yu, Simin Li
- **Affiliation**: State Key Lab of Software Development Environment, Beihang University, Beijing, China; Yangzhou Collaborative Innovation Research Institute CO., LTD; No. 38 Research Institute of CETC
- **Venue**: Not specified (appears to be a workshop/conference paper; page numbers 115–122)
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: State/observation perturbation, action perturbation (adversarial policy / "traitor" agent), and reward perturbation (reward poisoning / reward flipping) in cooperative MARL
- **Method paradigm**: Robustness testing / adversarial attacks as a testing framework; gradient-based attack (FGSM), reward poisoning, adversarial policy; multi-aspect (state/action/reward) evaluation motivated by the MMDP formulation
- **Keywords**: c-MARL, robustness testing, adversarial attack, reward poisoning, adversarial policy, SMAC

## TL;DR
The paper proposes MARLSafe, the first robustness-testing framework for cooperative MARL (c-MARL) that, motivated by the multi-agent MDP, attacks algorithms comprehensively from three aspects—state, action and reward—and shows on SMAC that state-of-the-art c-MARL algorithms (QMIX, MAPPO) have low robustness in all three aspects.

## Problem & Motivation
Deep-neural-network–based c-MARL powers safety-critical applications (traffic management, power management, UAV control), but agent policies can be easily perturbed by adversarial examples, so robustness must be tested before deployment. Existing adversarial attacks for MARL could be used for testing but each targets only a single robustness aspect (reward, state, or action), whereas a c-MARL model can be attacked from any aspect; an algorithm robust in one aspect may still be vulnerable in another. To the authors' knowledge, no prior work tests the robustness of c-MARL algorithms comprehensively, and c-MARL attack literature is scarce ([21] being the only paper attacking c-MARL, and only in the state aspect).

## Robustness Setting
- **Threat model / uncertainty set**: An adversary ν(·) ∈ B(·) perturbs an element of the MMDP—state s, action a, or reward r—within an available perturbation set B(·), with the goal of minimizing the discounted return. State test: white-box FGSM (ℓ∞-norm, ε = 0.05) on observations to suppress the optimal-action logit. Reward test: training-time reward poisoning that flips the sign of the top k% (k = 10) of rewards per episode. Action test: a black-box adversarial policy where one agent is taken over as a "traitor" trained to minimize the team reward while teammates' policies are fixed; the traitor has no access to global state or other agents' observations.
- **Setting**: cooperative (c-MARL); CTDE; attacks span both training time (reward) and test time (state, action), in white-box (state) and black-box (action) settings.

## Method
- Formulate c-MARL as a multi-agent MDP (MMDP) ⟨S, {Aⁱ}, R, P, γ⟩ and cast adversarial attacks as an adversary ν(·) ∈ B(·) that perturbs state, action, or reward to minimize the discounted return Gₜ = Σ γᵏ rₜ₊ₖ, subject to small perturbation budgets.
- State Test: apply untargeted FGSM to agents' observations, ν(s) = s − ε·sign(∇Q_s(s, a*; π)), reducing the logit of the optimal action a* = argmaxₐ π(s) so agents pick worse, non-cooperative actions.
- Reward Test: at training time, flip the sign of the maximum k% of rewards per episode; ν(r) = r if r ≤ r_thresh, else −r. With k = 0 it is normal training; with k = 100 the policy minimizes team reward.
- Action Test: take control of one agent as a "traitor" and train an adversarial policy π_α (with DRQN) whose reward is the negation of the team reward, perturbing teammates (fixed policies) to maximize Σ γᵏ r′ₜ₊ₖ.
- MARLSafe combines these three attacks to (1) cover MMDP elements comprehensively, (2) test at both training and test time, and (3) run in white-box and black-box settings.

## Theoretical Contributions
None / mostly empirical (the paper provides attack formulations within the MMDP framework but no convergence, sample-complexity, or certified-robustness guarantees).

## Experiments
- **Environment/Benchmark**: StarCraft II Multi-Agent Challenge (SMAC) [32], using the EPyMARL framework; maps 2s3z (2 Stalkers, 3 Zealots) and 11m (11 Marines, modified from "10m vs 11m"); built-in AI difficulty level 7 (hardest).
- **Baselines**: c-MARL algorithms under test are QMIX [31] (value-based) and MAPPO [41] (policy-gradient based); both use CTDE.
- **Evaluation metrics**: win rate (WR), team reward (TR), mean number of dead allies (mDA), mean number of dead enemies (mDE); 32 episodes per experiment. Attack hyperparameters: state test FGSM ℓ∞ ε = 0.05; reward test flip rate k% = 10%; action test traitor trained with DRQN, reward normalized to [−20, 20].

## Key Results
- Without attack, QMIX and MAPPO reach ~100% win rate with near-maximal reward, surpassing the hardest built-in AI.
- Under state test, win rate drops drastically (QMIX from 100% to as low as 0–9.38%); MAPPO is relatively more robust than QMIX, suggesting the centralized training network (mixer/critic) contributes to robustness.
- Under reward test, all algorithms reach 0% win rate; poisoning only 10% of rewards corrupts training and the real reward keeps declining, producing "fleeing" behavior.
- Under action test, the single "traitor" causes great failure (win rate near 0%), even when allies outnumber enemies; QMIX shows somewhat better robustness than MAPPO on 11m.

## Limitations & Future Work
- The work is a testing/attack framework and does not propose defenses; the authors call for comprehensive defense methods that jointly cover state, action, and reward.
- Evaluation is limited to two algorithms (QMIX, MAPPO), two SMAC maps, and specific attack settings; broader benchmarking is implied but not provided.

## Relevance to Survey
This paper sits on the adversarial-attack / robustness-evaluation line of robust MARL, specifically for the cooperative (c-MARL) setting. It is notable for unifying state-, action-, and reward-aspect attacks under the MMDP formulation and arguing that robustness must hold simultaneously across all aspects. It connects the state-perturbation line (FGSM/observation attacks), the reward-poisoning / reward-corruption line, and the adversarial-policy ("traitor"/Byzantine teammate) line, providing a testing-oriented complement to defensive robust-MARL methods.

## Related Work (verbatim excerpts from the paper)

> _[Section 2.1, Related Work — Adversarial Attacks]_

"Szegedy et al. [34] first defined adversarial attacks and proposed L-BFGS attack to generate adversarial examples. By leveraging the gradient of the target model, Goodfellow et al. [11] proposed the Fast Gradient Sign Method (FGSM) to quickly generate adversarial examples. Since then, many types of adversarial attacks have been proposed, such as gradient-based attacks (PGD, C&W) [4,27], boundary-based attack (DeepFool) [29], saliency-based attack (JSMA) [30]. Brown et al. [3] first proposed advesarial patch, which adds a local patch with impressive textures to the input image. Liu et al. [26] proposed a patch attack towards automatic check-out in physical world. Wang et al. [38] proposed Dual Attention Suppression attack to make the adversarial patches both malign and beautiful. Adversarial attacks on machine learning models have been adequately investigated, showing the potential risk of neural networks when it comes to practical application."

> _[Section 2.2, Related Work — Multi-Agent Deep Reinforcement Learning]_

"Deep reinforcement learning methods tend to train a policy network which maps state observations to action probabilities. DRL algorithms can be roughly categorized into two types: policy-based and value-based algorithm. Policy based algorithms often rely on policy gradient, such as DDPG [20] and PPO [33]. Value based algorithms often predict the Q-value, such as Deep Q Network (DQN) [28]. In MARL tasks, the most straightforward way to acquire a policy is to train individual agents, which is called Independent Q-Learning (IQL) [35, 36]. However, this strategy is not efficient in MARL environments requiring cooperation. Recent works adopted CTDE framework, such as QMIX [31] and MAPPO [41], can enhance the cooperation of agents and achieve better performance. However, those algorithms also suffer from robustness problem, which have not been properly evaluated."

> _[Section 2.3, Related Work — Adversarial Attacks on DRL]_

"Huang et al. [16] evaluated the robustness of DRL policies by perturbing the observations through FGSM attack on Atari Games. Liu et al. [23] proposed a spatiotemporal attack for embodied agents, which generates adversarial textures in the navigation environment. Lin et al. [22] proposed an attack method which perturbs the observation at some crucial frames, and they achieved targeted attack for DRL policies. Behzadan and Munir [2] propose a black-box attack by introducing a surrogate policy to minimize the return. Han et al. [13] proposed reward flipping attack at train time in software-defined networking tasks. Gleave et al. [10] proposed the adversarial policy in competitive multi-agent settings, which trains an opponent agent while fix parameters of the victim policy to attack the victim model. To the best of our knowledge, [21] is the only paper to attack c-MARL by perturbing the input state of agent."

> _[Introduction]_

"Recently, it has been shown that adversarial examples [2, 10, 19, 21, 23, 40] are capable to perturb these safety-critical application with high-confidence, raising a serious concern on the robustness of c-MARL algorithms. Testing the robustness has been a promising solution for DNN models. Being able to thoroughly test the robustness of DNN models will benefit researchers to discover weakness in DNN models and policy makers to ensure safe deployment in many sensitive scenarios. Many highly-influential works have been published in computer vision communities to test robustness and interpret adversarial examples [9, 15, 17, 18, 24, 25, 37, 42] using multiple algorithms, metrics and attack settings. Recently, Behzadan et al. [1] also benchmarked the robustness of reinforcement learning (RL) algorithms towards different state perturbations. However, to the best of our knowledge, no work exists to test the robustness of c-MARL algorithm. Besides, from the perspective of multi-agent MDP, its possible for hackers to attack from the aspect of reward [13], state [22] and action [10]. While existing attack could be used as testing tool, they all focus on only one aspect (state, action, reward), making the test limited since c-MARL algorithm might be robust in one aspect, but hacker can attack from all possible aspects."

### Cited references (resolved from the paper's bibliography)
- **[1]** Behzadan, Hsu. *RL-based method for benchmarking the adversarial resilience and robustness of deep reinforcement learning policies.* International Conference on Computer Safety, Reliability, and Security (Springer) 2019.
- **[2]** Behzadan, Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* International Conference on Machine Learning and Data Mining in Pattern Recognition (Springer) 2017.
- **[3]** Brown, Mané, Roy, Abadi, Gilmer. *Adversarial patch.* arXiv:1712.09665, 2017.
- **[4]** Carlini, Wagner. *Towards evaluating the robustness of neural networks.* IEEE Symposium on Security and Privacy (S&P) 2017.
- **[9]** Gao, Saha, Prasad, Roychoudhury. *Fuzz testing based data augmentation to improve robustness of deep neural networks.* ICSE 2020.
- **[10]** Gleave, Dennis, Wild, Kant, Levine, Russell. *Adversarial policies: Attacking deep reinforcement learning.* arXiv:1905.10615, 2019.
- **[11]** Goodfellow, Shlens, Szegedy. *Explaining and harnessing adversarial examples.* arXiv:1412.6572, 2014.
- **[13]** Han, Rubinstein, Abraham, Alpcan, De Vel, Erfani, Hubczenko, Leckie, Montague. *Reinforcement learning for autonomous defence in software-defined networking.* International Conference on Decision and Game Theory for Security (Springer) 2018.
- **[15]** Huang, Joseph, Nelson, Rubinstein, Tygar. *Adversarial machine learning.* ACM Workshop on Security and Artificial Intelligence 2011.
- **[16]** Huang, Papernot, Goodfellow, Duan, Abbeel. *Adversarial attacks on neural network policies.* arXiv:1702.02284, 2017.
- **[17]** Kim, Feldt, Yoo. *Guiding deep learning system testing using surprise adequacy.* ICSE 2019.
- **[18]** Kurakin, Goodfellow, Bengio. *Adversarial machine learning at scale.* arXiv:1611.01236, 2016.
- **[19]** Liang, Wu, Fan, Wei, Cao. *Parallel rectangle flip attack: A query-based black-box attack against object detection.* ICCV 2021.
- **[20]** Lillicrap, Hunt, Pritzel, Heess, Erez, Tassa, Silver, Wierstra. *Continuous control with deep reinforcement learning.* arXiv:1509.02971, 2015.
- **[21]** Lin, Dzeparoska, Zhang, Leon-Garcia, Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[22]** Lin, Hong, Liao, Shih, Liu, Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* arXiv:1703.06748, 2017.
- **[23]** Liu, Huang, Liu, Xu, Ma, Chen, Maybank, Tao. *Spatiotemporal attacks for embodied agents.* ECCV (Springer) 2020.
- **[24]** Liu, Liu, Guo, Wang, Ma, Zhao, Gao, Xiao. *A comprehensive evaluation framework for deep model robustness.* arXiv:2101.09617, 2021.
- **[25]** Liu, Liu, Yu, Zhang, Liu, Tao. *Training robust deep neural networks via adversarial noise propagation.* IEEE Transactions on Image Processing, 2021.
- **[26]** Liu, Wang, Liu, Cao, Zhang, Yu. *Bias-based universal adversarial patch attack for automatic check-out.* ECCV (Springer) 2020.
- **[27]** Madry, Makelov, Schmidt, Tsipras, Vladu. *Towards deep learning models resistant to adversarial attacks.* arXiv:1706.06083, 2017.
- **[28]** Mnih, Kavukcuoglu, Silver, Graves, Antonoglou, Wierstra, Riedmiller. *Playing Atari with deep reinforcement learning.* arXiv:1312.5602, 2013.
- **[29]** Moosavi-Dezfooli, Fawzi, Frossard. *DeepFool: a simple and accurate method to fool deep neural networks.* CVPR 2016.
- **[30]** Papernot, McDaniel, Jha, Fredrikson, Celik, Swami. *The limitations of deep learning in adversarial settings.* IEEE European Symposium on Security and Privacy (EuroS&P) 2016.
- **[31]** Rashid, Samvelyan, Schroeder, Farquhar, Foerster, Whiteson. *QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning.* ICML 2018.
- **[33]** Schulman, Wolski, Dhariwal, Radford, Klimov. *Proximal policy optimization algorithms.* arXiv:1707.06347, 2017.
- **[34]** Szegedy, Zaremba, Sutskever, Bruna, Erhan, Goodfellow, Fergus. *Intriguing properties of neural networks.* arXiv:1312.6199, 2013.
- **[35]** Tampuu, Matiisen, Kodelja, Kuzovkin, Korjus, Aru, Aru, Vicente. *Multiagent cooperation and competition with deep reinforcement learning.* PLoS ONE 12(4):e0172395, 2017.
- **[36]** Tan. *Multi-agent reinforcement learning: Independent vs. cooperative agents.* International Conference on Machine Learning (ICML) 1993.
- **[37]** Tang, Gong, Wang, Liu, Wang, Chen, Yu, Liu, Song, Yuille, et al. *RobustART: Benchmarking robustness on architecture design and training techniques.* arXiv:2109.05211, 2021.
- **[38]** Wang, Liu, Yin, Liu, Tang, Liu. *Dual attention suppression attack: Generate adversarial camouflage in physical world.* CVPR 2021.
- **[40]** Wei, Chen, Goldblum, Wu, Goldstein, Jiang. *Towards transferable adversarial attacks on vision transformers.* arXiv:2109.04176, 2021.
- **[41]** Yu, Velu, Vinitsky, Wang, Bayen, Wu. *The surprising effectiveness of PPO in cooperative, multi-agent games (MAPPO).* arXiv:2103.01955, 2021.
- **[42]** Zhang, Liu, Liu, Xu, Yu, Ma, Li. *Interpreting and improving adversarial robustness with neuron sensitivity.* IEEE Transactions on Image Processing, 2020.
