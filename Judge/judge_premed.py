from collections import Counter
import re

def judge_summaries_premed(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    judge_prompt = f"""
You are an academic tutor specializing in science communication for pre-medical students. Your task is to evaluate several summaries written for pre-med students with foundational knowledge in biology and chemistry. Each summary is based on the same scientific abstract.

These summaries are not for experts or practitioners. The goal is to make the content of the abstract clear and educationally accessible for students preparing for careers in health or medicine.

Evaluate each summary using these criteria:

- **Clarity and Accessibility:** The language should be simple. The summary shiuld try to simplfy complex sentences and avoid medical jargon whenever possible in the summary not seperately. If a advanced medical term is necessary, it must be briefly and clearly explained in plain words. The tone should support learning and comprehension.

- **Accuracy and Faithfulness:** The summary must directly reflect the abstract’s actual content — including its purpose, methods, key findings, and conclusions — without adding assumptions, interpretations, implications, or opinions not present in the abstract.

- **Relevance for Pre-Meds:** Only include details that would be meaningful or understandable to pre-med students. Omit information that is too technical or outside the scope of their background knowledge unless clearly explained.

---

**Abstract:**
{abstract}

---

**Summaries:**
{summaries_text}

---

Evaluate each summary step by step using the criteria above. The summary should be clear,accessible for pre-med students, and provide a complete overview of the study.

After evaluating, identify the best summary in this format:

**Summary X**

Your evaluation followed by the final choice:
"""

    judge_context = [{"role": "user", "content": judge_prompt}]
    response = judge_agent.generate_answer(judge_context)
    print(response)
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




def vote_on_summaries_premed(abstract, summaries, agents, tie_breaker):
    results = []

    # Step 1: Each agent votes using expert prompt logic
    for agent in agents:
        summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

        judge_prompt = f"""
You are an academic tutor specializing in science communication for pre-medical students. Your task is to evaluate several summaries written for pre-med students with foundational knowledge in biology and chemistry. Each summary is based on the same scientific abstract.

These summaries are not for experts or practitioners. The goal is to make the content of the abstract clear and educationally accessible for students preparing for careers in health or medicine.

Evaluate each summary using these criteria:

- **Clarity and Accessibility:** The language should be simple. The summary shiuld try to simplfy complex sentences and avoid medical jargon whenever possible in the summary not seperately. If a advanced medical term is necessary, it must be briefly and clearly explained in plain words. The tone should support learning and comprehension.

- **Accuracy and Faithfulness:** The summary must directly reflect the abstract’s actual content — including its purpose, methods, key findings, and conclusions — without adding assumptions, interpretations, implications, or opinions not present in the abstract.

- **Relevance for Pre-Meds:** Only include details that would be meaningful or understandable to pre-med students. Omit information that is too technical or outside the scope of their background knowledge unless clearly explained.

---

**Abstract:**
{abstract}

---

**Summaries:**
{summaries_text}

---

Evaluate each summary step by step using the criteria above. The summary should be clear,accessible for pre-med students, and provide a complete overview of the study.

After evaluating, identify the best summary in this format:

**Summary X**

Your evaluation followed by the final choice:
"""

        judge_context = [{"role": "user", "content": judge_prompt}]
        response = agent.generate_answer(judge_context)
        #print("Judge response:", response)

        match = re.findall(r"\*\*Summary\s+(\d+)\*\*", response)
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

    #tie-breaking function
    final_choice_str, _ = judge_summaries_premed(abstract, tied_summaries, tie_breaker)

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


def combine_summaries_premed(abstract, summaries, judge_agent):
    summaries_text = "\n\n".join([f"Summary {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    judge_prompt = f"""
You are an expert science communicator and academic tutor focused on supporting **pre-medical students**. Your task is to create a clear, accurate, lay summary of the research abstract below. Your audience includes students in pre-medical school who have a solid foundation in biology and chemistry, but limited exposure to complex clinical or medical terminology.
You are given multiple candidate summaries. Use them as raw material to draft a **single, improved summary** that provides the best overview of the abstract’s content in a student accessible language. Focus on supporting student understanding.
Your final summary should follow these guidelines:

- **Clarity and Simplicity**: Use plain, and clear language. Rephrase complex medical ideas in a way that makes them easier to understand without oversimplifying important scientific meaning. When technical terms must be used, give a short and clear explanation.
- **Educational Relevance**: Only include content that would be meaningful and understandable by a pre-med students. Avoid overly technical or specialized information unless clearly explained for the student audience.
- **Accuracy and Completeness**: Your summary must closely reflect the content of the original abstract, including the study’s purpose, methods, key findings, and conclusions. Do not add interpretations,opinions and own conlcusions, and do not leave out any important points.
---



**Abstract:**
{abstract}

---

**Candidate Summaries:**
{summaries_text}

---

Please write your final summary only. Do not include explanations or describe your process.
"""

    judge_context = [{"role": "user", "content": judge_prompt}]
    response = judge_agent.generate_answer(judge_context)
    return response.strip()