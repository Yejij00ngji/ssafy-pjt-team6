<template>
  <div class="search-bar-wrapper">
    <div class="search-container">

      <input 
        type="text" 
        class="search-input" 
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        @keyup.enter="$emit('search')"
      />

      <button class="search-submit-btn" @click="$emit('search')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  placeholder: {
    type: String,
    default: '지금 궁금한 주제를 검색해보세요'
  }
})
defineEmits(['update:modelValue', 'search'])
</script>

<style scoped>
.search-bar-wrapper {
  margin-bottom: 40px;
  display: flex;
  justify-content: center;
  width: 100%;
}

.search-container {
  display: flex;
  align-items: center;
  background-color: #fff;
  padding: 8px 10px 8px 28px; /* 우측 버튼 여백 조절 */
  border-radius: 50px; /* 완전한 캡슐형 */
  width: 100%;
  max-width: 640px;
  height: 64px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); /* 부드러운 그림자 */
  border: 1px solid #e5e8eb;
  transition: all 0.2s ease;
}

.search-container:focus-within {
  border-color: #3182f6; /* 인프런 그린 컬러 포인트 */
  box-shadow: 0 6px 20px rgba(0, 173, 124, 0.12);
}

/* 왼쪽 영역 스타일 */
.search-left {
  display: flex;
  align-items: center;
  gap: 6px;
  padding-right: 16px;
  border-right: 1px solid #f2f4f6;
  margin-right: 16px;
  cursor: pointer;
}

.category-icon {
  width: 36px;
  height: 36px;
  background-color: #f2f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.dropdown-arrow {
  font-size: 10px;
  color: #8b95a1;
}

/* 입력창 스타일 */
.search-input {
  flex: 1;
  border: none;
  background: none;
  outline: none;
  font-size: 17px;
  font-weight: 500;
  color: #191f28;
}

.search-input::placeholder {
  color: #adb5bd;
}

/* 우측 원형 검색 버튼 */
.search-submit-btn {
  width: 48px;
  height: 48px;
  background-color: #3182f6; /* 강조색: 파란색 */
  border: none;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
}

.search-submit-btn:hover {
  background-color: #3182f6;
  transform: scale(1.05);
}

.search-submit-btn:active {
  transform: scale(0.95);
}

@media (max-width: 480px) {
  .search-container {
    height: 56px;
  }
  .search-left {
    display: none; /* 모바일에서는 간소화 */
  }
}
</style>