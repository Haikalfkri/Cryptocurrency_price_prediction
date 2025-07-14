<template>
    <div>
        <Navbar class="top-0 left-0 w-full bg-white shadow-md z-50 mb-6" />
        <div class="min-h-screen bg-[#fafafa] px-4 py-6 overflow-hidden">
            <div v-if="loading" class="text-center py-10 text-sm text-gray-500">
                Loading coin data...
            </div>

            <div v-else class="flex flex-col space-y-6 h-full">
                <!-- Top Row -->
                <div
                    class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 flex-shrink-0">
                    <!-- Coin Identity -->
                    <div class="flex items-center gap-4">
                        <img :src="coin.image_url" alt="coin" class="w-16 h-16 sm:w-20 sm:h-20 object-contain rounded-lg" />
                        <div>
                            <h1 class="text-2xl sm:text-3xl font-bold leading-tight break-words">{{ coin.coin }}</h1>
                            <div v-if="coin.coin in coinFullNames" class="text-base sm:text-lg text-gray-500">
                                {{ coinFullNames[coin.coin] }}
                            </div>
                        </div>
                    </div>

                    <!-- Coin Stats -->
                    <div class="flex flex-wrap justify-center md:justify-between gap-4 w-full md:w-auto">
                        <!-- Price -->
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

                        <!-- Market Cap -->
                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">Market Cap</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                ${{ formatNumber(coin.market_cap) }}
                            </div>
                        </div>

                        <!-- 24H Volume -->
                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">24H Volume</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                ${{ formatNumber(coin.volume_to) }}
                            </div>
                        </div>

                        <!-- Circulating Supply -->
                        <div class="w-[130px] text-left">
                            <div class="text-sm text-gray-500 mb-1">Circ Supply</div>
                            <div class="text-xl sm:text-2xl font-bold text-gray-900 leading-snug tracking-wide">
                                {{ formatNumber(coin.circulating_supply) }}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Main Content -->
                <div class="flex flex-col md:flex-row flex-1 gap-6 overflow-hidden">
                    <!-- Left Column -->
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
                    </div>

                    <!-- Right Scrollable Column -->
                    <div class="flex-1 overflow-y-auto pr-1 md:pr-2 space-y-6 min-w-0">
                        <div class="bg-white p-4 sm:p-6 rounded-2xl shadow">
                            <ChartSwitcher :coin="coinSymbol" />
                        </div>
                        <div
                            class="bg-white p-4 sm:p-6 rounded-2xl shadow text-sm text-gray-800 leading-relaxed text-left">
                            <h2 class="text-lg font-semibold mb-3">Description</h2>
                            <p>{{ coin.description || 'No description available.' }}</p>
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
import axios from 'axios';

export default {
    name: 'CoinDetailPage',
    components: { Navbar, ChartSwitcher },
    data() {
        return {
            coin: {},
            loading: true,
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
        }
    },
    mounted() {
        this.fetchCoin();
    }
};
</script>

<style scoped></style>
