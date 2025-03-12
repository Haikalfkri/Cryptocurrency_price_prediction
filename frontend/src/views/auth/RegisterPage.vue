<template>
    <div>
        <div class="flex flex-col items-center justify-center px-6 py-6 mx-auto md:h-screen lg:py-0">
            <div
                class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <h1
                        class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                        Sign Up
                    </h1>
                    <form @submit.prevent="Register" class="space-y-4 md:space-y-6">
                        <div>
                            <label for="username" class="block mb-2 text-sm text-left font-medium">Username</label>
                            <input v-model="username" type="text" name="username" id="username"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Username" required>
                        </div>
                        <div>
                            <label for="email" class="block mb-2 text-sm text-left font-medium">Email address</label>
                            <input v-model="email" type="email" name="email" id="email"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="name@example.com" required>
                        </div>
                        <div>
                            <label for="password"
                                class="block mb-2 text-sm text-left font-medium">Password</label>
                            <input v-model="password" type="password" name="password" id="password" placeholder="••••••••"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                required>
                        </div>
                        <div>
                            <label for="confirm-password"
                                class="block mb-2 text-sm text-left font-medium">Confirm
                                password</label>
                            <input v-model="password2" type="password" name="confirm-password" id="confirm-password"
                                placeholder="••••••••"
                                class="border border-gray-[CFD5E3] text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                required>
                        </div>
                        <p class="text-sm text-left font-light text-gray-500 dark:text-gray-400">
                            Already have an account? <router-link to="/login"
                                class="font-medium text-blue-600 hover:underline dark:text-primary-500">Sign In</router-link>
                        </p>
                        <button type="submit"
                            class="w-full text-white bg-blue-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:focus:ring-primary-800">Sign Up</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "RegisterPage",
    data() {
        return {
            username: "",
            email: "",
            password: "",
            password2: "",
        }
    },
    methods: {
        async Register() {
            if (this.password != this.password2) {
                console.log("Password do not match!");
                return;
            }
            try {
                await axios.post("http://127.0.0.1:8000/api/v1/register", {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    password2: this.password2,
                });
                this.$router.push("/login");
            } catch (error) {
                console.log("Registration failed");
            }
        }
    }
}
</script>