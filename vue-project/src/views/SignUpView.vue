<template>
  <div>
    <h1>회원 가입</h1>
    <form @submit.prevent="signUp">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username">
      <br>
      <label for="password1">password: </label>
      <input type="password" id="password1" v-model.trim="password1">
      <br>
      <label for="password2">password confirmation: </label>
      <input type="password" id="password2" v-model.trim="password2">
      <br>
      <label for="birth_date">birth date: </label>
      <input type="date" id="birth_date" v-model="birth_date">
      <br>
      <label for="salary">salary: </label>
      <input type="number" id="salary" v-model.number="salary">
      <br>
      <label for="possessions">possessions: </label>
      <input type="number" id="possessions" v-model.number="possessions">
      <br>
      <label for="is_mydata_agreed">
        마이데이터 제공 동의: 
        <input type="checkbox" id="is_mydata_agreed" v-model="is_mydata_agreed">
      </label>
      <br>
      <input type="submit" value="signup">
    </form>
  </div>
</template>

<script setup>
  import { useAccountStore } from '@/stores/accounts';
  import { ref } from 'vue';

const accountStore = useAccountStore()

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const birth_date = ref(null)
const salary = ref(null)
const possessions = ref(null)
const is_mydata_agreed = ref(false)


const signUp = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    birth_date: birth_date.value,
    salary: salary.value,
    possessions: possessions.value,
    is_mydata_agreed: is_mydata_agreed.value,
  }
  accountStore.signUp(payload)
}
</script>

<style scoped>

</style>