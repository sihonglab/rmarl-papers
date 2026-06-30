# 72. Robust Multi-Agent Reinforcement Learning with Social Empowerment for Coordination and Communication

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning with Social Empowerment for Coordination and Communication
- **Authors**: Tessa van der Heiden, Herke van Hoof, Efstratios Gavves, Christoph Salge
- **Affiliation**: BMW Group; University of Amsterdam; University of Hertfordshire
- **Venue**: Not specified (arXiv preprint, arXiv:2012.08255, 15 Dec 2020)
- **Link/arXiv**: arXiv:2012.08255v1 [cs.MA]

## Taxonomy
- **Robustness / perturbation type targeted**: Robustness to changes in other (partner) agents' behavior; overfitting to training partners in cooperative communication and coordination tasks (non-reactive policies that fail when partners alter their strategies or are replaced by novel partners).
- **Method paradigm**: Intrinsic social motivation; information-theoretic empowerment (transfer empowerment / joint empowerment) used as an additional reward term; variational lower-bound estimation of mutual information; actor-critic (DDPG/MADDPG-based) with centralized training and decentralized execution.
- **Keywords**: Social empowerment, transfer empowerment, joint empowerment, intrinsic motivation, cooperative MARL, communication and coordination

## TL;DR
The paper biases cooperative MARL toward "reactive" rather than overfitted policies by adding social empowerment (the potential causal influence between agents' actions, measured via mutual information) as an extra reward, yielding faster learning, higher rewards, and higher success rates across three communication/coordination tasks.

## Problem & Motivation
A central problem in MARL is that agents — especially those trained in a centralized way — can derive strong policies that are overfitted to their partners' behavior: they adopt strategies that expect other agents to act in a certain way rather than react to their actions. Such agents are brittle and may fail when partners alter their strategies during learning or deployment, or when they must collaborate with novel partners. The authors define robustness as a training agent's ability to deal with changes in the other agents' behavior, and aim to obtain policies that stay reactive to such changes. They seek an additional reward that (1) applies, with minimal adaptation, to a wide range of problems with different sensor-actuator configurations (preserving the universality of the RL framework), and (2) does not negatively affect performance once good policies are found. They note that optimizing for the mutual information between agents' actions (social influence) requires policies to keep a certain degree of entropy, which may interfere with an exploitation strategy — a gap that empowerment (potential rather than actual information flow) avoids.

## Robustness Setting
- **Threat model / uncertainty set**: The "perturbation" is the change in training partners' policies (all agents change their policies during training, and partners may differ or be novel at deployment). There is no explicit adversary or uncertainty set; instead, robustness is sought by incentivizing agents to remain responsive (reactive) to others. The authors frame their problem as one-shot adaptation: the policy should quickly adapt if other agents alter their policies.
- **Setting**: Fully cooperative; Dec-POMDP; centralized training with decentralized execution (CTDE); online / model-free with experience replay.

## Method
- Define **transfer empowerment** between a pair of agents as the maximum mutual information between one agent's action a_t^k and another agent's later action a_{t+1}^j, conditioned on the current and next states (Eq. 1): E_{T,k→j}(s_t) = max_{ω_k} I[a_{t+1}^j, a_t^k | s_t]. This captures the potential causal influence (channel capacity) one agent has on another; for multiple agents, transfer empowerment to agent j is summed over all other agents. Unlike Salge and Polani (2017), it uses action→action influence (not action→sensor) and considers potential rather than actual information flow, so action distributions can be narrow without harming exploitation.
- Introduce **joint empowerment** as a scalable proxy (Eq. 2): E_J(s_t) = max_ω I[s_{t+1}, a_t | s_t], the empowerment from all agents' joint actions to the next state. It scales linearly (not quadratically) with the number of agents, upper-bounds each agent's self-empowerment, and measures the group's collective controllability.
- **Augment the reward** of each agent (Eq. 3): R_{i,t}(s_{t+1}, a_t, s_t) = r(a_t, s_t) + E(s_{t+1}), where r is the environmental reward and E is either transfer (E_T) or joint (E_J) empowerment. The combination encourages policies that both solve the task and remain reactive.
- **Estimation**: operate in continuous action-state space and maximize a variational lower bound on mutual information (Barber and Agakov 2003), following Karl et al. (2017). A source distribution ω(a_t, s_t) and a variational planning distribution q(a_t | s_{t+1}, s_t) are represented by neural networks; estimators are given for transfer (Eq. 4) and joint (Eq. 5) empowerment. A transition network p_ψ is trained to predict future states.
- Training is summarized in Algorithm 1 (policy π_φ^j trained with E_T) and Algorithm 2 (π_φ trained with E_J), using mini-batches, a Q-network Q_β, target networks, and gradient ascent on the empowerment-augmented objective.

## Theoretical Contributions
None / mostly empirical. The paper provides definitions and variational lower-bound estimators for transfer and joint empowerment and notes that joint empowerment upper-bounds single-agent self-empowerment, but offers no convergence, sample-complexity, or equilibrium-existence guarantees.

## Experiments
- **Environment/Benchmark**: Three tasks. (I) Cooperative Communication / Speaker-Listener and (II) Cooperative Navigation (Cover Landmarks), both built on OpenAI's Multi-Agent Particle Environment; (III) Cooperative Driving in a multi-agent car simulator combining the multi-agent and single-agent OpenAI Gym (three vehicles, top-view grayscale image observations, junctions and obstacles).
- **Baselines**: DDPG (Lillicrap et al. 2015), MADDPG (Lowe et al. 2017), and Social Influence (SI) (Jaques et al. 2019); compared against the proposed transfer (E_T) and joint (E_J) empowerment.
- **Evaluation metrics**: Average return / training curves; reward; average distance from landmark; target reach %; obstacle hit %; collision %; success % (all agents within .1 distance of distinct landmarks for the last 5 time steps); speaker alternating frequency; off-road %.

## Key Results
- Adding empowerment as an additional utility raises the average return and yields higher rewards faster on the first two tasks (training curves, Fig. 1).
- Cooperative Communication (Table 1): in the harder setting (L=6, C=5, O=6), E_{T,k→j} gives the best reward (-0.422), lowest average distance (0.072), highest target reach (61.1%), and lowest obstacle hit (31.1%), outperforming DDPG, MADDPG, and SI.
- Cooperative Navigation (Table 2): E_J achieves the best reward (-2.063), lowest collisions (13.3%), and highest success (95.9%); E_T is second best on most metrics. Both empowerment variants beat DDPG, MADDPG, and SI.
- Cooperative Driving (Table 3): agents trained with E_J outperform MADDPG on all metrics (e.g., fewer off-road, fewer obstacle hits, and fewer collisions at both junctions and obstacle scenarios), responding quicker and giving way to let other cars pass.

## Limitations & Future Work
- Transfer empowerment is computed per pair of agents and scales quadratically with the number of agents; joint empowerment is introduced as a more scalable (linear) proxy but does not give per-pair directionality.
- Empowerment estimation relies on variational lower bounds and learned source/planning/transition networks, introducing approximation error.
- Evaluation is limited to cooperative tasks and simulators.
- Future work: cooperation with partners not seen during training (e.g., humans); competitive settings where agents minimize opponents' empowerment; applications such as robots from different brands interacting with humans.

## Relevance to Survey
This work sits in the robust-cooperative-MARL line that targets robustness to partners' behavioral changes (overfitting to training partners), rather than environment/model uncertainty. It is methodologically distinct from minimax/adversarial robust MARL (e.g., M3DDPG) and from population-based / self-play and zero-shot coordination (Other-Play): instead it uses intrinsic social motivation (information-theoretic empowerment) as an auxiliary reward to keep policies reactive. It connects the robust MARL theme to the intrinsic-motivation / social-influence literature and to communication-robustness and coordination themes in the survey.

## Related Work (verbatim excerpts from the paper)
> _[Section 2.1, Related work — Robust Multi-Agent Reinforcement Learning]_

"There is a large body of research on constructing agents that are robust to their partners. In self-play, for example, agents train against themselves rather than a fixed opponent strategy to prevent developing exploitable strategies (Tesauro 1994). Population based-training goes one step further by training agents to play against a population of other agents rather than only a copy of itself. For instance, Jaderberg et al. (2018) and Lowe et al. (2017) train an ensemble of policies with a variety of collaborators and competitors. By using a whole population rather than only a copy of itself, the agent is forced to be robust to a wide variety of potential perturbations instead of a single perturbation. However, it requires a great deal of engineering because the policy parameters suitable for the previous environment are not necessarily the next stage's best initialization."

"Some works combine the minimax framework and MARL to find policies that are robust to opponents with different strategies. Minimax is a concept in game theory that can be applied to find an approach that minimizes the possible loss in a worst-case scenario (Osborne et al. 2004). Li et al. (2019) use it during training to optimize the reward for each agent under the assumption that all other agents act adversarial. We are interested in methods that can deal with perturbations in the training partners' behavior, which differs from dealing with partners with various strategies."

"In zero-shot coordination, agents need to cooperate with novel partners that are not seen during training. Other-play (Hu et al. 2020) constructs zero-shot coordination strategies by making their agents robust to how their partners break symmetries in the underlying system. We instead frame our problem as one-shot adaptation, i.e. our policy should be able to quickly adapt if the other agents alter their policies."

> _[Section 2.2, Related work — Intrinsic Social Motivation]_

"Due to centralized training in MARL, agents might adopt non-reactive strategies that may struggle with other agents' changing behaviors. Social intrinsic motivation can give an additional incentive to find reactive policies towards other agents."

"Intrinsic motivation (IM) in RL refers to reward functions that allow agents to learn interesting behavior, sometimes in the absence of an environmental reward (Chentanez, Barto, and Singh 2005). Computational models of IM are generally separated into two categories (Santucci, Baldassarre, and Mirolli 2012), (Baldassarre and Mirolli 2013), those that focus on curiosity (Burda et al. 2018), (Pathak et al. 2017) and exploration (Gregor, Rezende, and Wierstra 2016), (Eysenbach et al. 2018), and those that focus on competence and control (Oudeyer and Kaplan 2009), (Karl et al. 2017). The information-theoretic Empowerment formalism is in the latter category, trying to capture how much an agent is in control of the world it can perceive. Empowerment has produced robust behaviour linked to controllability, operationality and self-preservation - in both robots (van der Heiden et al. 2020), (Karl et al. 2017), (Leu et al. 2013) and simulations (Guckelsberger, Salge, and Colton 2016), with (de Abril and Kanai 2018) and without (Guckelsberger, Salge, and Togelius 2018) reinforcement learning and neural network approximations (Karl et al. 2017)."

"Empowerment has also been applied to multi-agent simulations, under the term of coupled empowerment maximization (Guckelsberger, Salge, and Colton 2016), in which it was used to produce supportive and antagonistic behavior. Of particular interest is the idea of transfer empowerment - a measure that quantifies behaviors such as collaboration, coordination, and lead-taking (Salge and Polani 2017). Empowerment has also been tested in collaborative scenarios involving humans and robots. In all scenarios, transfer empowerment provides an additional incentive for agents to interact and coordinate."

"There are similar techniques that quantify the interaction between agents for improving coordination between agents. Barton et al. (2018) analyze the degree of dependence between two agents' policies to measure coordination, specifically by using Convergence Cross Mapping (CCM). Strouse et al. (2018) show how agents can share (or hide) intentions by maximising the mutual information between actions and a categorical goal. One notably relevant work is by Jaques et al. (2019) that design social influence which is the influence of one agent on the policies of other agents, measured by the mutual information between action pairs of distinct agents. In contrast to social influence, transfer empowerment considers the potential mutual information or channel capacity. When optimizing for actual mutual information, then its value is bounded from above by the lowest entropy of both agent's action variables. This might easily interfere with an exploitation strategy and may need to be regularized once a good strategy is found. On the other hand, empowerment does not have this limitation and the action sets could have very narrow distributions."

> _[Introduction]_

"Robust Reinforcement learning (RL) was introduced by Morimoto and Doya (2005) considering the generalization ability of the learned policy in the single-agent setting. We consider robustness to be a training agent's ability to deal with changes in the other agents' behavior."

### Cited references (resolved from the paper's bibliography)
- **(Tesauro 1994)** Tesauro, G. *TD-Gammon, a self-teaching backgammon program, achieves master-level play.* Neural Computation 6(2):215–219, 1994.
- **(Jaderberg et al. 2018)** Jaderberg, Czarnecki, Dunning, Marris, Lever, Castaneda, et al. *Human-level performance in first-person multiplayer games with population-based deep reinforcement learning.* arXiv:1807.01281, 2018.
- **(Lowe et al. 2017)** Lowe, Wu, Tamar, Harb, Abbeel, Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS (Advances in Neural Information Processing Systems), 6379–6390, 2017.
- **(Osborne et al. 2004)** Osborne, M. J., et al. *An introduction to game theory*, volume 3. Oxford University Press, New York, 2004.
- **(Li et al. 2019)** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI Conference on Artificial Intelligence, vol. 33, 4213–4220, 2019.
- **(Hu et al. 2020)** Hu, Lerer, Peysakhovich, Foerster. *"Other-Play" for Zero-Shot Coordination.* arXiv:2003.02979, 2020.
- **(Chentanez, Barto, and Singh 2005)** Chentanez, Barto, Singh. *Intrinsically motivated reinforcement learning.* NeurIPS (Advances in Neural Information Processing Systems), 1281–1288, 2005.
- **(Santucci, Baldassarre, and Mirolli 2012)** Santucci, Baldassarre, Mirolli. *Intrinsic motivation mechanisms for competence acquisition.* IEEE International Conference on Development and Learning and Epigenetic Robotics (ICDL), 1–6, 2012.
- **(Baldassarre and Mirolli 2013)** Baldassarre, Mirolli. *Intrinsically motivated learning in natural and artificial systems.* Springer, 2013.
- **(Burda et al. 2018)** Burda, Edwards, Pathak, Storkey, Darrell, Efros. *Large-scale study of curiosity-driven learning.* arXiv:1808.04355, 2018.
- **(Pathak et al. 2017)** Pathak, Agrawal, Efros, Darrell. *Curiosity-driven exploration by self-supervised prediction.* CVPR Workshops, 16–17, 2017.
- **(Gregor, Rezende, and Wierstra 2016)** Gregor, Rezende, Wierstra. *Variational intrinsic control.* arXiv:1611.07507, 2016.
- **(Eysenbach et al. 2018)** Eysenbach, Gupta, Ibarz, Levine. *Diversity is all you need: Learning skills without a reward function.* arXiv:1802.06070, 2018.
- **(Oudeyer and Kaplan 2009)** Oudeyer, Kaplan. *What is intrinsic motivation? A typology of computational approaches.* Frontiers in Neurorobotics 1:6, 2009.
- **(Karl et al. 2017)** Karl, Soelch, Becker-Ehmck, Benbouzid, van der Smagt, Bayer. *Unsupervised real-time control through variational empowerment.* arXiv:1710.05101, 2017.
- **(van der Heiden et al. 2020)** van der Heiden, Weiss, Shankar, Gavves, van Hoof. *Social navigation with human empowerment driven reinforcement learning.* arXiv:2003.08158, 2020.
- **(Leu et al. 2013)** Leu, Ristić-Durrant, Slavnić, Glackin, Salge, Polani, Badii, Khan, Raval. *CORBYS cognitive control architecture for robotic follower.* Proceedings of the 2013 IEEE/SICE International Symposium on System Integration, 394–399, 2013.
- **(Guckelsberger, Salge, and Colton 2016)** Guckelsberger, Salge, Colton. *Intrinsically motivated general companion NPCs via coupled empowerment maximisation.* 2016 IEEE Conference on Computational Intelligence and Games (CIG), 1–8, 2016.
- **(de Abril and Kanai 2018)** de Abril, Kanai. *A unified strategy for implementing curiosity and empowerment driven reinforcement learning.* arXiv:1806.06505, 2018.
- **(Guckelsberger, Salge, and Togelius 2018)** Guckelsberger, Salge, Togelius. *New and surprising ways to be mean: adversarial NPCs with coupled empowerment minimisation.* arXiv:1806.01387, 2018.
- **(Salge and Polani 2017)** Salge, Polani. *Empowerment as replacement for the three laws of robotics.* Frontiers in Robotics and AI 4:25, 2017.
- **(Barton et al. 2018)** Barton, Waytowich, Zaroukian, Asher. *Measuring collaborative emergent behavior in multi-agent reinforcement learning.* International Conference on Human Systems Engineering and Design: Future Trends and Applications, 422–427, Springer, 2018.
- **(Strouse et al. 2018)** Strouse, Kleiman-Weiner, Tenenbaum, Botvinick, Schwab. *Learning to share and hide intentions using information regularization.* NeurIPS (Advances in Neural Information Processing Systems), 10249–10259, 2018.
- **(Jaques et al. 2019)** Jaques, Lazaridou, Hughes, Gulcehre, Ortega, Strouse, Leibo, De Freitas. *Social influence as intrinsic motivation for multi-agent deep reinforcement learning.* ICML (International Conference on Machine Learning), 3040–3049, PMLR, 2019.
- **(Morimoto and Doya 2005)** Morimoto, Doya. *Robust reinforcement learning.* Neural Computation 17(2):335–359, 2005.
