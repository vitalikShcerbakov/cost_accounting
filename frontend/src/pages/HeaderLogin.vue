<template>
  <div class="header_text">
    <div v-if="auth.user">
      <a class="header_text">{{ auth.user }} </a>
      <button @click="logout"> Выйти </button>
    </div>
    <div v-else>
      <router-link to="/login"> Войти</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../store/auth';
import { useRouter } from 'vue-router'

const router = useRouter()

const auth = useAuthStore()

// store: useRecordStore(),

const logout = () => {
  auth.logout()
  void router.push('/login')
}

</script>
<style>
.header_text {
  background-color: transparent;
  background-repeat: no-repeat;
  border: none;
  cursor: pointer;
  overflow: hidden;
  outline: none;
  color: white;
  font-size: 20px;
}
</style>