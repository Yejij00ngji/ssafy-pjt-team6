import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const login_required = ['']
const login_not_allowed = ['SignUpView']

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/login',
      name: 'LoginView',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: () => import('@/views/SignUpView.vue')
    },
    {
      path: '/community',
      name: 'Community',
      component: () => import('@/views/Community.vue')
    },
    {
      path: '/products',
      name: 'Products',
      component: () => import('@/views/Products.vue')
    },
    {
      path: '/products/:id',
      name: 'ProductDetails',
      component: () => import('@/views/ProductDetails.vue')
    },
    {
      path: '/goods',
      name: 'Goods',
      component: () => import('@/views/Goods.vue')
    },
    {
      path: '/externals/map',
      name: 'Map',
      component: () => import('@/views/Map.vue')
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/Profile.vue')
    },
    {
      path: '/recommendations',
      name: 'Recommendations',
      component: () => import('@/views/Recommendations.vue')
    },
    {
      path: '/externals/search',
      name: 'Search',
      component: () => import('@/views/Search.vue')
    },
    {
      path: '/externals/search/:videoId',
      name: 'SearchDetail',
      component: () => import('@/views/SearchDetail.vue')
    },
  ],
})

router.beforeEach((to,from) => {
  const accountstore = useAccountStore()

  if (to.name in login_required && !accountstore.isLogin){
    window.alert('로그인이 필요합니다.')
    return {name: 'LoginView'}
  }

  if (to.name in login_not_allowed && accountstore.isLogin){
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'Home' }
  }
})

export default router
