# 29. What is the Solution for State-Adversarial Multi-Agent Reinforcement Learning?

## Metadata
- **Title**: What is the Solution for State-Adversarial Multi-Agent Reinforcement Learning?
- **Authors**: Songyang Han, Sanbao Su, Sihong He, Shuo Han, Haizhao Yang, Shaofeng Zou, Fei Miao
- **Affiliation**: University of Connecticut (School of Computing); Sony AI; University of Illinois Chicago (ECE); University of Maryland College Park (Math & CS); University at Buffalo, SUNY (EE & CSE)
- **Venue**: Transactions on Machine Learning Research (TMLR) 2024
- **Link/arXiv**: arXiv:2212.02705v5 [cs.AI]; OpenReview https://openreview.net/forum?id=HyqSwNhM3x; code https://songyanghan.github.io/what_is_solution/

## Taxonomy
- **Robustness / perturbation type targeted**: Adversarial state perturbation / state observation uncertainty in MARL (each agent's state observation perturbed within an admissible, bounded "neighboring" set)
- **Method paradigm**: State-Adversarial Markov Game (SAMG) formulation, worst-case (minimax/maximin) robustness, game-theoretic solution-concept analysis (existence/non-existence), adversarial actor-critic with Gradient Descent Ascent (GDA)
- **Keywords**: state-adversarial MARL, SAMG, robust agent policy, worst-case expected state value, robust Nash equilibrium, RMA3C

## TL;DR
The paper formulates the State-Adversarial Markov Game (SAMG) to study MARL under adversarial state perturbations, proves that the usual solution concepts (state-robust totally optimal agent policy and robust total Nash equilibrium) do not always exist, introduces the "robust agent policy" that maximizes the worst-case expected state value (proven to exist for finite state/action spaces), and proposes the RMA3C actor-critic algorithm to learn such robust policies.

## Problem & Motivation
DRL-based MARL policies assume agents act on accurate state information, but DRL policies are vulnerable to adversarial state perturbation attacks where even small state changes cause drastically different actions, degrading multi-agent coordination (e.g., agents heading to the wrong landmarks). The adversarial state perturbation problem cannot be fully captured by POMDP/Dec-POMDP because the conditional observation probability cannot represent the worst-case uncertainty under adversarial attacks, and existing robust MARL work targets uncertainty in reward, transition dynamics, or training partners' policies rather than state. It is hard to formally analyze whether optimal or equilibrium solutions exist for MARL under adversarial state perturbations, motivating a principled study of fundamental properties and solution concepts.

## Robustness Setting
- **Threat model / uncertainty set**: Each agent i is paired with an adversary that chooses a perturbed state ρi within an admissible perturbed state set P_s^i ⊆ S (the true state s is always included; in experiments P_s^i is an ℓ∞-norm ball {ρi : ||ρi − s||∞ ≤ d} with perturbation budget d). The adversary policy χi(·|s) takes the true state s (adversaries know the true state) and outputs a perturbed state to minimize the agents' total expected return; agents act on the perturbed state ρi to maximize total expected return.
- **Setting**: cooperative / mixed multi-agent (shared stage-wise reward in the formulation; cooperative and competitive particle environments in experiments); centralized critic with per-agent actor and adversary networks (CTDE-style training); online model-free learning.

## Method
- Formulate the SAMG G = (N, S, A, r, P_s, p, γ, Pr(s0)): a Markov game where each agent has an associated adversary that perturbs the agent's state observation within an admissible set; under a fixed adversary the SAMG reduces to a Dec-POMDP, and under a fixed bijective adversary mapping it reduces to a standard Markov game.
- Analyze solution concepts: prove existence of an optimal adversary policy (by constructing an MDP for the joint adversary with negated reward), then prove non-existence of a state-robust totally optimal agent policy and of a robust total Nash equilibrium via counterexamples, because agents must trade off value across different states under perturbations.
- Introduce the worst-case expected state value objective E_{s0∼Pr(s0)}[ V̄_π(s0) ] and define the robust agent policy as the policy maximizing it; show this is equivalent to a maximin problem max_π min_χ Σ_{s0} Pr(s0) V_{π,χ}(s0).
- Propose the Robust Multi-Agent Adversarial Actor-Critic (RMA3C): each agent has one critic (true global state and action), one actor network πi, and one adversary network χi; the adversary network learns a perturbation vector Δi which is projected back into P_s^i, and a Gradient Descent Ascent (GDA) optimizer updates actors and adversaries to solve the maximin problem.

## Theoretical Contributions
- Existence of an optimal adversary policy for any given agent policy (Proposition 4.1).
- Non-existence of a state-robust totally optimal agent policy for SAMGs (Theorem 4.3).
- Existence and uniqueness of a robust state value function for each agent given others' policies, via contraction mapping / Banach fixed point theorem (Theorem 4.5); existence of a stage-wise equilibrium for each state (Theorem C.6).
- Non-existence of a robust total Nash equilibrium for SAMGs (Theorem 4.7).
- Equivalence of maximizing the worst-case expected state value to a maximin problem (Theorem 4.10), and existence of a robust agent policy for finite state/action SAMGs via the Weierstrass M-test, uniform limit theorem, and extreme value theorem (Theorem 4.11).

## Experiments
- **Environment/Benchmark**: Multi-agent particle environments (Lowe et al., 2017): cooperative navigation (CN), exchange target (ET), keep-away (KA), and physical deception (PD); also scaling experiments with 3/4/6 agents and varying perturbation budgets d.
- **Baselines**: MADDPG (Lowe et al., 2017), M3DDPG (Li et al., 2019), MAPPO (Yu et al., 2022), plus versions of these trained/tested under random state perturbations (truncated normal noise) and under well-trained adversary policies χ* (9 baselines total). MAPPO only reported on the fully cooperative CN and ET.
- **Evaluation metrics**: Mean episode reward (averaged over 2000 testing episodes / last 1000 training episodes, across 10 runs per scenario), under no perturbation, random perturbations, and well-trained adversarial perturbations.

## Key Results
- RMA3C consistently achieves higher mean episode rewards than the baselines under both random and adversarial state perturbations, achieving up to 58.46% higher mean episode rewards during training.
- With random state perturbations (Table 1), RMA3C achieves up to 46.56% higher mean episode rewards than the baselines; with well-trained adversaries χ* (Table 2), up to 54.02% higher.
- The well-trained adversary χ* is more effective at reducing agents' return than random perturbations, confirming it intentionally selects worst-case perturbations; RMA3C maintains its advantage as the number of agents increases (3, 4, 6 agents), while larger perturbation budgets d give adversaries more power and reduce agents' return.

## Limitations & Future Work
- The paper notes it is in general challenging to develop algorithms that compute optimal or equilibrium policies for MARL under uncertainties; further discussions and future directions are deferred to Appendix F (not summarized in the main text).
- The robust agent policy is motivated by non-existence results in specific instances but is intended for broader applicability; theory is established for finite state and finite action spaces.
- Experiments are limited to multi-agent particle environments; MAPPO comparison is restricted to fully cooperative tasks.

## Relevance to Survey
This is a foundational state-perturbation entry in the robust MARL landscape: it is the first to formally study solution concepts of MARL under adversarial state perturbations, complementing the model/reward/transition-uncertainty line (e.g., Zhang et al., 2020b) and the opponent/training-partner robustness line (M3DDPG, Li et al., 2019). It sits on the "state/observation perturbation" main line and the "worst-case / minimax adversarial training" method line, bridging single-agent state-adversarial robust RL (Zhang et al., 2020a; 2021) and the broader robust MARL theory; the SAMG formulation and the robust-agent-policy concept are reusable reference points for distributionally robust and certified-robustness MARL work.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — "Multi-Agent Reinforcement Learning (MARL)"]_

