<template>
  <header>
    <div class="header" style="margin: auto; text-align: center;">
      <h1 margin="auto">Welcome to ShowDekho</h1>
    </div>
    <!-- <h3 class="header" style="color: crimson; margin: auto; text-align: center;">Admin Portal</h3> -->
    <!-- <h3 class="header" style="color: crimson; margin: auto; text-align: center;">User Portal</h3> -->
    <RouterView></RouterView>

      <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->
      
  </header>

  
</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>