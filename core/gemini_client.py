from google import genai
from google.genai import types

import config

class GeminiClient:
    def __init__(self):
        self.error = None
        self.client = None
        self._chat = None
        self.start_session()
    
    def start_session(self):
        if not config.api_key:
            self.error = "no api key provided"
            return
        try:
            self.client = genai.Client(api_key=config.api_key)
            self._chat = self.client.chats.create(
                model=config.model,
                config=types.GenerateContentConfig(
                    system_instruction=config.system_prompt
                ),
            )
            self.error = None
        except Exception as e:
            self.error = str(e)
    def send(self, text):
        if self.error:
            return self.error
        try:
            response = self._chat.send_message(text)
            return response.text or "no response"
        except Exception as e:
            return f"something went wrong: {str(e)}"
    def generate(self, prompt, system=None):
        if self.error:
            return "something went wrong: "+self.error
        try:
            response = self.client.models.generate_content(
                model=config.model,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=system),
            )
            return response.text or "no response"

        except Exception as e:
            return "something went wrong: "+str(e)
    def run_with_tools(self, prompt, tools, system=None, max_calls=10):
        if self.error:
            return "something went wrong: "+self.error
        try:
            response = self.client.models.generate_content(
                model=config.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    tools=tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        maximum_remote_calls=max_calls
                    ),
                ),
            )
            return response.text or "no response"
        except Exception as e:
            return f"something went wrong: {str(e)}"

    def reset(self):
        self.start_session()