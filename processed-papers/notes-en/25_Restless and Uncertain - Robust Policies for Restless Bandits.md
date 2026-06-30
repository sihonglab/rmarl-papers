# 25. Restless and Uncertain: Robust Policies for Restless Bandits via Deep Multi-Agent Reinforcement Learning

## Metadata
- **Title**: Restless and Uncertain: Robust Policies for Restless Bandits via Deep Multi-Agent Reinforcement Learning
- **Authors**: Jackson A. Killian, Lily Xu, Arpita Biswas, Milind Tambe
- **Affiliation**: Computer Science, Harvard University; Center for Research on Computation and Society, Harvard University
- **Venue**: UAI 2022 (Proceedings of the 38th Conference on Uncertainty in Artificial Intelligence, PMLR 180:990–1000)
- **Link/arXiv**: Code: https://github.com/killian-34/RobustRMAB

## Taxonomy
- **Robustness / perturbation type targeted**: Environment/model uncertainty (interval uncertainty over the transition dynamics / arm parameters of restless multi-armed bandits); planning under uncertain estimated dynamics.
- **Method paradigm**: Minimax regret robust planning, double oracle (agent oracle + nature oracle), two-player zero-sum regret game, deep RL (DDLPO), multi-agent RL with centralized critic (MA-DDLPO), Lagrangian relaxation, PPO.
- **Keywords**: Restless multi-armed bandits (RMAB), minimax regret, double oracle, robust planning, multi-agent RL, Lagrangian relaxation

## TL;DR
The paper introduces Robust RMABs (RMABs with interval uncertainty over arm dynamics) and computes minimax regret–robust policies via a double oracle framework, where a novel deep-RL agent oracle (DDLPO, using a learned λ-network to tame combinatorial complexity) and a multi-agent-RL nature oracle (MA-DDLPO, casting regret maximization as a game between a policy optimizer and adversarial nature with a shared/centralized critic) are combined into the RR-DPO algorithm with convergence guarantees.

## Problem & Motivation
Restless multi-armed bandits (RMABs) model constrained resource allocation among N independent stochastic processes (arms) and are used in scheduling, machine replacement, vehicle routing, anti-poaching patrols, and healthcare. Nearly all RMAB techniques assume the stochastic dynamics are precisely known, which is impossible in many real-world problems (e.g., a patient's adherence probability or the probability of finding a poacher's snare). Online methods that learn without prior knowledge require tens of thousands of samples, prohibitive for finite-length settings (e.g., tuberculosis treatment with only a few dozen rounds). Real-world planners must instead use noisy estimates from historical data or experts, which induces significant uncertainty; the paper shows that ignoring this uncertainty can lead to arbitrarily bad policies. Robust RMABs add a combinatorial layer of complexity onto an already PSPACE-hard problem, motivating new techniques.

## Robustness Setting
- **Threat model / uncertainty set**: The exact transition probabilities are unknown; each arm n's transition dynamics Tn are governed by parameters ωn within a given interval uncertainty ωn := [ωn, ωn] (a continuous, closed set). Nature (adversary) selects a parameter setting ω within these intervals to maximize the agent's regret. The objective is the minimax regret policy π† = min_π max_ω L(π, ω), where regret L(π, ω) = G(π⋆_ω, ω) − G(π, ω) compares the policy against the optimal reward-maximizing policy under ω.
- **Setting**: Cooperative resource-allocation planning cast as a two-player zero-sum (regret) game between agent and adversarial nature; planning/offline robust planning solved with deep RL oracles; the nature oracle itself is formulated as a multi-agent RL problem (player A policy optimizer + player B adversarial nature) with centralized critics.

## Method
- **Double oracle (DO) framework (RR-DPO)**: Casts robust planning as a zero-sum game between an agent (minimizes regret by choosing RMAB policies π) and nature (maximizes regret by choosing environment parameters ω). Each iteration computes a mixed-strategy Nash equilibrium over current pure-strategy sets, then each oracle learns a best response to add to its set (adapted from the MIRROR framework).
- **Agent oracle — DDLPO**: A novel deep-RL algorithm that solves the multi-action RMAB via Lagrangian relaxation, which decouples the per-arm value functions except for a shared λ. It learns N independent per-arm policy/critic networks (with λ augmented into the state) plus an auxiliary "λ-network" Λ(s) trained by a derived dual gradient update rule (Proposition 1), greatly reducing sample complexity over the exponential full-combinatorial problem. Trained with PPO; the budget is not imposed at training time but enforced at test time (GreedyProba, QKnapsack, or Whittle binary search in Alg. 2).
- **Nature oracle — MA-DDLPO**: Casts the non-stationary regret-maximizing nature oracle as a MARL problem with two players: an auxiliary player A that learns the optimal policy π⋆_ω needed to compute the first regret term, and an adversarial player B (a single continuous-action policy network) that selects worst-case parameters ω to minimize G(π̃, ω). Non-stationarity is mitigated via centralized critics (from multi-agent PPO) that take the other player's actions as input; player B's regret reward is estimated via Monte Carlo rollouts of the fixed agent mixed strategy.
- **Generality**: DDLPO is the first deep-RL procedure for multi-action RMABs, extends to weakly-coupled MDPs and continuous-action RMABs (previously unstudied), and does not require indexability or special problem structure.

