<template>
  <div class="mypage-container">
    <section class="profile-section">
      <div class="card profile-card">
        <div v-if="!isEditMode" class="profile-card-inner">
          <div class="profile-header">
            <div class="profile-avatar">
              <div class="avatar-bg">
                <span class="avatar-text">{{ accountStore.user?.nickname?.[0] || 'G' }}</span>
              </div>
            </div>
            <div class="profile-info">
              <div class="name-edit-group">
                <h2 class="user-name">
                  {{ accountStore.user?.nickname || '사용자' }}님
                  <span @click="openEditMode" class="edit-text-link">내 정보 수정</span>
                </h2>
              </div>
              <p class="user-email">{{ accountStore.user?.email }}</p>
              <div class="tag-group">
                <span v-if="accountStore.financial_profile?.cluster_name" class="tag">#{{ accountStore.financial_profile.cluster_name }}</span>
                <span v-if="accountStore.financial_profile?.annual_income_amt" class="tag">#연소득_{{ (accountStore.financial_profile.annual_income_amt / 10000).toLocaleString() }}만</span>
                <span v-if="accountStore.user?.is_mydata_linked" class="tag" style="background: #E7F9F3; color: #00B06B;">#마이데이터_연동중</span>
              </div>
            </div>
          </div>
          <div class="profile-footer">
            <button v-if="recommendationStore.recommendations?.length == 0 && !accountStore.user?.is_mydata_agreed" @click="goToReDiagnostic" class="btn-secondary-full">투자 성향 진단</button>
            <button v-else @click="goToReDiagnostic" class="btn-secondary-full">투자 성향 재진단</button>
          </div>
        </div>

        <div v-else class="edit-mode-container">
          <h3 class="edit-title">내 정보 수정</h3>
          <div class="edit-form">
            <div class="input-item">
              <label>닉네임</label>
              <input v-model="editData.nickname" class="custom-input" placeholder="새 닉네임" />
            </div>
            <div class="input-item">
              <label>새 비밀번호</label>
              <input v-model="editData.password1" type="password" class="custom-input" placeholder="8자 이상 입력" />
            </div>
            <div class="input-item">
              <label>비밀번호 확인</label>
              <input v-model="editData.password2" type="password" class="custom-input" placeholder="다시 입력" />
              <p v-if="passwordError" class="error-text">{{ passwordError }}</p>
            </div>

            <div class="edit-actions" style="margin-top: 20px; display: flex; gap: 8px;">
              <button @click="updateFullProfile" class="btn-primary-small" style="background: #3182F6; color: white; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 600; cursor: pointer;">저장</button>
              <button @click="closeEditMode" class="btn-ghost-small" style="background: #F2F4F6; color: #4E5968; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 600; cursor: pointer;">취소</button>
            </div>
          </div>
        </div>
      </div>

      <div class="card persona-card">
        <div class="persona-content">
          <div class="persona-status-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
            <div class="persona-label" style="font-size: 13px; font-weight: 600; color: #3182F6; background: #E8F3FF; padding: 4px 12px; border-radius: 20px;">AI 분석 리포트</div>
            <div class="persona-status" style="font-size: 13px; color: #8B95A1;">
              <span class="status-dot" :class="{ active: accountStore.user?.is_mydata_linked }"></span>
              {{ accountStore.user?.is_mydata_linked ? '마이데이터 연동' : '데이터 미연동' }}
            </div>
          </div>

          <div class="persona-main" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 180px; text-align: center;">
            <template v-if="recommendationStore.persona">
              <div class="persona-icon" style="font-size: 56px; margin-bottom: 12px; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));">
                {{ recommendationStore.persona.icon }}
              </div>
              <h4 style="font-size: 22px; font-weight: 800; color: #191F28; margin-bottom: 8px;">
                {{ recommendationStore.persona.name }}
              </h4>
              <p style="font-size: 15px; color: #4E5968; line-height: 1.6; word-break: keep-all; padding: 0 10px; margin-bottom: 20px;">
                {{ recommendationStore.persona.description }}
              </p>
              
              <div class="financial-summary" style="display: flex; gap: 12px; width: 100%; justify-content: center; border-top: 1px solid #F2F4F6; pt: 20px; margin-top: 10px; padding-top: 20px;">
                <div class="summary-item">
                  <p style="font-size: 12px; color: #8B95A1; margin-bottom: 4px;">총 투자자산</p>
                  <p style="font-size: 14px; font-weight: 700;">{{ (accountStore.financial_profile?.invest_eval_amt / 100000000).toFixed(1) }}억+</p>
                </div>
                <div style="width: 1px; background: #F2F4F6;"></div>
                <div class="summary-item">
                  <p style="font-size: 12px; color: #8B95A1; margin-bottom: 4px;">소비율</p>
                  <p style="font-size: 14px; font-weight: 700; color: #F04452;">{{ (accountStore.financial_profile?.expense_to_income_ratio * 100).toFixed(1) }}%</p>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="empty-persona" style="color: #8B95A1;">
                <div style="font-size: 40px; margin-bottom: 12px; opacity: 0.5;">🔍</div>
                <p style="font-size: 14px; line-height: 1.5;">사용자님의 투자 성향을 분석 중입니다.<br/>진단을 완료해주세요.</p>
              </div>
            </template>
          </div>
        </div>
      </div>
    </section>

    <section v-if="recommendationStore.recommendations?.length > 0" class="recommend-section">
      <div class="section-title-group">
        <h3>머니:비가 찾은 <span class="highlight-text" style="color: #3182F6;">꿀단지 TOP 3</span></h3>
        <p class="subtitle">사용자님의 투자 데이터와 성향을 교차 분석한 결과입니다.</p>
      </div>
      <div class="recommend-grid">
        <div 
          v-for="(item, index) in recommendationStore.recommendations.slice(0, 3)" 
          :key="item.id" 
          class="recommend-card clickable-card"
          :class="{ 'best-pick': index === 0 }"
          @click="goOptionApply(item.id)"
        >
          <span v-if="index === 0" class="badge-best">AI BEST</span>
          <div class="card-header-info" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
             <span class="rank-num" style="font-size: 24px; font-weight: 800; color: #E5E8EB;">0{{ index + 1 }}</span>
             <span class="save-term" style="font-size: 12px; background: #F2F4F6; padding: 4px 8px; border-radius: 6px; color: #4E5968;">{{ item.save_trm }}개월·{{ item.intr_rate_type_nm }}</span>
          </div>
          
          <p class="bank-name" style="font-size: 13px; color: #8B95A1; margin-bottom: 4px; text-align: left;">{{ item.kor_co_nm }}</p>
          <h4 class="product-name" style="font-size: 17px; font-weight: 700; color: #191F28; text-align: left; margin-bottom: 16px; height: 48px; line-height: 1.4; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{{ item.fin_prdt_nm }}</h4>
          
          <div class="rate-display" style="background: #F9FAFB; border-radius: 12px; padding: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: left;">
              <span style="font-size: 11px; color: #8B95A1; display: block;">최고 금리</span>
              <span class="rate-value" style="font-size: 20px; font-weight: 800; color: #3182F6;">{{ item.intr_rate2 }}%</span>
            </div>
            <div style="text-align: right;">
              <span style="font-size: 11px; color: #8B95A1; display: block;">기본</span>
              <span style="font-size: 14px; font-weight: 600; color: #4E5968;">{{ item.intr_rate }}%</span>
            </div>
          </div>

          <p class="recommend-reason" style="font-size: 13px; color: #4E5968; text-align: left; line-height: 1.5; height: 60px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
            {{ item.ai_analysis?.reason || '사용자님의 성향과 자산 현황을 고려했을 때 가장 높은 수익률이 기대되는 상품입니다.' }}
          </p>
          
          <div class="hover-guide" style="margin-top: 16px; font-size: 13px; font-weight: 600; color: #3182F6; text-align: right;">자세히 보기 ❯</div>
        </div>
      </div>
    </section>

    <section class="subscribed-section">
      <div class="card list-card">
        <div class="card-header">
          <h3>내가 가입한 상품 <span class="count-badge">{{ productStore.subscriptions?.length || 0 }}</span></h3>
        </div>
        <div v-if="productStore.subscriptions?.length > 0" class="list-table">
          <div class="list-thead">
            <span class="th">상품정보</span>
            <span class="th text-center">은행</span>
            <span class="th text-center">금리</span>
            <span class="th text-center">잔액</span>
          </div>
          <div class="list-tbody">
            <div 
              v-for="sub in productStore.subscriptions" 
              :key="sub.id" 
              class="product-row clickable-row"
              @click="goToDetail(sub.id)"
            >
              <div class="td info">
                <div class="bank-avatar"><span class="avatar-text">{{ sub.product_name[0] }}</span></div>
                <strong class="product-name">{{ sub.product_name }}</strong>
              </div>
              <div class="td text-center text-secondary">{{ sub.bank_name }}</div>
              <div class="td text-center text-point">{{ sub.intr_rate2 }}%</div>
              <div class="td text-center font-bold">₩{{ sub.amount.toLocaleString() }}</div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>아직 가입한 금융 상품이 없어요.</p>
          <router-link to="/products" class="btn-link">상품 보러가기</router-link>
        </div>
      </div>
    </section>

    <section v-show="productStore.subscriptions?.length > 0" class="chart-section">
      <div class="card chart-card">
        <div class="card-header">
          <div class="header-text-group">
            <h3>내 금리 TOP 3 비교 차트</h3>
            <p class="text-tertiary">보유 중인 상품 중 금리가 가장 높은 3개 상품입니다.</p>
          </div>
        </div>
        <div class="chart-container"><canvas id="rateChart"></canvas></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, watch, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useProductStore } from '@/stores/products'
