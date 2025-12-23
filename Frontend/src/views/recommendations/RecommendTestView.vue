<template>
  <div>
    <h2>📊 나를 위한 금융 상품 추천</h2>

    <button @click="loadRecommendations">
      추천 받기
    </button>

    <ul v-if="recommendations.length">
      <li v-for="item in recommendations" :key="item.product_option_id">
        <strong>{{ item.product_name }}</strong><br />
        {{ item.bank_name }}<br />
        금리: {{ item.intr_rate }} ~ {{ item.intr_rate2 }}<br />
        점수: {{ item.score }} / 신뢰도: {{ item.confidence }}
        <hr />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { fetchRecommendations } from "@/api/recommendations";

const recommendations = ref([]);

const loadRecommendations = async () => {
  try {
    const res = await fetchRecommendations();
    recommendations.value = res.data.recommendations;
  } catch (e) {
    alert("추천 불러오기 실패");
    console.error(e);
  }
};
</script>

