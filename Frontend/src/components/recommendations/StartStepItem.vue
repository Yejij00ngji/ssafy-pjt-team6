<template>
  <div class="step-container">
    <div class="content-box">
      <div class="icon-header">💎</div>
      <h1 class="main-title">
        나에게 딱 맞는 예적금,<br />
        어떤 방식으로 찾을까요?
      </h1>
      <p class="description">
        마이데이터를 연결하면 흩어진 자산을 분석해<br />
        가장 높은 금리 혜택을 찾아드려요.
      </p>
    </div>

    <div class="button-group">
      <button class="btn-myData" @click="$emit('next', { agreed: true })">
        <div class="btn-content">
          <span class="bolt">⚡️</span>
          <div class="text">
            <span class="top-text">가장 빠르고 정확한</span>
            <span class="bottom-text">마이데이터로 시작하기</span>
          </div>
        </div>
      </button>

      <button class="btn-manual" @click="$emit('next', { agreed: false })">
        직접 입력해서 추천받기
      </button>
    </div>

    <p class="footer-info">개인정보는 암호화되어 안전하게 보호됩니다.</p>
  </div>
</template>

<style scoped>
.step-container {
  padding: 60px 24px;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.icon-header { font-size: 40px; margin-bottom: 24px; }
.main-title { font-size: 26px; font-weight: 700; line-height: 1.4; color: #191f28; margin-bottom: 16px; }
.description { font-size: 16px; color: #4e5968; line-height: 1.6; }

.button-group { margin-top: auto; display: flex; flex-direction: column; gap: 12px; }

/* 마이데이터 버튼 (Toss Primary 느낌) */
.btn-myData {
  background-color: #00ad7c;
  border: none;
  border-radius: 18px;
  padding: 20px;
  cursor: pointer;
  text-align: left;
}

.btn-content { display: flex; align-items: center; gap: 15px; }
.bolt { font-size: 24px; }
.text { display: flex; flex-direction: column; color: #fff; }
.top-text { font-size: 13px; opacity: 0.9; font-weight: 500; }
.bottom-text { font-size: 18px; font-weight: 700; }

/* 직접 입력 버튼 (Sub 느낌) */
.btn-manual {
  background-color: #f2f4f6;
  color: #4e5968;
  border: none;
  border-radius: 18px;
  padding: 20px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.footer-info {
  text-align: center;
  font-size: 13px;
  color: #adb5bd;
  margin-top: 30px;
}
</style>