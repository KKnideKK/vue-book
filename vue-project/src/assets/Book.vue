<template>
    <div class="book-management">
        <div class="header">
            <h1>图书管理系统</h1>
            <div class="search-input">
                <input class="input1" type="text" v-model="searchText" placeholder="请输入id"/>
                <button class="button2" @click="fetchBooks_id">搜索</button>
            </div>
            <div>
                <button class="buttontop10" @click="fetchBooks_top10">top10</button>
            </div>
            <div class="user-account" @click="toggleUserMenu">
                {{ phoneNumber }}
                <div class="user-menu" :class="{ active: userMenuActive }">
                    <button class="buttons" @click="logout">注销</button>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="category">
                <h2><li>分类</li></h2>
                <ul>
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
                        <div class="book-info">
                            <img class="book-cover" :src="book.imageUrl" alt="书籍封面">
                            <div class="book-detail">
                                <h3>{{ book.title }}</h3>
                                <p>书籍id: {{ book.id }}</p>
                                <p>作者: {{ book.author }}</p>
                                <p>分类: {{ book.category }}</p>
                                <p>借阅次数: {{ book.borrowing_times }}</p>
                                <button class="button2" @click="getBookDetail(book)">查看详情</button>
                            </div>
                        </div>
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
            phoneNumber:'', 
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

        getBookDetail(book) { // 点击查看详情按钮，跳转到详情页面
    const bookData = JSON.stringify(book); // 转换为 JSON 字符串
    this.$router.push({ path: '/book_data', query: { bookdata: bookData } });},

        fetchBooks_top10() {// 获取top10书籍信息
            let url = 'http://localhost:5000/api/books/top10';
            axios.get(url)
            .then(response => {
                this.books = response.data;
            })
            .catch(error => {
                console.error('获取书籍信息失败:', error);
            });
        },
        fetchBooks_id() {// 获取指定id书籍信息
            let url = `http://localhost:5000/api/book/book_id?searchText=${this.searchText}`;
            axios.get(url)
            .then(response => {
                this.books = [response.data]; // 假设返回的书籍数据是单个对象
            })
            .catch(error => {
                console.error('获取书籍信息失败:', error);
            });
        },
        fetchBooks() {// 获取指定分类书籍信息   
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
        toggleUserMenu() {// 点击用户账号按钮，显示/隐藏菜单    
            this.userMenuVisible = !this.userMenuVisible;
        },
    }
}
</script>

<style scoped>
.book-management {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    color: #333;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: #6a5acd;
    color: white;
}

.search-input input {
    padding: 10px;
    margin-right: 10px;
    border: none;
    border-radius: 5px;
}

.button2 {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #ff7f50;
    color: white;
    cursor: pointer;
}

.button2:hover {
    background-color: #ff6347;
}

.buttontop10 {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #4682b4;
    color: white;
    cursor: pointer;
}

.buttontop10:hover {
    background-color: #5f9ea0;
}

.user-account {
    position: relative;
    cursor: pointer;
}

.user-menu {
    display: none;
    position: absolute;
    top: 50px;
    right: 0;
    background-color: #fff;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    z-index: 1000;
}

.user-menu.active {
    display: block;
}

.buttons {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #dc143c;
    color: white;
    cursor: pointer;
    width: 100%;
    text-align: left;
}

.buttons:hover {
    background-color: #c71540;
}

.content {
    display: flex;
    padding: 20px;
}

.category {
    flex: 1;
    margin-right: 20px;
}

.category ul {
    list-style-type: none;
    padding: 0;
}

.category li {
    margin-bottom: 10px;
}

.button1 {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #4682b4;
    color: white;
    cursor: pointer;
    width: 100%; /* 统一按钮宽度 */
}

.button1:hover {
    background-color: #5f9ea0;
}

.book-display {
    flex: 3;
}

.books {
    display: flex;
    flex-wrap: wrap;
}

.book {
    width: calc(50% - 20px); /* 调整每本书的宽度 */
    margin: 10px; /* 增加间距 */
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    overflow: hidden; /* 确保内容不会溢出 */
}

.book-info {
    display: flex;
    align-items: center; /* 垂直居中对齐 */
}

.book-cover {
    width: 50%; /* 让图片占满整个div */
    height: auto; /* 保持图片比例 */
    object-fit: cover; /* 确保图片覆盖整个div */
}

.book-detail {
    padding: 10px; /* 增加内边距 */
}

.book-detail h3 {
    margin: 0 0 10px 0; /* 减少标题和内容的间距 */
}
</style>
