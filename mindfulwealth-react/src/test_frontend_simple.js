/**
 * Script simple pour tester l'affichage des messages dans le frontend
 * Exécutez ce script dans la console du navigateur sur la page de chat
 */

function testMessageDisplay() {
  console.log('=== Test d\'affichage des messages ===');
  
  // Vérifier si le conteneur de messages existe
  const messagesContainer = document.querySelector('[data-testid="messages-container"]');
  if (!messagesContainer) {
    console.error('Conteneur de messages non trouvé!');
    return false;
  }
  
  console.log('Conteneur de messages trouvé:', messagesContainer);
  
  // Vérifier les messages existants
  const existingMessages = messagesContainer.querySelectorAll('[data-testid^="message-"]');
  console.log('Nombre de messages existants:', existingMessages.length);
  
  // Afficher le contenu de chaque message
  existingMessages.forEach((msg, index) => {
    const messageText = msg.querySelector('.whitespace-pre-wrap.break-words');
    console.log(`Message ${index}:`, messageText ? messageText.textContent : 'Pas de texte');
  });
  
  // Injecter un message de test
  console.log('\nInjection d\'un message de test...');
  
  // Créer un élément de message
  const testMessageDiv = document.createElement('div');
  testMessageDiv.className = 'flex justify-start w-full';
  testMessageDiv.setAttribute('data-testid', 'message-test');
  
  // Créer le contenu du message
  testMessageDiv.innerHTML = `
    <div
      class="max-w-[80%] rounded-lg p-3 rounded-tl-none"
      style="
        background-color: var(--color-bot-message);
        color: var(--color-bot-message-text);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)
      "
    >
      <p class="whitespace-pre-wrap break-words">Ceci est un message de test injecté directement dans le DOM.</p>
      <div class="mt-2">
        <span
          class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
          style="
            background-color: var(--color-primary-light);
            color: var(--color-primary)
          "
        >
          test
        </span>
      </div>
    </div>
  `;
  
  // Ajouter le message au conteneur
  messagesContainer.appendChild(testMessageDiv);
  
  console.log('Message de test injecté avec succès!');
  
  // Vérifier à nouveau les messages
  const updatedMessages = messagesContainer.querySelectorAll('[data-testid^="message-"]');
  console.log('Nombre de messages après injection:', updatedMessages.length);
  
  return true;
}

function testConversationContext() {
  console.log('\n=== Test du contexte de conversation ===');
  
  // Vérifier si le contexte de conversation est accessible
  if (typeof window.conversationContext === 'undefined') {
    console.log('Le contexte de conversation n\'est pas exposé globalement. Cela est normal pour la sécurité.');
    
    // Essayer d'accéder aux hooks React (cela ne fonctionnera pas directement)
    console.log('Tentative d\'inspection des hooks React...');
    
    // Chercher des éléments React dans le DOM
    const reactRoot = document.querySelector('#root');
    if (reactRoot) {
      console.log('Élément racine React trouvé:', reactRoot);
      console.log('Pour inspecter les hooks React, utilisez les outils de développement React.');
    }
    
    return false;
  }
  
  console.log('Contexte de conversation:', window.conversationContext);
  return true;
}

function testApiCall() {
  console.log('\n=== Test d\'appel API direct ===');
  
  // Créer une requête fetch directe
  console.log('Envoi d\'une requête fetch directe à l\'API...');
  
  return fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: 'Test direct depuis le navigateur'
    })
  })
  .then(response => {
    console.log('Statut de la réponse:', response.status);
    return response.json();
  })
  .then(data => {
    console.log('Données de réponse:', data);
    
    if (data && data.response) {
      console.log('Texte de réponse:', data.response.substring(0, 100) + '...');
      return true;
    } else {
      console.error('Pas de texte de réponse dans les données');
      return false;
    }
  })
  .catch(error => {
    console.error('Erreur lors de l\'appel API:', error);
    return false;
  });
}

// Exécuter les tests
async function runTests() {
  console.log('=== Début des tests frontend ===');
  
  const displayTestResult = testMessageDisplay();
  console.log('Test d\'affichage des messages:', displayTestResult ? 'RÉUSSI' : 'ÉCHOUÉ');
  
  const contextTestResult = testConversationContext();
  console.log('Test du contexte de conversation:', contextTestResult ? 'RÉUSSI' : 'ÉCHOUÉ');
  
  const apiTestResult = await testApiCall();
  console.log('Test d\'appel API direct:', apiTestResult ? 'RÉUSSI' : 'ÉCHOUÉ');
  
  console.log('\n=== Résumé des tests ===');
  console.log('Test d\'affichage des messages:', displayTestResult ? 'RÉUSSI' : 'ÉCHOUÉ');
  console.log('Test du contexte de conversation:', contextTestResult ? 'RÉUSSI' : 'ÉCHOUÉ');
  console.log('Test d\'appel API direct:', apiTestResult ? 'RÉUSSI' : 'ÉCHOUÉ');
}

// Exécuter les tests
runTests(); 