<template>
  <div class = "form_authorization">
    <div class="login-page">
      <h2>Вход</h2>
      <form class="login" @submit.prevent="login">
        <div>
          <label for="username">Логин:</label>
          <input class="form_authorization--input" v-model="username" type="text" id="username" required />
        </div>
        <div>
          <label for="password">Пароль:</label>
          <input class="form_authorization--input" v-model="password" type="password" id="password" required />
        </div>
        <button type="submit">Войти</button>
      </form>
    </div>
  </div>
  </template>
  
  <script setup lang="ts">
  import { useAuthStore } from 'src/store/auth'
import { ref, type Ref } from 'vue';
    import { useRouter } from 'vue-router'

const router = useRouter()

  const username: Ref<string> = ref('');
  const password: Ref<string> = ref('');
  // const error: Ref<string> = ref('');
  const auth = useAuthStore();

  const login = async () => { 
      try {
        await auth.login(username.value, password.value)
        await auth.fetchUser()
        await router.push('/') // перенаправить на главную
      } catch (error) {
        console.error('Ошибка входа:', error)
      }
      }
  </script>
  
  <style scoped>
  .login-page {
    max-width: 400px;
    margin: auto;
  }
  </style>