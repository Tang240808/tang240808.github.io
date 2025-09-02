# 解决Email Validator错误

## 问题说明

在运行图书管理系统的Web版本时，您可能会遇到以下错误：

```
Exception: Install 'email_validator' for email validation support.
```

这个错误表示系统缺少`email_validator`包，这是Flask-WTF表单验证库用于验证电子邮件地址格式的必要依赖。

## 解决方案

### 方法1：使用已安装的依赖（推荐）

我已经为您安装了所需的`email_validator`包，您现在可以正常运行Web服务器了。

### 方法2：手动安装依赖（如果需要重新安装）

如果您需要在其他环境中运行此项目，可以通过以下命令安装所有必要的依赖：

```bash
# 使用虚拟环境中的pip
.venv\Scripts\pip install -r requirements.txt

# 或者使用系统pip（不推荐）
pip install -r requirements.txt
```

## 已添加的依赖

`requirements.txt`文件已更新，包含了所有必要的依赖包：

- `pymysql`: MySQL数据库连接库
- `cryptography`: 加密库，用于密码哈希
- `flask`: Web框架
- `flask-wtf`: 表单验证库
- `flask-sqlalchemy`: 数据库ORM库
- `flask-login`: 用户认证管理
- `flask-bcrypt`: 密码加密库
- `email_validator`: 电子邮件地址验证库

## 启动Web服务器

现在您可以通过以下方式启动Web服务器：

1. 双击运行 `run_web.bat` 脚本
2. 或在命令行中运行：
   ```bash
   python app.py
   ```

启动后，在浏览器中访问 `http://localhost:5000` 即可使用Web界面。