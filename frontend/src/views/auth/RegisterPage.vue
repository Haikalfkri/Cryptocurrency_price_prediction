<template>
    <div>
        <div class="flex flex-col items-center justify-center px-6 py-6 mx-auto md:h-screen lg:py-0">
            <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0">
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                        Sign Up
                    </h1>
                    <form @submit.prevent="Register" class="space-y-4 md:space-y-6">
                        <div>
                            <label for="username" class="block mb-2 text-sm text-left font-medium">Username</label>
                            <input v-model="username" type="text" name="username" id="username"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Username" required>
                        </div>
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
                        <div>
                            <label for="confirm-password" class="block mb-2 text-sm text-left font-medium">Confirm password</label>
                            <input v-model="password2" type="password" name="confirm-password" id="confirm-password"
                                placeholder="••••••••"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                required>
                        </div>
                        <p class="text-sm text-left font-light text-gray-500 dark:text-gray-400">
                            Already have an account? <router-link to="/login"
                                class="font-medium text-blue-600 hover:underline dark:text-primary-500">Sign In</router-link>
                        </p>
                        <button type="submit" :disabled="loading"
                            class="w-full text-white bg-blue-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:focus:ring-primary-800">
                            <span v-if="loading">Loading...</span>
                            <span v-else>Sign Up</span>
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Success Modal with smooth transition and larger size -->
        <transition name="fade">
            <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
                <div class="bg-white p-8 rounded-lg shadow-lg max-w-lg">
                    <div class="flex items-center justify-center mb-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    <h2 class="text-center text-2xl font-semibold text-gray-800">Registration Successful!</h2>
                    <p class="text-center text-gray-500 mt-2">You can now log in to your account.</p>
                </div>
            </div>
        </transition>

        <!-- Error Modal with smooth transition and larger size -->
        <transition name="fade">
            <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
                <div class="bg-white p-8 rounded-lg shadow-lg max-w-lg">
                    <div class="flex items-center justify-center mb-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </div>
                    <h2 class="text-center text-2xl font-semibold text-gray-800">Error!</h2>
                    <p class="text-center text-red-500 mt-2">{{ errorMessage }}</p>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

export default {
    name: "RegisterPage",
    data() {
        return {
            username: "",
            email: "",
            password: "",
            password2: "",
            loading: false,
            showModal: false, // For the success modal
            showErrorModal: false, // For the error modal
            errorMessage: "", // To display error message
        }
    },
    methods: {
        async Register() {
            if (this.password !== this.password2) {
                console.log("Passwords do not match!");
                return;
            }
            this.loading = true; // Start loading
            try {
                await axios.post("https://6f33-103-150-218-251.ngrok-free.app/api/v1/register", {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    password2: this.password2,
                });
                this.showModal = true; // Show success modal
                setTimeout(() => {
                    this.$router.push("/login");
                }, 2000); // Redirect to login after 2 seconds
            } catch (error) {
                if (error.response && error.response.data) {
                    // If there's an error, display the error message
                    this.errorMessage = error.response.data.email || "Registration failed.";
                    this.showErrorModal = true;
                    setTimeout(() => {
                        this.showErrorModal = false;
                    }, 2000); // Hide the error modal after 2 seconds
                } else {
                    console.log("Registration failed");
                }
            } finally {
                this.loading = false; // End loading
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
