# from mistralai.client import MistralClient
from mistralai import Mistral, UserMessage
# from mistralai.models.chat_completion import ChatMessage

def generate_response(model_name: str, api_key: str, prompt: str)-> str:
    api_key = api_key
    client = Mistral(api_key=api_key)
    messages = [
        {"role" : "user",
         "content" : f"{prompt}",
         }
    ]
    chat_response = client.chat.complete(
        model=model_name,
        messages=messages,
    )

    return chat_response.choices[0].message.content