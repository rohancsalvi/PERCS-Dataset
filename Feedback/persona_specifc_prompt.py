############################ EXPERT #######################################
def generate_summary_expert(abstract, agent, persona="Expert"):
    # Prompt A: For GPT & Mistral
    prompt_a = f"""
    You are a seasoned subject matter expert in the biological sciences and are preparing a summary of a research abstract for an expert audience in the same field.
    You decide to generate this summary with the following key principles in mind:
    1) The target audience is experts and professionals within the same scientific field who are seeking a concise overview of the study.\
    2) Do not simplify technical terms or scientific concepts; preserve their complexity and meaning.
    3) Maintain a formal and objective tone suitable for a professional scientific discourse.
    4) The sentence structure should be academically appropriate and support a coherent, logical flow of information.
    5) Ensure the summary includes the core findings, methodology, and significance of the study without omitting critical data.
    6) The text must remain factually accurate, including all relevant terminology, experimental parameters, numeric results, and implications.
       The word count should not exceed 250 words.
    """

    # Prompt B: For Gemini & LLaMA
    prompt_b = f"""
    You are a seasoned subject matter expert in the biological sciences and are preparing a summary of a research abstract for an expert audience in the same field.
    Write a structured summary using field-appropriate language and avoid simplifying key scientific concepts or vocabulary.
    The summary should retain methodological details, include relevant numerical figures, and clearly explain the study’s significance and contribution to the field.
    Maintain an academic tone and a coherent, logically structured narrative that flows naturally from background to findings.
    Do not use bullet points, question-answer format, or numbered lists. The summary should be written as continuous prose.
    The content must remain scientifically rigorous and factually accurate in all terminology, methods, results, and implications.
    The summary must not exceed 250 words.
    Produce only the summary. Do not add commentary, interpretation, or meta-level notes on the summarization process.
    """


    # Get agent name/model to choose prompt
    agent_name = agent.model.lower()  # Assuming each agent has a `.model` attribute

    if "gpt" in agent_name or "mistral" in agent_name:
        chosen_prompt = prompt_a
    elif "gemini" in agent_name or "llama" in agent_name:
        chosen_prompt = prompt_b
    else:
        raise ValueError(f"Unknown agent type for model: {agent.model}")

    # Combine with the abstract
    summary_context = [{
        "role": "user",
        "content": f"{chosen_prompt.strip()}\n\nAbstract: {abstract.strip()}"
    }]

    return agent.generate_answer(summary_context)

def feedback_summary_expert(summary, abstract, agent):
    feedback_categories = {
        "Content Accuracy": "Check if the summary covers all major findings and avoids introducing information not present in the abstract.",
        "Technical Detail": "Ensure that the summary includes relevant deatils for methods, sample sizes, statistical results, and quantitative findings.",
        "Terminology Use": "Evaluate whether technical terms are used appropriately for an expert audience, without unnecessary simplification or over-explanation.",
        "Factual Consistency": "Check for any factual mismatches or interpretive errors when compared to the original abstract.",
        "Logical Flow": "Assess whether the summary presents information in a clear, structured, and logically progressive manner.",
        "Expert-Level Clarity": "Ensure the summary reflects the tone, depth, and precision expected by domain experts. Highlight any vague or verbose sections."
    }

    feedback_instructions = "\n".join(
        [f"- **{category}**: {description}" for category, description in feedback_categories.items()]
    )

    feedback_prompt = f"""

You are reviewing a scientific summary written for an expert audience. Compare it to the original abstract and provide targeted feedback using the following categories.

{feedback_instructions}

Instructions:
- For each category, provide specific examples from the summary.
- Recommend concrete, concise edits to improve technical clarity and factual precision.
- Avoid general statements and focus on improvements that reflect expert expectations.
- If the summary adds interpretation not found in the abstract, flag and suggest a fix.

Abstract:
{abstract}

Summary:
{summary}
"""

    feedback_context = [{
        "role": "user",
        "content": feedback_prompt
    }]

    return agent.generate_answer(feedback_context)

