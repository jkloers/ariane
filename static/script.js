document.addEventListener('DOMContentLoaded', () => {
  const storyDiv = document.getElementById('story');

  let currentNode = 'start';
  const historyStack = [];

  // Créer et insérer le bouton "Retour"
  const backBtn = document.createElement('button');
  backBtn.textContent = '← Retour';
  backBtn.style.marginBottom = '10px';
  backBtn.disabled = true; // désactivé au début
  storyDiv.parentNode.insertBefore(backBtn, storyDiv);

  const loadNode = async (nodeName) => {
    try {
      const res = await fetch(`/continue?node=${encodeURIComponent(nodeName)}`);
      if (!res.ok) throw new Error('Erreur réseau');

      const data = await res.json();
      storyDiv.innerHTML = '';

      const regex = /<([^>]+)>/g;
      let lastIndex = 0;
      let match;

      while ((match = regex.exec(data.text)) !== null) {
        const textBefore = data.text.substring(lastIndex, match.index);
        if (textBefore) storyDiv.appendChild(document.createTextNode(textBefore));

        const word = match[1];
        const span = document.createElement('span');
        span.className = 'clickable';
        span.textContent = word;
        span.dataset.node = data.options[word] || null;
        storyDiv.appendChild(span);

        lastIndex = regex.lastIndex;
      }

      const remaining = data.text.substring(lastIndex);
      if (remaining) storyDiv.appendChild(document.createTextNode(remaining));

      currentNode = nodeName;
      backBtn.disabled = historyStack.length === 0;

    } catch (err) {
      storyDiv.innerHTML = "Erreur lors du chargement de l'histoire.";
      console.error(err);
    }
  };

  storyDiv.addEventListener('click', (e) => {
    if (e.target.classList.contains('clickable')) {
      const nextNode = e.target.dataset.node;
      if (nextNode) {
        historyStack.push(currentNode);
        loadNode(nextNode);
      }
    }
  });

  backBtn.addEventListener('click', () => {
    if (historyStack.length > 0) {
      const previousNode = historyStack.pop();
      loadNode(previousNode);
    }
  });

  loadNode(currentNode);
});
