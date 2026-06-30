# 58. Adversarial Deep Reinforcement Learning for Improving the Robustness of Multi-agent Autonomous Driving Policies

## Metadata
- **Title**: Adversarial Deep Reinforcement Learning for Improving the Robustness of Multi-agent Autonomous Driving Policies
- **Authors**: Aizaz Sharif, Dusica Marijan
- **Affiliation**: Simula Research Laboratory, Oslo, Norway
- **Venue**: 2022 29th Asia-Pacific Software Engineering Conference (APSEC) 2022
- **Link/arXiv**: https://github.com/T3AS/MAD-ARL (code repository)

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial agents (an adversarial driving car that creates natural-but-adversarial observations to drive victim autonomous cars into failure states: collisions and offroad steering); robustness against out-of-distribution inputs and adversarial attacks in vision-based autonomous driving.
- **Method paradigm**: Adversarial reinforcement learning (ARL); two-step adversarial testing + adversarial retraining; 2-player Markov game with a fixed-victim reduction to a single-player MDP; PPO policy gradient; empirical / engineering-focused.
- **Keywords**: autonomous driving, multi-agent, adversarial RL, adversarial testing, robustness, PPO, CARLA

## TL;DR
The paper proposes MAD-ARL, a two-step methodology that first trains an adversarial driving agent (via adversarial RL with two candidate reward functions) to drive vision-based DRL autonomous cars into failure states in a multi-agent urban environment, and then retrains the victim cars against that adversary to improve their robustness, reducing collisions and offroad steering errors.

## Problem & Motivation
Autonomous cars (ACs) using deep-learning-based driving software are prone to failures and known to be vulnerable to adversarial attacks, yet most prior testing work only detects errors without correcting them or improving robustness. Existing AC testing is also done in overly simplistic settings: single-agent SUTs, lane-keeping or mixed-traffic environments, rule-based driving systems, or offline dataset testing. There is a need for a comprehensive testing methodology that both discovers errors in AC driving models and improves the performance/robustness of the failing models in a realistic multi-agent, non-communicating, vision-based urban driving environment. The paper addresses three challenges: lack of robustness improvement after error detection, lack of realistic multi-agent vision-based evaluation, and the under-explored use of adversarial RL to both expose and fix DRL-based AC vulnerabilities.

## Robustness Setting
- **Threat model / uncertainty set**: A separate adversarial driving agent (α) acts in the same shared environment as the victim ACs. The adversary has no whitebox access to the victims' input state and no shared weights (blackbox); it influences victims only by taking driving actions that create "natural" yet adversarial visual observations (e.g., steering offroad while crossing the intersection). Victim weights are frozen during adversary training, reducing the 2-player game to a one-player MDP for the adversary; the model-free MDP dynamics are unknown. Two adversary reward functions are studied: Rcollision (maximize collision + offroad rate) and Roffroad (maximize offroad steering only).
- **Setting**: competitive, independent non-communicating multi-agent (two victim ACs T1, T2 + one adversary α); decentralized policies; online simulation-based training/testing (PPO, on-policy); partially observable vision-based inputs (84x84x3 camera images).

## Method
- Formulate adversarial AC testing as a 2-player Markov game M = (S, O, (A_T1, A_T2, A_α), P, (R_T1, R_T2, R_α)); each agent acts from its current observation and receives rewards.
- Step 1 (find failures): pre-train two victim AC policies (π_T1, π_T2) with PPO and no adversary; then freeze victim weights and train the adversary policy π_α to maximize discounted reward (a single-player MDP since victims are fixed); use the trained adversary to push victims into failure states by injecting natural adversarial observations.
- Two adversary reward designs: Rcollision rewards collisions and offroad steering (+5.0 collision term, +0.05 offroad term), while Roffroad rewards only offroad steering (+0.05 offroad term); victim reward penalizes collisions (−100.0 collision) and offroad steering, rewarding distance covered and forward speed, with a constant β to encourage staying in the ground-truth lane.
- Step 2 (improve robustness): unfreeze victim weights and retrain π_T1, π_T2 with the trained adversary kept in the environment, each maximizing its own discounted reward; retraining is done separately for each adversary reward type.
- Architecture: 84x84x3 camera images → convolutions and hidden layers → output layer with nine discrete actions reducible to Steer, Throttle, Brake; trained with PPO (clipping, KL target) and Adam.

## Theoretical Contributions
None / mostly empirical. The paper provides a Markov-game formulation and the fixed-victim MDP reduction but no convergence, equilibrium, or robustness-certification proofs.

