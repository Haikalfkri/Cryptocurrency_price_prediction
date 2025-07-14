<template>
    <div class="space-y-4">
      <!-- Selector Buttons -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="range in ranges"
          :key="range"
          @click="fetchChart(range)"
          :class="[
            'px-3 py-1 rounded-full text-sm font-medium transition',
            selectedRange === range
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          {{ range }}
        </button>
      </div>
  
      <!-- Chart Display -->
      <div class="bg-white rounded-xl shadow-sm p-4 h-[450px] overflow-hidden">
        <line-chart :chart-data="lineChartData" :chart-options="lineChartOptions" />
      </div>
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Filler
  } from 'chart.js'
  
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Filler
  )
  
  export default {
    name: 'ChartSwitcher',
    components: {
      LineChart: Line
    },
    props: ['coin'],
    data() {
      return {
        selectedRange: '1D',
        ranges: ['1D', '7D', '1M'],
        rawData: []
      }
    },
    computed: {
      lineChartData() {
        return {
          labels: this.rawData.map(row => this.formatDate(row.time)),
          datasets: [{
            label: 'Price',
            data: this.rawData.map(row => row.close_price),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            tension: 0.3,
            fill: true,
            pointRadius: 0
          }]
        }
      },
      lineChartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: value => '$' + this.formatNumber(value),
                color: '#6b7280'
              },
              grid: {
                display: true,
                drawBorder: false,
                color: '#e5e7eb' // light gray
              }
            },
            x: {
              ticks: {
                color: '#6b7280',
                autoSkip: true,
                maxTicksLimit: 10
              },
              grid: {
                display: false // no vertical lines
              }
            }
          }
        }
      }
    },
    methods: {
      async fetchChart(range) {
        this.selectedRange = range
        const hours = range === '1D' ? 24 : range === '7D' ? 24 * 7 : 24 * 30
        try {
          const res = await fetch(`http://localhost:8000/api/v1/chart/${this.coin}/?hours=${hours}`)
          this.rawData = await res.json()
        } catch (err) {
          console.error('Chart fetch failed', err)
        }
      },
      formatDate(isoString) {
        const date = new Date(isoString)
        const day = date.getDate().toString().padStart(2, '0')
        const month = date.toLocaleString('default', { month: 'short' }) // Jul
        const hours = date.getHours().toString().padStart(2, '0')
        const minutes = date.getMinutes().toString().padStart(2, '0')
  
        return this.selectedRange === '1D'
          ? `${day} ${month} ${hours}:${minutes}`
          : `${day} ${month}`
      },
      formatNumber(val) {
        const num = parseFloat(val)
        if (isNaN(num)) return '-'
        if (num >= 1_000_000_000) return (num / 1_000_000_000).toFixed(1) + 'B'
        if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M'
        if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K'
        return num.toFixed(2)
      }
    },
    mounted() {
      this.fetchChart(this.selectedRange)
    }
  }
  </script>
  