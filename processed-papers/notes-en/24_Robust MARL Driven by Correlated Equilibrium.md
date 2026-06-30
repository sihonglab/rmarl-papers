# 24. Robust Multi-Agent Reinforcement Learning Driven by Correlated Equilibrium

## Metadata
- **Title**: Robust Multi-Agent Reinforcement Learning Driven by Correlated Equilibrium
- **Authors**: Anonymous authors (double-blind submission)
- **Affiliation**: Not specified
- **Venue**: Under review as a conference paper at ICLR 2021
- **Link/arXiv**: Not specified

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial / faulty agent within a cooperative team (one agent makes mistakes or behaves adversarially, i.e., executes its "worst" action with some probability); robustness of cooperative MARL (CMARL) teams to agent malfunction.
- **Method paradigm**: Game-theoretic equilibrium (correlated equilibrium vs. decentralized equilibrium), team mini-max stochastic game, vanilla adversarial training, latent-variable model with mutual-information regularization (InfoGAN-style), QMIX value decomposition.
- **Keywords**: Robust CMARL, correlated equilibrium, team mini-max game, mutual information, global random variable, QMIX, SMAC

## TL;DR
The paper shows that under adversarial/faulty-agent settings, a decentralized (CTDE) equilibrium can be arbitrarily worse than a correlated equilibrium in stochastic team mini-max games, and proposes to recover correlation by giving all agents a shared global random variable plus a mutual-information loss, yielding markedly improved robustness over vanilla adversarial training on SMAC.

## Problem & Motivation
Cooperative MARL (CMARL) policies must be robust before real-world deployment, but if one agent makes mistakes (e.g., machine malfunction) or behaves adversarially, the whole team may fail. Prior robust-MARL work mainly applies vanilla adversarial training within the standard centralized-training-decentralized-execution (CTDE) routine. The authors observe that once a CMARL environment contains an adversarial agent it is no longer fully cooperative, so the decentralized equilibrium produced by CTDE can perform significantly worse than the correlated equilibrium — a gap that, drawing on team mini-max normal/extensive form game theory, they extend to stochastic team mini-max games. The gap motivates urging agents toward a correlated equilibrium while preserving the convenience of decentralized execution.

## Robustness Setting
- **Threat model / uncertainty set**: A worst-case mini-max problem where (fixed i or for all i) one mistaken agent executes a "mistaken" policy πi,mis constrained by D(πi,mis‖πi) ≤ ε. The practical instantiation: the mistaken agent performs arg max_a Qi(s,a) with probability 1−ε and arg min_a Qi(s,a) (its own Q-minimizing "worst" action under QMIX, since ∂Qtot/∂Qi ≥ 0) with probability ε. Mistakes are assumed occasional and largely unrelated to the team goal / other agents' policies. Two test regimes: (1) one fixed agent makes mistakes; (2) all agents may make mistakes randomly, but at most one per timestep.
- **Setting**: Cooperative team versus an embedded adversarial/faulty agent (team mini-max stochastic game); CTDE-style training/execution that is augmented with a shared global random variable; online; partially observable (SMAC) and fully observable (theory examples).

## Method
- Formulate robust CMARL as a worst-case mini-max problem (Eq. 1) and instantiate a weaker version into QMIX: with probability ε the mistaken agent takes its Q-minimizing action (Eq. 2); train QMIX against these perturbed rollouts ("vanilla adversarial training" baseline).
- Theoretically argue that decentralized equilibrium can be arbitrarily worse than correlated equilibrium in stochastic team mini-max games (Propositions 1–2), so correlation must be learned for robustness.
- Inject a global random variable z (shared across all agents) as an extra input to each agent's Q network, changing Qi(oit, ait) into Qi(oit, zt, ait); agents can thereby coordinate on a correlated (stochastic) policy while only needing to share a random-number generator and seed (preserving decentralized execution). Proposition 3 shows a deterministic policy µi(s,z) equivalent to the team's optimal correlated stochastic policy exists.
- To stop agents from ignoring z, add a mutual-information objective (conditional MI I(z;a|o)) approximated by an InfoGAN/Barber–Agakov variational lower bound; define LI = −Σ_i E[log q(z|ai,oi)] and train with the overall loss Ltot = LRL + λI·LI (here LRL = QMIX TD loss). q(z|·) is modeled as a Gaussian via a neural network. Algorithm 1 gives the full training loop.

