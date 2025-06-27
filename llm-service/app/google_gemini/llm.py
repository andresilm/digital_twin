import os

import google.generativeai as genai
from dotenv import load_dotenv

from ..prompt import BASE_PROMPT, OUT_DOMAIN_DEFAULT_ANSWER, OUT_KNOWLEDGE_DEFAULT_ANSWER

load_dotenv()

MY_GOOGLE_API_KEY = os.getenv("MY_GOOGLE_API_KEY", "default_api_key_here")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


class GeminiLLM:
    """
    Wrapper class for Google Gemini LLM API integration using the google.generativeai library.

    Attributes:
        _model (GenerativeModel): The configured Gemini generative model instance.
    """

    def __init__(self, model_name=GEMINI_MODEL, google_api_key=MY_GOOGLE_API_KEY):
        """
        Initializes the GeminiLLM instance by configuring the API key and loading the model.

        Args:
            model_name (str): The name of the Gemini model to use.
            google_api_key (str): Google API key to authenticate requests.
        """
        genai.configure(api_key=google_api_key)
        self._model = genai.GenerativeModel(model_name)

    def generate_content(self, user_input, document, base_profile: str):
        """
        Generates a response from the Gemini model given user input, context document, and base profile.

        Args:
            user_input (str): The question or prompt from the user.
            document (str): Specific context relevant to the user's input.
            base_profile (str): The base profile text representing the personality and background.

        Returns:
            str: The text content of the generated response from the model.
        """
        prompt = self._build_prompt(
            user_input,
            document,
            base_profile
        )
        response = self._model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text

    def _build_prompt(
        self,
        user_input,
        context,
        base_profile,
        history=None,
        out_of_domain_answer=OUT_DOMAIN_DEFAULT_ANSWER,
        out_of_knowledge_answer=OUT_KNOWLEDGE_DEFAULT_ANSWER
    ):
        """
        Builds the formatted prompt string to send to the Gemini model.

        Args:
            user_input (str): The current user query.
            context (str): Specific context related to the query.
            base_profile (str): The base profile text.
            history (list or None): Optional list of previous conversation entries.
            out_of_domain_answer (str): Default reply if question is out of domain.
            out_of_knowledge_answer (str): Default reply if question can't be answered.

        Returns:
            str: The formatted prompt ready for the model.
        """
        if isinstance(history, list):
            history = "".join(entry for entry in history)

        return BASE_PROMPT.format(
            base_profile=base_profile,
            context=context,
            user_input=user_input,
            history=history or "",
            out_of_domain_answer=out_of_domain_answer,
            out_of_knowledge_answer=out_of_knowledge_answer
        )
