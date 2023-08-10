<template>
    <h3 class="header" style="color: crimson; margin: auto; text-align: center;">ADMIN PORTAL</h3>
    <div class="sidebar" style="width: 250px;height: 100vh;padding: 20px;border-width: 250px; float: left;">
        <h2>Welcome {{ name }}</h2><br>
    </div><br>
    <AdminNavbar></AdminNavbar>
    <div class="container" style="margin-top: 3%; float: left;">
        <h1>Editing movie <a href='#' class="underline-link" v-on:click="getm()">{{ mname }} </a></h1>
        <form>
            <input v-model="mname" type="text" placeholder="Movie Name"><br><br>
            <input v-model="mdirector" type="text" placeholder="Director"><br><br>
            <input v-model="mduration" type=number placeholder="Duration(min)"><br><br>
            <input v-model="mratings" type="text" placeholder="Ratings"><br><br>
            <input v-model="msummary" type="text" placeholder="Summary"><br><br>
        </form>
        <br>
        <div v-if="mname=='' || mdirector=='' || mduration=='' || mratings=='' || msummary==''">
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

<script>
import axios from 'axios';
import AdminNavbar from '../components/AdminNavbar.vue';
// const name=ref(localStorage.getItem('admin_name'));
// console.log(name.value,"naam")
export default {
    components:{AdminNavbar},
    data(){
        return {
             mname:localStorage.getItem('movie_name'),
             mdirector:'',
             mduration:'',
             mratings:'',
             msummary:'',
             msg:'* Fill all the fields before submitting',
             name:localStorage.getItem('admin_name')
        };
    },
    methods:{
        async submit(){
            try {
              const res= await axios.put('http://127.0.0.1:5000/movie',
                {
                    movie_name: this.mname,
                    movie_director:this.mdirector,
                    movie_duration:this.mduration,
                    movie_ratings:this.mratings,
                    movie_summary:this.msummary,
                    admin_name:localStorage.getItem('admin_name'),
                    movie_id:this.$route.params.id
                }, 
                    {headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`}})
              this.msg=res.data;
              if(this.msg=='Update Successfull'){
                setTimeout(() => {
                localStorage.removeItem('movie_name')
                this.$router.push('/adashboard') }, 1500);
              }
                }           
            catch (error) {
              console.log(error,"ErrOR")
            }

        },
        async getm(){
            const res= await axios.get('http://127.0.0.1:5000/movie',{
                    headers:{'Authorization' : `Bearer ${localStorage.getItem('admin-access-token')}`},params:{movie_id:this.$route.params.id}});
                this.mdirector=res.data.director;
                this.mduration=res.data.duration;
                this.mratings=res.data.ratings;
                this.msummary=res.data.summary;
        }

}
}
</script>