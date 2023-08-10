<template>
  <h3 class="header" style="color: crimson; margin: auto; text-align: center;">ADMIN PORTAL</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ admin_name }}</h2>
    </div><br>
    <AdminNavbar></AdminNavbar><br>
    <RouterLink to="/createshow"><button type="button" class="btn btn-primary btn-lg">Add Show</button></RouterLink>
    <div v-if="shows.length">
        <div class="container" style="margin-top: 3%; float: left;">
            <h1>Available list of Shows</h1>
            <br>
            <div class="row">
            <AShowCard v-for="i in shows" :show="i" ></AShowCard>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No Shows Found</p>
    </div>
    
</template>

<script setup>
import AdminNavbar from '../components/AdminNavbar.vue';
import axios from 'axios'
import { ref } from 'vue'
import { RouterLink } from 'vue-router';
import AShowCard from '../components/AShowCard.vue'
const shows=ref(0);
const admin_name=localStorage.getItem('admin_name');
(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/shows',{headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    shows.value=response.data;
  } catch (error) {
    console.error('POST request error:', error);
  }
})();
</script>