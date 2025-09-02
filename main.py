from db import Database
from user import UserManager
from book import BookManager
import time

class BookManagementSystem:
    def __init__(self):
        self.db = Database()
        self.user_manager = UserManager()
        self.book_manager = BookManager()
        self.current_user = None
        
    def clear_screen(self):
        """清屏函数"""
        print("\n" * 50)
        
    def print_header(self):
        """打印标题头"""
        print("=" * 50)
        print("          图书管理系统          ")
        print("=" * 50)
        
    def print_subheader(self, title):
        """打印子标题"""
        print("-" * 50)
        print(f"{title.center(48)}")
        print("-" * 50)
        
    def wait_for_enter(self):
        """等待用户按Enter键"""
        input("\n按Enter键继续...")
        
    def init_system(self):
        """初始化系统"""
        self.clear_screen()
        self.print_header()
        print("正在初始化系统...")
        
        # 初始化数据库
        if not self.db.init_database():
            print("数据库初始化失败，请确保MySQL服务已启动，并配置正确的用户名和密码。")
            print("请修改db.py文件中的数据库连接参数。")
            return False
            
        print("系统初始化成功！")
        time.sleep(1)
        return True
        
    def main_menu(self):
        """主菜单"""
        while True:
            self.clear_screen()
            self.print_header()
            
            if self.current_user:
                print(f"当前用户: {self.current_user['username']} ({self.current_user['role']})")
            else:
                print("请登录或注册")
                
            print("\n主菜单：")
            print("1. 用户注册")
            print("2. 用户登录")
            if self.current_user:
                print("3. 浏览图书")
                print("4. 搜索图书")
                if self.current_user['role'] == 'admin':
                    print("5. 管理员功能")
                print("0. 退出登录")
            else:
                print("0. 退出系统")
                
            choice = input("请选择操作 (0-5): ")
            
            if not self.current_user:
                if choice == '1':
                    self.user_register()
                elif choice == '2':
                    self.user_login()
                elif choice == '0':
                    print("感谢使用图书管理系统，再见！")
                    break
                else:
                    print("无效的选择，请重试。")
                    self.wait_for_enter()
            else:
                if choice == '1':
                    self.user_register()
                elif choice == '2':
                    self.user_login()
                elif choice == '3':
                    self.browse_books()
                elif choice == '4':
                    self.search_books()
                elif choice == '5' and self.current_user['role'] == 'admin':
                    self.admin_menu()
                elif choice == '0':
                    self.current_user = None
                    print("已退出登录。")
                    self.wait_for_enter()
                else:
                    print("无效的选择，请重试。")
                    self.wait_for_enter()
                    
    def user_register(self):
        """用户注册功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("用户注册")
        
        username = input("请输入用户名: ")
        if not username:
            print("用户名不能为空！")
            self.wait_for_enter()
            return
            
        password = input("请输入密码: ")
        if not password:
            print("密码不能为空！")
            self.wait_for_enter()
            return
            
        confirm_password = input("请确认密码: ")
        if password != confirm_password:
            print("两次输入的密码不一致！")
            self.wait_for_enter()
            return
            
        email = input("请输入邮箱 (可选): ")
        
        success, message = self.user_manager.register_user(username, password, email)
        print(message)
        self.wait_for_enter()
        
    def user_login(self):
        """用户登录功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("用户登录")
        
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        
        success, user_info, message = self.user_manager.login(username, password)
        print(message)
        
        if success and user_info:
            self.current_user = user_info
        
        self.wait_for_enter()
        
    def browse_books(self):
        """浏览图书功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("浏览图书")
        
        # 获取可用分类
        success, categories, message = self.book_manager.get_available_categories()
        if success:
            print("可用分类:")
            if categories:
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                print("0. 查看所有图书")
                
                choice = input("请选择分类 (0-{}): ".format(len(categories)))
                try:
                    choice = int(choice)
                    if choice == 0:
                        category = None
                    elif 1 <= choice <= len(categories):
                        category = categories[choice - 1]
                    else:
                        print("无效的选择，将显示所有图书。")
                        category = None
                except ValueError:
                    print("无效的输入，将显示所有图书。")
                    category = None
            else:
                print("暂无图书分类，将显示所有图书。")
                category = None
        else:
            print("获取分类失败，将显示所有图书。")
            category = None
        
        # 获取并显示图书列表
        success, books, message = self.book_manager.get_all_books(category)
        if success:
            if books:
                self.display_books(books)
                
                # 查看图书详情
                try:
                    book_id = int(input("请输入要查看详情的图书ID (0返回): "))
                    if book_id > 0:
                        self.view_book_detail(book_id)
                except ValueError:
                    pass
            else:
                print("暂无图书信息。")
        else:
            print(message)
            
        self.wait_for_enter()
        
    def search_books(self):
        """搜索图书功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("搜索图书")
        
        keyword = input("请输入搜索关键词 (书名、作者、ISBN或分类): ")
        if not keyword:
            print("搜索关键词不能为空！")
            self.wait_for_enter()
            return
            
        success, books, message = self.book_manager.search_books(keyword)
        if success:
            if books:
                self.display_books(books)
                
                # 查看图书详情
                try:
                    book_id = int(input("请输入要查看详情的图书ID (0返回): "))
                    if book_id > 0:
                        self.view_book_detail(book_id)
                except ValueError:
                    pass
            else:
                print(f"未找到与'{keyword}'相关的图书。")
        else:
            print(message)
            
        self.wait_for_enter()
        
    def view_book_detail(self, book_id):
        """查看图书详情"""
        success, book, message = self.book_manager.get_book_by_id(book_id)
        if success and book:
            self.clear_screen()
            self.print_header()
            self.print_subheader(f"图书详情: {book['title']}")
            
            print(f"ID: {book['id']}")
            print(f"书名: {book['title']}")
            print(f"作者: {book['author']}")
            print(f"出版社: {book['publisher'] or '未知'}")
            print(f"出版日期: {book['publish_date'] or '未知'}")
            print(f"ISBN: {book['isbn'] or '未知'}")
            print(f"分类: {book['category'] or '未分类'}")
            print(f"库存: {book['stock']}")
            print(f"简介: {book['description'] or '暂无简介'}")
        else:
            print(message)
            
        self.wait_for_enter()
        
    def admin_menu(self):
        """管理员菜单"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_subheader("管理员功能")
            
            print("1. 图书管理")
            print("2. 用户管理")
            print("0. 返回主菜单")
            
            choice = input("请选择操作 (0-2): ")
            
            if choice == '1':
                self.book_management_menu()
            elif choice == '2':
                self.user_management_menu()
            elif choice == '0':
                break
            else:
                print("无效的选择，请重试。")
                self.wait_for_enter()
                
    def book_management_menu(self):
        """图书管理菜单"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_subheader("图书管理")
            
            print("1. 添加图书")
            print("2. 查看所有图书")
            print("3. 更新图书信息")
            print("4. 删除图书")
            print("0. 返回管理员菜单")
            
            choice = input("请选择操作 (0-4): ")
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                success, books, message = self.book_manager.get_all_books()
                if success and books:
                    self.display_books(books)
                else:
                    print(message)
                self.wait_for_enter()
            elif choice == '3':
                self.update_book()
            elif choice == '4':
                self.delete_book()
            elif choice == '0':
                break
            else:
                print("无效的选择，请重试。")
                self.wait_for_enter()
                
    def add_book(self):
        """添加图书功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("添加图书")
        
        title = input("请输入书名: ")
        if not title:
            print("书名不能为空！")
            self.wait_for_enter()
            return
            
        author = input("请输入作者: ")
        if not author:
            print("作者不能为空！")
            self.wait_for_enter()
            return
            
        publisher = input("请输入出版社 (可选): ")
        
        # 处理出版日期
        publish_date = None
        date_input = input("请输入出版日期 (格式: YYYY-MM-DD，可选): ")
        if date_input:
            try:
                # 简单验证日期格式
                if len(date_input) == 10 and date_input[4] == '-' and date_input[7] == '-':
                    publish_date = date_input
                else:
                    print("日期格式不正确，将不设置出版日期。")
            except:
                print("日期格式不正确，将不设置出版日期。")
                
        isbn = input("请输入ISBN (可选，唯一): ")
        category = input("请输入分类 (可选): ")
        description = input("请输入简介 (可选): ")
        
        # 处理库存
        stock = 1
        stock_input = input("请输入库存数量 (默认为1): ")
        if stock_input:
            try:
                stock = int(stock_input)
                if stock < 0:
                    print("库存数量不能为负数，将使用默认值1。")
                    stock = 1
            except:
                print("库存数量格式不正确，将使用默认值1。")
                
        success, message = self.book_manager.add_book(title, author, publisher, publish_date, isbn, category, description, stock)
        print(message)
        self.wait_for_enter()
        
    def update_book(self):
        """更新图书信息功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("更新图书信息")
        
        try:
            book_id = int(input("请输入要更新的图书ID: "))
        except ValueError:
            print("无效的图书ID！")
            self.wait_for_enter()
            return
            
        # 获取当前图书信息
        success, book, message = self.book_manager.get_book_by_id(book_id)
        if not success or not book:
            print(message)
            self.wait_for_enter()
            return
            
        # 显示当前图书信息
        self.display_books([book])
        print("\n请输入要更新的信息（直接回车跳过不更新）:")
        
        # 获取新的图书信息
        title = input(f"书名 [{book['title']}]: ") or None
        author = input(f"作者 [{book['author']}]: ") or None
        publisher = input(f"出版社 [{book['publisher'] or '未知'}]: ") or None
        
        # 处理出版日期
        publish_date = None
        date_input = input(f"出版日期 [{book['publish_date'] or '未知'}] (格式: YYYY-MM-DD): ")
        if date_input:
            try:
                # 简单验证日期格式
                if len(date_input) == 10 and date_input[4] == '-' and date_input[7] == '-':
                    publish_date = date_input
                else:
                    print("日期格式不正确，将不更新出版日期。")
            except:
                print("日期格式不正确，将不更新出版日期。")
                
        isbn = input(f"ISBN [{book['isbn'] or '未知'}]: ") or None
        category = input(f"分类 [{book['category'] or '未分类'}]: ") or None
        description = input(f"简介 [{book['description'] or '暂无简介'}]: ") or None
        
        # 处理库存
        stock = None
        stock_input = input(f"库存 [{book['stock']}]: ")
        if stock_input:
            try:
                stock_val = int(stock_input)
                if stock_val >= 0:
                    stock = stock_val
                else:
                    print("库存数量不能为负数，将不更新库存。")
            except:
                print("库存数量格式不正确，将不更新库存。")
                
        success, message = self.book_manager.update_book(book_id, title, author, publisher, publish_date, isbn, category, description, stock)
        print(message)
        self.wait_for_enter()
        
    def delete_book(self):
        """删除图书功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("删除图书")
        
        try:
            book_id = int(input("请输入要删除的图书ID: "))
        except ValueError:
            print("无效的图书ID！")
            self.wait_for_enter()
            return
            
        # 确认删除
        confirm = input("确定要删除该图书吗？(y/n): ").lower()
        if confirm != 'y':
            print("已取消删除操作。")
            self.wait_for_enter()
            return
            
        success, message = self.book_manager.delete_book(book_id)
        print(message)
        self.wait_for_enter()
        
    def user_management_menu(self):
        """用户管理菜单"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_subheader("用户管理")
            
            print("1. 查看所有用户")
            print("2. 修改用户角色")
            print("3. 删除用户")
            print("0. 返回管理员菜单")
            
            choice = input("请选择操作 (0-3): ")
            
            if choice == '1':
                success, users, message = self.user_manager.get_all_users()
                if success and users:
                    self.display_users(users)
                else:
                    print(message)
                self.wait_for_enter()
            elif choice == '2':
                self.change_user_role()
            elif choice == '3':
                self.delete_user_account()
            elif choice == '0':
                break
            else:
                print("无效的选择，请重试。")
                self.wait_for_enter()
                
    def change_user_role(self):
        """修改用户角色功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("修改用户角色")
        
        try:
            user_id = int(input("请输入要修改角色的用户ID: "))
        except ValueError:
            print("无效的用户ID！")
            self.wait_for_enter()
            return
            
        # 获取当前用户信息
        success, user, message = self.user_manager.get_user_by_id(user_id)
        if not success or not user:
            print(message)
            self.wait_for_enter()
            return
            
        print(f"当前用户: {user['username']} (当前角色: {user['role']})")
        
        # 选择新角色
        print("请选择新角色:")
        print("1. 普通用户 (user)")
        print("2. 管理员 (admin)")
        
        role_choice = input("请选择 (1-2): ")
        if role_choice == '1':
            new_role = 'user'
        elif role_choice == '2':
            new_role = 'admin'
        else:
            print("无效的选择，将不修改角色。")
            self.wait_for_enter()
            return
            
        if user['role'] == new_role:
            print("用户已经是该角色，无需修改。")
            self.wait_for_enter()
            return
            
        success, message = self.user_manager.update_user_role(user_id, new_role)
        print(message)
        self.wait_for_enter()
        
    def delete_user_account(self):
        """删除用户账户功能"""
        self.clear_screen()
        self.print_header()
        self.print_subheader("删除用户账户")
        
        try:
            user_id = int(input("请输入要删除的用户ID: "))
        except ValueError:
            print("无效的用户ID！")
            self.wait_for_enter()
            return
            
        # 获取用户信息
        success, user, message = self.user_manager.get_user_by_id(user_id)
        if not success or not user:
            print(message)
            self.wait_for_enter()
            return
            
        print(f"要删除的用户: {user['username']} (角色: {user['role']})")
        
        # 确认删除
        confirm = input("确定要删除该用户吗？(y/n): ").lower()
        if confirm != 'y':
            print("已取消删除操作。")
            self.wait_for_enter()
            return
            
        success, message = self.user_manager.delete_user(user_id)
        print(message)
        self.wait_for_enter()
        
    def display_books(self, books):
        """显示图书列表"""
        print("\n图书列表:")
        print("{:<5} {:<30} {:<20} {:<15} {:<10}".format("ID", "书名", "作者", "分类", "库存"))
        print("-" * 80)
        
        for book in books:
            print("{:<5} {:<30} {:<20} {:<15} {:<10}".format(
                book['id'],
                (book['title'][:27] + '...') if len(book['title']) > 30 else book['title'],
                (book['author'][:17] + '...') if len(book['author']) > 20 else book['author'],
                book['category'] or '未分类',
                book['stock']
            ))
        
    def display_users(self, users):
        """显示用户列表"""
        print("\n用户列表:")
        print("{:<5} {:<20} {:<30} {:<10} {:<20}".format("ID", "用户名", "邮箱", "角色", "注册时间"))
        print("-" * 95)
        
        for user in users:
            print("{:<5} {:<20} {:<30} {:<10} {:<20}".format(
                user['id'],
                user['username'],
                user['email'] or '无',
                user['role'],
                str(user['created_at'])[:19]
            ))
            
if __name__ == "__main__":
    system = BookManagementSystem()
    if system.init_system():
        system.main_menu()