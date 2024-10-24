<template>
    <div class="login-container">  
      <h2>用户登录</h2>  
      <form @submit.prevent="login">  
        <div>  
          <label for="phone_number">账号:</label>  
          <input type="text" id="phone_number" v-model="phone_number" required>  
        </div>  
        <div>  
          <label for="password">密码:</label>  
          <input type="password" id="password" v-model="password" required>  
        </div>  
        <button type="submit">登录</button>  
        <router-link to="/Admin" class="home-link">管理员</router-link>
        <router-link to="/get_user" class="home-link">注册</router-link>
        <router-link to="/get_itid" class="home-link">验证码登录</router-link>
      </form>  
    </div>
</template>
<script>  
import axios from 'axios'; 

export default {  
  data() {  
    return {  
      phone_number: '',  
      password: ''  
    };  
  },  
  methods: {
    login() {  
      axios.post('http://localhost:5000/userv', { // 替换为你的后端API地址
        phone_number: this.phone_number,
        password: this.password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
      .then(response => {
        if (response.data.success) {
          alert(response.data.message);
          this.$router.push({ 
              path: '/Book', 
            query: { phone_number: this.phone_number }  // 传递账号信息
             } ); //验证成功跳转页面

        } 
        else {
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