"The MARL has a long history in the AI field (Littman, 1994; Hu et al., 1998; Busoniu et al., 2008). Recent works have been investigated to encourage the collaboration of the agents by assigning rewards appropriately, such as a value decomposition network (Sunehag et al., 2018; Rashid et al., 2020; Su et al., 2021), subtracting a counterfactual baseline (Foerster & Farquhar, 2018), or an implicit method (Zhou et al., 2020). Multi-Agent Deep Deterministic Policy Gradient (MADDPG) proposes a centralized Q-function to alleviate the problem caused by the non-stationary environment (Lowe et al., 2017). The scalability issue of MARL can be alleviated by adding attention to the critic (Iqbal & Sha, 2019), using neighbor information (Qu et al., 2020), or using V-learning (Jin et al., 2021). The “team stochastic game” (Muniraj et al., 2018; Phan et al., 2020) splits the MARL agents into two teams to compete. However, during training, all methods assume that agents get the true state value. None of the recent MARL advances specifies how to deal with perturbed state values by malicious adversaries."

> _[Section 2, Related Work — "Robust Reinforcement Learning"]_

"Most existing robust MARL works focus on uncertainties in reward, transition dynamics, and training partners’ policies, while our work focuses on uncertainties in the state. Robust reinforcement learning can be traced back to Morimoto & Doya (2005) in the single-agent setting. With the advent of deep learning techniques, the robust MARL has been recently studied considering different types of uncertainties such as reward (Chen & Bowling, 2012; Zhang et al., 2020b), transition dynamics (Zhang et al., 2020b; Sinha et al., 2020; Hu et al., 2020; Yu et al., 2021; Wang et al., 2023), training partner’s type (Shen & How, 2021), training partners’ policies (Li et al., 2019; van der Heiden et al., 2020; Sun et al., 2021; 2022). The work in (Zhang et al., 2020b) considers the robust equilibrium of multi-agents with reward uncertainties where agents can access true state information at each stage. The work in Shen & How (2021) considers uncertain training partner’s type (e.g. adversary, neutral, or teammate) to the protagonist in two-player scenarios. The M3DDPG algorithm extends the MADDPG to get a robust policy for the worst situation by assuming all the training partners are adversaries (Li et al., 2019). However, none of the above MARL works consider the state perturbations."

