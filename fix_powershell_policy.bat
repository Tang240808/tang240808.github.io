@echo off
:: 修复PowerShell执行策略问题，允许运行虚拟环境激活脚本

:: 检查是否以管理员身份运行
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 请以管理员身份运行此脚本！
    echo 右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 显示当前执行策略
echo 当前PowerShell执行策略:
powershell -Command "Get-ExecutionPolicy -List"

echo.
echo 正在设置执行策略为RemoteSigned...
:: 设置PowerShell执行策略为RemoteSigned（允许运行本地脚本）
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

:: 验证执行策略是否已更改
echo.
echo 更新后的PowerShell执行策略:
powershell -Command "Get-ExecutionPolicy -List"

echo.
echo PowerShell执行策略已成功更新！
echo 现在您应该可以正常运行虚拟环境的激活脚本了。
echo.
echo 提示:
 echo 1. 在普通PowerShell中运行: .venv\Scripts\Activate.ps1
echo 2. 或者使用cmd.exe运行: .venv\Scripts\activate.bat
echo 3. 或者直接使用run_web.bat启动Web服务器

pause