def is_refinement_sufficient_expert(original, initial, refined, agent) -> bool:
    query_text = (
        "You are a seasoned subject matter expert in biology and medicine evaluating a revised research summary for an expert audience.\n\n"
        "Abstract:\n"
        f"{original}\n\n"
        "Initial Summary:\n"
        f"{initial}\n\n"
        "Refined Summary:\n"
        f"{refined}\n\n"
        "Assess whether the refined summary:\n"
        "- Uses field-appropriate scientific language without oversimplification.\n"
        "- Retains methodological detail, relevant numerical figures, and results.\n"
        "- Maintains a logical narrative from background through findings.\n"
        "- Uses paragraph form only (no lists or Q&A formats).\n"
        "- Stays under 250 words.\n"
        "- Is scientifically rigorous and factually accurate.\n"
        "- Summary does not add any additional information that is not entailed by the abstract.\n"
        "- Contains only the summary. Does not add commentary, what has been changed, interpretation, or meta-level notes on the summarization process.\n\n"
        "If the refined summary meets all these requirements, reply only with 'sufficient'. Otherwise, explain what needs to be improved."
    )

    response = agent.generate_answer([{"role": "system", "content": query_text}])

    if response is not None:
        return "sufficient" in response.lower()
    else:
        return False

def self_refine_summary_expert(text: str, agent,max_rounds) -> str:
    prompt = (
        f"You are a seasoned subject matter expert in biology and medicine. You are preparing a summary of a research abstract for an expert audience in the same field.\n\n"
        f"Abstract:\n{text}\n\n"
        f"Guidelines:\n"
        f"- Write a structured summary using field-appropriate language and avoid simplifying key scientific concepts or vocabulary.\n"
        f"- The summary should retain methodological details, include relevant numerical figures, and results.\n"
        f"- Maintain an academic tone and a coherent, logically structured narrative that flows naturally from background to findings.\n"
        f"- Do not use bullet points, question-answer format, or numbered lists. The summary should be written as continuous prose.\n"
        f"- The content must remain scientifically rigorous and factually accurate in all terminology, methods, results, and findings.\n"
        f"- The summary must not exceed 250 words.\n"
        f"- Produce only the summary. Do not add commentary, interpretation, or meta-level notes on the summarization process.\n"
    )

    answer = agent.generate_answer([
        {"role": "system", "content": "You are a subject matter expert in biology writing for an expert audience."},
        {"role": "user", "content": prompt}
    ])

    refinement_counter = 0
    while refinement_counter < max_rounds:
        feedback_prompt = (
            f"You are reviewing the following summary intended for a professional experts audience from the same field of the study:\n\n"
            f"{answer}\n\n"
            "Evaluate whether it:\n"
            "- Uses domain-specific language without oversimplifying key concepts.\n"
            "- Retains essential methodological details, relevant numerical data and results.\n"
            "- Maintains paragraph-only structure and is under 250 words.\n"
            "- Summary does not add any additional information that is not entailed by the abstract.\n"
            "- Is scientifically accurate in terminology, methods, results, and findings.\n"
            "Provide constructive feedback to improve clarity, completeness, and factual accuracy for an expert reader."
        )

        feedback = agent.generate_answer([
            {"role": "system", "content": "You are an expert reviewer of scientific summaries in biology."},
            {"role": "user", "content": feedback_prompt}
        ])

        refiner_prompt = (
            f"Revise the summary using the feedback below.\n\n"
            f"Feedback:\n{feedback}\n\n"
            f"Current Summary:\n{answer}\n\n"
            f"Ensure the revised summary aligns with expert-level expectations and meets all requirements listed earlier."
        )

        refined = agent.generate_answer([
            {"role": "system", "content": "You are a scientific editor refining a research summary for expert readers."},
            {"role": "user", "content": refiner_prompt}
        ])

        if is_refinement_sufficient_expert(text, answer, refined, agent):
            return refined

        answer = refined
        refinement_counter += 1

    return answer


########################## RESEARCHER  #######################################


