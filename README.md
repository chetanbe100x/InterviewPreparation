# AI Interview Preparation Framework

An agentic AI framework for interview preparation that generates personalized interview questions and answers based on job role, company, and experience level.

## Features

- **Personalized Interview Preparation**: Get tailored interview questions and answers based on your specific job role, target company, and experience level.
- **Multiple AI Models**: Choose between Ollama (local) and Google AI Studio models, including the advanced Gemini 2.5 Pro Preview model.
- **Comprehensive Research**: The system researches the company and analyzes the job role to provide relevant and accurate interview questions.
- **Downloadable Results**: Download your interview preparation materials for offline review.

## Architecture

This framework uses a multi-agent approach with specialized agents for different tasks:

1. **Research Agents**:
   - Company Research Agent: Gathers information about the target company
   - Role Analysis Agent: Analyzes the job role and required skills

2. **Interview Agents**:
   - Interview Preparation Agent: Generates interview questions and ideal answers
   - Feedback Agent: Provides feedback on practice answers

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd interview-preparation
   ```

2. **Important for Windows Users**: Install Microsoft Visual C++ Build Tools

   Some Python packages require C++ compilation. Before installing dependencies, you need to install Microsoft Visual C++ Build Tools:

   1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   2. During installation, select "Desktop development with C++"
   3. After installation, restart your computer

3. Install the required dependencies:

   ### Using Conda Environment (Recommended)

   #### Option 1: Create a new Conda environment using environment.yml

   ```bash
   # Create and activate a new conda environment from the provided file
   conda env create -f environment.yml
   conda activate interviewPrep
   ```

   #### Option 2: Use your existing Conda environment

   If you're already using a Conda environment (like `interviewPrep`):

   ```bash
   # Activate your conda environment
   conda activate interviewPrep

   # Install dependencies using the installation script
   python install_dependencies.py
   ```

   The script will automatically detect your Conda environment and try to use conda for packages when possible, falling back to pip when needed.

   ### Using Standard Python Environment

   If you're using a standard Python environment:

   ```bash
   # Using the installation script
   python install_dependencies.py
   ```

   ### Manual Installation

   If you prefer to install packages manually:

   ```bash
   # Core dependencies
   pip install python-dotenv==1.0.0
   pip install langchain-core>=0.1.29,<0.2.0

   # Main packages
   pip install streamlit==1.32.0
   pip install crewai==0.28.5
   pip install langchain==0.1.11
   pip install langchain-community==0.0.27
   pip install ollama==0.1.6
   pip install google-generativeai==0.3.2
   pip install requests==2.31.0
   pip install langchain-google-genai==0.0.9
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and add your Google AI API key if you plan to use Google AI Studio models.

4. Install Ollama (if you plan to use Ollama models):
   - Follow the installation instructions at [Ollama's official website](https://ollama.ai/download)

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Select your preferred model provider and model (Google AI Studio with gemini-2.5-pro-preview-03-25 is set as default)

4. Enter your job role, target company, and experience level

5. Click "Generate Interview Questions" to get personalized interview questions and answers

6. Download the results for offline review

## Testing

### Simple Test (Recommended for Python 3.12)

If you're having issues with dependencies, you can run a simplified test that only requires `python-dotenv` and `google-generativeai`:

```
pip install python-dotenv google-generativeai
python simple_test.py
```

This will test the Google AI integration directly without requiring all the other dependencies.

### Full Test

To test the full framework functionality:

```
python test_google_ai.py
```

## Requirements

- Python 3.8+
- Streamlit
- CrewAI
- LangChain
- Ollama (for local models)
- Google Generative AI Python SDK (for Google AI Studio models)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
