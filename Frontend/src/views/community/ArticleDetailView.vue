<template>
  <div class="toss-container" v-if="article">
    <div class="article-detail-wrapper">
      <header class="article-header">
        <div class="header-top">
          <span class="category-badge" :class="article.category">
            {{ article.category_label }}
          </span>
          <div v-if="accountStore.user && Number(accountStore.user.pk) === Number(article.user.id)" class="action-buttons">
            <router-link :to="{ name: 'ArticleUpdate', params: { id: article.id } }" class="text-btn">수정</router-link>
            <button @click="deleteArticle" class="text-btn delete">삭제</button>
          </div>
        </div>
        
        <h1 class="article-title">{{ article.title }}</h1>
        
        <div class="author-info">
          <div class="avatar-sm"></div>
          <div class="author-details">
            <span class="nickname">{{ article.user.nickname }}</span>
            <span class="meta">{{ formatDate(article.created_at) }} · 조회 {{ article.views }}</span>
          </div>
        </div>
      </header>

      <div class="article-body">
        <img v-if="article.image" :src="article.image" class="body-image">
        <div class="body-content">
          {{ article.content }}
        </div>
      </div>

      <div class="article-actions">
        <button class="like-btn" @click="handleLike">
          <span class="icon">👍</span>
          <span class="count">{{ article.likes }}</span>
        </button>
      </div>

      <section class="comment-section">
        <div class="comment-header">
          <h3 class="section-title">댓글 <span>{{ article.comments.length }}</span></h3>
        </div>

        <div class="comment-input-wrapper">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 남겨보세요" 
            rows="1"
            @input="autoResize"
          ></textarea>
          <button @click="submitComment" :disabled="!newComment.trim()" class="submit-btn">
            등록
          </button>
        </div>

        <div class="comment-list">
          <CommentItem 
            v-for="comment in article.comments" 
            :key="comment.id" 
            :comment="comment" 
            @delete-comment="handleDeleteComment"
            @update-comment="handleUpdateComment"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
/* 기존 로직 유지 (import, fetchArticleDetail, deleteArticle, submitComment 등) */
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

const fetchArticleDetail = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/community/${route.params.id}/`)
    article.value = response.data

    // 이 로그를 통해 버튼이 안 보이는 원인을 찾으세요!
    console.log('현재 로그인 유저 PK:', accountStore.user?.pk)
    console.log('게시글 작성자 ID:', article.value.user?.id)

  } catch (err) {
    alert('게시글을 찾을 수 없습니다.')
    router.push({ name: 'Community' })
  }
}

// 게시글 좋아요
const handleLike = async () => {
  try {
    await axios.post(`http://127.0.0.1:8000/community/${article.value.id}/like/`, {}, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    // 백엔드에서 준 최신 데이터로 로컬 상태 업데이트
    article.value.likes = response.data.like_count

    // fetchArticleDetail() // 좋아요 수 업데이트를 위해 다시 불러오기
  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}

const deleteArticle = async () => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await axios.delete(`http://127.0.0.1:8000/community/${route.params.id}/`, {
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      router.push({ name: 'Community' }) 
    } catch (err) { console.error(err) }
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    const token = accountStore.token 
    if (!token) { alert('로그인이 필요합니다.'); return }
    await axios.post(
      `http://127.0.0.1:8000/community/${article.value.id}/comments/`, 
      { content: newComment.value },
      { headers: { Authorization: `Token ${token}` } }
    )
    newComment.value = ''
    fetchArticleDetail()
  } catch (err) { console.error(err) }
}

// 1. 댓글 삭제 함수
const handleDeleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    try {
      await axios.delete(`http://127.0.0.1:8000/community/comments/${commentId}/`, {
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      // 삭제 후 게시글 상세 정보를 다시 불러와 댓글 목록 갱신
      fetchArticleDetail()
    } catch (err) {
      console.error('댓글 삭제 실패:', err)
      alert('본인의 댓글만 삭제할 수 있습니다.')
    }
  }
}

// 2. 댓글 수정 함수 (수정 로직이 있다면)
const handleUpdateComment = async (payload) => {
  // 디버깅용: 데이터가 어떻게 들어오는지 확인
  console.log('부모가 받은 데이터:', payload)

  try {
    // payload 안의 commentId와 content를 꺼냅니다.
    const { commentId, content } = payload
    
    // 만약 아이디가 없으면 여기서 차단
    if (!commentId) {
      console.error("댓글 ID를 찾을 수 없습니다. payload를 확인하세요.");
      return
    }

    await axios.put(`http://127.0.0.1:8000/community/comments/${commentId}/`, 
      { content: content },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    
    fetchArticleDetail() // 성공 시 목록 갱신
  } catch (err) {
    console.error('댓글 수정 실패:', err)
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}. ${date.getMonth() + 1}. ${date.getDate()}.`
}

const autoResize = (e) => {
  e.target.style.height = 'auto'
  e.target.style.height = e.target.scrollHeight + 'px'
}

onMounted(fetchArticleDetail)
</script>

<style scoped>
.article-detail-wrapper {
  max-width: 720px; /* 읽기 최적화 너비 */
  margin: 0 auto;
  padding: 20px 0;
}

/* Header 스타일 */
.article-header { margin-bottom: 40px; }
.header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }

.category-badge { font-size: 14px; font-weight: 700; color: var(--toss-blue); }
.text-btn { font-size: 14px; color: #8b95a1; background: none; border: none; margin-left: 12px; cursor: pointer; text-decoration: none; }
.text-btn.delete:hover { color: #f03e3e; }

.article-title { font-size: 32px; font-weight: 700; color: #191f28; line-height: 1.3; margin-bottom: 24px; }

.author-info { display: flex; align-items: center; gap: 12px; }
.avatar-sm { width: 40px; height: 40px; background-color: #f2f4f6; border-radius: 50%; }
.nickname { display: block; font-size: 16px; font-weight: 600; color: #191f28; }
.meta { font-size: 14px; color: #8b95a1; }

/* Body 스타일 */
.article-body { padding: 20px 0; margin-bottom: 40px; }
.body-image { width: 100%; border-radius: 16px; margin-bottom: 32px; }
.body-content { font-size: 17px; line-height: 1.8; color: #333d4b; white-space: pre-wrap; }

/* Actions 스타일 */
.article-actions { display: flex; justify-content: center; padding-bottom: 48px; border-bottom: 1px solid #f2f4f6; }
.like-btn { 
  display: flex; align-items: center; gap: 8px; padding: 12px 24px;
  border-radius: 24px; border: 1px solid #e5e8eb; background: #fff;
  font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.like-btn:hover { background-color: #f9fafb; border-color: #d1d6db; }

/* Comment 스타일 */
.comment-section { padding-top: 48px; }
.section-title { font-size: 20px; font-weight: 700; margin-bottom: 24px; }
.section-title span { color: var(--toss-blue); }

.comment-input-wrapper {
  display: flex; gap: 12px; align-items: flex-end;
  background-color: #f9fafb; padding: 16px; border-radius: 16px; margin-bottom: 32px;
}
.comment-input-wrapper textarea {
  flex: 1; background: none; border: none; outline: none;
  font-size: 15px; line-height: 1.5; resize: none; max-height: 200px;
}
.submit-btn {
  background-color: var(--toss-blue); color: #fff; border: none;
  padding: 8px 16px; border-radius: 10px; font-weight: 600; cursor: pointer;
}
.submit-btn:disabled { background-color: #d1d6db; cursor: default; }

@media (max-width: 768px) {
  .article-title { font-size: 24px; }
}
</style>