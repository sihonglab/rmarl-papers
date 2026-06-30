# 86. Robust Multi-Agent Bandits Over Undirected Graphs

## Metadata
- **Title**: Robust Multi-Agent Bandits Over Undirected Graphs
- **Authors**: Daniel Vial, Sanjay Shakkottai, R. Srikant
- **Affiliation**: University of Texas at Austin (Vial, Shakkottai); University of Illinois Urbana-Champaign (Srikant)
- **Venue**: Proc. ACM Meas. Anal. Comput. Syst. (SIGMETRICS) 2022, Vol. 6, No. 3, Article 53
- **Link/arXiv**: arXiv:2203.00076v2 [cs.LG]; https://doi.org/10.1145/3570614

## Taxonomy
- **Robustness / perturbation type targeted**: Malicious / adversarial agents in a multi-agent network (Byzantine-style attackers that recommend arbitrary arms / "review spam" or failed servers); robustness over general undirected communication graphs.
- **Method paradigm**: Multi-agent multi-armed bandits; gossip-based cooperative learning; UCB exploration; refined blocking rule (suspect-and-block defense); coupling to a noisy rumor process; regret analysis.
- **Keywords**: multi-armed bandits, malicious agents, undirected graphs, blocking, gossip, regret bounds

## TL;DR
The paper shows that the state-of-the-art robust multi-agent bandit blocking algorithm, which works on the complete graph, can incur nearly-linear regret on simple undirected graphs (e.g., the line) until time is doubly exponential in K and n, and proposes a refined blocking rule that achieves O((d_mal(i) + K/n) log(T)/Δ) regret on any connected undirected graph, proving the effect of malicious agents is entirely local (only directly-connected malicious neighbors matter long-term).

## Problem & Motivation
In multi-agent multi-armed bandits, n honest agents collaborate over a network (e.g., e-commerce servers or social-recommendation users) to minimize regret by exchanging arm recommendations, while m malicious agents can disrupt learning by recommending arbitrary arms (modeling review spam or failed servers). Prior work [56] solved this on the complete graph via a "blocking" rule that suspends communication with neighbors whose recommendations perform poorly, achieving O((m + K/n) log(T)/Δ) regret. However, this analysis relies heavily on the complete-graph assumption: the agent i* holding the best arm in its sticky set must be directly connected to every other honest agent. Generalizing beyond the complete graph is nontrivial because blocking causes honest agents to accidentally block each other (edges in the honest subgraph temporarily fail), so it is unclear whether the best arm still spreads via gossip — analytically this couples the randomness of communication and bandit algorithms over a dynamic graph.

## Robustness Setting
- **Threat model / uncertainty set**: An undirected graph G = ([n+m], E) where [n] are honest agents executing the algorithm and the remaining m are malicious agents who recommend arbitrary (worst-case) arms. The honest agent subgraph G_hon is assumed connected (Assumption 1), generalizing the complete-graph case of [56]. Malicious recommendations can depend on observed information (e.g., the "smart"/omniscient strategy recommends the least-played inactive suboptimal arm). d_mal(i) is the number of i's malicious neighbors.
- **Setting**: cooperative (among honest agents) with adversarial agents; decentralized peer-to-peer communication (o(T) pairwise, bit-limited recommendations); online stochastic bandit.

## Method
- Each honest agent runs phase-based UCB over an active set comprising a fixed "sticky set" plus two dynamically-updated non-sticky arms; at the end of each phase agents exchange best-arm recommendations with a random non-blocked neighbor (Algorithm 1, from [18, 56]).
- The existing blocking rule (Algorithm 3, from [56]) blocks a neighbor if its recommended arm is not the most-played arm in the following phase. The paper proves this fails on a "bad instance" (a line of honest agents sharing one malicious neighbor), where it spreads the best arm doubly-exponentially slowly.
- Proposed refined blocking rule (Algorithm 4): agent i blocks neighbor i' for recommending arm k only if (1) k performs poorly (UCB plays it fewer than κ_j times by end of phase j) AND (2) i has not changed its own best arm estimate recently (since phase θ_j). The second criterion — a confidence check that prevents blocking before the agent's own best-arm estimate has settled — is the main new algorithmic insight, directly motivated by the negative result.
- Analytically, the key contribution is showing honest agents eventually stop blocking each other, after which the arm-spreading process is coupled to (lower-bounded by) a tractable "noisy rumor process" (Definition 1) over the static honest subgraph that spreads the best arm in polynomial time.

