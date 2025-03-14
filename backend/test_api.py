#!/usr/bin/env python3
"""
Script de test pour l'API backend
"""
import requests
import json
import sys

# URL de base de l'API
BASE_URL = "http://localhost:5000/api"

def test_chat_endpoint():
    """Tester l'endpoint /api/chat"""
    print("\n=== Test de l'endpoint /api/chat ===")
    
    # Message de test
    test_message = "Je veux acheter des chaussures pour 100 euros"
    
    # Envoyer la requête
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": test_message}
        )
        
        # Vérifier le code de statut
        print(f"Code de statut: {response.status_code}")
        if response.status_code != 200:
            print(f"ERREUR: Code de statut attendu 200, reçu {response.status_code}")
            return False
        
        # Vérifier le contenu de la réponse
        try:
            data = response.json()
            print("\nRéponse reçue:")
            print(f"- Type de réponse: {type(data)}")
            
            if "response" not in data:
                print("ERREUR: Clé 'response' manquante dans la réponse")
                print(f"Contenu de la réponse: {data}")
                return False
            
            print(f"- Longueur de la réponse: {len(data['response'])}")
            print(f"- Début de la réponse: {data['response'][:100]}...")
            
            if "financial_data" in data:
                print("\nDonnées financières:")
                print(json.dumps(data["financial_data"], indent=2))
            else:
                print("\nAucune donnée financière dans la réponse")
            
            return True
            
        except json.JSONDecodeError:
            print("ERREUR: La réponse n'est pas au format JSON valide")
            print(f"Contenu de la réponse: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"ERREUR de connexion: {e}")
        return False

def test_personality_endpoint():
    """Tester l'endpoint /api/personality"""
    print("\n=== Test de l'endpoint /api/personality ===")
    
    # Modes de personnalité à tester
    personalities = ["nice", "funny", "irony"]
    
    for mode in personalities:
        print(f"\nTest du mode: {mode}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/personality",
                json={"mode": mode}
            )
            
            # Vérifier le code de statut
            print(f"Code de statut: {response.status_code}")
            if response.status_code != 200:
                print(f"ERREUR: Code de statut attendu 200, reçu {response.status_code}")
                continue
            
            # Vérifier le contenu de la réponse
            try:
                data = response.json()
                print(f"Réponse: {data}")
                
                if "success" not in data:
                    print("ERREUR: Clé 'success' manquante dans la réponse")
                    continue
                
                if data["success"] != True:
                    print(f"ERREUR: Valeur 'success' attendue True, reçu {data['success']}")
                    continue
                
                print(f"Test réussi pour le mode {mode}")
                
            except json.JSONDecodeError:
                print("ERREUR: La réponse n'est pas au format JSON valide")
                print(f"Contenu de la réponse: {response.text}")
                
        except requests.RequestException as e:
            print(f"ERREUR de connexion: {e}")
    
    return True

def main():
    """Fonction principale"""
    print("=== Test de l'API backend ===")
    
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
    chat_success = test_chat_endpoint()
    personality_success = test_personality_endpoint()
    
    # Résumé
    print("\n=== Résumé des tests ===")
    print(f"Test de l'endpoint /api/chat: {'RÉUSSI' if chat_success else 'ÉCHOUÉ'}")
    print(f"Test de l'endpoint /api/personality: {'RÉUSSI' if personality_success else 'ÉCHOUÉ'}")
    
    if chat_success and personality_success:
        print("\nTous les tests ont réussi!")
        return 0
    else:
        print("\nCertains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 