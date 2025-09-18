# The Logic For User Account Management System

This Python Logic project provides a simple yet secure user account management system. It handles user registration, login with password hashing, password updates, account deletion with backup, and account restoration using a MySQL database.

---

## Features

- Secure user signup with password hashing using bcrypt.
- User login with email and username verification.
- Password update functionality with encrypted storage.
- Account deletion that backs up deleted users to a separate table.
- Restore deleted accounts seamlessly.
- Uses environment variables to securely manage database credentials.
- Graceful input validation and user prompts.
- Database tables auto-created if not existing.

---

## Requirements

- Python 3.7 or higher
- MySQL server running and accessible
- The following Python packages:
  - mysql-connector-python
  - python-dotenv
  - bcrypt

---

## Setup Instructions

1. **Clone or download** this repository.

2. **Create a `.env` file** in the project root folder with your database credentials:

   ```ini
   DB_HOST=your_database_host
   DB_USER=your_database_username
   DB_PASSWORD=your_database_password
   DB_NAME=your_database_name
3. **Install the required Python packages** by running:

   pip install -r requirements.txt

4. **Run the script**

   python main.py

5. Follow the on-screen prompts to use the system (login, signup, change password, delete account, restore account).

## How It Works
- On startup, the script connects to the MySQL database using credentials from the .env file.

- It creates the necessary tables (users_data, deleted_data) if they don't exist.

- User passwords are securely hashed with bcrypt before storing.

- Login validates credentials by comparing input password with hashed password in DB.

- Deleted accounts are moved to a backup table before removal.

- Users can restore deleted accounts by providing their old credentials.

- The program provides a menu-driven command-line interface for user interactions.



## Project Structure
```
/project_root
│
├── .env                   # Environment variables for DB credentials
├── main.py                # Main Python script with user account management code
├── requirements.txt       # Required Python packages
└── README.md              # This file
