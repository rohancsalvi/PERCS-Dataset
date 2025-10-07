############# EXPERT ################
def feedback_phase_1_error(summary, abstract, agent):
    prompt = f"""
    You are a scientific fact-checking expert.

    Audience: The summary is intended for experts who are from the same field as the study in the abstract.

    Task: Evaluate the summary for defintions or background information if added for the experts.
    Specifically identify issues using the following error types (do not change their definitions):
    - Background Information Error: Missing or misleading contextual information that affects overall understanding.
    - Definition Error: Inaccurate or missing definitions and explanations of key terms.
    - Synonym Error: Improper substitution of terms or concepts that changes meaning.

    Instructions:
    - Compare the summary with the abstract.
    - Review each sentence carefully and identify and list any errors using the three error categories.
    - Analyse the summary with respect to needs of an expert from the same domain as of the study.
    - If no error for a category exist, state problem as “None”.
    - Format your output clearly.

    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_2_error(summary, abstract, agent):
    prompt = f"""
    You are a scientific writing reviewer.

    Audience: The summary is intended for experts who are from the same field as the study in the abstract.

    Task: Check if the summary accurately reflects what the abstract says, and that it doesn’t leave out important facts or add conclusions that aren’t supported.
    Specifically identify issues using the following error types (do not change their definitions):
    - Entity Error: Errors in names, study parameters, dosages, or other factual details.
    - Contradiction Error: Logical inconsistencies or conflicts between the summary and the abstract.
    - Misinterpretation Error: Misrepresentation of the original meaning or intent of the abstract.
    - Omission Error: Exclusion of critical details that are present in the abstract.
    - Jumping to Conclusions Error: Unsupported generalizations or claims not entailed by the original abstract.

    Instructions:
    - Compare the summary to the abstract carefully.
    - Review each sentence carefully and identify where the summary misstates or leaves out important facts, or makes claims the abstract does not support.
    - Use the error categories exactly as listed and defined above.
    - Analyse the summary with respect to needs of an expert from the same domain as of the study.
    - If a category has no issues, write “None.”
    - Follow the output format below.

    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_3_error(summary, abstract, agent):
    prompt = f"""
    You are a scientific writing reviewer.

    Audience: The summary is intended for experts who are from the same field as the study in the abstract.

    Task: Evaluate whether the summary is clear, appropriately detailed, non-redundant, and suitable in tone for an expert audience.
    Specifically identify issues using the following error types (do not change their definitions):
    - Structure Error: Poor organization, formatting, or layout that reduces readability or clarity.
    - Persona Relevance Error: Language that is too technical or too simplified for the intended audience.
    - Hallucination Error: Introduction of fabricated or unsupported content not grounded in the abstract.
    - Redundanct information: Identify if there is redundancy in the summary.

    Instructions:
    - Read both the summary and the abstract carefully.
    - Use the error categories exactly as defined above to find problems in how the summary is written for domain experts.
    - Suggest improvements to simplify structure, remove unnecessary repetition, and to improve clarity.
    - If no issues are found in a category, write “None.”
    - Use the output format below for each error type.


    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

############# RESEARCHER ################
def feedback_phase_1_researcher(summary, abstract, agent):
    prompt = f"""
    You are a scientific fact-checking expert.

    Audience: The summary is intended for for researchers who are not specialists in the specific field of the study but who are familiar with general scientific methods and concepts.

    Task: Evaluate the summary for defintions or background information added for the the researchers in the summary.
    Specifically identify issues using the following error types (do not change their definitions):
    - Background Information Error: Missing or misleading contextual information that affects overall understanding.
    - Definition Error: Inaccurate or missing definitions and explanations of key terms.
    - Synonym Error: Improper substitution of terms or concepts that changes meaning.

    Instructions:
    - Compare the summary with the abstract.
    - Review each sentence carefully and identify and list any errors using the three error categories.
    - Analyse the summary with respect to needs of a researcher from a non medical domain.
    - If no error for a category exist, state problem as “None”.
    - Format your output clearly.

    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_2_researcher(summary, abstract, agent):
    prompt = f"""
    You are a scientific writing reviewer.

    Audience: The summary is intended for for researchers who are not specialists in the specific field of the study but who are familiar with general scientific methods and concepts.

    Task: Check if the summary accurately reflects what the abstract says, and that it doesn’t leave out important facts or add conclusions that aren’t supported.
    Specifically identify issues using the following error types (do not change their definitions):
    - Entity Error: Errors in names, study parameters, dosages, or other factual details.
    - Contradiction Error: Logical inconsistencies or conflicts between the summary and the abstract.
    - Misinterpretation Error: Misrepresentation of the original meaning or intent of the abstract.
    - Omission Error: Exclusion of critical details that are present in the abstract.
    - Jumping to Conclusions Error: Unsupported generalizations or claims not entailed by the original abstract.

    Instructions:
    - Compare the summary to the abstract carefully.
    - Review each sentence carefully and identify where the summary misstates or leaves out important facts, or makes claims the abstract does not support.
    - Use the error categories exactly as listed and defined above.
    - Analyse the summary with respect to needs of researchers with a general scientific background and not from medical domain.
    - If a category has no issues, write “None.”
    - Follow the output format below.

    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_3_researcher(summary, abstract, agent):
    prompt = f"""
    You are a scientific writing reviewer.

    Audience: The summary is intended for for researchers who are not specialists in the specific field of the study but who are familiar with general scientific methods and concepts.

    Task: Evaluate whether the summary is clear, appropriately detailed, non-redundant, and accessible for the researchers.
    Specifically identify issues using the following error types (do not change their definitions):
    - Structure Error: Poor organization, formatting, or layout that reduces readability or clarity.
    - Persona Relevance Error: Language that is too technical or too simplified for the intended audience.
    - Hallucination Error: Introduction of fabricated or unsupported content not grounded in the abstract.
    - Redundanct information: Identify if there is redundancy in the summary.

    Instructions:
    - Read both the summary and the abstract carefully.
    - Use the error categories exactly as defined above to find problems in how the summary is written for researchers from non-medical domains.
    - Suggest improvements to simplify structure, remove unnecessary repetition, and to improve clarity.
    - If no issues are found in a category, write “None.”
    - Use the output format below for each error type.


    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])


