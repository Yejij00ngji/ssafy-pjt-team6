<template>
  <div class="article-item" @click="goDetail">
    <div class="content-left">
      <span class="category-text" :class="article.category">
        {{ getCategoryLabel(article.category) }}
      </span>
      
      <h3 class="article-title">{{ article.title }}</h3>
      <p class="article-excerpt">{{ article.content }}</p>
      
      <div class="article-meta">
        <span class="author">{{ article.user.nickname }}</span>
        <span class="divider">·</span>
        <span class="date">{{ formatDate(article.created_at) }}</span>
        <div class="stats">
          <span class="comment-count">💬 {{ article.comment_count }}</span>
        </div>
      </div>
    </div>

    <div v-if="article.image" class="thumbnail-area">
      <img :src="article.image" alt="thumbnail" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps(['article'])
const router = useRouter()

const goDetail = () => router.push({ name: 'ArticleDetail', params: { id: props.article.id } })

// 날짜 포맷팅 (예: 2분 전, 또는 날짜)
const formatDate = (dateStr) => {
  return dateStr.split('T')[0] // 단순 날짜만 표시 (정적 느낌 강조)
}

const getCategoryLabel = (cat) => {
  const labels = { notice: '공지', study: '스터디', contest: '공모전', qna: '질문답변', free: '자유' }
  return labels[cat] || cat
}
</script>

<style scoped>
.article-item {
  display: flex;
  justify-content: space-between;
  padding: 24px 0;
  border-bottom: 1px solid #f2f4f6; /* 얇고 정적인 구분선 */
  cursor: pointer;
}

/* 호버 시 배경색만 살짝 변경 (움직임 없음) */
.article-item:hover {
  background-color: #fafafa;
}

.content-left {
  flex: 1;
  padding-right: 20px;
}

.category-text {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 8px;
  display: inline-block;
}

/* 카테고리별 정적 색상 */
.category-text.notice { color: #3182f6; }
.category-text.study { color: #00ad7c; }
.category-text.qna { color: #7048e8; }
.category-text.free { color: #f03e3e; }

.article-title {
  font-size: 18px;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 8px;
  line-height: 1.4;
}

.article-excerpt {
  font-size: 15px;
  color: #4e5968;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;
}

.article-meta {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #8b95a1;
  gap: 8px;
}

.divider { color: #e5e8eb; }
.stats { margin-left: auto; }

.thumbnail-area img {
  width: 110px;
  height: 76px;
  object-fit: cover;
  border-radius: 8px;
  background-color: #f2f4f6;
}
</style>