##################### EXPERT #######################
def detect_errors_expert(summary, abstract, agent):

    error_categories = {
        "Background Information Error": "Missing or misleading contextual information that affects overall understanding.",
        "Definition Error": "Inaccurate or misleading definitions and explanations of key terms.",
        "Synonym Error": "Improper substitution of terms or concepts that changes meaning.",
        "Entity Error": "Errors in names, study parameters, dosages, or other factual details.",
        "Contradiction Error": "Logical inconsistencies or conflicts between the summary and the abstract.",
        "Misinterpretation Error": "Misrepresentation of the original meaning or intent of the abstract.",
        "Omission Error": "Exclusion of critical details that are present in the abstract.",
        "Jumping to Conclusions Error": "Unsupported generalizations or claims not entailed by the original abstract.",
        "Structure Error": "Poor organization, formatting, or layout that reduces readability or clarity.",
        "Persona Relevance Error": "Language that is too technical or too simplified for the intended audience.",
        "Hallucination Error": "Introduction of fabricated or unsupported content not grounded in the abstract."
      }


    error_categories_text = "\n".join([f"{category}: {description}" for category, description in error_categories.items()])

    error_prompt = f"""
      Role: Expert Content Analyst

      Task: Carefully compare the provided summary to the original abstract. The summary is intended for experts who are from the same field as the study in the abstract.
      Review each sentence carefully and identify and list any errors using the following error categories as a guide:

      {error_categories_text}

      Instructions:
      - For each error category, provide specific examples from the summary that deviate from or misrepresent the abstract.
      - Explain why these discrepancies lead to an error based on the definitions provided.
      - Consider the expectations of an audience who are experts from the same domain as of the study.
      - For 'Persona Relevance Error', assess whether the summary uses the correct level of readability in terms of technical detail and assumes a suitable level of domain knowledge for experts.
      - Highlight any omissions of key findings, methods, or data that an expert would reasonably expect to see.
      - Identify any hallucinated content not grounded in the abstract or accepted medical/scientific knowledge.
      - Highlight any redundancy in the summary that should be removed.

      Abstract:
      {abstract}

      Summary:
      {summary}
      """

    error_context = [{
        "role": "user",
        "content": error_prompt
    }]

    return agent.generate_answer(error_context)



