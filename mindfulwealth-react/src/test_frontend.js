/**
 * Script de test pour le frontend
 * 
 * Ce script teste l'affichage des messages dans l'interface de chat
 * en injectant directement des messages dans le contexte de conversation.
 */

// Fonction pour tester l'affichage des messages
function testChatDisplay() {
  console.log('=== Test d\'affichage des messages dans le chat ===');
  
  // Récupérer les éléments du DOM
  const messagesContainer = document.querySelector('[data-testid="messages-container"]');
  
  if (!messagesContainer) {
    console.error('Conteneur de messages non trouvé. Assurez-vous d\'être sur la page de chat.');
    return false;
  }
  
  console.log('Conteneur de messages trouvé.');
  
  // Vérifier si des messages sont déjà affichés
  const existingMessages = document.querySelectorAll('.whitespace-pre-wrap.break-words');
  console.log(`Nombre de messages déjà affichés: ${existingMessages.length}`);
  
  // Accéder au contexte React pour injecter des messages
  // Note: Ceci est une approche de débogage et ne devrait pas être utilisé en production
  let foundReactInstance = false;
  
  for (const key in window) {
    if (key.startsWith('__REACT_DEVTOOLS_GLOBAL_HOOK__')) {
      foundReactInstance = true;
      console.log('Hook React DevTools trouvé. Vous pouvez utiliser React DevTools pour inspecter les composants.');
      break;
    }
  }
  
  if (!foundReactInstance) {
    console.log('Hook React DevTools non trouvé. Utilisation d\'une approche alternative.');
  }
  
  // Injecter un message de test directement dans le DOM pour vérifier le rendu
  console.log('Injection d\'un message de test dans le DOM...');
  
  const testMessageDiv = document.createElement('div');
  testMessageDiv.className = 'flex justify-start';
  testMessageDiv.innerHTML = `
    <div class="max-w-[80%] rounded-lg p-3 rounded-tl-none" style="background-color: var(--color-bot-message); color: var(--color-bot-message-text); box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);">
      <p class="whitespace-pre-wrap break-words">Ceci est un message de test injecté directement dans le DOM. Si vous voyez ce message, le rendu HTML fonctionne correctement.</p>
    </div>
  `;
  
  // Ajouter le message au conteneur
  messagesContainer.appendChild(testMessageDiv);
  
  console.log('Message de test injecté. Vérifiez s\'il est visible dans l\'interface.');
  
  return true;
}

// Fonction pour tester l'envoi de messages via l'API
function testSendMessage() {
  console.log('\n=== Test d\'envoi de message via l\'API ===');
  
  // Récupérer les éléments du formulaire
  const inputField = document.querySelector('input[placeholder*="message"]');
  const sendButton = inputField?.closest('form')?.querySelector('button[type="submit"]');
  
  if (!inputField || !sendButton) {
    console.error('Champ de saisie ou bouton d\'envoi non trouvé.');
    return false;
  }
  
  console.log('Formulaire d\'envoi trouvé.');
  
  // Simuler la saisie d'un message
  const testMessage = 'Ceci est un message de test envoyé via le formulaire';
  console.log(`Saisie du message: "${testMessage}"`);
  
  // Définir la valeur du champ de saisie
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  nativeInputValueSetter.call(inputField, testMessage);
  
  // Déclencher l'événement de changement
  const inputEvent = new Event('input', { bubbles: true });
  inputField.dispatchEvent(inputEvent);
  
  // Simuler le clic sur le bouton d'envoi
  console.log('Clic sur le bouton d\'envoi...');
  sendButton.click();
  
  console.log('Message envoyé. Vérifiez la console pour les logs de l\'API et si la réponse s\'affiche dans l\'interface.');
  
  return true;
}

// Fonction pour vérifier les styles CSS
function testCSSStyles() {
  console.log('\n=== Test des styles CSS ===');
  
  // Vérifier les variables CSS
  const rootStyles = getComputedStyle(document.documentElement);
  const requiredVars = [
    '--color-bg-primary',
    '--color-text-primary',
    '--color-user-message',
    '--color-bot-message',
    '--color-user-message-text',
    '--color-bot-message-text'
  ];
  
  let allVarsFound = true;
  
  for (const varName of requiredVars) {
    const value = rootStyles.getPropertyValue(varName);
    if (value) {
      console.log(`✓ Variable CSS ${varName} trouvée: ${value}`);
    } else {
      console.error(`✗ Variable CSS ${varName} non trouvée`);
      allVarsFound = false;
    }
  }
  
  if (!allVarsFound) {
    console.error('Certaines variables CSS requises sont manquantes, ce qui peut affecter l\'affichage des messages.');
  }
  
  return allVarsFound;
}

// Fonction principale de test
function runTests() {
  console.log('=== Tests du frontend MindfulWealth ===');
  console.log('Exécution des tests...');
  
  // Vérifier que nous sommes sur la bonne page
  if (!window.location.pathname.includes('/chat') && !window.location.pathname.includes('/test-chat')) {
    console.error('Ces tests doivent être exécutés sur la page de chat (/chat ou /test-chat).');
    return;
  }
  
  // Exécuter les tests
  const cssResult = testCSSStyles();
  const displayResult = testChatDisplay();
  const sendResult = testSendMessage();
  
  // Afficher le résumé
  console.log('\n=== Résumé des tests ===');
  console.log(`Test des styles CSS: ${cssResult ? 'RÉUSSI' : 'ÉCHOUÉ'}`);
  console.log(`Test d'affichage des messages: ${displayResult ? 'RÉUSSI' : 'ÉCHOUÉ'}`);
  console.log(`Test d'envoi de message: ${sendResult ? 'RÉUSSI' : 'ÉCHOUÉ'}`);
  
  if (cssResult && displayResult && sendResult) {
    console.log('\nTous les tests ont réussi!');
  } else {
    console.log('\nCertains tests ont échoué.');
  }
}

// Instructions pour exécuter les tests
console.log(`
=== Instructions pour exécuter les tests ===
1. Naviguez vers la page de chat (/chat ou /test-chat)
2. Ouvrez la console du navigateur (F12)
3. Copiez ce script et collez-le dans la console
4. Appuyez sur Entrée pour exécuter les tests
5. Vérifiez les résultats dans la console
`);

// Exécuter les tests automatiquement si nous sommes sur la bonne page
if (window.location.pathname.includes('/chat') || window.location.pathname.includes('/test-chat')) {
  runTests();
} 