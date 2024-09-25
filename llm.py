from openai import OpenAI
from pydantic import BaseModel
import json

class LLM:
    def __init__(self, model_name: str = 'gpt-4o-2024-08-06', system_prompt: str = None) -> None:
        self.model_name = model_name
        self.client = OpenAI()
        if system_prompt is None:
            system_prompt =  'You are an expert mathematician.'
        self.system_prompt = system_prompt

    def _generate(self, messages: list[dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        return response.choices[0].message.content
    
    def _generate_structured(self, messages: list[dict[str, str]], response_format: type) -> any:
        if isinstance(response_format, type) and issubclass(response_format, BaseModel):
            response = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=messages,
                response_format=response_format
            )
            return response.choices[0].message.parsed
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_format=response_format
            )
            content = response.choices[0].message.content
            return json.loads(content)

    def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        if system_prompt is None:
            system_prompt = self.system_prompt
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',  'content': prompt}
        ]
        return self._generate(messages)

    def generate_structured(self, prompt: str, response_format: type, system_prompt: str = None) -> any:
        if system_prompt is None:
            system_prompt = self.system_prompt
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',  'content': prompt}
        ]
        return self._generate_structured(messages, response_format)
    
    def generate_multichoice(self, prompt: str, choices: list[str]) -> str:
        # JSON schema instead of Pydantic struct so choices can be
        # determined at runtime
        response_format = {
            'type':  'json_schema',
            'json_schema': {
                'name' : 'choices',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'choice': {
                            'type': 'string',
                            'enum': choices
                        }
                    },
                    'required': ['choice'],
                    'additionalProperties': False
                },
                'strict': True
            }
        }
        response = self.generate_structured(prompt, response_format)
        if 'choice' in response:
            return response['choice']
        raise KeyError('Invalid response -- choice key not present')
    
    def generate_int(self, prompt: str, low: int, high: int) -> int:
        if low >= high:
            raise Exception("Empty range")
        choices = [str(i) for i in range(low, high+1)]
        return int(self.generate_multichoice(prompt, choices))
    
    def generate_bool(self, prompt: str) -> bool:
        choices = ['True', 'False']
        return self.generate_multichoice(prompt, choices) == 'True'
