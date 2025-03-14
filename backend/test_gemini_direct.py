#!/usr/bin/env python3
"""
Script pour tester directement le service Gemini sans passer par l'API Flask
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

def test_gemini_direct():
    """Tester directement le service Gemini"""
    try:
        # Afficher des informations sur l'environnement Python
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Python executable: {sys.executable}")
        logger.info(f"Python path: {sys.path}")
        
        # Essayer d'importer le package google.generativeai directement
        try:
            import google.generativeai
            logger.info(f"google.generativeai version: {google.generativeai.__version__}")
            GENAI_AVAILABLE = True
        except ImportError as e:
            logger.error(f"Erreur lors de l'importation de google.generativeai: {str(e)}")
            GENAI_AVAILABLE = False
        
        # Importer le service Gemini
        try:
            from services.gemini_service import GeminiService, GENAI_AVAILABLE as SERVICE_GENAI_AVAILABLE
            logger.info(f"GENAI_AVAILABLE dans le service: {SERVICE_GENAI_AVAILABLE}")
        except ImportError as e:
            logger.error(f"Erreur lors de l'importation du service Gemini: {str(e)}")
            return False
        
        if not GENAI_AVAILABLE:
            logger.error("Le package google-generativeai n'est pas disponible.")
            return False
        
        # Récupérer la clé API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("Clé API Gemini non trouvée dans les variables d'environnement.")
            return False
        
        logger.info(f"Clé API Gemini: {api_key[:5]}...{api_key[-5:]}")
        
        logger.info("Initialisation du service Gemini...")
        gemini_service = GeminiService(api_key=api_key)
        
        # Vérifier si le modèle a été initialisé
        if not gemini_service.model:
            logger.error("Le modèle Gemini n'a pas pu être initialisé.")
            return False
        
        logger.info("Modèle Gemini initialisé avec succès.")
        logger.info(f"Modèle utilisé: {gemini_service.model}")
        
        # Messages de test
        test_messages = [
            "Je veux acheter des chaussures de luxe pour 500 euros",
            "Comment investir 1000 euros?",
            "Bonjour, comment ça va?",
            "Je veux économiser de l'argent"
        ]
        
        for message in test_messages:
            logger.info(f"\nTest avec le message: '{message}'")
            
            # Obtenir une réponse du service Gemini
            try:
                response = gemini_service.get_response(
                    message=message,
                    system_prompt="Tu es un assistant financier qui aide les utilisateurs à gérer leur argent.",
                    conversation_history=[],
                    context_data={},
                    language="fr"
                )
                
                # Vérifier si la réponse est valide
                if response:
                    logger.info(f"Réponse reçue: '{response[:100]}...'")
                    logger.info("Test réussi!")
                else:
                    logger.error("Pas de réponse reçue.")
                    logger.error("Test échoué.")
            except Exception as e:
                logger.error(f"Erreur lors de l'obtention de la réponse: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                logger.error("Test échoué.")
        
        return True
    
    except Exception as e:
        logger.error(f"Erreur lors du test du service Gemini: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Fonction principale"""
    logger.info("=== Test direct du service Gemini ===")
    
    success = test_gemini_direct()
    
    if success:
        logger.info("\nTest du service Gemini réussi!")
        return 0
    else:
        logger.error("\nTest du service Gemini échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 