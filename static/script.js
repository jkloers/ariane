document.addEventListener('DOMContentLoaded', () => {
  const storyDiv = document.getElementById('story');
  const controlsDiv = document.getElementById('controls');

  let currentNode = 'start';
  const visitedNodes = new Set();
  const historyStack = [];

  const updateVisitedNodes = () => {
    console.log("Visited nodes:", [...visitedNodes]);
    console.log("Navigation history:", [...historyStack]);
  };

  const addReturnButton = () => {
    controlsDiv.innerHTML = '';

    // Bouton retour
    const btn = document.createElement('button');
    btn.textContent = 'Retour';
    btn.disabled = historyStack.length === 0;
    btn.onclick = () => {
      const prevNode = historyStack.pop();
      if (prevNode) {
        loadNode(prevNode, true);
      }
    };
    controlsDiv.appendChild(btn);

    // Bouton "Voir l'arbre"
    const treeBtn = document.createElement('button');
    treeBtn.textContent = "Voir l'arbre";
    treeBtn.style.marginLeft = "16px";
    treeBtn.onclick = () => window.open('/static/draw_tree.html', '_blank');
    controlsDiv.appendChild(treeBtn);
  };

  const loadNode = async (nodeName, isReturn = false) => {
    if (nodeName !== 'end') {
      if (!isReturn && currentNode !== nodeName) {
        historyStack.push(currentNode);
      }
      currentNode = nodeName;
      visitedNodes.add(nodeName);
    }

    try {
      const res = await fetch(`/continue?node_id=${encodeURIComponent(nodeName)}`);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json(); // { text: "...", options: { mot: "id_noeud" } }
      displayStory(data);
    } catch (error) {
      storyDiv.innerHTML = `<p class="error">Failed to load story segment: ${error.message}</p>`;
    }

    updateVisitedNodes();
    addReturnButton();
  };

  const displayStory = (data) => {
    storyDiv.innerHTML = '';

    const words = data.text.split(/\s+/);

    words.forEach((word, idx) => {
      const span = document.createElement('span');
      span.className = 'clickable';
      span.textContent = word;

      // récupère le prochain nœud si défini dans options
      const nextNode = data.options?.[word] || null;
      if (nextNode) {
        span.dataset.node = nextNode;
      }

      storyDiv.appendChild(span);
      if (idx < words.length - 1) {
        storyDiv.appendChild(document.createTextNode(' '));
      }
    });
  };

  storyDiv.addEventListener('click', async (e) => {
    if (e.target.classList.contains('clickable')) {
      const word = e.target.textContent;
      const nextNode = e.target.dataset.node;

      if (nextNode) {
        // Si le mot existe déjà comme enfant, on affiche simplement la phrase associée
        loadNode(nextNode);
      } else {
        // Sinon, on génère une nouvelle branche
        const res = await fetch('/expand', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ parent_id: currentNode, word })
        });
        if (res.ok) {
          const data = await res.json(); // data is the new node
          displayStory(data);
          visitedNodes.add(word);
          updateVisitedNodes();
        } else {
          storyDiv.innerHTML = "<p class='error'>Erreur lors de la génération.</p>";
        }
      }
    }
  });

  loadNode(currentNode);
});
