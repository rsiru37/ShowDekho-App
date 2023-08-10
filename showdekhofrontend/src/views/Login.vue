<template>
  <div class="container">
  <div class="form">
      
      <div class="tab-content">
        <div id="signup">   
          <h1>USER Sign Up on ShowDekho</h1>
          
          <div class="top-row">
            <div class="field-wrap">
              <label>
                Name<span class="req">*</span>
              </label>
              <input type="text" v-model="signup.name" required autocomplete="off" />
            </div>
          </div>
    
          <div class="field-wrap">
            <label>
              Email Address<span class="req">*</span>
            </label>
            <input type="email" v-model="signup.email" required autocomplete="off"/>
          </div>
          
          <div class="field-wrap">
            <label>
              Set A Password<span class="req">*</span>
            </label>
            <input type="password" v-model="signup.pwd" required autocomplete="off"/>
          </div>
          <p style="color:red">{{ msg }}</p>
          <button type="submit" v-on:click="sign()"> SIGN UP! </button>
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
            <br>
            <p style="color:red">{{ lmsg }}</p>
          </div>   
      </div>   
      </div><!-- tab-content -->
    </div> <!-- /form -->
</template>

<script>
import axios from 'axios'
export default{
  data(){
      return{
          login_form:{
              email:'',
              pwd:'',
              isChecked:false
          },
          signup:{
            email:'',
            name:'',
            pwd:''
          },
          msg:'',
          lmsg:''
      }
  },
  methods: {
    async sign(){
    console.log(this.signup,"Testing")
    try{
      await axios.post('http://127.0.0.1:5000/usersignup', {
      email: this.signup.email,
      pwd:this.signup.pwd,
      name:this.signup.name
    }).then(response => { console.log(response.data); this.msg=response.data;})
    }
    catch(error){
      console.log(error,"Error")
    }
  },
  async login(){
        if(this.login_form.isChecked){ // Admin Login
          try {
            await axios.post('http://127.0.0.1:5000/logi',{
                  email: this.login_form.email,
                  pwd:this.login_form.pwd,
                  admin:this.login_form.isChecked
              }).then(response =>{ 
                  console.log("resp", response);
                  if(response.data=='Login Failed'){
                    this.lmsg='Invalid Credentials, Login Failed!, Try Again'
                  }
                  else if(response.data['user']){
                    this.lmsg='Not an Admin!'
                  }
                  else{
                  localStorage.setItem('admin-access-token', response.data.at)
                  localStorage.setItem('admin_name',response.data.admin)
                  this.$router.push('/adashboard')

                  }

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
                  if(response.data=='Login Failed'){
                    this.lmsg='Invalid Credentials, Login Failed!, Try Again'
                  }
                  else{
                  localStorage.setItem('user-access-token', response.data.at)
                  localStorage.setItem('user_name',response.data.user)
                  this.$router.push('/dashboard')
                  }
                })
          }
          catch(error){
              console.log("Login Failed", error)
          }
        }
      }
  }
}
</script>