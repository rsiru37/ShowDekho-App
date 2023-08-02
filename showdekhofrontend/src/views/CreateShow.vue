<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <div class="container" style="margin-top: 5%; float: left;">
        <h1>Create New Show</h1>
        <br><br><br>
            <div class="form-group">
              <h4><label for="dropdownSelect" style="font-style: italic;">Select the Movie:</label></h4>
              <select class="form-control" id="movie" style="font-weight: bold;" v-model="mid">
                <option v-for="movie in movies" :value="movie.id">{{ movie.name }}      |{{ movie.duration }} min       |{{ movie.ratings }}</option>
              </select>
            </div><br><br>
            <div class="form-group">
            <h4><label for="dropdownSelect" style="font-style: italic;">Select the Theatre:</label></h4>
            <select class="form-control" id="theatre" style="font-weight: bold;" v-model="tid">
              <option v-for="theatre in theatres" :value="theatre.tid"> {{ theatre.tname }}     | {{ theatre.city  }}       | {{ theatre.capacity }} seats</option>
            </select></div><br><br>
            <h4><label>Select Date and Time for the Show :</label></h4>
            <input type="datetime-local" id="show-time"
       name="show-time" min="2023-08-02T00:00" max="2024-06-14T00:00" v-model="datetime">
       <br><br>
       <br>
       <input v-model="ticket_price" type="number" placeholder="Ticket Price"><br><br>
       <button type="button" class="btn btn-primary btn-lg" v-on:click="submit()">SUBMIT</button>
    </div>
    <br>

</template>
<script setup>
import { ref } from 'vue'
import axios from 'axios';
import { useRouter } from 'vue-router';
const router=useRouter()
const name=localStorage.getItem('admin_name')
let movies=ref({});
let theatres=ref({});
const datetime=ref('');
const mid=ref();
const tid=ref(null);
const ticket_price=ref();
(async () => {
try {
    const response1 = await axios.get('http://127.0.0.1:5000/home',{headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    movies.value=response1.data;
    console.log(movies.value);
    const response2=await axios.get('http://127.0.0.1:5000/theatre',{headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    theatres.value=response2.data;
    console.log(theatres.value);
} catch (error) {
    console.error('POST request error:', error);
}
})();  

function submit(){
    const a=mid.value;
    const b=tid.value;
    const c=datetime.value;
    const d=ticket_price.value;
    try {
              const res= axios.post('http://127.0.0.1:5000/shows',{a,b,c,d},
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
    // function submit(){
    //     try {
    //           const res= axios.post('http://127.0.0.1:5000/theatre',theatre,
    //           {
    //             headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}` },
    //             });
    //           //this.msg="Theatre Creation Successful!"
    //           console.log(res.data);
    //           setTimeout(() => {
    //             router.push('/theatres') }, 1500);
    //             }           
    //         catch (error) {
    //           console.log(error,"ErrOR")
    //         }
    // }
</script>