import { useRecommendationStore } from '@/stores/recommendations'
import Chart from 'chart.js/auto'

const router = useRouter()
const accountStore = useAccountStore()
const productStore = useProductStore()
const recommendationStore = useRecommendationStore()

let rateChart = null

const goToDetail = (id) => {
  if (!id) return
  router.push({ name: 'Subscribed', params: { id: id } })
}

const isEditMode = ref(false)
const editData = ref({ 
  nickname: '', 
  password1: '', 
  password2: '',
  is_mydata_linked: false 
})

const passwordError = computed(() => {
  if (editData.value.password1 && editData.value.password1.length < 8) return '비밀번호는 8자 이상이어야 합니다.'
  if (editData.value.password1 !== editData.value.password2 && editData.value.password2 !== '') return '비밀번호가 일치하지 않습니다.'
  return ''
})

const openEditMode = () => {
  editData.value.nickname = accountStore.user?.nickname || ''
  editData.value.is_mydata_linked = accountStore.user?.is_mydata_linked || false 
  editData.value.password1 = ''
  editData.value.password2 = ''
  isEditMode.value = true
}

const closeEditMode = () => { isEditMode.value = false }

const updateFullProfile = async () => {
  if (passwordError.value) return alert(passwordError.value)
  const payload = { 
    nickname: editData.value.nickname,
  }
  if (editData.value.password1) payload.password = editData.value.password1
  if (await accountStore.updateProfile(payload)) {
    closeEditMode()
  }
}

