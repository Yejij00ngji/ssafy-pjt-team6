<template>
  <div class="toss-container">
    <div class="form-wrapper">
      <nav class="form-tabs">
        <button 
          v-for="tab in tabs" :key="tab.value"
          :class="['tab-item', { active: form.category === tab.value }]"
          @click="changeCategory(tab.value)"
        >
          {{ tab.label }}
        </button>
      </nav>

      <div class="guide-box">
        <span class="guide-icon">🍃</span>
        <p>{{ currentGuide }}</p>
      </div>

      <main class="editor-container">
        <input 
          v-model="form.title" 
          type="text" 
          class="editor-title" 
          placeholder="제목에 핵심 내용을 요약해보세요." 
        />
        
        <div class="image-upload-area">
          <label for="file-input" class="image-label" :class="{ 'has-image': imagePreview }">
            <div v-if="!imagePreview" class="upload-content">
              <span class="cam-icon">📸</span>
              <span>대표 이미지 추가 (선택)</span>
            </div>
            <img v-else :src="imagePreview" class="preview-img" />
          </label>
          <input id="file-input" type="file" @change="handleImageUpload" hidden accept="image/*" />
          <button v-if="imagePreview" @click="removeImage" class="remove-btn">✕ 삭제</button>
        </div>

        <textarea 
          v-model="form.content"
          class="editor-content" 
          :placeholder="currentPlaceholder"
          @input="autoResize"
        ></textarea>

        <footer class="form-actions">
          <button type="button" class="toss-btn-sub" @click="$router.back()">취소</button>
          <button 
            type="button" 
            class="toss-btn-primary" 
            :disabled="!isValid" 
            @click="handleSubmit"
          >
            {{ isEdit ? '수정하기' : '등록하기' }}
          </button>
        </footer>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const isEdit = computed(() => route.params.id !== undefined)
const imagePreview = ref(null)

const form = ref({
  title: '',
  category: 'qna',
  content: '',
  image: null
})

// 1. 카테고리별 가이드 및 작성 예시 데이터
const categoryMeta = {
  qna: {
    guide: "궁금한 내용을 상세히 적어주시면 지식공유자나 동료들이 답변해드려요.",
    example: "[질문 내용]\n- 환경: \n- 에러 메시지: \n- 시도해본 방법: "
  },
  study: {
    guide: "프로젝트 모집 예시를 참고해 작성해주세요. 멋진 팀원을 만날 수 있을 거예요.",
    example: "[프로젝트 모집 예시]\n- 주제: \n- 목표: \n- 모집 인원: \n- 연락 방법: "
  },
  free: {
    guide: "학습 고민이나 자유로운 이야기를 나누어보세요.",
    example: "자유롭게 내용을 작성해주세요."
  }
}

const tabs = [
  { label: '질문&답변', value: 'qna' },
  { label: '스터디', value: 'study' },
  { label: '자유게시판', value: 'free' }
]

const currentGuide = computed(() => categoryMeta[form.value.category]?.guide)
const currentPlaceholder = computed(() => categoryMeta[form.value.category]?.example)

// 카테고리 변경 시 로직 (수정 모드가 아닐 때만 예시 문구 삽입 옵션)
const changeCategory = (val) => {
  form.value.category = val
  if (!isEdit.value && !form.value.content) {
    // 사용자가 입력한 게 없을 때만 예시 넣어줌
    // form.value.content = categoryMeta[val].example 
  }
}

// 텍스트 영역 높이 자동 조절 함수 추가
const autoResize = (e) => {
  e.target.style.height = 'auto'
  e.target.style.height = e.target.scrollHeight + 'px'
}

// 2. 백엔드 연동 로직
onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await axios.get(`http://127.0.0.1:8000/community/${route.params.id}/`)
      form.value.title = data.title
      form.value.category = data.category
      form.value.content = data.content
      // 수정 시 기존 이미지가 있다면 미리보기에만 넣어둠
      if (data.image) imagePreview.value = data.image
    } catch (err) {
      alert('데이터를 가져오는데 실패했습니다.')
    }
  }
})

