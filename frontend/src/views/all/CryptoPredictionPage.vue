<template>
  <div class="flex flex-col items-center justify-center w-full px-4 mb-10">
    <!-- Back Button -->
    <button @click="$router.push('/predictPage')" class="absolute left-4 top-6 sm:top-10 p-2">
      <svg class="w-6 h-6 text-gray-800" fill="none" viewBox="0 0 14 10">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M13 5H1m0 0 4 4M1 5l4-4" />
      </svg>
    </button>

    <div v-if="originalPlot" class="w-full max-w-5xl flex flex-col items-center space-y-10 mt-20">

      <!-- Future Chart -->
      <div class="w-full">
        <h2 class="text-xl font-semibold text-center mb-4">Future Price Predictions (Chart)</h2>
        <div class="bg-white rounded-2xl shadow-lg p-4">
          <canvas id="futureChart" class="w-full"></canvas>
        </div>
      </div>

      <!-- Predicted Analysis (Table) -->
      <div class="w-full">
        <h2 class="text-xl font-semibold text-center mb-4">Predicted Analysis (Table)</h2>
        <div class="overflow-x-auto bg-white rounded-2xl shadow-lg">
          <table class="min-w-full text-sm text-left border border-gray-200">
            <thead class="bg-gray-100 text-gray-700">
              <tr>
                <th class="px-4 py-3 border">Date</th>
                <th class="px-4 py-3 border">Predicted Price</th>
                <th class="px-4 py-3 border">Trend</th>
                <th class="px-4 py-3 border">Action</th>
                <th class="px-4 py-3 border">Reason</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in filteredPredictionAnalysis" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-2 border">{{ item.date }}</td>
                <td class="px-4 py-2 border">{{ formatPrice(item.predicted_price) }}</td>
                <td class="px-4 py-2 border">{{ item.trend }}</td>
                <td class="px-4 py-2 border font-medium text-blue-600">{{ item.action }}</td>
                <td class="px-4 py-2 border text-left">{{ item.reason }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Sentiment, Recommendation, Final Score, and Summarize -->
      <div class="w-full mt-10">
        <h2 class="text-xl font-semibold text-center mb-6">Sentiment Analysis and Recommendations</h2>
        <div class="flex flex-wrap justify-center gap-6 mb-8">
          <!-- Sentiment Label -->
          <div
            :class="['flex flex-col items-center justify-center w-36 h-36 rounded-full border-4 shadow-lg transition-transform hover:scale-105', sentimentClass]">
            <p class="text-center text-lg font-semibold">{{ sentiment_label }}</p>
            <p class="text-xs text-gray-600 mb-1">Sentiment</p>
          </div>

          <!-- Recommendation -->
          <div
            :class="['flex flex-col items-center justify-center w-36 h-36 rounded-full border-4 shadow-lg transition-transform hover:scale-105', recommendationClass]">
            <p class="text-center text-lg font-semibold">{{ recommendation }}</p>
            <p class="text-xs text-gray-600 mb-1">Recommendation</p>
          </div>

          <!-- Final Score -->
          <div
            :class="['flex flex-col items-center justify-center w-36 h-36 rounded-full border-4 shadow-lg transition-transform hover:scale-105', scoreClass]">
            <p class="text-center text-lg font-semibold">{{ final_score }}%</p>
            <p class="text-xs text-gray-600 mb-1">Score</p>
          </div>
        </div>

        <!-- Summary -->
        <div class="w-full bg-white text-left rounded-2xl shadow-lg p-6">
          <h3 class="text-xl font-semibold mb-4">Summary</h3>
          <p>{{ summarize }}</p>
        </div>
      </div>

      <!-- Original Price Chart -->
      <div class="w-full mt-10">
        <h2 class="text-xl font-semibold text-center mb-4">Original Price Chart</h2>
        <img :src="originalPlot" alt="Original Chart"
          class="w-full rounded-2xl shadow-lg transition-transform hover:scale-105" />
      </div>

      <!-- Predicted Price Chart -->
      <div class="w-full mt-10">
        <h2 class="text-xl font-semibold text-center mb-4">Predicted Price Chart</h2>
        <img :src="predictedPlot" alt="Predicted Chart"
          class="w-full rounded-2xl shadow-lg transition-transform hover:scale-105" />
      </div>

    </div>
  </div>
</template>



<script>
import Chart from 'chart.js/auto';

export default {
  name: "CryptoPredictionPage",
  data() {
    return {
      originalPlot: null,
      predictedPlot: null,
      sentiment_label: '',
      recommendation: '',
      summarize: '',
      final_score: 0,
      futurePlot: [],
      predictPriceAnalysis: [],
    };
  },
  computed: {
    filteredPredictionAnalysis() {
      return this.predictPriceAnalysis.filter(item => item.date);
    },
    sentimentClass() {
      const label = this.sentiment_label.toLowerCase();
      if (label.includes('positive')) return 'border-green-500 text-green-700 bg-green-50';
      if (label.includes('neutral')) return 'border-yellow-500 text-yellow-700 bg-yellow-50';
      if (label.includes('negative')) return 'border-red-500 text-red-700 bg-red-50';
      return 'border-gray-300 text-gray-700 bg-gray-50';
    },
    recommendationClass() {
      const rec = this.recommendation.toLowerCase();
      if (rec.includes('buy')) return 'border-green-500 text-green-700 bg-green-50';
      if (rec.includes('hold')) return 'border-yellow-500 text-yellow-700 bg-yellow-50';
      if (rec.includes('sell')) return 'border-red-500 text-red-700 bg-red-50';
      return 'border-gray-300 text-gray-700 bg-gray-50';
    },
    scoreClass() {
      const score = this.final_score;
      if (score >= 70) return 'border-green-500 text-green-700 bg-green-50';
      if (score >= 40) return 'border-yellow-500 text-yellow-700 bg-yellow-50';
      return 'border-red-500 text-red-700 bg-red-50';
    }
  },
  methods: {
    formatPrice(value) {
      return `$${Number(value).toLocaleString('en-US', { maximumFractionDigits: 2 })}`;
    },
    renderFutureChart() {
      const ctx = document.getElementById('futureChart').getContext('2d');
      const labels = this.filteredPredictionAnalysis.map(item => item.date);
      const prices = this.filteredPredictionAnalysis.map(item => item.predicted_price);

      new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Predicted Price',
            data: prices,
            borderColor: 'rgba(59, 130, 246, 1)',
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            fill: true,
            tension: 0.3,
            pointRadius: 4,
            pointHoverRadius: 6,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: true },
            tooltip: {
              callbacks: {
                label: (context) => `Price: $${context.parsed.y.toFixed(2)}`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: value => `$${value}`
              }
            }
          }
        }
      });
    }
  },
  mounted() {
    const response = JSON.parse(localStorage.getItem("predictionResponse") || '{}');

    this.originalPlot = response.original_plot;
    this.predictedPlot = response.predicted_plot;
    this.sentiment_label = response.sentiment_label || '';
    this.recommendation = response.recommendation || '';
    this.final_score = response.final_score || 0;
    this.futurePlot = response.future_plot || [];
    this.summarize = response.summarize || '';
    this.predictPriceAnalysis = response.predict_price_analysis || [];

    this.$nextTick(() => {
      if (this.filteredPredictionAnalysis.length) {
        this.renderFutureChart();
      }
    });
  }
};
</script>

<style scoped>
/* No extra raw CSS needed, Tailwind handles everything */
</style>
