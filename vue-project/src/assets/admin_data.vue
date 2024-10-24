<template>
    <div class="admin-data">
      <h1>图书管理界面</h1>
      <div class="admin-container">
        <div class="admin-menu">
          <div class="search-box">
            <h2>图书搜索</h2>
            <div class="search-input">
                <input type="text" placeholder="请输入id" v-model="searchText">
                <button @click="fetchBooks">搜索</button>
            </div>
            <div class="books">
                <div v-for="book in books" :key="book.id" class="book">
                        <h3>{{ book.title }}</h3>
                        <p>作者: {{ book.author }}</p>
                        <p>分类: {{ book.category }}</p>
                        <p>简介: {{ book.description }}</p>
                        <button @click="deleteBook(book)">删除</button>
                </div>
            </div>
          </div>
          <div class="add-book">
            <h2>图书添加</h2>
            <form @submit.prevent="addBook">

                <label for="id">ID:</label>
                <input type="text" id="id" name="id" v-model="newBook.id" required>
                <label for="title">书名:</label>
                <input type="text" id="title" name="title" v-model="newBook.title" required>
                <label for="author">作者:</label>
                <input type="text" id="author" name="author" v-model="newBook.author" required>
                <label for="category">分类:</label>
                <input type="text" id="category" name="category" v-model="newBook.category" required>
                <label for="location">存放位置：</label>
                <input type="text" id="location" name="location" v-model="newBook.location" required>
                <label for="description">简介:</label>
                <textarea id="description" name="description" v-model="newBook.description" required></textarea>
                <label for="image">封面图片:</label>
                        <input type="file" id="image" @change="onImageChange" accept="image/*">

                        <!-- 显示选择的图片 -->
                        <div v-if="imagePreview">
                            <h3>预览图片:</h3>
                            <img :src="imagePreview" alt="书籍封面" style="width: 15%; height: auto;">
                        </div>
                <button type="submit">添加</button>
            </form>
          </div>
        </div>
        <div class="user-manage">
          <h2>查看用户</h2>
          <input type="text" placeholder="请输入用户名" v-model="searchTextx">
          <button @click="fetchUsers">搜索</button>
          <h3>{{ userdata }}</h3>
          <div v-for="user in users" :key="user.id" class="user">
                        <h3>{{ user.account }}</h3>
                        <p>借阅书籍: {{ user.title }}  书籍id: {{ user.id }}</p>
                        <button @click="returnBook(user)">归还书籍</button>
            </div>
            <button @click="borrowBook(user)">借阅书籍</button>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            users: [],
            books: [],
            userdata: '',
            searchTextx: '',
            searchText: '',
            newBook: {
                id: '',
                title: '',
                author: '',
                category: '',
                description: '',
                location: '',
                imageUrl: ''
            },
            imagePreview: null,
            imageFile: null // 存储图片文件
        };
    },
    methods: {

        onImageChange(event) {
            this.imageFile= event.target.files[0]; // 获取选择的文件
    if (this.imageFile) {
        const reader = new FileReader(); // 创建 FileReader 实例
        reader.onload = (e) => {
            this.imagePreview = e.target.result; // 将读取到的结果赋值给 imagePreview
        };
        reader.readAsDataURL(this.imageFile); // 读取文件
    }
    },

        fetchBooks() {
            let url = `http://localhost:5000/api/book/book_id?searchText=${this.searchText}`;
            axios.get(url)
            .then(response => {
                this.books = [response.data]; 
            })
            .catch(error => {
                console.error('获取书籍信息失败:', error);
            });
        },
        addBook() {
            let url = 'http://localhost:5000/api/newbook';
    const formData = new FormData(); // 创建 FormData 实例

    // 将书籍信息添加到 FormData
    formData.append('id', this.newBook.id);
    formData.append('title', this.newBook.title);
    formData.append('author', this.newBook.author);
    formData.append('category', this.newBook.category);
    formData.append('location', this.newBook.location);
    formData.append('description', this.newBook.description);
    
    if (this.imageFile) {
        formData.append('image', this.imageFile);
    }

    axios.post(url, formData, {
        headers: {
            'Content-Type': 'multipart/form-data' 
        }
    })
    .then(response => {
        console.log('书籍添加成功:', response.data);
        // 重置表单数据
        this.newBook = {
            id: '',
            title: '',
            author: '',
            category: '',
            description: '',
            location: '',
        };
        this.imageFile = null; // 重置图片文件
        this.imagePreview = null; // 重置预览
    })
    .catch(error => {
        console.error('添加书籍失败:', error);
    });
        },
        deleteBook(books) {
            if (confirm('您确定要删除这本书吗？')) {
        fetch(`http://localhost:5000/api/deletebook/${books.id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不是 OK');
            }
            return response.json();  // 将响应解析为 JSON
        })
        .then(data => {
            alert(data.message);  // 显示返回的消息
        })
        .catch(error => {
            console.error('发生错误:', error);  // 处理错误
            alert('删除书籍时发生错误');
        });
    }
        },
        fetchUsers() {
            let url = `http://localhost:5000/api/book/user_id?searchTextx=${this.searchTextx}`;
            axios.get(url)
            .then(response => {
                this.userdata="";
                this.users = response.data; 
            })
            .catch(error => {
                console.error('获取用户信息失败:', error);
                this.userdata = '无该用户信息。';
                this.users = [];
            });
        },
        //
        borrowBook() {
    const bookId = prompt('请输入书籍的 ID：');
    if (!bookId) {
        alert('书籍 ID 不能为空！');
        return; // 如果未输入 ID，则退出函数
    }

    // 提示用户输入书籍的名称
    const bookTitle = prompt('请输入书籍的名称：');
    if (!bookTitle) {
        alert('书籍名称不能为空！');
        return; // 如果未输入名称，则退出函数
    }
    
    // 使用模板字符串拼接 URL
    let url = `http://localhost:5000/api/borrowbook`;

    axios.post(url, { title: bookTitle, bookdata: bookId,account:this.searchTextx })  // 将 bookId 放入请求体
    .then(response => {
        // Axios 的响应对象没有 ok 属性
        if (response.status !== 200) {
            throw new Error('网络响应不是 OK');
        }
        return response.data;  // 将响应解析为 JSON
    })
    .then(data => {
        alert(data.message);  // 显示返回的消息
    })
    .catch(error => {
        console.error('发生错误:', error);  // 处理错误
    });
},
        returnBook() {
        const bookId = prompt('请输入书籍的 ID：');
    if (!bookId) {
        alert('书籍 ID 不能为空！');
        return; // 如果未输入 ID，则退出函数
    }

       let url =`http://localhost:5000/api/returnbook`;
       axios.post(url, { id: bookId,account:this.searchTextx })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不是 OK');
            }
            return response.json();  // 将响应解析为 JSON
        })
        .then(data => {
            alert(data.message);  // 显示返回的消息
        })
        .catch(error => {
            console.error('发生错误:', error);  // 处理错误
        });
    }
        },
    }
