import { createRouter, createWebHistory } from "vue-router";

// Auth
import LoginPage from "@/views/auth/LoginPage.vue";
import RegisterPage from "@/views/auth/RegisterPage.vue";

import AdminCryptoPage from "@/views/admin/CryptoPage.vue";

import UserCryptoPage from "@/views/user/CryptoPage.vue";

import CryptoDetailPage from "@/views/admin/CryptoDetailPage.vue";

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
                    next('/user/cryptoPage');
                } else if (role == 'admin') {
                    next('/admin/cryptoPage');
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

    // admin
    {
        path: "/admin/cryptoPage",
        name: "adminCryptoPage",
        component: AdminCryptoPage,
        meta: { requiresAuth: true, role: "admin" },
    },

    // user 
    {
        path: "/user/cryptoPage",
        name: "userCryptoPage",
        component: UserCryptoPage,
        meta: { requiresAuth: true, role: "user" },
    },

    {
        path: "/CryptoDetailPage",
        name: "CryptoDetailpage",
        component: CryptoDetailPage,
    },
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