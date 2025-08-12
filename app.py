from flask import Flask, request, jsonify, render_template
import json
import uuid
from llm_utils import generate_next_phrase
from story_tree import Node, StoryTree

app = Flask(__name__)

STORY_FILE = "story/narrative_oriented_tree.json"

# --- Chargement / sauvegarde de l'arbre ---

def load_story():
    try:
        with open(STORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return StoryTree.from_dict(data)
    except FileNotFoundError:
        print("Aucun fichier trouvé, initialisation d'une nouvelle histoire.")
        return StoryTree("Il était une fois...")

def save_story(tree):
    with open(STORY_FILE, "w", encoding="utf-8") as f:
        json.dump(tree.to_dict(), f, ensure_ascii=False, indent=2)

# --- Initialisation ---
story = load_story()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/story", methods=["GET"])
def get_story():
    """Renvoie tout l'arbre narratif"""
    return jsonify(story.to_dict())

@app.route("/continue", methods=["GET"])
def continue_story():
    node_id = request.args.get("node_id")
    if not node_id:
        return jsonify({"error": "Missing 'node_id'"}), 400
    node = story.find_node(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(node.to_dict())

@app.route("/expand", methods=["POST"])
def expand():
    data = request.get_json()
    parent_id = data.get("parent_id")
    if not parent_id:
        return jsonify({"error": "Missing 'parent_id'"}), 400

    parent_node = story.find_node(parent_id)
    if not parent_node:
        return jsonify({"error": "Parent node not found"}), 404

    # Génération d'un nouveau texte avec le LLM
    generated_text = generate_next_phrase(parent_node.text)
    if not generated_text:
        return jsonify({"error": "Le LLM n'a pas pu générer de phrase."}), 500

    # Ajout du nœud
    new_node = story.add_child(parent_id, generated_text)
    save_story(story)

    return jsonify(new_node.to_dict())

if __name__ == "__main__":
    app.run(debug=True)
