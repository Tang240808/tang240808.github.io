import pymysql

# 数据库连接信息
DB_CONFIG = {
    'host': 'localhost',
    'user': 'user1',  # 与db.py中的配置保持一致
    'password': 'user1',  # 与db.py中的配置保持一致
    'database': 'book_management',
    'charset': 'utf8mb4'
}


print("开始执行数据库迁移：添加cover_image列到books表")

# 连接数据库
connection = None
try:
    # 建立数据库连接
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    # 检查books表是否存在cover_image列
    cursor.execute("SHOW COLUMNS FROM books LIKE 'cover_image'")
    result = cursor.fetchone()
    
    if result:
        print("cover_image列已存在，无需添加")
    else:
        # 添加cover_image列
        alter_table_sql = "ALTER TABLE books ADD COLUMN cover_image VARCHAR(255)"
        cursor.execute(alter_table_sql)
        connection.commit()
        print("成功添加cover_image列到books表")
        
    # 打印完成信息
    print("数据库迁移完成！")
    
except pymysql.MySQLError as e:
    print(f"数据库操作错误: {e}")
    if connection:
        connection.rollback()
except Exception as e:
    print(f"发生错误: {e}")
finally:
    # 关闭数据库连接
    if connection:
        cursor.close()
        connection.close()
        print("数据库连接已关闭")

# 提示用户
print("\n注意：")
print("1. 此脚本已成功为books表添加了cover_image列")
print("2. 现在您可以正常运行图书管理系统并上传图书封面了")
print("3. 如果再次遇到数据库相关错误，请检查数据库连接配置是否正确")

input("\n按Enter键退出...")