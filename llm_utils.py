import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

ariane_agent_id = "ag:8781a9ee:20250810:ariane:182d3d86"

API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise RuntimeError("MISTRAL_API_KEY non défini")

client = Mistral(api_key=API_KEY)

def generate_next_phrase_with_agent(agent_id: str, user_input: str) -> str:
    response = client.beta.conversations.start(
        agent_id=agent_id,
        inputs=[{"role": "user", "content": user_input}],
        # store=False
    )
    # Adapte selon la structure de la réponse retournée par l'API beta
    return response.outputs[0].content

if __name__ == "__main__":
    print(generate_next_phrase_with_agent(ariane_agent_id, "Fraises"))
