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
        <input v-model="form.title" type="text" class="editor-title" placeholder="제목에 핵심 내용을 요약해보세요." />
        
        <div class="image-upload-area">
          <label for="file-input" class="image-label">
            <span v-if="!imagePreview">📸 대표 이미지 추가 (선택)</span>
            <img v-else :src="imagePreview" class="preview-img" />
          </label>
          <input id="file-input" type="file" @change="handleImageUpload" hidden accept="image/*" />
          <button v-if="imagePreview" @click="removeImage" class="remove-btn">삭제</button>
        </div>

        <div class="editor-toolbar">
          <button type="button"><b>B</b></button>
          <button type="button">🔗</button>
          <button type="button" @click="triggerImageUpload">🖼️</button>
        </div>

        <textarea 
          v-model="form.content"
          class="editor-content" 
          :placeholder="currentPlaceholder"
        ></textarea>
      </main>

      <footer class="form-footer">
        <button class="toss-btn-sub" @click="$router.back()">취소</button>
        <button class="toss-btn-primary" :disabled="!isValid" @click="handleSubmit">
          {{ isEdit ? '수정하기' : '등록하기' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
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

// 2. 백엔드 연동 로직
onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await axios.get(`http://127.0.0.1:8000/community/${route.params.id}/`)
      form.value = { ...data }
      if (data.image) imagePreview.value = data.image
    } catch (err) {
      alert('데이터를 가져오는데 실패했습니다.')
    }
  }
})

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
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
  if (form.value.image instanceof File) {
    formData.append('image', form.value.image)
  }

  try {
    const config = {
      headers: { Authorization: `Token ${accountStore.token}` }
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

const isValid = computed(() => form.value.title && form.value.content)
</script>

<style scoped>
.form-wrapper { max-width: 850px; margin: 0 auto; padding-bottom: 100px; }

/* 탭 디자인 */
.form-tabs { display: flex; border-bottom: 1px solid #e5e8eb; margin-bottom: 24px; }
.tab-item {
  padding: 12px 20px; border: none; background: none; font-size: 15px;
  color: #8b95a1; cursor: pointer; position: relative;
}
.tab-item.active { color: #191f28; font-weight: 700; }
.tab-item.active::after {
  content: ''; position: absolute; bottom: 0; left: 0; width: 100%;
  height: 2px; background-color: #00ad7c; /* 인프런 그린 */
}

/* 가이드 박스 */
.guide-box {
  display: flex; align-items: center; gap: 10px;
  background-color: #e7f9f4; color: #00ad7c;
  padding: 14px 20px; border-radius: 8px; margin-bottom: 32px;
  font-size: 14px; font-weight: 600;
}

/* 에디터 스타일 */
.editor-title {
  width: 100%; border: none; outline: none;
  font-size: 32px; font-weight: 700; color: #adb5bd; margin-bottom: 12px;
}
.editor-title:focus { color: #191f28; }

.tag-input {
  width: 100%; border: none; outline: none;
  font-size: 16px; color: #8b95a1; margin-bottom: 24px;
}

.editor-toolbar {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 16px; border: 1px solid #e5e8eb;
  border-radius: 8px 8px 0 0; background: #fafafa;
}
.editor-toolbar button { background: none; border: none; cursor: pointer; color: #4e5968; font-size: 16px; }

.editor-content {
  width: 100%; min-height: 450px; padding: 20px;
  border: 1px solid #e5e8eb; border-top: none;
  border-radius: 0 0 8px 8px; outline: none;
  font-size: 16px; line-height: 1.8; resize: none;
}

/* 하단 버튼 */
.form-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f2f4f6; /* 구분선 추가 */
}

.toss-btn-primary {
  background-color: #00ad7c;
  color: #fff;
  border: none;
  padding: 12px 32px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

.toss-btn-sub {
  background-color: #f2f4f6;
  color: #4e5968;
  border: none;
  padding: 12px 32px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

/* 기존 스타일 유지 + 이미지 업로드 스타일 추가 */
.image-upload-area { margin: 20px 0; position: relative; }
.image-label {
  display: block; width: 100%; height: 150px; border: 2px dashed #e5e8eb;
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; overflow: hidden; color: #8b95a1;
}
.preview-img { width: 100%; height: 100%; object-fit: cover; }
.remove-btn {
  position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5);
  color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer;
}
</style>