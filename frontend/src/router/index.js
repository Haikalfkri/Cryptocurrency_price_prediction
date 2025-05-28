import { createRouter, createWebHistory } from "vue-router";

// Auth
import LoginPage from "@/views/auth/LoginPage.vue";
import RegisterPage from "@/views/auth/RegisterPage.vue";

import CryptoPage from "@/views/all/CryptoPage.vue";
import PredictPage from "@/views/all/PredictPage.vue";

import CryptoDetailPage from "@/views/all/CryptoDetailPage.vue";
import CryptoPredictionPage from "@/views/all/CryptoPredictionPage.vue";

import CryptoNewsPage from "@/views/all/CryptoNewsPage.vue";
import CryptoInsightPage from "@/views/all/CryptoInsightPage.vue";

import UserAboutUsPage from "@/views/user/UserAboutUsPage.vue";



const routes = [
    // auth
    {
        path: "/",
        component: LoginPage,
        beforeEnter: (to, from, next) => {
            const token = localStorage.getItem('accessToken');
            const role = localStorage.getItem('role');

            if(token) {
                if (role == 'user') {
                    next('/cryptoPage');
                } else if (role == 'admin') {
                    next('/cryptoPage');
                } else {
                    next('/');
                }
            } else {
                next();
            }
        }
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
    },

    {
        path: "/CryptoNewsPage",
        name: "CryptoNewsPage",
        component: CryptoNewsPage,
        meta: { requiresAuth: true }
    },
    {
      path: "/CryptoInsight",
      name: "CryptoInsight",
      component: CryptoInsightPage,
      meta: { requiresAuth: true }  
    },
    {
        path: "/CryptoDetailPage",
        name: "CryptoDetailpage",
        component: CryptoDetailPage,
        meta: { requiresAuth: true },
    },

    {
        path: "/CryptoPredictionPage",
        name: "CryptoPredictionPage",
        component: CryptoPredictionPage,
        meta: { requiresAuth: true },
    },
    {
        path: "/cryptoPage",
        name: "CryptoPage",
        component: CryptoPage,
        meta: { requiresAuth: true },
    },
    {
        path: "/predictPage",
        name: "PredictPage",
        component: PredictPage,
        meta: { requiresAuth: true }
    },

    // User
    {
        path: "/UserAboutUsPage",
        name: "UserAboutUsPage",
        component: UserAboutUsPage,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// navigation guard to check the role
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("accessToken");
    const role = localStorage.getItem("role");

    if (to.meta.requiresAuth) {
        if(!token) {
            next("/login"); // redirect to login if not authenticated
        } else if (to.meta.role && to.meta.role !== role) {
            next("/login"); // redirect to login if role do not match
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;