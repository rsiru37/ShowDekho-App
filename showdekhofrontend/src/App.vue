<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <div class="header" style="margin: auto; text-align: center;">
      <h1 margin="auto">Welcome to ShowDekho</h1>
      <h3 style="color: crimson;">User Portal</h3>
  </div>
      <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->
  </header>
<RouterView></RouterView>
  
</template>