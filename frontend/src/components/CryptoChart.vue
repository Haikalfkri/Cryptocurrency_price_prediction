<template>
    <div class="w-full max-w-full">
      <!-- Period Selection -->
      <div class="mb-2 flex gap-1 justify-end flex-wrap">
        <button
          v-for="option in periodOptions"
          :key="option.value"
          @click="selectedPeriod = option.value"
          :class="[
            'px-4 py-2 text-sm rounded-md',
            selectedPeriod === option.value ? 'bg-blue-600 text-white' : 'bg-gray-200',
          ]"
        >
          {{ option.label }}
        </button>
      </div>
  
      <!-- Chart Loading & Error -->
      <div v-if="loading" class="text-gray-600">Loading chart...</div>
      <div v-else-if="error" class="text-red-500">{{ error }}</div>
  
      <!-- Chart -->
      <div v-else class="bg-white rounded-lg w-full">
        <apexchart
          type="area"
          :height="chartHeight"
          :options="chartOptions"
          :series="series"
          class="w-full"
        />
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, watch, onMounted, computed } from "vue";
  import axios from "axios";
  
  axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;
  
  export default defineComponent({
    name: "CryptoChart",
    props: {
      coin: {
        type: String,
        required: true,
      },
    },
    setup(props) {
      const series = ref([]);
      const chartOptions = ref({});
      const loading = ref(true);
      const error = ref(null);
      const selectedPeriod = ref("week");
  
      const periodOptions = [
        { label: "7D", value: "week" },
        { label: "1M", value: "month" },
      ];
  
      const fetchChartData = async () => {
        loading.value = true;
        error.value = null;
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/api/v1/fetchCryptoChart/",
            {
              coin: props.coin,
              period: selectedPeriod.value,
            },
            {
              withCredentials: true,
            }
          );
  
          const prices = response.data.chart;
  
          series.value = [
            {
              name: "Price (USD)",
              data: prices,
            },
          ];
  
          chartOptions.value = {
            chart: {
              type: "area",
              zoom: {
                enabled: false,
              },
              toolbar: {
                show: false,
              },
              dropShadow: {
                enabled: false,
              },
            },
            dataLabels: {
              enabled: false,
            },
            stroke: {
              curve: "smooth",
              width: 2,
              dropShadow: {
                enabled: false,
              },
            },
            xaxis: {
              type: "datetime",
              labels: {
                rotate: -45,
                datetimeUTC: false,
                format: "dd MMM",
              },
            },
            yaxis: {
              labels: {
                formatter: (val) => `$${val.toFixed(2)}`,
              },
            },
            tooltip: {
              x: {
                format: "dd MMM yyyy",
              },
            },
            fill: {
              type: "gradient",
              gradient: {
                shadeIntensity: 1,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 90, 100],
              },
              dropShadow: {
                enabled: false,
              },
            },
            colors: ["#4F46E5"],
          };
        } catch (err) {
          error.value = "Failed to load chart data.";
        } finally {
          loading.value = false;
        }
      };
  
      watch(selectedPeriod, fetchChartData);
      onMounted(fetchChartData);
  
      // Responsively adjust chart height
      const chartHeight = computed(() => {
        // Kalau layar kecil, lebih pendek
        return window.innerWidth < 640 ? 250 : 350;
      });
  
      return {
        series,
        chartOptions,
        loading,
        error,
        selectedPeriod,
        periodOptions,
        chartHeight,
      };
    },
  });
  </script>
  