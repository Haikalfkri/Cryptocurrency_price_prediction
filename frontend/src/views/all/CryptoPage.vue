<template>
  <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50" />
  
  <div class="mt-6">
    <CryptoSearchButton />
  </div>

  <div class="container mx-auto px-4 mt-10">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div
        v-for="(news, index) in displayedNews"
        :key="index"
        @click="openLink(news.link)"
        class="cursor-pointer rounded-lg overflow-hidden shadow-md hover:shadow-lg transition duration-300 bg-white transform hover:scale-105"
      >
        <transition name="pop-up">
          <img
            v-if="news.image"
            :src="news.image"
            alt="News Image"
            class="w-full h-40 object-cover"
          />
          <img
            v-else
            src="https://b2161880.smushcdn.com/2161880/wp-content/uploads/2023/07/financial-stock-market-exchange-gold-coins-global-economic-chart-generative-ai.jpg?lossy=1&strip=1&webp=1"
            alt="Default Image"
            class="w-full h-40 object-cover"
          />
        </transition>
        <div class="p-4">
          <h2 class="text-md font-semibold line-clamp-2">{{ news.title }}</h2>
        </div>
      </div>
    </div>

    <div class="flex justify-center mt-6 mb-6" v-if="displayedNews.length < allNews.length">
      <button
        @click="showMore"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300"
      >
        Show More
      </button>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import CryptoSearchButton from '@/components/CryptoSearchButton.vue';
import axios from 'axios';

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
    };
  },
  methods: {
    async fetchNews() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/cryptoNewsList/');
        this.allNews = response.data;
        this.displayedNews = this.allNews.slice(0, this.itemsToShow);
      } catch (error) {
        console.error('Error fetching news:', error);
      }
    },
    showMore() {
      this.itemsToShow += 4;
      this.displayedNews = this.allNews.slice(0, this.itemsToShow);
    },
    openLink(link) {
      window.open(link, '_blank');
    },
  },
  mounted() {
    this.fetchNews();
  },
};
</script>

<style scoped>
/* Optional: untuk membatasi 2 baris title */
.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Pop-up animation */
.pop-up-enter-active, .pop-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.pop-up-enter, .pop-up-leave-to /* .pop-up-leave-active in <2.1.8 */ {
  transform: scale(1.1);
  opacity: 0;
}
</style>
