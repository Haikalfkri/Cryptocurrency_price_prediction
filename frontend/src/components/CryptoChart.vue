<template>
    <div class="w-full max-w-3xl mt-6">
        <h2 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Price Chart</h2>

        <!-- Period Selection -->
        <div class="mb-4 flex gap-2">
            <button v-for="option in periodOptions" :key="option.value"
                @click="selectedPeriod = option.value"
                :class="['px-4 py-2 text-sm rounded-md',
                    selectedPeriod === option.value ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 dark:text-white']">
                {{ option.label }}
            </button>
        </div>

        <!-- Chart Loading & Error -->
        <div v-if="loading" class="text-gray-600 dark:text-gray-400">Loading chart...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>

        <!-- Chart -->
        <div v-else class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
            <LineChart v-if="chartData" :chart-data="chartData" :chart-options="chartOptions" />
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, watch, onMounted } from "vue";
import { LineChart } from "vue-chart-3";
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, LineController } from "chart.js";
import axios from "axios";

// ✅ Register necessary Chart.js components including LineController
ChartJS.register(LineController, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);

export default defineComponent({
    name: "CryptoChart",
    components: { LineChart },
    props: {
        coin: String, // Coin name (e.g., 'bitcoin')
    },
    setup(props) {
        const chartData = ref(null);
        const loading = ref(true);
        const error = ref(null);
        const selectedPeriod = ref("week"); // Default period

        const periodOptions = [
            { label: "7D", value: "week" },
            { label: "1M", value: "month" },
            { label: "All Time", value: "max" },
        ];

        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (tooltipItem) => `$${tooltipItem.raw.toFixed(2)}`,
                    },
                },
            },
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: { title: { display: true, text: "Price (USD)" }, beginAtZero: false },
            },
        };

        const fetchChartData = async () => {
            loading.value = true;
            error.value = null;
            try {
                const response = await axios.post("http://127.0.0.1:8000/api/v1/fetchCryptoChart/", {
                    coin: props.coin,
                    period: selectedPeriod.value,
                });

                const prices = response.data.chart;
                const labels = prices.map(item => new Date(item[0]).toLocaleDateString());
                const dataPoints = prices.map(item => item[1]);

                chartData.value = {
                    labels,
                    datasets: [{ label: "Price (USD)", data: dataPoints, borderColor: "#4CAF50", backgroundColor: "rgba(76, 175, 80, 0.2)", fill: true }]
                };
            } catch (err) {
                error.value = "Failed to load chart data.";
            } finally {
                loading.value = false;
            }
        };

        watch(selectedPeriod, fetchChartData);
        onMounted(fetchChartData);

        return { chartData, chartOptions, loading, error, selectedPeriod, periodOptions };
    },
});
</script>