## Theoretical Contributions
- Negative result (Theorem 1): on the bad-instance line graph, Algorithm 1 with the existing rule [56] incurs R^(n)_T = Ω(min{log(T) + exp(exp(n/3)), T/log^7 T}) — nearly linear regret until time doubly exponential in n = K, a doubly-exponential slowdown vs. the exponential slowdown of classical rumor processes.
- Positive result (Theorem 2): under the refined rule and parameter conditions (9), every honest agent i has R^(i)_T = O((d_mal(i) + S) log(T)/Δ) + (T-independent additive term 2E[A_{2τ̄_spr}] + C*), where S = O(K/n), generalizing the complete-graph bound (2) to connected undirected graphs and making the additive term polynomial in all parameters.
- Locality: for d_mal(i) = O(1) the log T term matches (1) up to constants; for d_mal(i) = 0 (Corollary 2) it matches the fully-cooperative bound of [18] including constants — malicious effects do not propagate beyond one-hop neighbors.
- Corollary 1 gives an explicit conductance-based bound for d-regular honest subgraphs; Remark 11 shows it strictly generalizes (and improves the arm-gap dependence over) [56] on the complete graph.

## Experiments
- **Environment/Benchmark**: Synthetic K = 100-armed Bernoulli bandits with n = 25 honest and m = 10 malicious agents over G(n+m, p) random graphs for p ∈ {1, 1/2, 1/4} (resampled until G_hon connected), 100 trials; also real-data arm means derived from the MovieLens dataset (m = 15). Two malicious strategies: "naive" (uniform random suboptimal arm) and "smart" (omniscient: least-played inactive suboptimal arm), plus mixed variants.
- **Baselines**: existing blocking rule [56] (Algorithm 3), no-blocking algorithm [18], and a no-communication single-agent UCB baseline.
- **Evaluation metrics**: per-agent regret averaged across agents Σ_i R^(i)_T / n (mean and standard deviation across trials).

## Key Results
- For the naive strategy, the existing blocking rule [56] eventually becomes worse than the no-blocking baseline [18] as p decreases; for the smart strategy it even becomes worse than the no-communication single-agent baseline — i.e., honest agents would have been better off ignoring the network.
- The proposed refined rule improves as p decreases, outperforms both baselines uniformly across p, and has much lower variance for smaller p; its advantage over the existing rule is most dramatic against the smarter adversary.
- The existing rule is slightly better only at p = 1 (the complete graph), where it spreads the best arm quickly and then blocks more aggressively.
- Real-data (MovieLens) and mixed-strategy experiments are qualitatively consistent; the proposed rule remains superior even for "nicer" malicious strategies.

## Limitations & Future Work
- The bad-instance construction uses specific numerical constants and a deterministic-reward line graph; though generalizable (Remark 4), it is one demonstrative instance.
- Experimental parameters (κ_j, θ_j) differ from the (more conservative) theoretical settings.
- The conclusion explicitly leaves open whether these gossip-despite-blocking insights extend to multi-agent reinforcement learning.

## Relevance to Survey
This paper sits on the "adversarial / malicious agents" and "fault tolerance / Byzantine robustness" line of robust multi-agent learning, instantiated in the multi-agent bandit (rather than full RL/MDP) setting. It contributes the notion that adversarial harm can be made local (confined to one-hop neighbors) on general communication topologies and that defenses tuned for dense graphs can catastrophically fail on sparse ones — themes relevant to communication robustness and network-structured robust MARL. Its explicit open question of extending to MARL marks it as a bridging reference between robust multi-agent bandits and robust MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 1.2, Robust multi-agent bandits on the complete graph]_

"Despite these improved bounds, [18, 49, 52] require all agents to execute the prescribed algorithm, and in particular, to recommend best arm estimates to their neighbors. As pointed out in [56], this may be unrealistic: in Example 2, review spam can be modeled as bad arm recommendations, while in Example 1, servers may fail entirely. Hence, [56] considers a more realistic setting where 𝑛 honest agents recommend best arm estimates but 𝑚 malicious agents recommend arbitrarily. For this setting, the authors propose a robust version of the algorithm from [18] where honest agents block suspected malicious agents."

"As shown in [56], this blocking scheme prevents each malicious agent from recommending more than 𝑂(1) bad arms long-term, which (effectively) results in an 𝑂(𝑚 + 𝐾/𝑛)-armed bandit (𝑂(𝑚) malicious recommendations, plus the 𝑂(𝐾/𝑛)-sized sticky set). Under the assumption that honest and malicious agents are connected by the complete graph, this allows [56] to prove [Equation (2)]. In [56], it is also shown that blocking is necessary: for any 𝑛 ∈ N, if even 𝑚 = 1 malicious agent is present, the algorithm from [18] (which does not use blocking) incurs Ω(𝐾 log(𝑇)/Δ) regret. Thus, one malicious agent negates the improvement over the single-agent baseline."

> _[Section 1.5, Other related work]_

