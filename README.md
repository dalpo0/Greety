# 🌟 Greety - Advanced Telegram Welcome Bot

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/greety-bot)

Automated welcome messages with location detection, admin controls, and PostgreSQL integration.

![Demo](https://i.imgur.com/welcome-demo.gif)

## ✨ Features

- **Personalized Welcomes**  
  Uses member's location for city/timezone detection
- **Admin Dashboard**  
  `/settings` menu for easy customization
- **Auto-Restrictions**  
  Temporary limits for new members
- **Database Backed**  
  PostgreSQL storage for user data
- **Multi-Platform Ready**  
  Works on Render, Railway, or any Python host

## 🚀 Quick Deployment

### 1. One-Click Install
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/greety-bot)

### 2. Manual Setup
```bash
# Clone repository
git clone https://github.com/yourusername/greety-bot.git
cd greety-bot

# Set up environment
cp .env.example .env
nano .env  # Fill your credentials

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m bot.main
