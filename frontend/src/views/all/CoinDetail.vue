<template>
    <div>
        <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50 mb-6" />
        <div class="min-h-screen bg-[#fafafa] px-4 py-6 overflow-hidden">
            <div v-if="loading" class="text-center py-10 text-sm text-gray-500">
                Loading coin data...
            </div>

            <div v-else class="flex flex-col space-y-6 h-full">
                <!-- Top Info Row -->
                <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 flex-shrink-0">
                    <!-- Coin Info -->
                    <div class="flex items-center gap-4">
                        <img :src="coin.image_url" alt="coin"
                            class="w-16 h-16 sm:w-20 sm:h-20 object-contain rounded-lg" />
                        <div>
                            <h1 class="text-2xl sm:text-3xl font-bold leading-tight break-words">{{ coin.coin }}</h1>
                            <div v-if="coin.coin in coinFullNames" class="text-base sm:text-lg text-gray-500">
                                {{ coinFullNames[coin.coin] }}
                            </div>
                        </div>
                    </div>

                    <!-- Stats -->
                    <div class="flex flex-wrap justify-center md:justify-between gap-4 w-full md:w-auto">
                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">Price</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                ${{ formatNumber(coin.close_price) }}
                            </div>
                            <div :class="{
                                'text-green-500': coin.percent_change_24h > 0,
                                'text-red-500': coin.percent_change_24h < 0,
                                'text-gray-500': coin.percent_change_24h === 0
                            }" class="text-sm font-medium mt-1">
                                <template v-if="coin.percent_change_24h > 0">
                                    ▲ {{ formatPercent(coin.percent_change_24h) }}
                                </template>
                                <template v-else-if="coin.percent_change_24h < 0">
                                    ▼ {{ formatPercent(coin.percent_change_24h) }}
                                </template>
                                <template v-else>
                                    {{ formatPercent(coin.percent_change_24h) }}
                                </template>
                            </div>
                        </div>

                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">Market Cap</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                ${{ formatNumber(coin.market_cap) }}
                            </div>
                        </div>

                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">24H Volume</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                ${{ formatNumber(coin.volume_to) }}
                            </div>
                        </div>

                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">Circ Supply</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                {{ formatNumber(coin.circulating_supply) }}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Main Area -->
                <div class="flex flex-col md:flex-row flex-1 gap-6 overflow-hidden">
                    <!-- Left Cards -->
                    <div class="w-full md:w-1/4 flex-shrink-0 space-y-4 text-gray-800">
                        <div class="grid grid-cols-2 gap-3">
                            <div v-for="(label, index) in statCards" :key="index"
                                class="bg-white p-4 rounded-xl shadow text-center">
                                <div class="text-sm text-gray-500">{{ label.title }}</div>
                                <div
                                    :class="['text-lg font-bold text-gray-900', label.isPercent ? getPercentClass(label.value) : '']">
                                    <span v-if="label.isPercent">
                                        <span v-if="label.value > 0">▲</span>
                                        <span v-else-if="label.value < 0">▼</span>
                                        {{ formatPercent(label.value) }}
                                    </span>
                                    <span v-else>
                                        {{ label.prefix }}{{ formatNumber(label.value) }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Latest News -->
                        <div class="hidden md:block">
                            <h3 class="text-base text-left font-semibold text-gray-800 mb-4">Latest News</h3>
                            <ul class="space-y-6 text-sm text-left text-gray-700">
                                <li v-for="(item, index) in latestNews.slice(0, 10)" :key="index" class="border-b pb-2">
                                    <a :href="item.link" target="_blank" rel="noopener noreferrer"
                                        class="no-underline text-black hover:underline">
                                        <div class="font-medium">
                                            {{ item.title }}
                                        </div>
                                    </a>
                                    <div class="text-xs text-gray-500 flex mt-1">
                                        <span class="mr-4">{{ formatDate(item.published_at) }}</span>
                                        <span :class="{
                                            'text-green-600': item.sentiment === 'positive',
                                            'text-red-600': item.sentiment === 'negative',
                                            'text-gray-500': item.sentiment === 'neutral'
                                        }">
                                            {{ item.sentiment }}
                                        </span>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!-- Right Column -->
                    <div class="flex-1 overflow-y-auto pr-1 md:pr-2 space-y-6 min-w-0">
                        <!-- Chart -->
                        <div class="bg-white p-4 sm:p-6 rounded-2xl shadow">
                            <ChartSwitcher :coin="coinSymbol" />
                        </div>

                        <!-- Description -->
                        <div
                            class="bg-white p-4 sm:p-6 rounded-2xl shadow text-sm text-gray-800 leading-relaxed text-left">
                            <h2 class="text-lg font-semibold mb-3">Description</h2>
                            <p>{{ coin.description || 'No description available.' }}</p>
                        </div>

                        <!-- Prediction & Analysis -->
                        <div class="bg-white p-4 sm:p-6 rounded-2xl shadow">
                            <div class="flex items-center justify-between mb-4">
                                <h2 class="text-lg font-semibold">Prediction & Analysis</h2>
                                <select v-model="selectedDays" @change="fetchPrediction"
                                    class="border rounded p-1 text-sm">
                                    <option value="2">Last 2 Days</option>
                                    <option value="7">Last 7 Days</option>
                                    <option value="14">Last 14 Days</option>
                                </select>
                            </div>

                            <div v-if="prediction.length">
                                <Chart :data="chartData" />

                                <div class="flex flex-col md:flex-row gap-4 mt-6">
                                    <img :src="prediction[0].original_plot" class="w-full md:w-1/2 rounded shadow" />
                                    <img :src="prediction[0].predicted_plot" class="w-full md:w-1/2 rounded shadow" />
                                </div>

                                <!-- Daily Explanation Table -->
                                <div class="overflow-x-auto mt-6">
                                    <h3 class="text-base font-semibold text-gray-700 mb-2">Daily Explanation</h3>
                                    <table class="min-w-full bg-white text-sm">
                                        <thead class="bg-gray-100">
                                            <tr>
                                                <th class="text-left px-4 py-2 border-b">Day</th>
                                                <th class="text-left px-4 py-2 border-b">Explanation</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(explanation, index) in prediction[0].price_analysis.daily_explanations.slice(0, selectedDays)"
                                                :key="index">
                                                <td class="px-4 py-2 border-b font-semibold">Day {{ index + 1 }}</td>
                                                <td class="px-4 py-2 border-b text-left">
                                                    {{ extractExplanation(explanation) }}
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <!-- Summary -->
                                <div
                                    class="mt-6 bg-gray-50 border-l-4 border-yellow-400 p-4 rounded-md text-left shadow-sm">
                                    <h3 class="text-base font-semibold text-yellow-700 mb-2 flex items-center gap-2">
                                        <svg class="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd"
                                                d="M18 10c0 4.418-3.582 8-8 8s-8-3.582-8-8 3.582-8 8-8 8 3.582 8 8zm-7-4a1 1 0 00-2 0v4a1 1 0 001 1h1a1 1 0 100-2h-.5V6zm.25 9a1.25 1.25 0 11-2.5 0 1.25 1.25 0 012.5 0z"
                                                clip-rule="evenodd" />
                                        </svg>
                                        Summary
                                    </h3>
                                    <p class="text-sm text-gray-800 leading-relaxed whitespace-pre-line">
                                        {{ prediction[0].summarize }}
                                    </p>
                                </div>
                            </div>

                            <div v-else class="text-gray-500 text-sm">No prediction data available.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import ChartSwitcher from '@/components/ChartSwitcher.vue';
