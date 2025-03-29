<template>
    <div class="flex flex-col items-center justify-center relative mb-10 px-4">
        <!-- Back Button (Aligned with First Row of Card) -->
        <button @click="$router.push('/')"
            class="absolute left-4 sm:left-6 md:left-10 top-0 mt-16 sm:mt-20 p-2">
            <svg class="w-6 h-6 text-gray-800" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                fill="none" viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 5H1m0 0 4 4M1 5l4-4" />
            </svg>
        </button>

        <!-- Centered Card -->
        <div class="">
            <CardCryptoData :cryptoData="cryptoData" />
        </div>

        <!-- Chart Section -->
        <div class="w-full flex justify-center">
            <CryptoChart :coin="coinName" />
        </div>

        <!-- Description Section -->
        <div class="w-full max-w-3xl mt-10 text-left px-4">
            <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900">Description</h5>
            <p class="text-md text-gray-900">
                {{ cryptoData?.Description || "No description available." }}
            </p>
        </div>
    </div>
</template>


<script>
import CardCryptoData from '@/components/CardCryptoData.vue';
import CryptoChart from '@/components/CryptoChart.vue';

export default {
    name: "CryptoDetailPage",
    components: {
        CardCryptoData,
        CryptoChart,
    },
    data() {
        return {
            cryptoData: this.$route.query, // get data from route query
        }
    },
    computed: {
        coinName() {
            return localStorage.getItem("coin") || "";
        }
    },
}
</script>
