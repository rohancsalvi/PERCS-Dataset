import pandas as pd
from tqdm import tqdm
from Feedback.persona_specifc_prompt import (
    generate_summary,
    feedback_summary,
    generate_summary_with_feedback)
from Feedback.error_feedback import (detect_errors, generate_summary_with_feedback_error)
from agents import OpenAIAgent, GeminiAIAgent, MistralAIAgent, LlamaAgent


from Feedback.every_round_error import ERROR_FEEDBACK_PHASES

def every_round_error_dispatcher(summary, abstract, agent, persona, round_number):
    persona = persona.lower()
    if persona not in ERROR_FEEDBACK_PHASES:
        raise ValueError(f"Unknown persona: {persona}")
    phase_fns = ERROR_FEEDBACK_PHASES[persona]
    idx = min(round_number, len(phase_fns)-1)
    return phase_fns[idx](summary, abstract, agent)

def generate_summary_with_feedback_dispatcher(last_summary, feedback_list, agent, persona, mode):
    if mode == "error":
        return generate_summary_with_feedback_error(last_summary, feedback_list, agent, persona)
    elif mode == "feedback":
        return generate_summary_with_feedback(last_summary, feedback_list, agent, persona)
    else:
        raise ValueError(f"Unknown mode: {mode}")

def rotate_list(items, n):
    return items[n:] + items[:n]

print("Script ran fine so far.")

if __name__ == "__main__":
    # ==== USER SETTINGS ====
    input_file = "input_demo.csv"
    output_file = "summaries_output_err_feedback.csv"
    abstract_column = "abstract"
    persona = "researcher"      # or "lay", "researcher", "expert"
    mode = "error"       # "feedback" or "error"
    number_of_rounds = 3
    accumulate_feedback = False

    # ==== DATA ====
    df = pd.read_csv(input_file, encoding='utf-8')
    abstracts = df[abstract_column].tolist()
    abstracts_selected = abstracts[:2]  # adjust slice as needed

    # ==== AGENTS ====
    agent1 = OpenAIAgent("gpt-4o")
    agent2 = GeminiAIAgent()
    agent3 = MistralAIAgent()
    agent4 = LlamaAgent()
    agents = [agent1, agent2, agent3, agent4]

    # ==== MAIN LOOP ====
    results = pd.DataFrame()

    for abstract in tqdm(abstracts_selected, desc="Processing Abstracts"):
        agent_summaries = {agent: [] for agent in agents}
        feedback_histories = {agent: [] for agent in agents}
        initial_summaries = {agent: generate_summary(abstract, agent, persona) for agent in agents}

        row = {"Abstract": abstract}
        for agent in agents:
            summary = initial_summaries[agent]
            agent_summaries[agent].append(summary)
            row[f"{agent}_Round0"] = summary

        for round_number in range(number_of_rounds):
            current_feedback = {agent: [] for agent in agents}
            feedback_order = rotate_list(agents, round_number)

            for idx, agent in enumerate(agents):
                feedback_agent = feedback_order[(idx + 1) % len(agents)]
                if mode == "error":
                    feedback = detect_errors(initial_summaries[agent], abstract, feedback_agent, persona)
                elif mode == "feedback":
                    feedback = feedback_summary(initial_summaries[agent], abstract, feedback_agent, persona)
                else:
                    raise ValueError(f"Unknown mode: {mode}")
                current_feedback[agent].append(feedback)
                row[f"Feedback_{agent}_Round{round_number + 1}"] = feedback

            for agent in agents:
                feedback_for_update = feedback_histories[agent] if accumulate_feedback else current_feedback[agent]
                updated_summary = generate_summary_with_feedback_dispatcher(
                    initial_summaries[agent],
                    feedback_for_update,
                    agent,
                    persona,
                    mode  # "feedback" or "error"
                )
                initial_summaries[agent] = updated_summary
                agent_summaries[agent].append(updated_summary)
                row[f"{agent}_Round{round_number + 1}"] = updated_summary

        results = pd.concat([results, pd.DataFrame([row])], ignore_index=True)

    results.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved feedback/error results to {output_file}")
