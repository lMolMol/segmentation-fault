from Syllabot.data.Database import Database

db=Database("test-data.db")

db = Database("teeeest_courses.db")
try:
    db.insert_email("test@example.com")
    db.insert_email("test@example.com")  # Should raise an error
except ValueError as e:
    print("Integrity Test Passed:", e)

try:
    db.insert_course("CS101", "Intro to CS", 2025, "Fall", "Basic CS course outline")
    db.insert_course("CS101", "Intro to CS", 2025, "Fall", "Basic CS course outline")  # Should raise an error
except ValueError as e:
    print("Integrity Test Passed:", e)

db.register_email_to_course("test@example.com", "CS101")
print("Registered emails for CS101:", db.fetch_registered_emails("CS101"))

try:
    db.register_email_to_course("test@example.com", "CS101")  # Should raise an error
except ValueError as e:
    print("Integrity Test Passed:", e)

db.unregister_email_from_course("test@example.com", "CS101")
print("Registered emails after unregistration:", db.fetch_registered_emails("CS101"))
db.register_email_to_course("test@example.com", "CS101")
print("Courses registered by test@example.com:", db.fetch_registered_courses("test@example.com"))
db.unregister_email_from_course("test@example.com", "CS101")
print("Courses after unregistration:", db.fetch_registered_courses("test@example.com"))