import Chart from '@/components/PredictionChart.vue';
import axios from 'axios';

export default {
    name: 'CoinDetailPage',
    components: { Navbar, ChartSwitcher, Chart },
    data() {
        return {
            coin: {},
            prediction: [],
            selectedDays: 2,
            loading: true,
            latestNews: [],
            coinFullNames: {
                BTC: 'Bitcoin', ETH: 'Ethereum', BNB: 'Binance Coin', SOL: 'Solana', XRP: 'XRP',
                TON: 'Toncoin', ADA: 'Cardano', DOGE: 'Dogecoin', AVAX: 'Avalanche', LINK: 'Chainlink',
                DOT: 'Polkadot', MATIC: 'Polygon', ICP: 'Internet Computer', LTC: 'Litecoin', SHIB: 'Shiba Inu',
                BCH: 'Bitcoin Cash', UNI: 'Uniswap', APT: 'Aptos', NEAR: 'NEAR Protocol', XLM: 'Stellar'
            }
        };
    },
    computed: {
        coinSymbol() {
            return this.$route.params.coin.toUpperCase();
        },
        coinSymbolWithUSDT() {
            return this.coinSymbol + 'USDT';
        },
        statCards() {
            return [
                { title: 'High Price', value: this.coin.high_price, prefix: '$' },
                { title: 'Low Price', value: this.coin.low_price, prefix: '$' },
                { title: 'Change (24h)', value: this.coin.percent_change_24h, isPercent: true },
                { title: 'Change (7d)', value: this.coin.percent_change_7d, isPercent: true },
                { title: 'Volume From', value: this.coin.volume_from, prefix: '$' },
                { title: 'Volume To', value: this.coin.volume_to, prefix: '$' },
                { title: 'Open Price', value: this.coin.open_price, prefix: '$' },
                { title: 'Close Price', value: this.coin.close_price, prefix: '$' },
            ];
        },
        chartData() {
            return this.prediction.map((entry) => ({
                date: entry.date,
                predicted_price: entry.predicted_price
            })).reverse();
        }
    },
    methods: {
        async fetchCoin() {
            try {
                const res = await axios.get(`http://localhost:8000/api/v1/coin/${this.coinSymbol}/`);
                this.coin = res.data;
            } catch (err) {
                console.error('Error fetching coin:', err);
            } finally {
                this.loading = false;
            }
        },
        async fetchPrediction() {
            try {
                const res = await axios.get(`http://localhost:8000/api/v1/prediction/${this.coinSymbolWithUSDT}/?days=${this.selectedDays}`);
                this.prediction = res.data;
            } catch (err) {
                console.error('Error fetching prediction:', err);
            }
        },
        async fetchNews() {
            try {
                const res = await axios.get('http://localhost:8000/api/v1/cryptoNewsList/');
                this.latestNews = res.data.slice(0, 10);
            } catch (err) {
                console.error('Error fetching news:', err);
            }
        },
        formatNumber(val) {
            if (!val && val !== 0) return '-';
            const num = parseFloat(val);
            if (num >= 1_000_000_000_000) return (num / 1_000_000_000_000).toFixed(2) + 'T';
            if (num >= 1_000_000_000) return (num / 1_000_000_000).toFixed(2) + 'B';
            if (num >= 1_000_000) return (num / 1_000_000).toFixed(2) + 'M';
            if (num >= 1_000) return (num / 1_000).toFixed(2) + 'K';
            return num.toFixed(2);
        },
        formatPercent(val) {
            return val ? `${val.toFixed(2)}%` : '-';
        },
        getPercentClass(val) {
            if (val > 0) return 'text-green-600 font-semibold';
            if (val < 0) return 'text-red-600 font-semibold';
            return 'text-gray-500';
        },
        extractExplanation(text) {
            const split = text.split(':');
            return split.length > 1 ? split.slice(1).join(':').trim() : text;
        },
        formatDate(dateStr) {
            const options = { year: 'numeric', month: 'short', day: 'numeric' };
            return new Date(dateStr).toLocaleDateString(undefined, options);
        }
    },
    mounted() {
        this.fetchCoin();
        this.fetchPrediction();
        this.fetchNews();
    }
};
</script>


<style scoped></style>