def generate_summary_with_feedback_expert(last_summary, feedback_list, agent,abstract):
    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
            "You are revising a summary of an abstract intended for medical domain experts.\n\n"
            "Use the feedback below to improve the summary. The revised version must meet the following criteria:\n"
            "- Use precise technical language suitable for an expert audience."
            "- Do not include interpretive statements that are not present in the original abstract.\n"
            "- While revising ensure that there is not redundancy in information and generic statements."
            "- Maintain a concise, professional tone and limit the summary to 250 words.\n"
            "- Do not use bulleted or numbered lists.\n\n"
            "Summary:\n"
            f"{last_summary}\n\n"
            "Feedback:\n"
            f"{feedback}"
        )
    }]

    return agent.generate_answer(feedback_and_refine_context)

############################ RESEARCHER #######################################
def generate_summary_researcher(abstract, agent, persona="Researcher"):
    # Prompt A: For GPT & Mistral
    prompt_a = f"""
                You are a knowledgeable science communicator with interdisciplinary expertise. Your task is to write a clear and comprehensive summary of a scientific abstract for researchers outside the specific field of the study but with a solid understanding of general scientific principles.
                When summarizing, follow these key principles:
                1) The audience consists of researchers in other fields than biology and medicine who may not be familiar with domain-specific terminology or methods.
                2) Use clear and accessible language. Avoid unnecessary technical jargon; when technical terms are necessary, explain them briefly in context.
                3) Accurately represent the study's main findings, methodology, and results.
                4) Maintain a professional but approachable tone. Aim for clarity and precision without overly simple or domain-specific language.
                5) Structure the summary as paragrapgh. Do not use bullet points, numbered lists, or Q&A formats.
                6) Focus on the scientific content only. Do not include commentary about the summarization process or subjective judgement of the study's importance.
                The final summary should not exceed 350 words."""


    # Prompt B: For Gemini & LLaMA
    prompt_b = f"""
                You are a knowledgeable science communicator summarizing a scientific abstract for an audience of researchers who are not specialists in the specific field of the study, but who are familiar with general scientific methods and concepts.
                Write a concise, clear summary that:
                  - Explains the study’s key findings, methods, and results.
                  - Uses clear and accessible language, avoiding heavy jargon. When technical terms are essential, include a short, simple explanation.
                  - Maintains an informative and professional tone without sounding overly technical or overly simplified.
                  - Do not use bullet points, numbered lists, or question-and-answer formats. Write in well-structured paragrapgh format.
                  - The summary must not exceed 350 words.
                  - The summary should not include any commentary about the summarization process or subjective judgments about the study's importance."""


    # Get agent name/model to choose prompt
    agent_name = agent.model.lower()  # Assuming each agent has a `.model` attribute

    if "gpt" in agent_name or "mistral" in agent_name:
        chosen_prompt = prompt_a
    elif "gemini" in agent_name or "llama" in agent_name:
        chosen_prompt = prompt_b
    else:
        raise ValueError(f"Unknown agent type for model: {agent.model}")

    # Combine with the abstract
    summary_context = [{
        "role": "user",
        "content": f"{chosen_prompt.strip()}\n\nAbstract: {abstract.strip()}"
    }]

    return agent.generate_answer(summary_context)