def is_refinement_sufficient_researcher(original, initial, refined, agent) -> bool:

    query_text = (
    "You are a science communication expert evaluating a revised research summary intended for researchers with a general scientific background, but who are not specialists in the specific field of the abstract.\n\n"
    f"Abstract:\n{original}\n\n"
    f"Initial Summary:\n{initial}\n\n"
    f"Refined Summary:\n{refined}\n\n"
    "Evaluate whether the refined summary:\n"
    "- Uses clear, precise, and scientifically accurate language suitable for a non-specialist research audience.\n"
    "- Accurately presents essential methods, findings,results, and any relevant quantitative data from the abstract.\n"
    "- Follows a coherent, well-structured paragraph format only (no lists or Q&A).\n"
    "- Remains under 350 words.\n"
    "- Avoids introducing information not supported by or inferable from the original abstract.\n"
    "- Includes only the summary itself, with no meta-commentary, interpretation, or explanation of changes.\n\n"
    "If the refined summary meets all these criteria, reply with 'sufficient'. Otherwise, explain what still needs improvement."
    )

    response = agent.generate_answer([{"role": "system", "content": query_text}])

    if response is not None:
        return "sufficient" in response.lower()
    else:
        return False

def self_refine_summary_researcher(text: str, agent,max_rounds) -> str:
    prompt = (
        f"You are a knowledgeable science communicator summarizing a scientific abstract for an audience of researchers who are not specialists in the specific field of the study, but who are familiar with general scientific methods and concepts.\n\n"
        f"Abstract:\n{text}\n\n"
        f"Guidelines:\n"
        f"- Uses clear and accessible language, avoiding heavy jargon. When domain specific terms are essential, include a short, simple explanation.\n"
        f"- Maintains an informative and professional tone without sounding overly technical or overly simplified.\n"
        f"- Explains the study’s key findings, methods, and results.\n"
        f"- Do not use bullet points, numbered lists, or Q&A formats. Write in well-structured, paragrapgh format.\n"
        f"- The summary must not exceed 350 words.\n"
        f"- Do not include any concluding commentary for the researchers, notes on the summarization process, or any self-determined importance of the study.\n"
        f"- Do not include a list of changes made to the summary.\n"
    )


    answer = agent.generate_answer([
        {"role": "system", "content": "You are a knowledgeable science communicator summarizing a scientific abstract for an audience of researchers who are not specialists in the specific field of the study, but who are familiar with general scientific methods and concepts."},
        {"role": "user", "content": prompt}
    ])

    refinement_counter = 0
    while refinement_counter < max_rounds:
        feedback_prompt = (
            f"You are reviewing the following summary written for pre-med students based on a research abstract:\n\n"
            f"{answer}\n\n"
            "Evaluate whether it:\n"
             "- Is the language clear and suitable for students with basic biology and chemistry knowledge?\n"
             "- Are key methods, findings, and relevant data accurately and concisely presented?\n"
             "- Are technical terms used appropriately and explained when needed?\n"
            "- Is the summary written as a paragragh (no lists) and under 350 words?\n"
            "- Summary does not add any additional information that is not entailed by the abstract.\n"
            "- Is scientifically accurate in terminology, methods, results, and findings.\n"
            "Provide constructive feedback to improve clarity, completeness, and factual accuracy for pre-med students."
        )

        feedback_prompt = (
        f"You are reviewing the following summary written for researchers who are not specialists in the specific field of the study but who are familiar with general scientific methods and concepts:\n\n"
        f"{answer}\n\n"
        "Evaluate whether it:\n"
        "- Uses clear and accessible language, avoiding heavy jargon, and explains domain specific terms briefly when necessary.\n"
        "- Maintains a professional tone suitable for a research-informed audience without oversimplification.\n"
        "- Clearly and concisely presents the study’s key methods, findings, and results.\n"
        "- Is written as a well-structured paragraph (no lists or Q&A formats) and is under 350 words.\n"
        "- Does not include any information not present or implied in the original abstract.\n"
        "- Is scientifically accurate in its terminology, methods, and reported results.\n"
        "Provide constructive feedback to improve clarity, completeness,and factual accuracy for scientifically informed researchers outside the medical domain."
    )

        feedback = agent.generate_answer([
            {"role": "system", "content": "You are a science communication expert who specializes in evaluating and refining research summaries for interdisciplinary scientific audiences."},
            {"role": "user", "content": feedback_prompt}
        ])

        refiner_prompt = (
            f"Revise the summary using the feedback below.\n\n"
            f"Feedback:\n{feedback}\n\n"
            f"Current Summary:\n{answer}\n\n"
            f"Ensure the revised summary aligns with the expectations for researchers with a general scientific background, and follows all previously listed guidelines."
        )

        refined = agent.generate_answer([
            {"role": "system", "content": "You are a science communication expert refining a summary of a scientific abstract for researchers with a general scientific background who are not specialists in the study’s specific field."},
            {"role": "user", "content": refiner_prompt}
        ])

        if is_refinement_sufficient_researcher(text, answer, refined, agent):
            return refined

        answer = refined
        refinement_counter += 1

    return answer


