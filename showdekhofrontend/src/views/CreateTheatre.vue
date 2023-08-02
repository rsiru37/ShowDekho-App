<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <div class="container" style="margin-top: 5%; float: left;">
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
const router=useRouter()
const name=localStorage.getItem('admin_name')
    let theatre=ref({});
    function submit(){
        try {
              const res= axios.post('http://127.0.0.1:5000/theatre',theatre,
              {
                headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}` },
                });
              //this.msg="Theatre Creation Successful!"
              console.log(res.data);
              setTimeout(() => {
                router.push('/theatres') }, 1500);
                }           
            catch (error) {
              console.log(error,"ErrOR")
            }
    }
</script>