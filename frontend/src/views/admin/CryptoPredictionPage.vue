<template>
    <div class="flex flex-col items-center justify-center relative mb-10 px-4">
        <!-- Back Button -->
        <button @click="$router.push('/predictPage')"
            class="absolute left-4 sm:left-6 md:left-10 top-0 mt-16 sm:mt-20 p-2">
            <svg class="w-6 h-6 text-gray-800" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 5H1m0 0 4 4M1 5l4-4" />
            </svg>
        </button>

        <!-- Chart Section -->
        <div v-if="originalPlot" class="flex flex-col items-center space-y-6 mt-10">
            <div class="chart-container">
                <h2 class="text-xl font-bold mb-5">Original Price Chart</h2>
                <img :src="originalPlot" alt="Original Chart" class="chart-image" />
            </div>

            <div class="chart-container">
                <h2 class="text-xl font-bold mb-5">Predicted Price Chart</h2>
                <img :src="predictedPlot" alt="Predicted Chart" class="chart-image" />
            </div>

            <div class="chart-container">
                <h2 class="text-xl font-bold mb-5">Future Predictions</h2>
                <img :src="futurePlot" alt="Future Predictions" class="chart-image" />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CryptoPredictionPage",
    data() {
        return {
            originalPlot: null,
            predictedPlot: null,
            futurePlot: null,
            sentimentAnalysis: []
        };
    },
    methods: {
    },
    mounted() {
        // Load from route query or localStorage
        this.originalPlot = this.$route.query.originalPlot || localStorage.getItem("originalPlot");
        this.predictedPlot = this.$route.query.predictedPlot || localStorage.getItem("predictedPlot");
        this.futurePlot = this.$route.query.futurePlot || localStorage.getItem("futurePlot");
    }
};
</script>

<style scoped>
.chart-container {
    width: 90%;
    max-width: 1200px;
    text-align: center;
}

.chart-image {
    width: 100%;
    max-height: 600px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease-in-out;
}

.chart-image:hover {
    transform: scale(1.1);
}
</style>
