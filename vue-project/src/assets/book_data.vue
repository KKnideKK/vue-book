<template>
    <div>
        <h1>书籍详情</h1>
        <div v-if="book">
            <img v-if="book.imageUrl" :src="book.imageUrl" alt="书籍封面" style="width: 100px; height: auto; border-radius: 4px; margin-right: 10px;">
            <h2>书名: {{ book.title }}</h2>
            <p>书籍id: {{ book.id }}</p>
            <p>作者: {{ book.author }}</p>
            <p>分类: {{ book.category }}</p>
            <p>存放位置：{{ book.location }}</p>
            <p>借阅量: {{ book.borrowing_times }}</p>
            <p>书籍简介: {{ book.description }}</p>
        </div>
        <div v-else>
            <p>未找到书籍详情。</p>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            book: null // 用于存储书籍信息
        };
    },
    mounted() {
        // 从路由的查询参数中获取 bookdata
        const bookData = this.$route.query.bookdata;
        if (bookData) {
            // 将 JSON 字符串解析为对象
            this.book = JSON.parse(bookData);
        }
    },
};
</script>

<style scoped>
/* 页面总体样式 */
div {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9; /* 柔和的背景色 */
    color: #333;
    padding: 20px;
    border-radius: 8px; /* 添加圆角 */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
    max-width: 600px; /* 限制最大宽度 */
    margin: auto; /* 居中对齐 */
}

/* 标题样式 */
h1 {
    text-align: center;
    color: #6a5acd; /* 深紫色 */
    margin-bottom: 20px; /* 标题与内容间的间距 */
}

/* 图书封面样式 */
img {
    width: 100px;
    height: auto;
    border-radius: 4px;
    margin-right: 10px;
}

/* 副标题样式 */
h2 {
    margin-top: 0;
    color: #5c5c5c; /* 深灰色 */
}

/* 段落样式 */
p {
    margin: 10px 0; /* 上下的间距 */
    line-height: 1.5; /* 增加行间距 */
    font-size: 16px; /* 字体大小 */
}

/* 样式改进 - 在段落中增加不同的背景色 */
p:nth-of-type(odd) {
    background-color: #e9ecef; /* 浅灰色背景 */
    padding: 10px; /* 内边距 */
    border-radius: 4px; /* 圆角 */
}

/* 提供更好的视觉分隔 */
p:not(:last-child) {
    border-bottom: 1px solid #ccc; /* 底部边框 */
    padding-bottom: 10px; /* 添加底部填充 */
}
</style>
