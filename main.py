import pandas as pd
from prompting import build_prompt
from self_refine import self_refine_summary
from agents import OpenAIAgent, GeminiAIAgent, MistralAIAgent, LlamaAgent

def generate_summaries(
    agents,
    input_file,
    output_file,
    persona="layman",
    mode="zero-shot"
):
    """
    Generate summaries for each abstract in the input file using specified agent,persona and mode.

    Parameters:
        agents: list of agent objects
        input_file: path to CSV file with 'abstract' or 'text' column
        output_file: path to save the output CSV
        persona: "expert", "researcher", "premed", or "layman"
        mode: "zero-shot", "few-shot", or "self-refine"
    """
    df = pd.read_csv(input_file)
    if "abstract" in df.columns:
        abstracts = df["abstract"].tolist()
        #abstracts = abstracts[:]
    elif "text" in df.columns:
        abstracts = df["text"].tolist()
    else:
        abstracts = df.iloc[:, 0].tolist()  # fallback: use first column

    results = []
    for idx, abstract in enumerate(abstracts):
        if idx % 10 == 0:
            print(f"Processing abstract {idx + 1}/{len(abstracts)}")
        for agent in agents:
            if mode == "self-refine":
                summary = self_refine_summary(abstract, persona, agent)
            else:
                context = build_prompt(abstract, persona, mode)
                summary = agent.generate_answer(context)
            results.append({
                "abstract": abstract,
                "summary": summary,
                "persona": persona,
                "mode": mode,
                "agent": agent.__class__.__name__
            })

    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Saved {len(results)} summaries to {output_file}")

# --------- MAIN ---------

if __name__ == "__main__":
    # ==== USER SETTINGS ====
    input_file = "input.csv"
    output_file = "output.csv"
    persona = "layman"         # Choose: "expert", "researcher", "premed", "layman"
    mode = "few-shot"          # Choose: "zero-shot", "few-shot", or "self-refine"

    agents = [
         OpenAIAgent(model="gpt-4o"),
        GeminiAIAgent(model="google/gemini-2.0-flash-lite-001"),
        MistralAIAgent(model="mistralai/mixtral-8x7b-instruct"),
        LlamaAgent(model="meta-llama/llama-3.3-70b-instruct"),
    ]

    generate_summaries(
        agents=agents,
        input_file=input_file,
        output_file=output_file,
        persona=persona,
        mode=mode
    )