## Theoretical Contributions
- **Proposition 1**: There exists a stochastic game with Ecor/Edec > m^(n−2) (for the constructed example Ecor/Edec ≥ m^(2n−4)(1−γ)^2), showing the correlation-vs-decentralization gap can exceed the normal-form bound.
- **Proposition 2**: For any fixed k ∈ Z+ there exists a stochastic game with Ecor/Edec ≥ O(m^(k(n−2))), i.e., the gap can be made arbitrarily larger than in normal-form games.
- **Proposition 3**: For a fully observable, finite discrete-action MARL environment, if all agents receive a global continuous random variable z, there exists a deterministic policy µi(s,z) equivalent to the team's optimal correlated stochastic policy.

## Experiments
- **Environment/Benchmark**: SMAC (StarCraft Multi-Agent Challenge); QMIX as base algorithm; maps 8m, 2s3z, 3m, 3s5z chosen so QMIX is good in non-robust settings but not robust with selected agents. Two robust settings (fixed-mistaken-agent; random one-agent-per-timestep), 9 agent settings total. ε = 0.3 for 3m, ε = 0.5 for the others. Global variable: 3-D U(0,1); MI loss coefficient λI = 0.1.
- **Baselines**: NP (normal policy, trained without adversary, tested with adversary); VA (vanilla adversarial training); GV (adversarial training with global variable, no MI loss); GM (adversarial training with global variable + MI loss). Additional baseline NG (normal training with global variable + MI loss) to isolate the partial-observability benefit of a shared variable.
- **Evaluation metrics**: Test winning rate vs. training steps; mean test winning rate over 1000 episodes at various adversarial/random rates (0%–50%); comparison of relative improvements NG/NP vs. GM/VA. Runs repeated 5 times; 25%/75% error bars.

## Key Results
- GM (global variable + MI loss) outperforms VA and GV in most settings; GV is sometimes but not always better than VA (without the MI loss agents tend to ignore z).
- Example mean test winning rates (Table 1): on 3s5z Agent 3, VA = 45.7 vs. GM = 73.5; on 2s3z Agent 4, VA = 53.9 vs. GM = 72.6 — large gains from adding correlation.
- The improvement of GM/VA generally exceeds that of NG/NP, supporting the claim that correlation matters more in robust settings than in normal settings (where a shared variable mainly helps with partial observability).
- Under purely random (non-adversarial) mistakes, GM yields a slight improvement over baselines.

## Limitations & Future Work
- A robust policy can slightly decrease non-robust performance; balancing performance and robustness is open.
- Only a weaker worst-case mini-max problem is solved; solving the real adversarial case (Eq. 1) remains future work.
- Only single-agent mistakes are considered; extending to all agents having some probability of error is left open.
- Only the most straightforward correlation method is used; whether more complex correlation methods give further gains in robust CMARL is an open problem.

## Relevance to Survey
This paper sits on the "agent failure / adversarial-agent within a cooperative team" line of robust MARL and connects the game-theoretic equilibrium theme (correlated vs. decentralized / team mini-max games) with the adversarial-training and value-decomposition (QMIX, CTDE) method lines. It is notable for arguing that the standard CTDE solution concept itself is inadequate under adversarial perturbation, and for introducing a shared-latent-variable + mutual-information mechanism to approximate correlated equilibria — relevant to surveying communication/coordination-based robustness and to comparisons with M3DDPG-style minimax robust MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Works — "Robust RL"]_

