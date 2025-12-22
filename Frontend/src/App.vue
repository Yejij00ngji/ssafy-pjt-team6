<script setup>
import { RouterView } from 'vue-router'
import NavbarItem from './components/home/NavbarItem.vue';

// 기존 store 및 로직 유지
import { useAccountStore } from './stores/accounts';
const accountstore = useAccountStore()
</script>

<template>
  <NavbarItem />

  <RouterView />
</template>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Pretendard', sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* 기존 차트/테이블 스타일은 유지하되, nav 요소에 영향을 주지 않도록 관리 */
.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
  margin-bottom: 30px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
}

.rate {
  font-weight: bold;
  color: #2c3e50;
}
</style>
