<template>
  <div class="container py-5">
    <div class="max-width-800 mx-auto bg-white p-5 shadow-sm rounded-4">
      <h3 class="fw-bold mb-5">글 작성하기</h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label class="form-label fw-bold">카테고리</label>
          <select v-model="formData.category" class="form-select border-0 bg-light p-3">
            <option value="study">스터디</option>
            <option value="qna">질문&답변</option>
            <option value="free">자유게시판</option>
          </select>
        </div>

        <div class="mb-4">
          <input v-model="formData.title" type="text" class="form-control border-0 bg-light p-3" placeholder="제목을 입력하세요">
        </div>

        <div class="mb-4">
          <textarea v-model="formData.content" class="form-control border-0 bg-light p-3" rows="12" placeholder="내용을 입력하세요"></textarea>
        </div>

        <div class="d-flex justify-content-end gap-2">
          <button type="button" class="btn btn-light px-4" @click="$router.back()">취소</button>
          <button type="submit" class="btn btn-primary px-4 fw-bold" :disabled="isSubmitting">
            {{ isSubmitting ? '게시 중...' : '게시하기' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore() 

const formData = ref({
  title: '',
  content: '',
  category: 'free'
})

const isSubmitting = ref(false)

const handleSubmit = async () => {
  // 3. localStorage 대신 스토어에서 바로 토큰을 가져옵니다.
  const token = accountStore.token 
  
  console.log("확인된 토큰:", token)

  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  isSubmitting.value = true
  try {
    const response = await axios.post('http://127.0.0.1:8000/community/', formData.value, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    alert('글이 등록되었습니다!')
    router.push({ name: 'ArticleDetail', params: { id: response.data.id } })
  } catch (err) {
    console.error('등록 실패:', err.response?.data)
    alert('글 등록에 실패했습니다.')
  } finally {
    isSubmitting.value = false
  }
}
</script>