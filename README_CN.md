[English](README.md) | [中文](README_CN.md)

# 🤖 ai-commit

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> 使用AI自动生成Git提交信息的命令行工具

## ✨ 功能特性

- 🚀 **AI驱动** - 使用OpenAI GPT模型生成高质量提交信息
- 🎨 **多种风格** - 支持conventional、simple、detailed、emoji四种风格
- 🌍 **多语言** - 支持生成任意语言的提交信息
- 📊 **差异预览** - 生成前预览代码变更
- ⚡ **快速** - 几秒钟内生成提交信息
- 🔧 **CLI界面** - 命令行操作简单便捷
- 📦 **Pip安装** - 一键安装

## 📦 安装

### 通过PyPI安装（推荐）

```bash
pip install ai-commit
```

### 从源码安装

```bash
git clone https://github.com/Alex-2Code/ai-commit.git
cd ai-commit
pip install -e .
```

## 🔧 配置

1. 从 [platform.openai.com](https://platform.openai.com/api-keys) 获取OpenAI API密钥

2. 设置API密钥：

```bash
export OPENAI_API_KEY="sk-your-api-key"
```

或添加到shell配置文件（`~/.bashrc`、`~/.zshrc`等）：

```bash
echo 'export OPENAI_API_KEY="sk-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

## 🚀 使用方法

### 基本用法

```bash
# 暂存更改
git add .

# 生成提交信息
ai-commit

# 生成并自动提交
ai-commit --commit
```

### 命令选项

```bash
ai-commit [OPTIONS]

选项:
  --style, -s TEXT     提交信息风格: conventional, simple, detailed, emoji
                       [默认: conventional]
  --language, -l TEXT  提交信息语言 [默认: en]
  --api-key, -k TEXT   OpenAI API密钥 (或设置 OPENAI_API_KEY 环境变量)
  --model, -m TEXT     使用的OpenAI模型 [默认: gpt-4o-mini]
  --commit, -c         生成后自动提交
  --preview, -p        生成前显示差异预览 [默认: True]
  --all, -a            生成前暂存所有更改
  --version            显示版本
  --help               显示帮助信息
```

### 示例

```bash
# 使用conventional风格
ai-commit --style conventional

# 使用emoji风格
ai-commit --style emoji

# 生成中文提交信息
ai-commit --language "Chinese"

# 使用指定模型
ai-commit --model gpt-4o

# 暂存所有并提交
ai-commit --all --commit
```

## 📝 提交风格

### Conventional Commits（默认）

```
feat(auth): add user login functionality

- Implement JWT token generation
- Add login endpoint
- Add password hashing
```

### Simple（简单）

```
Add user login functionality
```

### Detailed（详细）

```
Add user login functionality

- Implement JWT token generation
- Add login endpoint with validation
- Add bcrypt password hashing
- Add login form component
```

### Emoji

```
✨ Add user login functionality
```

## 📖 使用示例

### 示例 1: 简单更改

```bash
$ git add README.md
$ ai-commit

┌─ Git Diff 预览 ─────────────────────────────┐
│ diff --git a/README.md b/README.md         │
│ index 1234567..89abcde 100644              │
│ --- a/README.md                            │
│ +++ b/README.md                            │
│ @@ -1,3 +1,5 @@                            │
│  # My Project                              │
│ +## Features                                │
│ +- Feature 1                               │
└────────────────────────────────────────────┘

┌─ 生成的提交信息 ────────────────────────────┐
│ docs: add features section to README       │
└────────────────────────────────────────────┘

是否使用此信息提交? [y/N]: y
✓ 更改已成功提交!
```

### 示例 2: Emoji风格

```bash
$ ai-commit --style emoji --commit
📝 Update documentation with new features
✓ 更改已成功提交!
```

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`ai-commit`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

本项目基于MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [OpenAI](https://openai.com/) 提供的API
- [Click](https://click.palletsprojects.com/) CLI框架
- [Rich](https://rich.readthedocs.io/) 终端美化库

## 📧 联系方式

- GitHub: [@Alex-2Code](https://github.com/Alex-2Code)

---

由 [Alex-2Code](https://github.com/Alex-2Code) 用 ❤️ 制作
