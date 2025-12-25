<script setup>
// 필요한 로직이 있다면 여기에 추가하세요.
</script>

<template>
  <main>
    <!-- Feature Section -->
    <section class="bg-white py-24 sm:py-32">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-lg font-bold leading-8 text-yellow-500">머니:비 핵심 기능</h2>
          <p class="mt-2 text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            금융 생활의 새로운 기준
          </p>
          <p class="mt-6 text-lg leading-8 text-gray-600">
            안전하고 스마트한 자산 관리를 경험하세요. 당신의 데이터를 기반으로 최적의 솔루션을 제공합니다.
          </p>
        </div>

        <div class="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <div class="grid grid-cols-1 gap-x-8 gap-y-16 lg:grid-cols-3">
            <!-- Feature 1 -->
            <div class="group relative flex flex-col items-center text-center p-8 rounded-3xl bg-slate-50 hover:bg-white hover:shadow-2xl transition-all duration-500 border border-transparent hover:border-yellow-100">
              <div class="mb-8 relative">
                <div class="absolute inset-0 bg-yellow-400 blur-2xl opacity-10 group-hover:opacity-30 transition-opacity"></div>
                <div class="hexagon-shape bg-white shadow-lg relative z-10 group-hover:-translate-y-2 transition-transform duration-300">
                  <span class="material-symbols-outlined text-4xl text-yellow-500">pie_chart</span>
                </div>
              </div>
              <h3 class="text-xl font-bold leading-7 text-gray-900 group-hover:text-yellow-600 transition-colors">개인 맞춤형 포트폴리오</h3>
              <p class="mt-4 text-base leading-7 text-gray-500 text-balance">
                AI 알고리즘이 소비 패턴과 투자 성향을 분석하여, 나에게 딱 맞는 1:1 맞춤 금융 포트폴리오를 제안합니다.
              </p>
            </div>

            <!-- Feature 2 -->
            <div class="group relative flex flex-col items-center text-center p-8 rounded-3xl bg-slate-50 hover:bg-white hover:shadow-2xl transition-all duration-500 border border-transparent hover:border-yellow-100">
              <div class="mb-8 relative">
                <div class="absolute inset-0 bg-yellow-400 blur-2xl opacity-10 group-hover:opacity-30 transition-opacity"></div>
                <div class="hexagon-shape bg-white shadow-lg relative z-10 group-hover:-translate-y-2 transition-transform duration-300">
                  <span class="material-symbols-outlined text-4xl text-yellow-500">monitoring</span>
                </div>
              </div>
              <h3 class="text-xl font-bold leading-7 text-gray-900 group-hover:text-yellow-600 transition-colors">실시간 자산 분석</h3>
              <p class="mt-4 text-base leading-7 text-gray-500 text-balance">
                은행, 증권, 보험 등 흩어진 모든 자산을 한 화면에서 확인하세요. 실시간 변동 내역을 놓치지 않고 알려드립니다.
              </p>
            </div>

            <!-- Feature 3 -->
            <div class="group relative flex flex-col items-center text-center p-8 rounded-3xl bg-slate-50 hover:bg-white hover:shadow-2xl transition-all duration-500 border border-transparent hover:border-yellow-100">
              <div class="mb-8 relative">
                <div class="absolute inset-0 bg-yellow-400 blur-2xl opacity-10 group-hover:opacity-30 transition-opacity"></div>
                <div class="hexagon-shape bg-white shadow-lg relative z-10 group-hover:-translate-y-2 transition-transform duration-300">
                  <span class="material-symbols-outlined text-4xl text-yellow-500">shield_lock</span>
                </div>
              </div>
              <h3 class="text-xl font-bold leading-7 text-gray-900 group-hover:text-yellow-600 transition-colors">안전한 데이터 보안</h3>
              <p class="mt-4 text-base leading-7 text-gray-500 text-balance">
                금융권 수준의 철저한 보안 시스템으로 당신의 소중한 정보를 24시간 안전하게 보호합니다. 안심하고 사용하세요.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How it Works Section -->
    <section class="relative bg-slate-50 py-24 sm:py-32 overflow-hidden">
      <div class="absolute -top-40 -left-40 h-[500px] w-[500px] rounded-full bg-yellow-400/10 blur-3xl pointer-events-none"></div>
      
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="mb-16 md:text-center">
          <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">이용 방법</h2>
          <p class="mt-4 text-lg text-gray-600 font-medium">단 3단계면 충분합니다. 지금 바로 시작해보세요.</p>
        </div>

        <div class="relative">
          <!-- Connecting Line for Desktop -->
          <div aria-hidden="true" class="absolute left-0 top-12 hidden h-1 w-full -translate-y-1/2 bg-yellow-100 lg:block"></div>
          
          <div class="grid grid-cols-1 gap-12 lg:grid-cols-3 lg:gap-8">
            <!-- Step 1 -->
            <div class="relative flex flex-col items-center">
              <div class="relative z-10 flex h-24 w-24 items-center justify-center rounded-[2rem] bg-white shadow-xl ring-4 ring-yellow-50">
                <span class="material-symbols-outlined text-4xl text-yellow-500">account_balance_wallet</span>
                <div class="absolute -right-2 -top-2 h-9 w-9 rounded-2xl bg-yellow-400 flex items-center justify-center text-sm font-black text-slate-900 shadow-lg shadow-yellow-200">1</div>
              </div>
              <div class="mt-8 text-center">
                <h3 class="text-xl font-bold text-gray-900">계좌 연동</h3>
                <p class="mt-3 text-sm text-gray-500 leading-relaxed font-medium">간편 인증을 통해 보유하고 계신<br/>은행, 증권 계좌를 한 번에 연동하세요.</p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="relative flex flex-col items-center">
              <div class="relative z-10 flex h-24 w-24 items-center justify-center rounded-[2rem] bg-white shadow-xl ring-4 ring-yellow-50">
                <span class="material-symbols-outlined text-4xl text-yellow-500">psychology</span>
                <div class="absolute -right-2 -top-2 h-9 w-9 rounded-2xl bg-yellow-400 flex items-center justify-center text-sm font-black text-slate-900 shadow-lg shadow-yellow-200">2</div>
              </div>
              <div class="mt-8 text-center">
                <h3 class="text-xl font-bold text-gray-900">성향 분석</h3>
                <p class="mt-3 text-sm text-gray-500 leading-relaxed font-medium">간단한 설문을 통해 당신의<br/>투자 성향과 소비 패턴을 분석합니다.</p>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="relative flex flex-col items-center">
              <div class="relative z-10 flex h-24 w-24 items-center justify-center rounded-[2rem] bg-white shadow-xl ring-4 ring-yellow-50">
                <span class="material-symbols-outlined text-4xl text-yellow-500">lightbulb</span>
                <div class="absolute -right-2 -top-2 h-9 w-9 rounded-2xl bg-yellow-400 flex items-center justify-center text-sm font-black text-slate-900 shadow-lg shadow-yellow-200">3</div>
              </div>
              <div class="mt-8 text-center">
                <h3 class="text-xl font-bold text-gray-900">솔루션 받기</h3>
                <p class="mt-3 text-sm text-gray-500 leading-relaxed font-medium">분석 결과를 바탕으로 AI가 제안하는<br/>최적의 자산 관리 솔루션을 확인하세요.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-indigo-400 py-20 sm:py-28 relative overflow-hidden">
      <!-- Decorative background -->
      <div class="absolute inset-0 opacity-20" style="background-image: radial-gradient(#000000 1px, transparent 1px); background-size: 32px 32px;"></div>
      <div class="absolute right-0 top-0 h-96 w-96 translate-x-1/3 -translate-y-1/3 rounded-full bg-white/30 blur-3xl"></div>
      
      <div class="relative mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
        <h2 class="text-3xl font-black tracking-tight text-slate-900 sm:text-5xl">
          지금 바로 내 자산의 균형을 찾아보세요
        </h2>
        <p class="mx-auto mt-6 max-w-2xl text-lg text-slate-800 font-bold">
          머니:비와 함께라면 복잡한 금융이 놀랍도록 쉬워집니다.
        </p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.hexagon-shape {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
  margin: 0 auto;
}

@media (max-width: 1024px) {
  [aria-hidden="true"] {
    display: none;
  }
}
</style>