## Experiments
- **Environment/Benchmark**: Vision-based high-fidelity urban driving simulation using CARLA (Town 3 scenario via the Python Carla API) integrated with Macad-gym and RLlib (Ray); three independent non-communicating agents spawned near a T-intersection (two victim ACs T1, T2 and one adversary α). Victims drive straight across the intersection; the adversary takes a left turn. Testing runs 50 episodes of 2000 simulation steps per agent.
- **Baselines**: Adversary-free trained victim AC policies (baseline) compared against (i) victim performance with an adversary present, and (ii) retrained victim performance with the adversary present; the two adversary reward functions Rcollision and Roffroad are also compared against each other.
- **Evaluation metrics**: CV (rate of collision with other vehicles), CR (rate of collision with any other road objects), OS (rate of offroad steering from the ground-truth lane), and TTFC (time to first collision, in seconds).

## Key Results
- Adversarial testing is effective at exposing failures: introducing either adversary increases collisions (with cars and objects) and offroad steering for both victims versus the collision-free baseline; the Roffroad-based adversary works better at inducing failures (higher collision and offroad rates) and drives victims into collisions earlier than Rcollision.
- Adversarial retraining improves robustness: victims retrained with the Roffroad-based adversary show reduced collisions and offroad steering and can recover after a first collision; e.g., for Roffroad, Victim 1 collision-with-cars drops from 0.2563 (after adversary) to 0.0831 (after retraining) and TTFC increases.
- The Rcollision-based adversary is less useful for retraining because its collision-focused, intentional crashes leave victims unable to recover; the authors argue collision-focused drivers are impractical for robustness improvement and that Roffroad (collision-free, natural adversarial observations) is the more effective approach for making ACs robust.
- A single adversary trained against one victim generalizes to simultaneously attack and help retrain more than one victim policy.

## Limitations & Future Work
- Evaluated only in a single T-intersection scenario with two victim ACs and one adversary; the collision-focused Rcollision adversary is shown to be impractical for retraining.
- Future work: extend to mass-traffic scenarios with more cars, pedestrians, and traffic-light networks; investigate how retraining the adversarial agent affects victim performance; explore and compare robustness of different DRL algorithms against different adversary types; vary training/testing episodic steps for evaluation.

## Relevance to Survey
This paper sits on the "adversarial agents / adversarial RL" line of robust MARL applied to a safety-critical multi-agent domain (autonomous driving). Rather than modeling uncertainty as a nature player or a robust MDP/Markov game with formal guarantees, it instantiates robustness empirically: an adversarial agent both exposes failures (adversarial testing) and serves as a curriculum for adversarial retraining (robustification). It connects the robust MARL theme to the adversarial-attack / safety / multi-agent autonomous-driving sub-literature and to single-agent adversarial-RL attack methods (e.g., adversarial policies), illustrating the testing-and-retraining flavor of robustness in vision-based, non-communicating competitive multi-agent settings.

## Related Work (verbatim excerpts from the paper)
> _[Section II, Related Work — preamble]_

"The majority of related work has focused on generating test scenarios for discovering errors in ACs and adversarial testing of ACs. The main limitations of these works are the lack of focus on improving the robustness of ACs once errors are discovered, as well as simplistic evaluation conditions. Next, we summarize the main approaches, discussing their benefits and limitations."

> _[Section II-B, Adversarial Testing of ACs]_

"Recent work [23] proposes to use RL-based driving agents to test connected cars by perturbing both the inputs and outputs of a car during training. However, this approach targets mixed-traffic driving with a single AC and multiple human-driven cars, thus it does not consider complex scenarios having more than one non-communicating AC agent. Another work [24] performs adversarial RL for testing a multi-agent driving environment by training more than one adversarial RL agent against one rule-based driving model. While the results look promising, the approach only covers the cases where the trained adversarial cars are exposed to a single non-AI model. As another limitation, the approach has not been evaluated on more complex adversarial driving scenarios, such as T-intersection, which we target in our work."

"Another work [22] uses RL to stress-test ACs in a simulated environment. The extension of this work [25] proposes the idea of reward augmentation for increasing the search space and also finding failure cases in driving policies. Compared to our work, they lack multi-agent test cases even on a small scale. Besides, the work is tested neither in a vision-based simulator nor in real-world driving conditions. Furthermore, while the work improves driving conditions for experiments, it uses adversarial perturbations as noise in the simulation model itself. In contrast, our work adds perturbations by the adversarial car's policy, thus adding adversarial actions as example trajectories for improving AC's driving policies."

