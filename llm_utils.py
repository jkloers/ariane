import os
from dotenv import load_dotenv
from mistralai import Mistral
import json

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
ARIANE_AGENT_ID = os.getenv("ARIANE_AGENT_ID")

if not API_KEY:
    raise RuntimeError("MISTRAL_API_KEY non défini")

client = Mistral(api_key=API_KEY)

def generate_next_phrase(user_input: str) -> str:
    response = client.beta.conversations.start(
        agent_id = ARIANE_AGENT_ID,
        inputs=[{"role": "user", "content": user_input}],
    )
    # Retire les guillemets au début et à la fin si présents
    phrase = response.outputs[0].content
    return phrase.strip('"')