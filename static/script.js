document.addEventListener('DOMContentLoaded', () => {
  const storyDiv = document.getElementById('story');
  const controlsDiv = document.getElementById('controls');

  let currentNode = 'start';

  const allNodes = new Set([
    "start", "goût", "fraises", "rappeler", "vieux chalet",
    "l’été", "elle", "jamais", "entier", "étranger",
    "visage", "fraîcheur", "chambre"
  ]); //devenu inutile ? 

  const visitedNodes = new Set();
  const historyStack = [];

  const updateVisitedNodes = () => {
    console.log("Visited nodes:", [...visitedNodes]);
    console.log("Navigation history:", [...historyStack]);
  };

  const addReturnButton = () => {
    controlsDiv.innerHTML = '';
    const btn = document.createElement('button');
    btn.textContent = 'Return to Previous Node';
    btn.disabled = historyStack.length === 0; // désactive si pile vide
    btn.onclick = () => {
      const prevNode = historyStack.pop();
      if (prevNode) {
        loadNode(prevNode, true); // <-- indique qu'on revient en arrière
      }
    };
    controlsDiv.appendChild(btn);
  };

  const loadNode = async (nodeName, isReturn = false) => {
    if (nodeName !== 'end') {
      if (!isReturn && currentNode !== nodeName) {
        historyStack.push(currentNode);
      }
      currentNode = nodeName;
      visitedNodes.add(nodeName);
    }

    if (allNodes.size === visitedNodes.size) {
      nodeName = 'end';
    }

    try {
      const res = await fetch(`/continue?node=${encodeURIComponent(nodeName)}`);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();
      displayStory(data);
    } catch (error) {
      storyDiv.innerHTML = `<p class="error">Failed to load story segment: ${error.message}</p>`;
    }

    updateVisitedNodes();
    addReturnButton();
  };

  const displayStory = (data) => {
    storyDiv.innerHTML = '';

    // Découpe le texte en mots
    const words = data.text.split(/\s+/);

    words.forEach((word, idx) => {
      const span = document.createElement('span');
      span.className = 'clickable';
      span.textContent = word;

      // Si le mot correspond à une option, ajoute le dataset.node
      const nextNode = data.options?.[word] || null;
      if (nextNode) {
        span.dataset.node = nextNode;
      }

      storyDiv.appendChild(span);
      // Ajoute un espace après chaque mot sauf le dernier
      if (idx < words.length - 1) {
        storyDiv.appendChild(document.createTextNode(' '));
      }
    });
  };

  storyDiv.addEventListener('click', (e) => {
    if (e.target.classList.contains('clickable')) {
      const nextNode = e.target.dataset.node;
      if (nextNode) {
        loadNode(nextNode); // navigation normale, isReturn=false par défaut
      }
    }
  });

  loadNode(currentNode);
});