############# PREMED ################
def feedback_phase_1_premed(summary, abstract, agent):
    prompt = f"""
    You are a scientific fact-checking expert.

    Audience: The summary is intended for pre-med students.

    Task: Evaluate the summary for defintions or background information added for the pre-med students in the summary.
    Specifically identify issues using the following error types (do not change their definitions):
    - Background Information Error: Missing or misleading contextual information that affects overall understanding.
    - Definition Error: Inaccurate or missing definitions and explanations of key terms.
    - Synonym Error: Improper substitution of terms or concepts that changes meaning.

    Instructions:
    1. Carefully compare the summary with the abstract.
    2. For each sentence in the summary, check whether a pre-med student could understand the background and technical terms.
    3. Use the error categories exactly as defined above to identify problems.
    4. Suggest addition of background information, definition and synonyms if helpful to make the sentence more accessible to the pre-med students.
    5. If no problems are found in a category, write “None.”
    6. Follow the format below for each error category.


    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_2_premed(summary, abstract, agent):
    prompt = f"""
    You are a scientific writing reviewer.

    Audience:  The summary is intended for pre-med students.

    Task: Check if the summary accurately reflects what the abstract says, and that it doesn’t leave out important facts or add conclusions that aren’t supported.
    Specifically identify issues using the following error types (do not change their definitions):
    - Entity Error: Errors in names, study parameters, dosages, or other factual details.
    - Contradiction Error: Logical inconsistencies or conflicts between the summary and the abstract.
    - Misinterpretation Error: Misrepresentation of the original meaning or intent of the abstract.
    - Omission Error: Exclusion of critical details that are present in the abstract.
    - Jumping to Conclusions Error: Unsupported generalizations or claims not entailed by the original abstract.

    Instructions:
    - Compare the summary to the abstract carefully.
    - Review each sentence carefully and identify where the summary misstates or leaves out important facts, or makes claims the abstract does not support.
    - Use the error categories exactly as listed and defined above.
    - Analyse the summary with respect to the information needs and readability level for pre-med students.
    - If a category has no issues, write “None.”
    - Follow the output format below.

    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_3_premed(summary, abstract, agent):
    prompt = f"""
    You are a scientific writing reviewer.

    Audience: The summary is intended for pre-med students.

    Task: Evaluate whether the summary is clear, appropriately detailed, non-redundant, and easy to read for pre-med students.
    Specifically identify issues using the following error types (do not change their definitions):
    - Structure Error: Poor organization, formatting, or layout that reduces readability or clarity.
    - Persona Relevance Error: Language that is too technical or too simplified for the intended audience.
    - Hallucination Error: Introduction of fabricated or unsupported content not grounded in the abstract.
    - Redundanct information: Identify if there is redundancy in the summary.

    Instructions:
    - Read both the summary and the abstract carefully.
    - Use the error categories exactly as defined above to find problems in how the summary is written for the pre-med students.
    - Suggest improvements to simplify structure, remove unnecessary repetition, and to improve clarity.
    - If no issues are found in a category, write “None.”
    - Use the output format below for each error type.


    Output Format (repeat for each error type):
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])



############# LAYMAN ################

def feedback_phase_1_lay(summary, abstract, agent):
    prompt = f"""
    You are a science communication reviewer.

    Audience: The summary is intended for 10th-grade students with no background in medicine or scientific research.

    Task: Evaluate how well the summary helps students understand the basic background and key terms from the abstract. Use simple, accessible language to guide your evaluation.

    Specifically identify issues using the following error types (do not change their definitions):

    - Background Information Error: Missing or misleading contextual information that affects overall understanding.
    - Definition Error: Inaccurate or misleading definitions and explanations of key terms.
    - Synonym Error: Improper substitution of terms or concepts that changes meaning.

    Instructions:
    1. Carefully compare the summary with the abstract.
    2. For each sentence in the summary, check whether a 10th-grade student could understand the background and technical terms.
    3. Use the error categories exactly as defined above to identify problems.
    4. Suggest addition of background information, definition and synonyms if helpful to make the sentence more accessible to students.
    5. If no problems are found in a category, write “None.”
    6. Follow the format below for each error category.

    Output Format:
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])
def feedback_phase_2_lay(summary, abstract, agent):
    prompt = f"""
    You are a science fact-checking reviewer.

    Audience: The summary is written for 10th-grade students who do not have a medical or scientific background.

    Task: Check if the summary accurately reflects what the abstract says, and that it doesn’t leave out important facts or add conclusions that aren’t supported.

    Specifically identify issues using the following error types (do not change their definitions):

    - Entity Error: Errors in names, study parameters, dosages, or other factual details.
    - Contradiction Error: Logical inconsistencies or conflicts between the summary and the abstract.
    - Misinterpretation Error: Misrepresentation of the original meaning or intent of the abstract.
    - Omission Error: Exclusion of critical details that are present in the abstract.
    - Jumping to Conclusions Error: Unsupported generalizations or claims not entailed by the original abstract.

    Instructions:
    1. Compare the summary to the abstract carefully.
    2. Identify where the summary misstates or leaves out important facts, or makes claims the abstract does not support.
    3. Use the error categories exactly as listed and defined above.
    4. Suggest simple, clear rewrites if possible to help 10th-grade students better understand.
    5. If a category has no issues, write “None.”
    6. Follow the output format below.

    Output Format:
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])

def feedback_phase_3_lay(summary, abstract, agent):
    prompt = f"""
    You are a science writing reviewer.

    Audience: The summary is written for 10th-grade students with no prior knowledge of scientific or medical topics.

    Task: Evaluate whether the summary is easy to read, free of added or repeated content, and written in a clear, student-friendly structure.

    Specifically identify issues using the following error types (do not change their definitions):

    - Structure Error: Poor organization, formatting, or layout that reduces readability or clarity.
    - Persona Relevance Error: Language that is too technical or too simplified for the intended audience.
    - Hallucination Error: Introduction of fabricated or unsupported content not grounded in the abstract.
    - Redundant Information: Identify if there is redundancy in the summary.

    Instructions:
    1. Read both the summary and the abstract carefully.
    2. Use the error categories exactly as defined above to find problems in how the summary is written for high school students.
    3. Suggest improvements to simplify structure, remove unnecessary repetition, or improve clarity.
    4. If no issues are found in a category, write “None.”
    5. Use the output format below for each error type.

    Output Format:
    [Error Type]
    - Problem:
    - Evidence from Abstract:
    - Problematic Summary Segment:
    - Explanation:

    Abstract:
    {abstract}

    Summary:
    {summary}
    """
    return agent.generate_answer([{"role": "user", "content": prompt}])




ERROR_FEEDBACK_PHASES = {
    "expert": [
        feedback_phase_1_error,
        feedback_phase_2_error,
        feedback_phase_3_error
    ],
    "researcher": [
        feedback_phase_1_researcher,
        feedback_phase_2_researcher,
        feedback_phase_3_researcher
    ],
    "premed": [
        feedback_phase_1_premed,
        feedback_phase_2_premed,
        feedback_phase_3_premed
    ],
    "lay": [
        feedback_phase_1_lay,
        feedback_phase_2_lay,
        feedback_phase_3_lay
    ],
}
