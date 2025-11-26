# Django Blog - Setup và Chạy dự án

## Bước 1: Cài đặt MySQL Server

Đảm bảo MySQL Server đã được cài đặt và đang chạy trên máy.

## Bước 2: Tạo Database

Mở MySQL command line hoặc MySQL Workbench và chạy:

```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'hien2024';
GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_user'@'localhost';
FLUSH PRIVILEGES;
```

## Bước 3: Cài đặt dependencies

```powershell
cd d:\Data\blog
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Bước 4: Cấu hình Database

Mở file `blog_project/settings.py` và cập nhật thông tin MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_db',
        'USER': 'blog_user',
        'PASSWORD': 'hien2024',  # Thay đổi password nếu cần
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Bước 5: Tạo migrations và migrate

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Bước 6: Tạo superuser

```powershell
python manage.py createsuperuser
```

Nhập thông tin:
- Username: admin (hoặc tên bạn muốn)
- Email: your-email@example.com
- Password: (mật khẩu mạnh)

## Bước 7: Chạy server

```powershell
python manage.py runserver
```

Truy cập:
- **Trang chủ blog**: http://localhost:8000/
- **Admin panel**: http://localhost:8000/admin/

## Bước 8: Tạo dữ liệu mẫu

1. Đăng nhập vào Admin panel
2. Tạo Categories (Danh mục):
   - Django
   - Python
   - Database
   - Web Development
   
3. Tạo Tags (Thẻ):
   - tutorial
   - tips
   - guide
   - best-practices
   
4. Tạo Posts (Bài viết):
   - Điền đầy đủ: title, content, category, tags
   - Chọn status = "Đã xuất bản"
   - Upload featured image (nếu có)

## Tính năng chính

✅ Quản lý bài viết với editor
✅ Phân loại theo danh mục và thẻ
✅ Hệ thống bình luận (cần duyệt)
✅ Tìm kiếm bài viết
✅ Responsive design (mobile-friendly)
✅ Admin dashboard đầy đủ
✅ Thống kê lượt xem

## Lưu ý

- Thay đổi `SECRET_KEY` trong `settings.py` trước khi deploy production
- Đặt `DEBUG = False` khi deploy
- Cấu hình ALLOWED_HOSTS phù hợp với domain của bạn
- Sử dụng web server như nginx + gunicorn cho production