############################## PRE-MED ######################################
def is_refinement_sufficient_premed(original, initial, refined, agent) -> bool:

    query_text = (
        "You are a subject matter expert in medical and biological sciences evaluating a revised research summary intended for pre-med students.\n\n"
        f"Abstract:\n{original}\n\n"
        f"Initial Summary:\n{initial}\n\n"
        f"Refined Summary:\n{refined}\n\n"
        "Evaluate whether the refined summary:\n"
        "- Uses clear, scientifically accurate language appropriate for students with basic biology and chemistry knowledge.\n"
        "- Retains essential methodological details, results, and relevant quantitative data from the abstract.\n"
        "- Follows a coherent structure in paragraph format only (no lists or Q&A).\n"
        "- Remains under 350 words.\n"
        "- Avoids adding information not supported by the abstract.\n"
        "- Contains only the summary, with no meta-commentary, interpretation, or notes on changes.\n\n"
        "If the refined summary meets all these criteria, reply with 'sufficient'. Otherwise, explain what still needs improvement."
    )

    response = agent.generate_answer([{"role": "system", "content": query_text}])

    if response is not None:
        return "sufficient" in response.lower()
    else:
        return False

def self_refine_summary_premed(text: str, agent,max_rounds) -> str:
    prompt = (
        f"You are an experienced academic tutor in the medical sciences. Your task is to write a summary of a research abstract specifically for pre-med students.\n\n"
        f"Abstract:\n{text}\n\n"
        f"Guidelines:\n"
        f"- Write a clear and accessible summary using language suitable for students with basic knowledge of biology and chemistry.\n"
        f"- Avoid heavy technical jargon. When specialized terms are necessary, briefly explain them in simple words.\n"
        f"- Ensure the summary accurately conveys the study’s key findings, methodology, and relevance to medical sciences.\n"
        f"- Present the information in a logical, instructional tone that supports student learning and comprehension.\n"
        f"- Where possible in the summary, connect the research to foundational pre-med topics such as anatomy, physiology, or biochemistry.\n"
        f"- Do not use bullet points, numbered lists, or Q&A formats. Write in well-structured, paragrapgh format.\n"
        f"- The summary must not exceed 350 words.\n"
        f"- Do not include any concluding commentary for the students, notes on the summarization process, or any self-determined importance of the study.\n"
        f"- Do not include a list of changes made to the summary.\n"
    )

    answer = agent.generate_answer([
        {"role": "system", "content": "You are an experienced academic tutor in the medical sciences writing for a pre-med student audience"},
        {"role": "user", "content": prompt}
    ])

    refinement_counter = 0
    while refinement_counter < max_rounds:
        feedback_prompt = (
            f"You are reviewing the following summary written for pre-med students based on a research abstract:\n\n"
            f"{answer}\n\n"
            "Evaluate whether it:\n"
             "- Is the language clear and suitable for students with basic biology and chemistry knowledge?\n"
             "- Are key methods, findings, and relevant data accurately and concisely presented?\n"
             "- Are technical terms used appropriately and explained when needed?\n"
            "- Is the summary written as a paragragh (no lists) and under 350 words?\n"
            "- Summary does not add any additional information that is not entailed by the abstract.\n"
            "- Is scientifically accurate in terminology, methods, results, and findings.\n"
            "Provide constructive feedback to improve clarity, completeness, and factual accuracy for pre-med students."
        )

        feedback = agent.generate_answer([
            {"role": "system", "content": "You are an academic reviewer of scientific summaries for pre-med students."},
            {"role": "user", "content": feedback_prompt}
        ])

        refiner_prompt = (
            f"Revise the summary using the feedback below.\n\n"
            f"Feedback:\n{feedback}\n\n"
            f"Current Summary:\n{answer}\n\n"
            f"Ensure the revised summary aligns with pre-med student expectations and meets all requirements listed earlier."
        )

        refined = agent.generate_answer([
            {"role": "system", "content": "You are an academic tutor in medical sciences refining a summary of a research abstract for pre-med student readers."},
            {"role": "user", "content": refiner_prompt}
        ])

        if is_refinement_sufficient_premed(text, answer, refined, agent):
            return refined

        answer = refined
        refinement_counter += 1

    return answer




