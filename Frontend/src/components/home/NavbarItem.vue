<template>
  <nav class="toss-nav">
    <div class="nav-container">
      
      <div class="nav-left">
        <RouterLink :to="{name:'Home'}" class="logo">
          Money:Bee
        </RouterLink>

        <div class="nav-menu hidden md:flex">
          <RouterLink :to="{name:'Recommendations'}" class="nav-link">맞춤추천</RouterLink>
          <RouterLink :to="{name:'Products'}" class="nav-link">금융상품</RouterLink>
          <RouterLink :to="{name:'Community'}" class="nav-link">커뮤니티</RouterLink>
          <div 
            class="nav-item-dropdown"
            @mouseenter="isDropdownOpen = true"
            @mouseleave="isDropdownOpen = false"
          >
            <p class="nav-link flex items-center gap-1">
              서비스
              <span class="material-symbols-outlined text-[18px] transition-transform" :class="{'rotate-180': isDropdownOpen}">
                expand_more
              </span>
            </p>

            <transition name="fade">
              <div v-if="isDropdownOpen" class="dropdown-panel">
                <RouterLink :to="{name: 'Map'}" class="dropdown-item">
                  <span class="material-symbols-outlined">map</span>
                  <div>
                    <p class="item-title">은행 찾기</p>
                    <p class="item-desc">내 주변 가까운 은행 위치 확인</p>
                  </div>
                </RouterLink>
                <RouterLink :to="{name: 'Goods'}" class="dropdown-item">
                  <span class="material-symbols-outlined">payments</span>
                  <div>
                    <p class="item-title">금/은 시세</p>
                    <p class="item-desc">실시간 귀금속 시세 정보</p>
                  </div>
                </RouterLink>
                <RouterLink :to="{name:'Search'}" class="dropdown-item">
                  <span class="material-symbols-outlined">play_circle</span>
                  <div>
                    <p class="item-title">금융 영상</p>
                    <p class="item-desc">유튜브 금융 트렌드 검색</p>
                  </div>
                </RouterLink>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <div class="nav-right">
        <template v-if="!accountstore.isLogin">
          <RouterLink :to="{name:'LoginView'}" class="login-link">로그인</RouterLink>
          <RouterLink :to="{name:'SignUpView'}" class="btn-signup">회원가입</RouterLink>
        </template>
        
        <template v-else>
          <RouterLink :to="{name:'Profile'}" class="login-link">내 프로필</RouterLink>
          <button @click.prevent="logOut" class="btn-logout">로그아웃</button>
        </template>
      </div>
    </div>
  </nav>
  <div class="nav-spacer"></div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { ref } from 'vue'

const isDropdownOpen = ref(false)
const accountstore = useAccountStore()
const logOut = () => { accountstore.logOut() }
</script>

<style scoped>
/* 1. 전체 바 설정 */
.toss-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #f2f4f6;
  height: 64px;
  display: flex;
  align-items: center;
}

/* 2. 컨테이너 (가로 정렬 핵심) */
.nav-container {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

/* 3. 좌측 그룹 */
.nav-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.logo {
  text-decoration: none;
  font-size: 22px;
  font-weight: 700;
  color: #333d4b;
}

.nav-menu {
  display: flex;
  gap: 30px;
  list-style: none;
}

/* 4. 링크 스타일 */
.nav-link {
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  color: #4e5968;
  transition: color 0.2s;
}

.nav-link:hover, .router-link-active {
  color: #333d4b;
  font-weight: 600;
}

/* 5. 우측 그룹 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.login-link {
  text-decoration: none;
  font-size: 14px;
  color: #4e5968;
  padding: 0 10px;
}

.btn-signup {
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  color: white !important;
  background-color: #3182f6;
  padding: 8px 16px;
  border-radius: 8px;
  display: inline-block;
}

.btn-logout {
  border: none;
  background: none;
  font-size: 14px;
  color: #f04452;
  cursor: pointer;
}

.nav-spacer {
  height: 64px;
}

.nav-item-dropdown {
  position: relative;
  height: 64px;
  display: flex;
  align-items: center;
}

.dropdown-panel {
  position: absolute;
  top: 60px;
  left: 50%;
  transform: translateX(-50%);
  width: 260px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  padding: 12px;
  border: 1px solid #f2f4f6;
  z-index: 1001;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background-color: #f9fafb;
}

.dropdown-item .material-symbols-outlined {
  color: #4e5968;
  font-size: 24px;
}

.item-title {
  font-size: 15px;
  font-weight: 600;
  color: #333d4b;
  margin: 0;
}

.item-desc {
  font-size: 12px;
  color: #6b7684;
  margin: 0;
}

/* 애니메이션 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-10px);
}
</style>