"For adversarial state perturbations, there are some works (Mandlekar et al., 2017; Pinto et al., 2017; Pattanaik et al., 2018; Zhang et al., 2020a; 2021; Liang et al., 2022) considering a robust policy in single-agent reinforcement learning. Though the work (Lin et al., 2020a) studies state perturbation, only one single agent’s state observation can be perturbed in their MARL. The work (He et al., 2023) shows Nash equilibrium exists under a specific condition (bijective mapping for adversary policies). However, in this work, we show the Nash equilibrium is not a good solution concept as it can be corrupted by state perturbation adversaries. We also propose a new robust agent policy concept for state-adversarial MARL that is proven to exist."

> _[Introduction — adversarial state perturbation background]_

"Multi-Agent Reinforcement Learning (MARL) has been successfully used to solve problems such as multi-robot coordination (Hüttenrauch & Šošić, 2017), resource management (Pretorius et al., 2020), etc. However, Deep Reinforcement Learning (DRL) policies are vulnerable to adversarial state perturbation attacks (Behzadan & Munir, 2017; Pattanaik & Tang, 2017; Huang et al., 2017; Lin et al., 2017; Xiao et al., 2019). Even small changes to the state can lead to drastically different actions (Huang et al., 2017; Lin et al., 2017). To address this, it is important to develop robust policies that can handle adversarial state perturbations."

"The adversarial state perturbation problem cannot be fully understood using existing research on the Partially Observable Markov Decision Process (POMDP) or Decentralized Partially Observable Markov Decision Process (Dec-POMDP) (Oliehoek et al., 2016; Lerer et al., 2020), as the conditional observation probability cannot capture the worst-case uncertainty under adversarial attacks. Adversarial perturbations have a greater impact on an agent’s policy than random noise (Kos & Song, 2017; Pattanaik et al., 2018). However, due to the complexity of interactions among agents and adversaries, it remains challenging to formally analyze the existence of optimal or equilibrium solutions under adversarial state perturbations in MARL."

