import re
from collections import Counter
import re

def judge_summaries_researcher(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])
    judge_prompt = f"""
You are a knowledgeable science communicator with strong interdisciplinary expertise. You are evaluating summaries of a scientific abstract.
Each summary is intended for researchers **outside the original field of the study** but with a robust understanding of general scientific principles. Judge each summary on these criteria:

1. **Accuracy and Faithfulness:** All main findings, data, and claims should be *faithfully* and *accurately* represented. Any numbers, methods, or terminology must be traceable to the abstract itself—avoid fabricated or omitted content.

2. **Clarity and Accessibility:** The summary must use clear, accessible language. Domain-specific terms should be minimized; if used, they must be explained succinctly in context. Complex medical ideas must be paraphrased where possible for non-specialists.

3. **Comprehensiveness:** The summary should capture all essential study components: purpose, methodology, key results, and conclusions, ensuring none of the major points is omitted.

4. **Professional and Neutral Tone:** The writing should be professional, precise, and neutral. Avoid over-simplification or subjective commentary.

Evaluate each summary step by step against these criteria. Focus in particular on clear and accessible language for non-domain experts, accuracy of reported facts, and completeness of coverage versus the abstract.

After reviewing, report your reasoning, then state your final judgment in this format: **Summary X**

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
    

def vote_on_summaries_researcher(abstract, summaries, agents, tie_breaker):
    results = []

    # Step 1: Each agent votes using expert prompt logic
    for agent in agents:
        summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

        judge_prompt = f"""
You are a knowledgeable science communicator with strong interdisciplinary expertise. You are evaluating summaries of a scientific abstract.
Each summary is intended for researchers **outside the original field of the study** but with a robust understanding of general scientific principles. Judge each summary on these criteria:

1. **Accuracy and Faithfulness:** All main findings, data, and claims should be *faithfully* and *accurately* represented. Any numbers, methods, or terminology must be traceable to the abstract itself—avoid fabricated or omitted content.

2. **Clarity and Accessibility:** The summary must use clear, accessible language. Domain-specific terms should be minimized; if used, they must be explained succinctly in context. Complex medical ideas must be paraphrased where possible for non-specialists.

3. **Comprehensiveness:** The summary should capture all essential study components: purpose, methodology, key results, and conclusions, ensuring none of the major points is omitted.

4. **Professional and Neutral Tone:** The writing should be professional, precise, and neutral. Avoid over-simplification or subjective commentary.

Evaluate each summary step by step against these criteria. Focus in particular on clear and accessible language for non-domain experts, accuracy of reported facts, and completeness of coverage versus the abstract.

After reviewing, report your reasoning, then state your final judgment in this format: **Summary X**

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
    final_choice_str, _ = judge_summaries_researcher(abstract, tied_summaries, tie_breaker)

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

def combine_summaries_researcher(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    judge_prompt = f"""
You are a skilled science communicator with a deep understanding of interdisciplinary research.
Your task is to produce a single, well-structured and **accessible** summary of the research abstract below. Your readers are scientists and researchers **from non-medical disciplines**—such as computer science, engineering, psychology, or environmental science—who may not be familiar with clinical or biological terminology.
You are given multiple candidate summaries. Use them only as raw material to craft a new, superior version that retains scientific accuracy while maximizing accessibility.

The resulting summary must follow these principles:

- **Clarity for Non-Specialists**: Write in clear, professional language understandable to scientifically literate readers outside the medical domain. When technical terms are needed, explain them briefly in context.
- **Accessible Scientific Communication**: Avoid excessive jargon. Prioritize accurate paraphrasing of complex ideas. Focus on findings and relevance without oversimplification.
- **Appropriate Detail**: Provides key background, overview of methods, and main findings, detailed enough for non-medical researchers to understand what was studied, how, and its significance.
- **Accuracy and Faithfulness**: All reported findings, methods, data, and numeric results must match the original abstract exactly—no additions or omissions.
---

**Abstract:**
{abstract}

---

**Candidate Summaries:**
{summaries_text}

---

Please write your **final summary** only. Do not explain your reasoning or editing process.
"""

    judge_context = [{"role": "user", "content": judge_prompt}]
    response = judge_agent.generate_answer(judge_context)
    return response.strip()