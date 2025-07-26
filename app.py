from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Charger l'histoire une seule fois
with open("narrative_graph.json", "r", encoding="utf-8") as f:
    story_graph = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/continue', methods=['GET'])
def continue_story():
    node = request.args.get('node', 'start')
    data = story_graph.get(node, {"text": "Erreur : nœud inconnu", "options": {}})
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
