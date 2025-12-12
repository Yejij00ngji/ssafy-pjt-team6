import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from './accounts'
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
  
  const accountstore = useAccountStore()

  const products_recommanded = ref(null)
  const products_finance = ref(null)

  const map_info = ref(null)
  const currencies = ref(null)

  return { products_finance, products_recommanded, map_info, currencies }
}, { persist: true })