"The robustness in RL involves the perturbations occurring in different cases, such as state or observation, environment, action or policy, opponent's policy, etc. 1) For the robustness to state or observation perturbation, most works focused on adversarial attacks of image state/observation. Pattanaik et al. (2018) used gradient-based attack on image state, and vanilla adversarial training was adopted to obtain robust policy; Fischer et al. (2019) first trained a normal policy, and distilled it on adversarial states to achieve robustness; Ferdowsi et al. (2018) applied adversarial training to autonomous driving tasks that interfered agent's input sensors based on environment, and then conducted adversarial training; 2) For the robustness to environment, robust Markov decision process (MDP) could be used to formulate this problem. Many works (e.g. Wiesemann et al. (2013); Lim et al. (2013)) have studied this model and provided both theoretical analysis and algorithmic design. In deep RL scenario, Rajeswaran et al. (2016) used Monte Carlo approach to train agent, while Abdullah et al. (2019); Hou et al. (2020) adopted adversarial training to obtain a robust agent to all environments within a Wasserstein ball. Mankowitz et al. (2019) conducted adversarial training in MPO algorithm to optimize the performance in the worst performance environment. 3) To be against the perturbation of action or policy, Tessler et al. (2019); Gu et al. (2018); Vinitsky et al. (2020) considered the case that agent's action may be influenced by another action, and conducted adversarial training. 4) For the robustness to opponent, Pinto et al. (2017); Ma et al. (2018) focused on the case that agent's reward may be influenced by another agent, and adversarial training was implemented to solve the two-agent game to obtain a robust agent."

> _[Section 2, Related Works — "Correlated Equilibrium"]_

"Correlated equilibrium is a more general equilibrium in game theory compared to Nash equilibrium. In a cooperative task, if the team agents jointly make decisions together, then the optimal team policy is correlated equilibrium. Correlated equilibrium is widely studied in game theory (e.g. Hart & Mas-Colell (2001; 2000); Neyman (1997)). In team mini-max game, solving the team's correlated equilibrium in normal form game is straightforward (just treat the team as a single agent); Celli & Gatti (2017); Zhang & An (2020); Farina et al. (2018) proposed various algorithms to solve correlated equilibrium in extensive formal games. In deep RL scenario, Celli et al. (2019) applied vanilla hidden variable model to solve correlated equilibrium in simple repetitive environments, while information loss with hidden variable model was used in Chen et al. (2019) to solve correlated equilibrium in normal multi-agent environment."

> _[Introduction — prior robust CMARL work]_

"Therefore, in practice, we expect to have a multi-agent team policy in a fully cooperative environment that is robust when some agent(s) make some mistakes and even behave adversarially. To the best of knowledge, very few existing works on this issue mainly use vanilla adversarial training strategy. Klima et al. (2018) considered a two-agent cooperative case, in order to make the policy robust, agents become competitive with a certain probability during training. Li et al. (2019) provided a robust MADDPG approach called M3DDPG, where each agent optimizes its policy based on other agents' influenced sub-optimal actions."

> _[Introduction — CTDE vs. correlated equilibrium observation]_

"Most state-of-the-art MARL algorithms utilize centralized training and decentralized execution (CTDE) routine, since this setting is common in real world cases. The robust MARL method M3DDPG also followed the CTDE setting. However, existing works on team mini-max normal form or extensive form games show that if the environment contains an adversarial agent, then the decentralized equilibrium from CTDE routine can be significantly worse than the correlated equilibrium. We furthermore extend this finding into stochastic team mini-max games."

