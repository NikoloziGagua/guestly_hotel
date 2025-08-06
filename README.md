# 🏨 Guestly – Hotel Management System

Guestly is a Django-based hotel management system designed to model hospitality operations. It supports role-based workflows for guests, receptionists, housekeeping, and managers, covering booking, check-in, room service, cleaning, and staff payment management.

**Recomemded to read intro_to_guestly bfore this file**
----

## Features

### 👤 Guest
- Browse and book available rooms
- Submit food orders and service requests (cleaning, maintenance, extra towels)
- Track booking status, payments, and food delivery

### 🧾 Receptionist
- Check guests in and out
- View all bookings
- Notify housekeeping of check-outs for cleaning

### 🧼 Housekeeping
- View rooms requiring cleaning
- Mark rooms as cleaned
- Receive real-time check-out updates

### 👨‍💼 Manager
- Full room management (add, edit, delete, view)
- Manage bookings and food menu
- View service requests, users, staff payments, and reports
- Assign user roles and monitor activity

## 🛠 Modules
- **Room Management**: Tracks room types, availability, pricing, and cleaning status
- **Booking System**: Handles room bookings, check-in/out, and availability updates
- **Payments**: Links tasks to payments, visible in dashboards and manager reports
- **Room Service**: Manages guest food and service requests with status tracking
- **Cleaning Workflow**: Automates cleaning assignments and room status updates
- **User Management**: Uses Django’s authentication for role-based access and user creation

## 💻 Technical Overview
### Backend
- **Framework**: Django 4.x
- **Database**: MySQL (primary) or SQLite (alternative)
- **Migrations**: Managed via Django ORM
- **Fixtures**: Pre-populate data for rooms, payments, services, and users

### Frontend
- HTML, CSS, bootstrap and vanilla JavaScript
- Role-separated dashboards
- Responsive design with planned animations

### Security
- Role-based access control
- Secure login/logout
- Restricted dashboard access

## 🚀 Run Guestly Locally

### 1. Prerequisites
- Python 3.8+
- pip (included with Python)
- Git
- MySQL (optional, for production-like setup)

> SQLite is sufficient for testing and requires no additional setup.

### 2. Clone the Repository
```bash
git clone https://github.com/NikoloziGagua/guestly_hotel.git
cd guestly_hotel
```

### 3. Set Up a Virtual Environment
```bash
python -m venv venv
```
- **macOS/Linux**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Setup

#### Option A: SQLite (Quick Setup)
1. In `settings.py`, ensure:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```
2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

#### Option B: MySQL (Production-Like)
1. Install MySQL and create a database:
   ```sql
   CREATE DATABASE guestly CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Create a `.env` file in the project root:
   ```
   DB_NAME=guestly
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=3306
   ```
3. Update `settings.py`:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': os.getenv('DB_NAME'),
           'USER': os.getenv('DB_USER'),
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': os.getenv('DB_HOST'),
           'PORT': os.getenv('DB_PORT'),
       }
   }
   ```
4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 6. Load Fixtures
Pre-populate the database with sample data:
```bash
python manage.py loaddata rooms/fixtures/rooms.json
python manage.py loaddata payments/fixtures/salaryrates.json
python manage.py loaddata services/fixtures/food_menu.json
```
> Ensure migrations are applied before loading fixtures.

### 7. Run the Development Server
```bash
python manage.py runserver
```
Access the app at: `http://127.0.0.1:8000/users/users/main`
## 💬 Using Guestly
1. **Create account**: You will create guest account, in guestly staff accounts are created by the manager
2. **Log in**: Log in as guest, and explore what guests can do
3. **Developer Mode**:
   - Enable to explore all features without restrictions.
   - Disable to test role-based access.
   - While in Dev mode go to MANAGER-> VIEW ALL USERS from here you can add staff
4. **Try Features**:
   - **Guest**: Book rooms, request services.
   - **Receptionist**: Check guests in/out.
   - **Housekeeping**: Mark rooms as cleaned.
   - **Manager**: Manage rooms, users, and reports.

##  Notes
- Built entirely with Django’s template system (no APIs or frontend frameworks).
- Designed for demonstration purposes to showcase development skills.
- Extensible for theming or API integration.
- Congrats 🎉 You’re running Guestly!

### author **Nikolozi Gagua**
