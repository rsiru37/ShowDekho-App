<template>
    <h3 class="header" style="color: crimson; margin: auto; text-align: center;">ADMIN PORTAL</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div><br>
    <AdminNavbar></AdminNavbar>
    <div class="container" style="margin-top: 3%; float: left;">
        <h1>Create New Theatre</h1>
        <form>
             <input v-model="theatre.tname" type="text" placeholder="Theatre Name"><br><br>
             <input v-model="theatre.city" type="text" placeholder="CITY"><br><br>
             <input v-model="theatre.pincode" type="text" placeholder="PIN CODE"><br><br>
             <input v-model="theatre.capacity" type="text" placeholder="CAPACITY"><br><br>
             <input v-model="theatre.contact" type="text" placeholder="CONTACT"><br><br>
        </form>
        <br>
        <div v-if="theatre.tname==null || theatre.city==null || theatre.pincode==null || theatre.capacity==null || theatre.contact==null">
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
import { ref } from 'vue'
import axios from 'axios';
import { useRouter } from 'vue-router';
import AdminNavbar from '../components/AdminNavbar.vue';
const router=useRouter()
const name=localStorage.getItem('admin_name');
const msg=ref('');
    let theatre=ref({});
    async function submit(){
        try {
              const res= await axios.post('http://127.0.0.1:5000/theatre',theatre.value,
              {
                headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}` },
                });
                msg.value=res.data
              if(res.data=='Theatre Added Successfully!'){
                setTimeout(() => {
                router.push('/theatres') }, 1500);
              }

                }           
            catch (error) {
              console.log(error,"ErrOR")
            }
    }
</script>