### Cited references (resolved from the paper's bibliography)
- **[Littman, 1994]** Michael L. Littman. *Markov games as a framework for multi-agent reinforcement learning.* Machine Learning Proceedings 1994, Elsevier.
- **[Hu et al., 1998]** Junling Hu, Michael P. Wellman, et al. *Multiagent reinforcement learning: theoretical framework and an algorithm.* ICML 1998.
- **[Busoniu et al., 2008]** Lucian Busoniu, Robert Babuska, Bart De Schutter. *A comprehensive survey of multiagent reinforcement learning.* IEEE Trans. Syst., Man, Cybern. Syst. 2008.
- **[Sunehag et al., 2018]** Peter Sunehag, Guy Lever, et al. *Value-decomposition networks for cooperative multi-agent learning based on team reward.* AAMAS 2018.
- **[Rashid et al., 2020]** Tabish Rashid, Gregory Farquhar, Bei Peng, Shimon Whiteson. *Weighted QMIX: Expanding monotonic value function factorisation for deep multi-agent reinforcement learning.* NeurIPS 2020.
- **[Su et al., 2021]** Jianyu Su, Stephen Adams, Peter Beling. *Value-decomposition multi-agent actor-critics.* AAAI 2021.
- **[Foerster & Farquhar, 2018]** Jakob Foerster, Gregory Farquhar. *Counterfactual multi-agent policy gradients.* AAAI 2018.
- **[Zhou et al., 2020]** Meng Zhou, Ziyu Liu, Pengwei Sui, Yixuan Li, Yuk Ying Chung. *Learning implicit credit assignment for cooperative multi-agent reinforcement learning.* NeurIPS 2020.
- **[Lowe et al., 2017]** Ryan Lowe, Yi Wu, Aviv Tamar, Jean Harb, Pieter Abbeel, Igor Mordatch. *Multi-agent actor-critic for mixed cooperative-competitive environments.* NeurIPS 2017.
- **[Iqbal & Sha, 2019]** Shariq Iqbal, Fei Sha. *Actor-attention-critic for multi-agent reinforcement learning.* ICML 2019.
- **[Qu et al., 2020]** Guannan Qu, Yiheng Lin, Adam Wierman, Na Li. *Scalable multi-agent reinforcement learning for networked systems with average reward.* NeurIPS 2020.
- **[Jin et al., 2021]** Chi Jin, Qinghua Liu, Yuanhao Wang, Tiancheng Yu. *V-learning – a simple, efficient, decentralized algorithm for multiagent RL.* arXiv 2021.
- **[Muniraj et al., 2018]** Devaprakash Muniraj, Kyriakos G. Vamvoudakis, Mazen Farhood. *Enforcing signal temporal logic specifications in multi-agent adversarial environments: A deep Q-learning approach.* IEEE CDC 2018.
- **[Phan et al., 2020]** Thomy Phan, Thomas Gabor, Andreas Sedlmeier, Fabian Ritz, et al. *Learning and testing resilience in cooperative multi-agent systems.* AAMAS 2020.
- **[Morimoto & Doya, 2005]** Jun Morimoto, Kenji Doya. *Robust reinforcement learning.* Neural Computation 2005.
- **[Chen & Bowling, 2012]** Katherine Chen, Michael Bowling. *Tractable objectives for robust policy optimization.* NeurIPS 2012.
- **[Zhang et al., 2020b]** Kaiqing Zhang, Tao Sun, Yunzhe Tao, Sahika Genc, Sunil Mallya, Tamer Basar. *Robust multi-agent reinforcement learning with model uncertainty.* NeurIPS 2020.
- **[Sinha et al., 2020]** Aman Sinha, Matthew O’Kelly, et al. *FormulaZero: Distributionally robust online adaptation via offline population synthesis.* ICML 2020.
- **[Hu et al., 2020]** Yizheng Hu, Kun Shao, Dong Li, Jianye Hao, Wulong Liu, Yaodong Yang, Jun Wang, Zhanxing Zhu. *Robust multi-agent reinforcement learning driven by correlated equilibrium.* 2020.
- **[Yu et al., 2021]** Jing Yu, Clement Gehring, Florian Schäfer, Animashree Anandkumar. *Robust reinforcement learning: A constrained game-theoretic approach.* Learning for Dynamics and Control (L4DC) 2021.
- **[Wang et al., 2023]** Kaixin Wang, Uri Gadot, Navdeep Kumar, Kfir Levy, Shie Mannor. *Robust reinforcement learning via adversarial kernel approximation.* arXiv 2023.
- **[Shen & How, 2021]** Macheng Shen, Jonathan P. How. *Robust opponent modeling via adversarial ensemble reinforcement learning.* ICAPS 2021.
- **[Li et al., 2019]** Shihui Li, Yi Wu, Xinyue Cui, Honghua Dong, Fei Fang, Stuart Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[van der Heiden et al., 2020]** Tessa van der Heiden, C. Salge, Efstratios Gavves, H. van Hoof. *Robust multi-agent reinforcement learning with social empowerment for coordination and communication.* arXiv 2020.
- **[Sun et al., 2021]** Chuangchuang Sun, Dong-Ki Kim, Jonathan P. How. *Romax: Certifiably robust deep multiagent reinforcement learning via convex relaxation.* arXiv 2021.
- **[Sun et al., 2022]** Yanchao Sun, Ruijie Zheng, Parisa Hassanzadeh, Yongyuan Liang, Soheil Feizi, Sumitra Ganesh, Furong Huang. *Certifiably robust policy learning against adversarial communication in multi-agent systems.* ICLR 2022.
- **[Mandlekar et al., 2017]** Ajay Mandlekar, Yuke Zhu, Animesh Garg, Li Fei-Fei, Silvio Savarese. *Adversarially robust policy learning: Active construction of physically-plausible perturbations.* IROS 2017.
- **[Pinto et al., 2017]** Lerrel Pinto, James Davidson, Rahul Sukthankar. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Pattanaik et al., 2018]** Anay Pattanaik, Zhenyi Tang, Shuijing Liu, Gautham Bommannan, Girish Chowdhary. *Robust deep reinforcement learning with adversarial attacks.* AAMAS 2018.
- **[Zhang et al., 2020a]** Huan Zhang, Hongge Chen, Chaowei Xiao, Bo Li, Mingyan Liu, Duane Boning, Cho-Jui Hsieh. *Robust deep reinforcement learning against adversarial perturbations on state observations.* NeurIPS 2020.
- **[Zhang et al., 2021]** Huan Zhang, Hongge Chen, Duane Boning, Cho-Jui Hsieh. *Robust reinforcement learning on state observations with learned optimal adversary.* arXiv 2021.
- **[Liang et al., 2022]** Yongyuan Liang, Yanchao Sun, Ruijie Zheng, Furong Huang. *Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning.* NeurIPS 2022.
- **[Lin et al., 2020a]** Jieyu Lin, Kristina Dzeparoska, Sai Qian Zhang, Alberto Leon-Garcia, Nicolas Papernot. *On the robustness of cooperative multi-agent reinforcement learning.* IEEE Security and Privacy Workshops (SPW) 2020.
- **[He et al., 2023]** Sihong He, Songyang Han, Sanbao Su, Shuo Han, Shaofeng Zou, Fei Miao. *Robust multi-agent reinforcement learning with state uncertainty.* TMLR 2023.
- **[Hüttenrauch & Šošić, 2017]** Maximilian Hüttenrauch, Adrian Šošić. *Guided deep reinforcement learning for swarm systems.* arXiv 2017.
- **[Pretorius et al., 2020]** Arnu Pretorius, Scott Cameron, et al. *A game-theoretic analysis of networked system control for common-pool resource management using multi-agent reinforcement learning.* NeurIPS 2020.
- **[Behzadan & Munir, 2017]** Vahid Behzadan, Arslan Munir. *Vulnerability of deep reinforcement learning to policy induction attacks.* MLDM, Springer 2017.
- **[Pattanaik & Tang, 2017]** Anay Pattanaik, Zhenyi Tang. *Robust deep reinforcement learning with adversarial attacks.* AAMAS 2017.
- **[Huang et al., 2017]** Sandy Huang, Nicolas Papernot, Ian Goodfellow, Yan Duan, Pieter Abbeel. *Adversarial attacks on neural network policies.* ICLR 2017.
- **[Lin et al., 2017]** Yen-Chen Lin, Zhang-Wei Hong, Yuan-Hong Liao, Meng-Li Shih, Ming-Yu Liu, Min Sun. *Tactics of adversarial attack on deep reinforcement learning agents.* IJCAI 2017.
- **[Xiao et al., 2019]** Chaowei Xiao, Xinlei Pan, et al. *Characterizing attacks on deep reinforcement learning.* arXiv 2019.
- **[Oliehoek et al., 2016]** Frans A. Oliehoek, Christopher Amato, et al. *A concise introduction to decentralized POMDPs.* Springer 2016.
- **[Lerer et al., 2020]** Adam Lerer, Hengyuan Hu, Jakob Foerster, Noam Brown. *Improving policies via search in cooperative partially observable games.* AAAI 2020.
- **[Kos & Song, 2017]** Jernej Kos, Dawn Song. *Delving into adversarial attacks on deep policies.* ICLR 2017.
