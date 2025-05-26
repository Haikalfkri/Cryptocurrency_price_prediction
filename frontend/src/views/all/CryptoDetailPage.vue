<template>
    <div class="relative min-h-screen bg-white">
      <!-- Back Button Fixed Bottom Left -->
      <button
        @click="$router.push('/')"
        class="fixed bottom-4 left-4 z-50 flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-xl shadow-md hover:bg-blue-700"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 14 10" xmlns="http://www.w3.org/2000/svg">
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 5H1m0 0 4 4M1 5l4-4"
          />
        </svg>
        Back
      </button>
  
      <!-- Main Content -->
      <div class="flex flex-col md:flex-row h-full min-h-screen">
        <!-- Left: Crypto Cards -->
        <div
          class="w-full md:w-[430px] p-3 overflow-y-auto"
          style="border-right-width: 1px;"
        >
          <CardCryptoData :cryptoData="cryptoData" />
        </div>
  
        <!-- Chart and Description Side-by-Side on md+, stacked on mobile -->
        <div class="flex-1 mb-1 overflow-y-auto p-4 flex flex-col space-y-6">
          <!-- Apex Chart full width -->
          <div class="flex-1 w-full">
            <CryptoChart :coin="coinName" />
          </div>
  
          <!-- Description -->
          <div class="text-gray-900 text-left md:text-justify">
            <p class="text-md mb-3 font-bold">About {{ coinName }}</p>
            <p class="text-md">
              {{ cryptoData?.Description || "No description available." }}
            </p>
          </div>
        </div>
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
        cryptoData: this.$route.query,
      };
    },
    computed: {
      coinName() {
        return localStorage.getItem("coin") || "";
      },
    },
  };
  </script>
  
  <style scoped>
  /* Optional: agar height main content full viewport */
  html,
  body,
  #app {
    height: 100%;
    margin: 0;
  }
  </style>
  