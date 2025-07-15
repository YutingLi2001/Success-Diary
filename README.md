# SuccessDiary

A privacy-focused web application designed to support personal growth through structured daily reflection. Built for knowledge workers and personal growth enthusiasts who want to build positive mental health habits and track meaningful progress over time.

## ✨ Core Philosophy

**Structured Flexibility**: Users can define what they track while maintaining consistency. The app celebrates any reflection rather than demanding perfection.

**Human-Centered Design**: Optional fields reduce pressure. Only essential elements are required, encouraging authentic reflection over performance.

**Long-Term Growth**: Designed to support evolving goals while preserving data continuity for meaningful progress tracking.

## 🚀 Current Features

### ✅ Implemented (MVP 1.0 Complete)
- **User Authentication**: Email verification with 6-digit codes (10-minute expiration)
- **Daily Entry System**: 11-field structured reflection form
  - 3 Success highlights (first required, others optional)
  - 3 Gratitude points (first required, others optional) 
  - 3 Anxiety/worry items (all optional)
  - Overall day rating (1-5 scale, required)
  - Free-form journal section (optional)
- **Entry History**: View and browse past entries with chronological organization
- **Cross-Platform Development**: Automated setup scripts for Windows and Mac
- **Email Testing**: Local development with Mailpit integration

### ⏳ In Development (MVP 1.0 Completion)
- **Entry Editing**: Full editing functionality for historical entries
- **Entry Titles**: Custom titles with auto-generated date-based fallback
- **Dynamic UI**: Progressive field display (show next field after current has content)
- **Enhanced Validation**: Comprehensive form validation with user-friendly error messages
- **Mobile Optimization**: Full responsive design for mobile devices

### 📋 Planned Features
- **V2.0**: Health tracking modules (diet, exercise, sleep, productivity)
- **V3.0+**: Advanced analytics, custom fields, data export, OAuth integration, API access
- **Production**: AWS cloud deployment with PostgreSQL

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.110.1 with SQLModel ORM
- **Frontend**: Jinja2 templates with Tailwind CSS v3.4
- **Database**: SQLite (development) → PostgreSQL (production)
- **Authentication**: FastAPI-Users 14.0.1 with email verification
- **Email**: Mailpit (local testing) → Production SMTP
- **Enhancement**: HTMX for dynamic interactions
- **Deployment**: Planned AWS EC2/ECS + RDS

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js v20+
- Git

### Automated Setup (Recommended)

**Windows:**
```cmd
git clone https://github.com/YutingLi2001/Success-Diary.git
cd Success-Diary
scripts\windows\dev-start-with-email.bat
```

**Mac/Linux:**
```bash
git clone https://github.com/YutingLi2001/Success-Diary.git
cd Success-Diary
./scripts/mac/dev-start-with-email.sh
```

**Access Points:**
- **Application**: http://localhost:8000
- **Email Testing**: http://localhost:8025

### Manual Setup (Alternative)

1. **Clone and setup environment**
   ```bash
   git clone https://github.com/YutingLi2001/Success-Diary.git
   cd Success-Diary
   python -m venv venv
   ```

2. **Activate virtual environment**
   ```bash
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. **Start services**
   ```bash
   # Terminal 1: Email server
   mailpit
   
   # Terminal 2: Application server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Development Scripts

**Windows:**
- `scripts\windows\dev-start-with-email.bat` - Full development environment
- `scripts\windows\quick-start.bat` - Application server only
- `scripts\windows\reset-db.bat` - Reset database only
- `scripts\windows\install-deps.bat` - Install/update dependencies

**Mac/Linux:**
- `./scripts/mac/dev-start-with-email.sh` - Full development environment
- `./scripts/mac/quick-start.sh` - Application server only
- `./scripts/mac/reset-db.sh` - Reset database only
- `./scripts/mac/install-deps.sh` - Install/update dependencies

## 📁 Project Structure

