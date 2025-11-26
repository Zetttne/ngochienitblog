# Personal Blog - Django + MySQL

Personal blog application built with Django and MySQL featuring posts, categories, tags, comments, and search.

## Features

- 📝 Create and manage blog posts with rich content
- 🏷️ Organize posts by categories and tags
- 💬 Comment system for reader engagement
- 🔍 Search functionality
- 📱 Responsive design with Bootstrap 5
- 👤 Author profiles
- 📊 Admin dashboard for content management

## Setup Instructions

### 1. Install MySQL Server

Make sure MySQL Server is installed and running on your system.

### 2. Create MySQL Database

```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Install Python Dependencies

```powershell
cd d:\Data\blog
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Configure Database

Update `blog_project/settings.py` with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_db',
        'USER': 'blog_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```powershell
python manage.py createsuperuser
```

### 7. Run Development Server

```powershell
python manage.py runserver
```

Visit:
- Blog: http://localhost:8000/
- Admin: http://localhost:8000/admin/

## Project Structure

```
blog/
├── blog_project/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog_app/              # Blog application
│   ├── models.py          # Post, Category, Tag, Comment models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── manage.py
└── requirements.txt
```

## Usage

### Admin Panel

1. Login to `/admin/` with superuser credentials
2. Create categories and tags
3. Write and publish posts
4. Manage comments

### Features

- **Posts**: Full WYSIWYG editor, featured images, SEO-friendly slugs
- **Categories**: Organize posts by topics
- **Tags**: Add multiple tags to posts
- **Comments**: Moderate and manage reader comments
- **Search**: Find posts by title, content, or tags

## Development

Created by **Nguyễn Ngọc Hiền** - Data Processor

Contact for support and inquiries.
