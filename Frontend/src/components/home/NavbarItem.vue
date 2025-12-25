<template>
  <nav class="toss-nav">
    <div class="nav-container">
      
      <div class="nav-group-left">
        <img src="@/assets/icons/honeycomb.png" class="w-[30px] h-[30px] object-cover" alt="Logo" />
        <RouterLink :to="{name:'Home'}" class="logo no-wrap">Money:B</RouterLink>
      </div>

      <div class="nav-group-center lg-only">
        <RouterLink :to="{name:'Recommendations'}" class="nav-link no-wrap">맞춤추천</RouterLink>
        <RouterLink :to="{name:'Products'}" class="nav-link no-wrap">금융상품</RouterLink>
        <RouterLink :to="{name:'Community'}" class="nav-link no-wrap">커뮤니티</RouterLink>
        
        <div class="nav-item-dropdown" @mouseenter="isDropdownOpen = true" @mouseleave="isDropdownOpen = false">
          <div class="nav-link no-wrap dropdown-trigger">
            서비스
            <span class="material-symbols-outlined dropdown-arrow" :class="{'rotate-180': isDropdownOpen}">expand_more</span>
          </div>

          <transition name="fade">
            <div v-if="isDropdownOpen" class="dropdown-panel">
              <RouterLink :to="{name: 'Map'}" class="dropdown-item">
                <span class="material-symbols-outlined">map</span>
                <span class="item-text">은행 찾기</span>
              </RouterLink>
              <RouterLink :to="{name: 'Goods'}" class="dropdown-item" @click="isDropdownOpen = false">
                <span class="material-symbols-outlined">payments</span>
                <span class="item-text">금/은 시세</span>
              </RouterLink>
              <RouterLink :to="{name: 'Search'}" class="dropdown-item" @click="isDropdownOpen = false">
                <span class="material-symbols-outlined">search</span>
                <span class="item-text">관심 종목 검색</span>
              </RouterLink>
            </div>
          </transition>
        </div>
      </div>

      <div class="nav-group-right">
        <div class="lg-only auth-buttons">
          <template v-if="!accountstore.isLogin">
            <RouterLink :to="{name:'LoginView'}" class="btn-login no-wrap">로그인</RouterLink>
            <RouterLink :to="{name:'SignUpView'}" class="btn-signup no-wrap">회원가입</RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="{name:'Profile'}" class="btn-profile no-wrap">마이페이지</RouterLink>
            <button @click.prevent="logOut" class="btn-logout no-wrap">로그아웃</button>
          </template>
        </div>

        <button class="mobile-btn" @click="isMobileMenuOpen = !isMobileMenuOpen">
          <span class="material-symbols-outlined">{{ isMobileMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const isDropdownOpen = ref(false)
const isMobileMenuOpen = ref(false)
const accountstore = useAccountStore()

const logOut = () => { accountstore.logOut() }
const handleLogoutMobile = () => {
  isMobileMenuOpen.value = false
  logOut()
}
</script>

<style scoped>
/* 드롭다운 위치 고정 핵심 스타일 */
.nav-item-dropdown {
  position: relative; /* 자식인 패널이 위치할 기준점 */
  display: flex;
  align-items: center;
  height: var(--nav-height); /* 내브바 전체 높이를 사용하여 마우스 오버 유지 */
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 2px;
  cursor: pointer;
}

.dropdown-panel {
  position: absolute;
  top: 100%; /* 부모(nav-item-dropdown)의 하단 끝에 딱 붙음 */
  left: 50%;
  transform: translateX(-50%); /* 정확히 중앙 정렬 */
  margin-top: -8px; /* 내브바 하단 경계선과의 간격 미세 조정 */
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
  padding: 8px;
  border: 1px solid var(--toss-border);
  min-width: 160px;
  z-index: 1001;
}

/* 드롭다운 아이템 스타일 */
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  text-decoration: none;
  color: var(--toss-text-sub);
  transition: all 0.2s;
}

.dropdown-item:hover {
  background-color: var(--toss-gray-bg);
  color: var(--toss-blue);
}

.dropdown-item .material-symbols-outlined {
  font-size: 20px;
}

.item-text {
  font-size: 14px;
  font-weight: 500;
}

/* 애니메이션 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-10px);
}

.toss-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  height: var(--nav-height); background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px); border-bottom: 1px solid var(--toss-border);
  display: flex; align-items: center; /* 세로 중앙 정렬 핵심 */
}

.nav-container {
  width: 100%; max-width: 1100px; margin: 0 auto;
  padding: 0 20px; display: flex; justify-content: space-between; align-items: center;
}

/* 그룹별 공통 스타일 */
.nav-group-left, .nav-group-center, .nav-group-right { display: flex; align-items: center; }
.nav-group-center { gap: 32px; }
.auth-buttons { display: flex; align-items: center; gap: 12px; }

/* 텍스트 및 로고 */
.logo { font-size: 20px; font-weight: 700; color: var(--toss-text-main); text-decoration: none; margin-right: 40px; }
.nav-link { font-size: 15px; font-weight: 500; color: var(--toss-text-sub); text-decoration: none; display: flex; align-items: center; gap: 4px; }
.nav-link:hover { color: var(--toss-text-main); }

/* 버튼 디자인 (토스 스타일) */
.btn-signup {
  background: var(--toss-blue); color: white !important;
  padding: 6px 12px; border-radius: 8px; font-weight: 400; text-decoration: none;
}
.btn-profile {
  background: #f2f4f6; color: var(--toss-text-sub) !important;
  padding: 6px 12px; border-radius: 8px; font-weight: 400; text-decoration: none;
}
.btn-login { color: var(--toss-text-sub); text-decoration: none; padding: 8px; font-size: 15px; }
.btn-logout { background: none; border: none; color: #f04452; cursor: pointer; font-size: 15px; }

/* Prevent dropdown item text from wrapping; show ellipsis */
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  text-decoration: none;
  color: var(--toss-text-sub);
  transition: all 0.2s;
  white-space: nowrap;        /* 한 줄 고정 */
  overflow: hidden;          /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis;   /* 말줄임 처리 */
}

/* Allow the text span to shrink inside flex so ellipsis works */
.dropdown-item .item-text {
  flex: 1 1 auto;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 반응형 제어 (CSS만으로 확실하게) */
@media (max-width: 1023px) {
  .lg-only { display: none !important; }
}

@media (min-width: 1024px) {
  .mobile-btn { display: none !important; }
}

</style>