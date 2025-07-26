document.addEventListener('DOMContentLoaded', () => {
  const storyDiv = document.getElementById('story');
  const controlsDiv = document.getElementById('controls');

  let currentNode = 'start';

  const allNodes = new Set([
    "start", "goût", "fraises", "rappeler", "vieux chalet",
    "l’été", "elle", "jamais", "entier", "étranger",
    "visage", "fraîcheur", "chambre"
  ]);

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
        loadNode(prevNode);
      }
    };
    controlsDiv.appendChild(btn);
  };

  const loadNode = async (nodeName) => {
    if (nodeName !== 'end') {
      if (currentNode !== nodeName) {
        historyStack.push(currentNode);
      }
      currentNode = nodeName;  // déplacer ici la mise à jour
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

    const regex = /<([^>]+)>/g;
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(data.text)) !== null) {
      const textBefore = data.text.substring(lastIndex, match.index);
      if (textBefore) {
        storyDiv.appendChild(document.createTextNode(textBefore));
      }

      const word = match[1];
      const nextNode = data.options?.[word] || null;

      const span = document.createElement('span');
      span.className = 'clickable';
      span.textContent = word;
      if (nextNode) {
        span.dataset.node = nextNode;
      }
      storyDiv.appendChild(span);

      lastIndex = regex.lastIndex;
    }

    const remaining = data.text.substring(lastIndex);
    if (remaining) {
      storyDiv.appendChild(document.createTextNode(remaining));
    }
  };

  storyDiv.addEventListener('click', (e) => {
    if (e.target.classList.contains('clickable')) {
      const nextNode = e.target.dataset.node;
      if (nextNode) {
        loadNode(nextNode); // ne pas modifier currentNode ici
      }
    }
  });

  loadNode(currentNode);
});