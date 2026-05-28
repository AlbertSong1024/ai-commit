# 🤖 ai-commit

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> Automatically generate meaningful Git commit messages using AI (OpenAI).

## ✨ Features

- 🚀 **AI-Powered** - Uses OpenAI GPT models to generate high-quality commit messages
- 🎨 **Multiple Styles** - Conventional commits, simple, detailed, or emoji style
- 🌍 **Multi-language** - Generate commit messages in any language
- 📊 **Diff Preview** - See what changes will be committed before generating
- ⚡ **Fast** - Generate commit messages in seconds
- 🔧 **CLI Interface** - Easy to use from command line
- 📦 **Pip Installable** - Install with a single command

## 📦 Installation

### From PyPI (recommended)

```bash
pip install ai-commit
```

### From source

```bash
git clone https://github.com/Alex-2Code/ai-commit.git
cd ai-commit
pip install -e .
```

### Dependencies

- Python 3.8+
- OpenAI API key

## 🔧 Setup

1. Get an OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)

2. Set the API key:

```bash
export OPENAI_API_KEY="sk-your-api-key"
```

Or add it to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo 'export OPENAI_API_KEY="sk-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

## 🚀 Usage

### Basic Usage

```bash
# Stage your changes
git add .

# Generate commit message
ai-commit

# Generate and auto-commit
ai-commit --commit
```

### Command Options

```bash
ai-commit [OPTIONS]

Options:
  --style, -s TEXT     Commit message style: conventional, simple, detailed, emoji
                       [default: conventional]
  --language, -l TEXT  Language for commit message [default: en]
  --api-key, -k TEXT   OpenAI API key (or set OPENAI_API_KEY env var)
  --model, -m TEXT     OpenAI model to use [default: gpt-4o-mini]
  --commit, -c         Auto-commit after generating message
  --preview, -p        Show diff preview before generating [default: True]
  --all, -a            Stage all changes before generating
  --version            Show version
  --help               Show this message and exit
```

### Examples

```bash
# Generate with conventional commit style
ai-commit --style conventional

# Generate with emoji style
ai-commit --style emoji

# Generate in Chinese
ai-commit --language "Chinese"

# Generate in Japanese
ai-commit --language "Japanese"

# Use a specific model
ai-commit --model gpt-4o

# Stage all and commit
ai-commit --all --commit
```

## 📝 Commit Styles

### Conventional Commits (default)

```
feat(auth): add user login functionality

- Implement JWT token generation
- Add login endpoint
- Add password hashing
```

### Simple

```
Add user login functionality
```

### Detailed

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

## 📖 Examples

### Example 1: Simple change

```bash
$ git add README.md
$ ai-commit

┌─ Git Diff Preview ─────────────────────────┐
│ diff --git a/README.md b/README.md         │
│ index 1234567..89abcde 100644              │
│ --- a/README.md                            │
│ +++ b/README.md                            │
│ @@ -1,3 +1,5 @@                            │
│  # My Project                              │
│ +## Features                                │
│ +- Feature 1                               │
└────────────────────────────────────────────┘

┌─ Generated Commit Message ─────────────────┐
│ docs: add features section to README       │
└────────────────────────────────────────────┘

Do you want to commit with this message? [y/N]: y
✓ Changes committed successfully!
```

### Example 2: With emoji style

```bash
$ ai-commit --style emoji --commit
📝 Update documentation with new features
✓ Changes committed successfully!
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`ai-commit`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for the amazing API
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output

## 📧 Contact

- GitHub: [@Alex-2Code](https://github.com/Alex-2Code)

---

Made with ❤️ by [Alex-2Code](https://github.com/Alex-2Code)
