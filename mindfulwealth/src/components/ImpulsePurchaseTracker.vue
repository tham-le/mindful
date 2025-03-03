<template>
  <div class="tracker-container">
    <div class="tracker-header">
      <h2>Progress</h2>
      <button class="more-options">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="12" cy="5" r="1"></circle>
          <circle cx="12" cy="12" r="1"></circle>
          <circle cx="12" cy="19" r="1"></circle>
        </svg>
      </button>
    </div>

    <div class="progress-overview">
      <div class="progress-circle">
        <svg width="200" height="200" viewBox="0 0 200 200">
          <circle
            cx="100"
            cy="100"
            r="80"
            fill="none"
            stroke="#2A3A5C"
            stroke-width="20"
          />
          <circle
            cx="100"
            cy="100"
            r="80"
            fill="none"
            stroke="#FF9A8B"
            stroke-width="20"
            stroke-dasharray="502.4"
            :stroke-dashoffset="502.4 - (502.4 * progressPercentage) / 100"
            transform="rotate(-90 100 100)"
          />
          <text
            x="100"
            y="90"
            text-anchor="middle"
            fill="#E0E0E0"
            font-size="40"
          >
            {{ progressPercentage }}%
          </text>
          <text
            x="100"
            y="120"
            text-anchor="middle"
            fill="#E0E0E0"
            font-size="16"
          >
            COMPLETED
          </text>
        </svg>
      </div>

      <div class="progress-stats">
        <div class="stat-item">
          <span class="stat-value">23</span>
          <span class="stat-label">LOREM</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ progressPercentage }}%</span>
          <span class="stat-label">DOLOR SIT</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">234</span>
          <span class="stat-label">AMET</span>
        </div>
      </div>
    </div>

    <div class="progress-chart">
      <div class="chart-container">
        <canvas ref="growthChart"></canvas>
      </div>
    </div>

    <div class="day-indicators">
      <div
        class="day"
        v-for="day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']"
        :key="day"
      >
        {{ day }}
      </div>
    </div>

    <div class="saved-impulses" v-if="savedImpulses.length > 0">
      <h3>Saved Investments</h3>
      <div class="impulse-items">
        <div
          v-for="(impulse, index) in savedImpulses"
          :key="index"
          class="impulse-card"
        >
          <div class="impulse-icon" :class="getCardColor(index)">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
          </div>
          <div class="impulse-details">
            <h4>{{ impulse.item }}</h4>
            <div class="impulse-values">
              <div class="value-item">
                <span class="value-label">Saved</span>
                <span class="value-amount"
                  >{{ currencySymbol }}{{ impulse.amount }}</span
                >
              </div>
              <div class="value-item">
                <span class="value-label">Potential</span>
                <span class="value-amount"
                  >{{ currencySymbol }}{{ impulse.potential_value }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="add-impulse">
      <button
        @click="showAddImpulseForm = !showAddImpulseForm"
        class="add-button"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="16"></line>
          <line x1="8" y1="12" x2="16" y2="12"></line>
        </svg>
        <span>{{ showAddImpulseForm ? "Cancel" : "Add Investment" }}</span>
      </button>
    </div>

    <div v-if="showAddImpulseForm" class="impulse-form">
      <div class="form-group">
        <label for="impulse-item">Item Description</label>
        <input
          type="text"
          id="impulse-item"
          v-model="newImpulse.item"
          placeholder="e.g., Designer Shoes"
        />
      </div>
      <div class="form-group">
        <label for="impulse-amount">Amount ({{ currencySymbol }})</label>
        <input
          type="number"
          id="impulse-amount"
          v-model="newImpulse.amount"
          placeholder="0.00"
          min="0"
          step="0.01"
        />
      </div>
      <div class="form-actions">
        <button
          @click="addImpulse"
          :disabled="!newImpulse.item || !newImpulse.amount"
          class="save-button"
        >
          Save Investment
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { Chart, registerables } from "chart.js";
import api from "../services/api";

Chart.register(...registerables);

const props = defineProps({
  savedImpulses: {
    type: Array,
    default: () => [],
  },
  currencySymbol: {
    type: String,
    default: "€",
  },
});

const emit = defineEmits(["impulse-added"]);

const growthChart = ref(null);
const chart = ref(null);
const showAddImpulseForm = ref(false);
const newImpulse = ref({
  item: "",
  amount: "",
});

// Computed properties
const totalRedirected = computed(() => {
  return props.savedImpulses
    .reduce((total, impulse) => total + parseFloat(impulse.amount), 0)
    .toFixed(2);
});

const progressPercentage = computed(() => {
  // For demo purposes, hardcoded to 45.2%
  return 45.2;
});

// Methods
const getCardColor = (index) => {
  const colors = ["purple", "coral", "yellow", "blue", "green", "teal"];
  return colors[index % colors.length];
};

const calculateGrowthPercentage = (impulse) => {
  const growth =
    ((impulse.potential_value - impulse.amount) / impulse.amount) * 100;
  return growth.toFixed(1);
};

const addImpulse = async () => {
  if (!newImpulse.value.item || !newImpulse.value.amount) return;

  try {
    // Calculate potential value (8% annual return)
    const amount = parseFloat(newImpulse.value.amount);
    const potentialValue = (amount * 1.08).toFixed(2);

    const impulseData = {
      item: newImpulse.value.item,
      amount: amount,
      potential_value: parseFloat(potentialValue),
      date: new Date().toISOString(),
    };

    await api.addSavedImpulse(impulseData);
    emit("impulse-added", impulseData);

    // Reset form
    newImpulse.value = { item: "", amount: "" };
    showAddImpulseForm.value = false;
  } catch (error) {
    console.error("Error adding impulse purchase:", error);
  }
};

const initChart = () => {
  if (chart.value) {
    chart.value.destroy();
  }

  const ctx = growthChart.value.getContext("2d");

  const data = {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    datasets: [
      {
        label: "Weekly Progress",
        data: [5, 10, 3, 15, 8, 12, 7],
        borderColor: "#FF9A8B",
        backgroundColor: "rgba(0, 0, 0, 0)",
        tension: 0.4,
        borderWidth: 3,
      },
    ],
  };

  chart.value = new Chart(ctx, {
    type: "line",
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          display: false,
          beginAtZero: true,
        },
        x: {
          display: false,
        },
      },
      elements: {
        point: {
          radius: 0,
        },
      },
    },
  });
};

