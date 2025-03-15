<template>
    <div class="flex flex-col items-center justify-center relative">
        <!-- Back Button (Aligned with First Row of Card) -->
        <button class="absolute left-10 top-0 mt-20 p-2">
            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                fill="none" viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 5H1m0 0 4 4M1 5l4-4" />
            </svg>
        </button>

        <!-- Centered Card -->
        <div class="flex justify-center items-center mt-6">
            <CardCryptoData />
        </div>

        <!-- Description Section -->
        <div class="w-[800px] mt-10 text-left">
            <h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">Description</h5>
            <p class="text-gray-700 dark:text-gray-400">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Aspernatur est, debitis unde possimus explicabo
                et eveniet, ratione quia quisquam tempore dolore! Iste praesentium consectetur eius modi reiciendis, ut
                error delectus! Lorem ipsum dolor sit amet consectetur adipisicing elit. Sequi magni in eum iure id itaque consectetur quasi quas accusamus sint voluptates ut ipsam voluptatem et incidunt inventore, alias atque ducimus! Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur fugiat nisi vero commodi ipsam natus, nobis, dolor recusandae explicabo optio soluta nemo praesentium numquam sint deleniti necessitatibus, consequuntur aperiam fuga.
            </p>
        </div>
    </div>
</template>

<script>
import CardCryptoData from '@/components/CardCryptoData.vue';

export default {
    name: "CryptoDetailPage",
    components: {
        CardCryptoData,
    }
}
</script>
