<template>
    <div class="login-container">  
      <h2>用户登录</h2>  
      <form @submit.prevent="login">  
        <div>  
          <label for="phone_number">邮箱:</label>  
          <input type="text" id="phone_number" v-model="phone_number" required>  
        </div>  
        <div>  
          <label for="code">验证码:</label>  
          <input type="password" id="code" v-model="code" required>  
        </div>  
        <button type="button" @click="sendCode">发送验证码</button>
        <button type="submit" @click="login">登录</button>  
        <router-link to="/Admin" class="home-link">管理员</router-link>
        <router-link to="/get_user" class="home-link">注册</router-link>
        <router-link to="/" class="home-link">密码登录</router-link>
      </form>  
    </div>
</template>
<script>  
import axios from 'axios'; 

export default {  
  data() {  
    return {  
      phone_number: '',  
      code: ''  
    };  
  },  
  methods: {
    sendCode() {
      //验证账号是否存在
      axios.post('http://localhost:5000/api/check-username', {
        phone_number: this.phone_number
    })
    .then(response => {
      if (response.data.success) {
        // 如果账号存在，则发送验证码
        return axios.post('http://localhost:5000/api/send-code', {
          phone_number: this.phone_number
        });
      } else {
        // 如果账号不存在，提示用户
        alert('该账号不存在，请检查您的用户名。');
      }
    })
    .then(response => {
      if (response.data.success) {
          alert(response.data.message);
          // 假设验证成功，你可以使用Vue Router进行页面跳转  
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('请求错误:', error);
    });

    },
    login() {  
      // 这里可以添加登录逻辑，比如发送请求到后端验证  
      axios.post('http://localhost:5000/api/verify', { // 替换为你的后端API地址
        phone_number: this.phone_number,
        code: this.code
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
      .then(response => {
        if (response.data.success) {
          alert(response.data.message);
          this.$router.push('/Book');  //验证成功跳转页面 

        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('请求错误:', error);
      });
    }  
  }  
}
</script>  
  
<style scoped>  
.login-container {  
  max-width: 300px;  
  margin: 100px auto;  
  padding: 20px;  
  border: 1px solid #ccc;  
  border-radius: 5px;  
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);  
}  
  
.login-container h2 {  
  text-align: center;  
  margin-bottom: 20px;  
}  
  
.login-container form div {  
  margin-bottom: 15px;  
}  
  
.login-container label {  
  display: block;  
  margin-bottom: 5px;  
}  
  
.login-container input[type="text"],  
.login-container input[type="password"] {  
  width: 100%;  
  padding: 8px;  
  box-sizing: border-box;  
}  
  
.login-container button {  
  width: 100%;  
  padding: 10px;  
  margin-top: 10px;
  background-color: #4CAF50;  
  color: white;  
  border: none;  
  border-radius: 5px;  
  cursor: pointer;  
}  
  
.login-container button:hover {  
  background-color: #45a049;  
}  

.home-link {
  display: inline-block;
  margin-top: 10px;
  margin-right: 10px;
  padding: 10px 15px;
  background-color: #45a049; /* 按键背景 */
  color: white; /* 白色文字 */
  border-radius: 5px; /* 圆角 */
  text-decoration: none; /* 去掉下划线 */
  transition: background-color 0.3s; /* 添加过渡效果 */
}

.home-link:hover {
  background-color: #a6f606; /* 悬停时变深的粉色 */
}
</style>