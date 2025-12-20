<template>
  <div class="card border-0 shadow-sm mb-3 article-card" @click="goDetail">
    <div class="card-body p-4 d-flex justify-content-between align-items-center">
      <div class="flex-grow-1 pe-3">
        <span class="badge bg-light text-primary mb-2">{{ article.category }}</span>
        <h5 class="fw-bold mb-2">{{ article.title }}</h5>
        <p class="text-muted small text-truncate-2 mb-3">{{ article.content }}</p>
        <div class="d-flex align-items-center text-muted small">
          <span>{{ article.user.nickname }}</span>
          <span class="mx-2">·</span>
          <span>{{ article.created_at }}</span>
          <span class="ms-3">💬 {{ article.comment_count }}</span>
        </div>
      </div>
      <div v-if="article.image" class="thumbnail-box ms-3">
        <img :src="article.image" class="rounded-3" style="width: 100px; height: 70px; object-fit: cover;">
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps(['article'])
const router = useRouter()
const goDetail = () => router.push({ name: 'ArticleDetail', params: { id: props.article.id } })
</script>

<style scoped>
.article-card { cursor: pointer; transition: transform 0.2s; }
.article-card:hover { transform: translateY(-3px); }
.text-truncate-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>