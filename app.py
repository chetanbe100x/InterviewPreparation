"""
Main Streamlit application for the interview preparation framework.
"""
import streamlit as st
import os
import time
from dotenv import load_dotenv

from agents.research_agent import ResearchAgent
from agents.interview_agent import InterviewAgent
from utils.helpers import get_model_integration, format_interview_questions, validate_inputs

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI Interview Preparation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """
    Main function to run the Streamlit application.
    """
    # Add custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1rem;
        color: #555;
    }
    .result-container {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">AI Interview Preparation Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="info-text">Prepare for your next interview with the help of AI. Enter your details below to get personalized interview questions and answers.</p>', unsafe_allow_html=True)

    # Sidebar for model selection
    st.sidebar.title("Model Settings")

    model_provider = st.sidebar.selectbox(
        "Select Model Provider",
        ["Google AI Studio", "Ollama"],
        index=0
    )

    # Get available models based on the selected provider
    if model_provider == "Google AI Studio":
        try:
            google_integration = get_model_integration("google")
            available_models = google_integration.get_available_models()
            # Ensure our specific model is first in the list
            if "gemini-2.5-pro-exp-03-25" in available_models:
                available_models.remove("gemini-2.5-pro-exp-03-25")
                available_models.insert(0, "gemini-2.5-pro-exp-03-25")
        except Exception as e:
            st.sidebar.warning(f"Error connecting to Google AI Studio: {e}")
            available_models = ["gemini-2.5-pro-exp-03-25", "gemini-pro", "gemini-pro-vision"]
    else:  # Ollama
        try:
            ollama_integration = get_model_integration("ollama")
            available_models = ollama_integration.get_available_models()
        except Exception as e:
            st.sidebar.warning(f"Error connecting to Ollama: {e}")
            available_models = ["llama3", "mistral", "gemma", "codellama"]

    model_name = st.sidebar.selectbox(
        "Select Model",
        available_models,
        index=0
    )

    # Add API key input for Google AI Studio
    if model_provider == "Google AI Studio":
        google_api_key = st.sidebar.text_input(
            "Google AI API Key",
            type="password",
            value=os.getenv("GOOGLE_API_KEY", "")
        )
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key

    # Main form
    with st.form("interview_form"):
        st.markdown('<h2 class="sub-header">Interview Details</h2>', unsafe_allow_html=True)

        # Input fields
        col1, col2 = st.columns(2)

        with col1:
            role = st.text_input("Job Role", placeholder="e.g., Software Engineer, Data Scientist")
            company_name = st.text_input("Company Name", placeholder="e.g., Google, Microsoft")

        with col2:
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior (6+ years)"],
                index=0
            )

        # Submit button
        submit_button = st.form_submit_button("Generate Interview Questions")

    # Process form submission
    if submit_button:
        # Validate inputs
        is_valid, error_message = validate_inputs(role, company_name, experience_level)

        if not is_valid:
            st.error(error_message)
        else:
            # Show loading spinner
            with st.spinner("Generating interview questions and answers..."):
                try:
                    # Get model integration
                    model_integration = get_model_integration(
                        "ollama" if model_provider == "Ollama" else "google",
                        model_name
                    )

                    # Create agents
                    research_agent = ResearchAgent(model_integration)
                    interview_agent = InterviewAgent(model_integration)

                    # Set up progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        # Research company
                        status_text.info("Step 1/3: Researching company information...")
                        company_info = research_agent.research_company(company_name)
                        progress_bar.progress(33)

                        # Analyze role
                        status_text.info("Step 2/3: Analyzing job role requirements...")
                        role_info = research_agent.analyze_role(role, company_name, experience_level)
                        progress_bar.progress(66)

                        # Generate interview questions
                        status_text.info("Step 3/3: Generating interview questions and answers...")
                        interview_questions = interview_agent.generate_interview_questions(
                            role, company_name, experience_level, company_info, role_info
                        )
                        progress_bar.progress(100)
                        status_text.success("Completed! Here are your interview questions and answers.")
                    except Exception as e:
                        st.error(f"An error occurred during generation: {e}")
                        st.info("Trying alternative approach with simplified prompts...")

                        # Fallback to direct question generation without detailed research
                        interview_questions = interview_agent.generate_interview_questions(
                            role, company_name, experience_level,
                            f"Company: {company_name}",
                            f"Role: {role}, Experience: {experience_level}"
                        )

                    # Format and display results
                    formatted_questions = format_interview_questions(interview_questions)

                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(f"## Interview Questions for {role} at {company_name}")
                    st.markdown(formatted_questions)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Add download button
                    st.download_button(
                        label="Download Interview Questions",
                        data=f"# Interview Questions for {role} at {company_name}\n\n{interview_questions}",
                        file_name=f"{role.replace(' ', '_')}_{company_name.replace(' ', '_')}_interview_questions.md",
                        mime="text/markdown"
                    )

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Add information about the framework
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This interview preparation assistant uses AI to help you prepare for "
        "job interviews by generating personalized interview questions and answers "
        "based on the job role, company, and your experience level."
    )

    # Add instructions
    st.sidebar.markdown("### Instructions")
    st.sidebar.info(
        "1. Select a model provider and model\n"
        "2. Enter the job role, company name, and your experience level\n"
        "3. Click 'Generate Interview Questions'\n"
        "4. Review the generated questions and answers\n"
        "5. Download the questions for offline review"
    )

if __name__ == "__main__":
    main()
