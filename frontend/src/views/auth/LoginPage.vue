<template>
    <div>
        <!-- Modal for successful login -->
        <transition name="fade">
            <div v-if="showPopup" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
                <div class="bg-white p-8 rounded-lg shadow-lg max-w-lg">
                    <div class="flex items-center justify-center mb-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    <h2 class="text-center text-2xl font-semibold text-gray-800">Login Successful!</h2>
                    <p class="text-center text-gray-500 mt-2">Redirecting to crypto page</p>
                </div>
            </div>
        </transition>

        <div class="flex flex-col items-center justify-center px-6 py-6 mx-auto md:h-screen lg:py-0">
            <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0">
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                        Sign In
                    </h1>
                    <form @submit.prevent="Login" class="space-y-4 md:space-y-6">
                        <div>
                            <label for="email" class="block mb-2 text-sm text-left font-medium">Email address</label>
                            <input v-model="email" type="email" name="email" id="email"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="name@example.com" required>
                        </div>
                        <div>
                            <label for="password" class="block mb-2 text-sm text-left font-medium">Password</label>
                            <input v-model="password" type="password" name="password" id="password" placeholder="••••••••"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                required>
                        </div>
                        <p class="text-sm text-left font-light text-gray-500 dark:text-gray-400">
                            Already have an account? <router-link to="/register"
                                class="font-medium text-blue-600 hover:underline dark:text-primary-500">Sign Up</router-link>
                        </p>
                        <button type="submit" :disabled="loading"
                            class="w-full text-white bg-blue-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                            <span v-if="loading">Loading...</span>
                            <span v-else>Sign In</span>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

export default {
    name: "LoginPage",
    data() {
        return {
            email: "",
            password: "",
            showPopup: false,  // state for controlling popup visibility
            loading: false, // state for controlling button loading status
        }
    },
    methods: {
        async Login() {
            this.loading = true; // Start loading state for button
            try {
                const response = await axios.post("https://6f33-103-150-218-251.ngrok-free.app/api/v1/login", {
                    email: this.email,
                    password: this.password,
                });

                const token = response.data.access;
                const role = response.data.role;
                const username = response.data.username;
                const email = response.data.email;

                // Store token and user details in localStorage
                localStorage.setItem('accessToken', token);
                localStorage.setItem('role', role);
                localStorage.setItem('username', username);
                localStorage.setItem('email', email);

                // Show the success popup
                this.showPopup = true;

                // Hide the popup after 2 seconds and redirect to the next page
                setTimeout(() => {
                    this.showPopup = false;
                    this.$router.push("/cryptoPage");
                }, 2000);
            } catch (error) {
                console.log("Login failed. Check your credentials");
            } finally {
                this.loading = false; // End loading state for button
            }
        }
    }
}
</script>

<style scoped>
/* Modal Style */
.fixed {
    position: fixed;
}
.bg-gray-900 {
    background-color: rgba(0, 0, 0, 0.7);
}
.bg-opacity-50 {
    opacity: 1;
}

/* Smooth transition for modal */
.fade-enter-active, .fade-leave-active {
    transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0;
}
</style>
