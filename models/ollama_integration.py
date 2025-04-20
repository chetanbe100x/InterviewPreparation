"""
Ollama model integration for the interview preparation framework.
Simplified version that doesn't rely on crewai.
"""
import ollama

class OllamaIntegration:
    """
    Integration with Ollama models for the interview preparation framework.
    """

    def __init__(self, model_name="llama3"):
        """
        Initialize the Ollama integration.

        Args:
            model_name (str): The name of the Ollama model to use.
        """
        self.model_name = model_name

    def get_available_models(self):
        """
        Get a list of available Ollama models.

        Returns:
            list: A list of available model names.
        """
        try:
            models = ollama.list()
            return [model['name'] for model in models.get('models', [])]
        except Exception as e:
            print(f"Error fetching Ollama models: {e}")
            return ["llama3", "mistral", "gemma", "codellama"]  # Default fallback models

    def invoke(self, prompt):
        """
        Generate a response using the Ollama model (compatible with LLM interface).

        Args:
            prompt (str): The prompt to send to the model.

        Returns:
            str: The generated response.
        """
        return self.generate_response(prompt)

    def generate_response(self, prompt):
        """
        Generate a response using the Ollama model directly.

        Args:
            prompt (str): The prompt to send to the model.

        Returns:
            str: The generated response.
        """
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response.get('response', '')
        except Exception as e:
            print(f"Error generating response with Ollama: {e}")
            return "Error: Could not generate response with Ollama."
