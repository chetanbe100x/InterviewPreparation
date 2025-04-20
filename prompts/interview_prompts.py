"""
Prompt templates for the interview preparation framework.
"""

class InterviewPrompts:
    """
    Collection of prompt templates for the interview preparation framework.
    """

    @staticmethod
    def company_research_prompt(company_name):
        """
        Generate a prompt for researching a company.

        Args:
            company_name (str): The name of the company to research.

        Returns:
            str: The generated prompt.
        """
        return f"""
        You are a professional company researcher. Provide concise information about {company_name} for interview preparation.

        Include:
        1. Brief company overview: history, industry, main products/services
        2. Company culture and values (key points only)
        3. Recent news or developments (1-2 most relevant items)
        4. Interview approach and hiring process (if known)
        5. Key challenges or opportunities

        Keep your response brief and focused on the most important information for interview preparation.
        """

    @staticmethod
    def role_analysis_prompt(role, company_name, experience_level):
        """
        Generate a prompt for analyzing a job role.

        Args:
            role (str): The job role to analyze.
            company_name (str): The name of the company.
            experience_level (str): The experience level of the candidate.

        Returns:
            str: The generated prompt.
        """
        return f"""
        You are a career advisor specializing in the tech industry. Provide a concise analysis of the {role} role at {company_name} for a candidate with {experience_level} experience.

        Include:
        1. Key responsibilities (3-5 most important)
        2. Essential technical skills (most critical only)
        3. Important soft skills (top 3)
        4. Brief career progression insights
        5. How this role fits in the organization
        6. Specific skills that {company_name} might value

        Keep your response brief and focused on the most important information for interview preparation.
        """

    @staticmethod
    def interview_questions_prompt(role, company_name, experience_level, company_info="", role_info=""):
        """
        Generate a prompt for creating interview questions.

        Args:
            role (str): The job role.
            company_name (str): The name of the company.
            experience_level (str): The experience level of the candidate.
            company_info (str): Information about the company.
            role_info (str): Information about the role.

        Returns:
            str: The generated prompt.
        """
        # Truncate company_info and role_info if they're too long to avoid timeout issues
        if company_info and len(company_info) > 2000:
            company_info = company_info[:2000] + "... (truncated)"
        if role_info and len(role_info) > 2000:
            role_info = role_info[:2000] + "... (truncated)"

        return f"""
        You are an experienced technical interviewer at {company_name}. Your task is to create interview questions for a {role} position for a candidate with {experience_level} experience.

        Company Information (brief):
        {company_info}

        Role Information (brief):
        {role_info}

        Create 10 interview questions in these categories:

        1. Technical Skills (4 questions)
           - Questions that assess technical knowledge relevant to the {role} position
           - Tailored to {experience_level} experience level

        2. Problem-Solving (2 questions)
           - Questions that evaluate ability to solve problems
           - Relevant to {company_name} and the {role} position

        3. Behavioral/Situational (2 questions)
           - Questions about how the candidate handled past situations
           - Focus on company culture and values

        4. Company/Role-Specific (2 questions)
           - Questions specific to {company_name} and the {role}
           - Assess fit for the role and company

        For each question, provide:
        1. The question itself
        2. What the interviewer is looking for
        3. A sample strong answer

        Format as a structured interview guide.
        """

    @staticmethod
    def feedback_prompt(candidate_answer, question, ideal_answer):
        """
        Generate a prompt for providing feedback on a candidate's answer.

        Args:
            candidate_answer (str): The candidate's answer.
            question (str): The interview question.
            ideal_answer (str): The ideal answer to the question.

        Returns:
            str: The generated prompt.
        """
        return f"""
        You are an expert interview coach. Your task is to provide constructive feedback on a candidate's answer to an interview question.

        Question:
        {question}

        Candidate's Answer:
        {candidate_answer}

        Ideal Answer Components:
        {ideal_answer}

        Please provide feedback on the candidate's answer, including:
        1. Strengths of the answer
        2. Areas for improvement
        3. Specific suggestions to make the answer stronger
        4. A rating from 1-10 on how effective the answer is

        Format your response as constructive, actionable feedback that will help the candidate improve.
        """
