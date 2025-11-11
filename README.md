# PERCS-Dataset

## Overview
This repository contains the code for **PERCS**, a dataset of **500 biomedical abstracts** paired with persona-specific summaries designed to make biomedical research more accessible across varying levels of medical literacy.

**PERCS** (Persona-Guided Controllable Summarization) introduces four target personas:
- **Laypersons**
- **Premedical Students**
- **Non-medical Researchers**
- **Medical Experts**

---

#  Dataset Access

The **PERCS dataset**, is publicly available on OSF. 

🔗 [Link](https://osf.io/xxxxx)

This GitHub repository includes only  **prompt templates**, and **benchmarking code** to reproduce experiments described in the paper.

---
## Experimental Benchmarking

We evaluated four large language models (LLMs), including **GPT-4o**, **Mistral-8x7B-Instruct**, **Gemini-2.0 Flash Lite**, and **LLaMA-3 70B**, on the PERCS dataset.

### Experimental Setup
We benchmarked three standard prompting strategies for LLM-based summarization:

- **Zero-shot:** The model receives the persona-specific prompt used to create the dataset and generates a summary without additional examples.  
- **Few-shot:** The same persona-specific prompt is provided along with three in-domain exemplars from the dataset.  
- **Self-refine:** The model first produces a zero-shot summary, then critiques it for persona alignment and faithfulness to the abstract, provides self-feedback, and revises iteratively until satisfied. In this setup, the LLM acts as both feedback provider and evaluator.

Summaries were evaluated on **comprehensiveness**, **readability**, and **faithfulness** using automatic metrics.  
Comprehensiveness was measured using *ROUGE-1*, *ROUGE-2*, *ROUGE-L* and *SARI*; readability using *FKGL*, *DCRS*, *CLI*, and *LENS*; and faithfulness using *SummaC (Conv)*.  

##  API Access

You will need API keys for:

- **OpenAI** (for GPT-4o)  
- **OpenRouter** (for LLaMA-3, Mistral, and Gemini)

Set them as environment variables

---

# Citation

If you use the **PERCS dataset** or **benchmark code** in your research, please cite:


