<template>  
  <div class="main-container">
    <router-view></router-view>  
  </div>
  <footer class="footer">
    <p>卢汉超的Vue项目</p>
  </footer>
</template>  

<style>
.main-container {
  padding: 20px;
  background-color: #f9f9f9;
  min-height: 80vh; /* 确保主容器占满可视区域 */
}

.footer {
  text-align: center;
  padding: 10px;
  background-color: #282c34; /* 深色背景 */
  color: white; /* 白色字体 */
  position: relative;
  bottom: 0;
  width: 100%;
}
</style>
