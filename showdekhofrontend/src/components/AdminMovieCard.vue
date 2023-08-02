<template>  
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-header">
                <h2>{{ movi.movie.name }}</h2>
            </div>
            <div class="card-body">
                <h5 class="card-title">DIRECTOR: {{ movi.movie.director }}</h5>
                <h5 class="card-title">DURATION: {{ movi.movie.duration }}min</h5>
                <h5 class="card-title">RATINGS: {{ movi.movie.ratings }}</h5>
                <p class="card-text">SUMMARY: {{ movi.movie.summary }}</p>
                <div class="button-container" style="display: flex; gap: 20px;">
                <RouterLink :to="{name: 'EditMovie', params: { id: movi.movie.id } }" class="btn btn-primary" @click="adder">EDIT</RouterLink>

                <button class="btn btn-primary" @click="confirmdelete">DELETE</button>
            </div>
            </div>
        </div>
</div>

</template>
<script setup>
import axios from 'axios';
import { RouterLink, RouterView } from 'vue-router'
let movi=defineProps(['movie'])
function adder(){
    localStorage.setItem('movie_name', movi.movie.name)
}
function confirmdelete(){
    const dd={
        movie_id:movi.movie.id
    }
    if(confirm(`Are you sure you want to delete "${movi.movie.name}"`)){
        const res= axios.delete('http://127.0.0.1:5000/movie',{
                    headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`},
                    data: JSON.stringify(dd)
                    })
        console.log("resPONSE_> ", res);
        setTimeout(() => {
            window.location.reload();
                 }, 1500);
        

    }
}
</script>

<!-- name:movi.movie.name, director:movi.movie.director, duration:movi.movie.duration, ratings:movi.movie.ratings, summary:movi.movie.summary -->