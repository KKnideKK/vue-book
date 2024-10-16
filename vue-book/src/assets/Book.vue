<template>
    <div class="book-management">
        <div class="header">
            <h1>图书管理系统</h1>
            <div class="search-input">
                <input class="input1" type="text" placeholder="请输入id" v-model="searchText">
                <button class="button2" @click="fetchBooks_id">搜索</button>
            </div>
            <div class="user-account" @click="toggleUserMenu">
                {{ phoneNumber }}
                <div :class="['user-menu', { active: userMenuVisible }]">
                    <button @click="toggleUserMenu">借阅历史</button>
                    <button @click="logout">退出</button>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="category">
                <ul>
                    <li><h2>图书分类</h2></li>
                    <li><button class="button1" @click="selectedCategory = '全部'; fetchBooks()">全部</button></li>
                    <li><button class="button1" @click="selectedCategory = '科学'; fetchBooks()">科学</button></li>
                    <li><button class="button1" @click="selectedCategory = '机械'; fetchBooks()">机械</button></li>
                    <li><button class="button1" @click="selectedCategory = '历史'; fetchBooks()">历史</button></li>
                    <li><button class="button1" @click="selectedCategory = '哲学'; fetchBooks()">哲学</button></li>
                    <li><button class="button1" @click="selectedCategory = '计算机'; fetchBooks()">计算机</button></li>
                    <li><button class="button1" @click="selectedCategory = '生活'; fetchBooks()">生活</button></li>
                    <li><button class="button1" @click="selectedCategory = '农业'; fetchBooks()">农业</button></li>
                    <li><button class="button1" @click="selectedCategory = '体育'; fetchBooks()">体育</button></li>
                    <li><button class="button1" @click="selectedCategory = '医学'; fetchBooks()">医学</button></li>
                    <li><button class="button1" @click="selectedCategory = '音乐'; fetchBooks()">音乐</button></li>
                    <li><button class="button1" @click="selectedCategory = '绘画'; fetchBooks()">绘画</button></li>
                    <li><button class="button1" @click="selectedCategory = '建筑'; fetchBooks()">建筑</button></li>
                    <li><button class="button1" @click="selectedCategory = '服装'; fetchBooks()">服装</button></li>
                    <li><button class="button1" @click="selectedCategory = '动漫'; fetchBooks()">动漫</button></li>
                    <li><button class="button1" @click="selectedCategory = '文学'; fetchBooks()">文学</button></li>
                </ul>
            </div>

            <div class="book-display">
                <h2>图书展示</h2>
                <div class="books">
                    <div class="book" v-for="book in books" :key="book.id">
                        <h3>{{ book.title }}</h3>
                        <p>作者: {{ book.author }}</p>
                        <p>分类: {{ book.category }}</p>
                        <p>简介: {{ book.description }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            phoneNumber:'', // 接收账号信息
            userMenuVisible: false,
            books: [],
            selectedCategory: '全部',
            searchText: '',
        };
    },
    mounted() {
        this.phoneNumber = this.$route.query.phone_number;
        this.fetchBooks();
    },
    
    methods: {
        fetchBooks_id() {
            let url = `http://localhost:5000/api/book/book_id?searchText=${this.searchText}`;
            axios.get(url)
            .then(response => {
                this.books = [response.data]; // 假设返回的书籍数据是单个对象
            })
            .catch(error => {
                console.error('获取书籍信息失败:', error);
            });
        },
        fetchBooks() {
            let url = 'http://localhost:5000/api/books';
            if (this.selectedCategory !== '全部') {
                url += `?category=${this.selectedCategory}`;
            }
            axios.get(url)
            .then(response => {
                this.books = response.data;
            })
            .catch(error => {
                console.error('获取书籍信息失败:', error);
            });
        },
        toggleUserMenu() {
            this.userMenuVisible = !this.userMenuVisible;
        },
    }
}
</script>

<style>
.input1 {
    width: 200px; /* 设置输入框宽度 */
    padding: 10px; /* 内部填充 */
    margin-right: 10px; /* 右侧间距 */
    border: 1px solid #ccc; /* 边框 */
    border-radius: 5px; /* 圆角 */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); /* 轻微阴影效果 */
    transition: border-color 0.3s; /* 边框颜色过渡效果 */
}