"In addition to the paper [56] discussed above, several others have considered multi-agent bandits where some of the agents are uncooperative. In [6], the honest agents face a non-stochastic (i.e., adversarial) bandit [4] and communicate at every time step, in contrast to the stochastic bandit and limited communication of our work. The authors of [48] consider the objective of best arm identification [2] instead of cumulative regret. Most of their paper involves a different communication model where the agents/clients collaborate via a central server; Section 6 studies a “peer-to-peer” model which is closer to ours but requires additional assumptions on the number of malicious neighbors. A different line of work considers the case where an adversary can corrupt the observed rewards (see, e.g., [11, 12, 25, 26, 29, 33, 40, 41, 44], and the references therein), which is distinct from the role that malicious agents play in our setting."

"For the fully cooperative case, there are several papers with communication models that differ from the aforementioned [18, 49, 52]. For example, agents in [15, 17] broadcast information instead of exchanging pairwise arm recommendations, communication in [34, 36, 47] is more frequent, the number of transmissions in [45] depends on Δ−1 so could be large, and agents in [37] exchange arm mean estimates instead of (bit-limited) arm indices."

"More broadly, other papers have studied fully cooperative variants of different bandit problems. These include minimizing simple instead of cumulative regret (e.g., [28, 54]), minimizing the total regret across agents rather than ensuring all have low regret (e.g., [22, 57]), contextual instead of multi-armed bandits (e.g., [19, 23, 24, 35, 55]), adversarial rather than stochastic bandits (e.g., [7, 16, 31]), and bandits that vary across agents (e.g., [10, 53, 58]). Another long line of work features collision models where rewards are lower if multiple agents simultaneously pull the same arm (e.g., [1, 5, 13, 21, 30, 42, 43, 46, 51]), unlike our model. Along these lines, other reward structures have been studied, such as reward being a function of the agents’ joint action (e.g., [8, 9, 32])."

