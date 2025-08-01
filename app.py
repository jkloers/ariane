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
        # Appel au LLM si le mot n’existe pas
        generated = generate_next_phrase(word)
        narrative_graph[word] = [generated]
        # Optionnel : persistance en écrivant dans le fichier
        with open("narrative_graph.json", "w", encoding="utf-8") as f:
            json.dump(narrative_graph, f, indent=2, ensure_ascii=False)
    return jsonify({"next": narrative_graph[word]})

if __name__ == '__main__':
    app.run(debug=True)
