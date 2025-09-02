@echo off
:: Git仓库初始化脚本
:: 帮助您快速开始使用Git管理图书管理系统项目

:: 设置中文显示
chcp 65001 >nul

:: 检查Git是否安装
where git >nul 2>nul
if %errorLevel% neq 0 (
    echo 错误: 未找到Git命令！
    echo 请先从 https://git-scm.com/downloads 下载并安装Git
    pause
    exit /b 1
)

echo. ==================================================
echo.          Git仓库初始化脚本
 echo.       图书管理系统项目
 echo. ==================================================
echo. 

:: 检查当前目录是否已初始化Git仓库
echo 检查当前目录是否已初始化Git仓库...
if exist .git (
    echo 检测到当前目录已存在Git仓库！
    echo 如果您想重新初始化，请先删除 .git 目录
    pause
    exit /b 1
)

echo 当前目录尚未初始化Git仓库，继续操作...
echo.

:: 初始化Git仓库
echo 正在初始化Git仓库...
git init
if %errorLevel% neq 0 (
    echo 初始化Git仓库失败！
    pause
    exit /b 1
)
echo Git仓库初始化成功！
echo.

:: 配置Git用户信息
set /p username="请输入您的Git用户名: "
set /p email="请输入您的Git邮箱地址: "

if not defined username (
    echo 用户名不能为空！
    pause
    exit /b 1
)

if not defined email (
    echo 邮箱地址不能为空！
    pause
    exit /b 1
)

echo.正在配置Git用户信息...
git config user.name "%username%"
git config user.email "%email%"
echo Git用户信息配置成功！
echo 用户名: %username%
echo 邮箱: %email%
echo.

:: 检查.gitignore文件
echo 检查.gitignore文件...
if not exist .gitignore (
    echo 警告: 未找到.gitignore文件！
    echo 建议创建一个.gitignore文件来忽略不需要版本控制的文件
    echo 按任意键继续，或按Ctrl+C取消...
    pause >nul
)
echo .gitignore文件检查通过！
echo.

:: 添加所有文件到暂存区
echo 正在将所有文件添加到Git暂存区...
git add .
if %errorLevel% neq 0 (
    echo 添加文件到暂存区失败！
    pause
    exit /b 1
)
echo 文件添加成功！
echo.

:: 创建第一次提交
echo 正在创建第一次提交...
git commit -m "初始化图书管理系统项目"
if %errorLevel% neq 0 (
    echo 创建提交失败！
    pause
    exit /b 1
)
echo 第一次提交创建成功！
echo.

:: 显示当前状态
echo 当前Git仓库状态:
git status
echo.

:: 显示提交历史
echo 提交历史:
git log --oneline
echo.

:: 完成提示
echo ==================================================
echo.                初始化完成！
echo.
echo 您的项目已成功初始化Git仓库。
echo 接下来您可以：
echo 1. 创建远程仓库（GitHub、Gitee等）
echo 2. 将本地仓库与远程仓库关联：
echo    git remote add origin https://github.com/您的用户名/仓库名称.git
echo 3. 推送代码到远程仓库：
echo    git push -u origin master
echo.
echo 详细的Git使用指南请查看 GIT_GUIDE.md 文件
 echo ==================================================
echo.

pause