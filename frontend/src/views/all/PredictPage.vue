<template>
    <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50" />

    <div class="flex justify-center mt-10">
        <div class="w-full max-w-2xl">
            <PredictButton class="w-full text-sm rounded-2xl" />
        </div>
    </div>

    <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
        <!-- Top Volume Card -->
        <div v-if="allDataFetched" class="bg-white rounded-xl shadow-lg p-4 animate-popup">
            <h2 class="text-lg font-bold mb-4 text-center">Top Volume</h2>
            <table class="w-full text-sm border-separate border-spacing-2">
                <thead>
                    <tr>
                        <th class="text-left">Name</th>
                        <th class="text-right">Total Volume</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="coin in topVolume" :key="coin.id">
                        <td class="text-left">{{ coin.name }}</td>
                        <td class="text-right">{{ coin.total_volume.toLocaleString() }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Trending Coin Card -->
        <div v-if="allDataFetched" class="bg-white rounded-xl shadow-lg p-4 animate-popup">
            <h2 class="text-lg font-bold mb-4 text-center">Trending Coin</h2>
            <table class="w-full text-sm border-separate border-spacing-2">
                <thead>
                    <tr>
                        <th class="text-left">Name</th>
                        <th class="text-right">Price (BTC)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="coin in trendingCoins" :key="coin.name">
                        <td class="text-left">{{ coin.name }}</td>
                        <td class="text-right">{{ coin.price_btc.toFixed(8) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Market Cap Ranking Card -->
        <div v-if="allDataFetched" class="bg-white rounded-xl shadow-lg p-4 animate-popup">
            <h2 class="text-lg font-bold mb-4 text-center">Market Cap Rankings</h2>
            <table class="w-full text-sm border-separate border-spacing-2">
                <thead>
                    <tr>
                        <th class="text-left">ID</th>
                        <th class="text-right">Price (USD)</th>
                        <th class="text-right">Rank</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="coin in marketCapRanking" :key="coin.id">
                        <td class="text-left">{{ coin.id }}</td>
                        <td class="text-right">${{ coin.current_price.toLocaleString() }}</td>
                        <td class="text-right">{{ coin.market_cap_rank }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Top Exchanges Card -->
        <div v-if="allDataFetched" class="bg-white rounded-xl shadow-lg p-4 animate-popup">
            <h2 class="text-lg font-bold mb-4 text-center">Top Exchanges</h2>
            <table class="w-full text-sm border-separate border-spacing-2">
                <thead>
                    <tr>
                        <th class="text-left">Name</th>
                        <th class="text-right">Year</th>
                        <th class="text-right">Score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="exchange in topExchanges" :key="exchange.id">
                        <td class="text-left">{{ exchange.name }}</td>
                        <td class="text-right">{{ exchange.year_established }}</td>
                        <td class="text-right">{{ exchange.trust_score }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import PredictButton from '@/components/PredictButton.vue';
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

export default {
    name: "PredictPage",
    components: {
        Navbar,
        PredictButton,
    },
    data() {
        return {
            topVolume: [],
            trendingCoins: [],
            marketCapRanking: [],
            topExchanges: [],
            allDataFetched: false, // Track if all data is fetched
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        async fetchData() {
            try {
                const [topVolumeRes, trendingCoinsRes, marketCapRes, topExchangesRes] = await Promise.all([
                    axios.get('https://6f33-103-150-218-251.ngrok-free.app/api/v1/topVolumeCoin/', { withCredentials: true }),
                    axios.get('https://6f33-103-150-218-251.ngrok-free.app/api/v1/trendingCoin/', { withCredentials: true }),
                    axios.get('https://6f33-103-150-218-251.ngrok-free.app/api/v1/marketCapRankings/', { withCredentials: true }),
                    axios.get('https://6f33-103-150-218-251.ngrok-free.app/api/v1/topExchangesRankings/', { withCredentials: true })
                ]);

                this.topVolume = topVolumeRes.data;
                this.trendingCoins = trendingCoinsRes.data;
                this.marketCapRanking = marketCapRes.data;
                this.topExchanges = topExchangesRes.data;

                this.allDataFetched = true; // All data is fetched, trigger the animation
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
    },
};
</script>

<style scoped>
@keyframes popup {
    0% {
        opacity: 0;
        transform: scale(0.8);
    }

    100% {
        opacity: 1;
        transform: scale(1);
    }
}

.animate-popup {
    animation: popup 0.6s ease-out forwards;
}

/* Biar tabelnya lebih rapi */
table th,
table td {
    padding: 8px 12px;
    border-bottom: 1px solid #ddd;
    /* sedikit garis bawah di tabel */
}

/* Shadow card yang lebih soft */
.shadow-lg {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Gaya untuk card headings */
h2 {
    font-size: 1.125rem;
    /* ukuran font heading */
    color: #333;
    /* teks gelap biar jelas */
}

/* Gaya umum untuk tabel */
table {
    width: 100%;
    border-collapse: collapse;
}

thead {
    background-color: #f9fafb;
    font-weight: bold;
}
</style>