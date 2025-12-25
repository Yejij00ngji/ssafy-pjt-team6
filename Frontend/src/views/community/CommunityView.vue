<template>
  <div class="toss-container">
      <SearchBar 
      v-model="searchQuery" 
      placeholder="지금 궁금한 주제를 검색해보세요"
      @search="fetchArticles" 
    />

    <nav class="icon-menu-grid">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        @click="changeCategory(tab.value)"
        :class="['menu-item', { active: currentCategory === tab.value }]"
      >
        <div class="icon-circle" :style="{ backgroundColor: tab.bgColor }">
          <span class="menu-icon">{{ tab.icon }}</span>
        </div>
        <span class="menu-label">{{ tab.label }}</span>
      </button>
    </nav>

    <main class="community-content">
      <div class="article-list">
        <div v-if="isLoading" class="loading-state">데이터를 불러오는 중입니다...</div>
        
        <ArticleListItem 
          v-for="article in articles" 
          :key="article.id" 
          :article="article" 
          class="toss-article-card"
        />

        <div v-if="!isLoading && articles.length === 0" class="empty-state">
          <p>아직 작성된 게시글이 없습니다.</p>
        </div>
      </div>
    </main>

    <button class="fab-button" @click="goCreate">
      <span class="fab-icon">✏️</span>
      <span class="fab-text">글 작성하기</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import ArticleListItem from '@/components/community/ArticleListItem.vue'
import SearchBar from '@/components/home/SearchBar.vue'
const searchQuery = ref('') // 검색어 상태 추가

const router = useRouter()
const route = useRoute()

const articles = ref([])
const isLoading = ref(false)
const currentCategory = ref(route.query.category || 'all') // URL 쿼리에서 카테고리 초기화

// 인프런 스타일 아이콘 및 색상 추가
const tabs = [
  { label: '전체', value: 'all', icon: '🏠', bgColor: '#f2f4f6' },
  { label: '공지사항', value: 'notice', icon: '📢', bgColor: '#e8f3ff' },
  { label: '스터디', value: 'study', icon: '📖', bgColor: '#e7f9f4' },
  { label: '공모전', value: 'contest', icon: '🏆', bgColor: '#fff4e6' },
  { label: 'Q&A', value: 'qna', icon: '❓', bgColor: '#f3f0ff' },
  { label: '자유게시판', value: 'free', icon: '💬', bgColor: '#fff0f6' },
]

// API 호출: 카테고리에 맞는 목록 가져오기
const fetchArticles = async () => {
  isLoading.value = true
  try {
    const params = currentCategory.value === 'all' ? {} : { category: currentCategory.value }
    const response = await axios.get('http://127.0.0.1:8000/community/', { params })
    articles.value = response.data
  } catch (err) {
    console.error('목록 로드 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 카테고리 변경 시 URL 쿼리 업데이트
const changeCategory = (val) => {
  currentCategory.value = val
  router.push({ query: { category: val } })
}

// URL 쿼리가 바뀔 때마다(탭 클릭 시) 데이터를 다시 부름
watch(() => route.query.category, (newVal) => {
  currentCategory.value = newVal || 'all'
  fetchArticles()
})

const goCreate = () => router.push({ name: 'ArticleCreate' })

onMounted(fetchArticles)
</script>

<style scoped>
/* 검색바 디자인 */
.search-section {
  margin-bottom: 32px;
  display: flex;
  justify-content: center;
}

.search-bar-inner {
  display: flex;
  align-items: center;
  background-color: #f2f4f6;
  padding: 12px 20px;
  border-radius: 32px;
  width: 100%;
  max-width: 600px;
  gap: 12px;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.search-bar-inner:focus-within {
  background-color: #fff;
  border-color: var(--toss-blue);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.toss-input-invisible {
  border: none;
  background: none;
  outline: none;
  width: 100%;
  font-size: 16px;
  color: #191f28;
}

/* 아이콘 메뉴 그리드 */
.icon-menu-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
  margin-bottom: 48px;
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  border: none;
  background: none;
  cursor: pointer;
  padding: 12px;
  border-radius: 16px;
  transition: all 0.2s;
}

.menu-item:hover { background-color: #f9fafb; }
.menu-item.active .menu-label { color: var(--toss-blue); font-weight: 700; }
.menu-item.active .icon-circle { transform: scale(1.1); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }

.icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  transition: all 0.2s;
}

.menu-label { font-size: 14px; color: #4e5968; font-weight: 500; }

/* 리스트 스타일 */
.article-list {
  display: flex;
  flex-direction: column;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 80px 0;
  color: #8b95a1;
}

/* FAB 버튼 */
.fab-button {
  position: fixed;
  bottom: 40px;
  right: calc(50% - 540px);
  background-color: #3182f6; /* 토스 블루 */
  color: white;
  padding: 16px 24px;
  border-radius: 32px;
  border: none;
  font-weight: 700;
  font-size: 16px;
  box-shadow: 0 8px 24px rgba(0, 173, 124, 0.3);
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  z-index: 999;
  transition: all 0.2s ease;
}

.fab-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(0, 173, 124, 0.4);
}

@media (max-width: 1100px) {
  .fab-button { right: 32px; }
  .icon-menu-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>