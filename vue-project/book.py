import os
from sched import scheduler
import schedule # type: ignore
import time
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # 跨域
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask, jsonify
import redis

app = Flask(__name__)
CORS(app)#跨域连接
###################################mysql连接数据库#################################

# 数据库配置
db_config = {
    'host': 'localhost', # 数据库主机
    'user': 'root',  # 数据库用户名
    'password': '123456', # 数据库密码
    'database': 'book'   # 数据库名称
}


###############################mysql数据库连接配置###################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/book'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 存储哈希密码

class Book(db.Model):
    __tablename__ = 'book'  # 替换为你的表名
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    borrowing_times = db.Column(db.Integer, default=0)  # 借阅次数
    location = db.Column(db.String(100), nullable=True)  # 书籍位置
    imageUrl = db.Column(db.String(255), nullable=True)  # 用于存储书籍封面图片的路径

class Borrowing(db.Model):
    __tablename__ = 'book_borrowing'  # 替换为你的表名
    id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    account = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255))
#############################redis配置##################################
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

######################################获取排行榜接口##################
@app.route('/api/books/top10', methods=['GET'])
def get_top10_books():
    try:
        # 从Redis获取借阅次数前十的书籍ID
        book_ids = redis_client.get('top_borrowed_book_ids')
        
        if book_ids is None:
            return jsonify({"error": "没有找到前十本书籍的信息。"}), 404

        # 将获取的ID列表转换为Python列表
        book_ids = list(map(int, book_ids.decode('utf-8').split(',')))

        # 根据书籍ID查询详细信息
        top_books = db.session.query(Book).filter(Book.id.in_(book_ids)).order_by(desc(Book.borrowing_times)).all()
        
        # 将结果转换为字典格式
        books_data = [{"id": book.id,"category":book.category,"description":book.description,  "title": book.title, "author": book.author, "borrowing_times": book.borrowing_times} for book in top_books]

        return jsonify(books_data), 200  # 返回书籍信息及 HTTP 200 状态码
    except Exception as e:
        return jsonify({"error": "发生错误，无法获取书籍信息。"}), 500  # 返回错误信息及 HTTP 500 状态码


######################################更新排行榜定时任务##############
def store_top_borrowed_books():
    # 查询借阅次数前十的书籍ID
    top_books = db.session.query(Book.id).order_by(desc(Book.borrowing_times)).limit(10).all()
    
    # 将结果存入Redis
    book_ids = [book.id for book in top_books]
    
    # 在存入新的ID之前，先删除旧的键值对
    redis_client.delete('top_borrowed_book_ids')

    # 存入Redis，使用一个键（例如 'top_borrowed_book_ids'）存储这些ID
    redis_client.set('top_borrowed_book_ids', ','.join(map(str, book_ids)))

# 在适当的地方调用这个函数，例如在接口处理完之后，或者定时任务中
def schedule_job():
    schedule.every(1).minutes.do(run_store_top_borrowed_books)  # 设置定时任务
    while True:
        schedule.run_pending()
        time.sleep(10)  # 等待并检查是否有任务需要执行

def run_store_top_borrowed_books():
    with app.app_context():  # 创建应用上下文
        store_top_borrowed_books()  # 调用函数

# 启动定时任务的线程
thread = threading.Thread(target=schedule_job)
thread.start()



#############################归还书籍的接口##################################
@app.route('/api/returnbook', methods=['POST'])
def returnbook():
    data=request.json
    account=data.get('account')
    id=data.get('id')
    if not account or not id:
        return jsonify({'message': '缺少必要参数'}), 400 
    book_to_return = Borrowing.query.filter_by(account=account, id=id).first()

    if not book_to_return:
        return jsonify({'message': '未找到对应的书籍记录'}), 404

    # 删除对应的记录
    db.session.delete(book_to_return)
    db.session.commit()

    return jsonify({'message': '书籍归还成功'}), 200
    
