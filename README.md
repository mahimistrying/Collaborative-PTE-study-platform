# PTE Guide Website (2024 Format)

A comprehensive Django-based website for PTE Academic preparation with the latest 2024 format updates, featuring advanced content organization, progress tracking, and practice tools.

## Features

### 🎯 **Updated for 2024 PTE Format**
- **Speaking Section** (30-35 min): All 8 tasks including NEW Group Discussion & Respond to Situation
- **Writing Section** (24-32 min): Summarize Written Text & Essay Writing
- **Reading Section** (29-30 min): All 5 task types with updated timing
- **Listening Section** (30-43 min): All 8 tasks including Write from Dictation

### 📚 **Content Management**
- **YouTube videos, notes, important links, and text content**
- **Advanced tagging system** with 35+ predefined tags
- **Content filtering** by type, difficulty, and completion status
- **Smart search** across all content

### ⏱️ **Practice Tools**
- **Built-in timer widget** with PTE-specific presets
- **Task-specific timers** for all question types
- **Audio notifications** and visual indicators
- **Keyboard shortcuts** (Ctrl+Space to start/pause)

### 📊 **Progress Tracking**
- **Mark content as completed** with visual indicators
- **Favorite/bookmark system** for important content
- **Progress dashboard** showing completion by section
- **Session-based tracking** (no login required)

### 🔐 **Access Control**
- **Public viewing** for all content
- **Protected editing** with passcode authentication
- **Admin panel** for advanced management

### 🎨 **User Experience**
- **Responsive Bootstrap design**
- **Real-time progress updates**
- **Advanced filtering and sorting**
- **Mobile-friendly interface**

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser** (optional, for admin panel):
   ```bash
   python manage.py createsuperuser
   ```

4. **Set up Initial Data**:
   ```bash
   python manage.py setup_initial_data
   python manage.py setup_tags
   python manage.py update_pte_format
   python manage.py add_new_task_tags
   ```

5. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Website**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Default Configuration

- **Edit Passcode**: `pte2024` (change in `guide/views.py`)
- **Superuser**: username `admin`, no password set (use admin panel to set password)

## Usage

1. **Public Access**: Anyone can view all sections and content
2. **Edit Mode**: Click "Edit Mode" button and enter passcode `pte2024`
3. **Adding Content**: In edit mode, use "Add Content" buttons or admin panel
4. **Content Types**:
   - **YouTube Videos**: Paste full YouTube URLs for automatic embedding
   - **Notes**: Rich text content for study materials
   - **Important Links**: External websites and resources
   - **Text Content**: General text information

## Customization

- Change edit passcode in `guide/views.py` (line 9)
- Modify sections in the admin panel or `guide/models.py`
- Update styling in templates or add custom CSS
- Add more content types by extending the models

## Security Notes

- Change the default SECRET_KEY in `settings.py` for production
- Set DEBUG = False in production
- Use environment variables for sensitive settings
- Consider using a proper authentication system for production use