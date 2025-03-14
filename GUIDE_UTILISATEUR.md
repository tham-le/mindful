# Guide Utilisateur - MindfulWealth

## Introduction

MindfulWealth est une application d'assistant financier conçue pour vous aider à prendre des décisions d'achat réfléchies et à encourager l'épargne et l'investissement. Ce guide vous explique comment installer, configurer et utiliser l'application.

![Logo MindfulWealth](https://via.placeholder.com/600x200?text=MindfulWealth+Logo)

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Démarrage de l'application](#démarrage-de-lapplication)
4. [Utilisation de l'interface de chat](#utilisation-de-linterface-de-chat)
5. [Analyse des achats impulsifs](#analyse-des-achats-impulsifs)
6. [Personnalisation de l'assistant](#personnalisation-de-lassistant)
7. [Cas d'utilisation concrets](#cas-dutilisation-concrets)
8. [Dépannage](#dépannage)

## Prérequis

Pour utiliser MindfulWealth, vous aurez besoin de :

- Docker et Docker Compose installés sur votre ordinateur
- Une clé API Gemini (disponible gratuitement sur [Google AI Studio](https://ai.google.dev/))
- Ports 80, 3000 et 5000 disponibles sur votre machine

## Installation

### Étape 1 : Téléchargement de l'application

1. Téléchargez l'application depuis le dépôt Git ou décompressez l'archive fournie
2. Ouvrez un terminal et naviguez jusqu'au dossier de l'application

### Étape 2 : Configuration

1. Exécutez le script de déploiement qui vous guidera à travers la configuration :

```bash
./deploy.sh
```

![Exécution du script de déploiement](https://via.placeholder.com/800x400?text=Execution+du+script+de+deploiement)

2. Lorsque vous y êtes invité, entrez votre clé API Gemini
3. Le script vérifiera automatiquement les ports disponibles et configurera l'environnement

## Démarrage de l'application

Une fois l'installation terminée, l'application sera accessible à :

- Interface utilisateur : <http://localhost> ou <http://localhost:3000>
- API backend : <http://localhost:5000/api>

Vous verrez la page d'accueil de MindfulWealth avec l'interface de chat.

![Page d'accueil MindfulWealth](https://via.placeholder.com/800x500?text=Page+d'accueil+MindfulWealth)

## Utilisation de l'interface de chat

### Poser une question financière

1. Dans la zone de texte en bas de l'écran, tapez votre question ou décrivez un achat que vous envisagez
2. Exemples de questions :
   - "Je veux acheter des chaussures Gucci à 800€, est-ce une bonne idée ?"
   - "Comment puis-je économiser pour ma retraite ?"
   - "Devrais-je investir dans un ETF ?"
3. Appuyez sur Entrée ou cliquez sur le bouton d'envoi

![Interface de chat](https://via.placeholder.com/800x500?text=Interface+de+chat)

### Comprendre les réponses

L'assistant vous répondra avec :

- Une analyse de votre question ou de votre achat potentiel
- Des conseils financiers personnalisés
- Des calculs montrant comment votre argent pourrait croître s'il était investi
- Des alternatives à considérer

**Exemple d'entrée :** "Je veux acheter des chaussures Gucci à 800€"

**Exemple de sortie :**

```
Je vois que vous êtes intéressé par des chaussures Gucci. C'est une marque de luxe avec des prix élevés. Avant de faire cet achat, avez-vous considéré l'impact sur vos finances?

Une paire de chaussures Gucci coûte généralement entre 500€ et 1500€. Si vous investissiez cette somme au lieu de l'utiliser pour un achat impulsif, elle pourrait valoir entre 864€ et 1620€ dans un an, et entre 1175€ et 2205€ dans cinq ans (avec un rendement annuel de 8%).

Voici quelques alternatives à considérer:
- Investir dans un ETF qui suit le marché global
- Ajouter à votre épargne d'urgence
- Chercher des chaussures de qualité à un prix plus abordable

Que pensez-vous de ces options?
```

![Exemple de réponse](https://via.placeholder.com/800x500?text=Exemple+de+reponse)

## Analyse des achats impulsifs

L'application est spécialement conçue pour vous aider à identifier les achats impulsifs et à comprendre leur impact financier à long terme.

### Comment ça marche

1. Mentionnez un achat que vous envisagez (ex: "Je veux acheter un nouveau téléphone à 1000€")
2. L'assistant détectera automatiquement s'il s'agit d'un achat impulsif
3. Vous recevrez une analyse montrant :
   - Le coût immédiat de l'achat
   - La valeur potentielle future si cet argent était investi
   - Des alternatives plus économiques
   - L'impact sur vos objectifs financiers à long terme

![Analyse d'achat impulsif](https://via.placeholder.com/800x500?text=Analyse+d'achat+impulsif)

### Exemples d'achats à analyser

- Articles de luxe (vêtements, accessoires, électronique)
- Achats non planifiés
- Produits en promotion que vous n'aviez pas prévu d'acheter

## Personnalisation de l'assistant

MindfulWealth propose différents modes de personnalité pour l'assistant financier.

### Changer le mode de personnalité

1. Cliquez sur l'icône des paramètres (⚙️) en haut à droite de l'interface
2. Sélectionnez l'un des modes de personnalité :
   - **Sympathique** : Conseils bienveillants et encourageants
   - **Amusant** : Conseils avec une touche d'humour
   - **Ironique** : Conseils avec un ton légèrement sarcastique

![Paramètres de personnalité](https://via.placeholder.com/800x400?text=Parametres+de+personnalite)

### Changer la langue

1. Cliquez sur l'icône des paramètres (⚙️)
2. Sélectionnez la langue souhaitée :
   - Français
   - Anglais

## Cas d'utilisation concrets

Voici quelques scénarios où MindfulWealth peut vous aider :

### Scénario 1 : Achat impulsif de vêtements

**Situation :** Vous naviguez en ligne et voyez une veste de marque en solde à 300€ (au lieu de 500€).

**Comment utiliser MindfulWealth :**

1. Ouvrez l'application et tapez : "Je veux acheter une veste de marque à 300€ qui est en solde"
2. L'assistant analysera votre demande et vous montrera :
   - Que malgré la réduction, c'est toujours un investissement significatif
   - Comment ces 300€ pourraient croître s'ils étaient investis
   - Des alternatives comme attendre les prochaines soldes ou chercher des options similaires moins chères

![Scénario achat de vêtements](https://via.placeholder.com/800x400?text=Scenario+achat+de+vetements)

### Scénario 2 : Planification d'épargne

**Situation :** Vous voulez commencer à épargner pour un objectif à long terme.

**Comment utiliser MindfulWealth :**

1. Ouvrez l'application et tapez : "Comment puis-je épargner 10 000€ en 3 ans ?"
2. L'assistant vous fournira :
   - Un calcul du montant mensuel à mettre de côté
   - Des suggestions de véhicules d'investissement adaptés
   - Des conseils pour réduire vos dépenses actuelles

![Scénario planification d'épargne](https://via.placeholder.com/800x400?text=Scenario+planification+epargne)

### Scénario 3 : Comparaison d'options d'achat

**Situation :** Vous hésitez entre acheter un nouvel appareil électronique maintenant ou attendre.

**Comment utiliser MindfulWealth :**

1. Ouvrez l'application et tapez : "Devrais-je acheter un nouvel ordinateur à 1200€ maintenant ou attendre 6 mois ?"
2. L'assistant analysera :
   - L'urgence de votre besoin
   - Les tendances de prix pour ce type de produit
   - L'impact financier d'attendre vs acheter maintenant
   - Les options alternatives (comme l'achat reconditionné)

![Scénario comparaison d'options](https://via.placeholder.com/800x400?text=Scenario+comparaison+options)

## Dépannage

### L'application ne démarre pas

- Vérifiez que Docker et Docker Compose sont installés et fonctionnent correctement
- Assurez-vous que les ports 80, 3000 et 5000 sont disponibles
- Consultez les logs avec la commande : `docker-compose logs`

### L'assistant ne répond pas correctement

- Vérifiez que votre clé API Gemini est valide
- Assurez-vous que votre connexion internet fonctionne
- Essayez de redémarrer l'application : `docker-compose restart`

### Problèmes de connexion

Si l'interface utilisateur ne peut pas se connecter à l'API :

1. Vérifiez que les deux conteneurs sont en cours d'exécution : `docker-compose ps`
2. Assurez-vous que le port 5000 est accessible
3. Vérifiez les logs du backend : `docker-compose logs backend`

## Conclusion

MindfulWealth est conçu pour vous aider à prendre de meilleures décisions financières en vous montrant l'impact à long terme de vos achats. En utilisant régulièrement l'application, vous développerez une meilleure conscience de vos habitudes de dépense et pourrez progressivement construire un avenir financier plus solide.

Pour toute question ou assistance supplémentaire, n'hésitez pas à consulter la documentation ou à contacter l'équipe de support.
