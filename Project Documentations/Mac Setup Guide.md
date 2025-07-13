# Mac Development Setup Guide – SuccessDiary

*Preparation guide for post-Calgary development on Mac*

---

## 🖥️ **Required Software Installation**

### **Core Development Tools**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12+
brew install python@3.12

# Install Node.js (for Tailwind CSS)
brew install node

# Install Git (if not installed)
brew install git

# Install VS Code or preferred editor
brew install --cask visual-studio-code
```

### **Optional but Recommended**
```bash
# Install iTerm2 for better terminal
brew install --cask iterm2

# Install GitHub CLI
brew install gh
```

---

## 📁 **Project Setup**

### **1. Clone Repository**
```bash
# Navigate to preferred directory
cd ~/Projects

# Clone the repository
git clone https://github.com/YutingLi2001/Success-Diary.git
cd Success-Diary
```

### **2. Python Environment Setup**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Mac syntax)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Node.js Dependencies**
```bash
# Install Node dependencies
npm install
```

### **4. Environment Configuration**
```bash
# Copy environment file
cp .env .env.local

# Edit .env.local with Mac-specific settings if needed
# (Mailtrap credentials should remain the same)
```

---

## 🔧 **Mac-Specific Script Adaptations**

### **Create Mac-Compatible Scripts**
The existing Windows `.bat` scripts need Mac equivalents:

**scripts/dev-start.sh:**
```bash
#!/bin/bash
echo "===================================="
echo "   Success Diary - Dev Startup"
echo "===================================="

# Change to project root
cd "$(dirname "$0")/.."

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Reset database
if [ -f "db.sqlite3" ]; then
    read -p "Reset database? (y/n): " confirm
    if [[ $confirm == [yY] ]]; then
        rm db.sqlite3
        echo "Database reset"
    fi
fi

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Make executable:**
```bash
chmod +x scripts/dev-start.sh
chmod +x scripts/quick-start.sh
chmod +x scripts/reset-db.sh
chmod +x scripts/install-deps.sh
```

---

## 🧪 **Testing Mac Setup**

### **Verification Steps**
```bash
# 1. Test Python version
python3 --version  # Should be 3.12+

# 2. Test virtual environment
source venv/bin/activate
python --version

# 3. Test dependency installation
pip list | grep fastapi

# 4. Test server startup
./scripts/dev-start.sh

# 5. Test application
open http://localhost:8000
```

---

## 🔄 **Cross-Platform Differences**

### **File Paths**
- **Windows**: `venv\Scripts\activate`
- **Mac**: `source venv/bin/activate`

### **Script Extensions**
- **Windows**: `.bat` files
- **Mac**: `.sh` files (with shebang)

### **Command Differences**
- **Windows**: `del filename`
- **Mac**: `rm filename`

---

## 📋 **Pre-Calgary Preparation Checklist**

Before traveling, ensure:
- [ ] All code is committed and pushed to GitHub
- [ ] `.env` file is documented (without sensitive data)
- [ ] Mac setup commands are tested and documented
- [ ] Any Windows-specific configurations are noted
- [ ] Database schema is documented for potential changes

---

## 🚨 **Troubleshooting Common Issues**

### **Permission Issues**
```bash
# If permission denied on scripts
chmod +x scripts/*.sh

# If permission denied on pip install
pip install --user -r requirements.txt
```

### **Python Version Issues**
```bash
# If python3 not found
brew link python@3.12

# If virtual environment fails
python3.12 -m venv venv
```

### **Database Issues**
```bash
# If SQLite issues on Mac
brew install sqlite3

# If database locked
lsof db.sqlite3  # Find process using database
kill <PID>       # Kill the process
```

---

## 🎯 **Post-Setup Goals**

Once Mac environment is working:
1. **Test full development workflow**
2. **Verify all existing features work**
3. **Begin AWS deployment preparation**
4. **Test production database migration**

---

*This guide will be updated based on actual Mac setup experience*