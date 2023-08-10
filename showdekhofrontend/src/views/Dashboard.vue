<script setup>
import Card from '../components/Card.vue';
import UserNavbar from '../components/UserNavbar.vue';
import { defineProps } from 'vue'
import { onMounted } from 'vue'
import axios from 'axios'
import { ref } from 'vue'
const movies=ref(0);
const name=localStorage.getItem('user_name');
const choice=ref(2);
const search_data=ref();
let netmovies=ref([]);

(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/home');
    movies.value=response.data;
  } catch (error) {
    console.error('POST request error:', error);
  }
})();
function searchfn(){
  netmovies.value=[]
  if(choice.value==2){
    for (const m of movies.value){
      if(m['director'] == search_data.value){
        netmovies.value.push(m)
      }
    }
  }
  else if(choice.value==1){
    for (const m of movies.value){
      if(m['ratings'] >= search_data.value){
        netmovies.value.push(m)
      }
    }
  }
}
</script>

<template>
  <h3 class="header" style="color: crimson; margin: auto; text-align: center;">User Portal</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <br><br><br>
    
    <br>
    <UserNavbar></UserNavbar>
    <br>
    <div v-if="movies.length">
      <div class="row">
        <div class="col-md-8">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="Search..." v-model="search_data">
            <div v-if="choice!=0">
              <button class="btn btn-primary" v-on:click="searchfn()">Search</button>
            </div>
            <div v-else>
              <button type="submit" class="btn btn-primary" disabled>Search</button>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="input-group">
            <select class="form-select" v-model="choice">
              <option value="0">Filter by...</option>
              <option value="1">Ratings (Whatever you type on the search box movies above that rating only will be shown)</option>
              <option value="2">Director</option>
            </select>
          </div>
        </div>
      </div>
        <div class="container" style="margin-top: 2%; float: left;">
            <h1>Available list of Movies</h1>
            <br>
            <div v-if="netmovies.length==0">
              <div class="row">
                <Card v-for="i in movies" :movie="i"></Card>
                </div>
            </div>
            <div v-else>
              <div class="row">
                <Card v-for="i in netmovies" :movie="i"></Card>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No Movies Found</p>
    </div>
    
</template>
<!-- v-for="i in movies" :movie="i" -->