def feedback_summary_researcher(summary, abstract, agent):


    feedback_categories = {
        "Definition Enhancement": "Suggest where brief definitions or clarifications of technical terms would improve clarity for researchers outside the domain.",
        "Synonym Suggestions": "Identify domain-specific terms or phrases that could be replaced with more familiar synonyms to enhance accessibility.",
        "Simplification Needs": "Highlight sentences or phrases that are unnecessarily complex or technical, and propose simpler alternatives written in a scientific tone appropriate for researchers.",
        "Detail Adjustment": "Assess whether key methodological, results-related, or numerical details are appropriately included. Indicate where these are missing or could be more clearly represented.",
        "Factuality Check": "Verify that all information in the summary accurately reflects the original abstract. Point out any inaccuracies or misinterpretations.",
        "Overall Coherence": "Evaluate the logical flow of the summary. Suggest revisions if the structure, organization, or transitions reduce clarity.",
        "Key Point Highlight": "Ensure all major ideas and findings are clearly conveyed to help researchers from other domains understand the study while maintaining accessibility."
    }


    feedback_instructions = "\n".join([f"{category}: {description}" for category, description in feedback_categories.items()])

    feedback_prompt = f"""
    Task: Review the provided summary compared to the original abstract. Suggest improvements to make the summary better intended for researchers with a general scientific background, but who are not specialists in the specific field of the abstract, using the following feedback categories as guidance.

    {feedback_instructions}

    Instructions:
    - For each feedback category, provide specific examples from the summary and propose clear, constructive improvements.
    - Where applicable discuss why these changes or additions would enhance the understanding or appeal of the summary.
    - Keep your comments focused on what researchers who are not specialists in the specific field of the study may need.

    Abstract:
    {abstract}

    Summary:
    {summary}
    """

    feedback_context = [{
        "role": "user",
        "content": feedback_prompt
    }]

    return agent.generate_answer(feedback_context)

