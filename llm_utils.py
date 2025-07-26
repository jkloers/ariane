import os
from dotenv import load_dotenv
from mistralai.client import MistralClient

load_dotenv()

def format_response(text: str, max_length: int = 280) -> str:
    text = ' '.join(text.split())
    text = text[:max_length - 3] + "..." if len(text) > max_length else text
    ngraph_input = text.json()
    return ngraph_input

def generate_next_phrase(user_input: str) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=api_key)

    try:
        chat_response = client.chat(
            model="mistral-tiny",
            messages=[{"role": "user", "content": user_input}],
        )
        response_text = chat_response.choices[0].message.content
        return format_response(response_text)
    except Exception as e:
        return f"Error getting LLM response: {str(e)}"
    
    