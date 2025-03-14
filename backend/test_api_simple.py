#!/usr/bin/env python3
"""
Script simple pour tester l'API /api/chat avec curl
"""
import os
import sys
import subprocess
import json

def test_api_with_curl():
    """Tester l'API /api/chat avec curl"""
    print("=== Test de l'API /api/chat avec curl ===")
    
    # Message de test
    test_message = "Je veux acheter des chaussures de luxe pour 500 euros"
    
    # Construire la commande curl
    curl_command = [
        "curl",
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"message": test_message}),
        "http://localhost:5000/api/chat"
    ]
    
    # Exécuter la commande curl
    try:
        print(f"Exécution de la commande: {' '.join(curl_command)}")
        result = subprocess.run(curl_command, capture_output=True, text=True)
        
        # Vérifier le code de retour
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de curl: {result.stderr}")
            return False
        
        # Afficher la sortie
        print("\nRéponse brute:")
        print(result.stdout)
        
        # Essayer de parser la réponse JSON
        try:
            response_data = json.loads(result.stdout)
            
            print("\nRéponse formatée:")
            print(f"Texte de réponse: {response_data.get('response', 'Pas de texte de réponse')[:100]}...")
            
            if 'financial_data' in response_data:
                print(f"Données financières: {response_data['financial_data']}")
            else:
                print("Pas de données financières dans la réponse")
            
            return True
        except json.JSONDecodeError:
            print("La réponse n'est pas un JSON valide")
            return False
    
    except Exception as e:
        print(f"Erreur lors du test de l'API: {str(e)}")
        return False

def main():
    """Fonction principale"""
    success = test_api_with_curl()
    
    if success:
        print("\nTest de l'API réussi!")
        return 0
    else:
        print("\nTest de l'API échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 