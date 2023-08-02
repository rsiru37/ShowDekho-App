<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ user_name }}</h2>
    </div>
    <h1>Available list of Shows for the Movie : {{ movie_name }}</h1>
    <div v-if="shows.length">
        <div class="container" style="margin-top: 5%; float: left;">
            <br>
             <div class="row">
            <ShowCard v-for="i in shows" :show="i"></ShowCard>
            </div>
         </div>
    </div>
    <div v-else>
        <p>No Shows Found Found</p>
    </div> 

</template>

<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router';
import { onBeforeMount, ref } from 'vue';
import ShowCard from '../components/ShowCard.vue';
const movie_id=useRoute().params.id;
const user_name = ref(null);
const movie_name=ref(null)
const shows=ref(null)
//console.log('route', movie_id);
onBeforeMount(async() =>{
    try{
        const response1= await axios.get('http://127.0.0.1:5000/uauth', {headers:{'Authorization' : `Bearer ${localStorage.getItem('user-access-token')}`}})
        console.log(response1)
        user_name.value=response1.data;
        console.log(user_name, user_name.value)
        console.log(movie_id)
        const response2=await axios.get('http://127.0.0.1:5000/movie',{ headers:{'Authorization' : `Bearer ${localStorage.getItem('user-access-token')}`}, params:{id:movie_id}})
            movie_name.value=response2.data;
        const response3=await axios.get(`http://127.0.0.1:5000/shows/${movie_id}`,{ headers:{'Authorization' : `Bearer ${localStorage.getItem('user-access-token')}`}})
            shows.value=response3.data
            console.log(shows.value,'raj377')
        }
        catch(err){
            console.log(err, 'Error');
        }
    });
</script>