<template>
  <h3 class="header" style="color: crimson; margin: auto; text-align: center;">ADMIN PORTAL</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ admin_name }}</h2>
    </div><br>
    <AdminNavbar></AdminNavbar><br><br>
    <RouterLink to="/createtheatre"><button type="button" class="btn btn-primary btn-lg">Add Theatre</button></RouterLink>
    <div v-if="theatres.length">
        <div class="container" style="margin-top: 3%; float: left;">
            <h1>Available list of Theatres</h1>
            <br>
            <div class="row">
            <TheatreCard v-for="i in theatres" :th="i" ></TheatreCard>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No Theatres Found</p>
    </div>
    
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { RouterLink } from 'vue-router';
import AdminNavbar from '../components/AdminNavbar.vue';
import TheatreCard from '../components/TheatreCard.vue';
const theatres=ref(0);
const admin_name=localStorage.getItem('admin_name');
(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/theatre',{headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    theatres.value=response.data;
  } catch (error) {
    console.error('POST request error:', error);
  }
})();
</script>