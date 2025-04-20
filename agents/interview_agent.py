"""
Interview agent for the interview preparation framework.
Simplified version that doesn't rely on crewai.
"""
from prompts.interview_prompts import InterviewPrompts

class InterviewAgent:
    """
    Agent responsible for generating interview questions and answers.
    """

    def __init__(self, llm):
        """
        Initialize the interview agent.

        Args:
            llm: The language model to use for the agent.
        """
        self.llm = llm

    def get_interview_preparation_prompt(self):
        """
        Get the prompt for the interview preparation agent.

        Returns:
            str: The agent prompt.
        """
        return """You are a seasoned technical interviewer who has conducted thousands of
        interviews for top tech companies. You have a deep understanding of what makes a
        successful interview and can craft questions that accurately assess a candidate's
        skills and fit for a specific role and company."""

    def get_feedback_prompt(self):
        """
        Get the prompt for the feedback agent.

        Returns:
            str: The agent prompt.
        """
        return """You are an expert interview coach who has helped thousands of candidates
        improve their interview performance. You have a keen eye for identifying strengths and
        weaknesses in answers and can provide actionable feedback that helps candidates improve."""

    def generate_interview_questions(self, role, company_name, experience_level, company_info, role_info):
        """
        Generate interview questions and answers.

        Args:
            role (str): The job role.
            company_name (str): The name of the company.
            experience_level (str): The experience level of the candidate.
            company_info (str): Information about the company.
            role_info (str): Information about the role.

        Returns:
            str: Generated interview questions and answers.
        """
        prompt = InterviewPrompts.interview_questions_prompt(
            role, company_name, experience_level, company_info, role_info
        )

        # For now, we'll use the LLM directly instead of the agent
        # In a future implementation, we'll use the agent with tools
        if hasattr(self.llm, 'generate_response'):
            return self.llm.generate_response(prompt)
        else:
            # Fallback for CrewAI LLM
            return str(self.llm.invoke(prompt))

    def provide_feedback(self, candidate_answer, question, ideal_answer):
        """
        Provide feedback on a candidate's answer.

        Args:
            candidate_answer (str): The candidate's answer.
            question (str): The interview question.
            ideal_answer (str): The ideal answer to the question.

        Returns:
            str: Feedback on the candidate's answer.
        """
        prompt = InterviewPrompts.feedback_prompt(candidate_answer, question, ideal_answer)

        # For now, we'll use the LLM directly instead of the agent
        # In a future implementation, we'll use the agent with tools
        if hasattr(self.llm, 'generate_response'):
            return self.llm.generate_response(prompt)
        else:
            # Fallback for CrewAI LLM
            return str(self.llm.invoke(prompt))
