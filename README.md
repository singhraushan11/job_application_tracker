# Job Application Tracker

A command-line based Job Application Tracker developed using Python and MySQL. This application help users manage job applications efficiently by storing records in a MySQL database.

## Features

- **Add Application** – Add a new job application with company name, role, applied date, status, and notes.
- **View Applications** – Display all saved job applications.
- **Search Applications** – Search applications by company name, role.
- **Update Status** – Update the status of an existing application.
- **Delete Application** – Remove an application from the database.
- **Input Validation** – Prevent invalid or empty user input.
- **Exception Handling** – Handle invalid input and database errors gracefully.
- **Secure Configuration** – Store database credentials securely using a `.env` file.

## Technologies Used

- Python
- MySQL
- mysql-connector-python
- python-dotenv

## Project Files

- **main.py** – Main application logic.
- **schema.sql** – Creates the database and applications table.
- **.env** – Stores database credentials (not included in repo).
- **.env.example** – Sample file showing required environment variables.
- **requirements.txt** – Lists the required Python packages.
- **.gitignore** – Prevents sensitive files from being uploaded to GitHub.

## How to Run

1. Clone or download this repository.
2. Install the required Python packages:

```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the project root (refer to `.env.example` for the required variables) and add your MySQL database credentials:

```env
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=job_tracker
```

4. Run the `schema.sql` file to create the database and table.
5. Start the application:

```bash
   python main.py
```

## Author

**Raushan**