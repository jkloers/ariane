import tkinter as tk
from demo.narrative_tree import narrative_tree

# 🧠 Liste des phrases précédentes pour gérer l'historique
history_stack = []

# 🚀 Classe principale de l'application
class InteractiveFictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ariane")
        self.current_text = narrative_tree["root    "]

        # Zone d'affichage
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(padx=10, pady=10)

        # Bouton Retour
        self.back_button = tk.Button(root, text="Retour", command=self.go_back)
        self.back_button.pack(pady=(0, 10))

        self.update_display()

    def update_display(self):
        # Nettoyer l'affichage précédent
        for widget in self.text_frame.winfo_children():
            widget.destroy()

        phrase = self.current_text
        segments = narrative_tree.get(phrase, {})

        text_widget = tk.Text(
            self.text_frame,
            wrap="word",
            height=3,
            font=("Helvetica", 14),
            borderwidth=0,
            highlightthickness=0
        )
        text_widget.pack(fill="x")
        text_widget.config(state="normal")

        words = phrase.split()
        idx = 0
        for word in words:
            start_idx = f"1.{idx}"
            text_widget.insert("end", word + " ")
            matched_key = next((key for key in segments if key in word), None)
            end_idx = f"1.{idx + len(word)}"
            if matched_key:
                text_widget.tag_add(matched_key, start_idx, end_idx)
                text_widget.tag_config(matched_key, foreground="blue", underline=True)
                def make_callback(key):
                    return lambda event, key=key: self.select_segment(key)
                text_widget.tag_bind(matched_key, "<Button-1>", make_callback(matched_key))
            idx += len(word) + 1

        text_widget.config(state="disabled")

    def select_segment(self, key):
        next_phrase = narrative_tree[self.current_text][key]
        history_stack.append(self.current_text)
        self.current_text = next_phrase
        self.update_display()

    def go_back(self):
        if history_stack:
            self.current_text = history_stack.pop()
            self.update_display()

# 🔧 Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveFictionApp(root)
    root.mainloop()