### Cited references (resolved from the paper's bibliography)
- **[Pattanaik et al. (2018)]** Pattanaik, Tang, Liu, Bommannan, Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* AAMAS 2018.
- **[Fischer et al. (2019)]** Fischer, Mirman, Vechev. *Online robustness training for deep reinforcement learning.* arXiv:1911.00887, 2019.
- **[Ferdowsi et al. (2018)]** Ferdowsi, Challita, Saad, Mandayam. *Robust deep reinforcement learning for security and safety in autonomous vehicle systems.* ITSC 2018.
- **[Wiesemann et al. (2013)]** Wiesemann, Kuhn, Rustem. *Robust Markov decision processes.* Mathematics of Operations Research, 38(1):153–183, 2013.
- **[Lim et al. (2013)]** Lim, Xu, Mannor. *Reinforcement learning in robust Markov decision processes.* NeurIPS 2013.
- **[Rajeswaran et al. (2016)]** Rajeswaran, Ghotra, Ravindran, Levine. *EPOpt: Learning robust neural network policies using model ensembles.* arXiv:1610.01283, 2016.
- **[Abdullah et al. (2019)]** Abdullah, Ren, Bou Ammar, Milenkovic, Luo, Zhang, Wang. *Wasserstein robust reinforcement learning.* arXiv:1907.13196, 2019.
- **[Hou et al. (2020)]** Hou, Pang, Hong, Lan, Ma, Yin. *Robust reinforcement learning with Wasserstein constraint.* 2020 (OpenReview, id=HkeeITEYDr).
- **[Mankowitz et al. (2019)]** Mankowitz, Levine, Jeong, Abdolmaleki, Springenberg, Mann, Hester, Riedmiller. *Robust reinforcement learning for continuous control with model misspecification.* arXiv:1906.07516, 2019.
- **[Tessler et al. (2019)]** Tessler, Efroni, Mannor. *Action robust reinforcement learning and applications in continuous control.* arXiv:1901.09184, 2019.
- **[Gu et al. (2018)]** Gu, Jia, Choset. *Adversary A3C for robust reinforcement learning.* 2018 (OpenReview, id=SJvrXqvaZ).
- **[Vinitsky et al. (2020)]** Vinitsky, Du, Parvate, Jang, Abbeel, Bayen. *Robust reinforcement learning using adversarial populations.* arXiv:2008.01825, 2020.
- **[Pinto et al. (2017)]** Pinto, Davidson, Sukthankar, Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Ma et al. (2018)]** Ma, Driggs-Campbell, Kochenderfer. *Improved robustness and safety for autonomous vehicle control with adversarial reinforcement learning.* IEEE Intelligent Vehicles Symposium (IV) 2018.
- **[Hart & Mas-Colell (2000)]** Hart, Mas-Colell. *A simple adaptive procedure leading to correlated equilibrium.* Econometrica, 68(5):1127–1150, 2000.
- **[Hart & Mas-Colell (2001)]** Hart, Mas-Colell. *A reinforcement procedure leading to correlated equilibrium.* In Economics Essays, pp. 181–200, Springer, 2001.
- **[Neyman (1997)]** Neyman. *Correlated equilibrium and potential games.* International Journal of Game Theory, 26(2):223–227, 1997.
- **[Celli & Gatti (2017)]** Celli, Gatti. *Computational results for extensive-form adversarial team games.* arXiv:1711.06930, 2017.
- **[Zhang & An (2020)]** Zhang, An. *Computing team-maxmin equilibria in zero-sum multiplayer extensive-form games.* AAAI 2020, pp. 2318–2325.
- **[Farina et al. (2018)]** Farina, Celli, Gatti, Sandholm. *Ex ante coordination and collusion in zero-sum multi-player extensive-form games.* NeurIPS 2018, pp. 9638–9648.
- **[Celli et al. (2019)]** Celli, Ciccone, Bongo, Gatti. *Coordination in adversarial sequential team games via multi-agent deep reinforcement learning.* arXiv:1912.07712, 2019.
- **[Chen et al. (2019)]** Chen, Guo, Zhang, Fang, Zhu, Zhou, Zhang, Wang, Yu. *Signal instructed coordination in team competition.* arXiv:1909.04224, 2019.
- **[Klima et al. (2018)]** Klima, Bloembergen, Kaisers, Tuyls. *Learning robust policies when losing control.* Adaptive and Learning Agents workshop at AAMAS, 2018.
- **[Li et al. (2019)]** Li, Wu, Cui, Dong, Fang, Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient (M3DDPG).* AAAI 2019, vol. 33, pp. 4213–4220.
