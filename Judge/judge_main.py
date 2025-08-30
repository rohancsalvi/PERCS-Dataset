import pandas as pd
from tqdm import tqdm
from Judge.judge_researcher import (
    judge_summaries_researcher,
    vote_on_summaries_researcher,
    combine_summaries_researcher,
)
from agents import OpenAIAgent, GeminiAIAgent, MistralAIAgent, LlamaAgent

def evaluate_summaries(csv_file, output_csv, mode="voting"):
    """
    Evaluate summaries for each abstract using either:
    - "voting": all agents vote and resolve ties
    - "judge": single judge agent decides

    Args:
        csv_file: input CSV file path
        output_csv: output CSV file path
        mode: "voting" (default) or "judge"
    """
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    models = ['gpt', 'gemini', 'mistral', 'llama']
    current_columns = df.columns.tolist()
    for i in range(1, 5):
        current_columns[-i] = models[-i]
    df.columns = current_columns

    # Instantiate agents
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
            best_summary_index = vote_on_summaries_researcher(abstract, summaries, agents, tie_breaker)
            best_summary = summaries[best_summary_index] if best_summary_index is not None else "No consensus"
            best_num = best_summary_index + 1 if best_summary_index is not None else "No consensus"
        elif mode == "judge":
            agent_no, best_summary = judge_summaries_researcher(abstract, summaries, judge_agent)
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
        output_summary = combine_summaries_researcher(abstract, summaries, judge_agent)
        results.append({
            "Abstract": abstract,
            "Combined Summary": output_summary,
        })
    results = pd.DataFrame(results)
    results.to_csv(output_csv, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    # Example usage:
     # ==== USER SETTINGS ====
    input_file = "input_demo_judge.csv"
    output_file = "summaries_output_judge_researcher.csv"
    evaluate_summaries(input_file,output_file )
    generate_combined_summaries(input_file, "combined_summaries_demo.csv")