<template>
    <div class="mt-6">
        <div class="w-[800px] grid grid-cols-4 gap-4">
            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">Price</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    ${{ formatCurrency(cryptoData?.Price) }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 dark:text-white">Market Cap (USD)</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    ${{ formatNumber(cryptoData?.MarketCap) }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 dark:text-white">24h Volume (USD)</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    ${{ formatNumber(cryptoData?.Volume24h) }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 dark:text-white">FDV (USD)</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    ${{ formatNumber(cryptoData?.FDV) }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 dark:text-white">Total Supply</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    {{ formatNumber(cryptoData?.TotalSupply) }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 dark:text-white">Max Supply</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    {{ cryptoData?.MaxSupply ? formatNumber(cryptoData?.MaxSupply) : 'Null' }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 dark:text-white">Circulating Supply</h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    {{ formatNumber(cryptoData?.CirculatingSupply) }}
                </p>
            </div>

            <div
                class="block w-[200px] p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-sm font-bold tracking-tight text-gray-900 dark:text-white">Market Cap Change (24h)
                </h5>
                <p class="font-normal text-gray-700 dark:text-gray-400">
                    {{ formatPercentage(cryptoData?.MarketCapChangePercentage) }}
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CardCryptoData",
    props: {
        cryptoData: Object,
    },
    methods: {
        formatCurrency(value) {
            return value ? Number(value).toFixed(2) : '0.00';
        },
        formatNumber(value) {
            return value ? Number(value).toLocaleString() : '0';
        },
        formatPercentage(value) {
            return value ? Number(value).toFixed(2) + '%' : '0.00%';
        }
    }
}
</script>