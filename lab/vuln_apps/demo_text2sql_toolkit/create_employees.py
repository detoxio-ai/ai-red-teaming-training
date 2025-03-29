# import sqlite3
# import os

# # Determine the path for the database file inside the 'db' folder.
# base_dir = os.path.dirname(os.path.abspath(__file__))
# db_dir = os.path.join(base_dir, "db")
# os.makedirs(db_dir, exist_ok=True)
# db_file = os.path.join(db_dir, "example.db")

# # Connect to the SQLite database (it will be created if it doesn't exist)
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()

# # Create the 'employees' table with appropriate columns.
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS employees (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     position TEXT,
#     department TEXT,
#     email TEXT,
#     salary REAL,
#     joining_date TEXT
# )
# """)

# # Prepare 30 rows of employee data (Indian Hindu popular names).
# employees = [
#     ("Mithlesh Upadhyay", "Senior Developer", "IT", "mithlesh.upadhyay@example.com", 75000.00, "2022-01-15"),
#     ("Rudra Upadhyay", "Project Manager", "IT", "rudra.upadhyay@example.com", 90000.00, "2021-11-10"),
#     ("Aarav Sharma", "Software Engineer", "IT", "aarav.sharma@example.com", 60000.00, "2022-03-20"),
#     ("Vivaan Gupta", "Data Analyst", "Finance", "vivaan.gupta@example.com", 58000.00, "2022-05-10"),
#     ("Aditya Singh", "HR Specialist", "HR", "aditya.singh@example.com", 50000.00, "2021-07-01"),
#     ("Advait Patel", "Business Analyst", "Business", "advait.patel@example.com", 65000.00, "2022-04-15"),
#     ("Arjun Reddy", "Developer", "IT", "arjun.reddy@example.com", 62000.00, "2022-02-28"),
#     ("Rohan Mehta", "System Administrator", "IT", "rohan.mehta@example.com", 55000.00, "2021-12-05"),
#     ("Siddharth Joshi", "Marketing Manager", "Marketing", "siddharth.joshi@example.com", 70000.00, "2022-06-18"),
#     ("Kunal Rao", "Operations Manager", "Operations", "kunal.rao@example.com", 72000.00, "2021-08-12"),
#     ("Rajesh Khanna", "Finance Manager", "Finance", "rajesh.khanna@example.com", 80000.00, "2022-01-30"),
#     ("Sanjay Kumar", "Sales Executive", "Sales", "sanjay.kumar@example.com", 48000.00, "2022-03-01"),
#     ("Pranav Verma", "Developer", "IT", "pranav.verma@example.com", 61000.00, "2022-07-07"),
#     ("Tarun Desai", "Data Scientist", "IT", "tarun.desai@example.com", 68000.00, "2022-05-25"),
#     ("Neeraj Chawla", "Customer Support", "Support", "neeraj.chawla@example.com", 40000.00, "2022-08-12"),
#     ("Manish Agarwal", "Senior Developer", "IT", "manish.agarwal@example.com", 77000.00, "2021-10-20"),
#     ("Abhishek Mishra", "Product Manager", "Product", "abhishek.mishra@example.com", 85000.00, "2022-04-30"),
#     ("Aniket Kulkarni", "QA Engineer", "IT", "aniket.kulkarni@example.com", 57000.00, "2022-02-15"),
#     ("Saurabh Deshpande", "Developer", "IT", "saurabh.deshpande@example.com", 63000.00, "2022-06-02"),
#     ("Harshad Rane", "Network Engineer", "IT", "harshad.rane@example.com", 54000.00, "2022-01-12"),
#     ("Dhruv Menon", "Software Engineer", "IT", "dhruv.menon@example.com", 61000.00, "2022-03-14"),
#     ("Varun Pillai", "Consultant", "Consulting", "varun.pillai@example.com", 70000.00, "2022-04-18"),
#     ("Omkar Iyer", "Developer", "IT", "omkar.iyer@example.com", 60000.00, "2022-02-02"),
#     ("Praveen Nair", "Data Analyst", "Finance", "praveen.nair@example.com", 59000.00, "2022-05-08"),
#     ("Ishaan Chatterjee", "Business Analyst", "Business", "ishaan.chatterjee@example.com", 65000.00, "2022-03-22"),
#     ("Gaurav Sinha", "HR Manager", "HR", "gaurav.sinha@example.com", 75000.00, "2022-01-10"),
#     ("Karan Kapoor", "Developer", "IT", "karan.kapoor@example.com", 62000.00, "2022-06-15"),
#     ("Nikhil Jain", "Product Designer", "Design", "nikhil.jain@example.com", 68000.00, "2022-07-20"),
#     ("Rahul Tripathi", "Finance Analyst", "Finance", "rahul.tripathi@example.com", 64000.00, "2022-04-05"),
#     ("Sameer Goyal", "Sales Manager", "Sales", "sameer.goyal@example.com", 72000.00, "2022-02-25")
# ]

# # Insert all employee rows into the table.
# cursor.executemany("""
# INSERT INTO employees (name, position, department, email, salary, joining_date)
# VALUES (?, ?, ?, ?, ?, ?)
# """, employees)

# conn.commit()
# conn.close()

# print("Employee table created and populated successfully.")
