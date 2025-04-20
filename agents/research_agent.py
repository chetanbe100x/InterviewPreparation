"""
Research agent for the interview preparation framework.
Simplified version that doesn't rely on crewai.
"""
from prompts.interview_prompts import InterviewPrompts

class ResearchAgent:
    """
    Agent responsible for researching company and role information.
    """

    def __init__(self, llm):
        """
        Initialize the research agent.

        Args:
            llm: The language model to use for the agent.
        """
        self.llm = llm

    def get_company_research_prompt(self):
        """
        Get the prompt for the company research agent.

        Returns:
            str: The agent prompt.
        """
        return """You are an expert in corporate research with years of experience analyzing
        companies across various industries. You have a knack for uncovering valuable insights
        about company culture, values, and interview processes that help candidates prepare
        effectively for interviews."""

    def get_role_analysis_prompt(self):
        """
        Get the prompt for the role analysis agent.

        Returns:
            str: The agent prompt.
        """
        return """You are a career advisor with deep expertise in job market trends and
        role requirements across the tech industry. You can break down complex job descriptions
        into clear skill requirements and help candidates understand what companies are really
        looking for in specific roles."""

    def research_company(self, company_name):
        """
        Research information about a company.

        Args:
            company_name (str): The name of the company to research.

        Returns:
            str: Information about the company.
        """
        prompt = InterviewPrompts.company_research_prompt(company_name)

        # For now, we'll use the LLM directly instead of the agent
        # In a future implementation, we'll use the agent with tools
        if hasattr(self.llm, 'generate_response'):
            return self.llm.generate_response(prompt)
        else:
            # Fallback for CrewAI LLM
            return str(self.llm.invoke(prompt))

    def analyze_role(self, role, company_name, experience_level):
        """
        Analyze a job role.

        Args:
            role (str): The job role to analyze.
            company_name (str): The name of the company.
            experience_level (str): The experience level of the candidate.

        Returns:
            str: Analysis of the job role.
        """
        prompt = InterviewPrompts.role_analysis_prompt(role, company_name, experience_level)

        # For now, we'll use the LLM directly instead of the agent
        # In a future implementation, we'll use the agent with tools
        if hasattr(self.llm, 'generate_response'):
            return self.llm.generate_response(prompt)
        else:
            # Fallback for CrewAI LLM
            return str(self.llm.invoke(prompt))
