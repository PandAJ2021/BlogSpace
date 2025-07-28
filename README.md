# BlogSpace

BlogSpace is a social blogging platform built with Django and Django REST Framework. It allows users to create, manage, and share blog posts, follow other authors, subscribe for premium content, and manage personal profiles with social links and biometric authentication.

## Features

- **User Authentication**
  - JWT-based authentication using `rest_framework_simplejwt`
  - OTP (One-Time Password) login via phone number
  - Custom user model with profile management

- **Blog System**
  - Create, update, and delete posts with categorization and tags
  - Like and comment on posts
  - Manage published and draft posts

- **Social Features**
  - Follow other authors
  - Subscribe to premium content from authors (with duration and expiry)
  - View and manage social links on user profiles

- **User Profiles**
  - Custom profile fields (name, surname, picture, bio, gender, birth date)
  - Social links integration
  - Private profile endpoints (`/me` for current user)

- **Admin Panel**
  - Manage users, posts, followers, and subscriptions
  - Search and filter capabilities for efficient management

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.2+
- Django REST Framework
- SQLite (default, you may switch to PostgreSQL/MySQL)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/PandAJ2021/BlogSpace.git
   cd BlogSpace
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

### Configuration

- Environment variables can be set for secret keys and other settings.
- Static and media files are served from the `static/` and `media/` directories.
- Change `DEBUG` and `ALLOWED_HOSTS` appropriately for production.

## API Overview

BlogSpace uses RESTful endpoints for all major features. JWT authentication is required for protected endpoints.

- `/api/auth/login/` - Login via JWT or OTP
- `/api/blog/` - Manage posts
- `/api/accounts/profile/` - Manage user profiles
- `/api/relationships/follow/` - Follow/unfollow authors
- `/api/relationships/subscribe/` - Subscribe to premium content

## Folder Structure

- `core/` - Main Django project settings
- `accounts/` - User, profile, and authentication logic
- `blog/` - Blog post logic
- `relationships/` - Follow and subscribe logic

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes.
4. Push to your branch (`git push origin feature-name`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License.
