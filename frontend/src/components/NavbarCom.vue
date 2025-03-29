<template>
    <nav class="bg-white border-gray-200 shadow-md">
        <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
            <!-- Left Section: Title and Links -->
            <div class="flex items-center space-x-6">
                <a href="#" class="flex items-center space-x-3">
                    <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Logo" />
                    <span class="hidden md:inline text-lg font-semibold">Cryptocurrency Price
                        Prediction</span>
                </a>
                <ul class="hidden md:flex space-x-6 text-sm font-medium">
                    <li><router-link :to="cryptoPageRoute" class="text-gray-900 hover:text-blue-700">Crypto</router-link></li>
                    <li><router-link to="/predictPage" class="text-gray-900 hover:text-blue-700">Predict</router-link></li>
                    <li v-if="role === 'admin'"><a href="#"
                            class="text-gray-900 hover:text-blue-700">User Management</a></li>
                    <li v-if="role === 'admin'"><a href="#"
                            class="text-gray-900 hover:text-blue-700">Feedbacks</a></li>
                </ul>
            </div>

            <!-- Right Section: Profile and Mobile Menu Button -->
            <div class="flex items-center space-x-4">
                <!-- Profile -->
                <div class="relative">
                    <button @click="toggleDropdown"
                        class="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600">
                        <span class="sr-only">Open user menu</span>
                        <img class="w-8 h-8 rounded-full"
                            src="https://img.freepik.com/free-vector/smiling-young-man-illustration_1308-174401.jpg"
                            alt="user photo">
                    </button>
                    <div v-show="isDropdownOpen"
                        class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-md">
                        <div class="px-4 py-3">
                            <span class="block text-sm text-gray-900">{{ username }}</span>
                            <span class="block text-sm text-gray-900">{{ email }}</span>
                        </div>
                        <ul class="py-2">
                            <li>
                                <a @click.prevent="handleLogout" href="#"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600">Logout</a>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <button @click="toggleMobileMenu" class="md:hidden p-2 text-gray-500 dark:text-gray-400">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 6h16M4 12h16m-7 6h7">
                        </path>
                    </svg>
                </button>
            </div>

        </div>

        <!-- Mobile Menu -->
        <div v-show="isMobileMenuOpen" class="md:hidden px-4 pb-4">
            <ul class="space-y-2 text-sm font-medium">
                <li><router-link to="/cryptoPage"
                        class="block text-gray-900 hover:text-blue-700">Crypto</router-link></li>
                <li><router-link to="/predictPage"
                        class="block text-gray-900 hover:text-blue-700">Predict</router-link></li>
                <li v-if="role === 'admin'"><a href="#"
                        class="block text-gray-900 hover:text-blue-700">User Management</a></li>
                <li v-if="role === 'admin'"><a href="#"
                        class="block text-gray-900 hover:text-blue-700">Feedbacks</a></li>
            </ul>
        </div>
    </nav>
</template>

<script>
import axios from 'axios';

export default {
    name: "NavbarComponent",
    data() {
        return {
            isDropdownOpen: false,
            isMobileMenuOpen: false,
            username: localStorage.getItem("username"),
            email: localStorage.getItem("email"),
            role: localStorage.getItem("role"),
        };
    },
    methods: {
        // handle logout
        async handleLogout() {
            const token = localStorage.getItem("accessToken");

            try {
                await axios.post("http://localhost:8000/api/v1/logout", {}, {
                    withCredentials: true,
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                // remove access token & role from localstorage
                localStorage.removeItem("accessToken");
                localStorage.removeItem("role");
                localStorage.removeItem("username");
                localStorage.removeItem("email");

                // redirect to login page
                this.$router.push("/login").then(() => {
                    window.location.reload();  // Ensures full refresh and reactivity
                });
            } catch (error) {
                console.log("Logout failed")
            }
        },
        // dropdown button
        toggleDropdown() {
            this.isDropdownOpen = !this.isDropdownOpen;
        },
        toggleMobileMenu() {
            this.isMobileMenuOpen = !this.isMobileMenuOpen;
        },
        closeDropdown(e) {
            // Close dropdown when clicking outside
            if (!this.$el.contains(e.target)) {
                this.isDropdownOpen = false;
            }
        },
    },
    mounted() {
        // Add click event listener to close dropdown when clicking outside
        document.addEventListener('click', this.closeDropdown);
    },
    beforeUnmount() {
        // Clean up event listener
        document.removeEventListener('click', this.closeDropdown);
    },
    computed: {
        cryptoPageRoute() {
            const userRole = localStorage.getItem('role'); // Assuming role is stored in Vuex
            return userRole === 'admin' ? '/admin/cryptoPage' : '/user/cryptoPage';
        }
    }
};
</script>

<style>
nav ul li a {
    transition: color 0.3s ease;
}
</style>