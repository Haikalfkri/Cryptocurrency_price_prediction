<template>
    <form @submit.prevent="fetchCryptoData" class="flex items-center max-w-2xl mx-auto mt-10">
        <label for="voice-search" class="sr-only">Search</label>
        <div class="relative w-full">
            <input v-model="cryptoName" type="text" id="crypto-search"
                class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Search Crypto e.g bitcoin" required />
        </div>
        <button type="submit"
            class="inline-flex items-center py-2.5 px-3 ms-2 text-sm font-medium text-white bg-blue-700 rounded-2xl border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>Search
        </button>
    </form>
</template>

<script>
import axios from 'axios';

export default {
    name: "CryptoSearchButton",
    data() {
        return {
            cryptoName: "",
            loading: false,
            error: null,
        }
    },
    methods: {
        async fetchCryptoData() {
            if (!this.cryptoName) return;

            this.loading = true;
            this.error = null;

            try {
                // send request to the fetch crypto data api
                const response = await axios.post("http://localhost:8000/api/v1/fetchCryptoData/", {
                    coin: this.cryptoName.toLowerCase(),
                });
                
                localStorage.setItem("coin", this.cryptoName.toLowerCase())
                // navigate to cryptoDetailPage with the fetched data
                this.$router.push({
                    path: "/CryptoDetailPage",
                    query: response.data, // pas data via query params
                });

            } catch (err) {
                this.error = "Failed to fetch data. Please try again."
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>