/**
 * Extracts financial context from a user message
 * @param {string} message - The user's message
 * @param {object} currentContext - The current conversation context
 * @returns {object|null} - Updated context or null if no financial data found
 */
export const extractFinancialContext = (message, currentContext) => {
  // Extract amount and currency
  const amountMatch = message.match(
    /(\d+(?:\.\d+)?)\s*(euros?|€|pounds?|£|dollars?|\$|USD|GBP|EUR)/i
  );

  // Extract item being purchased
  const itemMatch = message.match(
    /(spent|buying|bought|purchase[d]?|for)\s+(?:[\w\s]+\s+)?(?:on|in|for)\s+([\w\s]+)/i
  );

  // If we found both amount and item
  if (amountMatch && itemMatch) {
    const amount = parseFloat(amountMatch[1]);
    const item = itemMatch[2].trim();

    // Determine currency
    let currency = "EUR"; // Default
    if (
      amountMatch[2].includes("$") ||
      amountMatch[2].toLowerCase().includes("dollar") ||
      amountMatch[2].includes("USD")
    ) {
      currency = "USD";
    } else if (
      amountMatch[2].includes("£") ||
      amountMatch[2].toLowerCase().includes("pound") ||
      amountMatch[2].includes("GBP")
    ) {
      currency = "GBP";
    }

    // Determine if this is likely an impulse or reasonable purchase
    const reasonableCategories = [
      "groceries",
      "food",
      "rent",
      "bills",
      "utilities",
      "healthcare",
      "medical",
      "education",
    ];
    const isReasonable = reasonableCategories.some((cat) =>
      item.toLowerCase().includes(cat)
    );

    // Create updated context
    const updatedContext = {
      lastMentionedAmount: amount,
      lastMentionedCurrency: currency,
      lastMentionedItem: item,
      lastDetectedType: isReasonable ? "reasonable" : "impulse",
      ongoingDiscussion: true,
    };

    // Initialize or update arrays
    if (!currentContext.mentionedItems) {
      updatedContext.mentionedItems = [item];
    } else if (!currentContext.mentionedItems.includes(item)) {
      updatedContext.mentionedItems = [...currentContext.mentionedItems, item];
    }

    if (!currentContext.mentionedAmounts) {
      updatedContext.mentionedAmounts = [];
    }

    updatedContext.mentionedAmounts = [
      ...(currentContext.mentionedAmounts || []),
      {
        amount,
        currency,
        timestamp: new Date().toISOString(),
      },
    ];

    // Start a discussion if not already ongoing
    if (!currentContext.ongoingDiscussion) {
      updatedContext.discussionStartTime = new Date().toISOString();
    }

    return updatedContext;
  }

  // If we only found an amount but no item
  if (amountMatch && !itemMatch) {
    // Check for common expense categories in the message
    const categories = [
      "food",
      "groceries",
      "rent",
      "bills",
      "clothes",
      "electronics",
      "dinner",
      "lunch",
      "coffee",
      "shoes",
    ];
    let detectedCategory = null;

    for (const category of categories) {
      if (message.toLowerCase().includes(category)) {
        detectedCategory = category;
        break;
      }
    }

    if (detectedCategory) {
      // We found a category mentioned in the message
      const amount = parseFloat(amountMatch[1]);

      // Determine currency
      let currency = "EUR"; // Default
      if (
        amountMatch[2].includes("$") ||
        amountMatch[2].toLowerCase().includes("dollar") ||
        amountMatch[2].includes("USD")
      ) {
        currency = "USD";
      } else if (
        amountMatch[2].includes("£") ||
        amountMatch[2].toLowerCase().includes("pound") ||
        amountMatch[2].includes("GBP")
      ) {
        currency = "GBP";
      }

      // Determine if this is likely an impulse or reasonable purchase
      const reasonableCategories = [
        "groceries",
        "food",
        "rent",
        "bills",
        "utilities",
        "healthcare",
        "medical",
        "education",
      ];
      const isReasonable = reasonableCategories.some((cat) =>
        detectedCategory.toLowerCase().includes(cat)
      );

      // Create updated context
      const updatedContext = {
        lastMentionedAmount: amount,
        lastMentionedCurrency: currency,
        lastMentionedItem: detectedCategory,
        lastDetectedType: isReasonable ? "reasonable" : "impulse",
        ongoingDiscussion: true,
      };

      // Initialize or update arrays
      if (!currentContext.mentionedItems) {
        updatedContext.mentionedItems = [detectedCategory];
      } else if (!currentContext.mentionedItems.includes(detectedCategory)) {
        updatedContext.mentionedItems = [...currentContext.mentionedItems, detectedCategory];
      }

      if (!currentContext.mentionedAmounts) {
        updatedContext.mentionedAmounts = [];
      }

      updatedContext.mentionedAmounts = [
        ...(currentContext.mentionedAmounts || []),
        {
          amount,
          currency,
          timestamp: new Date().toISOString(),
        },
      ];

      // Start a discussion if not already ongoing
      if (!currentContext.ongoingDiscussion) {
        updatedContext.discussionStartTime = new Date().toISOString();
      }

      return updatedContext;
    }
  }

  return null;
};

