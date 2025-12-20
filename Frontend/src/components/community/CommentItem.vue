<template>

  <div class="comment-wrapper d-flex gap-3 py-4 border-bottom">
    <div class="vote-section d-flex flex-column align-items-center">
      <button class="btn btn-link p-0 text-secondary"><i class="bi bi-hand-thumbs-up"></i></button>
      <button class="btn btn-link p-0 text-secondary"><i class="bi bi-hand-thumbs-down"></i></button>
    </div>

    <div class="content-section flex-grow-1">
      <div v-if="!isEditing">
        <div class="d-flex align-items-center mb-2">
          <div class="avatar me-2">
            <img :src="`https://ui-avatars.com/api/?name=${comment.user.nickname}`" class="rounded-circle" width="32">
          </div>
          <div class="user-info">
            <span class="fw-bold me-2">{{ comment.user.nickname }}</span>
            <span class="badge bg-light text-success border">글쓴이</span> 
            <div class="text-muted small">{{ comment.created_at }}</div>
          </div>
        </div>
        
        <div class="comment-text mb-3 text-dark">
          {{ comment.content }}
        </div>
        
        <div v-if="accountStore.user && Number(accountStore.user.pk) === Number(comment.user.id)" class="mb-2">
          <button @click="toggleEdit" class="btn btn-sm text-primary border-0 p-0 me-2">수정</button>
          <button @click="$emit('delete-comment', comment.id)" class="btn btn-sm text-danger border-0 p-0">삭제</button>
        </div>
        
        <div class="comment-actions d-flex gap-2">
          <button class="btn btn-sm btn-light border-0 rounded-pill px-3">💬 답글</button>
          <button class="btn btn-sm btn-link text-secondary"><i class="bi bi-link-45deg"></i></button>
        </div>
      </div>

      <div v-else>
        <textarea v-model="editContent" class="form-control mb-2" rows="2"></textarea>
        <div class="d-flex justify-content-end gap-2">
          <button @click="cancelEdit" class="btn btn-sm btn-outline-secondary">취소</button>
          <button @click="onUpdate" class="btn btn-sm btn-primary">저장</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/accounts';
const accountStore = useAccountStore()

const props = defineProps({
  comment: Object
})

// 부모에게 보낼 이벤트 이름 정의
const emit = defineEmits(['delete-comment', 'update-comment'])

// 수정 관련 상태
const isEditing = ref(false)
const editContent = ref(props.comment.content)

// 수정 모드 전환
const toggleEdit = () => {
  isEditing.value = true
  editContent.value = props.comment.content // 취소했다가 다시 누를 때를 대비해 초기화
}

// 수정 취소
const cancelEdit = () => {
  isEditing.value = false
}

// 부모에게 수정 신호 보내기
const onUpdate = () => {
  if (!editContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }
  // 부모에게 댓글 ID와 수정된 내용을 보냄
  emit('update-comment', props.comment.id, editContent.value)
  isEditing.value = false // 입력창 닫기
}
</script>

<style scoped>
.avatar img { background: #f0f0f0; }
.comment-text { white-space: pre-wrap; line-height: 1.6; }
.vote-section .bi { font-size: 1.2rem; }
</style>