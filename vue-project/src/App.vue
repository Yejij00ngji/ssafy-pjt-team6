<script setup>
import { RouterLink, RouterView } from 'vue-router'

import { useRoute, useRouter } from 'vue-router';

import { useAccountStore } from './stores/accounts';
import { useProductStore } from './stores/products';

const route = useRoute()
const router = useRouter()

const accountstore = useAccountStore()
const store = useProductStore()

const logOut = () => {
  accountstore.logOut()
}

</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink :to="{name:'Home'}">home</RouterLink>
        <span> | </span>
        <template v-if="!accountstore.isLogin">
          <RouterLink :to="{name:'LoginView'}">login</RouterLink>
          <span> | </span>
          <RouterLink :to="{name:'SignUpView'}">signup</RouterLink>
          <span> | </span>
        </template>
        <template v-else>
          <a href="#" @click.prevent="logOut">logout</a>
          <span> | </span>
        </template>
        <RouterLink :to="{name:'FinanceProducts'}">finance</RouterLink>
        <span> | </span>
        <RouterLink :to="{name:'RecommandProducts'}">recommand</RouterLink>
        <span> | </span>
        <RouterLink :to="{name:'ExchangeRate'}">exchange</RouterLink>
        <span> | </span>
        <RouterLink :to="{name:'Map'}">map</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

</style>
