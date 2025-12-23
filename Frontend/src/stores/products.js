import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
  
  const accountStore = useAccountStore()

  const subscriptions = ref([])

  const getProducts = async ({ bank, term }) => {
    const response = await axios.get(
      `${accountStore.API_URL}/products/`,{
      // headers: {
      //   'Authorization': `Token ${accountStore.token}`
      // },
      params: {
        bank: bank || undefined,
        term: term || undefined
      }
      })
    
    console.log(response.data)

    return response.data
  }

  const getProductDetails = async (id) => {
    const response = await axios.get(
      `${accountStore.API_URL}/products/${id}`,{
      // headers: {
      //   'Authorization': `Token ${accountStore.token}`
      // },
      })
    
    console.log(response.data)

    return response.data
  }

  const getSubscriptions = async () => {
    const response = await axios.get(
      `${accountStore.API_URL}/subscriptions/`,{
      headers: {
        'Authorization': `Token ${accountStore.token}`
      },
      })
    
    console.log(response.data)

    subscriptions.value = response.data
    return response.data
  }

  const subscribeProduct = async ({product_option, amounts}) => {
    await axios.post(
      `${accountStore.API_URL}/subscriptions/`,
      {
        product_option: product_option,
        amount: amounts,
      },
      {
      headers: {
        'Authorization': `Token ${accountStore.token}`
        },
      })
  }

  return { subscriptions, getProducts, getProductDetails, subscribeProduct, getSubscriptions }
}, { persist: true })