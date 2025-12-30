import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'
import Login from '../views/Login.vue'
import ThreeDPage from "@/views/ThreeDPage.vue";

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Home',
    component: App,
    meta: { requiresAuth: true } // 需要登录才能访问
  },
  {
    path: "/3d", 
    name: "ThreeD",
    component: ThreeDPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录跳转到登录页
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  if (to.meta.requiresAuth && !token) {
    next("/login")
  } else {
    next()
  }
})

export default router