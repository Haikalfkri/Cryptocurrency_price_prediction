<template>
    <form class="flex items-center max-w-2xl mx-auto mt-10 space-x-2">
        <label for="crypto-search" class="sr-only">Search</label>

        <!-- Search Input -->
        <div class="relative w-full">
            <input type="text" id="crypto-search"
                class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 
            dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Search Crypto e.g BTC-USD, ETH-USD" required />
        </div>

        <!-- Dropdown -->
        <select id="days-filter"
            class="border border-gray-300 text-gray-900 text-sm rounded-2xl focus:ring-blue-500 focus:border-blue-500 
        p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option value="7">7 Days</option>
            <option value="14">14 Days</option>
        </select>

        <!-- Search Button -->
        <button type="submit"
            class="inline-flex items-center py-2.5 px-3 text-sm font-medium text-white bg-blue-700 rounded-2xl border border-blue-700 
        hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>
            Search
        </button>
    </form>

</template>

<script>

export default {
    name: "PredictButton",
    data() {
        return {
        }
    },
    methods: {
    }
}
</script>