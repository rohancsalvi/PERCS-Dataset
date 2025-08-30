import re
from collections import Counter


def judge_summaries_lay(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])
    judge_prompt = f"""
You are a skilled science communicator who specializes in making scientific research understandable and engaging for **high school students**. Your task is to evaluate summaries of a research abstract written for this audience.

Each summary should help **10th-grade students** understand the study, even if they have no background in biology, medicine, or research methods.

Judge each summary using these criteria:

1. **Accuracy and Faithfulness**: All key facts, results, and ideas must reflect the original abstract correctly. Do not reward summaries that add made-up details or leave out important findings.The summary should sound natural, friendly, and easy to follow
2. **Clarity and Simplicity**: The language must be simple and clear. Jargon or technical terms should be avoided, or briefly explained in a way a curious teenager can grasp.
3. **Essential Coverage**: The summary should briefly explain the study’s purpose, what was done (methods), the main results, and why it matters — without overwhelming the reader with too much technical detail.

Read the abstract and summaries carefully. Then judge each summary step-by-step using the four criteria above. Focus especially on **readability for teenagers**, **faithfulness to the abstract**, and **inclusion of core study elements**.

After your evaluation, state your reasoning briefly, then give your final judgment in this format: **Summary X**

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
   # print(response)
    matches = re.findall(r"\*\*Summary\s+(\d+)\*\*", response)
    if matches:
        final_choice_str = matches[-1]
        summary_number = int(final_choice_str) - 1
        if 0 <= summary_number < len(summaries):
            return str(summary_number + 1), summaries[summary_number]
        else:
            return None, "Invalid summary number or out of index range"
    else:
        return None, "No summary number found in the response"
    
def vote_on_summaries_lay(abstract, summaries, agents, tie_breaker):
    results = []

    # Step 1: Each agent votes using expert prompt logic
    for agent in agents:
        summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

        judge_prompt = f"""
You are a skilled science communicator who specializes in making scientific research understandable and engaging for **high school students**. Your task is to evaluate summaries of a research abstract written for this audience.

Each summary should help **10th-grade students** understand the study, even if they have no background in biology, medicine, or research methods.

Judge each summary using these criteria:

1. **Accuracy and Faithfulness**: All key facts, results, and ideas must reflect the original abstract correctly. Do not reward summaries that add made-up details or leave out important findings.The summary should sound natural, friendly, and easy to follow
2. **Clarity and Simplicity**: The language must be simple and clear. Jargon or technical terms should be avoided, or briefly explained in a way a curious teenager can grasp.
3. **Essential Coverage**: The summary should briefly explain the study’s purpose, what was done (methods), the main results, and why it matters — without overwhelming the reader with too much technical detail.

Read the abstract and summaries carefully. Then judge each summary step-by-step using the four criteria above. Focus especially on **readability for teenagers**, **faithfulness to the abstract**, and **inclusion of core study elements**.

After your evaluation, state your reasoning briefly, then give your final judgment in this format: **Summary X**

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
    final_choice_str, _ = judge_summaries_lay(abstract, tied_summaries, tie_breaker)

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


def combine_summaries_lay(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    judge_prompt = f"""
You are a skilled science communicator with a talent for explaining research in a way that is engaging and understandable for **high school students** (around 10th grade).

You are given a scientific abstract and multiple candidate summaries written for this audience. Use these summaries as **raw material** to draft a **single, improved summary** that provides the best possible overview of the abstract’s content in **student-accessible language**. Focus on supporting comprehension for curious students who have no background in biology, medicine, or research methods.

Your final summary should follow these guidelines:

1. **Accuracy and Faithfulness**: All key facts, results, and ideas must reflect the original abstract correctly. Do not reward summaries that add made-up details or leave out important findings. The summary should sound natural, friendly, and easy to follow.
2. **Clarity and Simplicity**: The language must be simple and clear. Jargon or technical terms should be avoided, oif included muste be briefly explained in a way a layperson can grasp.
3. **Essential Coverage**: The summary should briefly explain the study’s purpose, what was done (methods), the main results, and why it matters — without overwhelming the reader with too much technical detail.
---


**Abstract:**
{abstract}

---

**Candidate Summaries:**
{summaries_text}

---

Please write your **final summary only**. Do not include reasoning, scoring, or commentary.
"""

    judge_context = [{"role": "user", "content": judge_prompt}]
    response = judge_agent.generate_answer(judge_context)
    return response.strip()
