import json
import uuid

# Ton JSON d'origine
with open("story/initial_narrative_graph.json", "r", encoding="utf-8") as f:
    old_graph = json.load(f)

class Node:
    def __init__(self, text, parent=None, node_id=None, options=None):
        self.id = node_id or str(uuid.uuid4())
        self.text = text
        self.parent = parent
        self.children = []
        self.options = options or {}

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "options": self.options,
            "children": [child.to_dict() for child in self.children]
        }

def build_tree_from_flat(flat_graph, start_key="start", visited=None, id_map=None):
    if visited is None:
        visited = set()
    if id_map is None:
        id_map = {}

    if start_key in visited:
        return None, id_map  # éviter les boucles éventuelles
    visited.add(start_key)

    node_data = flat_graph[start_key]
    node_id = id_map.get(start_key) or str(uuid.uuid4())
    id_map[start_key] = node_id

    # On crée le nœud sans options pour l'instant
    node = Node(node_data["text"], node_id=node_id)

    # On prépare les options (mot -> id du child)
    options = {}
    for mot, child_key in node_data["options"].items():
        if child_key in flat_graph:
            # On construit le child et récupère son id
            child_node, id_map = build_tree_from_flat(flat_graph, child_key, visited, id_map)
            if child_node:
                child_node.parent = node
                node.children.append(child_node)
                options[mot] = child_node.id
    node.options = options

    return node, id_map

# Construire l'arbre
root_node, _ = build_tree_from_flat(old_graph, start_key="start")

# Sauvegarder en nouveau format
with open("story/narrative_oriented_tree.json", "w", encoding="utf-8") as f:
    json.dump(root_node.to_dict(), f, ensure_ascii=False, indent=2)

print("Conversion terminée → narrative_graph_new.json")
