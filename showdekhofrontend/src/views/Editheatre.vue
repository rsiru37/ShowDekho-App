<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <div class="container" style="margin-top: 5%; float: left;">
        <h1>Editing Theatre {{ theatre.tname }}</h1>
        <form>
            Theatre Name <input v-model="theatre.tname" type="text" placeholder="Theatre Name"><br><br>
            CITY <input v-model="theatre.city" type="text" placeholder="CITY"><br><br>
            PIN CODE <input v-model="theatre.pincode" type="text" placeholder="PIN CODE"><br><br>
            CAPACITY <input v-model="theatre.capacity" type="text" placeholder="CAPACITY"><br><br>
            CONTACT <input v-model="theatre.contact" type="text" placeholder="CONTACT"><br><br>
        </form>
        <br>
        <button type="button" class="btn btn-primary btn-lg" v-on:click="submit()">SUBMIT</button>
        <br>
        <p style="color: red;">{{ msg }}</p>
    </div>
    <br>

</template>

<script setup>
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
const router=useRouter();
const id=useRoute().params.id
import axios from 'axios'
import { ref } from 'vue'
const theatre=ref(null);
const name=localStorage.getItem('admin_name');
let msg=ref('* Fill all the Details before u hit Submit!')
console.log("ID-->", id);
(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/theatre/${id}`, {headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    theatre.value=response.data;
    console.log(response.data);
  } catch (error) {
    console.error('GET request error:', error);
  }
})();
function submit(){
  const thea={
    theatre_name:theatre.value.tname,
    theatre_city:theatre.value.city,
    theatre_pincode:theatre.value.pincode,
    theatre_contact:theatre.value.contact,
    theatre_capacity:theatre.value.capacity
  }
  console.log("thea", theatre.value)
  try{
    const response= axios.put(`http://127.0.0.1:5000/theatre/${id}`, {headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`},
     data: thea})
    msg=response.data;
    setTimeout(() => {
                router.push('/theatres') }, 1500);
                
  }
  catch(err){
    console.log(err,'error')
  }
}


</script>