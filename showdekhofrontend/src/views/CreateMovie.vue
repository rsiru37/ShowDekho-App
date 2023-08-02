<template>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2>
    </div>
    <div class="container" style="margin-top: 5%; float: left;">
        <h1>Add New Movie</h1>
        <form>
            <input v-model="mname" type="text" placeholder="Movie Name"><br><br>
            <input v-model="mdirector" type="text" placeholder="Director"><br><br>
            <input v-model="mduration" type=number placeholder="Duration(min)"><br><br>
            <input v-model="mratings" type="text" placeholder="Ratings"><br><br>
            <input v-model="msummary" type="text" placeholder="Summary"><br><br>
        </form>
        <br>
        <div v-if="mname==null || mdirector==null || mduration==null || mratings==null || msummary==null"><button type="button" class="btn btn-primary btn-lg" disabled>SUBMIT</button></div>
        <div v-else><button type="button" class="btn btn-primary btn-lg" v-on:click="submit()">SUBMIT</button></div>
        <br>
        <p style="color: red;">{{ msg }}</p>
    </div>
    <br>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
// const name=ref(localStorage.getItem('admin_name'));
// console.log(name.value,"naam")
export default {
    data(){
        return {
             mname:'',
             mdirector:'',
             mduration:'',
             mratings:'',
             msummary:'',
             msg:'* Please Enter all the Details before you hit the Submit Button',
             name:localStorage.getItem('admin_name')
        };
    },
    methods:{
        submit(){
            try {
              const res= axios.post('http://127.0.0.1:5000/movie',{
                    headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`},
                    movie_name: this.mname,
                    movie_director:this.mdirector,
                    movie_duration:this.mduration,
                    movie_ratings:this.mratings,
                    movie_summary:this.msummary,
                    admin_name:localStorage.getItem('admin_name')
                    }
              )
              this.msg="Movie Creation Successful!"
              setTimeout(() => {
                this.$router.push('/adashboard') }, 1500);
                }           
            catch (error) {
              console.log(error,"ErrOR")
            }

        }
}
}

   
</script>