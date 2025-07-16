<template>
    <nav class="bg-white border-gray-200 shadow-md">
        <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-3">
            <!-- Left Section: Title and Links -->
            <div class="flex items-center space-x-6">
                <a href="#" class="flex items-center space-x-3">
                    <span class="hidden md:inline text-xl font-bold">Crypeek</span>
                </a>
                <ul class="hidden md:flex space-x-6 text-md font-semibold">
                    <li><router-link to="/CryptoNewsPage" class="text-gray-900 hover:text-blue-700">News</router-link>
                    </li>
                    <li><router-link to="/CryptoInsight"
                            class="text-gray-900 hover:text-blue-700">Insights</router-link>
                    </li>
                    <li><router-link to="/coinPage" class="text-gray-900 hover:text-blue-700">Coins</router-link>
                    </li>
                    <li v-if="role === 'user'"><router-link to="/UserAboutUsPage"
                            class="text-gray-900 hover:text-blue-700">About Us</router-link></li>

                    <li v-if="role === 'admin'"><a href="#" class="text-gray-900 hover:text-blue-700">User
                            Management</a></li>
                    <li v-if="role === 'admin'"><a href="#" class="text-gray-900 hover:text-blue-700">User Feedbacks</a>
                    </li>
                </ul>
            </div>

            <!-- Right Section: Profile and Mobile Menu Button -->
            <div class="flex items-center space-x-4">
                <!-- Profile -->
                <div class="relative">
                    <button @click="toggleDropdown"
                        class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-100 hover:ring-2 hover:ring-indigo-500 transition">
                        <img class="w-10 h-10 rounded-full object-cover"
                            src="https://img.freepik.com/free-vector/smiling-young-man-illustration_1308-174401.jpg"
                            alt="User Avatar">
                    </button>

                    <!-- Dropdown Menu -->
                    <transition name="fade">
                        <div v-show="isDropdownOpen"
                            class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg ring-1 ring-black/5 z-50">
                            <div class="px-4 py-3 border-b border-gray-100">
                                <p class="text-sm font-medium text-gray-900">{{ username }}</p>
                                <p class="text-sm text-gray-500 truncate">{{ email }}</p>
                            </div>
                            <ul class="py-2">
                                <li>
                                    <a @click.prevent="handleLogout" href="#"
                                        class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition rounded-b-lg">
                                        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor"
                                            stroke-width="2" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1m0-9V6" />
                                        </svg>
                                        Logout
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </transition>
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
                <li><router-link to="/CryptoNewsPage" class="block text-gray-900 hover:text-blue-700">News</router-link>
                </li>
                <li><router-link to="/CryptoInsight"
                        class="block text-gray-900 hover:text-blue-700">Insights</router-link>
                </li>
                <li><router-link to="/coinPage" class="block text-gray-900 hover:text-blue-700">Coins</router-link></li>
                <li v-if="role === 'user'"><router-link to="/UserAboutUsPage"
                        class="block text-gray-900 hover:text-blue-700">About Us</router-link></li>

                <li v-if="role === 'admin'"><a href="#" class="block text-gray-900 hover:text-blue-700">User
                        Management</a></li>
                <li v-if="role === 'admin'"><a href="#" class="block text-gray-900 hover:text-blue-700">Feedbacks</a>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

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
                await axios.post("http://127.0.0.1:8000/api/v1/logout", {}, {
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
                localStorage.removeItem("coin");
                localStorage.removeItem("predictionResponse");

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
};
</script>

<style>
nav ul li a {
    transition: color 0.3s ease;
}
</style>