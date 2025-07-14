<template>
    <div>
      <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50 mb-6" />
      <div class="min-h-screen bg-[#fafafa] px-4 py-6">
        <div class="mb-6">
          <h1 class="text-2xl font-semibold mb-1 text-left">Top Coins</h1>
          <p class="text-gray-600 text-sm text-left">Here are the top 20 coins</p>
        </div>
  
        <div v-if="loading" class="text-center text-gray-600 py-10 text-sm">
          Loading data...
        </div>
  
        <div v-else class="overflow-x-auto bg-white rounded-2xl shadow transition-all duration-300">
          <table class="w-full divide-y divide-gray-200">
            <thead class="bg-gray-100">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">#</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">Coin</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">Current Price</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">24h</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">7d</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">Market Cap</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">High</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">Low</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700">Volume</th>
              </tr>
            </thead>
            <tbody>
              <router-link
                v-for="(item, index) in coins"
                :key="index"
                :to="`/coin/${item.coin}`"
                custom
                v-slot="{ navigate, href }"
              >
                <tr
                  @click="navigate"
                  :href="href"
                  class="hover:bg-blue-50 transition duration-200 ease-in-out cursor-pointer"
                  :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
                >
                  <td class="px-4 py-4 text-left text-sm text-gray-700 font-medium">{{ index + 1 }}</td>
                  <td class="px-4 py-4 text-sm text-gray-800">
                    <div class="flex items-center space-x-3">
                      <img
                        v-if="item.image_url"
                        :src="item.image_url"
                        alt="coin"
                        class="w-6 h-6 object-contain"
                      />
                      <span class="font-semibold text-left text-gray-900">{{ item.coin }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-4 text-left text-sm text-gray-800">
                    ${{ formatNumber(item.current_price) }}
                  </td>
                  <td class="px-4 py-4 text-left text-sm">
                    <span
                      :class="{
                        'text-green-600 font-semibold': item.percent_change_24h > 0,
                        'text-red-600 font-semibold': item.percent_change_24h < 0,
                        'text-gray-500': item.percent_change_24h === 0
                      }"
                    >
                      <template v-if="item.percent_change_24h > 0">
                        ▲ {{ item.percent_change_24h.toFixed(2) }}%
                      </template>
                      <template v-else-if="item.percent_change_24h < 0">
                        ▼ {{ item.percent_change_24h.toFixed(2) }}%
                      </template>
                      <template v-else>
                        0.00%
                      </template>
                    </span>
                  </td>
                  <td class="px-4 py-4 text-left text-sm">
                    <span
                      :class="{
                        'text-green-600 font-semibold': item.percent_change_7d > 0,
                        'text-red-600 font-semibold': item.percent_change_7d < 0,
                        'text-gray-500': item.percent_change_7d === 0
                      }"
                    >
                      <template v-if="item.percent_change_7d > 0">
                        ▲ {{ item.percent_change_7d.toFixed(2) }}%
                      </template>
                      <template v-else-if="item.percent_change_7d < 0">
                        ▼ {{ item.percent_change_7d.toFixed(2) }}%
                      </template>
                      <template v-else>
                        0.00%
                      </template>
                    </span>
                  </td>
                  <td class="px-4 py-4 text-left text-sm text-gray-800">
                    ${{ formatNumber(item.market_cap) }}
                  </td>
                  <td class="px-4 py-4 text-left text-sm text-gray-800">
                    ${{ formatNumber(item.high_price) }}
                  </td>
                  <td class="px-4 py-4 text-left text-sm text-gray-800">
                    ${{ formatNumber(item.low_price) }}
                  </td>
                  <td class="px-4 py-4 text-left text-sm text-gray-800">
                    {{ item.volume_to != null ? '$' + formatNumber(item.volume_to) : '-' }}
                  </td>
                </tr>
              </router-link>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from "@/components/NavbarCom.vue";
  import axios from "axios";
  
  export default {
    name: "CoinListPage",
    components: {
      Navbar,
    },
    data() {
      return {
        coins: [],
        loading: true,
      };
    },
    methods: {
      async fetchCoins() {
        try {
          const response = await axios.get("http://localhost:8000/api/v1/allCoinDetailList/");
          this.coins = response.data;
        } catch (error) {
          console.error("Failed to fetch coins:", error);
        } finally {
          this.loading = false;
        }
      },
      formatNumber(value) {
        if (value == null || isNaN(value)) return "-";
        const num = parseFloat(value);
        if (num >= 1_000_000_000) return (num / 1_000_000_000).toFixed(2) + "B";
        if (num >= 1_000_000) return (num / 1_000_000).toFixed(2) + "M";
        if (num >= 1_000) return (num / 1_000).toFixed(2) + "K";
        return num.toFixed(2);
      },
    },
    mounted() {
      this.fetchCoins();
    },
  };
  </script>
  
  <style scoped>
  /* Optional styling */
  </style>
  