.input1:focus {
    border-color: #007bff; /* 聚焦时边框颜色 */
    outline: none; /* 去掉默认的轮廓线 */
}

.button2 {
    background-color: #007bff; /* 背景颜色 */
    color: white; /* 文字颜色 */
    padding: 10px 15px; /* 内部填充 */
    border: none; /* 去掉边框 */
    border-radius: 5px; /* 圆角 */
    cursor: pointer; /* 鼠标指针为手指 */
    transition: background-color 0.3s; /* 背景颜色过渡效果 */
}

.button2:hover {
    background-color: #0056b3; /* 悬停时背景颜色 */
}
body {
    font-family: 'Arial', sans-serif;  /* 使用简约的字体 */
    background-color: #f5f5f5;  /* 轻柔的背景色 */
    margin: 0; 
    padding: 20px; 
    color: #333;  /* 字体颜色 */
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background-color: #ffffff;  /* 白色背景 */
    border-radius: 6px;  /* 圆角 */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);  /* 轻微阴影 */
}

ul {
    list-style-type: none;  /* 去掉圆点 */
    padding: 0;  /* 去掉内边距 */
    margin: 0;  /* 去掉外边距 */
}

.button1 {
    display: block;  /* 块级元素 */
    width: 100%;  /* 宽度为100% */
    padding: 10px;  /* 内边距 */
    margin-bottom: 10px;  /* 外边距 */
    background-color: #007bff;  /* 主要按钮颜色 */
    border: none;  /* 去掉边框 */
    border-radius: 5px;  /* 圆角 */
    color: white;  /* 字体颜色 */
    cursor: pointer;  /* 鼠标指针为手指 */
    transition: background-color 0.3s;  /* 添加过渡效果 */
}

.button1:hover {
    background-color: #0056b3;  /* 悬停颜色 */
}

.user-account {
    position: relative;  /* 设置为相对定位 */
    display: flex;  /* 使用flex布局 */
    align-items: center;  /* 居中对齐内容 */
    width: 150px;  /* 固定宽度 */
    border: 1px solid #ddd;  /* 边框 */
    border-radius: 5px;  /* 圆角 */
    padding: 10px;  /* 内边距 */
    background-color: #ffffff;  /* 白色背景 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* 轻微阴影 */
    cursor: pointer;  /* 鼠标指针为手指 */
}

.user-menu {
    display: none;  /* 默认隐藏 */
    position: absolute;  /* 绝对定位 */
    top: 100%;  /* 菜单位于用户账号下方 */
    left: 0;  /* 左对齐 */
    width: 160px;  /* 固定宽度 */
    border: 1px solid #ddd;  /* 边框 */
    background-color: #ffffff;  /* 白色背景 */
    z-index: 1000;  /* 使菜单在其他控件之上 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* 轻微阴影 */
}

.user-menu.active {
    display: flex;  /* 点击时显示菜单 */
    flex-direction: column;  /* 按钮竖直排列 */
}

.user-menu button {
    margin-top: 5px;  /* 添加按钮间的间距 */
    width: 100%;  /* 按钮宽度设置为100% */
    background-color: transparent;  /* 背景透明 */
    border: none;  /* 去掉边框 */
    color: #007bff;  /* 按钮文本颜色 */
    cursor: pointer;  /* 鼠标指针为手指 */
}

.user-menu button:hover {
    text-decoration: underline;  /* 悬停时文本下划线 */
}

.content {
    display: flex;
    margin-top: 20px;  /* 顶部间距 */
}

.category {
    margin: 10px;
    width: 250px;  /* 固定宽度 */
    border: 1px solid #ddd;  /* 边框 */
    border-radius: 5px;  /* 圆角 */
    padding: 10px;
    background-color: #ffffff;  /* 白色背景 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* 轻微阴影 */
}

.book-display {
    width: 60%;  /* 固定宽度 */
    background-color: #ffffff;  /* 白色背景 */
    border-radius: 5px;  /* 圆角 */
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* 轻微阴影 */
}

.book {
    border: 1px solid #ddd;  /* 边框 */
    border-radius: 5px;  /* 圆角 */
    padding: 15px;  /* 内部填充 */
    margin-bottom: 15px;  /* 底部间距 */
    background-color: #f9f9f9;  /* 每本书的背景色 */
}

</style>
