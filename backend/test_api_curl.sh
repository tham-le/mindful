#!/bin/bash

# Couleurs pour la sortie du terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Test de l'API /api/chat avec curl ===${NC}"

# Message de test
TEST_MESSAGE="Je veux acheter des chaussures de luxe pour 500 euros"

# Construire la commande curl
echo -e "${YELLOW}Envoi d'une requête à l'API avec le message:${NC} $TEST_MESSAGE"

# Exécuter la commande curl
RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$TEST_MESSAGE\"}" \
  http://localhost:5000/api/chat)

# Vérifier si la commande a réussi
if [ $? -ne 0 ]; then
  echo -e "${RED}Erreur lors de l'exécution de curl${NC}"
  exit 1
fi

# Afficher la réponse brute
echo -e "\n${YELLOW}Réponse brute:${NC}"
echo "$RESPONSE" | python3 -m json.tool

# Extraire le texte de réponse
RESPONSE_TEXT=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('response', 'Pas de texte de réponse')[:100] + '...')")

# Vérifier si la réponse contient des données financières
if echo "$RESPONSE" | grep -q "financial_data"; then
  echo -e "\n${GREEN}La réponse contient des données financières${NC}"
else
  echo -e "\n${RED}La réponse ne contient pas de données financières${NC}"
fi

# Afficher le texte de réponse
echo -e "\n${YELLOW}Texte de réponse:${NC}"
echo -e "${GREEN}$RESPONSE_TEXT${NC}"

echo -e "\n${GREEN}Test de l'API réussi!${NC}"

# Tester avec un autre message
echo -e "\n${YELLOW}=== Test avec un autre message ===${NC}"
TEST_MESSAGE2="Bonjour, comment ça va?"

echo -e "${YELLOW}Envoi d'une requête à l'API avec le message:${NC} $TEST_MESSAGE2"

# Exécuter la commande curl
RESPONSE2=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$TEST_MESSAGE2\"}" \
  http://localhost:5000/api/chat)

# Vérifier si la commande a réussi
if [ $? -ne 0 ]; then
  echo -e "${RED}Erreur lors de l'exécution de curl${NC}"
  exit 1
fi

# Afficher la réponse brute
echo -e "\n${YELLOW}Réponse brute:${NC}"
echo "$RESPONSE2" | python3 -m json.tool

# Extraire le texte de réponse
RESPONSE_TEXT2=$(echo "$RESPONSE2" | python3 -c "import sys, json; print(json.load(sys.stdin).get('response', 'Pas de texte de réponse')[:100] + '...')")

# Afficher le texte de réponse
echo -e "\n${YELLOW}Texte de réponse:${NC}"
echo -e "${GREEN}$RESPONSE_TEXT2${NC}"

echo -e "\n${GREEN}Test de l'API réussi!${NC}"

exit 0 