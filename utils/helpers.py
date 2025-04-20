"""
Helper functions for the interview preparation framework.
"""
import os
from dotenv import load_dotenv
from models.ollama_integration import OllamaIntegration
from models.google_ai_integration import GoogleAIIntegration

# Load environment variables from .env file
load_dotenv()

def get_model_integration(model_provider, model_name=None):
    """
    Get the appropriate model integration based on the provider.
    
    Args:
        model_provider (str): The model provider ("ollama" or "google").
        model_name (str, optional): The name of the model to use.
        
    Returns:
        object: The model integration instance.
    """
    if model_provider.lower() == "ollama":
        if model_name:
            return OllamaIntegration(model_name=model_name)
        return OllamaIntegration()
    elif model_provider.lower() == "google":
        if model_name:
            return GoogleAIIntegration(model_name=model_name)
        return GoogleAIIntegration()
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

def format_interview_questions(questions_text):
    """
    Format the interview questions and answers for display.
    
    Args:
        questions_text (str): The raw text of questions and answers.
        
    Returns:
        str: Formatted questions and answers.
    """
    # This is a simple implementation that assumes the text is already well-formatted
    # In a more advanced implementation, we would parse the text and format it more nicely
    return questions_text

def validate_inputs(role, company_name, experience_level):
    """
    Validate user inputs.
    
    Args:
        role (str): The job role.
        company_name (str): The name of the company.
        experience_level (str): The experience level of the candidate.
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not role:
        return False, "Please enter a job role."
    if not company_name:
        return False, "Please enter a company name."
    if not experience_level:
        return False, "Please select an experience level."
    return True, ""
