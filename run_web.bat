@echo off
:: 图书管理系统Web版本启动脚本

:: 检查是否在虚拟环境中运行
if exist ".venv\Scripts\python.exe" (
    echo 使用虚拟环境中的Python解释器...
    .venv\Scripts\python.exe app.py
) else (
    echo 未找到虚拟环境，使用系统Python解释器...
    python app.py
)

pause