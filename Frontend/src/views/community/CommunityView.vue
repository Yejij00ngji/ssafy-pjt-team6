<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-8">
        <h2 class="fw-bold mb-4">커뮤니티</h2>
        
        <ul class="nav nav-tabs mb-4 border-0 custom-tabs">
          <li class="nav-item" v-for="tab in tabs" :key="tab.value">
            <button 
              class="nav-link" 
              :class="{ active: currentCategory === tab.value }"
              @click="changeCategory(tab.value)"
            >
              {{ tab.label }}
            </button>
          </li>
        </ul>

        <div class="search-box mb-4">
          <div class="input-group bg-light rounded-3 p-1">
            <span class="input-group-text border-0 bg-transparent">🔍</span>
            <input type="text" class="form-control border-0 bg-transparent" placeholder="관심있는 주제나 게시글을 검색해보세요">
          </div>
        </div>

        <div class="article-list">
          <ArticleListItem 
            v-for="article in articles" 
            :key="article.id" 
            :article="article" 
          />
        </div>
      </div>

      <div class="col-lg-4 d-none d-lg-block">
        <button class="btn btn-primary w-100 py-3 rounded-3 fw-bold mb-4" @click="goCreate">
          📝 게시글 작성하기
        </button>

        <div class="card border-0 shadow-sm rounded-3 mb-4 p-4">
          <h6 class="fw-bold mb-3">내 활동</h6>
          <div class="d-flex align-items-center mb-3">
            <div class="avatar me-3"></div>
            <div>
              <div class="fw-bold">User123</div>
              <div class="text-muted small">가입일 2024.01.01</div>
            </div>
          </div>
          <div class="d-flex justify-content-around text-center border-top pt-3">
            <div><div class="fw-bold">12</div><div class="small text-muted">작성글</div></div>
            <div><div class="fw-bold">45</div><div class="small text-muted">댓글</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import ArticleListItem from '@/components/community/ArticleListItem.vue'

const router = useRouter()
const route = useRoute()

const articles = ref([])
const isLoading = ref(false)
const currentCategory = ref(route.query.category || 'all') // URL 쿼리에서 카테고리 초기화

const tabs = [
  { label: '전체', value: 'all' },
  { label: '공지사항', value: 'notice' },
  { label: '스터디', value: 'study' },
  { label: '공모전', value: 'contest' },
  { label: 'Q&A', value: 'qna' },
  { label: '자유게시판', value: 'free' },
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
.custom-tabs .nav-link { color: #666; border: none; font-weight: bold; }
.custom-tabs .nav-link.active { color: #000; border-bottom: 2px solid #000 !important; background: none; }
.avatar { width: 45px; height: 45px; background: #eee; border-radius: 50%; }
</style>