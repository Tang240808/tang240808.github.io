# Git版本控制使用指南

本指南将帮助您使用Git来管理和版本控制您的图书管理系统项目。

## 前提条件

确保您的计算机上已安装Git。如果尚未安装，请访问 [Git官网](https://git-scm.com/downloads) 下载并安装。

## 第一步：初始化Git仓库

1. 打开命令提示符（CMD）或PowerShell
2. 导航到您的项目目录：
   ```bash
   cd d:\projects\web_tushu
   ```
3. 初始化Git仓库：
   ```bash
   git init
   ```

这将在您的项目目录中创建一个.git目录，用于存储Git的版本控制信息。

## 第二步：配置Git用户信息

在使用Git之前，需要设置您的用户名和电子邮件地址：

```bash
# 设置全局用户名
git config --global user.name "您的用户名"

# 设置全局电子邮件
git config --global user.email "您的电子邮件@example.com"
```

## 第三步：检查.gitignore文件

您的项目中已经包含了一个合理的.gitignore文件，它会忽略不需要版本控制的文件，如虚拟环境、编译文件、日志文件等。

如果您需要自定义.gitignore文件，可以编辑它以满足您的特定需求。

## 第四步：添加文件到暂存区

现在，将项目文件添加到Git的暂存区：

```bash
# 添加所有文件到暂存区
git add .

# 或者单独添加特定文件
# git add filename
```

## 第五步：提交更改

将暂存区的文件提交到本地仓库：

```bash
git commit -m "初始化图书管理系统项目"
```

请使用有意义的提交消息，描述您所做的更改。

## 第六步：创建和管理分支

分支允许您在不影响主代码的情况下进行开发：

```bash
# 创建新分支
git branch feature/new-feature

# 切换到新分支
git checkout feature/new-feature

# 创建并切换到新分支
git checkout -b feature/new-feature

# 查看所有分支
git branch

# 合并分支（先切换到目标分支，再合并源分支）
git checkout main
# 或者在较旧的Git版本中是master分支
git checkout master

git merge feature/new-feature

# 删除分支（完成开发后）
git branch -d feature/new-feature
```

## 第七步：设置远程仓库

如果您想将代码备份到远程仓库（如GitHub、Gitee或GitLab）：

1. 首先在远程平台创建一个新的空仓库
2. 然后将本地仓库与远程仓库关联：
   ```bash
   git remote add origin https://github.com/您的用户名/仓库名称.git
   ```
3. 将本地代码推送到远程仓库：
   ```bash
   git push -u origin main
   # 或者在较旧的Git版本中是master分支
   git push -u origin master
   ```

## 第八步：日常工作流程

在日常开发中，您可以遵循以下工作流程：

1. **更新代码**：在开始工作前，确保您的本地仓库是最新的
   ```bash
   git pull origin main
   ```

2. **创建分支**：为新功能或修复创建一个新分支
   ```bash
   git checkout -b feature/your-feature
   ```

3. **开发和提交**：进行代码更改，然后添加并提交
   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

4. **推送更改**：将您的分支推送到远程仓库
   ```bash
   git push origin feature/your-feature
   ```

5. **合并代码**：当功能完成后，将其合并回主分支
   ```bash
   git checkout main
   git pull origin main
   git merge feature/your-feature
   git push origin main
   ```

## 第九步：常见Git命令

```bash
# 查看工作目录状态
git status

# 查看提交历史
git log

# 查看文件差异
git diff

git diff --staged  # 查看暂存区和最后一次提交的差异

# 撤销工作目录中的更改
git checkout -- filename

# 取消暂存文件
git reset HEAD filename

# 撤销最后一次提交（保留更改）
git reset --soft HEAD~

# 撤销最后一次提交（丢弃更改）
git reset --hard HEAD~
```

## 第十步：Git最佳实践

1. 经常提交，保持提交消息清晰明了
2. 每个提交只包含相关的更改
3. 使用分支进行功能开发和错误修复
4. 定期推送到远程仓库进行备份
5. 合并前先更新主分支
6. 遵循团队的Git工作流规范

## 第十一章：使用图形化工具

如果您更喜欢使用图形化界面，可以考虑以下Git客户端：

- [Git GUI](https://git-scm.com/downloads/guis) - Git官方提供的GUI工具
- [SourceTree](https://www.sourcetreeapp.com/) - Atlassian提供的免费Git客户端
- [GitHub Desktop](https://desktop.github.com/) - GitHub官方客户端
- [GitKraken](https://www.gitkraken.com/) - 功能强大的Git客户端

## 遇到问题？

如果您在使用Git时遇到问题，可以使用以下命令获取帮助：

```bash
git help 命令名称
```

或者访问 [Git官方文档](https://git-scm.com/doc) 获取更多信息。

祝您使用Git愉快！