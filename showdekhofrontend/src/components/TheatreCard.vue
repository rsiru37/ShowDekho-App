<template>  
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-header">
                <h2>{{ th.th.tname }}</h2>
            </div>
            <div class="card-body">
                <h5 class="card-title">CAPACITY: {{ th.th.capacity }}</h5>
                <h5 class="card-title">CITY: {{ th.th.city }}</h5>
                <h5 class="card-title">CONTACT: {{ th.th.contact }}</h5>
                <h5 class="card-text">PINCODE: {{ th.th.pincode }}</h5>
                <div class="button-container" style="display: flex; gap: 20px;">
                <RouterLink :to="{name: 'Editheatre', params: { id: th.th.tid } }" class="btn btn-primary" @click="adder">EDIT</RouterLink>
                <button class="btn btn-danger" @click="confirmdelete">DELETE</button>
                <button type="button" class="btn btn-outline-success" style="margin-left: auto;" @click="exprt()">Export CSV</button>
            </div>
            </div>
        </div>
</div>

</template>

<script setup>
import axios from 'axios';
import { RouterLink, RouterView } from 'vue-router'
let th=defineProps(['th'])
function adder(){
    localStorage.setItem('theatre_name', th.th.name)
}
function confirmdelete(){
    const dd={
        theatre_id:th.th.tid
    }
    if(confirm(`Are you sure you want to delete "${th.th.tname}"`)){
        const res= axios.delete('http://127.0.0.1:5000/theatre',{
                    headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`},
                    data: JSON.stringify(dd)
                    })
        setTimeout(() => {
            window.location.reload();
                 }, 1500);
    }
}
async function exprt(){
    const res=await axios.get(`http://127.0.0.1:5000/report/${th.th.tid}`, {headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}})
    window.location.href=`http://127.0.0.1:5000/download-file/${res.data}`;

}
</script>