/**
 * Updates context based on bot response
 * @param {object} financialData - Financial data from the response
 * @param {string} responseText - The bot's response text
 * @param {object} currentContext - The current conversation context
 * @returns {object} - Updated context
 */
export const updateContextFromResponse = (financialData, responseText, currentContext) => {
  const updatedContext = { ...currentContext };
  
  if (!financialData) return updatedContext;

  // Update context with financial data from response
  if (financialData.amount && financialData.category) {
    // Update last mentioned values
    updatedContext.lastMentionedAmount = financialData.amount;
    updatedContext.lastMentionedItem = financialData.category;
    updatedContext.lastDetectedType = financialData.type || "unknown";

    // Add to history arrays if not already present
    if (!updatedContext.mentionedItems.includes(financialData.category)) {
      updatedContext.mentionedItems = [...updatedContext.mentionedItems, financialData.category];
    }

    updatedContext.mentionedAmounts = [
      ...(updatedContext.mentionedAmounts || []),
      {
        amount: financialData.amount,
        currency: updatedContext.lastMentionedCurrency || "EUR",
        timestamp: new Date().toISOString(),
      },
    ];
  }

  // Extract potential follow-up questions from the response
  const questionMatch = responseText.match(/\?([^.!?]*)(?:[.!?]|$)/g);
  if (questionMatch) {
    const questions = questionMatch.map((q) => q.trim());

    // Add to follow-up questions array
    if (!updatedContext.followUpQuestions) {
      updatedContext.followUpQuestions = [];
    }

    const newQuestions = questions.map(question => ({
      question,
      timestamp: new Date().toISOString(),
      isGenerated: false,
    }));

    updatedContext.followUpQuestions = [
      ...(updatedContext.followUpQuestions || []),
      ...newQuestions
    ];
  }

  // Mark that we have an ongoing discussion
  updatedContext.ongoingDiscussion = true;
  updatedContext.lastResponseTime = new Date().toISOString();

  return updatedContext;
};

/**
 * Generates a demo response for testing
 * @param {string} text - The user's message
 * @param {Array} conversationHistory - Previous messages
 * @param {string} personalityMode - The current personality mode
 * @param {object} context - The current conversation context
 * @returns {object} - Demo response with financial data
 */
