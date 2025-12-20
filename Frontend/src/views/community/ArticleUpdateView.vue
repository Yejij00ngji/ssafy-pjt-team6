<template>
  <div class="container py-5">
    <div class="max-width-800 mx-auto">
      <h2 class="fw-bold mb-4">게시글 수정</h2>
      
      <form @submit.prevent="updateArticle">
        <div class="mb-3">
          <label class="form-label">제목</label>
          <input v-model="title" type="text" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">내용</label>
          <textarea v-model="content" class="form-control" rows="10" required></textarea>
        </div>

        <div class="d-flex justify-content-end gap-2">
          <button type="button" class="btn btn-outline-secondary" @click="$router.back()">취소</button>
          <button type="submit" class="btn btn-primary">수정 완료</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const title = ref('')
const content = ref('')

// 1. 기존 데이터 불러오기
const fetchOriginalArticle = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/community/${route.params.id}/`)
    
    // 작성자 본인인지 확인
    if (response.data.user.id !== accountStore.user.pk) {
      alert('본인의 게시글만 수정할 수 있습니다.')
      router.back()
      return
    }

    title.value = response.data.title
    content.value = response.data.content
  } catch (err) {
    console.error(err)
  }
}

// 2. 수정 요청 보내기
const updateArticle = async () => {
  try {
    await axios.put(
      `http://127.0.0.1:8000/community/${route.params.id}/`,
      {
        title: title.value,
        content: content.value,
      },
      {
        headers: { Authorization: `Token ${accountStore.token}` }
      }
    )
    alert('게시글이 성공적으로 수정되었습니다.')
    router.push({ name: 'ArticleDetail', params: { id: route.params.id } })
  } catch (err) {
    console.error(err)
    alert('수정에 실패했습니다.')
  }
}

onMounted(fetchOriginalArticle)
</script>