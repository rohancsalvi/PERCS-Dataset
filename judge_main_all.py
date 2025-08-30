# ==== USER SETTINGS ====
PERSONA = "researcher"  # Change to "lay", "premed", or "expert"
from Judge.judge_lay import (
    judge_summaries_lay, vote_on_summaries_lay, combine_summaries_lay
)
from Judge.judge_premed import (
    judge_summaries_premed, vote_on_summaries_premed, combine_summaries_premed
)
from Judge.judge_researcher import (
    judge_summaries_researcher, vote_on_summaries_researcher, combine_summaries_researcher
)
from Judge.judge_expert import (
    judge_summaries_experts, vote_on_summaries_experts, combine_summaries_experts
)

# Set persona-specific functions based on PERSONA variable
if PERSONA == "lay":
    judge_summaries = judge_summaries_lay
    vote_on_summaries = vote_on_summaries_lay
    combine_summaries = combine_summaries_lay
elif PERSONA == "premed":
    judge_summaries = judge_summaries_premed
    vote_on_summaries = vote_on_summaries_premed
    combine_summaries = combine_summaries_premed
elif PERSONA == "researcher":
    judge_summaries = judge_summaries_researcher
    vote_on_summaries = vote_on_summaries_researcher
    combine_summaries = combine_summaries_researcher
elif PERSONA == "expert":
    judge_summaries = judge_summaries_experts
    vote_on_summaries = vote_on_summaries_experts
    combine_summaries = combine_summaries_experts
else:
    raise ValueError(f"Unknown persona '{PERSONA}'. Choose from: lay, premed, researcher, expert.")


import pandas as pd
from agents import OpenAIAgent, GeminiAIAgent, MistralAIAgent, LlamaAgent

def evaluate_summaries(csv_file, output_csv, mode="voting"):
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    models = ['gpt', 'gemini', 'mistral', 'llama']
    current_columns = df.columns.tolist()
    for i in range(1, 5):
        current_columns[-i] = models[-i]
    df.columns = current_columns

    agent1 = OpenAIAgent("gpt-4o")
    agent2 = GeminiAIAgent()
    agent3 = MistralAIAgent()
    agent4 = LlamaAgent()
    judge_agent = LlamaAgent()
    tie_breaker = LlamaAgent()
    agents = [agent1, agent2, agent3, agent4]

    results = []
    for index, row in df.iterrows():
        abstract = row["abstract"]
        summaries = [row[name] for name in models]
        if mode == "voting":
            best_summary_index = vote_on_summaries(abstract, summaries, agents, tie_breaker)
            best_summary = summaries[best_summary_index] if best_summary_index is not None else "No consensus"
            best_num = best_summary_index + 1 if best_summary_index is not None else "No consensus"
        elif mode == "judge":
            agent_no, best_summary = judge_summaries(abstract, summaries, judge_agent)
            best_num = agent_no if agent_no is not None else "No consensus"
        else:
            raise ValueError("mode must be either 'voting' or 'judge'")
        results.append({
            "Abstract": abstract,
            "Best Summary": best_summary,
            "Best Summary Number": best_num,
        })
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False, encoding='utf-8-sig')


def generate_combined_summaries(csv_file, output_csv):
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    models = ['gpt', 'gemini', 'mistral', 'llama']
    current_columns = df.columns.tolist()
    for i in range(1, 5):
        current_columns[-i] = models[-i]
    df.columns = current_columns
    judge_agent = LlamaAgent()
    results = []
    for index, row in df.iterrows():
        abstract = row['abstract']
        summaries = [row[model] for model in models if model in row]
        output_summary = combine_summaries(abstract, summaries, judge_agent)
        results.append({
            "Abstract": abstract,
            "Combined Summary": output_summary,
        })
    results = pd.DataFrame(results)
    results.to_csv(output_csv, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    # ==== USER SETTINGS ====
    input_file = "input_demo_judge.csv"
    output_file = f"summaries_output_judge_{PERSONA}.csv"

    # Evaluate summaries (choose mode="judge" or "voting")
    evaluate_summaries(input_file, output_file, mode="voting")
    generate_combined_summaries(input_file, f"combined_summaries_{PERSONA}.csv")
