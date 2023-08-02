<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <div class="container" style="margin-top: 5%; float: left;">
        <h1>Editing Show</h1>
        <div v-if="show.available_seats == show.total_seats">
          <div class="form-group">
            <h4><label for="dropdownSelect" style="font-style: italic;">Select the Movie:</label></h4>
            <select class="form-control" id="movie" style="font-weight: bold;" v-model="show.movie_id">
              <option v-for="movie in movies" :value="movie.id">{{ movie.name }}      |{{ movie.duration }} min       |{{ movie.ratings }}</option>
            </select>
          </div><br><br>
          <div class="form-group">
          <h4><label for="dropdownSelect" style="font-style: italic;">Select the Theatre:</label></h4>
          <select class="form-control" id="theatre" style="font-weight: bold;" v-model="show.theatre_id">
            <option v-for="theatre in theatres" :value="theatre.tid"> {{ theatre.tname }}     | {{ theatre.city  }}       | {{ theatre.capacity }} seats</option>
          </select></div><br><br>
          <h4><label>Select Date and Time for the Show :</label></h4>
          <input type="datetime-local" id="show-time"
     name="show-time" min="2023-08-02T00:00" max="2024-06-14T00:00" v-model="show.date_time">
     <br><br>
     <br>
     <input v-model="show.ticket_price" type="number" placeholder="Ticket Price"><br><br>
     <button type="button" class="btn btn-primary btn-lg" v-on:click="submit()">SUBMIT</button>
        </div>
        <div v-else>
            <p>Sorry we cannot Edit</p>
        </div>
        <br>
        <br>
    </div>
    <br>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
const router=useRouter();
const id=useRoute().params.id
import axios from 'axios'
import { ref } from 'vue';
const movies=ref();
const show=ref();

const datetime=ref();

const theatres=ref();
(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/show/${id}`, {headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    show.value=response.data;
    console.log(response.data);
    const response1 = await axios.get('http://127.0.0.1:5000/home',{headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    movies.value=response1.data;
    const response2=await axios.get('http://127.0.0.1:5000/theatre',{headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    theatres.value=response2.data;
  } catch (error) {
    console.error('GET request error:', error);
  }
})();
setTimeout(() => {
const mid=ref(show.movie_id);
const tid=ref(show.theatre_id);
                 }, 2000);
function submit(){
    const a=show.value.movie_id;
    const b=show.value.theatre_id;
    const c=show.value.date_time;
    const d=show.value.ticket_price;
    const e=id;
    console.log(show)
    console.log('Log37',a,b,c,d,e)
    try {
              const res= axios.put('http://127.0.0.1:5000/shows',{a,b,c,d,e},
              {
                headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}` },
                });
              //this.msg="Theatre Creation Successful!"
              setTimeout(() => {
                router.push('/shows') }, 1500);
                }           
            catch (error) {
              console.log(error,"ErrOR")
            }
    console.log("Logging", mid.value, tid.value, datetime.value);
}
</script>
