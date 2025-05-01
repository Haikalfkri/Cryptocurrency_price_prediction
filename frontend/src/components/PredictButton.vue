<template>
    <form @submit.prevent="fetchPrediction" class="flex items-center max-w-2xl mx-auto space-x-2">
        <label for="crypto-search" class="sr-only">Search</label>

        <!-- Search Input -->
        <div class="relative w-full">
            <input v-model="coin" type="text" id="crypto-search" class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5
         dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search Crypto e.g BTC-USD, ETH-USD" required
                @input="fetchCryptoList" />

            <!-- Dropdown -->
            <ul v-if="cryptoList.length > 0"
                class="absolute bg-white border border-gray-300 w-full mt-1 rounded-lg shadow-lg max-h-48 overflow-y-auto z-10">
                <li v-for="(crypto, index) in cryptoList" :key="index" @click="selectCrypto(crypto.name)"
                    class="text-left p-2 cursor-pointer hover:bg-blue-100">
                    {{ crypto.name }}
                </li>
            </ul>
        </div>

        <!-- Dropdown -->
        <select v-model="days" id="days-filter" class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500
        p-2.5 dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option :value="2">2 Days</option>
            <option :value="7">7 Days</option>
            <option :value="14">14 Days</option>
        </select>

        <!-- Search Button -->
        <button type="submit" :disabled="loading"
            class="inline-flex items-center py-2.5 px-3 text-sm font-medium text-white bg-blue-700 rounded-2xl border border-blue-700
    hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">

            <!-- Loading Spinner -->
            <svg v-if="loading" class="animate-spin h-4 w-4 text-white mr-2" xmlns="http://www.w3.org/2000/svg"
                fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>

            <!-- Search Icon (Hide when loading) -->
            <svg v-else class="w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>

            <span>{{ loading ? 'Loading...' : 'Search' }}</span>
        </button>
    </form>
</template>

<script>
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

export default {
    name: "PredictButton",
    data() {
        return {
            coin: '',
            days: 2,
            loading: false,
            error: null,
            cryptoList: [],  // Daftar cryptocurrency yang muncul saat mengetik
            debounceTimeout: null,  // Untuk debouncing
        };
    },
    methods: {
        async fetchPrediction() {
            console.log("Selected Coin:", this.coin);
            console.log("Selected Days:", this.days);  // Debugging

            this.loading = true;
            this.error = null;

            try {
                const response = await axios.post('https://6f33-103-150-218-251.ngrok-free.app/api/v1/predictedCryptoData/', {
                    coin: this.coin,
                    no_of_days: this.days
                },
                {
                    withCredentials: true
                }
            );

                console.log("Response:", response.data);  // Debugging

                localStorage.setItem("predictionResponse", JSON.stringify(response.data));

                this.$router.push("/cryptoPredictionPage");
            } catch (err) {
                console.error("Fetch error:", err);
                this.error = "Failed to fetch data. Please try again.";
            } finally {
                this.loading = false;
            }
        },

        async fetchCryptoList() {
            // Hapus timeout sebelumnya jika ada
            if (this.debounceTimeout) {
                clearTimeout(this.debounceTimeout);
            }

            // Tunggu sebentar sebelum melakukan request ke API (debouncing)
            this.debounceTimeout = setTimeout(async () => {
                if (this.coin.length < 3) {
                    this.cryptoList = []; // Hapus daftar jika input terlalu pendek
                    return;
                }

                try {
                    const response = await axios.get('http://127.0.0.1:8000/api/v1/cryptoList/');
                    this.cryptoList = response.data.filter(crypto =>
                        crypto.name.toLowerCase().includes(this.coin.toLowerCase())
                    );
                } catch (err) {
                    console.error("Fetch crypto list error:", err);
                    this.cryptoList = [];
                }
            }, 500); // Delay 500ms sebelum request
        },

        selectCrypto(cryptoName) {
            this.coin = cryptoName;  // Set input ke nama yang dipilih
            this.cryptoList = [];  // Hapus dropdown setelah memilih
        }
    }
}
</script>


<style scoped>
.chart-container {
    width: 90%;
    max-width: 1200px;
    /* Make it large */
    text-align: center;
}

.chart-image {
    width: 100%;
    /* Full width */
    max-height: 600px;
    /* Increase height */
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease-in-out;
}

/* Zoom effect on hover */
.chart-image:hover {
    transform: scale(1.1);
}
</style>
