import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const TestChat = () => {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);

    // Fonction pour faire défiler vers le bas
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    // Faire défiler vers le bas quand les messages changent
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Ajouter des logs de débogage
    useEffect(() => {
        console.log('Messages actuels:', messages);
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        // Ajouter le message de l'utilisateur à la liste
        const userMessage = { sender: 'user', text: message };
        setMessages(prevMessages => [...prevMessages, userMessage]);
        console.log('Message utilisateur ajouté:', userMessage);

        setLoading(true);
        setError('');

        try {
            console.log('Envoi de la requête à l\'API:', message);
            const result = await axios.post('http://localhost:5000/api/chat', { message });
            console.log('Réponse de l\'API:', result);

            if (result.data && result.data.response) {
                setResponse(result.data.response);
                console.log('Texte de réponse:', result.data.response);

                // Ajouter le message du bot à la liste
                const botMessage = { sender: 'bot', text: result.data.response };
                console.log('Message bot à ajouter:', botMessage);
                setMessages(prevMessages => [...prevMessages, botMessage]);
                console.log('Messages après ajout du message bot:', [...messages, botMessage]);
            } else {
                console.error('Réponse invalide du serveur:', result.data);
                setError('Réponse invalide du serveur');

                // Ajouter un message d'erreur
                const errorMessage = {
                    sender: 'bot',
                    text: 'Désolé, je n\'ai pas pu générer une réponse. Veuillez réessayer.',
                    isError: true
                };
                setMessages(prevMessages => [...prevMessages, errorMessage]);
            }
        } catch (err) {
            console.error('Erreur lors de l\'envoi du message:', err);
            setError(err.message || 'Erreur lors de l\'envoi du message');

            // Ajouter un message d'erreur
            const errorMessage = {
                sender: 'bot',
                text: `Erreur: ${err.message || 'Erreur de connexion au serveur'}`,
                isError: true
            };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        } finally {
            setLoading(false);
            setMessage('');
        }
    };

    return (
        <div className="p-4 max-w-2xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">Test Chat</h1>

            <div className="border rounded-lg p-4 mb-4 min-h-[300px] max-h-[500px] overflow-y-auto">
                {messages.length === 0 ? (
                    <p className="text-gray-500">Pas de messages. Envoyez un message pour commencer la conversation.</p>
                ) : (
                    <div className="space-y-4">
                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`p-3 rounded-lg ${msg.sender === 'user'
                                    ? 'bg-blue-500 text-white ml-auto'
                                    : msg.isError
                                        ? 'bg-red-100 text-red-800'
                                        : 'bg-gray-200 text-gray-800'
                                    } max-w-[80%] ${msg.sender === 'user' ? 'ml-auto' : 'mr-auto'}`}
                            >
                                <pre className="whitespace-pre-wrap break-words font-sans">
                                    {msg.text || "Message vide"}
                                </pre>
                                {msg.sender === 'bot' && !msg.isError && (
                                    <div className="mt-2 text-xs text-gray-500">
                                        Bot
                                    </div>
                                )}
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                )}

                {loading && (
                    <div className="flex space-x-2 mt-4">
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                )}

                {error && (
                    <div className="text-red-500 mt-4">{error}</div>
                )}
            </div>

            <form onSubmit={handleSubmit} className="flex space-x-2">
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Tapez votre message..."
                    className="flex-1 p-2 border rounded-lg"
                />
                <button
                    type="submit"
                    disabled={loading || !message.trim()}
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                >
                    Envoyer
                </button>
            </form>

            <div className="mt-4">
                <h2 className="text-lg font-semibold mb-2">Messages de test rapides</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {[
                        "Je veux acheter des chaussures de luxe pour 500 euros",
                        "Comment investir 1000 euros?",
                        "Bonjour, comment ça va?",
                        "Je veux économiser de l'argent"
                    ].map((testMessage, index) => (
                        <button
                            key={index}
                            onClick={() => {
                                setMessage(testMessage);
                                setTimeout(() => {
                                    handleSubmit({ preventDefault: () => { } });
                                }, 100);
                            }}
                            className="p-2 text-sm bg-gray-100 hover:bg-gray-200 rounded text-left"
                        >
                            {testMessage}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default TestChat;
