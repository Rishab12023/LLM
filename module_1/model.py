from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def generate_response(model_name: str, api_key: str, prompt: str)-> str:
    api_key = api_key
    client = MistralClient(api_key=api_key)
    messages = [ChatMessage(role="user", content=prompt)]
    chat_response = client.chat(
        model=model_name,
        messages=messages,
    )

    return chat_response.choices[0].message.content