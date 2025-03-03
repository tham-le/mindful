<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>Goals</h2>
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

    <div class="goals-grid">
      <div
        class="goal-card"
        v-for="(category, index) in budgetData.categories"
        :key="index"
        :class="getCardColor(index)"
      >
        <div class="goal-icon">
          <svg
            v-if="index === 0"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <svg
            v-else-if="index === 1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z"
            ></path>
            <polyline points="9 17 5 13 7 11"></polyline>
            <path d="M19 13l-4 4-4-4"></path>
          </svg>
          <svg
            v-else-if="index === 2"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
            <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
            <line x1="6" y1="1" x2="6" y2="4"></line>
            <line x1="10" y1="1" x2="10" y2="4"></line>
            <line x1="14" y1="1" x2="14" y2="4"></line>
          </svg>
        </div>
        <div class="goal-content">
          <h3>{{ category.name }}</h3>
          <p class="goal-frequency">{{ getFrequency(index) }}</p>
        </div>
      </div>

      <div class="goal-card add-goal">
        <div class="add-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </div>
        <div class="goal-content">
          <h3>Add New Goal</h3>
        </div>
      </div>
    </div>

    <div class="progress-section" v-if="selectedGoal">
      <div class="progress-header">
        <button class="back-button" @click="selectedGoal = null">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
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

      <div class="progress-content">
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
              :stroke-dashoffset="
                502.4 - 502.4 * (selectedGoal.actual / selectedGoal.planned)
              "
              transform="rotate(-90 100 100)"
            />
            <text
              x="100"
              y="90"
              text-anchor="middle"
              fill="#E0E0E0"
              font-size="40"
            >
              {{
                Math.round((selectedGoal.actual / selectedGoal.planned) * 100)
              }}%
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
            <span class="stat-value">{{
              Math.round(selectedGoal.actual)
            }}</span>
            <span class="stat-label">CURRENT</span>
          </div>
          <div class="stat-item">
            <span class="stat-value"
              >{{
                Math.round((selectedGoal.actual / selectedGoal.planned) * 100)
              }}%</span
            >
            <span class="stat-label">PROGRESS</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{
              Math.round(selectedGoal.planned)
            }}</span>
            <span class="stat-label">TARGET</span>
          </div>
        </div>

        <div class="progress-chart">
          <div class="chart-container">
            <canvas ref="progressChart"></canvas>
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { Chart, registerables } from "chart.js";
import api from "../services/api";

Chart.register(...registerables);

const props = defineProps({
  budgetData: {
    type: Object,
    default: () => ({
      starting_balance: 0,
      ending_balance: 0,
      expenses: {
        planned: 0,
        actual: 0,
      },
      income: {
        planned: 0,
        actual: 0,
      },
      categories: [],
    }),
  },
  currencySymbol: {
    type: String,
    default: "€",
  },
});

const selectedGoal = ref(null);
const progressChart = ref(null);
const chart = ref(null);

const balanceChange = computed(() => {
  if (!props.budgetData.starting_balance) return 0;
  const change =
    ((props.budgetData.ending_balance - props.budgetData.starting_balance) /
      props.budgetData.starting_balance) *
    100;
  return Math.round(change * 10) / 10;
});

const getCardColor = (index) => {
  const colors = ["purple", "coral", "yellow", "blue", "green", "teal"];
  return colors[index % colors.length];
};

const getFrequency = (index) => {
  const frequencies = [
    "2 times a day",
    "3 times a week",
    "3 times a week",
    "1 time a day",
    "3 times a day",
    "2 times a week",
  ];
  return frequencies[index % frequencies.length];
};

const selectGoal = (goal) => {
  selectedGoal.value = goal;
  setTimeout(() => {
    if (progressChart.value) {
      initProgressChart();
    }
  }, 100);
};

const initProgressChart = () => {
  if (chart.value) {
    chart.value.destroy();
  }

  const ctx = progressChart.value.getContext("2d");

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

watch(
  () => props.budgetData,
  (newVal) => {
    if (newVal.categories && newVal.categories.length > 0) {
      // Auto-select first goal for demo purposes
      selectGoal(newVal.categories[0]);
    }
  },
  { immediate: true, deep: true }
);

onMounted(() => {
  if (props.budgetData.categories && props.budgetData.categories.length > 0) {
    // Auto-select first goal for demo purposes
    selectGoal(props.budgetData.categories[0]);
  }
});
</script>

<style scoped>
.dashboard-container {
  background-color: var(--bg-dark);
  border-radius: 12px;
  height: 100%;
  overflow-y: auto;
  position: relative;
}

.dashboard-header,
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.dashboard-header h2,
.progress-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.more-options,
.back-button {
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
  padding: 0.5rem;
}

.more-options svg,
.back-button svg {
  width: 24px;
  height: 24px;
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  padding: 0 1rem 1rem;
}

.goal-card {
  background-color: var(--bg-card);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.goal-card:hover {
  transform: translateY(-5px);
}

.goal-card.purple {
  background-color: #9c6ade;
}

.goal-card.coral {
  background-color: #ff9a8b;
}

.goal-card.yellow {
  background-color: #ffd166;
}

.goal-card.blue {
  background-color: #73c2fb;
}

.goal-card.green {
  background-color: #06d6a0;
}

.goal-card.teal {
  background-color: #40e0d0;
}

.goal-icon,
.add-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.goal-icon svg,
.add-icon svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.goal-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: white;
}

.goal-frequency {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0.25rem 0 0;
}

.add-goal {
  background-color: var(--bg-card);
  border: 2px dashed var(--border-color);
  opacity: 0.7;
}

.add-goal:hover {
  opacity: 1;
}

.progress-section {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--bg-dark);
  z-index: 10;
  display: flex;
  flex-direction: column;
}

.progress-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
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

@media (min-width: 768px) {
  .goals-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
