<script setup>
import { ref, onMounted } from "vue";
import ChatInterface from "./components/ChatInterface.vue";
import FinancialDashboard from "./components/FinancialDashboard.vue";
import ImpulsePurchaseTracker from "./components/ImpulsePurchaseTracker.vue";
import api from "./services/api";

// State
const currentPage = ref("dashboard");
const preferredCurrency = ref("EUR");
const currencySymbols = {
  EUR: "€",
  GBP: "£",
  USD: "$",
};
const budgetData = ref({
  starting_balance: 230,
  ending_balance: 1673,
  expenses: {
    planned: 1391,
    actual: 944,
  },
  income: {
    planned: 2387,
    actual: 2387,
  },
  categories: [
    { name: "Food", planned: 120, actual: 22 },
    { name: "Gifts", planned: 400, actual: 400 },
    { name: "Home", planned: 470, actual: 470 },
    { name: "Restaurant", planned: 100, actual: 35 },
  ],
});
const savedImpulses = ref([
  { item: "Designer Shoes", amount: 150, potential_value: 162 },
  { item: "Tech Gadget", amount: 299, potential_value: 323 },
]);

// Methods
const fetchBudgetData = async () => {
  try {
    const response = await api.getBudget();
    if (response.data) {
      budgetData.value = response.data;
    }
  } catch (error) {
    console.error("Error fetching budget data:", error);
  }
};

const fetchCurrencyPreference = async () => {
  try {
    const response = await api.getCurrency();
    if (response.data && response.data.currency) {
      preferredCurrency.value = response.data.currency;
    }
  } catch (error) {
    console.error("Error fetching currency preference:", error);
  }
};

const setCurrency = async (currency) => {
  try {
    await api.setCurrency(currency);
    preferredCurrency.value = currency;
  } catch (error) {
    console.error("Error setting currency:", error);
  }
};

const fetchSavedImpulses = async () => {
  try {
    const response = await api.getSavedImpulses();
    if (response.data && response.data.saved_impulses) {
      savedImpulses.value = response.data.saved_impulses;
    }
  } catch (error) {
    console.error("Error fetching saved impulses:", error);
  }
};

const handleMessageSent = (message) => {
  console.log("Message sent:", message);
  // Additional logic if needed
};

const handleFinancialDataDetected = (data) => {
  console.log("Financial data detected:", data);
  // Update dashboard or impulse tracker based on detected data
  fetchBudgetData();
  fetchSavedImpulses();
};

const handleImpulseAdded = (impulse) => {
  savedImpulses.value.push(impulse);
};

const navigateTo = (page) => {
  currentPage.value = page;
};

onMounted(() => {
  fetchBudgetData();
  fetchSavedImpulses();
  fetchCurrencyPreference();
});
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <div class="logo" @click="navigateTo('dashboard')">
          <h1>MindfulWealth</h1>
        </div>
        <div class="header-actions">
          <div class="currency-selector">
            <div class="currency-options">
              <button
                @click="setCurrency('EUR')"
                :class="{ active: preferredCurrency === 'EUR' }"
                aria-label="Set currency to Euro"
              >
                €
              </button>
              <button
                @click="setCurrency('GBP')"
                :class="{ active: preferredCurrency === 'GBP' }"
                aria-label="Set currency to British Pound"
              >
                £
              </button>
              <button
                @click="setCurrency('USD')"
                :class="{ active: preferredCurrency === 'USD' }"
                aria-label="Set currency to US Dollar"
              >
                $
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="app-content">
      <!-- Dashboard Page -->
      <div v-if="currentPage === 'dashboard'" class="page-container">
        <FinancialDashboard
          :budget-data="budgetData"
          :currency-symbol="currencySymbols[preferredCurrency]"
        />
      </div>

      <!-- Chat Page -->
      <div v-if="currentPage === 'chat'" class="page-container">
        <ChatInterface
          @message-sent="handleMessageSent"
          @financial-data-detected="handleFinancialDataDetected"
        />
      </div>

      <!-- Progress Page -->
      <div v-if="currentPage === 'progress'" class="page-container">
        <ImpulsePurchaseTracker
          :saved-impulses="savedImpulses"
          :currency-symbol="currencySymbols[preferredCurrency]"
          @impulse-added="handleImpulseAdded"
        />
      </div>

      <!-- Profile Page -->
      <div v-if="currentPage === 'profile'" class="page-container profile-page">
        <div class="profile-header">
          <h2>Profile</h2>
        </div>
        <div class="profile-content">
          <div class="profile-avatar">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <h3>Guest User</h3>
          <p>Using prototype version</p>

          <div class="settings-section">
            <h4>Settings</h4>
            <div class="setting-item">
              <span>Personality Mode</span>
              <div class="toggle-switch">
                <div class="toggle-handle"></div>
              </div>
            </div>
            <div class="setting-item">
              <span>Dark Mode</span>
              <div class="toggle-switch">
                <div class="toggle-handle right"></div>
              </div>
            </div>
            <div class="setting-item">
              <span>Currency</span>
              <div class="currency-options-small">
                <button
                  @click="setCurrency('EUR')"
                  :class="{ active: preferredCurrency === 'EUR' }"
                >
                  €
                </button>
                <button
                  @click="setCurrency('GBP')"
                  :class="{ active: preferredCurrency === 'GBP' }"
                >
                  £
                </button>
                <button
                  @click="setCurrency('USD')"
                  :class="{ active: preferredCurrency === 'USD' }"
                >
                  $
                </button>
              </div>
            </div>
          </div>

          <div class="about-section">
            <h4>About MindfulWealth</h4>
            <p>
              A financial chatbot that helps transform shopping impulses into
              investment growth opportunities.
            </p>
            <p class="version">Version 1.0.0 (Prototype)</p>
          </div>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <nav class="app-nav">
        <button
          @click="navigateTo('dashboard')"
          :class="{ active: currentPage === 'dashboard' }"
          aria-label="Dashboard"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          </svg>
          <span>Goals</span>
        </button>

        <button
          @click="navigateTo('progress')"
          :class="{ active: currentPage === 'progress' }"
          aria-label="Progress"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          <span>Progress</span>
        </button>

        <button
          @click="navigateTo('chat')"
          :class="{ active: currentPage === 'chat' }"
          aria-label="Chat"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
            ></path>
          </svg>
          <span>Chat</span>
        </button>

        <button
          @click="navigateTo('profile')"
          :class="{ active: currentPage === 'profile' }"
          aria-label="Profile"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span>Profile</span>
        </button>
      </nav>
    </footer>
  </div>
