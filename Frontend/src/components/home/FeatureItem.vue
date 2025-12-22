<template>
  <section class="feature-section">
    <div class="max-w-[1100px] mx-auto px-5">
      <h2 class="section-title">Money:B는 이렇게 추천해요</h2>
      
      <div class="process-grid">
        <div class="process-card">
          <div class="icon-circle bg-blue-light">
            <span class="material-symbols-outlined text-blue">person_search</span>
          </div>
          <h3>1. 페르소나 분석</h3>
          <p>
            간단한 설문을 통해 당신의 소비 습관과 투자 성향을 분석하고, 
            맞춤 금융 페르소나를 도출합니다.
          </p>
        </div>

        <div class="process-card">
          <div class="icon-circle bg-purple-light">
            <span class="material-symbols-outlined text-purple">database</span>
          </div>
          <h3>2. 실시간 상품 비교</h3>
          <p>
            시중에 나와 있는 은행별 예적금 상품의 금리와 조건을 
            실시간으로 수집하고 대조합니다.
          </p>
        </div>

        <div class="process-card">
          <div class="icon-circle bg-green-light">
            <span class="material-symbols-outlined text-green">verified</span>
          </div>
          <h3>3. 최적의 Top 3 제안</h3>
          <p>
            복잡한 조건과 서류 없이, 당신의 페르소나에 가장 큰 이득을 줄 
            수 있는 상품 3가지를 엄선하여 제안해 드립니다.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// 스크립트 로직은 현재 필요 없음
</script>

<style scoped>
/* 서비스 설명 섹션 */
.feature-section {
  padding: 100px 0;
  background-color: #fcfcfc; /* 배경색 살짝 변경 */
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 60px;
  color: #191f28;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.process-card {
  padding: 40px;
  background: #ffffff; /* 카드 배경은 흰색으로 */
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); /* 은은한 그림자 */
  transition: all 0.3s;
  text-align: center; /* 카드 내용 중앙 정렬 */
}

.process-card:hover {
  transform: translateY(-5px); /* 호버 시 살짝 떠오르는 효과 */
  box-shadow: 0 15px 40px rgba(0,0,0,0.08);
}

.icon-circle {
  width: 60px; /* 아이콘 크기 약간 키움 */
  height: 60px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px auto; /* 중앙 정렬 */
  font-size: 28px; /* 아이콘 자체 크기 */
}

.bg-blue-light { background-color: #e8f3ff; color: #3182f6; } /* 아이콘 컬러도 설정 */
.bg-purple-light { background-color: #f2f0ff; color: #8657f2; }
.bg-green-light { background-color: #e7f9ed; color: #21b66b; }

.process-card h3 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
  color: #333d4b;
}

.process-card p {
  font-size: 15px;
  color: #6b7684;
  line-height: 1.6;
}

/* 반응형 처리 */
@media (max-width: 768px) {
  .process-grid { grid-template-columns: 1fr; }
  .section-title { font-size: 28px; margin-bottom: 40px; }
  .process-card { padding: 30px; }
}
</style>