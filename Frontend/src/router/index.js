import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HomeView from '@/views/HomeView.vue'

const login_required = ['']
const login_not_allowed = ['SignUpView']

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    // 회원 관리
    {
      path: '/login',
      name: 'LoginView',
      component: () => import('@/views/users/LoginView.vue')
    },
    {
      path: '/login/callback',
      name: 'GoogleCallbackView',
      component: () => import('@/views/users/GoogleCallback.vue')
    },
    {
      path: '/login/kakao/callback',
      name: 'KakaoCallbackView',
      component: () => import('@/views/users/KakaoCallback.vue')
    },    
    {
      path: '/login/naver/callback',
      name: 'NaverCallback',
      component: () => import('@/views/users/NaverCallback.vue')
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: () => import('@/views/users/SignUpView.vue')
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/users/Profile.vue')
    },
    {
      path: '/subscribe/:id',
      name: 'Subscribe',
      component: () => import('@/views/users/Subscribe.vue')
    },
    //상품
    {
      path: '/products',
      name: 'Products',
      component: () => import('@/views/products/Products.vue')
    },
    {
      path: '/products/:id',
      name: 'ProductDetails',
      component: () => import('@/views/products/ProductDetails.vue')
    },
    // 상품 추천
    {
      path: '/recommendations',
      name: 'Recommendations',
      component: () => import('@/views/Recommendations.vue')
    },
    // 커뮤니티
    {
      path: '/community',
      name: 'Community',
      component: () => import('@/views/community/CommunityView.vue')
    },
    {
      path: '/community/:id',
      name: 'ArticleDetail',
      component: () => import('@/views/community/ArticleDetailView.vue')
    },
    {
      path: '/community/create',
      name: 'ArticleCreate',
      component: () => import('@/views/community/ArticleCreateView.vue')
    },
    {
      path: '/community/:id/update',  // 수정 기능
      name: 'ArticleUpdate',
      component: () => import('@/views/community/ArticleUpdateView.vue')
    },
    // EXTERNALS
    {
      path: '/externals/goods',
      name: 'Goods',
      component: () => import('@/views/externals/Goods.vue')
    },
    {
      path: '/externals/map',
      name: 'Map',
      component: () => import('@/views/externals/Map.vue')
    },
    {
      path: '/externals/search',
      name: 'Search',
      component: () => import('@/views/externals/SearchView.vue')
    },
    {
      path: '/externals/search/:videoId',
      name: 'SearchDetail',
      component: () => import('@/views/externals/SearchDetail.vue')
    },
  ],
})

// 가드 로직 수정
router.beforeEach((to, from) => {
  const accountstore = useAccountStore()

  // includes를 사용해야 정확히 체크됩니다.
  if (login_required.includes(to.name) && !accountstore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LoginView' }
  }

  if (login_not_allowed.includes(to.name) && accountstore.isLogin) {
    return { name: 'Home' }
  }
})
export default router
