<template>  
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-header">
                <h2>{{show.show.theatre_name}}</h2>
            </div>
            <div class="card-body">
                <h5 class="card-title">Ticket price: {{ show.show.price }}</h5>
                <p class="card-text">DATE: {{ show.show.date }}/{{ show.show.month }}</p>
                <p class="card-text">TIME: {{ show.show.hour }}:{{ show.show.minute }}(24-Hr Format)</p>
                <h3 class="card-text">AVAILABLE SEATS : {{ show.show.available_seats }}</h3>
                <div v-if="show.show.available_seats!=0">
                    <button class="btn btn-primary" @click="seats()">Select No.of Seats</button>
                    <br><br>
                    <div v-if="a==5" style="display: flex; gap: 20px;">
                        <h5>Select Seats: </h5>
                        <select v-model="b">
                            <option v-for="i in show.show.available_seats">{{ i }}</option>
                        </select>
                        <button class="btn btn-primary" @click="confirmation()">CONFIRM BOOKING</button>
                    </div>
                </div>
                <div v-else>
                        <button class="btn btn-primary" disabled>HOUSEFUL!</button>
                </div>
                </div>

            </div>
        </div>
</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue';
import axios from 'axios';
let a=ref(0);
const b=ref(null)
const show=defineProps(['show']) // This show we are receiving from Shows Dashboard
console.log("raj37", show,show.value)
function seats(){ a.value=5;}
function confirmation(){
    const dd={show_id:show.show.id, seats:b.value}
    console.log(show.show)
    if(confirm(`Are you sure you want to book "${b.value}" seats for "${show.show.movie_name}"`))
    {
        const res= axios.post('http://127.0.0.1:5000/booking',{dd},{
                    headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`},
                    })
        console.log("resPONSE_> ", res);
        setTimeout(() => {
            window.location.reload();
                 }, 1500);
        

    }
}
</script>