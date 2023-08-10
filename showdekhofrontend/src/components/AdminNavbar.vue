<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <a class="navbar-brand" href="#"></a>
        <RouterLink to="/adashboard" class="navbar-brand">MOVIES</RouterLink>
        <a class="navbar-brand" href="#"></a>
        <RouterLink to="/theatres" class="navbar-brand">THEATRES</RouterLink>
        <a class="navbar-brand" href="#"></a>
        <RouterLink to="/shows" class="navbar-brand">SHOWS</RouterLink>
        <a class="navbar-brand" href="#"></a>
        <button style="margin: auto; text-align: center;" v-on:click="logout()">LOGOUT</button>
      </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router=useRouter()
function logout(){
  localStorage.removeItem('admin-access-token');
  localStorage.removeItem('admin_name');
  router.push('/')
}
</script>