<template>
  <div style="background: #fff3f3; padding: 5px; font-size: 12px; border: 1px solid red;">
    내 ID: {{ accountStore.user?.pk }} (타입: {{ typeof accountStore.user?.pk }}) <br>
    작성자 ID: {{ comment.user.id }} (타입: {{ typeof comment.user.id }}) <br>
    비교 결과: {{ accountStore.user?.id == comment.user.id }}
  </div>
  <div class="comment-wrapper d-flex gap-3 py-4 border-bottom">
    <div class="vote-section d-flex flex-column align-items-center">
      <button class="btn btn-link p-0 text-secondary"><i class="bi bi-hand-thumbs-up"></i></button>
      <button class="btn btn-link p-0 text-secondary"><i class="bi bi-hand-thumbs-down"></i></button>
    </div>

    <div class="content-section flex-grow-1">
      <div class="d-flex align-items-center mb-2">
        <div class="avatar me-2">
          <img :src="`https://ui-avatars.com/api/?name=${comment.user.nickname}`" class="rounded-circle" width="32">
        </div>
        <div class="user-info">
          <span class="fw-bold me-2">{{ comment.user.nickname }}</span>
          <span class="badge bg-light text-success border">지식공유자</span> <div class="text-muted small">{{ comment.created_at }}</div>
        </div>
      </div>

      <div class="comment-text mb-3 text-dark">
        {{ comment.content }}
      </div>

      <div v-if="accountStore.user && Number(accountStore.user.pk) === Number(comment.user.id)">
        <button 
          @click="$emit('delete-comment', comment.id)" 
          class="btn btn-sm text-danger border-0 p-0"
        >삭제
        </button>
      </div>

      <div class="comment-actions d-flex gap-2">
        <button class="btn btn-sm btn-light border-0 rounded-pill px-3">💬 답글</button>
        <button class="btn btn-sm btn-link text-secondary"><i class="bi bi-link-45deg"></i></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';
const accountStore = useAccountStore()

defineProps({
  comment: Object
})

// 부모에게 보낼 이벤트 이름 정의
defineEmits(['delete-comment'])

</script>

<style scoped>
.avatar img { background: #f0f0f0; }
.comment-text { white-space: pre-wrap; line-height: 1.6; }
.vote-section .bi { font-size: 1.2rem; }
</style>