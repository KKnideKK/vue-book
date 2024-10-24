import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('./components/Home.vue') // 加载登录组件
  },
  {
    path: '/get_itid',
    component: () => import('./components/get_itid.vue') // 验证码登录组件
  },
  {
    path: '/get_admin',
    component: () => import('./components/get_admin.vue') // 加载管理员注册组件
  },
  {
    path: '/get_user',
    component: () => import('./components/get_user.vue') // 加载用户注册组件
  },
  {
    path: '/Admin',
    component: () => import('./components/Admin.vue')// 加载管理员主页组件
  },
  {
    path: '/Book',
    component: () => import('./assets/Book.vue')// 加载图书管理组件
  },
  {
    path: '/admin_data',
    component: () => import('./assets/admin_data.vue')// 加载图书管理组件
  },
  {
    path: '/book_data',
    component: () => import('./assets/book_data.vue')// 加载图书详情
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router