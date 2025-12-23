<template>
  <div class="comment-item">
    <div class="comment-header">
      <div class="user-group">
        <div class="avatar-wrapper">
          <img :src="`https://ui-avatars.com/api/?name=${comment.user.nickname}&background=f2f4f6&color=8b95a1`" class="avatar-img">
        </div>
        <div class="user-info">
          <div class="name-row">
            <span class="nickname">{{ comment.user.nickname }}</span>
            <span v-if="isAuthor" class="author-label">작성자</span>
          </div>
          <span class="created-at">{{ formatDate(comment.created_at) }}</span>
        </div>
      </div>

      <div v-if="isMyComment && !isEditing" class="action-group">
        <button @click="toggleEdit" class="text-btn">수정</button>
        <button @click="$emit('delete-comment', comment.id)" class="text-btn delete">삭제</button>
      </div>
    </div>

    <div class="comment-body">
      <div v-if="!isEditing" class="content-text">
        {{ comment.content }}
      </div>
      
      <div v-else class="edit-wrapper">
        <textarea v-model="editContent" class="edit-textarea" rows="3"></textarea>
        <div class="edit-actions">
          <button @click="cancelEdit" class="toss-btn-sub-s">취소</button>
          <button @click="onUpdate" class="toss-btn-primary-s">저장</button>
        </div>
      </div>
    </div>

    <div v-if="!isEditing" class="comment-footer">
      <button class="interaction-btn">
        <span class="icon">💬</span> 답글 달기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore()
const props = defineProps({
  comment: Object,
  articleAuthorId: [Number, String] // 부모로부터 게시글 작성자 ID를 전달받으면 좋습니다
})

const emit = defineEmits(['delete-comment', 'update-comment'])

const isEditing = ref(false)
const editContent = ref(props.comment.content)

// 권한 확인 로직
const isMyComment = computed(() => 
  accountStore.user && Number(accountStore.user.pk) === Number(props.comment.user.id)
)

// 작성자 여부 (예시: 상위 컴포넌트에서 정보를 주거나 비교 로직 필요)
const isAuthor = computed(() => false) // 로직에 따라 구현

const toggleEdit = () => {
  isEditing.value = true
  editContent.value = props.comment.content
}

const cancelEdit = () => { isEditing.value = false }

const onUpdate = () => {
  if (!editContent.value.trim()) return

  // 부모에게 보낼 때 'commentId'라는 이름을 정확히 사용합니다.
  emit('update-comment', { 
    commentId: props.comment.id, 
    content: editContent.value 
  })
  
  isEditing.value = false // 수정 모드 종료
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}월 ${date.getDate()}일`
}
</script>

<style scoped>
.comment-item {
  padding: 24px 0;
  border-bottom: 1px solid #f2f4f6;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.user-group { display: flex; align-items: center; gap: 12px; }
.avatar-img { width: 36px; height: 36px; border-radius: 50%; }

.name-row { display: flex; align-items: center; gap: 6px; }
.nickname { font-size: 15px; font-weight: 600; color: #191f28; }
.author-label { font-size: 12px; color: var(--toss-blue); font-weight: 700; }
.created-at { font-size: 13px; color: #8b95a1; }

.text-btn { font-size: 13px; color: #8b95a1; background: none; border: none; cursor: pointer; margin-left: 8px; }
.text-btn.delete:hover { color: #f03e3e; }

.comment-body { margin-bottom: 16px; }
.content-text { font-size: 15px; line-height: 1.6; color: #333d4b; white-space: pre-wrap; }

/* 수정 모드 스타일 */
.edit-wrapper {
  background-color: #f9fafb;
  padding: 12px;
  border-radius: 12px;
}
.edit-textarea {
  width: 100%;
  background: none;
  border: none;
  outline: none;
  font-size: 15px;
  resize: none;
}
.edit-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }

/* 하단 버튼 */
.interaction-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 600;
  color: #4e5968;
  cursor: pointer;
  padding: 0;
}
.interaction-btn:hover { color: var(--toss-blue); }

/* 토스 스타일 공통 버튼(작은 사이즈) */
.toss-btn-primary-s { background-color: var(--toss-blue); color: #fff; border: none; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600; }
.toss-btn-sub-s { background-color: #e5e8eb; color: #4e5968; border: none; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600; }
</style>