export const processDemoMessage = (text, conversationHistory = [], personalityMode = 'nice', context = {}) => {
  // Check if we're in an ongoing conversation about a previous purchase
  const isFollowUp =
    conversationHistory.length >= 2 &&
    context.ongoingDiscussion;

  // Get the last few messages for context
  const lastMessages = conversationHistory
    .slice(-3)
    .map((msg) => msg.content?.toLowerCase() || '');
  
  const lastUserMessages = conversationHistory
    .filter((msg) => msg.role === "user")
    .slice(-2)
    .map((msg) => msg.content?.toLowerCase() || '');

  // Check if there's a specific follow-up pattern
  const isAskingForDetails = lastMessages.some(
    (msg) =>
      msg.includes("tell me more") ||
      msg.includes("why did you") ||
      msg.includes("what made you")
  );

  const isConfirmingImpulse = text
    .toLowerCase()
    .match(/impulse|moment|quick|spur|spontaneous|unplanned/);
  const isClaimingPlanned = text
    .toLowerCase()
    .match(/planned|needed|necessary|essential|thought about|saving for/);

  // If this is a follow-up to a previous financial discussion
  if (isFollowUp) {
    const {
      lastMentionedItem,
      lastMentionedAmount,
      lastMentionedCurrency,
      lastDetectedType,
    } = context;

    // If user is explaining why they made a purchase (responding to "tell me more")
    if (isAskingForDetails) {
      if (personalityMode === "sarcastic") {
        return {
          response: `Ah, I see! Well, thanks for that fascinating glimpse into your shopping psychology. So you're saying these ${lastMentionedItem} were worth parting with ${lastMentionedAmount} ${
            lastMentionedCurrency || "euros"
          }? I mean, who needs retirement funds when you have fashion, right? 😜 But seriously, was this more of a planned purchase or a spontaneous decision?`,
          financialData: null,
        };
      } else {
        return {
          response: `Thank you for sharing that context. It helps me understand your purchasing decisions better. Would you say this was something you had planned to buy for a while, or was it more of a spontaneous decision?`,
          financialData: null,
        };
      }
    }

    // Check if user is confirming it was an impulse purchase
    if (isConfirmingImpulse) {
      if (personalityMode === "sarcastic") {
        return {
          response: `Ah, the classic impulse buy! 🛍️ Don't worry, we've all been there - that moment when your wallet makes decisions before your brain catches up! Those ${lastMentionedAmount} ${
            lastMentionedCurrency || "euros"
          } might be walking away on your feet now, but just think - that same money could have been making little euro babies in an investment account! Next time that impulse hits, maybe give me a quick chat first? I promise I'll only judge you a little bit! 😜`,
          financialData: null,
        };
      } else {
        return {
          response: `I understand. Impulse purchases happen to everyone. I've added these ${lastMentionedItem} to your impulse tracker. Next time you feel the urge to make an unplanned purchase, try checking in with me first - I can help you evaluate whether it's worth it in the long run.`,
          financialData: null,
        };
      }
    }

    // Check if user is saying it was a planned purchase
    if (isClaimingPlanned) {
      if (personalityMode === "sarcastic") {
        return {
          response: `Oh, so you're telling me those ${lastMentionedItem} were a carefully planned financial decision? 🤔 Well, aren't you the responsible one! I'll move this from the "impulse buy" category to "totally necessary purchases." Your financial advisor would be so proud! 👏`,
          financialData: {
            type: "reasonable",
            amount: lastMentionedAmount,
            category: lastMentionedItem,
            budget_allocation: true,
          },
        };
      } else {
        return {
          response: `That's great to hear you planned for this purchase! I've updated my records to categorize these ${lastMentionedItem} as a planned expense rather than an impulse buy. Planning purchases in advance is a great financial habit.`,
          financialData: {
            type: "reasonable",
            amount: lastMentionedAmount,
            category: lastMentionedItem,
            budget_allocation: true,
          },
        };
      }
    }

    // If the user is asking about investment potential
    if (text.toLowerCase().match(/invest|investment|growth|return|potential/)) {
      const amount = lastMentionedAmount || 100;
      const oneYearValue = Math.round(amount * 1.08 * 100) / 100;
      const fiveYearValue = Math.round(amount * Math.pow(1.08, 5) * 100) / 100;

      if (personalityMode === "sarcastic") {
        return {
          response: `Ah, now you're speaking my language! 💰 If you'd invested that ${amount} instead of buying ${lastMentionedItem}, you could have had ${oneYearValue} in just a year, or a whopping ${fiveYearValue} after five years! But hey, I'm sure those ${lastMentionedItem} will totally still be in style five years from now... 😏`,
          financialData: {
            type: "impulse",
            amount: amount,
            category: lastMentionedItem,
            potential_value_1yr: oneYearValue,
            potential_value_5yr: fiveYearValue,
          },
        };
      } else {
        return {
          response: `Great question about the investment potential! If you had invested ${amount} instead of purchasing the ${lastMentionedItem}, it could have grown to approximately ${oneYearValue} in one year or ${fiveYearValue} in five years, assuming an 8% annual return. Would you like me to help you set up a savings goal for future purchases?`,
          financialData: {
            type: "impulse",
            amount: amount,
            category: lastMentionedItem,
            potential_value_1yr: oneYearValue,
            potential_value_5yr: fiveYearValue,
          },
        };
      }
    }
  }

  // Check for initial financial statements about shoes
  if (
    text.toLowerCase().includes("shoes") &&
    (text.toLowerCase().includes("100") || text.toLowerCase().includes("euros"))
  ) {
    if (personalityMode === "sarcastic") {
      return {
        response:
          "Hey there! Shoes, huh? 👠 Well, aren't we feeling fancy today? I love shoes too, but let's see what the future you thinks about this purchase! 😉 Just so you know, that 100 euros could have been doing some serious growing! If you'd invested it instead, you could have had 108 euros in a year, or even 146.93 euros in five years! 😮 But hey, at least you'll be stepping out in style! 😎 Was it a pair you've been eyeing for a while, or a total spur-of-the-moment thing?",
        financialData: {
          type: "impulse",
          amount: 100,
          category: "shoes",
          potential_value_1yr: 108,
          potential_value_5yr: 146.93,
        },
      };
    } else {
      return {
        response:
          "I see you spent 100 euros on shoes. If you had invested this amount instead, it could grow to approximately 108 euros in one year or 146.93 euros in five years. Would you like me to add this to your impulse purchases tracker?",
        financialData: {
          type: "impulse",
          amount: 100,
          category: "shoes",
          potential_value_1yr: 108,
          potential_value_5yr: 146.93,
        },
      };
    }
  }

  // Check for other financial statements with amounts and items
  const amountMatch = text.match(
    /(\d+(?:\.\d+)?)\s*(euros?|€|pounds?|£|dollars?|\$|USD|GBP|EUR)/i
  );
  const itemMatch = text.match(
    /(spent|buying|bought|purchase[d]?|for)\s+(?:[\w\s]+\s+)?(?:on|in|for)\s+([\w\s]+)/i
  );

  if (
    amountMatch &&
    (itemMatch ||
      text
        .toLowerCase()
        .match(
          /food|groceries|rent|bills|clothes|electronics|dinner|lunch|coffee/
        ))
  ) {
    const amount = parseFloat(amountMatch[1]);
    let item = itemMatch ? itemMatch[2].trim() : null;

    // If no specific item was matched but we have keywords, use them
    if (!item) {
      const keywords = [
        "food",
        "groceries",
        "rent",
        "bills",
        "clothes",
        "electronics",
        "dinner",
        "lunch",
        "coffee",
      ];
      for (const keyword of keywords) {
        if (text.toLowerCase().includes(keyword)) {
          item = keyword;
          break;
        }
      }
    }

    if (item) {
      // Determine if this is likely an impulse or reasonable purchase
      const reasonableCategories = [
        "groceries",
        "food",
        "rent",
        "bills",
        "utilities",
        "healthcare",
        "medical",
        "education",
      ];
      const isReasonable = reasonableCategories.some((cat) =>
        item.toLowerCase().includes(cat)
      );

      if (isReasonable) {
        if (personalityMode === "sarcastic") {
          return {
            response: `${amount} on ${item}? Well, I suppose that's a reasonable expense. I've added it to your budget, though I'm sure you could have found a better deal if you tried. 😏`,
            financialData: {
              type: "reasonable",
              amount: amount,
              category: item,
              budget_allocation: true,
            },
          };
        } else {
          return {
            response: `I've recorded your ${amount} expense for ${item}. This looks like a necessary purchase, so I've added it to your monthly budget. Is there anything else you'd like me to track?`,
            financialData: {
              type: "reasonable",
              amount: amount,
              category: item,
              budget_allocation: true,
            },
          };
        }
      } else {
        // Calculate potential investment growth
        const oneYearValue = Math.round(amount * 1.08 * 100) / 100;
        const fiveYearValue =
          Math.round(amount * Math.pow(1.08, 5) * 100) / 100;

        if (personalityMode === "sarcastic") {
          return {
            response: `Another impulse buy, huh? 🛍️ That ${amount} on ${item} could have been ${oneYearValue} in just a year if invested! Or even ${fiveYearValue} after five years! But hey, who needs financial security when you have ${item}, right? 😜 Was this a spontaneous purchase or something you've been planning?`,
            financialData: {
              type: "impulse",
              amount: amount,
              category: item,
              potential_value_1yr: oneYearValue,
              potential_value_5yr: fiveYearValue,
            },
          };
        } else {
          return {
            response: `I see you spent ${amount} on ${item}. If you had invested this amount instead, it could grow to approximately ${oneYearValue} in one year or ${fiveYearValue} in five years. Would you like me to add this to your impulse purchases tracker?`,
            financialData: {
              type: "impulse",
              amount: amount,
              category: item,
              potential_value_1yr: oneYearValue,
              potential_value_5yr: fiveYearValue,
            },
          };
        }
      }
    }
  }

  // Default response if no specific pattern is matched
  return {
    response:
      personalityMode === "sarcastic"
        ? "I'm not quite sure what you're asking about. Care to share some financial decisions you're pondering? Maybe something you're thinking of buying? I promise my judgment will be only slightly cutting! 😉"
        : "I'm here to help with your financial decisions. Feel free to tell me about any purchases you're considering or expenses you want to track.",
    financialData: null,
  };
}; 