def generate_summary_with_feedback_researcher(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary intended for researchers with a general scientific background, but who are not specialists in the specific field of the abstract, based on the feedback provided below.\n"
          f"Do not use numbered list format in the revised summary to explain meaning of jargons, research methodology, and findings of the study. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 350 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)
############################ PREMED  #######################################

def generate_summary_premed(abstract, agent, persona="Premed"):
    # Prompt A: For GPT & Mistral
    prompt_a = f"""
                  You are an experienced academic tutor in the medical sciences. Your task is to write a summary of a research abstract specifically for pre-med students.
                  When summarizing, follow these key principles:
                  1) The audience has foundational knowledge of biology and chemistry.
                  2) Use clear, simple language, and avoid technical jargon unless essential; when used, briefly explain the term.
                  3) Maintain accuracy while making the information accessible and engaging for pre med students.
                  4) Ensure the summary flows logically and reads like a helpful explanation, not as dense scientific writing.
                  5) Ensure the summary accurately conveys the study’s key findings, methodology, and relevance to medical sciences.
                  6) The summary should be written as continuous paragrapgh avoid bullet points, lists, or Q&A formats.
                  The word count of the summary should not exceed 350 words.
                  Do not include any concluding commentary for the students, notes on the summarization process, or any self-determined importance of the study for pre med students."""


    # Prompt B: For Gemini & LLaMA
    prompt_b = f"""
                  You are an academic tutor tasked with summarizing a scientific abstract for pre-medical students.
                  Write a clear and accessible summary using language suitable for students with basic knowledge of biology and chemistry.
                  Avoid heavy technical jargon. When specialized terms are necessary, briefly explain them in simple words.
                  Ensure the summary accurately conveys the study’s key findings, methodology, and relevance to medical sciences.
                  Present the information in a logical, instructional tone that supports student learning and comprehension.
                  Do not use bullet points, numbered lists, or Q&A formats. Write in well-structured, continuous prose.
                  The summary must not exceed 350 words.
                  Do not include any concluding commentary for the students, notes on the summarization process, or any self-determined importance of the study."""

    # Get agent name/model to choose prompt
    agent_name = agent.model.lower()  # Assuming each agent has a `.model` attribute

    if "gpt" in agent_name or "mistral" in agent_name:
        chosen_prompt = prompt_a
    elif "gemini" in agent_name or "llama" in agent_name:
        chosen_prompt = prompt_b
    else:
        raise ValueError(f"Unknown agent type for model: {agent.model}")

    # Combine with the abstract
    summary_context = [{
        "role": "user",
        "content": f"{chosen_prompt.strip()}\n\nAbstract: {abstract.strip()}"
    }]

    return agent.generate_answer(summary_context)


def feedback_summary_premed(summary, abstract, agent):
    feedback_categories = {
        "Definition Addition": "Identify any technical or medical terms that may need a brief explanation for better understanding by pre-med students.",
        "Simpler Words": "Suggest where complex or domain-specific terms could be replaced with simpler, more familiar words.",
        "Clearer Sentences": "Highlight sentences that are too complex or technical, and suggest simpler, clearer alternatives that maintain scientific accuracy.",
        "Missing or Unclear Details": "Check whether key elements of the study (e.g., methods, findings, statistics) are missing or unclear. Recommend where to add or clarify information.",
        "Accuracy Check": "Ensure the summary accurately reflects the content of the original abstract. Flag any misleading or incorrect interpretations.",
        "Redundancy": "Point out any repetitive or unnecessary content that could be removed or condensed.",
        "Easy to Follow": "Evaluate the logical flow and structure of the summary. Suggest improvements to transitions, organization, or coherence if needed."
    }

    feedback_instructions = "\n".join(
        [f"**{category}**: {description}" for category, description in feedback_categories.items()]
    )

    feedback_prompt = f"""
You are reviewing a summary written for pre-med students. Your task is to compare the summary to the original research abstract and provide constructive, category-based feedback to help improve clarity, accuracy, and accessibility.

Use the following feedback categories as a guide:

{feedback_instructions}

**Instructions:**
- For each feedback category, provide specific examples from the summary and suggest improvements.
- If no issues are found in a category, you may skip it.
- Explain how your suggestions would improve the summary for a pre-med audience.
- Focus on clarity, accuracy, and accessibility for students with limited medical background.

---

**Abstract:**
{abstract}

---

**Summary:**
{summary}
"""

    feedback_context = [{
        "role": "user",
        "content": feedback_prompt
    }]

    return agent.generate_answer(feedback_context)



def generate_summary_with_feedback_premed(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary intended for pre-med students, based on the feedback provided below.\n"
          f"Do not use numbered list format in the revised summary to explain meaning of jargons, research methodology, and findings of the study. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 350 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)


############################ LAYMAN #######################################


def generate_summary_lay(abstract, agent, persona="Lay"):
    # Prompt A: For GPT & Mistral
    prompt_a = f"""
    You are a biology teacher in a high school and want to teach students in 10th grade about a research study. Your goal is to convey the information in the abstract in plain and easy to understand language that students can follow.
    You decide to generate a plain text for the same abstract keeping in mind what makes a text simple and easy to understand.
    1) It attempts to avoid as much scientific jargon as possible. If it cannot avoid it, then it replaces it with easy to understand synonyms.
    2) It has explanation and definition for complex biological terms  and can include simple real-life examples to make it easier to understand.
    3) The sentence structure is simple and text has a good coherent flow.
    4) The word count cannot exceed 350 words.
    5) The text should have all the important points. And if words are replaced by simpler terms it is good to connect them to original words by referencing them using brackets.
    6) Ensure the text is factually correct this includes definitions, synonyms, important numeric figures and findings.
    """

    # Prompt B: For Gemini & LLaMA
    prompt_b = f"""
    You are a biology teacher in a high school and want to teach students in 10th grade about a research study. Your goal is to convey the information in the abstract in plain and easy to understand language that students can follow.
    You decide to generate a plain text for the same abstract keeping in mind what makes a text simple and easy to understand.
    Write a plain text summary such that it attempts to avoid as much scientific jargon as possible. If it cannot avoid it, then it replaces it with easy to understand synonyms.
    It has explanation and definition for complex biological terms  and can include simple real-life examples to make it easier to understand.
    The sentence structure of the summary is simple and the text has a good coherent flow. The summary should cover all the important details from the abstract. And if words are replaced by simpler terms it is good to connect them to original words by referencing them using brackets.
    Ensure the text is factually correct this includes definitions, synonyms, important numeric figures and findings.
    Furthermore, do not use bullet list within the summary.
    Summary should also not be structured in a question and answer format.
    The word count for the generated summary must not exceed 350 words.
    Do not use numbered list format in the summary to explain meaning of jargons, research methodology, and findings of the study. It negatively impacts the readability of the summary.
    Lastly, produce only the summary. Do not add any additional analysis, conclusions, findings or comments on its generation in the end.
    """

    # Get agent name/model to choose prompt
    agent_name = agent.model.lower()  # Assuming each agent has a `.model` attribute

    if "gpt" in agent_name or "mistral" in agent_name:
        chosen_prompt = prompt_a
    elif "gemini" in agent_name or "llama" in agent_name:
        chosen_prompt = prompt_b
    else:
        raise ValueError(f"Unknown agent type for model: {agent.model}")

    # Combine with the abstract
    summary_context = [{
        "role": "user",
        "content": f"{chosen_prompt.strip()}\n\nAbstract: {abstract.strip()}"
    }]

    return agent.generate_answer(summary_context)



def feedback_summary_lay(summary, abstract, agent):

    feedback_categories = {
        "Definition Enhancement": "Consider adding or refining definitions of key terms to enhance clarity.",
        "Synonym Suggestions": "Identify terms where synonyms could be used to simplify language or clarify meaning.",
        "Analogy Addition": "Suggest places where analogies could help in understanding complex concepts.",
        "Detail Adjustment": "Point out areas that need more detail to improve understanding or areas that should be simplified.",
        "Simplification Needs": "Highlight sentences or terms that are overly complex and suggest simpler alternatives.",
        "Overall Coherence": "Evaluate how well the summary flows and whether it logically progresses from one point to another.",
        "Key Point Highlight": "Ensure all critical points from the abstract are clearly summarized, noting any omissions."
    }

    feedback_instructions = "\n".join([f"{category}: {description}" for category, description in feedback_categories.items()])

    feedback_prompt = f"""

      Task: Review the provided lay summary compared to the original abstract. Suggest improvements to make the summary more accessible and informative, using the following feedback categories as guidance:

      {feedback_instructions}

      Instructions:
      - For each feedback category, provide specific examples from the summary and propose constructive improvements.
      - Discuss why these changes or additions would enhance the understanding or appeal of the summary.

      Abstract:
      {abstract}

      Summary:
      {summary}
      """

    feedback_context = [{
        "role": "user",
        "content": feedback_prompt
    }]

    return agent.generate_answer(feedback_context)


def generate_summary_with_feedback_lay(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary based on the provided feedback.\n"
          f"Do not use numbered list format in the revised summary to explain meaning of jargons, research methodology, and findings of the study. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 400 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)



def generate_summary(abstract, agent, persona):
    persona = persona.lower()
    if persona == "lay":
        return generate_summary_lay(abstract, agent)
    elif persona == "premed":
        return generate_summary_premed(abstract, agent)
    elif persona == "researcher":
        return generate_summary_researcher(abstract, agent)
    elif persona == "expert":
        return generate_summary_expert(abstract, agent)
    else:
        raise ValueError(f"Unknown persona: {persona}")

def feedback_summary(summary, abstract, agent, persona):
    persona = persona.lower()
    if persona == "lay":
        return feedback_summary_lay(summary, abstract, agent)
    elif persona == "premed":
        return feedback_summary_premed(summary, abstract, agent)
    elif persona == "researcher":
        return feedback_summary_researcher(summary, abstract, agent)
    elif persona == "expert":
        return feedback_summary_expert(summary, abstract, agent)
    else:
        raise ValueError(f"Unknown persona: {persona}")

def generate_summary_with_feedback(last_summary, feedback_list, agent, persona):
    persona = persona.lower()
    if persona == "lay":
        return generate_summary_with_feedback_lay(last_summary, feedback_list, agent)
    elif persona == "premed":
        return generate_summary_with_feedback_premed(last_summary, feedback_list, agent)
    elif persona == "researcher":
        return generate_summary_with_feedback_researcher(last_summary, feedback_list, agent)
    elif persona == "expert":
        return generate_summary_with_feedback_expert(last_summary, feedback_list, agent)
    else:
        raise ValueError(f"Unknown persona: {persona}")
