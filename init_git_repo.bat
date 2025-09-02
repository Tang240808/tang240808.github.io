@echo off
:: Git�ֿ��ʼ���ű�
:: ���������ٿ�ʼʹ��Git����ͼ�����ϵͳ��Ŀ

:: ����������ʾ
chcp 65001 >nul

:: ���Git�Ƿ�װ
where git >nul 2>nul
if %errorLevel% neq 0 (
    echo ����: δ�ҵ�Git���
    echo ���ȴ� https://git-scm.com/downloads ���ز���װGit
    pause
    exit /b 1
)

echo. ==================================================
echo.          Git�ֿ��ʼ���ű�
 echo.       ͼ�����ϵͳ��Ŀ
 echo. ==================================================
echo. 

:: ��鵱ǰĿ¼�Ƿ��ѳ�ʼ��Git�ֿ�
echo ��鵱ǰĿ¼�Ƿ��ѳ�ʼ��Git�ֿ�...
if exist .git (
    echo ��⵽��ǰĿ¼�Ѵ���Git�ֿ⣡
    echo ����������³�ʼ��������ɾ�� .git Ŀ¼
    pause
    exit /b 1
)

echo ��ǰĿ¼��δ��ʼ��Git�ֿ⣬��������...
echo.

:: ��ʼ��Git�ֿ�
echo ���ڳ�ʼ��Git�ֿ�...
git init
if %errorLevel% neq 0 (
    echo ��ʼ��Git�ֿ�ʧ�ܣ�
    pause
    exit /b 1
)
echo Git�ֿ��ʼ���ɹ���
echo.

:: ����Git�û���Ϣ
set /p username="����������Git�û���: "
set /p email="����������Git�����ַ: "

if not defined username (
    echo �û�������Ϊ�գ�
    pause
    exit /b 1
)

if not defined email (
    echo �����ַ����Ϊ�գ�
    pause
    exit /b 1
)

echo.��������Git�û���Ϣ...
git config user.name "%username%"
git config user.email "%email%"
echo Git�û���Ϣ���óɹ���
echo �û���: %username%
echo ����: %email%
echo.

:: ���.gitignore�ļ�
echo ���.gitignore�ļ�...
if not exist .gitignore (
    echo ����: δ�ҵ�.gitignore�ļ���
    echo ���鴴��һ��.gitignore�ļ������Բ���Ҫ�汾���Ƶ��ļ�
    echo ���������������Ctrl+Cȡ��...
    pause >nul
)
echo .gitignore�ļ����ͨ����
echo.

:: ��������ļ����ݴ���
echo ���ڽ������ļ���ӵ�Git�ݴ���...
git add .
if %errorLevel% neq 0 (
    echo ����ļ����ݴ���ʧ�ܣ�
    pause
    exit /b 1
)
echo �ļ���ӳɹ���
echo.

:: ������һ���ύ
echo ���ڴ�����һ���ύ...
git commit -m "��ʼ��ͼ�����ϵͳ��Ŀ"
if %errorLevel% neq 0 (
    echo �����ύʧ�ܣ�
    pause
    exit /b 1
)
echo ��һ���ύ�����ɹ���
echo.

:: ��ʾ��ǰ״̬
echo ��ǰGit�ֿ�״̬:
git status
echo.

:: ��ʾ�ύ��ʷ
echo �ύ��ʷ:
git log --oneline
echo.

:: �����ʾ
echo ==================================================
echo.                ��ʼ����ɣ�
echo.
echo ������Ŀ�ѳɹ���ʼ��Git�ֿ⡣
echo �����������ԣ�
echo 1. ����Զ�ֿ̲⣨GitHub��Gitee�ȣ�
echo 2. �����زֿ���Զ�ֿ̲������
echo    git remote add origin https://github.com/�����û���/�ֿ�����.git
echo 3. ���ʹ��뵽Զ�ֿ̲⣺
echo    git push -u origin master
echo.
echo ��ϸ��Gitʹ��ָ����鿴 GIT_GUIDE.md �ļ�
 echo ==================================================
echo.

pause