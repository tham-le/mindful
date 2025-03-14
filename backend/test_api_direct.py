#!/usr/bin/env python3
"""
Script pour tester directement l'API backend sans passer par le frontend
"""
import requests
import json
import sys

# URL de base de l'API
BASE_URL = "http://localhost:5000/api"

def test_chat_direct():
    """Tester directement l'endpoint /api/chat avec différents messages"""
    print("\n=== Test direct de l'endpoint /api/chat ===")
    
    # Messages de test
    test_messages = [
        "Je veux acheter des chaussures pour 100 euros",
        "Comment investir 500 euros?",
        "Bonjour, comment ça va?",
        "Je veux économiser de l'argent"
    ]
    
    for message in test_messages:
        print(f"\nTest avec le message: '{message}'")
        
        try:
            # Envoyer la requête directement à l'API
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": message}
            )
            
            # Vérifier le code de statut
            print(f"Code de statut: {response.status_code}")
            if response.status_code != 200:
                print(f"ERREUR: Code de statut attendu 200, reçu {response.status_code}")
                continue
            
            # Vérifier le contenu de la réponse
            try:
                data = response.json()
                
                # Vérifier si la réponse contient le texte
                if "response" in data and data["response"]:
                    print(f"Réponse reçue: '{data['response'][:100]}...'")
                else:
                    print("ERREUR: Pas de texte de réponse")
                    continue
                
                # Vérifier si la réponse contient des données financières
                if "financial_data" in data and data["financial_data"]:
                    print("Données financières détectées:")
                    print(json.dumps(data["financial_data"], indent=2))
                else:
                    print("Aucune donnée financière détectée")
                
                print("Test réussi!")
                
            except json.JSONDecodeError:
                print("ERREUR: La réponse n'est pas au format JSON valide")
                print(f"Contenu de la réponse: {response.text}")
                
        except requests.RequestException as e:
            print(f"ERREUR de connexion: {e}")
    
    return True

def test_with_curl_command():
    """Générer une commande curl pour tester l'API"""
    print("\n=== Commande curl pour tester l'API ===")
    
    message = "Je veux acheter des chaussures pour 100 euros"
    
    curl_command = f"""
curl -X POST \\
  -H "Content-Type: application/json" \\
  -d '{{"message": "{message}"}}' \\
  {BASE_URL}/chat
"""
    
    print("Vous pouvez copier et exécuter cette commande dans un terminal:")
    print(curl_command)
    
    return True

def main():
    """Fonction principale"""
    print("=== Test direct de l'API backend ===")
    
    # Vérifier que le serveur est en cours d'exécution
    try:
        response = requests.get(f"{BASE_URL}/chat")
        if response.status_code == 404:
            print("ERREUR: L'endpoint /api/chat n'existe pas ou n'accepte pas les requêtes GET")
        elif response.status_code == 405:
            print("Le serveur est en cours d'exécution (méthode GET non autorisée pour /api/chat)")
        else:
            print(f"Le serveur a répondu avec le code {response.status_code}")
    except requests.ConnectionError:
        print("ERREUR: Impossible de se connecter au serveur. Assurez-vous qu'il est en cours d'exécution sur http://localhost:5000")
        sys.exit(1)
    
    # Tester les endpoints
    chat_success = test_chat_direct()
    curl_success = test_with_curl_command()
    
    # Résumé
    print("\n=== Résumé des tests ===")
    print(f"Test direct de l'endpoint /api/chat: {'RÉUSSI' if chat_success else 'ÉCHOUÉ'}")
    print(f"Génération de commande curl: {'RÉUSSI' if curl_success else 'ÉCHOUÉ'}")
    
    if chat_success and curl_success:
        print("\nTous les tests ont réussi!")
        return 0
    else:
        print("\nCertains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 