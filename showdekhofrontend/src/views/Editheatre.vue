<template>
  <h3 class="header" style="color: crimson; margin: auto; text-align: center;">ADMIN PORTAL</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div><br>
    <AdminNavbar></AdminNavbar>
    <div class="container" style="margin-top: 3%; float: left;">
        <h1>Editing Theatre : {{ theatre.tname }}</h1>
        <form>
            Theatre Name <input v-model="theatre.tname" type="text" placeholder="Theatre Name"><br><br>
            CITY <input v-model="theatre.city" type="text" placeholder="CITY"><br><br>
            PIN CODE <input v-model="theatre.pincode" type="text" placeholder="PIN CODE"><br><br>
            CAPACITY <input v-model="theatre.capacity" type="text" placeholder="CAPACITY"><br><br>
            CONTACT <input v-model="theatre.contact" type="text" placeholder="CONTACT"><br><br>
        </form>
        <br>
        <div v-if="theatre.tname=='' || theatre.city=='' || theatre.pincode=='' || theatre.capacity=='' || theatre.contact==''">
          <button type="button" class="btn btn-primary btn-lg" disabled>SUBMIT</button>
        </div>
        <div v-else>
          <button type="button" class="btn btn-primary btn-lg" v-on:click="submit()">SUBMIT</button>
        </div>
        <br>
        <p style="color: red;">{{ msg }}</p>
    </div>
    <br>

</template>

<script setup>
import AdminNavbar from '../components/AdminNavbar.vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
const router=useRouter();
const id=useRoute().params.id
import axios from 'axios'
import { ref } from 'vue'
const theatre=ref(null);
const name=localStorage.getItem('admin_name');
const msg=ref('* Fill all the Details before u hit Submit!')
(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/theatre/${id}`, {headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}});
    theatre.value=response.data;
  } catch (error) {
    console.error('GET request error:', error);
  }
})();
async function submit(){
  const thea={
    theatre_id:theatre.value.tid,
    theatre_name:theatre.value.tname,
    theatre_city:theatre.value.city,
    theatre_pincode:theatre.value.pincode,
    theatre_contact:theatre.value.contact,
    theatre_capacity:theatre.value.capacity
  }
  try{
    const response= await axios.put(`http://127.0.0.1:5000/theatre`,
    {data: thea},
     {headers:{'Content-Type': 'application/json', 'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}}
     )
    msg.value=response.data;
    if(msg.value == 'Update Successfull!!'){
      setTimeout(() => {
                router.push('/theatres') }, 1500);
    }           
  }
  catch(err){
    console.log(err,'error')
  }
}


</script>