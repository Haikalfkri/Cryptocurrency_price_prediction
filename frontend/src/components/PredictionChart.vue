<template>
    <div class="w-full">
      <line-chart :chart-data="lineChartData" :chart-options="chartOptions" class="mb-6" />
      <bar-chart :chart-data="barChartData" :chart-options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { Line, Bar } from 'vue-chartjs';
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    BarElement,
    CategoryScale,
    LinearScale,
    PointElement,
  } from 'chart.js';
  
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    BarElement,
    CategoryScale,
    LinearScale,
    PointElement
  );
  
  export default {
    name: 'PredictionChart',
    components: {
      LineChart: Line,
      BarChart: Bar,
    },
    props: {
      data: {
        type: Array,
        required: true,
      },
    },
    computed: {
      lineChartData() {
        return {
          labels: this.data.map((item) => item.date),
          datasets: [
            {
              label: 'Predicted Price',
              data: this.data.map((item) => item.predicted_price),
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              tension: 0.4,
              fill: true,
            },
          ],
        };
      },
      barChartData() {
        return {
          labels: this.data.map((item) => item.date),
          datasets: [
            {
              label: 'Predicted Price',
              data: this.data.map((item) => item.predicted_price),
              backgroundColor: '#10b981',
            },
          ],
        };
      },
      chartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: true },
            tooltip: { mode: 'index', intersect: false },
          },
          scales: {
            x: { display: true, title: { display: true, text: 'Date' } },
            y: { display: true, title: { display: true, text: 'Price (USD)' } },
          },
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .line-chart-wrapper,
  .bar-chart-wrapper {
    width: 100%;
    height: 300px;
  }
  </style>
  