#############################添加借阅书籍的接口##################################
@app.route('/api/borrowbook', methods=['POST'])
def borrow_book():
    # 从请求体中获取数据
    data = request.json
    account = data.get('account')
    title = data.get('title')
    bookdata = data.get('bookdata')
    # 检查是否提供了必要的信息
    if not account or not title or not bookdata:
        return jsonify({'message': '缺少必要参数'}), 400 

    # 创建借阅记录
    new_borrowing = Borrowing(account=account, title=title, id=bookdata)
    
    try:
        db.session.add(new_borrowing)  # 将新的借阅记录添加到数据库会话
        # 借阅次数加1
        db.session.execute(
    Book.__table__.update().where(Book.id == bookdata).values(borrowing_times=func.coalesce(Book.borrowing_times, 0) + 1))
        db.session.commit()  # 提交会话
        return jsonify({'message': '借阅成功！'}), 201  # 返回成功消息
    except Exception as e:
        db.session.rollback()  # 回滚会话
        print(f'发生错误: {str(e)}')
        return jsonify({'message': '借阅失败，发生错误！'}), 500  # 返回失败消息


##########################################借阅记录接口###############################
@app.route('/api/book/user_id', methods=['GET'])
def book_user():
    searchTextx = request.args.get('searchTextx')  # 获取搜索文本
    book_borrowingv = Borrowing.query.filter(Borrowing.account == searchTextx).all()  # 查询匹配的记录
    if book_borrowingv:
        # 将记录信息转换为字典格式
        borrowing_data = [{
            'id': borrowing.id,  # 假设有一个 ID 字段
            'account': borrowing.account,  # 用户账号
            'title': borrowing.title  # 书籍名称
        } for borrowing in book_borrowingv]
        return jsonify(borrowing_data), 200  # 返回借阅记录信息
    else:
        return jsonify({'message': '没有找到匹配的借阅记录'}), 404  # 找不到记录的处理


####################################删除书籍接口############################
@app.route('/api/deletebook/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book_to_delete = Book.query.get(book_id)
    
    if book_to_delete is None:
        return jsonify({'message': '图书未找到！'}), 404  # 如果书籍未找到，返回404错误

    db.session.delete(book_to_delete)  # 删除书籍
    db.session.commit()  # 提交事务

    return jsonify({'message': '图书删除成功！'}), 200

####################################添加书籍接口############################
@app.route('/api/newbook', methods=['POST'])
def add_new_book():
    if 'image' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400
    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    category = request.form['category']
    description = request.form['description']
    location=request.form['location']

    # 获取上传的文件（图片）
    image = request.files.get('image')  # 使用 .get() 方法避免 KeyError
    if image.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    # 数据验证
    new_book = Book(
        id=id,
        title=title,
        author=author,
        category=category,
        description=description,
        location=location
    )

    # 如果有上传的图片，处理图片
    upload_folder = 'uploads/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)  # 创建目录

    # 处理图片保存
    if image:
        image_path = os.path.join(upload_folder, image.filename)  # 构建文件路径
        image.save(image_path)  # 保存上传的图片
        new_book.imageUrl = image_path

    # 将新书籍添加到数据库
    try:
        db.session.add(new_book)
        db.session.commit()  # 提交更改
        return jsonify({'message': '书籍添加成功', 'book': {
            'id': new_book.id,
            'title': new_book.title,
            'author': new_book.author,
            'category': new_book.category,
            'description': new_book.description,
            'location': new_book.location,
            'imageUrl': new_book.imageUrl  # 返回图片的路径
        }}), 201  # 返回201状态码，表示成功创建
    
    except Exception as e:
        db.session.rollback()  # 发生异常时回滚事务
        print(f"添加书籍失败: {str(e)}")  # 打印错误堆栈
        return jsonify({'error': '添加书籍失败', 'details': str(e)}), 500  # 返回错误信息

####################################id搜索接口############################
@app.route('/api/book/book_id', methods=['GET'])
def get_book_id():
    searchText = request.args.get('searchText')  # 获取分类参数
    # 从数据库中获取所有书籍
    try:
        search_id = int(searchText)  # 将 searchText 转换为整数
    except ValueError:
        return jsonify({'error': '无效的ID格式'}), 400  # 返回400错误响应
    book = Book.query.filter_by(id=search_id).first()  # 通过ID查找单个书籍

    if book:
        # 将书籍信息转换为字典格式
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'description': book.description,
            'location': book.location,
            'borrowing_times': book.borrowing_times,
            'imageUrl': request.host_url + book.imageUrl if book.imageUrl else None  # 生成绝对的 imageUrl
        }
        return jsonify(book_data)  # 返回书籍数据
    else:
        return jsonify({'message': '未找到该ID对应的书籍'}), 404  # 查无结果时返回404
