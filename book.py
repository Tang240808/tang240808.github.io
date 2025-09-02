from db import Database
from datetime import datetime

class BookManager:
    def __init__(self):
        self.db = Database()
        
    def add_book(self, title, author, publisher=None, publish_date=None, isbn=None, category=None, description=None, stock=1):
        """添加图书（管理员功能）"""
        if not self.db.connect():
            return False, "数据库连接失败"
            
        try:
            # 检查ISBN是否已存在（如果提供了ISBN）
            if isbn:
                self.db.cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
                if self.db.cursor.fetchone():
                    return False, "该ISBN的图书已存在"
                    
            # 插入新图书
            self.db.execute_update(
                "INSERT INTO books (title, author, publisher, publish_date, isbn, category, description, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (title, author, publisher, publish_date, isbn, category, description, stock)
            )
            
            return True, "图书添加成功"
        except Exception as e:
            return False, f"添加失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def get_all_books(self, category=None):
        """获取所有图书列表"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            if category:
                # 按分类查询
                books = self.db.execute_query("SELECT * FROM books WHERE category = %s ORDER BY title", (category,))
            else:
                # 查询所有图书
                books = self.db.execute_query("SELECT * FROM books ORDER BY title")
                
            return True, books, "查询成功"
        except Exception as e:
            return False, None, f"查询失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def search_books(self, keyword):
        """搜索图书（按书名、作者、ISBN或分类）"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            # 构建搜索查询
            search_term = f"%{keyword}%"
            books = self.db.execute_query(
                "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s OR category LIKE %s ORDER BY title",
                (search_term, search_term, search_term, search_term)
            )
            
            return True, books, "查询成功"
        except Exception as e:
            return False, None, f"查询失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def get_book_by_id(self, book_id):
        """根据ID获取图书信息"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            # 查询图书
            self.db.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            book = self.db.cursor.fetchone()
            
            if not book:
                return False, None, "图书不存在"
                
            return True, book, "查询成功"
        except Exception as e:
            return False, None, f"查询失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def update_book(self, book_id, title=None, author=None, publisher=None, publish_date=None, isbn=None, category=None, description=None, stock=None):
        """更新图书信息（管理员功能）"""
        if not self.db.connect():
            return False, "数据库连接失败"
            
        try:
            # 检查图书是否存在
            self.db.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            if not self.db.cursor.fetchone():
                return False, "图书不存在"
                
            # 构建更新语句
            update_fields = []
            update_params = []
            
            if title is not None:
                update_fields.append("title = %s")
                update_params.append(title)
            if author is not None:
                update_fields.append("author = %s")
                update_params.append(author)
            if publisher is not None:
                update_fields.append("publisher = %s")
                update_params.append(publisher)
            if publish_date is not None:
                update_fields.append("publish_date = %s")
                update_params.append(publish_date)
            if isbn is not None:
                # 检查新ISBN是否已被其他图书使用
                self.db.cursor.execute("SELECT * FROM books WHERE isbn = %s AND id != %s", (isbn, book_id))
                if self.db.cursor.fetchone():
                    return False, "该ISBN已被其他图书使用"
                update_fields.append("isbn = %s")
                update_params.append(isbn)
            if category is not None:
                update_fields.append("category = %s")
                update_params.append(category)
            if description is not None:
                update_fields.append("description = %s")
                update_params.append(description)
            if stock is not None:
                update_fields.append("stock = %s")
                update_params.append(stock)
                
            # 如果没有要更新的字段
            if not update_fields:
                return False, "没有要更新的字段"
                
            # 执行更新
            update_query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = %s"
            update_params.append(book_id)
            
            affected_rows = self.db.execute_update(update_query, update_params)
            
            if affected_rows <= 0:
                return False, "更新失败"
                
            return True, "图书信息更新成功"
        except Exception as e:
            return False, f"更新失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def delete_book(self, book_id):
        """删除图书（管理员功能）"""
        if not self.db.connect():
            return False, "数据库连接失败"
            
        try:
            # 检查图书是否存在
            self.db.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            if not self.db.cursor.fetchone():
                return False, "图书不存在"
                
            # 删除图书
            affected_rows = self.db.execute_update("DELETE FROM books WHERE id = %s", (book_id,))
            
            if affected_rows <= 0:
                return False, "删除失败"
                
            return True, "图书删除成功"
        except Exception as e:
            return False, f"删除失败: {str(e)}"
        finally:
            self.db.disconnect()
            
    def get_available_categories(self):
        """获取所有可用的图书分类"""
        if not self.db.connect():
            return False, None, "数据库连接失败"
            
        try:
            categories = self.db.execute_query("SELECT DISTINCT category FROM books WHERE category IS NOT NULL ORDER BY category")
            return True, [cat['category'] for cat in categories], "查询成功"
        except Exception as e:
            return False, None, f"查询失败: {str(e)}"
        finally:
            self.db.disconnect()