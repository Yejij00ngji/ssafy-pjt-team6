<script setup>
import { ref } from 'vue';

// 필요한 경우 Props 정의
defineProps({
  badgeText: {
    type: String,
    default: 'Best Investment 2024'
  }
});
</script>

<template>
  <section class="relative pt-16 pb-20 lg:pt-32 lg:pb-32 overflow-hidden bg-white">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <!-- 컨테이너를 lg:flex-row 및 items-stretch로 설정하여 높이를 맞추고 간격을 조절합니다 -->
      <div class="flex flex-col lg:flex-row items-center justify-between gap-12 lg:gap-16">
        
        <!-- Left Content: 왼쪽 절반 영역 -->
        <div class="flex flex-col gap-6 flex-1 w-full lg:w-1/2 text-center lg:text-left z-10">
          <h1 class="animate-fade-in-up text-4xl lg:text-7xl font-bold leading-[1.1] tracking-tight text-slate-900 text-balance">
            똑똑하게<br/>
            머니를 비교하다<br/>
            <span class="text-blue-600">머니:비</span>
          </h1>
          <p class="animate-fade-in-up delay-100 text-lg lg:text-xl text-slate-500 leading-relaxed text-balance font-medium max-w-xl">
            마이데이터부터 자연어 입력까지,<br class="hidden lg:block"/>
            내 모든 금융 상황을 분석해 최적의 상품을 제안합니다.
          </p>
          <div class="animate-fade-in-up delay-200 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-3 mt-6">
            <RouterLink :to="{ name: 'Recommendations' }" class="w-full sm:w-auto">
              <button class="w-full h-16 px-10 rounded-2xl bg-blue-600 text-white text-lg font-bold hover:bg-blue-700 transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-xl shadow-indigo-200 flex items-center justify-center gap-2">
                내 예/적금 추천 받아보기
                <span class="material-symbols-outlined text-[24px]">arrow_forward</span>
              </button>
            </RouterLink>
          </div>
        </div>

        <!-- Right Visual: 오른쪽 절반 영역 -->
        <div class="flex-1 w-full lg:w-1/2 relative">
          <div class="relative mx-auto w-full max-w-lg lg:max-w-xl perspective-1000 animate-float">
            
            <!-- Abstract Dashboard Card Representation -->
            <div class="relative z-10 overflow-hidden rounded-[2.5rem] bg-white p-8 shadow-[0_32px_64px_-12px_rgba(0,0,0,0.14)] ring-1 ring-gray-900/5">
              <div class="mb-8 flex items-center justify-between">
                <div>
                  <p class="text-sm font-semibold text-gray-400 uppercase tracking-wider">총 자산 현황</p>
                  <p class="text-3xl font-black text-gray-900 mt-1">₩ 124,500,000</p>
                </div>
                <div class="rounded-full bg-emerald-50 px-3 py-1.5 text-sm font-bold text-emerald-600 flex items-center gap-1 border border-emerald-100">
                  <span class="material-symbols-outlined text-[18px]">trending_up</span>
                  +12.5%
                </div>
              </div>

              <!-- Hexagon Graph Simulation -->
              <div class="relative flex h-72 items-center justify-center rounded-3xl bg-slate-50/50 border border-slate-100">
                <svg class="w-56 h-56 drop-shadow-xl" viewBox="0 0 200 200">
                  <!-- Background Hexagon -->
                  <polygon fill="white" points="100,10 180,50 180,140 100,180 20,140 20,50" stroke="#E2E8F0" stroke-width="2"></polygon>
                  <!-- Data Hexagon -->
                  <polygon fill="rgba(79, 70, 229, 0.15)" points="100,30 160,60 150,130 100,160 40,120 40,60" stroke="#4F46E5" stroke-width="3" stroke-linejoin="round"></polygon>
                  <!-- Data Nodes -->
                  <circle cx="100" cy="30" fill="#4F46E5" r="5"></circle>
                  <circle cx="160" cy="60" fill="#4F46E5" r="5"></circle>
                  <circle cx="150" cy="130" fill="#4F46E5" r="5"></circle>
                  <circle cx="100" cy="160" fill="#4F46E5" r="5"></circle>
                  <circle cx="40" cy="120" fill="#4F46E5" r="5"></circle>
                  <circle cx="40" cy="60" fill="#4F46E5" r="5"></circle>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <div class="bg-white/90 backdrop-blur-sm px-4 py-2 rounded-2xl shadow-lg border border-indigo-50">
                    <span class="text-sm font-black text-indigo-600">B-Score 88</span>
                  </div>
                </div>
              </div>

              <div class="mt-8 grid grid-cols-3 gap-6 text-center">
                <div class="p-3 rounded-2xl bg-slate-50">
                  <p class="text-xs font-bold text-gray-400">투자</p>
                  <p class="text-lg font-bold text-gray-900 mt-1">45%</p>
                </div>
                <div class="p-3 rounded-2xl bg-slate-50">
                  <p class="text-xs font-bold text-gray-400">저축</p>
                  <p class="text-lg font-bold text-gray-900 mt-1">30%</p>
                </div>
                <div class="p-3 rounded-2xl bg-slate-50">
                  <p class="text-xs font-bold text-gray-400">소비</p>
                  <p class="text-lg font-bold text-gray-900 mt-1">25%</p>
                </div>
              </div>
            </div>

            <!-- Floating decorative elements -->
            <div class="absolute -right-6 -top-6 h-28 w-28 rounded-[2rem] bg-gradient-to-br from-orange-400 to-rose-500 p-4 shadow-xl flex items-center justify-center text-white transform rotate-12 z-0">
              <div class="flex flex-col items-center">
                <span class="material-symbols-outlined text-4xl">flight</span>
                <span class="text-xs font-black mt-1">YOLO</span>
              </div>
            </div>

            <!-- Floating Badge -->
            <div class="absolute -bottom-8 right-10 bg-white p-5 rounded-[1.5rem] shadow-2xl border border-slate-50 flex items-center gap-4 animate-bounce" style="animation-duration: 4s;">
              <div class="size-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                <span class="material-symbols-outlined font-bold">check_circle</span>
              </div>
              <div>
                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-tight">맞춤 상품 발견</p>
                <p class="text-lg font-black text-slate-900">3.2% 금리 절약</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotateX(0); }
  50% { transform: translateY(-20px) rotateX(2deg); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out forwards;
}

.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
</style>