// 컴포넌트 종료 시 메모리 해제
onUnmounted(() => {
  if (imagePreview.value && !imagePreview.value.startsWith('http')) {
    URL.revokeObjectURL(imagePreview.value)
  }
})

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    // 이전 미리보기 메모리 해제
    if (imagePreview.value && !imagePreview.value.startsWith('http')) {
      URL.revokeObjectURL(imagePreview.value)
    }
    form.value.image = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

const removeImage = () => {
  form.value.image = null
  imagePreview.value = null
}

const handleSubmit = async () => {
  // 실제 백엔드 전송을 위한 FormData 객체 생성 (이미지 포함 시 필수)
  const formData = new FormData()
  formData.append('title', form.value.title)
  formData.append('category', form.value.category)
  formData.append('content', form.value.content)
  // 이미지가 '파일' 객체일 때만(새로 업로드했을 때만) 전송
  if (form.value.image instanceof File) {
    formData.append('image', form.value.image)
  }

  try {
    const config = {
      headers: { 
        Authorization: `Token ${accountStore.token}`,
        'Content-Type': 'multipart/form-data' // FormData 전송 시 명시
    }
  }
    
    if (isEdit.value) {
      await axios.put(`http://127.0.0.1:8000/community/${route.params.id}/`, formData, config)
    } else {
      await axios.post(`http://127.0.0.1:8000/community/`, formData, config)
    }
    
    router.push({ name: 'Community' })
  } catch (err) {
    alert('저장 중 오류가 발생했습니다.')
  }
}

// isValid 계산식을 더 안전하게 변경
const isValid = computed(() => {
  const titleOk = form.value.title && form.value.title.trim().length > 0
  const contentOk = form.value.content && form.value.content.trim().length > 0
  return !!(titleOk && contentOk)
})
</script>

<style scoped>
.form-wrapper { max-width: 850px; margin: 0 auto; padding: 40px 20px; }

/* 카테고리 탭 */
.form-tabs { display: flex; border-bottom: 1px solid #e5e8eb; margin-bottom: 24px; }
.tab-item {
  padding: 12px 20px; border: none; background: none; font-size: 16px;
  color: #8b95a1; cursor: pointer; position: relative;
}
.tab-item.active { color: #191f28; font-weight: 700; }
.tab-item.active::after {
  content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 2px; background: #00ad7c;
}

/* 가이드 박스 */
.guide-box {
  display: flex; align-items: center; gap: 10px; background: #f2fcf9;
  color: #00ad7c; padding: 14px 20px; border-radius: 8px; margin-bottom: 32px; font-size: 14px;
}

/* 에디터 본문 */
.editor-title {
  width: 100%; border: none; outline: none; font-size: 32px; font-weight: 700;
  color: #191f28; margin-bottom: 20px;
}
.editor-title::placeholder { color: #adb5bd; }

.editor-content {
  width: 100%; min-height: 400px; border: 1px solid #e5e8eb; border-radius: 8px;
  padding: 20px; outline: none; font-size: 16px; line-height: 1.8; resize: none;
}

/* 이미지 업로드 영역 */
.image-upload-area { margin-bottom: 24px; }
.image-label {
  display: flex; align-items: center; justify-content: center; width: 100%; height: 200px;
  border: 1px solid #e5e8eb; border-radius: 8px; cursor: pointer; background: #fafafa; overflow: hidden;
}
.image-label.has-image { border: none; }
.preview-img { width: 100%; height: 100%; object-fit: cover; }
.upload-content { display: flex; flex-direction: column; align-items: center; color: #8b95a1; gap: 8px; }
.cam-icon { font-size: 24px; }
.remove-btn { margin-top: 8px; background: none; border: none; color: #f03e3e; font-size: 14px; cursor: pointer; }

/* 하단 액션 버튼 */
.form-actions {
  display: flex; justify-content: flex-end; gap: 12px; margin-top: 32px;
  padding-top: 24px; border-top: 1px solid #f2f4f6;
}
.toss-btn-primary {
  background: #00ad7c; color: #fff; border: none; padding: 12px 32px;
  border-radius: 8px; font-weight: 700; cursor: pointer;
}
.toss-btn-sub {
  background: #f2f4f6; color: #4e5968; border: none; padding: 12px 32px;
  border-radius: 8px; font-weight: 700; cursor: pointer;
}
.toss-btn-primary:disabled { background: #e5e8eb; cursor: default; }
</style>