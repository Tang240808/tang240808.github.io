from db import Database
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class UserManager:
    def __init__(self):
        self.db = Database()
        
    def _hash_password(self, password):
        """对密码进行哈希处理"""
        salt = b'salt_123456'  # 在实际应用中应该为每个用户使用不同的salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        hashed_password = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8'))).decode('utf-8')
        return hashed_password
        
    def register_user(self, username, password, email=None):
        """注册普通用户"""
        if not self.db.connect():
            return False, "数据库连接失败"
            
        try:
            # 检查用户名是否已存在
            self.db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if self.db.cursor.fetchone():
                return False, "用户名已存在"
                
            # 哈希密码
            hashed_password = self._hash_password(password)
            
            # 插入新用户
            self.db.execute_update(
                "INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, 'user')",
                (username, hashed_password, email)
            )
            
            return True, "注册成功"
        except Exception as e:
            return False, f"注册失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def login(self, username, password):
        """用户登录验证"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            # 查询用户
            self.db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = self.db.cursor.fetchone()
            
            if not user:
                return False, None, "用户不存在"
                
            # 验证密码
            hashed_password = self._hash_password(password)
            if hashed_password != user['password']:
                return False, None, "密码错误"
                
            # 登录成功，返回用户信息（不包含密码）
            user_info = {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'email': user['email']
            }
            return True, user_info, "登录成功"
        except Exception as e:
            return False, None, f"登录失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def get_all_users(self):
        """获取所有用户列表（管理员功能）"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            # 查询所有用户
            users = self.db.execute_query("SELECT id, username, email, role, created_at FROM users")
            return True, users, "查询成功"
        except Exception as e:
            return False, None, f"查询失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def update_user_role(self, user_id, role):
        """更新用户角色（管理员功能）"""
        if role not in ['user', 'admin']:
            return False, "角色只能是'user'或'admin'"
            
        if not self.db.connect():
            return False, "数据库连接失败"
            
        try:
            # 更新用户角色
            affected_rows = self.db.execute_update(
                "UPDATE users SET role = %s WHERE id = %s",
                (role, user_id)
            )
            
            if affected_rows <= 0:
                return False, "用户不存在或未进行更改"
                
            return True, "用户角色更新成功"
        except Exception as e:
            return False, f"更新失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def delete_user(self, user_id):
        """删除用户（管理员功能）"""
        if not self.db.connect():
            return False, "数据库连接失败"
            
        try:
            # 检查是否是最后一个管理员
            self.db.cursor.execute("SELECT id FROM users WHERE role = 'admin'")
            admin_users = self.db.cursor.fetchall()
            
            # 查询当前要删除的用户是否是管理员
            self.db.cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            user = self.db.cursor.fetchone()
            
            if user and user['role'] == 'admin' and len(admin_users) <= 1:
                return False, "不能删除最后一个管理员"
                
            # 删除用户
            affected_rows = self.db.execute_update("DELETE FROM users WHERE id = %s", (user_id,))
            
            if affected_rows <= 0:
                return False, "用户不存在"
                
            return True, "用户删除成功"
        except Exception as e:
            return False, f"删除失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def get_user_by_id(self, user_id):
        """根据ID获取用户信息"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            # 查询用户
            self.db.cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,))
            user = self.db.cursor.fetchone()
            
            if not user:
                return False, None, "用户不存在"
                
            return True, user, "查询成功"
        except Exception as e:
            return False, None, f"查询失败: {str(e)}"
        finally:
            self.db.disconnect()