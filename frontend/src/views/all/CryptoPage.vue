<template>
  <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50" />

  <div class="mt-6">
    <CryptoSearchButton />
  </div>

  <div class="container mx-auto px-4 mt-10">
    <!-- Loading Spinner -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <!-- News Masonry Grid -->
    <transition-group name="fade-pop" tag="div" class="news-masonry-container">
      <div
        v-for="(news, index) in displayedNews"
        :key="news.link"
        @click="openLink(news.link)"
        class="news-card cursor-pointer rounded-lg overflow-hidden shadow-md hover:shadow-lg transition duration-300 bg-white transform relative group"
        @mouseenter="expandSummary(index)"
        @mouseleave="collapseSummary(index)"
      >
        <img v-if="isValidImage(news.image)" :src="news.image" alt="News Image" class="w-full h-40 object-cover" />
        <img v-else
          src="https://b2161880.smushcdn.com/2161880/wp-content/uploads/2023/07/financial-stock-market-exchange-gold-coins-global-economic-chart-generative-ai.jpg?lossy=1&strip=1&webp=1"
          alt="Default Image" class="w-full h-40 object-cover" />
        <div class="p-4">
          <h2 class="text-md text-center font-semibold line-clamp-2">{{ news.title }}</h2>

          <!-- Hover Reveal Content -->
          <div
            ref="hoverDetails"
            :style="{ maxHeight: expandedIndex === index ? summaryHeights[index] + 'px' : '0px' }"
            class="hover-details overflow-hidden transition-max-height duration-300"
          >
            <p class="text-sm text-left text-gray-600 mt-2 mb-2 text-justify">{{ news.summary }}</p>
            <p class="text-sm text-center text-gray-500 news-date">{{ formatDate(news.date) }}</p>
          </div>
        </div>

        <span v-if="news.sentiment" :class="[
            'inline-block px-3 py-1 text-xs font-semibold rounded-full mb-4',
            {
              'bg-green-100 text-green-800': news.sentiment === 'Good',
              'bg-red-100 text-red-800': news.sentiment === 'Bad',
              'bg-gray-200 text-gray-800': news.sentiment === 'Neutral'
            }
          ]">
          {{ news.sentiment }}
        </span>
      </div>
    </transition-group>

    <!-- Show More Button -->
    <div class="flex justify-center mt-4 mb-4" v-if="displayedNews.length <= allNews.length && !isLoading">
      <button @click="showMore"
        class="px-2 py-2 bg-blue-600 text-white text-md rounded-lg hover:bg-blue-700 transition duration-300">
        Read More
      </button>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import CryptoSearchButton from '@/components/CryptoSearchButton.vue';
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

export default {
  name: "AdminCryptoPage",
  components: {
    Navbar,
    CryptoSearchButton,
  },
  data() {
    return {
      allNews: [],
      displayedNews: [],
      itemsToShow: 8,
      isLoading: true,
      expandedIndex: null,
      summaryHeights: [], // simpan tinggi tiap summary
    };
  },
  methods: {
    async fetchNews() {
      this.isLoading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/cryptoNewsList/', {
          withCredentials: true
        });
        this.allNews = response.data;
        this.displayedNews = this.allNews.slice(0, this.itemsToShow);

        // Reset tinggi summary (buat nanti di hover)
        this.$nextTick(() => {
          this.calculateSummaryHeights();
        });
      } catch (error) {
        console.error('Error fetching news:', error);
      } finally {
        this.isLoading = false;
      }
    },
    showMore() {
      this.itemsToShow += 8;
      this.displayedNews = this.allNews.slice(0, this.itemsToShow);
      this.$nextTick(() => {
        this.calculateSummaryHeights();
      });
    },
    openLink(link) {
      window.open(link, '_blank');
    },
    isValidImage(url) {
      if (!url || url === "null" || url.trim() === "") return false;
      const unsupportedFormats = ['.webp', '.svg'];
      return !unsupportedFormats.some(ext => url.toLowerCase().endsWith(ext));
    },
    formatDate(dateStr) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },

    calculateSummaryHeights() {
      // Reset dulu arraynya
      this.summaryHeights = [];

      this.$refs.hoverDetails.forEach((el) => {
        if (!el) {
          this.summaryHeights.push(0);
          return;
        }
        // supaya dapat tinggi asli konten, kita set dulu maxHeight ke 'none' lalu ambil scrollHeight
        el.style.maxHeight = 'none';
        const height = el.scrollHeight;
        this.summaryHeights.push(height);
        // reset lagi maxHeight ke 0 supaya hidden
        el.style.maxHeight = '0px';
      });
    },

    expandSummary(index) {
      this.expandedIndex = index;
    },
    collapseSummary() {
      this.expandedIndex = null;
    },
  },
  mounted() {
    this.fetchNews();
  },
};
</script>

<style scoped>
.news-masonry-container {
  column-count: 4;
  column-gap: 1.5rem;
}

.news-masonry-container > div {
  break-inside: avoid;
  margin-bottom: 1.5rem;

  display: inline-block;
  width: 100%;
  cursor: pointer;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
  background-color: white;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  position: relative;
}

.news-masonry-container > div:hover {
  box-shadow: 0 10px 15px rgb(0 0 0 / 0.2);
  transform: scale(1.05);
}

.news-masonry-container img {
  width: 100%;
  height: 10rem;
  object-fit: cover;
}

.news-masonry-container .p-4 {
  padding: 1rem;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.hover-details {
  overflow: hidden;
  transition: max-height 0.3s ease;
  margin-top: 0.5rem;
  max-height: 0px;
  will-change: max-height;
}

.hover-details p {
  margin: 0;
}

span {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
  margin-bottom: 1rem;
  color: #374151;
}

.bg-green-100 {
  background-color: #dcfce7;
  color: #166534;
}

.bg-red-100 {
  background-color: #fee2e2;
  color: #991b1b;
}

.bg-gray-200 {
  background-color: #e5e7eb;
  color: #374151;
}

@media (max-width: 1024px) {
  .news-masonry-container {
    column-count: 3;
  }
}

@media (max-width: 768px) {
  .news-masonry-container {
    column-count: 2;
  }
}

@media (max-width: 480px) {
  .news-masonry-container {
    column-count: 1;
  }
}

</style>
