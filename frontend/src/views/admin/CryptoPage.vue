<template>
    <Navbar class="fixed top-0 left-0 w-full bg-white shadow-md z-50" />

    <div class="mt-[100px]">
        <CryptoSearchButton />
    </div>
</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import CryptoSearchButton from '@/components/CryptoSearchButton.vue';

export default {
    name: "AdminCryptoPage",
    components: {
        Navbar,
        CryptoSearchButton,
    }
}
</script>