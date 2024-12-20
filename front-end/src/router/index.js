import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import Login from '@/views/Login.vue';

const routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: Dashboard,
        children: [
            {
                path: 'dataupload',
                name: 'DataUpload',
                component: () => import('@/views/dashboard/DataUpload.vue')
            },
            {
                path: 'service-SA',
                name: 'SSA',
                component: () => import('@/views/dashboard/ServerShow.vue')
            }
        ]
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.VITE_BASE_URL),
    routes
});

export default router;