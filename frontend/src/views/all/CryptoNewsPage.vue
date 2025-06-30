<template>
  <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50 mb-6" />
  <div class="min-h-screen bg-[#fafafa] px-4 py-6">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold mb-1 text-left">Latest Crypto News</h1>
      <p class="text-gray-600 text-sm text-left">
        Here are the latest news articles related to cryptocurrency, updated in real-time.
      </p>
    </div>

    <div
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 transition-all duration-300 ease-in-out"
    >
      <a
        v-for="(news, index) in paginatedNews"
        :key="index"
        :href="news.link"
        target="_blank"
        class="group bg-white shadow-md rounded-xl p-4 hover:shadow-xl transition-all duration-300 transform hover:scale-[1.01] flex flex-col justify-between relative overflow-hidden"
      >
        <img
          v-if="news.image"
          :src="imageSources[index] || news.image"
          :alt="`news image ${index}`"
          class="w-full h-32 object-cover rounded-md mb-3"
          loading="lazy"
          @error="handleImageError(index)"
        />

        <div class="flex-grow text-left">
          <h2 class="text-sm font-bold mb-2">{{ news.title }}</h2>
          <p class="text-sm text-gray-500">{{ formatDate(news.published_at) }}</p>
        </div>

        <!-- Sentiment badge -->
        <div class="mt-4 flex justify-center">
          <span
            :class="[
              'px-3 py-1 text-xs font-semibold rounded-full',
              news.sentiment === 'Good'
                ? 'bg-green-100 text-green-700'
                : news.sentiment === 'Bad'
                ? 'bg-red-100 text-red-700'
                : 'bg-gray-200 text-gray-700'
            ]"
          >
            {{ news.sentiment }}
          </span>
        </div>

        <!-- Summary -->
        <div
          class="absolute bottom-0 left-0 w-full bg-white bg-opacity-95 px-4 py-3 text-sm text-gray-700 opacity-0 translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300 ease-in-out max-h-40 overflow-auto rounded-b-xl z-10"
        >
          {{ news.summary }}
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
  name: "CryptoNewsPage",
  components: {
    Navbar,
  },
  data() {
    return {
      newsList: [],
      currentPage: 1,
      pageSize: 12,
      imageSources: {}, // will store valid or fallback images
      fallbackImage:
        "https://www.pymnts.com/wp-content/uploads/2021/05/us-eyes-regulatory-perimeter-for-cryptos.jpg",
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
    handleImageError(index) {
      this.imageSources[index] = this.fallbackImage;
    },
  },
  mounted() {
    this.fetchNews();
  },
};
</script>

<style scoped>
/* All styles handled by Tailwind */
</style>
