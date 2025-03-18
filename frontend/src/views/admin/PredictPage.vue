<template>
    <Navbar class="fixed top-0 left-0 w-full bg-white shadow-md z-50" />

    <div class="flex justify-center items-center min-h-screen">
        <div class="w-full max-w-2xl">
            <PredictButton class="w-full text-sm rounded-2xl" />
        </div>
    </div>

</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import PredictButton from '@/components/PredictButton.vue';

export default {    
    name: "PredictPage",
    components: {
        Navbar,
        PredictButton,
    }
}
</script>