"Authors in [20] proposes a Bayesian optimization-based method for testing ACs. Their method involves creating adversarial scenarios in a Carla-based urban driving simulation [38] to expose the weaknesses of autonomous driving policy. Another work [17] [18] also uses an optimization technique for producing physical attacks on driving lanes, in order to attack vision-based driving models. Compared to our work, these works are lacking multi-agent AC scenarios. Authors in [13] use a GAN model to generate adversarial objects able to attack LiDAR-based driving systems. Another work [39] uses GAN to apply metamorphic testing to CNN-based driving models. Authors in [40] propose a stress testing methodology for LiDAR based perception. Using a real-world driving dataset, they use various weather conditions to test the performance of autonomous driving systems. However, neither of these approaches has been tested in an RL-based multi-agent AC environment."

> _[Introduction — on DRL vulnerability and adversarial RL]_

"Third, deep reinforcement learning (DRL) algorithms are extensively used in training vision-based safe AC models in urban driving environments [28] [29] [30] [31] [32]. One way to test their driving behavior is using adversarial RL (ARL) since DRL is proven to be vulnerable multiple times against adversarial attacks. Existing research suggests that ARL-based agents can be effective in exposing vulnerabilities of DRL-based agents in a blackbox manner [33]. However, the idea has been explored in a simplistic driving environment [24] [23]. In our work, we make use of ARL for discovering effective attacking inputs that we further use to improve the robustness of DRL-based AC policies in a complex non-communicating vision-based urban driving environment. Specifically, we introduce ARL as part of a driving simulation in order to add adversarial actions against the AC policies under test. By doing so, we show not only find failure scenarios of the DRL-based ACs interacting with the adversarial drivers but to leverage effective adversarial actions to improve the AC driving robustness."

### Cited references (resolved from the paper's bibliography)
- **[13]** Y. Cao, C. Xiao, D. Yang, J. Fang, R. Yang, M. D. Liu, B. Li. *Adversarial objects against LiDAR-based autonomous driving systems.* arXiv 2019.
- **[17]** *Attacking vision-based perception in end-to-end autonomous driving models.* Journal of Systems Architecture 2020.
- **[18]** J. Yang, A. Boloor, A. Chakrabarti, X. Zhang, Y. Vorobeychik. *Finding physical adversarial examples for autonomous driving with fast and differentiable image compositing.* arXiv 2020.
- **[20]** Y. Abeysirigoonawardena, F. Shkurti, G. Dudek. *Generating adversarial driving scenarios in high-fidelity simulators.* ICRA 2019.
- **[22]** M. Koren, S. Alsaif, R. Lee, M. J. Kochenderfer. *Adaptive stress testing for autonomous vehicles.* IEEE Intelligent Vehicles Symposium (IV) 2018.
- **[23]** B. Chalaki, L. E. Beaver, B. Remer, K. Jang, E. Vinitsky, A. M. Bayen, A. A. Malikopoulos. *Zero-shot autonomous vehicle policy transfer: From simulation to real-world via adversarial learning.* ICCA 2020.
- **[24]** A. Wachi. *Failure-scenario maker for rule-based agent using multi-agent adversarial reinforcement learning and its application to autonomous driving.* IJCAI 2019.
- **[25]** A. Corso, P. Du, K. Driggs-Campbell, M. J. Kochenderfer. *Adaptive stress testing with reward augmentation for autonomous vehicle validation.* ITSC 2019.
- **[28]** M. Holen, R. Saha, M. Goodwin, C. W. Omlin, K. E. Sandsmark. *Road detection for reinforcement learning based autonomous car.* ICISS (ACM) 2020.
- **[29]** B. Tan, N. Xu, B. Kong. *Autonomous driving in reality with reinforcement learning and image translation.* 2018.
- **[30]** P. Almási, R. Moni, B. Gyires-Tóth. *Robust reinforcement learning-based autonomous driving agent for simulation and real world.* 2020.
- **[31]** *Deep reinforcement learning for autonomous driving.* 2018.
- **[32]** H. Porav, P. Newman. *Imminent collision mitigation with reinforcement learning and vision.* 21st International Conference on Intelligent Transportation Systems (ITSC) 2018.
- **[33]** A. Gleave, M. Dennis, C. Wild, N. Kant, S. Levine, S. Russell. *Adversarial policies: Attacking deep reinforcement learning.* ICLR 2020.
- **[38]** A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, V. Koltun. *CARLA: An open urban driving simulator.* CoRL 2017.
- **[39]** M. Zhang, Y. Zhang, L. Zhang, C. Liu, S. Khurshid. *DeepRoad: GAN-based metamorphic testing and input validation framework for autonomous driving systems.* ASE 2018.
- **[40]** H. Delecki, M. Itkina, B. Lange, R. Senanayake, M. J. Kochenderfer. *How do we fail? Stress testing perception in autonomous vehicles.* 2022.
