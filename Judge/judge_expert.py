from collections import Counter
import re

def judge_summaries_experts(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    judge_prompt = f"""
You are a biomedical domain expert evaluating summaries of a research abstract. Each summary is intended for expert readers and should be judged on the following criteria:

1. Factual Faithfulness**: All numerical data (e.g., percentages, odds ratios, p-values), study design elements (e.g., sample size, timepoints), biological findings, and terminology **must be directly supported by the abstract**. Fabricated or hallucinated content must be penalized heavily.

2. **Level of Detail for Experts**: The summary should effectively capture all key elements relevant to expert readers, such as specific methods used, immune/bio markers mentioned, types of findings, interpretation of data, and clinical implications.

3. **Clarity and Appropriateness of Tone**: The summary should be technically clear, and use appropriate tone for a scientific expert audience.

4. **Completeness**: The best summary will accurately reflect all important points from the abstract, without omitting key results or context.

---

Review each summary step by step against these criteria — especially checking that every number or result matches the abstract and that no additional or fake statistical values are invented.

After your evaluation, report your reasoning and then state your final judgment in the format: **Summary X**

---

**Abstract:**
{abstract}

---

**Summaries:**
{summaries_text}

---

Your evaluation (step by step) followed by the final choice:
"""

    judge_context = [{"role": "user", "content": judge_prompt}]
    response = judge_agent.generate_answer(judge_context)
    #print(response)
    matches = re.findall(r"\*\*Summary\s+(\d+)\*\*", response)

    if matches:
        final_choice_str = matches[-1]  # use the last match as the final choice
        summary_number = int(final_choice_str) - 1
        if 0 <= summary_number < len(summaries):
            return str(summary_number + 1), summaries[summary_number]
        else:
            return None, "Invalid summary number or out of index range"
    else:
        return None, "No summary number found in the response"
    

def vote_on_summaries_experts(abstract, summaries, agents, tie_breaker):
    results = []

    # Step 1: Each agent votes using expert prompt logic
    for agent in agents:
        summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

        judge_prompt = f"""
You are a biomedical domain expert evaluating summaries of a research abstract. Each summary is intended for expert readers and should be judged on the following criteria:

1. **Factual Faithfulness**: All numerical data (e.g., percentages, odds ratios, p-values), study design elements (e.g., sample size, timepoints), biological findings, and terminology **must be directly supported by the abstract**. Fabricated or hallucinated content must be penalized heavily.

2. **Level of Detail for Experts**: The summary should effectively capture all key elements relevant to expert readers, such as specific methods used, immune/bio markers mentioned, types of findings, interpretation of data, and clinical implications.

3. **Clarity and Appropriateness of Tone**: The summary should be technically clear, and use appropriate tone for a scientific expert audience.

4. **Completeness**: The best summary will accurately reflect all important points from the abstract, without omitting key results or context.

---

Review each summary step by step against these criteria — especially checking that every number or result matches the abstract and that no additional or fake values are invented.

After your evaluation, report your reasoning and then state your final judgment in the format: **Summary X**

---

**Abstract:**
{abstract}

---

**Summaries:**
{summaries_text}

---

Your evaluation (step by step) followed by the final choice:
"""

        judge_context = [{"role": "user", "content": judge_prompt}]
        response = agent.generate_answer(judge_context)
        #print("Judge response:", response)

        match = re.findall(r"\*\*Summary\s*(\d+)\*\*", response)
        if match:
            selected = int(match[-1]) - 1  # Convert to 0-indexed
            if 0 <= selected < len(summaries):
                results.append(selected)
            else:
                results.append(None)
        else:
            results.append(None)

    # Step 2: Vote counting
    counter = Counter([r for r in results if r is not None])
    if not counter:
        return None  # No valid votes

    top_count = max(counter.values())
    top_candidates = [idx for idx, cnt in counter.items() if cnt == top_count]

    if len(top_candidates) == 1:

        return top_candidates[0]

    # Step 3: Tie-break using judge_summaries_experts_perp
    tied_summaries = [summaries[i] for i in top_candidates]

    #Call your imported tie-breaking function here
    final_choice_str, _ = judge_summaries_experts_perp(abstract, tied_summaries, tie_breaker)

    if final_choice_str:
        try:
            final_index = int(final_choice_str) - 1  # judge_summaries_experts_perp returns "1"-indexed
            if 0 <= final_index < len(tied_summaries):
                return top_candidates[final_index]
        except ValueError:
            print("Tie-break output could not be parsed.")
    else:
        print("No valid tie-break result.")

    return None


def combine_summaries_experts(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    judge_prompt = f"""
You are a biomedical research specialist tasked with generating an expert-level summary of the following research abstract by synthesizing multiple candidate summaries.

This summary must be written for an expert audience and will be judged on:

1. **Factual Faithfulness**: All statistics, time points, and findings must exactly match the abstract.
2. **Expert-Level Detail**: Include study design, biomarkers, precise numerical data (e.g., ORs, p-values), and key biological mechanisms if mentioned.
3. **Clarity & Technical Tone**: Use appropriate professional biomedical language.
4. **Completeness**: Cover all major findings and their clinical significance.

Use the candidate summaries only as raw materials. Combine their strengths to generate one superior expert-level summary — improving clarity, structure, analytic rigor, and conciseness.

**Do not explain your process. Output only the final refined expert-level summary.**

Abstract:
{abstract}

Candidate Summaries:
{summaries_text}

Your final expert summary:
"""

    judge_context = [{"role": "user", "content": judge_prompt}]
    response = judge_agent.generate_answer(judge_context)
    return response.strip()