## Theoretical Contributions
- **Proposition 1**: Gradient update rule for the λ-network that minimizes the Lagrangian objective (Eq. 4) for a given state s.
- **Proposition 2**: Given arm policies corresponding to optimal Q-functions, the λ-network update converges to the optimal Λ⋆ as training epochs and sample count K → ∞.
- **Proposition 3**: In the binary-action setting, assuming each oracle returns true best responses and finite pure strategy sets, RR-DPO converges in a finite number of steps to the minimax regret–optimal policy.
- **Proposition 4**: In the Robust RMAB problem with interval uncertainty, the max regret of a reward-maximizing policy can be arbitrarily large compared to a minimax regret–optimal policy.
- (Proofs in Appendix A.)

## Experiments
- **Environment/Benchmark**: Three domains — (1) Synthetic (handcrafted binary-action domain with three arm types {U, V, W}, illustrating Prop. 4); (2) ARMMAN (real-world maternal-healthcare intervention modeled as a binary-action RMAB with three states: Self-motivated, Persuadable, Lost Cause; uncertainty intervals of 0.5 around transition parameters, 6 uncertain parameters per arm); (3) SIS Epidemic Model (discrete-state, large-state, multi-action domain where arms are geographic regions, with actions {a0, a1, a2} for no-action / physical distancing / face masks).
- **Baselines**: For robust setting (RR-DPO): three reward-maximizing Hawkins variants — pessimistic (HP), mean (HM), optimistic (HO); RLvMid (DDLPO with mean parameters); Rand (random budget-filling). For DDLPO (agent oracle / reward-maximizing setting): No Action, Random, and the Hawkins Lagrange policy.
- **Evaluation metrics**: Maximum policy regret (regret/N, lower is better) for the robust setting; returns (reward/N, higher is better) for the reward-maximizing setting; runtime/query-time scaling vs. population size. Averaged over 50 random seeds (regret evaluations over 25 simulations, horizon 10); DO runs 6 epochs with 100 rollout steps and 100 training epochs per oracle.

## Key Results
- RR-DPO incurs the lowest regret, beating all baselines across all three domains; on Synthetic it reduces regret by ~50% across various N and B, and on ARMMAN it achieves regret around 50% lower than the best baselines.
- On SIS, results are robust across parameter settings even as the state space grows from S = 100 to 500, where the Hawkins baseline becomes prohibitively expensive.
- DDLPO (agent oracle) achieves reward comparable to the exact Hawkins algorithm and significantly better than random, while scaling far better computationally — a single Hawkins rollout (10 rounds) takes ~100 seconds at 500 states (scaling quadratically), making it prohibitive inside the RR-DPO loop.
- Sensitivity analyses: as horizon H varies 10→100, RR-DPO maintains very low regret (relative improvement up to ~60%) while competitor regret roughly doubles; RR-DPO dominates across uncertainty-interval widths (0.25×, 0.5×, 1.0×).

## Limitations & Future Work
- The finite-step convergence guarantee (Proposition 3) is established for the binary-action setting under true best responses and finite pure strategy sets (the continuous nature-oracle case is handled empirically / via discretization).
- The nature oracle is a hard, generally non-convex, non-stationary optimization requiring Monte Carlo rollout estimates of regret.
- Future work (implied): broader deployment of RMABs for real-world impact; the MARL nature-oracle formulation is presented as of potential general interest for robust planning beyond RMABs.

