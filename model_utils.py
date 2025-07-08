# gemini_loader.py

import google.generativeai as genai


class GeminiLoadError(Exception):
    """Raised when the Gemini model fails to initialize due to configuration issues."""
    pass


def load_gemini(api_key: str, model_name: str = "gemini-2.0-flash"):
    """
    Initializes and returns a configured Gemini model instance.

    Args:
        api_key (str): API key for Gemini. Must be provided explicitly.
        model_name (str): The Gemini model name to use (default: "gemini-2.0-flash").

    Returns:
        genai.GenerativeModel: Configured Gemini model object.

    Raises:
        GeminiLoadError: If API key is missing or configuration fails.
    """
    try:
        if not api_key:
            raise GeminiLoadError(
                "❌ Gemini API key must be provided explicitly to load_gemini()."
            )

        # Configure Gemini SDK
        genai.configure(api_key=api_key)

        # Initialize and return the Gemini model
        model = genai.GenerativeModel(model_name)
        return model

    except Exception as e:
        raise GeminiLoadError(f"⚠️ Failed to load Gemini model: {str(e)}")