####################################分类搜索接口############################
@app.route('/api/books', methods=['GET'])
def get_books():
    category = request.args.get('category')  # 获取分类参数
    # 从数据库中获取所有书籍
    books = Book.query.all()  # 假设 Book 是一个 ORM 模型

    # 根据分类参数过滤书籍
    if category and category != '全部':
        books = [book for book in books if book.category == category]  # 直接使用对象属性
    # 将书籍信息转换为字典格式
    books_data = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'description': book.description,
            'location': book.location,
            'borrowing_times': book.borrowing_times,
            'imageUrl': request.host_url + book.imageUrl if book.imageUrl else None  # 生成绝对的 imageUrl
        } for book in books
    ]


    # 返回JSON响应
    return jsonify(books_data)



###################################注册接口#################################
# 用于存储手机号和验证码的字典
verification_codes = {}

# 发送电子邮件的函数
def send_email(to_email, code):
    from_email = "13640152736@163.com"  # 电子邮件地址
    password = "RAZaFEW5jhnJXgBL"  # 邮箱授权密码
    subject = "验证码"
    body = f"您的验证码是：{code}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        # 连接到SMTP服务器并登录
        with smtplib.SMTP_SSL('smtp.163.com', 465) as server:  
            server.login(from_email, password)  # 登录
            server.sendmail(from_email, to_email, msg.as_string())  # 发送邮件
            print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

@app.route('/uploads/<path:filename>')
def upload_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/api/send-code', methods=['POST'])#获取验证码
def send_code():
    data = request.json
    phone_number = data.get('phone_number')

    # 简单生成六位数验证码
    code = str(random.randint(100000, 999999))
    
    # 存储验证码及失效时间（有效期设置为5分钟）
    verification_codes[phone_number] = {
        'code': code,
        'expires_at': datetime.now() + timedelta(minutes=5)
    }
    # 发送验证码到用户的电子邮件
    send_email(phone_number, code)
    return jsonify({"message": "验证码已发送"}), 200

@app.route('/api/verify-code', methods=['POST'])#验证验证码
def verify_code():
    data = request.json
    phone_number = data.get('phone_number')#获取账号
    password = data.get('password')#获取密码
    code = data.get('code')#获取验证码

    # 获取存储的验证码和有效时间
    record = verification_codes.get(phone_number)
    
    if record and record['code'] == code and record['expires_at'] > datetime.now():
        hashed_password = generate_password_hash(password)  # 对密码进行哈希处理
        new_user = User(phone_number=phone_number, password=hashed_password)  # 创建新用户实例
        db.session.add(new_user)  # 将新用户添加到会话
        db.session.commit()  # 提交到数据库
        return jsonify({'success': True,"message": "验证码验证成功"}), 200
    else:
        return jsonify({'success': False,"message": "验证码无效或已过期"}), 400
    
###################################账号验证码验证接口################################
@app.route('/api/verify', methods=['POST'])#验证验证码
def verify():
    data = request.json
    phone_number = data.get('phone_number')#获取账号
    code = data.get('code')#获取验证码

    # 获取存储的验证码和有效时间
    record = verification_codes.get(phone_number)
    print("验证码验证")
    if record and record['code'] == code and record['expires_at'] > datetime.now():
        return jsonify({'success': True,"message": "验证码验证成功"}), 200
    else:
        return jsonify({'success': False,"message": "验证码无效或已过期"}), 400
###################################管理员登录接口#################################
@app.route('/login', methods=['POST'])#管理员登录接口
def login():
    data = request.get_json()
    username = data.get('username')#获取管理员用户名
    password = data.get('password')#获取管理员密码
    print(username)
    print(password)

    # 连接到MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 查询用户信息
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '登录失败'})

###################################用户登录接口##################################
@app.route('/userv', methods=['POST'])#用户登录接口
def userv():
    data = request.get_json()
    phone_number=data.get('phone_number')#获取用户手机号
    password=data.get('password')#获取用户密码
    print(phone_number)
    print(password)

    # 连接到MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 查询用户信息
    query = "SELECT * FROM user WHERE phone_number = %s "
    cursor.execute(query, (phone_number,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # 检查用户是否存在，并验证密码
    if user and check_password_hash(user['password'], password):
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '登录失败'})
###################################验证账号是否存在接口##################################
@app.route('/api/check-username', methods=['POST'])
def check_username():
    data = request.get_json()
    phone_number=data.get('phone_number')#获取用户账号
    print(phone_number)
    # 连接到MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 查询用户信息
    query = "SELECT * FROM user WHERE phone_number = %s "
    cursor.execute(query, (phone_number,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user :
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)