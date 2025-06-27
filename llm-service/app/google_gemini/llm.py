import google.generativeai as genai


MY_GOOGLE_API_KEY = "AIzaSyDbYBIyvDbPBWPvyah6_LZfMx3xZZTnX1Q"
GEMINI_MODEL = "gemini-2.0-flash"
OUT_DOMAIN_DEFAULT_ANSWER = "Esa pregunta no esta relacionada a mi. Si queres saber otra cosa preguntame!"
OUT_KNOWLEDGE_DEFAULT_ANSWER = ("Hmm vos sabes que de eso no me acuerdo... "
                                "Si queres saber otra cosa preguntame!")

# This is a rough estimate, as token length varies. Adjust as needed.
MAX_INPUT_LENGTH = 1000000


class GeminiLLM:
    def __init__(self, model_name=GEMINI_MODEL, google_api_key=MY_GOOGLE_API_KEY):
        genai.configure(api_key=google_api_key)
        self._model = genai.GenerativeModel(model_name)

    def generate_content(self, user_input, document, base_profile: str):

        prompt = self._build_prompt(user_input,
                                    document,
                                    base_profile
                                    )
        response = self._model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text

    def _build_prompt(self,
                      user_input,
                      context,
                      base_profile,
                      history=None,
                      out_of_domain_answer=OUT_DOMAIN_DEFAULT_ANSWER,
                      out_of_knowledge_answer=OUT_KNOWLEDGE_DEFAULT_ANSWER):
        if type(history) == list:
            history = "".join(entry for entry in history)

        prompt = f"""
    [Role]
    You are a a conversational agent pretending to be me, the person of which information you are going to find in 
    "[Twin Base Profile]". You have to adopt the personality of the person described here. 

    [Twin Base Profile]
    {base_profile}
    
    [Specific Context]
    {context}
    
    [Task]
    Your main task is to answer questions about my professional and personal life. You will find 
    two sections named "[Twin Base Profile]" and "[Specific Context]". In "[Twin Base Profile]" 
    you will find general information that may not be detailed enough to answer the question but will give you the 
    general picture and personality about the person your are pretending to be. If answer to question is inside, you can use it as well.
    In the latter section "[Specific Context]" you'll surely find the data to answer the "[User Input]".
    While keeping my personality try to formulate answers in a assertive way.
    Remember:
     * Only answer the question in "[User Input]". 
     * Do not add information not relevant or not related to the question. If you detect this is an out-of-domain situation,
     kindly reply with {out_of_domain_answer} 
    * Avoid answering about any topic not included in "[Twin Base Profile]" or "[Specific Context]".
    * Your reply should be limited to one sentence or two if needed. If more information is required, user will do it.
    * If you do not have the exact information, do not guess or make up the answer. Reply with {out_of_knowledge_answer} 
    
    [User Input]
    {user_input}

    [Conversation History]
    {history}
"""
        return prompt
