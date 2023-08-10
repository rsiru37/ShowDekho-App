<template>  
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-header">
                <h2>MOVIE: {{ show.show.movie }}</h2>
            </div>
            <div class="card-body">
                <h5 class="card-title">AVAILABLE SEATS: {{ show.show.available_seats }}</h5>
                <h5 class="card-title">Ticket price: ₹ {{ show.show.price }}</h5>
                <p class="card-text">DATE: {{ show.show.date }}/{{ show.show.month }}/{{ show.show.year }}</p>
                <p class="card-text">TIME: {{ show.show.hour }}:{{ show.show.minute }}(24-Hr Format)</p>
                <h4 class="card-title"> THEATRE: {{ show.show.theatre }}</h4>
                <div class="button-container" style="display: flex; gap: 20px;">
                <RouterLink :to="{name: 'EditShow', params:{id: show.show.id } }" class="btn btn-primary" >EDIT</RouterLink>
                <button class="btn btn-danger" @click="confirmdelete()">DELETE</button>
            </div>
            </div>
        </div>
</div>

</template>

<script setup>
import axios from 'axios';
import { RouterLink, RouterView } from 'vue-router'
let show=defineProps(['show'])
const dd={show_id: show.show.id}
function confirmdelete(){
    if(confirm(`Are you sure you want to delete the show of Movie ${show.show.movie} in ${show.show.theatre} ?`)){
        const res= axios.delete('http://127.0.0.1:5000/shows',{
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