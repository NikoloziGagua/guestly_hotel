   # 🏨 Guestly – Comprehensive Overview 
-line175- how to run guestly yourself-
## 🧠 What is Guestly?
Guestly is a replica of a small hotel management system replica built with Django. It models hotel operations and enhances guest experiences by providing role-based workflows for every part of the hospitality process — from booking and check-in to room service, cleaning, and staff payment management.

---
# 🔑 Role-Based System
Guestly is centered around four primary roles, each with its own access level, dashboard, and permissions:

### 👤 Guest
View available rooms

book a room

Submit food order

Submit service request(cleaning, maintanance, extra towels)

Track booking status

Track payment

Track food delivey status

---
### 🧾 Receptionist
Check guests in 

Check guest out

View all  bookings

Tell housekeeping when guest is check out so they can clean

---

### 🧼 Housekeeping
View rooms that need cleaning

Mark rooms as cleaned

Receive real-time updates from check-outs

---
### 👨‍💼 Manager

Full access to room managment

view all rooms

edit rooms

delete rooms

add rooms

view all bookings

manage food menu(add new item, delete, edit items)

view all service requests

view all users

assign roles to users

view staff payments

view reports

View staff and guest activity

---
# 🔍 Module Breakdown
### 🛏️ Room Management
Room types with availability, and pricing

Room availability and booking integration

Cleaning status tracking

Room-type table used instead of choices (more flexible)

---
### 📆 Booking System
Guests can book available rooms based on check-in/check-out dates

Receptionists chenk in/out guests manually

Bookings change room availability automatically

Check-out triggers room status as “needs cleaning”

---
### 🧾 Payments
linked to all roles(exept manager)

is triggered by compleated task by said role

Visible in payment dashboards

affects manager reports

---
### 🍽 Room Service
Guests can request food and services

Requests tracked and updated in real time

Supports status changes (e.g., pending → completed)

---
### 🧼 Cleaning Workflow
Housekeeping sees rooms marked “needs cleaning”

Once cleaned, rooms are marked “ready”

System automatically updates room availability

---
### 👥 User Management
Users stored with Django’s built-in authentication


Admin and manager can create and manage users

Login system supports role-based routing

# 💡 Technical Overview
### 🧱 Backend
Framework: Django 4.x

Database: MySQL (primary) or SQLite (alternative)

Migrations: Handled by Django ORM

Fixtures: Provided in rooms/, payments/, services/, and users/ for easy demo setup

---
### 🌐 Frontend
Built using HTML, CSS, and vanilla JavaScript

Clean, light-themed interface

Fully role-separated dashboards

Animated elements and responsive design planned

---
🔐 Security
Role-based access control for each view

Login/logout routes

Users cannot access other dashboards or perform restricted actions

---

# 🚀 RUN GUESTLY YOURSELF

Follow this step-by-step guide to set up and run the Guestly project locally.



### 🔧 1. Prerequisites

Before getting started, make sure you have the following installed:

- **Python 3.8+** – Required for running Django
- **pip** – Comes with Python (used for installing Python packages)
- **Git** – Used to clone the repository
- **MySQL** *(optional)* – Only needed if you choose to use MySQL instead of SQLite

> You do **not** need to install MySQL if you choose to use SQLite (explained below).

### 📁 2. Clone the Repository

This will download the Guestly project to your machine.

         git clone https://github.com/NikoloziGagua/guestly_hotel.git

         cd guestly_hotel
         

### 🐍 3. Set Up a Virtual Environment

Using a virtual environment ensures your Python dependencies are isolated from other projects.

create virtual enviroment

         python -m venv venv

macOS/Linux:         source venv/bin/activate

Windows:             venv\Scripts\activate
         cd guestly
### 📦 4. Install Python Dependencies
Install all required libraries listed in requirements.txt:

         pip install -r requirements.txt

This includes Django, MySQL support (if needed), and other packages used in the project.


# 💾 Database Setup Options
You have two options for setting up your database:
___
### 🔵 Option A: Use SQLite (Best for testing and quick setup)
SQLite is lightweight and doesn’t require any installation.

### ⚙️ Step 1: Use SQLite Settings in settings.py
Comment out the MySQL section and replace it with the following:

      DATABASES = {

          'default': {
    
              'ENGINE': 'django.db.backends.sqlite3',
           
              'NAME': BASE_DIR / 'db.sqlite3',
           
          }
    
      }

This tells Django to use a simple .sqlite3 file for storing your data.
### 🔨 5. Apply Migrations
Migrations set up your database schema (tables and structure) based on your Django models.

         python manage.py makemigrations
         python manage.py migrate
This will:

Create the necessary tables

Prepare your database (MySQL or SQLite) for use

---
### 🟢 Option B: Use MySQL (Recommended for production-like environments)
This method connects Django to a MySQL database, providing better performance and scalability.

### 🛠 Step 1: Install MySQL
Make sure MySQL is installed on your machine. You can download it from mysql.com.

### 🗃 Step 2: Create a MySQL Database
Use your MySQL CLI or GUI tool (like phpMyAdmin or MySQL Workbench) to create a new database:

         CREATE DATABASE guestly CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

### 🔐 Step 3: Create a .env File

In the root of the project, create a file named .env and paste your MySQL credentials:


      DB_NAME=guestly
      DB_USER=root
      DB_PASSWORD=yourpassword
      DB_HOST=localhost
      DB_PORT=3306

### ⚙️ Step 4: Update settings.py
Make sure your settings.py uses the .env variables like this:


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




### 🔨 5. Apply Migrations
Migrations set up your database schema (tables and structure) based on your Django models.

      python manage.py makemigrations
      python manage.py migrate
This will:

Create the necessary tables

Prepare your database (MySQL or SQLite) for use

### 🧩 6. Load Initial Data with Fixtures
Fixtures are JSON files that pre-populate your database with necessary data (like rooms, users, services, and payments).

This is especially useful if you're using SQLite or setting up MySQL for the first time.

To load all fixtures, run the following commands:

      python manage.py loaddata rooms/fixtures/rooms.json

      python manage.py loaddata payments/fixtures/salaryrates.json

      python manage.py loaddata services/fixtures/food_menu.json

      python manage.py loaddata users/fixtures/users.json

### 💡 Make sure your database is migrated before loading fixtures (python manage.py migrate), and that your virtual environment is activated.

These commands will:

Set up initial room types and details

Add default payment records

Populate available services

Create sample users and roles



### ▶️ 8. Run the Development Server
Start your server locally:


      python manage.py runserver

Visit the application in your browser:

      http://127.0.0.1:8000/users/users/main
# 💬 How to Use the Application
1. **log in as super user** go to login page username:super passowrd:super 
1. **Start with Developer Mode ON** to explore features and UI.
2. **Log in as any sample user** to experience individual roles:
   - Guest: Try booking a room and requesting room service.
   - Receptionist: Perform a check-in or cancel a booking.
   - Housekeeping: Mark a room as cleaned.
   - Manager: View all staff, control salaries, review performance.
3. **Turn OFF Developer Mode** to test real access restrictions.
   ***all passwords for already created users is Nikolozi12***
Final Notes

- Guestly is a fully working simulation of a hotel management workflow.
- This project was developed entirely using Django's template system (no APIs or frontend frameworks).
- Developer Mode makes it easy to test everything without login.
-This application is purely made for demonstrating what I can do
- Ready for extension, theming, or API integration later!
---
congrats 🎉 you are running guestly
___

