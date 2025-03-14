<template>
    <Navbar />

    <div>
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