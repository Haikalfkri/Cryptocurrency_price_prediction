<template>
    <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50 mb-6" />
    <div class="min-h-screen bg-[#fafafa] px-4 py-6">
      <div class="mb-6">
        <h1 class="text-2xl font-semibold mb-1 text-left">Latest Crypto News</h1>
        <p class="text-gray-600 text-sm text-left">
          Here are the latest news articles related to cryptocurrency, updated in real-time.
        </p>
      </div>
  
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-6 transition-all duration-300 ease-in-out">
        <a
          v-for="(news, index) in paginatedNews"
          :key="index"
          :href="news.link"
          target="_blank"
          class="bg-white shadow-md rounded-xl p-4 hover:shadow-xl transition-shadow duration-300 flex flex-col justify-between hover:scale-[1.01] transform transition-transform"
        >
          <img
            v-if="news.image"
            :src="news.image"
            alt="news image"
            class="w-full h-32 object-cover rounded-md mb-3"
            loading="lazy"
          />
          <div class="flex-grow text-left">
            <h2 class="text-sm font-bold mb-2">{{ news.title }}</h2>
            <p class="text-sm text-gray-500">{{ formatDate(news.date) }}</p>
          </div>
        </a>
      </div>
  
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
    name: "CryptoNewsPage",
    components: {
      Navbar,
    },
    data() {
      return {
        newsList: [],
        currentPage: 1,
        pageSize: 10,
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
          const res = await axios.get("http://127.0.0.1:8000/api/v1/cryptoNewsList/");
          this.newsList = res.data;
        } catch (error) {
          console.error("Failed to fetch news:", error);
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
    },
    mounted() {
      this.fetchNews();
    },
  };
  </script>
  
  <style scoped>
  /* Removed line-clamp for full title display */
  </style>
  