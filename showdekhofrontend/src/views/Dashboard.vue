<script setup>
import Card from '../components/Card.vue';
import TheWelcome from '../components/TheWelcome.vue';
import { defineProps } from 'vue'
import { onMounted } from 'vue'
import axios from 'axios'
import { ref } from 'vue'
const movies=ref(0);
const name=localStorage.getItem('user_name');
(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/home');
    console.log('POST request success:', response.data);
    movies.value=response.data;
    console.log(movies,movies.value);
  } catch (error) {
    console.error('POST request error:', error);
  }
})();
</script>

<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <div v-if="movies.length">
        <div class="container" style="margin-top: 5%; float: left;">
            <h1>Available list of Movies</h1>
            <br>
            <div class="row">
            <Card v-for="i in movies" :movie="i"></Card>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No Movies Found</p>
    </div>
    
</template>
<!-- v-for="i in movies" :movie="i" -->