import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

export const useRecommendationStore = defineStore('recommendation', () => {
  
  const accountStore = useAccountStore()

  const recommendations = ref([])

  const setRecommendations = (data) => {
    recommendations.value = data
  }

  const getRecommendations = async () => {

    try {

      const response = await axios.get(`${accountStore.API_URL}/recommendations/`, {

        headers: { Authorization: `Token ${accountStore.token}` },

        timeout: 60000 // OpenAI 응답을 위해 넉넉히 설정

      })

      recommendations.value = response.data.recommendations

    } catch (error) {

      console.error("추천 데이터 로드 실패:", error)

      alert("추천 결과를 가져오는 데 실패했습니다. 다시 시도해 주세요.")

    }
  }

  return { recommendations, setRecommendations, getRecommendations }
}, { persist: true })