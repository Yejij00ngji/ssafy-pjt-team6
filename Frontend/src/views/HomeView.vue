<template>
  <main>
    <HeroItem />
    <FeatureItem />
    <!-- <BannerSection />  -->
     <button @click="getData(myFinancialData)">getData</button>
  </main>
</template>

<script setup>
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts';
import HeroItem from '@/components/home/HeroItem.vue';
import FeatureItem from '@/components/home/FeatureItem.vue';

const accountStore = useAccountStore()

const getData = async (financialData) => {
  try {
    // 1. FormData 객체 생성
    const formData = new FormData();
    
    // 2. 전달받은 5가지 데이터 추가 (문자열이 아닌 숫자로 보내도 FormData가 처리함)
    formData.append('balance_amt', financialData.balance_amt);
    formData.append('invest_eval_amt', financialData.invest_eval_amt);
    formData.append('annual_income_amt', financialData.annual_income_amt);
    formData.append('monthly_paid_amt', financialData.monthly_paid_amt);
    formData.append('withdrawable_amt', financialData.withdrawable_amt);

    // 4. POST 요청 전송
    const response = await axios.post(
      `${accountStore.API_URL}/accounts/finacial-profile/`, 
      formData, 
      {
        headers: {
          'Authorization': `Token ${accountStore.token}`, // 반드시 Bearer 문구 포함
          // 'Content-Type': 'multipart/form-data' // Axios가 FormData를 감지하면 자동으로 설정하므로 생략 가능합니다.
        }
      }
    );

    console.log('성공:', response.data);
    return response.data;

  } catch (error) {
    console.error('에러 발생:', error.response ? error.response.data : error.message);
  }
};

// 호출 예시
const myFinancialData = {'balance_amt': 78478662, 'invest_eval_amt': 33633711, 'annual_income_amt': 50000000, 'monthly_paid_amt': 3196661, 'withdrawable_amt': 15695732};
// const myFinancialData = {
//   balance_amt: 32000000,
//   invest_eval_amt: 5000000,
//   annual_income_amt: 45000000,
//   monthly_paid_amt: 1200000,
//   withdrawable_amt: 3000000
// };
</script>