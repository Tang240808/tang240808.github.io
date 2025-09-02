# 图书管理系统

这是一个使用Python和MySQL开发的图书管理系统，提供了命令行界面和Web界面两种使用方式，支持普通用户注册、登录、浏览和搜索图书，以及管理员添加、删除、修改图书信息和管理用户。

## 功能特点

### 普通用户功能
- ✅ 用户注册
- ✅ 用户登录
- ✅ 浏览图书（按分类或全部）
- ✅ 搜索图书（按书名、作者、ISBN或分类）
- ✅ 查看图书详情

### 管理员功能
- ✅ 添加新图书
- ✅ 更新图书信息
- ✅ 删除图书
- ✅ 查看所有用户列表
- ✅ 修改用户角色
- ✅ 删除用户
- ✅ 防止删除最后一个管理员账户

## 环境要求

- Python 3.6+ 
- MySQL 5.7+ 

## 安装和配置

### 1. 安装依赖包

```bash
pip install -r requirements.txt
```

### 2. 配置MySQL数据库

1. 确保MySQL服务已启动
2. 创建数据库：
   ```sql
   CREATE DATABASE book_management;
   ```
3. 创建MySQL用户（可选）：
   ```sql
   CREATE USER 'book_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON book_management.* TO 'book_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 3. 修改数据库连接配置

打开 `db.py` 文件，修改以下数据库连接参数：

```python
self.conn = pymysql.connect(
    host='localhost',
    user='root',  # 替换为你的MySQL用户名
    password='',  # 替换为你的MySQL密码
    database='book_management',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
```

## 使用方法

### 1. 命令行版本

运行主程序：

```bash
python main.py
```

### 2. Web版本

运行Web服务器：

```bash
python app.py
```

启动后，在浏览器中访问：`http://localhost:5000`

### 默认管理员账户

系统初始化时会自动创建一个默认管理员账户：
- 用户名：admin
- 密码：admin123

请在首次登录后修改密码以确保安全。

## 项目结构

- `main.py`：命令行版本程序入口文件
- `app.py`：Web版本程序入口文件，使用Flask框架
- `db.py`：数据库连接和初始化模块
- `user.py`：用户管理模块
- `book.py`：图书管理模块
- `templates/`：Web界面模板文件目录
- `requirements.txt`：项目依赖包列表
- `README.md`：项目说明文档

## Web界面功能

### 普通用户界面
- 响应式设计，适配不同设备屏幕
- 美观的图书展示卡片
- 分类浏览和关键词搜索功能
- 详细的图书信息展示
- 简单直观的登录注册流程

### 管理员界面
- 数据统计面板
- 图书管理（增删改查）
- 用户管理（角色修改、删除）
- 表单验证和错误提示
- 安全操作确认机制

## 注意事项

1. Web版本使用Flask框架开发，默认在本地5000端口运行
2. 在生产环境中，建议使用Gunicorn等WSGI服务器部署
3. 请确保设置安全的SECRET_KEY（在app.py文件中）
4. 数据库连接配置位于app.py文件中，与db.py保持一致
5. 旧系统的密码需要重新设置才能在Web版本中登录（因为哈希方式不同）

## 注意事项

1. 本系统使用了简单的密码哈希算法进行密码存储，但在实际生产环境中，应考虑使用更安全的密码存储方式
2. 系统目前仅提供命令行界面，可根据需要扩展为Web界面或GUI界面
3. 为了安全起见，建议不要在生产环境中使用默认的管理员账户和密码
4. 在运行程序前，请确保MySQL服务已启动，并且已正确配置数据库连接参数

## 扩展建议

1. 添加图书借阅功能
2. 实现密码找回功能
3. 添加图书封面图片管理
4. 开发Web界面或GUI界面
5. 添加更复杂的权限控制
6. 实现数据统计和报表功能