</template>

<style>
/* Global styles */
:root {
  --primary-color: #40e0d0;
  --primary-light: #7fffd4;
  --primary-dark: #20b2aa;
  --success-color: #ff9a8b;
  --danger-color: #ff6b6b;
  --text-light: #e0e0e0;
  --text-dark: #1e293b;
  --bg-dark: #1a2234;
  --bg-card: #242f45;
  --border-color: #2a3a5c;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  color: var(--text-light);
  background-color: var(--bg-dark);
  line-height: 1.5;
}

/* App specific styles */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: 100%;
  margin: 0 auto;
}

.app-header {
  background-color: var(--bg-dark);
  padding: 1rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.logo {
  cursor: pointer;
}

.logo h1 {
  color: var(--text-light);
  font-size: 1.8rem;
  font-weight: 700;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.currency-selector {
  display: flex;
  align-items: center;
}

.currency-options {
  display: flex;
  gap: 0.25rem;
}

.currency-options button {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  color: var(--text-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.currency-options button:hover {
  background-color: var(--primary-dark);
  color: var(--text-dark);
}

.currency-options button.active {
  background-color: var(--primary-color);
  color: var(--text-dark);
  border-color: var(--primary-color);
}

.app-content {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.page-container {
  height: 100%;
  padding: 1rem;
  overflow-y: auto;
}

.app-footer {
  background-color: var(--bg-card);
  padding: 0.5rem 1rem;
  position: sticky;
  bottom: 0;
  z-index: 10;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
}

.app-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;
}

.app-nav button {
  background: none;
  border: none;
  color: var(--text-light);
  opacity: 0.6;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.app-nav button svg {
  width: 24px;
  height: 24px;
}

.app-nav button span {
  font-size: 0.7rem;
}

.app-nav button:hover {
  opacity: 0.8;
}

.app-nav button.active {
  opacity: 1;
  color: var(--primary-color);
}

/* Profile page styles */
.profile-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-header {
  padding: 1rem 0;
}

.profile-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  background-color: var(--bg-card);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-avatar svg {
  width: 60px;
  height: 60px;
  stroke: var(--primary-color);
}

.profile-content h3 {
  font-size: 1.5rem;
  margin: 0;
}

.profile-content p {
  color: var(--text-light);
  opacity: 0.7;
  margin: 0;
}

.settings-section {
  width: 100%;
  max-width: 400px;
  margin-top: 1rem;
}

.settings-section h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: var(--text-light);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.toggle-switch {
  width: 50px;
  height: 24px;
  background-color: var(--bg-card);
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-handle {
  width: 20px;
  height: 20px;
  background-color: var(--primary-color);
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: all 0.3s;
}

.toggle-handle.right {
  left: calc(100% - 22px);
}

.currency-options-small {
  display: flex;
  gap: 0.25rem;
}

.currency-options-small button {
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  color: var(--text-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.currency-options-small button.active {
  background-color: var(--primary-color);
  color: var(--text-dark);
  border-color: var(--primary-color);
}

.about-section {
  width: 100%;
  max-width: 400px;
  margin-top: 2rem;
  text-align: center;
}

.about-section h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: var(--text-light);
}

.about-section p {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.version {
  font-size: 0.8rem;
  opacity: 0.6;
}

/* Responsive styles */
@media (min-width: 768px) {
  .app-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .page-container {
    padding: 2rem;
  }
}
</style>
