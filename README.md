# Collaborative PTE Study Platform

A comprehensive Django-based web application for PTE (Pearson Test of English) study preparation with collaborative features, interactive whiteboard, and progress tracking.

## 🚀 Live Demo

**Live Application**: https://collaborative-pte-study-platform.onrender.com/

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Features Overview](#features-overview)
- [Usage Instructions](#usage-instructions)
- [Deployment Guide](#deployment-guide)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Features
- **PTE Study Sections**: Speaking, Writing, Reading, and Listening preparation materials
- **Interactive Timer**: Collapsible timer with presets and custom time options
- **User Authentication**: Simple name + PIN based authentication system
- **Progress Tracking**: Track completion status and favorites across all content
- **Search Functionality**: Search across all study materials

### Collaborative Features
- **Interactive Whiteboard**: Draw, write, and take collaborative notes
- **Whiteboard Gallery**: Save and view all whiteboard sessions
- **Real-time Collaboration**: Multiple users can work together

### Advanced Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Session Management**: Secure user sessions with progress persistence
- **Content Management**: Admin interface for adding/editing study materials

## 🛠 Technology Stack

- **Backend**: Django 5.1.3 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL ready
- **Authentication**: Custom session-based authentication
- **Deployment**: Render.com with Gunicorn
- **Static Files**: WhiteNoise for static file serving
- **Drawing**: HTML5 Canvas API for interactive whiteboard

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mahimistrying/Collaborative-PTE-study-platform.git
   cd Collaborative-PTE-study-platform
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**
   ```bash
   cd pte_guide
   python manage.py makemigrations
   python manage.py migrate
   python manage.py setup_initial_data
   ```

5. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - The application should be running locally

### Dependencies

Create `requirements.txt` with:
```
Django==5.1.3
gunicorn==21.2.0
whitenoise==6.9.0
```

## 📁 Project Structure

```
pte_guide/
├── guide/                          # Main Django app
│   ├── migrations/                 # Database migrations
│   ├── templates/guide/           # HTML templates
│   │   ├── base.html              # Base template with timer
│   │   ├── home.html              # Homepage
│   │   ├── section_detail.html    # Study section pages
│   │   ├── whiteboard.html        # Interactive whiteboard
│   │   ├── whiteboard_gallery.html # Gallery view
│   │   └── login.html             # User authentication
│   ├── static/guide/              # Static files (CSS, JS, images)
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── urls.py                    # URL routing
│   └── admin.py                   # Admin interface
├── pte_guide/                     # Django project settings
│   ├── settings.py                # Main settings
│   ├── urls.py                    # Root URL config
│   └── wsgi.py                    # WSGI configuration
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── Procfile                       # Render deployment config
├── build.sh                       # Build script for deployment
└── README.md                      # This documentation
```

## 🎯 Features Overview

### 1. User Authentication System

**Simple Name + PIN Authentication**
- Users create accounts with just a name and 4-6 digit PIN
- Secure PIN hashing using SHA256
- Session-based authentication
- Progress persistence across sessions

```python
# Example user creation
user = SimpleUser(name="John Doe")
user.set_pin("1234")
user.save()
```

### 2. Interactive Timer Widget

**Features:**
- Collapsible interface (starts closed)
- Preset times: 5, 10, 15, 20, 30, 45, 60 minutes
- Custom time input
- Start/pause/reset functionality
- Audio notifications
- Stays open only when running

**Usage:**
```javascript
// Timer automatically initializes on page load
// Click timer header to expand/collapse
// Select preset or enter custom time
// Click start to begin timer
```

### 3. Interactive Whiteboard

**Capabilities:**
- Smooth drawing with quadratic curves
- Multiple drawing tools and colors
- Text input (inline, no popups)
- Clear canvas functionality
- Save to gallery as JPG
- Touch device support

**Technical Implementation:**
- HTML5 Canvas API
- Event handling for mouse and touch
- Base64 image encoding for storage
- Real-time drawing optimization

### 4. Progress Tracking

**Features:**
- Mark content as completed/incomplete
- Favorite/unfavorite content
- Section-wise progress overview
- Recent activity tracking
- Persistent across sessions

### 5. Content Management

**Study Sections:**
- **Speaking**: Practice questions, tips, video tutorials
- **Writing**: Essay templates, sample responses
- **Reading**: Comprehension strategies, practice texts
- **Listening**: Audio exercises, note-taking techniques

## 📖 Usage Instructions

### For Students

1. **Getting Started**
   - Visit the application URL
   - Click "Track Your Progress" to create an account
   - Enter your name and create a 4-6 digit PIN
   - Click "Register" to create your account

2. **Studying with Timer**
   - Navigate to any study section
   - Click the timer widget to expand it
   - Select a preset time or enter custom time
   - Click "Start" - timer stays open while running
   - Focus on your studies with audio notifications

3. **Using the Whiteboard**
   - Go to "Collaborative Study" section
   - Access the interactive whiteboard
   - Draw, write notes, and collaborate
   - Save important sessions to gallery
   - View saved whiteboards anytime

4. **Tracking Progress**
   - Mark content as complete using checkmark buttons
   - Add content to favorites using heart buttons
   - View progress overview in "Progress" section
   - See completion percentages by section

### For Study Groups

1. **Collaborative Features**
   - Share the application URL with study partners
   - Everyone creates individual accounts
   - Use whiteboard for group note-taking
   - Save important diagrams and notes
   - Access shared gallery of whiteboards

2. **Study Sessions**
   - Coordinate timer usage across the group
   - Take turns presenting using whiteboard
   - Track individual progress
   - Share favorite resources

## 🚀 Deployment Guide

### Render.com Deployment

1. **Prepare for Deployment**
   ```bash
   # Ensure all files are committed
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `Collaborative-PTE-study-platform`

3. **Configure Build Settings**
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn pte_guide.wsgi --log-file -`
   - **Environment**: `Python 3`

4. **Set Environment Variables**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Visit your live application URL

### Build Script (build.sh)
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py setup_initial_data
```

### Procfile Configuration
```
web: gunicorn pte_guide.wsgi --log-file -
```

## 🔌 API Endpoints

### Public Endpoints
- `GET /` - Homepage
- `GET /section/<name>/` - Study section detail
- `GET /health/` - Health check
- `POST /login/` - User authentication
- `GET /whiteboard/` - Interactive whiteboard

### Authenticated Endpoints
- `POST /toggle-progress/` - Toggle content completion
- `POST /whiteboard/save/` - Save whiteboard image
- `DELETE /whiteboard/delete/<id>/` - Delete whiteboard
- `GET /progress/` - User progress overview
- `GET /favorites/` - User favorite content

### Admin Endpoints
- `POST /auth/` - Edit mode authentication
- `POST /add/` - Add new content
- `POST /edit/<id>/` - Edit existing content
- `POST /delete/<id>/` - Delete content

## 🐛 Troubleshooting

### Common Issues

**1. Local Server Won't Start**
```bash
# Install missing dependencies
pip install whitenoise
pip install -r requirements.txt

# Reset database if needed
python manage.py migrate --run-syncdb
```

**2. Whiteboard Not Loading**
- Check browser console for JavaScript errors
- Ensure Canvas API is supported
- Try refreshing the page

**3. User Authentication Issues**
- Clear browser cookies and sessions
- Ensure PIN is 4-6 digits only
- Try with a different username

**4. Deployment Issues**
- Verify all environment variables are set
- Check build logs in Render dashboard
- Ensure requirements.txt includes all dependencies

### Environment Variables

For local development, create a `.env` file:
```
DEBUG=True
SECRET_KEY=your-development-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Reset
If you need to reset the database:
```bash
rm db.sqlite3
rm -rf guide/migrations/00*.py
python manage.py makemigrations
python manage.py migrate
python manage.py setup_initial_data
```

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the GitHub Issues page
3. Create a new issue with detailed information about your problem

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for PTE students worldwide**

*Last Updated: August 2025*