</script>

<style>
body {
    font-family: 'Arial', sans-serif; /* 更现代的字体 */
    background-color: #f4f4f4; /* 整个页面的背景色 */
    margin: 0;
    padding: 20px;
}

.admin-container {
    display: flex; /* 使用flex布局，让admin-menu和user-manage并排显示 */
    gap: 20px; /* 组件之间的间距 */
}

.admin-menu, .user-manage {
    border-radius: 8px; /* 边框圆角 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 投影效果 */
    padding: 20px; /* 内部填充 */
    background-color: white; /* 背景色为白色 */
}

.admin-menu {
    display: flex;
    flex-direction: column; /* 垂直排列search-box和add-book */
    width: 70%; /* 设置admin-menu的宽度 */
}

.search-box {
    margin-bottom: 20px; /* 与添加书籍框的间距 */
    background-color: #f8d7da; /* 柔和的背景颜色 */
    padding: 15px; /* 内部填充 */
    border-radius: 8px; /* 边框圆角 */
}

.add-book {
    margin-top: 20px; /* 与搜索框的间距 */
    background-color: #d4edda; /* 柔和的背景颜色 */
    padding: 15px; /* 内部填充 */
    border-radius: 8px; /* 边框圆角 */
}

input[type="text"], 
input[type="submit"], 
textarea {
    width: 100%; /* 使输入框宽度占满父容器 */
    padding: 10px; /* 内部填充 */
    margin: 8px 0; /* 上下外边距 */
    border: 1px solid #ccc; /* 边框样式 */
    border-radius: 4px; /* 边框圆角 */
    box-sizing: border-box; /* 计算宽度时包含边框 */
}

button {
    background-color: #007bff; /* 主要按钮颜色 */
    color: white; /* 字体颜色 */
    padding: 10px 15px; /* 内部填充 */
    border: none; /* 去除边框 */
    border-radius: 4px; /* 边框圆角 */
    cursor: pointer; /* 鼠标悬停时更改指针 */
}

button:hover {
    background-color: #0056b3; /* 悬停时的颜色 */
}

.user-manage {
    flex: 1; /* 让user-manage自动适应剩余空间 */
    background-color: #e9ecef; /* 更柔和的背景色 */
    padding: 20px; /* 内部填充 */
    border-radius: 8px; /* 边框圆角 */
}

.user {
    margin-bottom: 15px; /* 每个用户之间的间距 */
    padding: 10px; /* 内部填充 */
    background-color: white; /* 用户信息背景 */
    border-radius: 5px; /* 边框圆角 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 投影效果 */
}
</style>
