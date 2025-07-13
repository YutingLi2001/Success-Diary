# SuccessDiary

A lightweight, human-centered web application for tracking daily successes, gratitude, and reflections. SuccessDiary encourages consistent self-reflection through structured flexibility—helping users build confidence and clarity one day at a time.

## ✨ Features

- **Daily Entry Form**: Track 3 successes, 3 gratitudes, 3 worries, and an overall day rating (1-5)
- **Human-Centered Design**: Only first field in each category is required—optional fields reduce pressure
- **Beautiful Display**: Entries shown with emoji bullet points (✨🙏💭) for easy reading
- **Encouraging UX**: Supportive placeholder text and visual cues guide users
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js v20+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YutingLi2001/Success-Diary.git
   cd Success-Diary
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Install Node dependencies**
   ```bash
   npm install
   ```

4. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Open your browser**
   Visit http://localhost:8000

## 🛠️ Tech Stack

- **Backend**: FastAPI with SQLModel ORM
- **Frontend**: HTML templates with Tailwind CSS
- **Database**: SQLite (development)
- **Styling**: Tailwind CSS
- **Enhancement**: HTMX for dynamic interactions

## 📁 Project Structure

```
Success-Diary/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLModel database models
│   └── database.py      # Database configuration
├── templates/
│   └── index.html       # Main application template
├── Project Documentations/
│   ├── Project Vision.md
│   ├── MVP Scope.md
│   └── Development Journal.md
├── requirements.txt     # Python dependencies
├── package.json        # Node.js dependencies
└── README.md
```

## 🎯 Product Philosophy

**Structured Flexibility**: Users can define what they track while maintaining consistency. The app celebrates any reflection rather than demanding perfection.

**Reinforcement Through Reflection**: Designed to build confidence by encouraging users to recognize daily wins, express gratitude, and process concerns.

**Long-Term Growth**: Supports evolving goals while preserving data continuity for meaningful progress tracking.

## 🔮 Roadmap

- [ ] User authentication system
- [ ] Daily highlight feature (show past positive entries)
- [ ] Data export (JSON/CSV)
- [ ] Edit/delete historical entries
- [ ] Custom field management
- [ ] Data visualization and trends

## 🤝 Contributing

This project welcomes contributions! Please see our development documentation in the `Project Documentations/` folder for detailed information about the project vision and current status.

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

Built with modern web technologies and human-centered design principles to make daily reflection both meaningful and accessible.