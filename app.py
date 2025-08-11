from flask import Flask, request, jsonify, render_template
import json
from llm_utils import generate_next_phrase

app = Flask(__name__)

with open("story/narrative_graph.json", "r", encoding="utf-8") as f:
    narrative_graph = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/continue', methods=['GET'])
def continue_story():
    node = request.args.get('node', 'start')
    data = narrative_graph.get(node, {"text": "Erreur : nœud inconnu", "options": {}})
    return jsonify(data)

@app.route("/expand", methods=["POST"])
def expand():
    word = request.json.get("word")
    if not word:
        return jsonify({"error": "Missing 'word' in request"}), 400

    if word not in narrative_graph:
        print(f"Le mot '{word}' n'existe pas dans le graphe narratif.")
        print("Appel au LLM pour générer la phrase suivante...")
        # Appel au LLM si le mot n’existe pas
        generated = generate_next_phrase(word)
        if not generated:
            return jsonify({"error": "Le LLM n'a pas pu générer de phrase."}), 500
        print(f"Phrase générée : {generated}")
        # Ajouter le mot généré au graphe narratif
        narrative_graph[word] = {"text": generated, "options": {}}

        # Persistance dans le bon fichier
        with open("story/narrative_graph.json", "w", encoding="utf-8") as f:
            json.dump(narrative_graph, f, indent=2, ensure_ascii=False)
        
        print(f"Le mot '{word}' a été ajouté au graphe narratif.")
    return jsonify({"next": narrative_graph[word]})

if __name__ == '__main__':
    app.run(debug=True)