const goToReDiagnostic = () => {
  router.push({ name: 'Recommendations', query: { step: 'survey' } })
}

const goOptionApply = (id) => {
  if (id) router.push({ name: 'Subscribe', params: { id: id } })
}

const renderChart = () => {
  const ctx = document.getElementById('rateChart')
  if (!ctx || !productStore.subscriptions?.length) return
  
  const topThreeSubscriptions = [...productStore.subscriptions]
    .sort((a, b) => b.intr_rate2 - a.intr_rate2)
    .slice(0, 3)

  if (rateChart) rateChart.destroy()
  rateChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: topThreeSubscriptions.map(s => s.product_name),
      datasets: [
        { label: '기본 금리 (%)', data: topThreeSubscriptions.map(s => s.intr_rate), backgroundColor: 'rgba(49, 130, 246, 0.4)', borderRadius: 8 },
        { label: '우대 금리 (%)', data: topThreeSubscriptions.map(s => s.intr_rate2), backgroundColor: '#3182F6', borderRadius: 8 }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: true, position: 'bottom', labels: { usePointStyle: true, boxWidth: 6 } } },
      scales: { y: { beginAtZero: true, grid: { color: '#F2F4F6' } }, x: { grid: { display: false } } }
    }
  })
}

onMounted(async () => {
  await Promise.all([
    productStore.getSubscriptions(),
    accountStore.getFinancialProfile()
  ])
  if (recommendationStore.recommendations?.length == 0 && accountStore.user?.is_mydata_linked){
    await recommendationStore.getRecommendations()
  }
  renderChart()
})

watch(() => productStore.subscriptions, renderChart, { deep: true })
</script>