```
Success-Diary/
├── app/                         # FastAPI application
├── templates/                   # Jinja2 HTML templates
├── scripts/                     # Development automation
│   ├── mac/                    # macOS/Linux scripts
│   └── windows/                # Windows batch files
├── docs/                        # Comprehensive documentation
│   ├── logs/                   # Development tracking
│   ├── operations/             # Development procedures
│   ├── requirements/           # Project specifications
│   └── project-timeline.md
├── prompts/                     # AI collaboration templates
├── config/                      # Configuration files
├── data/                        # Data storage and backups
├── tests/                       # Test files
├── venv/                        # Python virtual environment
├── db.sqlite3                   # SQLite database (auto-created)
└── requirements.txt             # Dependencies
```

## 📚 Documentation

This project uses comprehensive documentation to guide development and collaboration:

### 📋 Requirements & Planning
- **Product Vision**: `docs/requirements/product-overview.md`
- **Feature Roadmap**: `docs/requirements/core-functionality-overview.md`
- **Technical Requirements**: `docs/requirements/development-requirements.md`
- **Project Scope**: `docs/requirements/project-scope.md`

### 🛠️ Development Operations
- **Developer Manual**: `docs/operations/developer-manual.md`
- **Setup Procedures**: Cross-platform installation and troubleshooting guides
- **Database Management**: Schema procedures and migration documentation

### 📈 Progress Tracking
- **Development Journal**: `docs/logs/development-journal.md`
- **Project Timeline**: `docs/project-timeline.md`
- **Development Notes**: `docs/logs/development-notes.md`

## 🎯 Development Status

**Current Phase**: MVP 1.0 Development (Core Features Completion)

**Target**: Complete core emotional reflection functionality, followed by AWS production deployment in August 2025.

**Methodology**: "Planning Then Go" approach with comprehensive upfront planning, template-driven AI collaboration, and detailed progress tracking.

### Success Metrics
- **Active Users**: >10 users creating ≥1 entry by 4 weeks post-launch
- **User Retention**: >30 days average entries per user within first 45 days  
- **System Stability**: <1% error rate in production
- **Self-Adoption**: ≥50 consecutive days of founder usage

## 🤖 AI Collaboration

This project uses template-driven AI collaboration for consistent development outcomes:

- **Prompt Templates**: Located in `prompts/` folder
- **Development Methodology**: "Planning Then Go" approach
- **Documentation**: Automatic progress tracking via prompt system

## 🔧 Development Workflow

### Daily Development
1. **Review Planning**: Check `docs/requirements/` for current objectives
2. **Start Environment**: Use automated setup scripts
3. **Track Progress**: Document sessions using prompt templates
4. **Database Changes**: Reset database when modifying models
5. **Update Documentation**: Use `prompts/update-development-journal.md`

### Database Management
- **Development**: SQLite with automatic creation
- **Schema Changes**: Delete `db.sqlite3` and restart (development only)
- **Production**: PostgreSQL migration planned for deployment

## 🏔️ Deployment Plan

### Phase 2: Production (August 2025)
- **Platform**: AWS EC2/ECS with PostgreSQL RDS
- **Domain**: Custom domain with Route 53 and SSL
- **Environment**: Mac development setup for continued development
- **Target Launch**: August 17, 2025

## 🤝 Contributing

This project welcomes contributions! Key resources:

- **Project Vision**: `docs/requirements/product-overview.md`
- **Development Setup**: `docs/operations/developer-manual.md`
- **Current Status**: `docs/logs/development-journal.md`
- **Feature Planning**: `docs/requirements/core-functionality-overview.md`

### Development Environment
- Use automated scripts for consistent setup
- Follow "Planning Then Go" methodology
- Document progress using prompt templates
- Refer to comprehensive documentation in `docs/`

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

Built with modern web technologies and human-centered design principles. Developed using AI-assisted programming with Claude Code to accelerate development while maintaining quality and consistency.

---

**📚 For detailed development information, see the `docs/` folder.**
**🚀 For quick setup, use the automated scripts in `scripts/`.**
**🤖 For AI collaboration workflows, see templates in `prompts/`.**