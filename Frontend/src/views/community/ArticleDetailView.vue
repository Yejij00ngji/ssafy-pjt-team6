<template>
  <div class="container py-5" v-if="article">
    <div class="max-width-800 mx-auto">
      <header class="mb-5 text-center">
        <span class="text-primary fw-bold mb-3 d-block">{{ article.category_label }}</span>
        <h1 class="fw-bold mb-4">{{ article.title }}</h1>
        <div class="d-flex justify-content-center align-items-center text-muted">
          <div class="avatar-sm me-2"></div>
          <span class="fw-bold text-dark me-3">{{ article.user.nickname }}</span>
          <span>{{ article.created_at }}</span>
          <span class="ms-3">👁️ {{ article.views }}</span>
        </div>
      </header>

      <div class="article-body py-4 border-top">
        <img v-if="article.image" :src="article.image" class="w-100 rounded-4 mb-5 shadow-sm">
        <div class="content fs-5" style="line-height: 1.8;">{{ article.content }}</div>
      </div>

      <div class="text-center my-5 pb-5 border-bottom">
        <button class="btn btn-outline-danger px-4 rounded-pill me-3">👍 {{ article.likes }}</button>
        <button class="btn btn-outline-secondary px-4 rounded-pill">💬 댓글 {{ article.comments.length }}</button>
      </div>

      <!-- <section class="comment-section">
        <h5 class="fw-bold mb-4">Comments</h5>
        <textarea v-model="newComment" class="form-control mb-3 p-3 bg-light border-0" rows="3" placeholder="의견을 남겨주세요..."></textarea>
        <div class="text-end mb-5">
          <button class="btn btn-primary px-4" @click="submitComment">등록</button>
        </div>

        <div v-for="comment in article.comments" :key="comment.id" class="comment-item py-3 border-bottom">
          <div class="fw-bold mb-1">{{ comment.user.nickname }}</div>
          <div class="text-secondary small">{{ comment.content }}</div>
        </div>
      </section> -->

      <section class="comment-section mt-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h5 class="fw-bold">답변 <span class="text-success">{{ article.comments.length }}</span></h5>
        <select class="form-select form-select-sm w-auto">
          <option>좋아요순</option>
          <option>최신순</option>
        </select>
      </div>

      <div class="comment-input-card mb-5 border rounded-3 p-3 shadow-sm bg-white">
        <textarea v-model="newComment" class="form-control border-0" rows="2" placeholder="답변을 작성해보세요."></textarea>
        <div class="text-end mt-2">
          <button @click="submitComment" class="btn btn-primary btn-sm">등록</button>
        </div>
      </div>

      <CommentItem 
        v-for="comment in article.comments" 
        :key="comment.id" 
        :comment="comment" 
      />
    </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import CommentItem from '@/components/community/CommentItem.vue'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore() 

const article = ref(null)
const newComment = ref('')

// 상세 데이터 및 댓글 가져오기
const fetchArticleDetail = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/community/${route.params.id}/`)
    article.value = response.data
  } catch (err) {
    alert('게시글을 찾을 수 없습니다.')
    router.push({ name: 'Community' })
  }
}

// 댓글 등록 로직
const submitComment = async () => {
  // 입력값 검증 (공백만 있는 경우 방지)
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }
  
  try {
    // 2. 스토어에서 토큰 가져오기 (가장 확실한 방법)
    const token = accountStore.token 
    
    if (!token) {
      alert('로그인이 필요한 서비스입니다.')
      return
    }

    // 3. POST 요청 실행
    await axios.post(
      `http://127.0.0.1:8000/community/${article.value.id}/comments/`, 
      { content: newComment.value },
      { 
        headers: { 
          // 'Token ' 문자열 뒤에 한 칸 띄우는 것 잊지 마세요!
          Authorization: `Token ${token}` 
        } 
      }
    )
    
    // 성공 시 처리
    newComment.value = '' // 입력창 비우기
    fetchArticleDetail()   // 게시글 상세 정보를 다시 불러와 댓글 목록 갱신
    alert('댓글이 등록되었습니다.')

  } catch (err) {
    console.error('댓글 등록 실패:', err.response?.data || err)
    // 400 에러 등이 날 경우 서버에서 주는 에러 메시지를 alert로 띄워주면 좋습니다.
    alert('댓글 등록에 실패했습니다.')
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`
}

onMounted(fetchArticleDetail)
</script>

<style scoped>
.max-width-800 { max-width: 800px; }
.avatar-sm { width: 30px; height: 30px; background: #ddd; border-radius: 50%; }
</style>