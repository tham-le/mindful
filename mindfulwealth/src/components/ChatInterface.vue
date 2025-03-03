<template>
  <div class="chat-container">
    <div class="chat-interface">
      <div class="chat-header">
        <h2>Financial Assistant</h2>
        <div class="personality-toggle">
          <span
            :class="{ active: personalityMode === 'nice' }"
            @click="togglePersonalityMode('nice')"
          >
            Nice
          </span>
          <span class="toggle-divider">|</span>
          <span
            :class="{ active: personalityMode === 'sarcastic' }"
            @click="togglePersonalityMode('sarcastic')"
          >
            Sarcastic
          </span>
        </div>
      </div>

      <div class="messages-container" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="[
            'message',
            message.role === 'user' ? 'user-message' : 'bot-message',
          ]"
        >
          <div class="message-content">
            {{ message.content }}
          </div>
          <div class="message-time">
            {{
              new Date(message.timestamp).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })
            }}
          </div>
        </div>
        <div v-if="isLoading" class="message bot-message typing">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>

      <div class="input-container">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Type your message..."
          :disabled="isLoading"
        />
        <button
          @click="sendMessage"
          :disabled="!newMessage.trim() || isLoading"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from "vue";
import api from "../services/api";
import axios from "axios";

const props = defineProps({
  initialMessages: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["message-sent", "financial-data-detected"]);

// State
const messages = ref(
  props.initialMessages.length
    ? [...props.initialMessages]
    : [
        {
          text: "Hello! I'm your MindfulWealth assistant. How can I help you with your financial decisions today?",
          sender: "bot",
        },
      ]
);
const newMessage = ref("");
const isLoading = ref(false);
const messagesContainer = ref(null);
const personalityMode = ref("nice");

// Conversation context tracking
const conversationContext = ref({
  // Current financial context
  lastMentionedAmount: null,
  lastMentionedCurrency: null,
  lastMentionedItem: null,
  lastDetectedType: null, // "impulse" or "reasonable"
  ongoingDiscussion: false,

  // Historical context
  discussionStartTime: null,
  lastResponseTime: null,
  mentionedItems: [],
  mentionedAmounts: [],

  // Conversation flow
  followUpQuestions: [],
  userResponses: [],
});

// Computed properties for context
const hasActiveFinancialContext = computed(() => {
  return (
    conversationContext.value.lastMentionedAmount !== null &&
    conversationContext.value.lastMentionedItem !== null &&
    conversationContext.value.ongoingDiscussion === true
  );
});

// Methods
const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatMessage = (text) => {
  // Convert URLs to clickable links
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return text.replace(urlRegex, (url) => {
    return `<a href="${url}" target="_blank">${url}</a>`;
  });
};

const togglePersonalityMode = async (mode) => {
  try {
    await api.setPersonalityMode(mode);
    personalityMode.value = mode;

    // Add a message from the bot indicating the mode change
    messages.value.push({
      text: `Switched to ${mode} mode. ${
        mode === "nice"
          ? "I'll be supportive and encouraging."
          : "Prepare for some witty remarks!"
      }`,
      sender: "bot",
    });

    scrollToBottom();
  } catch (error) {
    console.error("Error setting personality mode:", error);
  }
};

const extractFinancialContext = (message) => {
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

    // Update context
    conversationContext.value.lastMentionedAmount = amount;
    conversationContext.value.lastMentionedCurrency = currency;
    conversationContext.value.lastMentionedItem = item;
    conversationContext.value.lastDetectedType = isReasonable
      ? "reasonable"
      : "impulse";

    // Initialize or update arrays
    if (!conversationContext.value.mentionedItems) {
      conversationContext.value.mentionedItems = [item];
    } else if (!conversationContext.value.mentionedItems.includes(item)) {
      conversationContext.value.mentionedItems.push(item);
    }

    if (!conversationContext.value.mentionedAmounts) {
      conversationContext.value.mentionedAmounts = [];
    }

    conversationContext.value.mentionedAmounts.push({
      amount,
      currency,
      timestamp: new Date().toISOString(),
    });

    // Start a discussion if not already ongoing
    if (!conversationContext.value.ongoingDiscussion) {
      conversationContext.value.ongoingDiscussion = true;
      conversationContext.value.discussionStartTime = new Date().toISOString();
    }

    // Initialize other tracking arrays if needed
    if (!conversationContext.value.followUpQuestions) {
      conversationContext.value.followUpQuestions = [];
    }

    if (!conversationContext.value.userResponses) {
      conversationContext.value.userResponses = [];
    }

    return true;
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

      // Update context
      conversationContext.value.lastMentionedAmount = amount;
      conversationContext.value.lastMentionedCurrency = currency;
      conversationContext.value.lastMentionedItem = detectedCategory;
      conversationContext.value.lastDetectedType = isReasonable
        ? "reasonable"
        : "impulse";

      // Initialize or update arrays
      if (!conversationContext.value.mentionedItems) {
        conversationContext.value.mentionedItems = [detectedCategory];
      } else if (
        !conversationContext.value.mentionedItems.includes(detectedCategory)
      ) {
        conversationContext.value.mentionedItems.push(detectedCategory);
      }

      if (!conversationContext.value.mentionedAmounts) {
        conversationContext.value.mentionedAmounts = [];
      }

      conversationContext.value.mentionedAmounts.push({
        amount,
        currency,
        timestamp: new Date().toISOString(),
      });

      // Start a discussion if not already ongoing
      if (!conversationContext.value.ongoingDiscussion) {
        conversationContext.value.ongoingDiscussion = true;
        conversationContext.value.discussionStartTime =
          new Date().toISOString();
      }

      return true;
    }
  }

  return false;
};