## Relevance to Survey
This paper sits on the "environment/model uncertainty" main line of robust (MA)RL but adopts a minimax regret criterion rather than the more common maximin/worst-case reward, explicitly arguing that maximin reward yields overly conservative policies. It connects the robust-adversarial-RL and robust-MARL literature (Pinto et al. 2017; Lanctot et al. 2017; Li et al. 2019) to the structured restless-bandit / weakly-coupled-MDP setting, and contributes a MARL-with-centralized-critic formulation of an adversarial "nature" oracle — relevant to the survey's themes of adversarial training, nature-player modeling, and game-theoretic (double oracle / Nash equilibrium) approaches to robustness.

## Related Work (verbatim excerpts from the paper)

> _[Section 2, Related Work — "Robust planning" subsection]_

"Work on robust planning in RL mainly focuses on maximin reward via robust adversarial RL [Pinto et al., 2017] or multi-agent RL (MARL) [Lanctot et al., 2017, Li et al., 2019], but maximin reward leads to overly conservative policies [Nguyen et al., 2014]. The minimax regret criterion [Braziunas and Boutilier, 2007] avoids this pitfall, but this objective is challenging with very large or continuous strategy spaces. This can be addressed with the DO approach proposed by McMahan et al. [2003] which explores a small subset of strategies while still guaranteeing optimal convergence [Gilbert and Spanjaard, 2017]. Subsequently, DO has been extended to optimize MARL problems with multiple selfish agents [Lanctot et al., 2017]. Recently, Xu et al. [2021] used DO to solve a single Markov decision process (MDP) minimax-regret planning problem and used RL to implement the oracles. However, when applied to RMABs, the number of outputs in their policy network grows exponentially, as does the size of the state space being learned, both of which require prohibitively long training times beyond trivially sized RMABs. Accordingly, we found that their RL algorithms failed to scale past N = 5 arms and S = 2 states, whereas we show in Sec. 5 that our algorithms solve problems that are orders of magnitude larger. Additionally, their approach is designed only for continuous state/action spaces, whereas our approach can find robust policies for any combination of discrete or continuous state/action spaces. We accomplish this via our novel formulation of the nature oracle as a MARL problem, which decomposes the causes of non-stationarity, i.e., agent and nature, and learn them with separate networks."

> _[Section 2, Related Work — "RMABs" subsection]_

"The reward-maximizing, binary-action RMAB problem was introduced by Whittle [1988]. His widely used Whittle index policy [Mate et al., 2020, Glazebrook et al., 2006, Bagheri and Scaglione, 2015] is asymptotically optimal under indexability [Weber and Weiss, 1990]. Glazebrook et al. [2011] and Hodge and Glazebrook [2015] extended the Whittle index to multi-action RMABs with special monotonic structure, while Killian et al. [2021b] gave a more general Lagrange-based method. Hawkins [2003] studied methods for weakly coupled Markov decision processes (WCMDP), which generalize multi-action RMABs to have multiple constraints, and propose Lagrangian solutions for small problems. Adelman and Mersereau [2008] and Gocgun and Ghate [2012] followed by providing better solutions to WCMDPs but sacrifice scalability. All these works assumed precise knowledge of stochastic dynamics. Some recent works have studied online RMABs with unknown dynamics but all have prohibitively large sample complexity [Gafni and Cohen, 2020, Jung and Tewari, 2019, Biswas et al., 2021, Killian et al., 2021a]. None consider robust planning under environment uncertainty, which we address."

> _[Section 2, Related Work — "RL for RMABs" subsection]_

"A few recent works learn Whittle indices for indexable binary-action RMABs using (i) deep RL (DRL) [Nakhleh et al., 2021] and (ii) tabular Q-learning [Biswas et al., 2021, Fu et al., 2019, Avrachenkov and Borkar, 2022]. Killian et al. [2021a] take tabular Q-learning to the multi-action setting. In contrast, our DRL approach provides a more general solution to binary and multi-action RMAB domains, not requiring indexability or problem structure, and is far more scalable than tabular methods."

