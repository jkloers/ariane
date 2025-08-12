import uuid

class Node:
    def __init__(self, text, parent=None, node_id=None):
        self.id = node_id or str(uuid.uuid4())
        self.text = text
        self.parent = parent
        self.children = []

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "children": [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data, parent=None):
        node = Node(data["text"], parent=parent, node_id=data["id"])
        for child_data in data.get("children", []):
            node.children.append(Node.from_dict(child_data, parent=node))
        return node

class StoryTree:
    def __init__(self, root_text=None):
        self.root = Node(root_text) if root_text else None

    def find_node(self, node_id, current=None):
        if current is None:
            current = self.root
        if current.id == node_id:
            return current
        for child in current.children:
            found = self.find_node(node_id, child)
            if found:
                return found
        return None

    def add_child(self, parent_id, text):
        parent = self.find_node(parent_id)
        if parent:
            new_node = Node(text, parent)
            parent.children.append(new_node)
            return new_node
        return None

    def to_dict(self):
        return self.root.to_dict() if self.root else {}

    @staticmethod
    def from_dict(data):
        tree = StoryTree()
        tree.root = Node.from_dict(data)
        return tree