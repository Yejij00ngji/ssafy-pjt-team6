<template>
  <div>
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <label for="email">email: </label><br>
      <input type="text" id="email" v-model.trim="email">
      <br>
      <label for="password">password: </label><br>
      <input type="password" id="password" v-model.trim="password">
      <br>
      <input type="submit" value="LogIn">
      <hr>
      <button type="button" @click="googleLogin">googleLogin</button>
    </form>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';
import { ref } from 'vue';

const accountStore = useAccountStore()

const email = ref(null)
const password = ref(null)

const logIn = () => {
  const payload = {
    email: email.value,
    password: password.value,
  }

  accountStore.logIn(payload)
}

const googleLogin = () => {
  const GOOGLE_CLIENT_ID = '59174330604-ovkfbnke8jb8e9fs3bbmrtf9jlfcuqlg.apps.googleusercontent.com'
  const REDIRECT_URI = 'http://localhost:5173/login/callback'
  
  const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=email profile`
  
  window.location.href = googleAuthUrl
}
</script>

<style scoped>

</style>