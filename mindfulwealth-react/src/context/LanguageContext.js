import React, { createContext, useContext, useState, useEffect } from 'react';

// Translations
const translationData = {
  en: {
    // General
    appName: 'MindfulWealth',
    ai: 'AI',
    mindfulWealth: 'MindfulWealth',
    assistantDescription: 'Your AI Financial Assistant',
    personality: 'Personality',
    
    // Navigation
    profile: 'Profile',
    chat: 'Chat',
    dashboard: 'Dashboard',
    
    // Layout and Theme
    theme: 'Theme',
    dark: 'Dark',
    light: 'Light',
    layoutStyle: 'Layout Style',
    gradient: 'Gradient',
    modern: 'Modern',
    
    // Chat Interface
    typeMessage: 'Type your message...',
    clearConversation: 'Clear conversation',
    clearConfirm: 'Are you sure you want to clear the conversation history?',
    welcomeTitle: 'Welcome to MindfulWealth',
    welcomeMessage: 'I\'m your AI financial assistant. How can I help you today?',
    sampleQuestion1: 'Should I buy a new laptop for $1200?',
    sampleQuestion2: 'How can I save more money each month?',
    sampleQuestion3: 'Is it better to invest or pay off debt?',
    sampleQuestion4: 'What\'s a good budget for eating out?',
    financialContextDetected: 'Financial context detected in your message',
    processingError: 'Sorry, I couldn\'t process your financial context',
    
    // Demo responses
    demoNiceResponse1: 'That\'s a great question! I\'d be happy to help you make a wise financial decision about this.',
    demoNiceResponse2: 'I understand your financial concerns. Let\'s look at this from a budget perspective.',
    demoNiceResponse3: 'Thanks for sharing that with me. I can definitely help you evaluate if this is a good financial move.',
    demoSarcasticResponse1: 'Oh sure, because money grows on trees! Let\'s see if this is actually worth your hard-earned cash.',
    demoSarcasticResponse2: 'Wow, another shopping opportunity! Let me check if your bank account will be crying after this one.',
    demoSarcasticResponse3: 'Ah, the eternal question of "should I spend money on things I probably don\'t need?" Let\'s find out!',
    
    // Personality
    nice: 'Nice',
    direct: 'Direct',
    analytical: 'Analytical',
    switchedToNice: "I'll be supportive and encouraging.",
    switchedToDirect: "I'll be straightforward and to the point.",
    switchedToAnalytical: "I'll be data-driven and thorough.",
    switchedTo: 'Switched to',
    mode: 'mode',
    personalityNice: 'Nice',
    personalityDirect: 'Direct',
    personalityAnalytical: 'Analytical',
    personalityNiceDesc: 'Warm, supportive, and encouraging',
    personalityDirectDesc: 'Straightforward, concise, and to the point',
    personalityAnalyticalDesc: 'Data-driven, detailed, and thorough',
    
    // User Profile
    userSettings: 'User Settings',
    name: 'Name',
    email: 'Email',
    financialSettings: 'Financial Settings',
    preferredCurrency: 'Preferred Currency',
    monthlySavingsGoal: 'Monthly Savings Goal',
    monthlyBudget: 'Monthly Budget',
    appSettings: 'App Settings',
    assistantPersonality: 'Assistant Personality',
    enableNotifications: 'Enable Notifications',
    privacy: 'Privacy',
    clearHistory: 'Clear Conversation History',
    clearHistoryWarning: 'This will permanently delete all your conversation history with the financial assistant.',
    language: 'Language',
    english: 'English',
    french: 'French',
    
    // Dashboard
    financialDashboard: 'Financial Dashboard',
    remaining: 'remaining',
    spent: 'Spent',
    toGo: 'to go',
    saved: 'Saved',
    impulsePurchasesAvoided: 'Impulse Purchases Avoided',
    itemsSaved: 'items saved',
    thisMonth: 'This Month',
    savingsHistory: 'Savings History',
    spendingByCategory: 'Spending by Category',
    recentImpulseDecisions: 'Recent Impulse Decisions',
    ofBudgetUsed: 'of budget used',
    averageSavings: 'Average Savings',
    goalProgress: 'Goal Progress',
    totalSpent: 'Total Spent',
    totalBudget: 'Total Budget',
    ofBudget: 'of budget',
    ofTotal: 'of total',
    noImpulsePurchases: 'No impulse purchase decisions yet',
    totalSaved: 'Total Saved',
    
    // Dashboard Charts
    income: 'Income',
    expenses: 'Expenses',
    savingsRate: 'Savings Rate',
    housing: 'Housing',
    food: 'Food',
    transportation: 'Transportation',
    entertainment: 'Entertainment',
    utilities: 'Utilities',
    other: 'Other',
    incomeVsExpenses: 'Income vs Expenses',
    expenseBreakdown: 'Expense Breakdown',
    financialSummary: 'Financial Summary',
    currentMonthIncome: 'Current Month Income',
    currentMonthExpenses: 'Current Month Expenses',
    currentSavingsRate: 'Current Savings Rate',
    biggestExpenseCategory: 'Biggest Expense Category',
    
    // Tip of the day
    tipOfTheDay: 'Tip of the day',
    tip1: 'Small daily savings add up to big results over time. Try the 50/30/20 rule for budgeting!',
    tip2: 'Consider automating your savings to make it easier to stick to your financial goals.',
    tip3: 'Before making a large purchase, wait 24 hours to avoid impulse buying.',
    tip4: 'Track your expenses for a month to identify areas where you can cut back.',
    tip5: 'Pay yourself first by setting aside savings as soon as you receive income.',
    
    // Personality Settings
    personalitySettings: 'Personality Settings',
    personalitySettingsDesc: 'Choose how your AI assistant communicates with you',
  },
  fr: {
    // General
    appName: 'MindfulWealth',
    ai: 'IA',
    mindfulWealth: 'MindfulWealth',
    assistantDescription: 'Votre Assistant Financier IA',
    personality: 'Personnalité',
    
    // Navigation
    profile: 'Profil',
    chat: 'Discussion',
    dashboard: 'Tableau de bord',
    
    // Layout and Theme
    theme: 'Thème',
    dark: 'Sombre',
    light: 'Clair',
    layoutStyle: 'Style de mise en page',
    gradient: 'Gradient',
    modern: 'Moderne',
    
    // Chat Interface
    typeMessage: 'Tapez votre message...',
    clearConversation: 'Effacer la conversation',
    clearConfirm: 'Êtes-vous sûr de vouloir effacer l\'historique de conversation?',
    welcomeTitle: 'Bienvenue sur MindfulWealth',
    welcomeMessage: 'Je suis votre assistant financier IA. Comment puis-je vous aider aujourd\'hui?',
    sampleQuestion1: 'Devrais-je acheter un nouvel ordinateur portable à 1200€?',
    sampleQuestion2: 'Comment puis-je économiser plus d\'argent chaque mois?',
    sampleQuestion3: 'Est-il préférable d\'investir ou de rembourser ses dettes?',
    sampleQuestion4: 'Quel est un bon budget pour les repas au restaurant?',
    financialContextDetected: 'Contexte financier détecté dans votre message',
    processingError: 'Désolé, je n\'ai pas pu traiter votre contexte financier',
    
    // Demo responses
    demoNiceResponse1: 'C\'est une excellente question! Je serais ravi de vous aider à prendre une décision financière judicieuse à ce sujet.',
    demoNiceResponse2: 'Je comprends vos préoccupations financières. Examinons cela du point de vue du budget.',
    demoNiceResponse3: 'Merci de partager cela avec moi. Je peux certainement vous aider à évaluer si c\'est un bon mouvement financier.',
    demoSarcasticResponse1: 'Oh bien sûr, parce que l\'argent pousse sur les arbres! Voyons si cela vaut vraiment votre argent durement gagné.',
    demoSarcasticResponse2: 'Wow, une autre opportunité de shopping! Voyons si votre compte bancaire va pleurer après celle-ci.',
    demoSarcasticResponse3: 'Ah, l\'éternelle question de "devrais-je dépenser de l\'argent pour des choses dont je n\'ai probablement pas besoin?" Découvrons-le!',
    
    // Personality
    nice: 'Gentil',
    direct: 'Direct',
    analytical: 'Analytique',
    switchedToNice: "Je serai encourageant et bienveillant.",
    switchedToDirect: "Je serai direct et précis.",
    switchedToAnalytical: "Je serai axé sur les données et approfondi.",
    switchedTo: 'Passé en mode',
    mode: '',
    personalityNice: 'Amical',
    personalityDirect: 'Direct',
    personalityAnalytical: 'Analytique',
    personalityNiceDesc: 'Chaleureux, encourageant et bienveillant',
    personalityDirectDesc: 'Franc, concis et précis',
    personalityAnalyticalDesc: 'Axé sur les données, détaillé et approfondi',
    
    // User Profile
    userSettings: 'Paramètres Utilisateur',
    name: 'Nom',
    email: 'Email',
    financialSettings: 'Paramètres Financiers',
    preferredCurrency: 'Devise Préférée',
    monthlySavingsGoal: 'Objectif d\'Épargne Mensuel',
    monthlyBudget: 'Budget Mensuel',
    appSettings: 'Paramètres de l\'Application',
    assistantPersonality: 'Personnalité de l\'Assistant',
    enableNotifications: 'Activer les Notifications',
    privacy: 'Confidentialité',
    clearHistory: 'Effacer l\'Historique de Conversation',
    clearHistoryWarning: 'Cela supprimera définitivement tout votre historique de conversation avec l\'assistant financier.',
    language: 'Langue',
    english: 'Anglais',
    french: 'Français',
    
    // Dashboard
    financialDashboard: 'Tableau de Bord Financier',
    remaining: 'restant',
    spent: 'Dépensé',
    toGo: 'à atteindre',
    saved: 'Économisé',
    impulsePurchasesAvoided: 'Achats Impulsifs Évités',
    itemsSaved: 'articles économisés',
    thisMonth: 'Ce Mois',
    savingsHistory: 'Historique d\'Épargne',
    spendingByCategory: 'Dépenses par Catégorie',
    recentImpulseDecisions: 'Décisions d\'Achat Impulsif Récentes',
    ofBudgetUsed: 'du budget utilisé',
    averageSavings: 'Épargne Moyenne',
    goalProgress: 'Progression vers l\'Objectif',
    totalSpent: 'Total Dépensé',
    totalBudget: 'Budget Total',
    ofBudget: 'du budget',
    ofTotal: 'du total',
    noImpulsePurchases: 'Pas encore de décisions d\'achat impulsif',
    totalSaved: 'Total Économisé',
    
    // Dashboard Charts
    income: 'Revenu',
    expenses: 'Dépenses',
    savingsRate: 'Taux d\'Épargne',
    housing: 'Logement',
    food: 'Alimentation',
    transportation: 'Transport',
    entertainment: 'Divertissement',
    utilities: 'Services',
    other: 'Autre',
    incomeVsExpenses: 'Revenus vs Dépenses',
    expenseBreakdown: 'Répartition des Dépenses',
    financialSummary: 'Résumé Financier',
    currentMonthIncome: 'Revenu du Mois Actuel',
    currentMonthExpenses: 'Dépenses du Mois Actuel',
    currentSavingsRate: 'Taux d\'Épargne Actuel',
    biggestExpenseCategory: 'Plus Grande Catégorie de Dépenses',
    
    // Tip of the day
    tipOfTheDay: 'Conseil du jour',
    tip1: 'Les petites économies quotidiennes s\'additionnent pour donner de grands résultats. Essayez la règle 50/30/20 pour votre budget!',
    tip2: 'Envisagez d\'automatiser vos économies pour faciliter le respect de vos objectifs financiers.',
    tip3: 'Avant de faire un achat important, attendez 24 heures pour éviter les achats impulsifs.',
    tip4: 'Suivez vos dépenses pendant un mois pour identifier les domaines où vous pouvez réduire.',
    tip5: 'Payez-vous d\'abord en mettant de côté des économies dès que vous recevez un revenu.',
    
    // Personality Settings
    personalitySettings: 'Paramètres de Personnalité',
    personalitySettingsDesc: 'Choisissez comment votre assistant IA communique avec vous',
  }
};

const LanguageContext = createContext();

export const useLanguage = () => useContext(LanguageContext);

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    const savedLanguage = localStorage.getItem('language');
    return savedLanguage || 'en';
  });

  const [translations, setTranslations] = useState(() => {
    const lang = localStorage.getItem('language') || 'en';
    return translationData[lang];
  });

  useEffect(() => {
    localStorage.setItem('language', language);
    setTranslations(translationData[language]);
  }, [language]);

  const changeLanguage = (lang) => {
    setLanguage(lang);
  };

  const t = (key) => {
    return translations[key] || key;
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        changeLanguage,
        t,
        translations
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export default LanguageContext; 