const updateContextFromResponse = (financialData, responseText) => {
  if (!financialData) return;

  // Update context with financial data from response
  if (financialData.amount && financialData.category) {
    // Update last mentioned values
    conversationContext.value.lastMentionedAmount = financialData.amount;
    conversationContext.value.lastMentionedItem = financialData.category;
    conversationContext.value.lastDetectedType =
      financialData.type || "unknown";

    // Add to history arrays if not already present
    if (
      !conversationContext.value.mentionedItems.includes(financialData.category)
    ) {
      conversationContext.value.mentionedItems.push(financialData.category);
    }

    conversationContext.value.mentionedAmounts.push({
      amount: financialData.amount,
      currency: conversationContext.value.lastMentionedCurrency || "EUR",
      timestamp: new Date().toISOString(),
    });
  }

  // Extract potential follow-up questions from the response
  const questionMatch = responseText.match(/\?([^.!?]*)(?:[.!?]|$)/g);
  if (questionMatch) {
    const questions = questionMatch.map((q) => q.trim());

    // Add to follow-up questions array
    if (!conversationContext.value.followUpQuestions) {
      conversationContext.value.followUpQuestions = [];
    }

    questions.forEach((question) => {
      conversationContext.value.followUpQuestions.push({
        question,
        timestamp: new Date().toISOString(),
        isGenerated: false,
      });
    });
  }

  // Mark that we have an ongoing discussion
  conversationContext.value.ongoingDiscussion = true;
};

