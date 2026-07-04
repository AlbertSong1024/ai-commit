# AI Commit

> Automatically generate Git commit messages using AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/ai-commit.svg)](https://pypi.org/project/ai-commit/)

## Features

- **AI-Powered**: Generate commit messages with OpenAI or local Ollama models
- **Multiple Styles**: conventional, simple, detailed, emoji
- **Local Support**: Use Ollama for offline commit message generation
- **Multi-Language**: Support English, Chinese, Japanese
- **Auto Commit**: One-click commit with generated message
- **Preview**: See diff before generating

## Installation

```bash
pip install ai-commit
```

## Usage

### Cloud Mode (OpenAI)

```bash
# Generate commit message
ai-commit

# Auto-commit
ai-commit --commit

# Emoji style
ai-commit --style emoji

# Chinese language
ai-commit --language zh
```

### Local Mode (Ollama)

```bash
# Install Ollama: https://ollama.ai
ollama pull llama3

# List available models
ai-commit --list-models

# Use local model
ai-commit --local

# Specify model
ai-commit --local --ollama-model mistral
```

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your-key-here
```

## Styles

| Style | Example |
|-------|---------|
| conventional | `feat(auth): add OAuth2 login` |
| simple | `add user authentication` |
| detailed | `feat(auth): add OAuth2 login\\n\nImplemented OAuth2 login flow with Google and GitHub providers.` |
| emoji | `✨ feat(auth): add OAuth2 login` |

## License

MIT
