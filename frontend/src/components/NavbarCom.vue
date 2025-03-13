<template>
    <nav class="bg-white border-gray-200 shadow-md dark:bg-gray-900">
        <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-3">
            <div class="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                <button type="button" @click="toggleDropdown"
                    class="flex text-sm bg-gray-800 rounded-full md:me-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                    id="user-menu-button">
                    <span class="sr-only">Open user menu</span>
                    <img class="w-8 h-8 rounded-full"
                        src="https://img.freepik.com/free-vector/smiling-young-man-illustration_1308-174401.jpg?semt=ais_hybrid"
                        alt="user photo">
                </button>

                <!-- Dropdown menu -->
                <div v-show="isDropdownOpen"
                    class="z-50 absolute right-0 mt-[160px] w-48 bg-white divide-y divide-gray-100 rounded-lg shadow-md dark:bg-gray-700 dark:divide-gray-600"
                    id="user-dropdown">
                    <div class="px-4 py-3">
                        <span class="block text-sm text-gray-900 dark:text-white">{{ username }}</span>
                        <span class="block text-sm text-gray-500 truncate dark:text-gray-400">{{ email }}</span>
                    </div>
                    <ul class="py-2">
                        <li>
                            <a @click.prevent="handleLogout" href="#"
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-user">
                <a href="https://flowbite.com/" class="flex items-center mr-5 space-x-3 rtl:space-x-reverse">
                    <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Flowbite Logo" />
                    <span class="self-center text-md font-semibold whitespace-nowrap dark:text-white">Cryptocurrency
                        Price Prediction</span>
                </a>
                <ul
                    class="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
                    <li><a href="#"
                            class="block py-2 px-3 text-white text-sm bg-blue-700 rounded-sm md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
                            aria-current="page">Home</a></li>
                    <li><a href="#"
                            class="block py-2 px-3 text-gray-900 text-sm rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Crypto</a>
                    </li>
                    <li><a href="#"
                            class="block py-2 px-3 text-gray-900 text-sm rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Predict</a>
                    </li>
                    <li><a href="#"
                            class="block py-2 px-3 text-gray-900 text-sm rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">User
                            Management</a></li>
                    <li><a href="#"
                            class="block py-2 px-3 text-gray-900 text-sm rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Feedbacks</a>
                    </li>
                </ul>
            </div>
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
            username: localStorage.getItem("username"),
            email: localStorage.getItem("email"),
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
                    window.location.reload();  // 🔥 Ensures full refresh and reactivity
                });
            } catch (error) {
                console.log("Logout failed")
            }
        },
        // dropdown button
        toggleDropdown() {
            this.isDropdownOpen = !this.isDropdownOpen;
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
    }
};
</script>
