<template>
    <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50 mb-6" />
    <div class="min-h-screen bg-[#fafafa] px-4 py-6">
      <h1 class="text-2xl font-semibold mb-1 text-left">Top Crypto Insights</h1>
      <p class="text-gray-600 mb-6 text-left">
        This section shows curated crypto insights from top sources like CryptoCompare and CryptoSlate.
      </p>
  
      <!-- Grid 4 kolom -->
      <div class="grid grid-cols-1 gap-6 transition-all duration-300 ease-in-out sm:grid-cols-2 md:grid-cols-3">
        <a
          v-for="(news, index) in paginatedNews"
          :key="index"
          :href="news.link"
          target="_blank"
          class="bg-white shadow-md rounded-xl p-4 hover:shadow-xl transition-shadow duration-300 flex gap-4 hover:bg-blue-50"
          style="height: 120px;"
        >
          <!-- Left: Image -->
          <div class="w-1/3 flex-shrink-0">
            <img
              v-if="news.image"
              :src="news.image"
              alt="news image"
              class="w-full h-full object-cover rounded-md"
              loading="lazy"
            />
            <div v-else class="w-full h-full bg-gray-200 rounded-md flex items-center justify-center text-gray-400 text-sm">
              No Image
            </div>
          </div>
  
          <!-- Right: Content -->
          <div class="flex flex-col justify-between w-2/3">
            <!-- Title max 2 baris dengan ellipsis -->
            <p class="text-sm font-bold text-left title-clamp">
              {{ news.title }}
            </p>
  
            <p class="text-xs text-gray-500 text-left">{{ formatDate(news.date) }}</p>
  
            <div class="flex justify-start gap-2 mt-1">
              <div
                v-if="extractTag(news.tags)"
                :class="['px-2 py-0.5 rounded-full text-xs font-semibold text-white', tagColorClass(extractTag(news.tags))]"
              >
                {{ extractTag(news.tags) }}
              </div>
              <div class="px-2 py-0.5 rounded-full text-xs font-semibold text-gray-700 bg-gray-300">
                {{ news.source || 'Unknown Source' }}
              </div>
            </div>
          </div>
        </a>
      </div>
  
      <!-- Pagination -->
      <div class="flex flex-wrap justify-center mt-8 space-x-2">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page"
          :class="[
            'px-3 py-1 rounded-md transition-colors mb-2',
            currentPage === page
              ? 'bg-blue-600 text-white'
              : 'bg-white text-blue-600 border border-blue-600 hover:bg-blue-100'
          ]"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from "@/components/NavbarCom.vue";
  import axios from "axios";
  
  axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;
  
  export default {
    name: "CryptoInsightPage",
    components: {
      Navbar,
    },
    data() {
      return {
        newsList: [],
        currentPage: 1,
        pageSize: 12,
        categories: ['BTC','ETH','USDT','BNB','SOL','XRP','DOGE','TON','ADA','AVAX'],
      };
    },
    computed: {
      totalPages() {
        return Math.ceil(this.newsList.length / this.pageSize);
      },
      paginatedNews() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.newsList.slice(start, end);
      },
    },
    methods: {
      async fetchNews() {
        try {
          const res = await axios.get("http://127.0.0.1:8000/api/v1/cryptoInsightList/");
          this.newsList = res.data;
        } catch (error) {
          console.error("Failed to fetch insight news:", error);
        }
      },
      formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric",
        });
      },
      extractTag(tags) {
        if (!tags) return null;
        const parts = tags.split('|');
        for (const part of parts) {
          if (this.categories.includes(part)) {
            return part;
          }
        }
        return null;
      },
      tagColorClass(tag) {
        const colors = {
          BTC: 'bg-yellow-500',
          ETH: 'bg-purple-600',
          USDT: 'bg-green-500',
          BNB: 'bg-yellow-400',
          SOL: 'bg-cyan-500',
          XRP: 'bg-blue-600',
          DOGE: 'bg-orange-400',
          TON: 'bg-gray-600',
          ADA: 'bg-red-600',
          AVAX: 'bg-pink-600',
        };
        return colors[tag] || 'bg-gray-500';
      },
    },
    mounted() {
      this.fetchNews();
    },
  };
  </script>
  
  <style scoped>
  .title-clamp {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-word;
  }
  </style>
  