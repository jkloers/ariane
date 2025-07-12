import tkinter as tk

# 🌳 Définition de l'arbre narratif (exemple simple)
narrative_tree = {
    "Un homme marche dans la forêt.": {
        "homme": "Il est vieux, le regard perdu.",
        "forêt": "Les arbres penchent comme pour écouter."
    },
    "Il est vieux, le regard perdu.": {
        "regard": "Il se souvient de la guerre."
    },
    "Les arbres penchent comme pour écouter.": {
        "arbres": "Des visages semblent apparaître dans l’écorce."
    },
    "Il se souvient de la guerre.": {
        "guerre": "Un silence glacé remplit ses pensées."
    },
    "Un silence glacé remplit ses pensées.": {},
    "Des visages semblent apparaître dans l’écorce.": {}
}

# 🧠 Liste des phrases précédentes pour gérer l'historique
history_stack = []

# 🚀 Classe principale de l'application
class InteractiveFictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roman Interactif")
        self.current_text = "Un homme marche dans la forêt."

        # 🖼️ Zone d'affichage
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(padx=10, pady=10)

        # 🔙 Bouton Retour
        self.back_button = tk.Button(root, text="Retour", command=self.go_back)
        self.back_button.pack(pady=(0, 10))

        self.update_display()

    def update_display(self):
        # Nettoyer l'affichage précédent
        for widget in self.text_frame.winfo_children():
            widget.destroy()

        tk.Label(self.text_frame, text="Cliquez sur un segment :").pack(anchor="w")

        # 🔤 Phrase actuelle
        phrase = self.current_text
        segments = narrative_tree.get(phrase, {})

        if not segments:
            # Fin de branche
            tk.Label(self.text_frame, text=phrase, font=("Helvetica", 14, "italic")).pack(pady=10)
            return

        # Affichage segmenté avec boutons
        words = phrase.split()
        for word in words:
            # Vérifie si le mot est un segment interactif
            matched_key = next((key for key in segments if key in word), None)
            if matched_key:
                btn = tk.Button(
                    self.text_frame,
                    text=word,
                    relief=tk.RAISED,
                    command=lambda key=matched_key: self.select_segment(key)
                )
                btn.pack(side=tk.LEFT, padx=3, pady=5)
            else:
                lbl = tk.Label(self.text_frame, text=word + " ")
                lbl.pack(side=tk.LEFT, padx=1)

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
