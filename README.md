# BugattAgent

Exploring self-improvement in LLMs.

My motivation for this project is https://arxiv.org/abs/2410.04444 (Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement), which presents a theoretical framework for a 'true' self-improving machine based off the godel machine, which I find really cool.

In this project, I investigated the extent to which multi-agents can be utilised to perform domain specific tasks, in this case, to simulate a quantitative finance firm, due to my prior knowledge in quantitative finance.

1. Self-improvement in iterations with one LLM. (2/4/2025)
Model chosen is the DeepSeek-R1-Distill-Qwen-14B, quantised 4-bit for memory efficiency. It is prompted to produce one code file and a note file, which gives the model the potential to utilise free space for chain of thought or any reasoning the model performs, hence it can provide plans for itself in the future). The code file and note file of the LLM is self-fed into itself, and modifications are made as a form of improvement.

Before I created a virtual environment for the LLM to run its code, large amounts of hallucinations are observed in the third iteration of the code (This assumes the code written by the LLM runs without bugs in the previous two iterations). This prompted me to shift towards a 'society' of LLMs even before creating the environment to mitigate hallucinations, as introducing a large number of agents allows a large number of observers, evaluators and entities to correct each other. My motivation for this is https://arxiv.org/abs/2411.00114, multi-agents that form a civilization in Minecraft.
