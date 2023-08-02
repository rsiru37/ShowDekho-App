<template>
    <div class="container">
    <div class="form">
        <ul class="tab-group">
          <li class="tab active"><a href="#signup">Sign Up</a></li>
          <li class="tab"><a href="#login">Log In</a></li>
        </ul>
        
        <div class="tab-content">
          <div id="signup">   
            <h1>Sign Up for Free</h1>
            
            <form>
            
            <div class="top-row">
              <div class="field-wrap">
                <label>
                  First Name<span class="req">*</span>
                </label>
                <input type="text" required autocomplete="off" />
              </div>
          
              <div class="field-wrap">
                <label>
                  Last Name<span class="req">*</span>
                </label>
                <input type="text" required autocomplete="off"/>
              </div>
            </div>
      
            <div class="field-wrap">
              <label>
                Email Address<span class="req">*</span>
              </label>
              <input type="email" required autocomplete="off"/>
            </div>
            
            <div class="field-wrap">
              <label>
                Set A Password<span class="req">*</span>
              </label>
              <input type="password" required autocomplete="off"/>
            </div>
            
            <button type="submit"> SIGN UP! </button>
            
            </form>
      
          </div>
          
          <div id="login">
            <h1>Welcome Back!</h1>
            <label>
                Email Address<span class="req">*</span>
              </label>
              <input v-model="login_form.email" type="email" name="email" required autocomplete="off"/>
              <label>
                Password<span class="req">*</span>
              </label>
              <input v-model="login_form.pwd" type="password" name="pwdd" required autocomplete="off"/>
              <button type='submit' v-on:click="login()"> LogIn </button><br>
              ADMIN<input type="checkbox" v-model="login_form.isChecked" />
            </div>   
        </div>   
        </div><!-- tab-content -->
      </div> <!-- /form -->
</template>

<script>
import axios from 'axios'
let a='raj';
let b='siru';
export default{
    data(){
        return{
            login_form:{
                email:'',
                pwd:'',
                isChecked:false
            }
        }
    },
    methods: {
        async login(){
          console.log(this.login_form.email,this.login_form.pwd,this.login_form.isChecked)
          if(this.login_form.isChecked){ // Admin Login
            try {
              await axios.post('http://127.0.0.1:5000/logi',{
                    email: this.login_form.email,
                    pwd:this.login_form.pwd,
                    admin:this.login_form.isChecked
                }).then(response =>{ 
                    localStorage.setItem('admin-access-token', response.data.at)
                    localStorage.setItem('admin_name',response.data.admin)
                    this.$router.push('/adashboard')
                    })

              
            } catch (error) {
              console.log(error,"ErrOR")
            }
          }
          else{ // User Login
            try{
                await axios.post('http://127.0.0.1:5000/logi',{
                    email: this.login_form.email,
                    pwd:this.login_form.pwd,
                    admin:this.login_form.isChecked
                }).then(response =>{ 
                    localStorage.setItem('user-access-token', response.data.at)
                    localStorage.setItem('user_name',response.data.user)
                    this.$router.push('/dashboard')
                    console.log(response.data)})
            }
            catch(error){
                console.log("Login Failed", error)
            }
          }
        }
    }
}
</script>