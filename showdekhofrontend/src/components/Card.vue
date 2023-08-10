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
                <RouterLink :to="{name: 'Mshow', params: { id: movi.movie.id } }" class="btn btn-primary">Book</RouterLink>
            </div>
        </div>
</div>
</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
let movi=defineProps(['movie'])
</script>