"""
Google AI Studio model integration for the interview preparation framework.
Simplified version that doesn't rely on crewai or langchain.
"""
import os
import google.generativeai as genai

class GoogleAIIntegration:
    """
    Integration with Google AI Studio models for the interview preparation framework.
    """

    def __init__(self, model_name="gemini-2.5-pro-exp-03-25"):
        """
        Initialize the Google AI Studio integration.

        Args:
            model_name (str): The name of the Google AI model to use.
        """
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")

        if self.api_key:
            genai.configure(api_key=self.api_key)

    def get_available_models(self):
        """
        Get a list of available Google AI models.

        Returns:
            list: A list of available model names.
        """
        if not self.api_key:
            return ["gemini-2.5-pro-exp-03-25", "gemini-pro", "gemini-pro-vision"]  # Default fallback models

        try:
            models = genai.list_models()
            return [model.name.split('/')[-1] for model in models]
        except Exception as e:
            print(f"Error fetching Google AI models: {e}")
            return ["gemini-2.5-pro-exp-03-25", "gemini-pro", "gemini-pro-vision"]  # Default fallback models

    def invoke(self, prompt):
        """
        Generate a response using the Google AI model (compatible with LLM interface).

        Args:
            prompt (str): The prompt to send to the model.

        Returns:
            str: The generated response.
        """
        return self.generate_response(prompt)

    def generate_response(self, prompt, max_retries=3):
        """
        Generate a response using the Google AI model directly.

        Args:
            prompt (str): The prompt to send to the model.
            max_retries (int): Maximum number of retry attempts.

        Returns:
            str: The generated response.
        """
        if not self.api_key:
            return "Error: Google API key not found. Please set the GOOGLE_API_KEY environment variable."

        # Check if prompt is too long and truncate if necessary
        if len(prompt) > 30000:  # Approximate token limit
            print("Warning: Prompt is very long, truncating to avoid timeout issues.")
            prompt = prompt[:30000] + "\n[Note: Prompt was truncated due to length.]"

        # Configure generation settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,  # Adjust based on your needs
        }

        # Safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )

                # Use a simpler approach without timeout parameter
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_message = str(e)
                print(f"Attempt {attempt + 1}/{max_retries} failed: {error_message}")

                # Check for specific errors
                if "504" in error_message or "Deadline Exceeded" in error_message:
                    print("Timeout error detected, retrying with a shorter prompt...")
                    # If this is not the last retry, try with a shorter prompt
                    if len(prompt) > 15000:
                        prompt = prompt[:15000] + "\n[Note: Prompt was truncated due to timeout issues.]"
                        print(f"Prompt truncated to {len(prompt)} characters")
                elif "429" in error_message or "quota" in error_message.lower():
                    print("Rate limit or quota exceeded, waiting before retry...")
                    import time
                    time.sleep(5 * (attempt + 1))  # Exponential backoff
                elif "Unknown field" in error_message:
                    print("API parameter error detected. Using default parameters.")

                # If this is the last attempt, give up and return error
                if attempt == max_retries - 1:
                    return f"Error: Could not generate response with Google AI after {max_retries} attempts. Last error: {e}"
