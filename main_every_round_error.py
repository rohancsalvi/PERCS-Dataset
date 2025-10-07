import pandas as pd
from tqdm import tqdm

from Feedback.every_round_error import ERROR_FEEDBACK_PHASES
from persona_specifc_prompt import generate_summary
from Feedback.error_feedback import generate_summary_with_feedback_error
from agents import OpenAIAgent, GeminiAIAgent, MistralAIAgent, LlamaAgent

def rotate_list(items, n):
    return items[n:] + items[:n]

def every_round_error_dispatcher(summary, abstract, agent, persona, round_number):
    persona = persona.lower()
    if persona not in ERROR_FEEDBACK_PHASES:
        raise ValueError(f"Unknown persona: {persona}")
    phase_fns = ERROR_FEEDBACK_PHASES[persona]
    idx = min(round_number, len(phase_fns) - 1)
    return phase_fns[idx](summary, abstract, agent)

if __name__ == "__main__":
    # ==== USER SETTINGS ====
    input_file = "input_demo.csv"
    output_file = "summaries_output_err_feedback.csv"
    abstract_column = "abstract"
    persona = "expert"    # "expert", "researcher", "premed", "lay"
    number_of_rounds = 3
    accumulate_feedback = False

    # ==== DATA ====
    df = pd.read_csv(input_file, encoding='utf-8')
    abstracts = df[abstract_column].tolist()
    abstracts_selected = abstracts[:2]  # adjust as needed

    # ==== AGENTS ====
    agent1 = OpenAIAgent("gpt-4o")
    agent2 = GeminiAIAgent()
    agent3 = MistralAIAgent()
    agent4 = LlamaAgent()
    agents = [agent1, agent2, agent3, agent4]
    feedback_agent = LlamaAgent()  # Can use any model for review

    # ==== MAIN LOOP ====
    results = pd.DataFrame()

    for abstract in tqdm(abstracts_selected, desc="Processing Sentences"):
        summary_data = {"Abstract": abstract}
        # Generate initial summaries for each agent
        initial_summaries = {agent: generate_summary(abstract, agent, persona) for agent in agents}

        for agent in agents:
            summary_data[f"{agent.model}_Round0"] = initial_summaries[agent]

        feedback_histories = {agent: [] for agent in agents}

        for round_number in range(number_of_rounds):
            current_feedback = {agent: [] for agent in agents}
            # Use persona-specific phase function for the current round
            for agent in agents:
                feedback = every_round_error_dispatcher(
                    initial_summaries[agent],
                    abstract,
                    feedback_agent,
                    persona,
                    round_number
                )
                current_feedback[agent].append(feedback)
                summary_data[f"Feedback_{agent.model}_Round{round_number+1}"] = feedback

            # Update summaries using the feedback
            for agent in agents:
                if accumulate_feedback:
                    feedback_histories[agent].extend(current_feedback[agent])
                    feedback_for_update = feedback_histories[agent]
                else:
                    feedback_for_update = current_feedback[agent]
                # --- Now actually refine the summary with feedback:
                updated_summary = generate_summary_with_feedback_error(
                    initial_summaries[agent],
                    feedback_for_update,
                    agent,
                    persona
                )
                initial_summaries[agent] = updated_summary
                summary_data[f"{agent.model}_Round{round_number+1}"] = updated_summary

        results = pd.concat([results, pd.DataFrame([summary_data])], ignore_index=True)

    results.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved every-round error results to {output_file}")
