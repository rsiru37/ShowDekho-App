<template>
  <h3 class="header" style="color: crimson; margin: auto; text-align: center;">ADMIN PORTAL</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ admin_name }}</h2>
    </div>
    <br>
    <AdminNavbar></AdminNavbar><br>
    <RouterLink to="/addmovie"><button type="button" class="btn btn-primary btn-lg">Add Movie</button></RouterLink>
    <div v-if="movies.length">
        <div class="container" style="margin-top: 3%; float: left;">
            <h1>Available list of Movies</h1>
            <br>
            <div class="row">
            <AdminMovieCard v-for="i in movies" :movie="i"></AdminMovieCard>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No Movies Found</p>
    </div>
    
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import AdminMovieCard from '../components/AdminMovieCard.vue';
import { RouterLink } from 'vue-router';
import AdminNavbar from '../components/AdminNavbar.vue';
const movies=ref(0);
const admin_name=localStorage.getItem('admin_name');
(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/home');
    movies.value=response.data;
    
  } catch (error) {
    console.error('POST request error:', error);
  }
})();
</script>