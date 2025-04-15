Guestly - Hotel Management System 🏨

Guestly is a complete, multi-role hotel management system designed to simulate real-world hotel operations in a clean and responsive user interface. Whether you're a guest booking a room or a manager reviewing service performance, Guestly delivers an organized, intuitive experience.

Features

-  Role-Based Access:
  - **Guest**: View available rooms, book stays, check-in/check-out, request services.
  - **Receptionist**: Manage bookings, perform check-ins & check-outs, monitor room status.
  - **Housekeeping**: View rooms needing cleaning, mark rooms as cleaned.
  - **Manager**: Full access to manager control panel .

- 📦 Developer Mode (for demo/testing):
  - Bypass login restrictions.
  - Toggle visibility of all dashboards via a **Developer Mode** button.
  - Easily explore the entire app without needing real authentication.

-  Clean UI with full styling using **Bootstrap 5** and custom CSS.
-  Fully responsive design.



Getting Started

Follow these steps to get Guestly up and running locally:

1. Clone the Repository
git clone https://github.com/NikoloziGagua/guestly.git
cd guestly

2. Create Virtual Environment and Install Dependencies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Apply Migrations
python manage.py makemigrations
python manage.py migrate

4. Run the Development Server
python manage.py runserver

Visit http://127.0.0.1:8000/users/users/main in your browser.





🧪 Sample User Accounts

To demonstrate the app's full capabilities, Guestly comes with pre-created user accounts. All use the same password:

**Password for all accounts:** `Nikolozi12`

username	Role         	Description               
guest1	Guest        	Can book rooms, request services
receptionist1	Receptionist	Manage bookings & check-ins
receptionist1	Housekeeping	See & clean rooms          
manager1	Manager      	Oversee everything

🛠 Developer Mode (Toggle View)

This app includes a built-in **Developer Mode** for demo purposes. When enabled:

- You bypass role restrictions (no login needed).
- You can instantly view **all dashboards**.
- Great for showing the system without managing user sessions.

🧪 Just click the **"Toggle Developer Mode"** button at the top of any page.

When **Developer Mode is OFF**:
- Regular role-based login is enforced.
- Pages like `manager dashboard` or `housekeeping panel` require role authentication.



🛏 Preloaded Database Content

- ✅ 4 sample users (listed above)
- ✅ 6 rooms with types like `Single`, `Double`, `Suite`
- ✅ Pre-populated food & service menus

——————————————————————————————————————————————————

💬 How to Use the Application

1. **Start with Developer Mode ON** to explore features and UI.
2. **Log in as any sample user** to experience individual roles:
   - Guest: Try booking a room and requesting room service.
   - Receptionist: Perform a check-in or cancel a booking.
   - Housekeeping: Mark a room as cleaned.
   - Manager: View all staff, control salaries, review performance.
3. **Turn OFF Developer Mode** to test real access restrictions.
Final Notes

- Guestly is a fully working simulation of a hotel management workflow.
- This project was developed entirely using Django's template system (no APIs or frontend frameworks).
- Developer Mode makes it easy to test everything without login.
-This application is purely made for demonstrating what I can do
- Ready for extension, theming, or API integration later!