### Cited references (resolved from the paper's bibliography)
- **[1]** Anandkumar, Michael, Tang, Swami. *Distributed algorithms for learning and cognitive medium access with logarithmic regret.* IEEE Journal on Selected Areas in Communications 2011.
- **[2]** Audibert, Bubeck. *Best Arm Identification in Multi-Armed Bandits.* COLT 2010.
- **[4]** Auer, Cesa-Bianchi, Freund, Schapire. *Gambling in a rigged casino: The adversarial multi-armed bandit problem.* FOCS 1995.
- **[5]** Avner, Mannor. *Concurrent bandits and cognitive radio networks.* ECML-PKDD 2014.
- **[6]** Awerbuch, Kleinberg. *Competitive collaborative learning.* J. Comput. System Sci. 2008.
- **[7]** Bar-On, Mansour. *Individual regret in cooperative nonstochastic multi-armed bandits.* NeurIPS 2019.
- **[8]** Bargiacchi, Verstraeten, Roijers, Nowé, Hasselt. *Learning to coordinate with coordination graphs in repeated single-stage multi-agent decision problems.* ICML 2018.
- **[9]** Bistritz, Bambos. *Cooperative multi-player bandit optimization.* NeurIPS 2020.
- **[10]** Bistritz, Leshem. *Distributed multi-player bandits — a game of thrones approach.* NeurIPS 2018.
- **[11]** Bogunovic, Krause, Scarlett. *Corruption-tolerant Gaussian process bandit optimization.* AISTATS 2020.
- **[12]** Bogunovic, Losalka, Krause, Scarlett. *Stochastic linear bandits robust to adversarial attacks.* AISTATS 2021.
- **[13]** Boursier, Perchet. *SIC-MMAB: Synchronisation Involves Communication in Multiplayer Multi-Armed Bandits.* NeurIPS 2019.
- **[15]** Buccapatnam, Tan, Zhang. *Information sharing in distributed stochastic bandits.* IEEE INFOCOM 2015.
- **[16]** Cesa-Bianchi, Gentile, Mansour, Minora. *Delay and cooperation in non-stochastic bandits.* COLT 2016.
- **[17]** Chakraborty, Chua, Das, Juba. *Coordinated Versus Decentralized Exploration In Multi-Agent Multi-Armed Bandits.* IJCAI 2017.
- **[18]** Chawla, Sankararaman, Ganesh, Shakkottai. *The Gossiping Insert-Eliminate Algorithm for Multi-Agent Bandits.* AISTATS 2020.
- **[19]** Chawla, Sankararaman, Shakkottai. *Multi-agent low-dimensional linear bandits.* IEEE Trans. Automat. Control 2022.
- **[21]** Dakdouk, Féraud, Laroche, Varsier, Maillé. *Collaborative Exploration and Exploitation in massively Multi-Player Bandits.* 2021.
- **[22]** Dubey et al. *Cooperative multi-agent bandits with heavy tails.* ICML 2020.
- **[23]** Dubey et al. *Kernel methods for cooperative multi-agent contextual bandits.* ICML 2020.
- **[24]** Dubey, Pentland. *Differentially-Private Federated Linear Bandits.* NeurIPS 2020.
- **[25]** Garcelon, Roziere, Meunier, Tarbouriech, Teytaud, Lazaric, Pirotta. *Adversarial Attacks on Linear Contextual Bandits.* NeurIPS 2020.
- **[26]** Gupta, Koren, Talwar. *Better Algorithms for Stochastic Bandits with Adversarial Corruptions.* COLT 2019.
- **[28]** Hillel, Karnin, Koren, Lempel, Somekh. *Distributed exploration in multi-armed bandits.* NeurIPS 2013.
- **[29]** Jun, Li, Ma, Zhu. *Adversarial attacks on stochastic bandits.* NeurIPS 2018.
- **[30]** Kalathil, Nayyar, Jain. *Decentralized learning for multiplayer multiarmed bandits.* IEEE Transactions on Information Theory 2014.
- **[31]** Kanade, Liu, Radunovic. *Distributed non-stochastic experts.* NeurIPS 2012.
- **[32]** Kao, Wei, Subramanian. *Decentralized cooperative reinforcement learning with hierarchical information structure.* ALT 2022.
- **[33]** Kapoor, Patel, Kar. *Corruption-tolerant bandit learning.* Machine Learning 2019.
- **[34]** Kolla, Jagannathan, Gopalan. *Collaborative learning of stochastic bandits over a social network.* IEEE/ACM Transactions on Networking 2018.
- **[35]** Korda, Szörényi, Shuai. *Distributed clustering of linear bandits in peer to peer networks.* JMLR Workshop and Conference Proceedings 2016.
- **[36]** Lalitha, Goldsmith. *Bayesian Algorithms for Decentralized Stochastic Bandits.* IEEE Journal on Selected Areas in Information Theory 2021.
- **[37]** Landgren, Srivastava, Leonard. *Distributed cooperative decision-making in multiarmed bandits: Frequentist and Bayesian algorithms.* IEEE CDC 2016.
- **[40]** Liu, Shroff. *Data Poisoning Attacks on Stochastic Bandits.* ICML 2019.
- **[41]** Liu, Li, Li. *Cooperative Stochastic Multi-agent Multi-armed Bandits Robust to Adversarial Corruptions.* arXiv preprint arXiv:2106.04207, 2021.
- **[42]** Liu, Zhao. *Distributed learning in multi-armed bandit with multiple players.* IEEE Transactions on Signal Processing 2010.
- **[43]** Liu, Mania, Jordan. *Competing bandits in matching markets.* AISTATS 2020.
- **[44]** Lykouris, Mirrokni, Paes Leme. *Stochastic bandits robust to adversarial corruptions.* ACM STOC 2018.
- **[45]** Madhushani, Leonard. *When to call your neighbor? strategic communication in cooperative stochastic bandits.* arXiv preprint arXiv:2110.04396, 2021.
- **[46]** Mansour, Slivkins, Wu. *Competing bandits: Learning under competition.* ITCS 2018.
- **[47]** Martínez-Rubio, Kanade, Rebeschini. *Decentralized cooperative stochastic multi-armed bandits.* NeurIPS 2019.
- **[48]** Mitra, Hassani, Pappas. *Exploiting Heterogeneity in Robust Federated Best-Arm Identification.* arXiv preprint arXiv:2109.05700, 2021.
- **[49]** Newton, Ganesh, Reeve. *Asymptotic Optimality for Decentralised Bandits.* Reinforcement Learning in Networks and Queues, Sigmetrics 2021.
- **[51]** Rosenski, Shamir, Szlak. *Multi-player bandits — a musical chairs approach.* ICML 2016.
- **[52]** Sankararaman, Ganesh, Shakkottai. *Social learning in multi agent multi armed bandits.* Proc. ACM on Measurement and Analysis of Computing Systems 2019.
- **[53]** Shahrampour, Rakhlin, Jadbabaie. *Multi-armed bandits in multi-agent networks.* IEEE ICASSP 2017.
- **[54]** Szörényi, Busa-Fekete, Hegedűs, Ormándi, Jelasity, Kégl. *Gossip-based distributed stochastic bandit algorithms.* JMLR Workshop and Conference Proceedings 2013.
- **[55]** Tekin, Van Der Schaar. *Distributed online learning via cooperative contextual bandits.* IEEE Transactions on Signal Processing 2015.
- **[56]** Vial, Shakkottai, Srikant. *Robust multi-agent multi-armed bandits.* MobiHoc 2021.
- **[57]** Wang, Proutiere, Ariu, Jedra, Russo. *Optimal algorithms for multiplayer multi-armed bandits.* AISTATS 2020.
- **[58]** Zhu, Zhu, Liu, Liu. *Federated bandit: A gossiping approach.* ACM SIGMETRICS 2021.
