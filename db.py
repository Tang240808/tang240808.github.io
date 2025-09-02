import pymysql

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='user1',  # 默认用户，实际使用时可能需要修改
                password='user1',  # 默认密码为空，实际使用时应设置密码
                database='book_management',  # 数据库名称，需要先创建
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False
            
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询执行失败: {e}")
            return None
            
    def execute_update(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"更新执行失败: {e}")
            self.conn.rollback()
            return -1
            
    def init_database(self):
        """初始化数据库，创建所需的表"""
        if not self.connect():
            return False
            
        try:
            # 创建用户表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    role ENUM('user', 'admin') DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建图书表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    author VARCHAR(100) NOT NULL,
                    publisher VARCHAR(100),
                    publish_date DATE,
                    isbn VARCHAR(20) UNIQUE,
                    category VARCHAR(50),
                    description TEXT,
                    stock INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建借阅记录表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrow_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    book_id INT,
                    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    return_date TIMESTAMP,
                    status ENUM('borrowed', 'returned', 'overdue') DEFAULT 'borrowed',
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                )
            ''')
            
            # 创建默认管理员账户
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
            result = self.cursor.fetchone()
            if result['count'] == 0:
                # 默认管理员账号：admin，密码：admin123
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                from cryptography.hazmat.backends import default_backend
                import base64
                
                password = b'admin123'
                salt = b'salt_123456'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                hashed_password = base64.urlsafe_b64encode(kdf.derive(password)).decode('utf-8')
                
                self.cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    ('admin', hashed_password, 'admin')
                )
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            self.conn.rollback()
            return False
        finally:
            self.disconnect()