const generateContextualFollowUp = () => {
  if (!hasActiveFinancialContext.value) return null;

  const { lastMentionedAmount, lastMentionedItem, lastDetectedType } =
    conversationContext.value;

  if (lastDetectedType === "impulse") {
    return personalityMode.value === "nice"
      ? `Was this ${lastMentionedItem} purchase planned, or was it more of a spontaneous decision?`
      : `So, did you actually need those ${lastMentionedItem}, or was it just another impulse buy? 😏`;
  } else if (lastDetectedType === "reasonable") {
    return personalityMode.value === "nice"
      ? `I've added this ${lastMentionedItem} expense to your budget. Is there anything else you'd like to track?`
      : `Fine, I'll add your ${lastMentionedItem} to the "actually responsible purchases" list. Anything else you want to confess? 😉`;
  }

  return null;
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  // Add user message to the conversation
  const userMessage = {
    role: "user",
    content: newMessage.value,
    timestamp: new Date().toISOString(),
  };
  messages.value.push(userMessage);

  // Extract financial context from the user message
  extractFinancialContext(newMessage.value);

  // Clear input and scroll to bottom
  newMessage.value = "";
  scrollToBottom();

  // Show typing indicator
  isLoading.value = true;

  try {
    // Prepare context data for the API
    const contextData = {
      // Current financial context
      currentContext: {
        lastMentionedAmount: conversationContext.value.lastMentionedAmount,
        lastMentionedCurrency: conversationContext.value.lastMentionedCurrency,
        lastMentionedItem: conversationContext.value.lastMentionedItem,
        lastDetectedType: conversationContext.value.lastDetectedType,
        ongoingDiscussion: conversationContext.value.ongoingDiscussion,
      },
      // Historical context
      historicalContext: {
        mentionedItems: conversationContext.value.mentionedItems || [],
        mentionedAmounts: conversationContext.value.mentionedAmounts || [],
        discussionStartTime: conversationContext.value.discussionStartTime,
        followUpQuestions: conversationContext.value.followUpQuestions || [],
      },
      // Conversation flow
      conversationFlow: {
        personalityMode: personalityMode.value,
        messageCount: messages.value.length,
        lastUserResponses: conversationContext.value.userResponses || [],
      },
    };

    // For demo purposes, we'll use a mock response
    // In production, this would call the actual API
    let response;

    if (
      process.env.NODE_ENV === "development" ||
      !process.env.VUE_APP_API_URL
    ) {
      // Use demo response in development
      const demoResponse = processDemoMessage(
        userMessage.content,
        messages.value
      );
      response = {
        data: {
          response: demoResponse.response,
          financial_data: demoResponse.financialData,
        },
      };
    } else {
      // In production, call the actual API
      response = await axios.post(`${process.env.VUE_APP_API_URL}/api/chat`, {
        message: userMessage.content,
        personality_mode: personalityMode.value,
        conversation_history: messages.value.map((msg) => ({
          role: msg.role,
          content: msg.content,
        })),
        context_data: contextData,
      });
    }

    // Add bot response to the conversation
    const botMessage = {
      role: "bot",
      content: response.data.response,
      timestamp: new Date().toISOString(),
    };
    messages.value.push(botMessage);

    // Update context based on the response
    if (response.data.financial_data) {
      updateContextFromResponse(
        response.data.financial_data,
        botMessage.content
      );
    }

    // Record the response time
    conversationContext.value.lastResponseTime = new Date().toISOString();

    // Add user message to the user responses array for context
    if (conversationContext.value.userResponses) {
      conversationContext.value.userResponses.push({
        content: userMessage.content,
        timestamp: userMessage.timestamp,
      });
    } else {
      conversationContext.value.userResponses = [
        {
          content: userMessage.content,
          timestamp: userMessage.timestamp,
        },
      ];
    }

    // Store conversation in localStorage
    localStorage.setItem("chatHistory", JSON.stringify(messages.value));
    localStorage.setItem(
      "chatContext",
      JSON.stringify(conversationContext.value)
    );
  } catch (error) {
    console.error("Error sending message:", error);
    messages.value.push({
      role: "bot",
      content:
        "Sorry, I'm having trouble connecting right now. Please try again later.",
      timestamp: new Date().toISOString(),
    });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};

// Handle demo conversation for prototype
const processDemoMessage = (text, conversationHistory = []) => {
  // This is a simplified demo function to simulate responses for the prototype

  // Check if we're in an ongoing conversation about a previous purchase
  const isFollowUp =
    conversationHistory.length >= 2 &&
    conversationContext.value.ongoingDiscussion;

  // Get the last few messages for context
  const lastMessages = conversationHistory
    .slice(-3)
    .map((msg) => msg.content.toLowerCase());
  const lastUserMessages = conversationHistory
    .filter((msg) => msg.role === "user")
    .slice(-2)
    .map((msg) => msg.content.toLowerCase());

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
    } = conversationContext.value;

    // If user is explaining why they made a purchase (responding to "tell me more")
    if (isAskingForDetails) {
      if (personalityMode.value === "sarcastic") {
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
      if (personalityMode.value === "sarcastic") {
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
      if (personalityMode.value === "sarcastic") {
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

      if (personalityMode.value === "sarcastic") {
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
    // Set context
    conversationContext.value = {
      lastMentionedAmount: 100,
      lastMentionedCurrency: "EUR",
      lastMentionedItem: "shoes",
      lastDetectedType: "impulse",
      ongoingDiscussion: true,
      discussionStartTime: new Date().toISOString(),
      lastResponseTime: null,
      mentionedItems: ["shoes"],
      mentionedAmounts: [
        { amount: 100, currency: "EUR", timestamp: new Date().toISOString() },
      ],
      followUpQuestions: [],
      userResponses: [],
    };

    // Return demo response
    if (personalityMode.value === "sarcastic") {
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

  // Rest of the function remains the same...
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

      // Set context
      conversationContext.value = {
        lastMentionedAmount: amount,
        lastMentionedCurrency:
          amountMatch[2].includes("€") || amountMatch[2].includes("euro")
            ? "EUR"
            : amountMatch[2].includes("£") || amountMatch[2].includes("pound")
            ? "GBP"
            : "USD",
        lastMentionedItem: item,
        lastDetectedType: isReasonable ? "reasonable" : "impulse",
        ongoingDiscussion: true,
        discussionStartTime: new Date().toISOString(),
        lastResponseTime: null,
        mentionedItems: [item],
        mentionedAmounts: [
          {
            amount,
            currency:
              amountMatch[2].includes("€") || amountMatch[2].includes("euro")
                ? "EUR"
                : amountMatch[2].includes("£") ||
                  amountMatch[2].includes("pound")
                ? "GBP"
                : "USD",
            timestamp: new Date().toISOString(),
          },
        ],
        followUpQuestions: [],
        userResponses: [],
      };

      if (isReasonable) {
        if (personalityMode.value === "sarcastic") {
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

        if (personalityMode.value === "sarcastic") {
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
      personalityMode.value === "sarcastic"
        ? "I'm not quite sure what you're asking about. Care to share some financial decisions you're pondering? Maybe something you're thinking of buying? I promise my judgment will be only slightly cutting! 😉"
        : "I'm here to help with your financial decisions. Feel free to tell me about any purchases you're considering or expenses you want to track.",
    financialData: null,
  };
};

// Override sendMessage for demo purposes
const sendMessageDemo = async () => {
  if (!newMessage.value.trim() || isLoading.value) return;

  const messageText = newMessage.value;
  newMessage.value = "";

  // Extract context from user message
  extractFinancialContext(messageText);

  // Add user message to chat
  messages.value.push({
    text: messageText,
    sender: "user",
  });

  scrollToBottom();
  isLoading.value = true;

  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  try {
    // Get conversation history for context-aware responses
    const conversationHistory = messages.value
      .slice(-5) // Get last 5 messages for context
      .map((msg) => ({
        role: msg.sender === "user" ? "user" : "assistant",
        content: msg.text,
      }));

    // Process demo message with conversation history
    const demoResponse = processDemoMessage(messageText, conversationHistory);

    // Add bot response to chat
    messages.value.push({
      text: demoResponse.response,
      sender: "bot",
    });

    // Check if financial data was detected
    if (demoResponse.financialData) {
      emit("financial-data-detected", demoResponse.financialData);
    }
  } catch (error) {
    console.error("Error in demo message:", error);
    messages.value.push({
      text: "Sorry, I'm having trouble processing that. Please try again.",
      sender: "bot",
    });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }

  emit("message-sent", messageText);
};

// Watch for changes in messages to scroll to bottom
watch(
  () => messages.value.length,
  () => {
    scrollToBottom();
  }
);

// Load saved messages and context on component mount
onMounted(() => {
  // Load saved messages from localStorage
  const savedMessages = localStorage.getItem("chatHistory");
  if (savedMessages) {
    try {
      messages.value = JSON.parse(savedMessages);
    } catch (e) {
      console.error("Error parsing saved messages:", e);
    }
  } else {
    // Add default welcome message if no history
    messages.value = [
      {
        role: "bot",
        content:
          "Hello! I'm your MindfulWealth assistant. How can I help you with your financial decisions today?",
        timestamp: new Date().toISOString(),
      },
    ];
  }

  // Load saved context from localStorage
  const savedContext = localStorage.getItem("chatContext");
  if (savedContext) {
    try {
      const parsedContext = JSON.parse(savedContext);
      // Merge with default values to ensure all fields exist
      conversationContext.value = {
        ...conversationContext.value,
        ...parsedContext,
      };
    } catch (e) {
      console.error("Error parsing saved context:", e);
    }
  }

  // Scroll to bottom of messages
  nextTick(() => {
    scrollToBottom();
  });
});
</script>

<style scoped>
.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-dark);
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #1e1e1e;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #252525;
  border-bottom: 1px solid #333;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 500;
  color: #fff;
}

.personality-toggle {
  display: flex;
  align-items: center;
  background-color: #2a2a2a;
  border-radius: 20px;
  padding: 5px 10px;
  font-size: 0.9rem;
}

.personality-toggle span {
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.personality-toggle span.active {
  background-color: #00b8a9;
  color: #fff;
  font-weight: 500;
}

.toggle-divider {
  color: #555;
  margin: 0 5px;
  cursor: default;
}

.messages-container {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: #1e1e1e;
}

.message {
  margin: 10px 0;
  max-width: 80%;
  position: relative;
}

.user-message {
  margin-left: auto;
  background-color: #00b8a9;
  color: #fff;
  border-radius: 18px 18px 4px 18px;
  padding: 12px 16px;
}

.bot-message {
  margin-right: auto;
  background-color: #2a2a2a;
  color: #fff;
  border-radius: 18px 18px 18px 4px;
  padding: 12px 16px;
}

.message-content {
  word-break: break-word;
  line-height: 1.4;
}

.message-time {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 5px;
  text-align: right;
}

.typing {
  padding: 15px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%,
  60%,
  100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

.input-container {
  display: flex;
  padding: 15px;
  background-color: #1e1e1e;
  border-top: 1px solid #333;
}

.input-container input {
  flex: 1;
  padding: 12px 15px;
  border: none;
  border-radius: 20px;
  background-color: #2a2a2a;
  color: #fff;
  font-size: 0.95rem;
}

.input-container input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 184, 169, 0.5);
}

.input-container input::placeholder {
  color: #888;
}

.input-container button {
  width: 40px;
  height: 40px;
  margin-left: 10px;
  border: none;
  border-radius: 50%;
  background-color: #00b8a9;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.input-container button:hover {
  background-color: #00a599;
}

.input-container button:disabled {
  background-color: #555;
  cursor: not-allowed;
}
</style>
