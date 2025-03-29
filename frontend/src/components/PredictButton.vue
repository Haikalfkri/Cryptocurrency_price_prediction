<template>
    <form @submit.prevent="fetchPrediction" class="flex items-center max-w-2xl mx-auto space-x-2">
        <label for="crypto-search" class="sr-only">Search</label>

        <!-- Search Input -->
        <div class="relative w-full">
            <input v-model="coin" type="text" id="crypto-search" class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5
         dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search Crypto e.g BTC-USD, ETH-USD"
                required />
        </div>

        <!-- Dropdown -->
        <select v-model="days" id="days-filter" class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500
        p-2.5 dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option :value="7">7 Days</option>
            <option :value="14">14 Days</option>
        </select>

        <!-- Search Button -->
        <button type="submit"
            class="inline-flex items-center py-2.5 px-3 text-sm font-medium text-white bg-blue-700 rounded-2xl border border-blue-700
        hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>
            Search
        </button>
    </form>

    <!-- Display Charts -->
    <div v-if="originalPlot" class="flex flex-col items-center space-y-8">
        <div class="chart-container">
            <h2 class="text-xl font-bold mt-4 text-center">Original Price Chart</h2>
            <img :src="originalPlot" alt="Original Chart" class="chart-image" />
        </div>

        <div class="chart-container">
            <h2 class="text-xl font-bold mt-4 text-center">Predicted Price Chart</h2>
            <img :src="predictedPlot" alt="Predicted Chart" class="chart-image" />
        </div>

        <div class="chart-container">
            <h2 class="text-xl font-bold mt-4 text-center">Future Predictions</h2>
            <img :src="futurePlot" alt="Future Predictions" class="chart-image" />
        </div>
    </div>


</template>

<script>
import axios from 'axios';

export default {
    name: "PredictButton",
    data() {
        return {
            coin: '',
            days: 7,
            originalPlot: "",  // Store base64 chart
            predictedPlot: "",
            futurePlot: "",
            loading: false,
            error: null
        };
    },
    methods: {
        async fetchPrediction() {
            console.log("Selected Coin:", this.coin);
            console.log("Selected Days:", this.days);  // Debugging

            this.loading = true;
            this.error = null;

            try {
                const response = await axios.post('http://127.0.0.1:8000/api/v1/predictedCryptoData/', {
                    coin: this.coin,
                    no_of_days: this.days
                });

                console.log("Response:", response.data);  // Debugging

                this.originalPlot = response.data.original_plot;
                this.predictedPlot = response.data.predicted_plot;
                this.futurePlot = response.data.future_plot;
            } catch (err) {
                console.error("Fetch error:", err);
                this.error = "Failed to fetch data. Please try again.";
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>

<style scoped>
.chart-container {
    width: 90%;
    max-width: 1200px;
    /* Make it large */
    text-align: center;
}

.chart-image {
    width: 100%;
    /* Full width */
    max-height: 600px;
    /* Increase height */
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease-in-out;
}

/* Zoom effect on hover */
.chart-image:hover {
    transform: scale(1.1);
}
</style>