<style scoped>
.mypage-container { max-width: 1100px; margin: 0 auto; padding: 48px 24px; background-color: #F9FAFB; display: flex; flex-direction: column; gap: 32px; font-family: 'Pretendard', sans-serif; color: #191F28; }
.card { background: #FFFFFF; border-radius: 28px; padding: 32px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.02); }

.profile-card { 
  display: flex; 
  flex-direction: column; 
  justify-content: center;
  min-height: 300px;
}
.profile-card-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: space-between;
}
.profile-header { display: flex; gap: 24px; align-items: center; margin-bottom: 32px; }

.profile-section { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.avatar-bg { width: 80px; height: 80px; background: #F2F4F6; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #3182F6; font-size: 32px; font-weight: bold; }

.user-name { font-size: 26px; font-weight: 700; display: flex; align-items: baseline; gap: 8px; }
.edit-text-link { font-size: 13px; font-weight: 500; color: #8B95A1; cursor: pointer; text-decoration: underline; text-underline-offset: 2px; }
.edit-text-link:hover { color: #4E5968; }

.user-email { color: #8B95A1; font-size: 15px; margin-top: 4px; }
.tag-group { display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }
.tag { background: #E8F3FF; color: #3182F6; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; }
.btn-secondary-full { width: 100%; padding: 18px; border-radius: 16px; border: none; background: #3182F6; color: white; font-weight: 700; font-size: 16px; cursor: pointer; transition: 0.2s; }
.btn-secondary-full:hover { background: #1B64DA; transform: translateY(-2px); }
.custom-input { padding: 14px 18px; border-radius: 14px; border: 1px solid #E5E8EB; background-color: #F9FAFB; font-size: 15px; outline: none; transition: 0.2s; width: 100%; box-sizing: border-box; }
.custom-input:focus { border-color: #3182F6; background-color: #fff; }
.input-item { display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }
.input-item label { font-size: 14px; font-weight: 600; color: #4E5968; }
.error-text { color: #F04452; font-size: 12px; margin-top: 4px; }

.recommend-section .subtitle { color: #8B95A1; margin-top: 4px; font-size: 15px; }
.recommend-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 24px; }
.recommend-card { background: #fff; border-radius: 24px; padding: 24px; border: 1px solid #F2F4F6; transition: 0.3s; position: relative; cursor: pointer; }
.recommend-card:hover { transform: translateY(-8px); border-color: #3182F6; box-shadow: 0 12px 32px rgba(49, 130, 246, 0.08); }
.recommend-card.best-pick { border-color: #3182F6; background: linear-gradient(180deg, #FFFFFF 0%, #F0F7FF 100%); }
.badge-best { position: absolute; top: -12px; left: 24px; background: #3182F6; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; }

.list-table { margin-top: 16px; }
.list-thead, .product-row { display: grid; grid-template-columns: 2fr 1fr 1fr 1.2fr; align-items: center; padding: 20px 0; gap: 12px; }
.list-thead { border-bottom: 1px solid #F2F4F6; }
.th { font-size: 14px; color: #8B95A1; font-weight: 500; }
.product-row { border-radius: 16px; cursor: pointer; transition: 0.2s; }
.product-row:hover { background-color: #F9FAFB; padding-left: 12px; padding-right: 12px; }
.bank-avatar { width: 40px; height: 40px; background: #F2F4F6; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 14px; color: #3182F6; font-weight: 700; }
.td { text-align: center; }
.td.info { display: flex; align-items: center; justify-content: flex-start; text-align: left; }
.text-point { color: #3182F6; font-weight: 700; }
.count-badge { background: #E8F3FF; color: #3182F6; padding: 2px 10px; border-radius: 12px; font-size: 14px; }
.chart-container { height: 320px; margin-top: 24px; }
.empty-state { text-align: center; padding: 64px 0; color: #8B95A1; }
.btn-link { color: #3182F6; text-decoration: none; font-weight: 600; margin-top: 12px; display: inline-block; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #E5E8EB; display: inline-block; margin-right: 8px; }
.status-dot.active { background: #3182F6; box-shadow: 0 0 8px rgba(49,130,246,0.4); }

@media (max-width: 900px) {
  .profile-section { grid-template-columns: 1fr; }
  .recommend-grid { grid-template-columns: 1fr; }
  .list-thead, .product-row { grid-template-columns: 1.5fr 1fr 1fr; }
  .th:nth-child(4), .td:nth-child(4) { display: none; }
}
</style>