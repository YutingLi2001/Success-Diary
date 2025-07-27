# Mac Development Scripts

## 🚀 Quick Start

**First time setup:**
1. Double-click `initial-setup.command` to set up your development environment
2. Double-click `server-start.command` to start the server

## 📋 Available Scripts

### Main Scripts
- **`initial-setup.command`** - ⭐ **START HERE** - Complete first-time setup
- **`dev-setup.command`** - Full development setup with database reset
- **`server-start.command`** - Quick server start (GUI friendly)
- **`email-start.command`** - Start email testing server only

### Command Line Scripts
- **`quick-start.sh`** - Fast server start from terminal
- **`dev-start-with-email.sh`** - Start both app and email servers

### Utilities (`utilities/` folder)
- **`install-deps.command`** - Install/update Python dependencies
- **`reset-db.command`** - Reset database (deletes all data!)
- **`reset-venv.command`** - Recreate virtual environment
- **`kill-server.command`** - Force kill stubborn server processes

## 🖱️ GUI Usage (Double-Click)
All `.command` files can be double-clicked in Finder to run with a GUI interface.

## 💻 Terminal Usage
```bash
# Make sure you're in the project root directory
cd /path/to/Success-Diary

# Run any script
./scripts/mac/quick-start.sh
./scripts/mac/dev-start-with-email.sh
```

## 🔧 Troubleshooting

**"Virtual environment not found":**
- Run `initial-setup.command` first
- Or use `utilities/reset-venv.command`

**"Permission denied":**
- Scripts should be executable by default
- If needed: `chmod +x scripts/mac/*.command scripts/mac/*.sh`

**Server won't start/stop:**
- Use `utilities/kill-server.command` to force kill processes
- Check port 8000 isn't used by another app

**Email server not working:**
- Install Mailpit: `brew install mailpit`
- Or follow instructions in `email-start.command`

## 🌐 Development URLs
- **App**: http://localhost:8000
- **Email Interface**: http://localhost:8025