from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import os
import uuid
from datetime import datetime

# 初始化Flask应用
app = Flask(__name__)
# 注意：在生产环境中请务必更改此密钥为随机生成的安全密钥
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:user1@localhost/book_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# 数据库模型定义
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(db.Enum('user', 'admin'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
    isbn = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=1)
    cover_image = db.Column(db.String(255))  # 封面图片路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"
    
    def get_cover_url(self):
        """获取封面图片URL"""
        if self.cover_image:
            return url_for('static', filename=f'covers/{self.cover_image}')
        else:
            return url_for('static', filename='covers/default_cover.png')

class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('borrowed', 'returned', 'overdue'), default='borrowed')
    
    user = db.relationship('User', backref=db.backref('borrow_records', lazy=True))
    book = db.relationship('Book', backref=db.backref('borrow_records', lazy=True))

# 用户加载回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 设置静态文件目录
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'covers')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传文件大小为16MB

# 确保covers目录存在
COVERS_FOLDER = app.config['UPLOAD_FOLDER']
if not os.path.exists(COVERS_FOLDER):
    os.makedirs(COVERS_FOLDER)
    
# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
# 生成唯一的文件名
def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = str(uuid.uuid4()) + '.' + ext
    return unique_name
    
# 表单定义
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('邮箱', validators=[Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名。')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

from flask_wtf.file import FileField, FileAllowed, FileRequired

class BookForm(FlaskForm):
    title = StringField('书名', validators=[DataRequired(), Length(max=200)])
    author = StringField('作者', validators=[DataRequired(), Length(max=100)])
    publisher = StringField('出版社', validators=[Length(max=100)])
    publish_date = DateField('出版日期', format='%Y-%m-%d')
    isbn = StringField('ISBN', validators=[Length(max=20)])
    category = StringField('分类', validators=[Length(max=50)])
    description = TextAreaField('简介')
    stock = IntegerField('库存', validators=[DataRequired()])
    cover_image = FileField('封面图片', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许图片文件！')])
    submit = SubmitField('提交')

class UpdateUserRoleForm(FlaskForm):
    role = SelectField('角色', choices=[('user', '普通用户'), ('admin', '管理员')], validators=[DataRequired()])
    submit = SubmitField('更新')

# 路由定义
@app.route('/')
@app.route('/home')
def home():
    books = Book.query.order_by(Book.title).all()
    return render_template('home.html', books=books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('您的账户已创建成功！现在您可以登录了。', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('登录失败，请检查用户名和密码。', 'danger')
    return render_template('login.html', title='登录', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', title=book.title, book=book)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        if keyword:
            search_term = f"%{keyword}%"
            books = Book.query.filter(
                Book.title.like(search_term) | 
                Book.author.like(search_term) | 
                Book.isbn.like(search_term) | 
                Book.category.like(search_term)
            ).all()
            return render_template('search.html', title='搜索结果', books=books, keyword=keyword)
    return render_template('search.html', title='搜索')

@app.route('/category/<string:category>')
def category(category):
    books = Book.query.filter_by(category=category).all()
    return render_template('category.html', title=f'分类: {category}', books=books, category=category)

# 管理员路由
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    total_users = User.query.count()
    total_books = Book.query.count()
    return render_template('admin/dashboard.html', title='管理员面板', total_users=total_users, total_books=total_books)

@app.route('/admin/books')
@login_required
def admin_books():
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    books = Book.query.all()
    return render_template('admin/books.html', title='图书管理', books=books)

@app.route('/admin/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    form = BookForm()
    if form.validate_on_submit():
        # 检查ISBN是否已存在
        if form.isbn.data:
            existing_book = Book.query.filter_by(isbn=form.isbn.data).first()
            if existing_book:
                flash('该ISBN的图书已存在。', 'danger')
                return redirect(url_for('add_book'))
        
        # 处理封面图片上传
        cover_image_filename = None
        if 'cover_image' in request.files and request.files['cover_image'].filename:
            file = request.files['cover_image']
            if file and allowed_file(file.filename):
                filename = generate_unique_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_image_filename = filename
        
        book = Book(
            title=form.title.data,
            author=form.author.data,
            publisher=form.publisher.data,
            publish_date=form.publish_date.data,
            isbn=form.isbn.data,
            category=form.category.data,
            description=form.description.data,
            stock=form.stock.data,
            cover_image=cover_image_filename
        )
        db.session.add(book)
        db.session.commit()
        flash('图书已成功添加！', 'success')
        return redirect(url_for('admin_books'))
    return render_template('admin/add_book.html', title='添加图书', form=form)

@app.route('/admin/update_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    book = Book.query.get_or_404(book_id)
    form = BookForm()
    
    if form.validate_on_submit():
        # 检查ISBN是否已被其他图书使用
        if form.isbn.data and form.isbn.data != book.isbn:
            existing_book = Book.query.filter_by(isbn=form.isbn.data).first()
            if existing_book:
                flash('该ISBN已被其他图书使用。', 'danger')
                return redirect(url_for('update_book', book_id=book_id))
        
        # 处理封面图片更新
        if 'cover_image' in request.files and request.files['cover_image'].filename:
            file = request.files['cover_image']
            if file and allowed_file(file.filename):
                # 删除旧的封面图片（如果有）
                if book.cover_image:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # 保存新的封面图片
                filename = generate_unique_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                book.cover_image = filename
        
        book.title = form.title.data
        book.author = form.author.data
        book.publisher = form.publisher.data
        book.publish_date = form.publish_date.data
        book.isbn = form.isbn.data
        book.category = form.category.data
        book.description = form.description.data
        book.stock = form.stock.data
        
        db.session.commit()
        flash('图书信息已成功更新！', 'success')
        return redirect(url_for('admin_books'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.publisher.data = book.publisher
        form.publish_date.data = book.publish_date
        form.isbn.data = book.isbn
        form.category.data = book.category
        form.description.data = book.description
        form.stock.data = book.stock
        
    return render_template('admin/update_book.html', title='更新图书', form=form, book_id=book_id, book=book)

@app.route('/admin/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    book = Book.query.get_or_404(book_id)
    
    # 删除封面图片（如果有）
    if book.cover_image:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(book)
    db.session.commit()
    flash('图书已成功删除！', 'success')
    return redirect(url_for('admin_books'))

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin/users.html', title='用户管理', users=users)

@app.route('/admin/update_user_role/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user_role(user_id):
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    user = User.query.get_or_404(user_id)
    
    # 不允许修改最后一个管理员的角色
    if user.role == 'admin':
        admin_users = User.query.filter_by(role='admin').all()
        if len(admin_users) <= 1:
            flash('不能取消最后一个管理员的权限。', 'danger')
            return redirect(url_for('admin_users'))
    
    form = UpdateUserRoleForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash('用户角色已成功更新！', 'success')
        return redirect(url_for('admin_users'))
    elif request.method == 'GET':
        form.role.data = user.role
    
    return render_template('admin/update_user_role.html', title='更新用户角色', form=form, user=user)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('您没有权限访问此页面。', 'danger')
        return redirect(url_for('home'))
    user = User.query.get_or_404(user_id)
    
    # 不允许删除当前登录的用户
    if user.id == current_user.id:
        flash('不能删除当前登录的用户。', 'danger')
        return redirect(url_for('admin_users'))
    
    # 不允许删除最后一个管理员
    if user.role == 'admin':
        admin_users = User.query.filter_by(role='admin').all()
        if len(admin_users) <= 1:
            flash('不能删除最后一个管理员。', 'danger')
            return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('用户已成功删除！', 'success')
    return redirect(url_for('admin_users'))

# 创建静态文件目录
if not os.path.exists('static'):
    os.makedirs('static')

# 应用初始化
with app.app_context():
    # 创建数据库表（如果不存在）
    db.create_all()
    
    # 检查并更新密码哈希方式（从旧系统迁移）
    try:
        users = User.query.all()
        for user in users:
            # 如果密码不是bcrypt哈希格式（长度小于60）
            if len(user.password) < 60:
                # 注意：由于无法获取明文密码，旧系统的用户需要使用Web界面重置密码
                # 这里我们只是确保admin账户在Web版本中可用
                if user.username == 'admin':
                    # 为admin账户设置新的bcrypt哈希密码（admin123）
                    hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
                    user.password = hashed_password
                    db.session.commit()
    except Exception as e:
        print(f"密码迁移过程中出现错误: {e}")

if __name__ == '__main__':
    # 在生产环境中请将debug设置为False
    app.run(debug=True, host='0.0.0.0', port=5000)