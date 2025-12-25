<template>
  <div class="step-content">
    <div class="nlp-header">
      <div class="icon-circle">💬</div>
      <h1 class="toss-title">
        더 구체적인 <br />
        조건이 있으신가요?
      </h1>
      <p class="toss-desc">
        "금리가 낮아도 우대 조건이 쉬운 곳", "국민은행 상품만 보여줘" 등 
        자유롭게 입력하시면 AI가 결과를 조정합니다.
      </p>
    </div>

    <div class="input-area">
      <textarea 
        v-model="inputText"
        placeholder="예: 월 납입 한도가 높았으면 좋겠어"
        class="toss-textarea"
      ></textarea>
    </div>

    <div class="button-group">
      <button class="btn-secondary" v-on:click="$emit('next', { text: '' })">건너뛰기</button>
      <button class="btn-primary" v-on:click="$emit('next', { text: inputText })">입력 완료</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['next'])
const inputText = ref('')
</script>

<style scoped>
.step-content {
  animation: fadeIn 0.5s ease-out;
  padding-bottom: 100px;
}

.nlp-header {
  margin-bottom: 32px;
}

.icon-circle {
  font-size: 40px;
  margin-bottom: 20px;
}

.toss-title {
  font-size: 26px;
  font-weight: 700;
  line-height: 1.4;
  color: #191f28;
  margin-bottom: 12px;
}

.toss-desc {
  font-size: 15px;
  line-height: 1.6;
  color: #4e5968;
}

.input-area {
  margin-top: 24px;
}

.toss-textarea {
  width: 100%;
  height: 180px;
  padding: 20px;
  border-radius: 20px;
  background-color: #f2f4f6;
  border: 2px solid transparent;
  font-size: 16px;
  line-height: 1.6;
  color: #191f28;
  resize: none;
  transition: all 0.2s;
}

.toss-textarea:focus {
  outline: none;
  border-color: #3182f6;
  background-color: #ffffff;
}

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  width: 100%;
}

.btn-primary, .btn-secondary {
  flex: 1;
  padding: 14px 16px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-primary, .btn-secondary {
  flex: 1;
  padding: 18px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background-color: #3182f6;
  color: #ffffff;
}

.btn-secondary {
  background-color: #f2f4f6;
  color: #4e5968;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>