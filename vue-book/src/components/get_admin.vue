<template>
    <div class="login-container">  
      <h2>管理员注册</h2>  
      <form @submit.prevent="login">  
        <div>  
          <label for="username">账号:</label>  
          <input type="text" id="username" v-model="username" required>  
        </div>  
        <div>  
          <label for="password">密码:</label>  
          <input type="password" id="password" v-model="password" required>  
        </div>  
        <div>  
          <label for="password">内部指令:</label>  
          <input type="password" id="password" v-model="password" required>  
        </div>  
        <button type="submit">登录</button>  
        <router-link to="/Admin" class="getadmin-link">返回登录页面</router-link>
      </form>  
    </div>
</template>
<script>  
import axios from 'axios'; 

export default {  
  data() {  
    return {  
      username: '',  
      password: ''  
    };  
  },  
  methods: {
    login() {  
      // 这里可以添加登录逻辑，比如发送请求到后端验证  
      axios.post('http://localhost:5000/login', { // 替换为你的后端API地址
        username: this.username,
        password: this.password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
      .then(response => {
        // 假设返回的数据中包含一个success字段表示登录是否成功
        if (response.data.success) {
          alert('登录成功');
          // 假设验证成功，你可以使用Vue Router进行页面跳转  
          this.$router.push('/Book');  
        } else {
            alert('登录失败');
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

.getadmin-link {
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

.getadmin-link:hover {
  background-color: #a6f606; /* 悬停时变深的粉色 */
}
</style>