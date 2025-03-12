import { createRouter, createWebHistory } from "vue-router";

// Auth
import LoginPage from "@/views/auth/LoginPage.vue";
import RegisterPage from "@/views/auth/RegisterPage.vue";

const routes = [
    {
        path: "/",
        component: LoginPage
    },
    {
        path: "/login",
        name: "LoginPage",
        component: LoginPage
    },
    {
        path: "/register",
        name: "RegisterPage",
        component: RegisterPage
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;