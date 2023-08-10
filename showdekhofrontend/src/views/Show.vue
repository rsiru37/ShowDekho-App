<template>
    <h3 class="header" style="color: crimson; margin: auto; text-align: center;">User Portal</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ user_name }}</h2>
    </div>
    <br>
    <UserNavbar></UserNavbar><br><br>
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
                <option value="1">City</option>
                <option value="2">Pincode</option>
                <!-- <option value="category3">Category 3</option> -->
              </select>
              <!-- <button type="submit" class="btn btn-secondary">Apply</button> -->
            </div>
          </div>
        </div>
        <br>
        <h1>Available list of Shows for the Movie : {{ shows[0].movie_name }}</h1>
    <div v-if="shows.length">
        <div class="container" style="margin-top: 2%; float: left;">
            <br>
                <div v-if="netshows.length==0">
                    <div class="row">
                    <ShowCard v-for="i in shows" :show="i"></ShowCard>
                    </div>
                </div>
                <div v-else>
                    <div class="row">
                    <ShowCard v-for="i in netshows" :show="i"></ShowCard>
                </div>
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
import UserNavbar from '../components/UserNavbar.vue';
const movie_id=useRoute().params.id;
const user_name = ref(null);
const shows=ref()
const choice=ref(0);
const search_data=ref();
let netshows=ref([]);
//console.log('route', movie_id)

async function searchfn(){
    netshows.value=[];
    if(choice.value==1){
        for(const sh of shows.value){
            if(sh['city']==search_data.value){
                netshows.value.push(sh)
            }
        }
    }
    else if(choice.value==2){
        for(const sh of shows.value){
            if(sh['pincode']==search_data.value){
                netshows.value.push(sh)
            }
        }
    }
}
onBeforeMount(async() =>{
    try{
        const response1= await axios.get('http://127.0.0.1:5000/uauth', {headers:{'Authorization' : `Bearer ${localStorage.getItem('user-access-token')}`}})
        user_name.value=response1.data;
        const response3=await axios.get(`http://127.0.0.1:5000/shows/${movie_id}`,{ headers:{'Authorization' : `Bearer ${localStorage.getItem('user-access-token')}`}})
            shows.value=response3.data
        }
        catch(err){
            console.log(err, 'Error');
        }
    });
</script>