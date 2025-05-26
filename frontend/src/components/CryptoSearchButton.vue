<template>
    <form @submit.prevent="fetchCryptoData" class="flex items-center max-w-2xl mx-auto mt-10">
      <label for="crypto-search" class="sr-only">Search</label>
      <div class="relative w-full">
        <input
          v-model="cryptoName"
          type="text"
          id="crypto-search"
          placeholder="Search Crypto e.g bitcoin"
          required
          class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
        />
      </div>
      <button
        type="submit"
        :disabled="loading"
        class="inline-flex items-center py-2.5 px-4 ms-2 text-sm font-medium text-white bg-blue-700 rounded-2xl border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 disabled:opacity-70 disabled:cursor-not-allowed"
      >
        <svg
          v-if="loading"
          class="animate-spin w-4 h-4 me-2 text-white"
          fill="none"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
          ></path>
        </svg>
        <svg
          v-else
          class="w-4 h-4 me-2"
          fill="none"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
        {{ loading ? 'Loading...' : 'Search' }}
      </button>
    </form>
  </template>
  
  <script>
  import axios from 'axios';
  
  axios.defaults.headers.common['ngrok-skip-browser-warning'] = true;
  
  export default {
    name: 'CryptoSearchButton',
    data() {
      return {
        cryptoName: '',
        loading: false,
        error: null,
      };
    },
    methods: {
      async fetchCryptoData() {
        if (!this.cryptoName) return;
  
        this.loading = true;
        this.error = null;
  
        try {
          const response = await axios.post(
            'http://127.0.0.1:8000/api/v1/fetchCryptoData/',
            { coin: this.cryptoName.toLowerCase() },
            { withCredentials: true }
          );
  
          localStorage.setItem('coin', this.cryptoName.toLowerCase());
  
          this.$router.push({
            path: '/CryptoDetailPage',
            query: response.data,
          });
        } catch (err) {
          this.error = 'Failed to fetch data. Please try again.';
          console.error(err);
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Optional: Smooth spinner animation */
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  </style>
  