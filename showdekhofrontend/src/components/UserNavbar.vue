<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <a class="navbar-brand" href="#"></a>
        <RouterLink to="/dashboard" class="navbar-brand">MOVIES</RouterLink>
        <a class="navbar-brand" href="#"></a>
        <button style="margin: auto; text-align: center;" v-on:click="logout()">LOGOUT</button>
      </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router=useRouter()
function logout(){
  localStorage.removeItem('user-access-token');
  localStorage.removeItem('user_name');
  router.push('/')
}
</script>