############################# LAYMAN ##########################################

def is_refinement_sufficient_layman(original, initial, refined, agent) -> bool:
    query_text = (
        "You are a high school biology teacher evaluating a summary meant for 10th-grade students.\n\n"
        "Abstract:\n"
        f"{original}\n\n"
        "Initial Summary:\n"
        f"{initial}\n\n"
        "Refined Summary:\n"
        f"{refined}\n\n"
        "Assess whether the refined summary:\n"
        "- Avoids complex scientific jargon OR explains it clearly using simpler terms in parentheses.\n"
        "- Includes clear definitions for any advanced biology terms, and uses relatable real-life examples if helpful.\n"
        "- Covers all key points and findings from the original research, including important numbers or results.\n"
        "- Is written in plain paragraph form only (no lists or question-answer format).\n"
        "- Stays under 350 words.\n"
        "- Maintains factual accuracy in definitions, terms, and findings.\n\n"
        "If the refined summary meets all these requirements, reply only with 'sufficient'. Otherwise, explain what needs to be improved."
    )

    response = agent.generate_answer([{"role": "system", "content": query_text}])

    if response is not None:
        return "sufficient" in response.lower()
    else:
        #print("Warning: agent.generate_answer returned None. Assuming refinement is not sufficient.")
        return False

def self_refine_summary_layman(text: str, agent,max_rounds) -> str:
    prompt = (
        f"You are a high school biology teacher summarizing a research study for 10th-grade students.\n\n"
        f"Please write a clear and engaging paragraph-style summary of the following text:\n\n{text}\n\n"
        f"Guidelines:\n"
        f"- Use simple language and avoid complex scientific jargon as much as possible.\n"
        f"- If scientific terms must be used, provide easy-to-understand explanations or synonyms in parentheses.\n"
        f"- Include all important details, including key results and numbers from the original text.\n"
        f"- Use real-life examples when helpful to explain concepts.\n"
        f"- Do not use lists, bullet points, or question-and-answer formats. Only use full sentences in paragraph form.\n"
        f"- Keep the summary under 350 words.\n"
        f"- Ensure the explanation is factually correct, especially when defining terms or describing findings."
    )

    answer = agent.generate_answer([
        {"role": "system", "content": "You are a high school biology teacher summarizing science for 10th-grade students."},
        {"role": "user", "content": prompt}
    ])

    refinement_counter = 0
    while refinement_counter < max_rounds:
        feedback_prompt = (
            f"Evaluate the following summary as if you are a high school biology teacher preparing material for 10th-grade students:\n\n"
            f"{answer}\n\n"
            "Does it:\n"
            "- Use plain language and avoid or explain scientific jargon?\n"
            "- Clearly define complex biological terms and include examples?\n"
            "- Cover all key details and important findings accurately?\n"
            "- Maintain paragraph-only format and stay under 350 words?\n"
            "Give constructive feedback to improve readability and factual accuracy for this audience."
        )

        feedback = agent.generate_answer([
            {"role": "system", "content": "You are an expert in simplifying biology for high school students."},
            {"role": "user", "content": feedback_prompt}
        ])

        refiner_prompt = (
            f"Revise the summary using the feedback below.\n\n"
            f"Feedback:\n{feedback}\n\n"
            f"Current Summary:\n{answer}\n\n"
            f"Ensure the revised summary is engaging, easy to understand for 10th graders, and meets all the listed requirements."
        )

        refined = agent.generate_answer([
            {"role": "system", "content": "You are a skilled editor refining science content for high school students."},
            {"role": "user", "content": refiner_prompt}
        ])

        if is_refinement_sufficient_layman(text, answer, refined, agent):
            return refined

        answer = refined
        refinement_counter += 1

    return answer



def self_refine_summary(text, persona, agent, max_rounds=3):
    """
    Dispatcher: Calls the correct self-refine function based on persona.
    """
    persona = persona.lower()
    if persona == "expert":
        return self_refine_summary_expert(text, agent, max_rounds)
    elif persona == "researcher":
        return self_refine_summary_researcher(text, agent, max_rounds)
    elif persona == "premed":
        return self_refine_summary_premed(text, agent, max_rounds)
    elif persona == "layman":
        return self_refine_summary_layman(text, agent, max_rounds)
    else:
        raise ValueError(f"Unknown persona: {persona}")