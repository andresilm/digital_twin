import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv
from prompt import BASE_PROMPT, OUT_DOMAIN_DEFAULT_ANSWER, OUT_KNOWLEDGE_DEFAULT_ANSWER

load_dotenv()

logger = logging.getLogger(__name__)

MY_GOOGLE_API_KEY = os.getenv("MY_GOOGLE_API_KEY", "AIzaSyDbYBIyvDbPBWPvyah6_LZfMx3xZZTnX1Q")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
CONVERSATION_HISTORY_LENGTH = 3


GENERATION_CONFIG = {
        "temperature": 0.00,
}


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
        self._history = ["" for _ in range(CONVERSATION_HISTORY_LENGTH)]
        self._history_ptr = 0

    def __update_history(self, new_input: str):
        self._history[self._history_ptr] = new_input
        self._history_ptr = (self._history_ptr + 1) % CONVERSATION_HISTORY_LENGTH

    @property
    def history(self):
        return "\n".join([entry for entry in self._history])

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
        logger.debug("Conversation history:\n%s", self._history)
        response = self._model.generate_content(prompt, generation_config=GENERATION_CONFIG)
        self.__update_history(user_input)
        return response.candidates[0].content.parts[0].text

    def _build_prompt(
        self,
        user_input,
        context,
        base_profile,
        out_of_domain_answer=OUT_DOMAIN_DEFAULT_ANSWER,
        out_of_knowledge_answer=OUT_KNOWLEDGE_DEFAULT_ANSWER
    ):
        """
        Builds the formatted prompt string to send to the Gemini model.

        Args:
            user_input (str): The current user query.
            context (str): Specific context related to the query.
            base_profile (str): The base profile text.
            out_of_domain_answer (str): Default reply if question is out of domain.
            out_of_knowledge_answer (str): Default reply if question can't be answered.

        Returns:
            str: The formatted prompt ready for the model.
        """

        prompt_filled = BASE_PROMPT.format(
            base_profile=base_profile,
            context=context,
            user_input=user_input,
            history=self.history,
            out_of_domain_answer=out_of_domain_answer,
            out_of_knowledge_answer=out_of_knowledge_answer
        )
        logger.debug("PROMPT:\n%s", prompt_filled)
        return prompt_filled
