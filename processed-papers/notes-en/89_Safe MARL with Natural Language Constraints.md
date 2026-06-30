# 89. Safe Multi-agent Reinforcement Learning with Natural Language Constraints

## Metadata
- **Title**: Safe Multi-agent Reinforcement Learning with Natural Language Constraints
- **Authors**: Ziyan Wang, Meng Fang, Tristan Tomilin, Fei Fang, Yali Du
- **Affiliation**: King's College London; University of Liverpool; Eindhoven University of Technology; Carnegie Mellon University
- **Venue**: Not specified (arXiv preprint, arXiv:2405.20018v1 [cs.MA], 30 May 2024)
- **Link/arXiv**: arXiv:2405.20018v1

## Taxonomy
- **Robustness / perturbation type targeted**: Safety constraints expressed in free-form natural language (constrained multi-agent RL); the "robustness" angle is the agents' ability to interpret and adhere to diverse, unseen, context-specific language constraints rather than fixed pre-designed cost functions.
- **Method paradigm**: Safe / constrained MARL, Lagrangian constrained policy optimization, language-model-based cost prediction (LLM summarization + BERT embedding + decoder violation check), contrastive learning (triplet loss), CTDE PPO backbones (MAPPO / HAPPO).
- **Keywords**: Safe MARL, natural language constraints, Language Constrained Markov Game, Lagrangian, language models, cost prediction

## TL;DR
The paper proposes SMALL, a safe MARL method that uses fine-tuned language models to convert free-form natural language constraints into predicted per-agent costs (without ground-truth cost), integrates them into Lagrangian MAPPO/HAPPO, and introduces the LaMaSafe benchmark, achieving comparable rewards with significantly fewer constraint violations.

## Problem & Motivation
Safe MARL has large potential in robotics, autonomous vehicles, and other domains, but current approaches require constraints to be specified as pre-designed mathematical cost functions or fixed barrier/shielding functions, demanding heavy domain and RL expertise and lacking flexibility for diverse, evolving constraints. Natural language is an intuitive, accessible medium for both experts and end-users (e.g., interacting with household robots), yet existing safe MARL methods cannot adapt to the nuances of human language constraints: language constraints are hard to map into numerical cost functions, and the difficulty is magnified in multi-agent settings where agents must understand instructions individually while still cooperating. The paper aims to make safe MARL more accessible by letting users specify safety requirements directly in natural language.

## Robustness Setting
- **Threat model / uncertainty set**: Constraints are given as free-form natural language `l` whose corresponding ground-truth cost function `Cl` is unknown to the agents. The method must infer constraint violations purely from text (instructions plus textual environment observations) and generalize to language constraints never encountered during training, including abstract/metaphorical phrasings.
- **Setting**: Fully-cooperative multi-agent (Language Constrained Markov Game); centralized training with decentralized execution (CTDE, via MAPPO/HAPPO); online policy learning. No ground-truth cost is required for training or evaluation.

## Method
- **Language Constrained Markov Game**: Augments the Constrained Markov Game tuple with a constraint transformation function `Pc : L → Cl` and a natural language constraint space `L`; agents know only the language constraint `l`, not the ground-truth cost `Cl(st, at)`. A language constraint is sampled at the start of each episode and reused throughout.
- **Cost Learning Module**: (1) An LLM (e.g., GPT-3.5) summarizes/disambiguates the verbose constraint `l` into a concise `lc`; (2) a BERT-based encoder, fine-tuned with contrastive learning using a triplet loss `Ltri` (cosine-similarity distance, margin α), converts `lc` into a constraint embedding `El` and encodes textual observations into observation embeddings `Eo,t`; (3) the predicted cost combines cosine similarity `dist(El, Ei_o,t)` with a binary violation flag `vi_t ∈ {0,1}` obtained by querying a decoder LLM (e.g., Llama3-8B) with the observation and constraint: `ĉi_t = vi_t · dist(El, Ei_o,t)`.
- **Multi-Agent Policy Learning**: Integrates the predicted costs into MAPPO and HAPPO with a Lagrange multiplier: `π = arg max_π Jr(π) − λ Jc(π)`, where `Jc` is the expected sum of predicted costs over all agents. Value and cost-value functions are trained via mean-squared TD-error; the PPO-clip objective updates the policy. This yields SMALL-MAPPO and SMALL-HAPPO.
- **Descriptor**: Automatically filters raw text observations to retain only the most pertinent entity/obstacle information, aligning observations with the constraint embedding for more accurate cost prediction.

## Theoretical Contributions
None / mostly empirical. The paper formalizes the Language Constrained Markov Game and the constrained optimization objective but provides no convergence, sample-complexity, or equilibrium guarantees.