def generate_summary_with_feedback_expert(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary for domain experts from the field of study, based on the feedback provided below.\n"
          f"Do not use numbered list format in the revised summary. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 250 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)
##################### PREMED #######################
def detect_errors_premed(summary, abstract, agent):

    error_categories = {
        "Background Information Error": "Missing or misleading contextual information that affects overall understanding.",
        "Definition Error": "Inaccurate or misleading definitions and explanations of key terms.",
        "Synonym Error": "Improper substitution of terms or concepts that changes meaning.",
        "Entity Error": "Errors in names, study parameters, dosages, or other factual details.",
        "Contradiction Error": "Logical inconsistencies or conflicts between the summary and the abstract.",
        "Misinterpretation Error": "Misrepresentation of the original meaning or intent of the abstract.",
        "Omission Error": "Exclusion of critical details that are present in the abstract.",
        "Jumping to Conclusions Error": "Unsupported generalizations or claims not entailed by the original abstract.",
        "Structure Error": "Poor organization, formatting, or layout that reduces readability or clarity.",
        "Persona Relevance Error": "Language that is too technical or too simplified for the intended audience.",
        "Hallucination Error": "Introduction of fabricated or unsupported content not grounded in the abstract."
      }


    error_categories_text = "\n".join([f"{category}: {description}" for category, description in error_categories.items()])

    error_prompt = f"""
      Role: Expert Content Analyst

      Task: Carefully compare the provided summary to the original abstract. The summary is intended for pre-med students.
      Review each sentence carefully and identify and list any errors using the following error categories as a guide:

      {error_categories_text}

      Instructions:
      - For each error category, provide specific examples from the summary that deviate from or misrepresent the abstract.
      - Explain why these discrepancies lead to an error based on the definitions provided.
      - Consider the expectations of an audience who are pre-med students.
      - For 'Persona Relevance Error', assess whether the summary uses the correct level of readability through simplification and assumes a suitable level of basic domain knowledge for pre-med students.
      - Highlight any omissions of key findings, methods, or data that a pre-med would reasonably need to understand the abstract.
      - Check for any redundant information, complex sentence, or unnecessary medical details that are not appropriate at pre-med students level in a summary.
      - Identify any hallucinated content not grounded in the abstract or accepted medical/scientific knowledge.

      Abstract:
      {abstract}

      Summary:
      {summary}
      """

    error_context = [{
        "role": "user",
        "content": error_prompt
    }]

    return agent.generate_answer(error_context)


def generate_summary_with_feedback_premed(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary intended for pre-med students, based on the feedback provided below.\n"
          f"Do not use numbered list format in the revised summary. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 350 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)
##################### RESEARCHER #######################
def detect_errors_researcher(summary, abstract, agent):

    error_categories = {
        "Background Information Error": "Missing or misleading contextual information that affects overall understanding.",
        "Definition Error": "Inaccurate or misleading definitions and explanations of key terms.",
        "Synonym Error": "Improper substitution of terms or concepts that changes meaning.",
        "Entity Error": "Errors in names, study parameters, dosages, or other factual details.",
        "Contradiction Error": "Logical inconsistencies or conflicts between the summary and the abstract.",
        "Misinterpretation Error": "Misrepresentation of the original meaning or intent of the abstract.",
        "Omission Error": "Exclusion of critical details that are present in the abstract.",
        "Jumping to Conclusions Error": "Unsupported generalizations or claims not entailed by the original abstract.",
        "Structure Error": "Poor organization, formatting, or layout that reduces readability or clarity.",
        "Persona Relevance Error": "Language that is too technical or too simplified for the intended audience.",
        "Hallucination Error": "Introduction of fabricated or unsupported content not grounded in the abstract."
      }


    error_categories_text = "\n".join([f"{category}: {description}" for category, description in error_categories.items()])

    error_prompt = f"""
      Role: Expert Content Analyst

      Task: Carefully compare the provided summary to the original abstract. The summary is intended for researchers with a general scientific background, but who are not specialists in the specific field of the abstract.
      Review each sentence carefully and identify and list any errors using the following error categories as a guide:

      {error_categories_text}

      Instructions:
      - For each error category, provide specific examples from the summary that deviate from or misrepresent the abstract.
      - Explain why these discrepancies lead to an error based on the definitions provided.
      - Consider the expectations of an audience who are researchers, not specialists in the specific field of the study in the abstract.
      - For 'Persona Relevance Error', assess whether the summary uses the correct level of readability in terms of technical detail for researchers with a general scientific background.
      - Highlight any omissions of key findings, methods, or data that an researcher would reasonably expect to see in a research study summary.
      - Highlight redundant or overly specific details that may not be suitable for researchers from other fields.
      - Identify any hallucinated content not grounded in the abstract or accepted medical/scientific knowledge.

      Abstract:
      {abstract}

      Summary:
      {summary}
      """

    error_context = [{
        "role": "user",
        "content": error_prompt
    }]

    return agent.generate_answer(error_context)


def generate_summary_with_feedback_researcher(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary intended for researchers with a general scientific background, but who are not specialists in the specific field of the abstract, based on the feedback provided below.\n"
          f"Do not use numbered list format in the revised summary. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 350 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)
##################### LAYMAN #######################

def detect_errors_lay(summary, abstract, agent):

    error_categories = {
        "Background Information Error": "Missing or misleading contextual information that affects overall understanding.",
        "Definition Error": "Inaccurate or misleading definitions and explanations of key terms.",
        "Synonym Error": "Improper substitution of terms or concepts that changes meaning.",
        "Entity Error": "Errors in names, study parameters, dosages, or other factual details.",
        "Contradiction Error": "Logical inconsistencies or conflicts between the summary and the abstract.",
        "Misinterpretation Error": "Misrepresentation of the original meaning or intent of the abstract.",
        "Omission Error": "Exclusion of critical details that are present in the abstract.",
        "Jumping to Conclusions Error": "Unsupported generalizations or claims not entailed by the original abstract.",
        "Structure Error": "Poor organization, formatting, or layout that reduces readability or clarity.",
        "Persona Relevance Error": "Language that is too technical or too simplified for the intended audience.",
        "Hallucination Error": "Introduction of fabricated or unsupported content not grounded in the abstract."
      }


    error_categories_text = "\n".join([f"{category}: {description}" for category, description in error_categories.items()])

    error_prompt = f"""
      Role: Expert Content Analyst

      Task: Carefully compare the provided summary to the original abstract. The summary is intended for 10th grade students. The goal is to convey the information in the abstract in plain and easy to understand language that students can follow.
      Review each sentence carefully and identify and list any errors using the following error categories as a guide:


      {error_categories_text}

      Instructions:
      - For each error category, provide specific examples from the summary that deviate from or misrepresent the abstract.
      - Explain why these discrepancies lead to an error based on the definitions provided.
      - Consider the expectations of an audience who are 10th grade students.
      - For 'Persona Relevance Error', assess whether the summary uses the correct level of readability through simplification and by employing simple sentences to make it easy to understand for students.
      - For 'Structure Error', look for sentence sequencing, paragraph flow, or transitions that reduce clarity for the target audience.
      - Highlight any omissions of key details that would hinder students from understanding the research study summary.
      - Check for any redundant information, complex sentences, or unnecessary medical details that are not appropriate for a 10th-grade student.
      - Identify any hallucinated content not grounded in the abstract or accepted medical/scientific knowledge.
      - If possible, suggest a clearer or simpler alternative for any sentence that is difficult to understand for students.

      Abstract:
      {abstract}

      Summary:
      {summary}
      """

    error_context = [{
        "role": "user",
        "content": error_prompt
    }]

    return agent.generate_answer(error_context)


def generate_summary_with_feedback_lay(last_summary, feedback_list, agent):

    feedback = "\n\n".join(feedback_list)

    feedback_and_refine_context = [{
        "role": "user",
        "content": (
          f"Refine the following summary based on the provided feedback.\n"
          f"Do not use numbered list format in the revised summary. It negatively impacts the readability of the summary.\n"
          f"Ensure that the revised summary is no more than 400 words:\n\n"
          f"Summary:\n{last_summary}\n\n"
          f"Feedback:\n{feedback}"
      )
    }]

    return agent.generate_answer(feedback_and_refine_context)



def detect_errors(summary, abstract, agent, persona):
    persona = persona.lower()
    if persona == "expert":
        return detect_errors_expert(summary, abstract, agent)
    elif persona == "premed":
        return detect_errors_premed(summary, abstract, agent)
    elif persona == "researcher":
        return detect_errors_researcher(summary, abstract, agent)
    elif persona == "lay" or persona == "layman":
        return detect_errors_lay(summary, abstract, agent)
    else:
        raise ValueError(f"Unknown persona: {persona}")


def generate_summary_with_feedback_error(last_summary, feedback_list, agent, persona):
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