onMounted(() => {
  initChart();
});

watch(
  () => props.savedImpulses,
  () => {
    // Update chart if needed
  },
  { deep: true }
);
</script>

<style scoped>
.tracker-container {
  background-color: var(--bg-dark);
  border-radius: 12px;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
}

.tracker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tracker-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.more-options {
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
  padding: 0.5rem;
}

.more-options svg {
  width: 24px;
  height: 24px;
}

.progress-overview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.progress-circle {
  width: 200px;
  height: 200px;
  position: relative;
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 300px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
}

.stat-label {
  font-size: 0.7rem;
  color: var(--text-light);
  opacity: 0.7;
}

.progress-chart {
  width: 100%;
  height: 100px;
}

.chart-container {
  width: 100%;
  height: 100%;
}

.day-indicators {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.day {
  font-size: 0.8rem;
  color: var(--text-light);
  text-align: center;
}

.saved-impulses {
  margin-top: 1rem;
}

.saved-impulses h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.impulse-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.impulse-card {
  background-color: var(--bg-card);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.impulse-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.impulse-icon svg {
  width: 20px;
  height: 20px;
  stroke: white;
}

.impulse-icon.purple {
  background-color: #9c6ade;
}

.impulse-icon.coral {
  background-color: #ff9a8b;
}

.impulse-icon.yellow {
  background-color: #ffd166;
}

.impulse-icon.blue {
  background-color: #73c2fb;
}

.impulse-icon.green {
  background-color: #06d6a0;
}

.impulse-icon.teal {
  background-color: #40e0d0;
}

.impulse-details {
  flex: 1;
}

.impulse-details h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 500;
}

.impulse-values {
  display: flex;
  gap: 1rem;
}

.value-item {
  display: flex;
  flex-direction: column;
}

.value-label {
  font-size: 0.7rem;
  color: var(--text-light);
  opacity: 0.7;
}

.value-amount {
  font-size: 0.9rem;
  font-weight: 500;
}

.add-impulse {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.add-button {
  background-color: var(--primary-color);
  color: var(--text-dark);
  border: none;
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.add-button:hover {
  background-color: var(--primary-light);
}

.add-button svg {
  width: 20px;
  height: 20px;
}

.impulse-form {
  background-color: var(--bg-card);
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-light);
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-dark);
  color: var(--text-light);
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.save-button {
  background-color: var(--primary-color);
  color: var(--text-dark);
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.save-button:hover {
  background-color: var(--primary-light);
}

.save-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
