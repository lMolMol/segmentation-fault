import sqlite3

from Syllabot.data.CourseSyllabus import CourseSyllabus


class Database:
    def __init__(self, db_name="courses.db"):
        """Initialize the database connection and create the tables if they don't exist."""
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        """Creates the courses and emails tables if they don't already exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_code TEXT NOT NULL UNIQUE,
                    course_name TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    semester TEXT NOT NULL,
                    course_outline TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS course_registrations (
                    email_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    FOREIGN KEY (email_id) REFERENCES emails(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    PRIMARY KEY (email_id, course_id)
                )
            """)

            conn.commit()

    def insert_course(self, course_code, course_name, year, semester, course_outline):
        """Inserts a new course into the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO courses (course_code, course_name, year, semester, course_outline) 
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (course_code, course_name, year, semester, course_outline),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Course {course_code} already exists!")

    def insert_email(self, email):
        """Inserts a new email into the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT OR IGNORE INTO emails (email) VALUES (?)", (email,))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Email {email} already exists!")

    def register_email_to_course(self, email, course_code):
        """Registers an email to a course."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM emails WHERE email = ?", (email,))
            email_id = cursor.fetchone()

            cursor.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,))
            course_id = cursor.fetchone()

            if not email_id:
                self.insert_email(email)
                cursor.execute("SELECT id FROM emails WHERE email = ?", (email,))
                email_id = cursor.fetchone()
            if not course_id:
                raise ValueError(f"Course {course_code} not found.")

            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO course_registrations (email_id, course_id) VALUES (?, ?)",
                    (email_id[0], course_id[0]),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Email {email} is already registered in course {course_code}!")

    def unregister_email_from_course(self, email, course_code):
        """Unregisters an email from a course."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM emails WHERE email = ?", (email,))
            email_id = cursor.fetchone()

            cursor.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,))
            course_id = cursor.fetchone()

            if not email_id:
                raise ValueError(f"Email {email} not found.")
            if not course_id:
                raise ValueError(f"Course {course_code} not found.")

            cursor.execute(
                "DELETE FROM course_registrations WHERE email_id = ? AND course_id = ?",
                (email_id[0], course_id[0]),
            )
            conn.commit()


    def fetch_courses(self):
        """Fetches all courses from the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            return cursor.fetchall()

    def fetch_registered_emails(self, course_code):
        """Fetches all emails registered in a specific course."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT emails.email FROM emails
                JOIN course_registrations ON emails.id = course_registrations.email_id
                JOIN courses ON courses.id = course_registrations.course_id
                WHERE courses.course_code = ?
                """,
                (course_code,),
            )
            return cursor.fetchall()

    def fetch_registered_courses(self, email):
        """Fetches all courses a specific email is registered in."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT courses.course_code, courses.course_name FROM courses
                JOIN course_registrations ON courses.id = course_registrations.course_id
                JOIN emails ON emails.id = course_registrations.email_id
                WHERE emails.email = ?
                """,
                (email,),
            )
            return cursor.fetchall()

    def fetch_all_email(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM emails")
            return cursor.fetchall()

    def fill_data(self):
        self.insert_course("COMP 1012", "Computer Science 1", 2025, "Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("COMP 1020", "Data Structures", 2025, "Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("MATH 1300", "Linear Algebra", 2025, "Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("STAT 1000", "Introductory Statistics", 2025, "Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("PHIL 1290", "Critical Thinking", 2025, "Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("COMP 2160","Programming Practices", 2025,"Fall",CourseSyllabus.SYLLABUS)
        self.insert_course("COMP 2140","Data Structures & Algorithms",2025,"Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("COMP 2080","Analysis of Algorithms",2025,"Fall",CourseSyllabus.SYLLABUS)
        self.insert_course("ECON 1010","Introduction to Microeconomics",2025,"Fall", CourseSyllabus.SYLLABUS)
        self.insert_course("ECON 1020","Introduction to Macroeconomics",2025,"Fall", CourseSyllabus.SYLLABUS)
        print(self.fetch_courses())


