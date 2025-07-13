# Success Diary - Development Scripts

This folder contains automation scripts to streamline development workflow.

## 📁 Available Scripts

### 🚀 **dev-start.bat**
**Complete development setup (recommended for daily use)**
- Activates virtual environment
- Installs/updates dependencies
- Resets database (deletes existing data)
- Starts development server on port 8000

### ⚡ **quick-start.bat**
**Quick server start (when no changes needed)**
- Activates virtual environment
- Starts development server immediately

### 🗃️ **reset-db.bat**
**Database reset only**
- Safely deletes existing database with confirmation
- Smart error handling (detects if file is in use by server)
- Flexible input (accepts y/yes/n/no and any case)
- Useful when schema changes are made to models

### 📦 **install-deps.bat**
**Install/update dependencies only**
- Activates virtual environment
- Runs `pip install -r requirements.txt`

## 🎯 Usage

### From Windows Explorer:
Double-click any `.bat` file to run it

### From Command Prompt:
```bash
cd "C:\Users\Yuting\Projects\success-diary\scripts"
dev-start.bat
```

### From Project Root:
```bash
scripts\dev-start.bat
```

## 🛠️ Script Features

- **Smart directory handling**: Automatically navigates to project root
- **Error checking**: Verifies project structure and virtual environment
- **Safe operations**: Confirmation prompts for destructive actions
- **Clear feedback**: Progress indicators and helpful messages
- **Robust error handling**: Graceful failure with informative messages
- **Professional input handling**: Case-insensitive, flexible user responses
- **Environment isolation**: Proper variable scoping with setlocal/endlocal

## 📋 Recommended Workflow

1. **Daily development**: Use `dev-start.bat` for full setup
2. **Quick restarts**: Use `quick-start.bat` when server stops
3. **Schema changes**: Use `reset-db.bat` after modifying `models.py`
4. **Dependency updates**: Use `install-deps.bat` when `requirements.txt` changes

## 🔧 Troubleshooting

If scripts don't work:
1. Ensure you're running from the correct directory
2. Check that virtual environment exists at `venv\Scripts\activate.bat`
3. Verify project structure (should have `app\main.py`)
4. Run scripts as Administrator if permission issues occur