## Experiments
- **Environment/Benchmark**: LaMaSafe (the paper's new benchmark), comprising LaMaSafe-Grid (2D discrete navigation based on Mini-Grid, with lava/water/grass hazards and inter-agent collisions; Random and One-Path layouts) and LaMaSafe-Goal (3D continuous control based on Gymnasium / Safety-Gymnasium-style robots: Point, Car, Ant; hazards, vases, collisions; Easy/Medium/Hard layouts with 2 and 4 agents).
- **Baselines**: MAPPO; HAPPO; MAPPO-Lagrange; HAPPO-Lagrange (the latter two use a pre-defined ground-truth cost function and are treated as oracles in one comparison).
- **Evaluation metrics**: Average reward (over three random seeds) under the condition of following the natural language constraints, and cost (number of constraint violations / contacts with hazards); ablations report reward and cost in LaMaSafe-Goal(Ant) Easy.

## Key Results
- SMALL-MAPPO and SMALL-HAPPO achieve rewards slightly below their backbone algorithms but maintain a similar performance level and excel in more challenging scenarios (e.g., Ant Medium and Hard layouts).
- On cost, SMALL-based algorithms converge to extremely low cost in almost all environments, whereas MAPPO and HAPPO incur high costs because they cannot handle the language constraints; SMALL generalizes to natural language descriptions never seen before.
- Scalability: extending LaMaSafe-Goal(Ant) to 4 agents, SMALL keeps rewards slightly below baseline while substantially reducing violations. Compared with ground-truth-cost oracles (MAPPO/HAPPO-Lagrange), SMALL converges similarly and occasionally outperforms.
- Ablations (SMALL-HAPPO, 2-agent Easy): removing fine-tuning, the decoder, the descriptor, or the violation flag `vi_t` all degrade performance; e.g., w/o `vi_t` yields very low cost (4.78) but much lower reward (5.12), while full SMALL-HAPPO attains reward 11.62 / cost 5.82.

## Limitations & Future Work
- Scalability to larger multi-agent systems with more agents and more complex constraints is left to future work.
- Handling ambiguous or conflicting constraints is not yet addressed and is noted as a future direction to enhance robustness.
- The cost-prediction module may misjudge certain high-risk but potentially beneficial actions (e.g., navigating close to hazardous zones) as acceptable, which can encourage rule-breaking "bold" strategies.

## Relevance to Survey
This paper extends safe / constrained MARL toward a language-driven specification of safety, situating it on the "safety constraints" line of the robust MARL landscape. Its robustness contribution is generalization to diverse, unseen, free-form natural language constraints (rather than to environment/model perturbations or adversarial agents), connecting safe MARL with language-model-based instruction following. It also contributes a benchmark (LaMaSafe) and a Lagrangian constrained-optimization method built on standard CTDE PPO backbones (MAPPO/HAPPO), useful as a reference for the intersection of LLMs, safety, and cooperative MARL.

## Related Work (verbatim excerpts from the paper)
> _[Section 2, Related Work — Safe Multi-Agent Reinforcement Learning]_

"Safe Multi-Agent Reinforcement Learning: Despite the significant attention given to safe MARL in recent years, many safety-related challenges remain unresolved [10], such as dealing with natural language constraints. Several approaches have been proposed to address the safety problem by using fixed pre-design cost functions. The safe model-free MARL algorithms MACPO and MAPPO-Lagrange [9], which are the safe extensions of HATRPO [14] and MAPPO [31] respectively. However, these methods are not guaranteed to work under free-form language constraints and are unable to deal with multiple constraints simultaneously. Other research directions include approaches based on the shielding and barrier functions [8, 3], but these methods require pre-training or strong prior knowledge to create barriers that filter actions and cannot generalize to new scenarios, and these barrier functions will change if constraints change."

> _[Section 2, Related Work — Constraints with Natural Language]_

"Constraints with Natural Language: Previous works used natural language to constrain agents to behave safely under a single agent setting. Prakash et al. [20] trained a constraint checker in a supervised fashion to predict whether the natural language constraints are violated and guide RL agents to learn safe policies. During training, a ground-truth cost for each constraint was required to train the constraint checker. However, this approach may not be feasible if the constraint or language structure changes during the application. Yang et al. [30] trained a constraint interpreter to predict which entities in the environment may be relevant to the constraint and used the interpreter to predict costs. Their approach did not rely on a ground-truth cost, but the interpreter had to model and predict all entities in the environment. This necessitated a constraint in a similar structure, which could result in inaccurate outcomes in complex tasks since the cost prediction model cannot handle free-form language. Our method, in contrast, utilizes Language Models to predict constraint violations, eliminating the need for ground-truth costs and extra training modules."

> _[Section 2, Related Work — Language Models]_

"Language Models: In recent years, LMs based on utilizing Transformers [28] have attracted great attention. For example, Bidirectional Encoder Representations from Transformers (BERT) [6] focuses on extracting semantic meaning and learning representations for text inputs by joint conditioning on their context, which can be easily fine-tuned for downstream tasks. Models such as the GPT [2] and Llama [26] have been developed to generate text by incorporating extensive prior knowledge with an emphasis on the decoder aspect. These models are trained to create text based on the preceding context and have shown proficiency in text-generation tasks. As Language Models provide the potential to align human language with policy learning and decision-making domains, previous research has attempted to introduce Language Models into MARL [4]. However, to the best of our knowledge, our work is the first to apply the fine-tuned LMs to the field of Safe MARL specifically to tackle natural language constraint challenges."

> _[Introduction — on limitations of current safe MARL]_

"A surge in interest in safe MARL has led to the rise of learning algorithms that optimize agents' policies for maximum efficacy while adhering to human-imposed constraints. However, current safe MARL approaches rather only consider a fixed format barrier or factored shielding function generated by the prior knowledge [3, 8] or only consider the settling pre-designed cost function [16, 9, 17]."

### Cited references (resolved from the paper's bibliography)
- **[2]** T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, et al. *Language models are few-shot learners.* NeurIPS 2020.
- **[3]** Z. Cai, H. Cao, W. Lu, L. Zhang, H. Xiong. *Safe multi-agent reinforcement learning through decentralized multiple control barrier functions.* arXiv preprint arXiv:2103.12553, 2021.
- **[4]** W. Chen, Y. Su, J. Zuo, C. Yang, C. Yuan, C. Qian, et al. *Agentverse: Facilitating multi-agent collaboration and exploring emergent behaviors in agents.* arXiv preprint arXiv:2308.10848, 2023.
- **[6]** J. Devlin, M.-W. Chang, K. Lee, K. Toutanova. *BERT: Pre-training of deep bidirectional transformers for language understanding.* arXiv preprint arXiv:1810.04805, 2018.
- **[8]** I. ElSayed-Aly, S. Bharadwaj, C. Amato, R. Ehlers, U. Topcu, L. Feng. *Safe multi-agent reinforcement learning via shielding.* arXiv preprint arXiv:2101.11196, 2021.
- **[9]** S. Gu, J. G. Kuba, M. Wen, R. Chen, Z. Wang, Z. Tian, J. Wang, A. Knoll, Y. Yang. *Multi-agent constrained policy optimisation.* arXiv preprint arXiv:2110.02793, 2021.
- **[10]** S. Gu, L. Yang, Y. Du, G. Chen, F. Walter, J. Wang, Y. Yang, A. Knoll. *A review of safe reinforcement learning: Methods, theory and applications.* arXiv preprint arXiv:2205.10330, 2022.
- **[14]** J. G. Kuba, R. Chen, M. Wen, Y. Wen, F. Sun, J. Wang, Y. Yang. *Trust region policy optimisation in multi-agent reinforcement learning (HATRPO/HAPPO).* arXiv preprint arXiv:2109.11251, 2021.
- **[16]** C. Liu, N. Geng, V. Aggarwal, T. Lan, Y. Yang, M. Xu. *CMIX: Deep multi-agent reinforcement learning with peak and average constraints.* ECML PKDD 2021.
- **[17]** S. Lu, K. Zhang, T. Chen, T. Başar, L. Horesh. *Decentralized policy gradient descent ascent for safe multi-agent reinforcement learning.* AAAI 2021.
- **[20]** B. Prakash, N. Waytowich, A. Ganesan, T. Oates, T. Mohsenin. *Guiding safe reinforcement learning policies using structured language constraints.* UMBC Student Collection, 2020.
- **[26]** H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozière, et al. *Llama: Open and efficient foundation language models.* arXiv preprint arXiv:2302.13971, 2023.
- **[28]** A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, I. Polosukhin. *Attention is all you need.* NeurIPS 2017.
- **[30]** T.-Y. Yang, M. Y. Hu, Y. Chow, P. J. Ramadge, K. Narasimhan. *Safe reinforcement learning with natural language constraints.* NeurIPS 2021.
- **[31]** C. Yu, A. Velu, E. Vinitsky, J. Gao, Y. Wang, A. Bayen, Y. Wu. *The surprising effectiveness of PPO in cooperative multi-agent games (MAPPO).* NeurIPS 2022.