### Cited references (resolved from the paper's bibliography)
- **[Pinto et al., 2017]** L. Pinto, J. Davidson, R. Sukthankar, A. Gupta. *Robust adversarial reinforcement learning.* ICML 2017.
- **[Lanctot et al., 2017]** M. Lanctot, V. Zambaldi, A. Gruslys, A. Lazaridou, K. Tuyls, J. Pérolat, et al. *A unified game-theoretic approach to multiagent reinforcement learning.* NeurIPS 2017.
- **[Li et al., 2019]** S. Li, Y. Wu, X. Cui, H. Dong, F. Fang, S. Russell. *Robust multi-agent reinforcement learning via minimax deep deterministic policy gradient.* AAAI 2019.
- **[Nguyen et al., 2014]** T. H. Nguyen, A. Yadav, B. An, M. Tambe, C. Boutilier. *Regret-based optimization and preference elicitation for Stackelberg security games with uncertainty.* AAAI 2014.
- **[Braziunas and Boutilier, 2007]** D. Braziunas, C. Boutilier. *Minimax regret based elicitation of generalized additive utilities.* UAI 2007.
- **[McMahan et al., 2003]** H. B. McMahan, G. J. Gordon, A. Blum. *Planning in the presence of cost functions controlled by an adversary.* ICML 2003.
- **[Gilbert and Spanjaard, 2017]** H. Gilbert, O. Spanjaard. *A double oracle approach to minmax regret optimization problems with interval data.* European Journal of Operational Research 2017.
- **[Xu et al., 2021]** L. Xu, A. Perrault, F. Fang, H. Chen, M. Tambe. *Robust reinforcement learning under minimax regret for green security.* UAI 2021.
- **[Whittle, 1988]** P. Whittle. *Restless bandits: Activity allocation in a changing world.* J. Appl. Probab. 1988.
- **[Mate et al., 2020]** A. Mate, J. A. Killian, H. Xu, A. Perrault, M. Tambe. *Collapsing bandits and their application to public health interventions.* NeurIPS 2020.
- **[Glazebrook et al., 2006]** K. D. Glazebrook, D. Ruiz-Hernandez, C. Kirkbride. *Some indexable families of restless bandit problems.* J. Appl. Probab. 2006.
- **[Bagheri and Scaglione, 2015]** S. Bagheri, A. Scaglione. *The restless multi-armed bandit formulation of the cognitive compressive sensing problem.* IEEE Trans. Signal Process. 2015.
- **[Weber and Weiss, 1990]** R. R. Weber, G. Weiss. *On an index policy for restless bandits.* J. Appl. Probab. 1990.
- **[Glazebrook et al., 2011]** K. D. Glazebrook, D. J. Hodge, C. Kirkbride. *General notions of indexability for queueing control and asset management.* Ann. Appl. Probab. 2011.
- **[Hodge and Glazebrook, 2015]** D. J. Hodge, K. D. Glazebrook. *On the asymptotic optimality of greedy index heuristics for multi-action restless bandits.* Adv. Appl. Probab. 2015.
- **[Killian et al., 2021b]** J. A. Killian, A. Perrault, M. Tambe. *Beyond "To act or not to act": Fast Lagrangian approaches to general multi-action restless bandits.* AAMAS 2021.
- **[Hawkins, 2003]** J. T. Hawkins. *A Lagrangian decomposition approach to weakly coupled dynamic optimization problems and its applications.* PhD thesis, MIT, 2003.
- **[Adelman and Mersereau, 2008]** D. Adelman, A. J. Mersereau. *Relaxations of weakly coupled stochastic dynamic programs.* Operations Research 2008.
- **[Gocgun and Ghate, 2012]** Y. Gocgun, A. Ghate. *Lagrangian relaxation and constraint generation for allocation and advanced scheduling.* Computers & Operations Research 2012.
- **[Gafni and Cohen, 2020]** T. Gafni, K. Cohen. *Learning in restless multi-armed bandits via adaptive arm sequencing rules.* IEEE Trans. Automat. Contr. 2020.
- **[Jung and Tewari, 2019]** Y. H. Jung, A. Tewari. *Regret bounds for Thompson sampling in episodic restless bandit problems.* NeurIPS 2019.
- **[Biswas et al., 2021]** A. Biswas, G. Aggarwal, P. Varakantham, M. Tambe. *Learn to intervene: An adaptive learning policy for restless bandits in application to preventive healthcare.* IJCAI 2021.
- **[Killian et al., 2021a]** J. A. Killian, A. Biswas, S. Shah, M. Tambe. *Q-learning Lagrange policies for multi-action restless bandits.* KDD 2021.
- **[Nakhleh et al., 2021]** K. Nakhleh, S. Ganji, P.-C. Hsieh, I.-H. Hou, S. Shakkottai. *NeurWIN: Neural Whittle index network for restless bandits via deep RL.* NeurIPS 2021.
- **[Fu et al., 2019]** J. Fu, Y. Nazarathy, S. Moka, P. G. Taylor. *Towards Q-learning the Whittle index for restless bandits.* ANZCC (IEEE) 2019.
- **[Avrachenkov and Borkar, 2022]** K. E. Avrachenkov, V. S. Borkar. *Whittle index based Q-learning for restless bandits with average reward.* Automatica 2022.
