from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Your API key and endpoint
API_KEY = ""#"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"
url = "https://openrouter.ai/api/v1/chat/completions"

# Your syllabus info (or any long text content)
info = """Programming Practices
 COMP 2160 A01
 Department of Computer Science
 University of Manitoba
 COMP 2160– Winter 2025
 Programming Practices
 ROASS Document
 Section
 Instructor
 Form of address
 Email
 Lecture
 Office hours
 Contents
 1 Course Content
 A01
 Tim Zapp
 Tim (They/Them)
 zappt3@myumanitoba.ca
 10:30am– 11:20am on Mondays, Wednesdays, and Fridays in 172 Agriculture.
 1:00pm– 2:30pm on Tuesdays and Thursdays in EITC E2-511, or by appointment.
 course description, goals, prerequisites, textbooks, schedule
 2 Contact
 course website, class and office hours, email policy
 3 Assessment
 academic integrity policies, marking scheme, due dates and midterm date, illness policies,
 letter grades
 4 Dates and Policies
 important dates, copyright and class recordings, additional policies and links
 2
 3
 4
 6
 1
Programming Practices
 COMP 2160 A01
 Department of Computer Science
 University of Manitoba
 1 Course Content
 1.1 Course Description
 Introduction to issues involved in real-world computing. Topics will include memory management,
 debugging, compilation, performance, and good programming practices.
 1.2 Course Goals
 Upon completing this course, students should be able to:
 • (Idioms) Write software using an unfamiliar programming language idiomatically.
 • (Design) Break software down into functional units.
 • (UNIX) Use a UNIX or UNIX-like operating system to write and build software.
 • (DbC) Write code that does not crash.
 • (Testing) Test and debug software.
 • (Performance) Identify performance problems and solve them with optimizations.
 1.3 Prerequisites
 Students must have completed the following course with a minimum grade of:
 • C+ or higher in COMP 1020 or COMP 1021.
 1.4 Textbook
 There is no required textbook for this course. The following books are recommended:
 • Programming Pearls, second edition by Jon Bentley, Addison Wesley, 2000.
 • The C Programming Language, Second Edition by Brian Kernighan and Dennis
 Ritchie, Prentice Hall, 1988.
 2
Programming Practices
 COMP 2160 A01
 Department of Computer Science
 University of Manitoba
 2 Contact
 2.1 Class Meetings and Course Content
 Classes will be held in person on Mondays, Wednesdays, and Fridays from 10:30am– 11:20am in
 172 agriculture.
 If you are sick, stay home! Although classes will not be recorded, all notes shown during class will
 be posted on UM Learn.
 If your instructor is sick, either a substitute lecturer will be found or a class cancellation announce
ment will be posted on UM Learn.
 2.2 Office Hours
 Office hours will take place in person on Tuesdays and Thursdays from 1:00pm– 2:30pm in EITC
 E2-511, or by appointment.
 2.3 Email Policy
 The best way to contact your instructor is by email. Volume permitting, I will attempt to reply to
 emails within 1 business day.
 The University requires all students to activate an official University of Manitoba email account,
 and use this account for all communication between yourself and the university. Please note that
 all communication between the instructor and you as a student must comply with the Electronic
 Communication with Students policy.
 3
Programming Practices
 COMP 2160 A01
 Department of Computer Science
 University of Manitoba
 3 Assessment
 3.1 Academic Integrity Policies
 Students are expected to familiarize themselves with the Computer Science Department expec
tations for individual work. These expectations apply to all graded components of this course:
 quizzes, assignments, midterm and final exam.
 The Faculty of Science takes academic integrity very seriously. Any evidence of academic dishonesty
 on assignments or tests will be forwarded to the appropriate authorities for potential disciplinary
 actions.
 The University Student Discipline By-Law may be accessed here. Information from the Faculty of
 Science regarding Academic Integrity can be found here.
 3.2 Grading Scheme
 Grades will be calculated as follows.
 Assignments
 Midterm exam
 Final exam
 25%
 25%
 50%
 3.3 Assignments
 There will be 4 assignments. The assignments will be weighted equally. Assignments must be com
pleted independently, without any collaboration, discussion, or consultation with others, including
 posting questions to online forums. You may have general discussions about course content and
 class examples with your peers, but you must complete the assignment questions yourself.
 Illness policy. As per the Self-Declaration for Brief and Temporary Absences Procedure and
 Policy, medical documentation is not required for absences of up to 120 hours. A self-declaration
 form must be submitted instead.
 If you miss an assignment deadline due to illness or other circumstances, please submit this form
 either in person or by email as soon as possible, and no later than 48 hours after the absence. The
 weight of the missed assignment will be shifted to the final exam.
 In the absence of documentation, late assignments will receive a score of 0.
 Additional documentation may be requested from students who claim multiple temporary absences
 or absences for more than 120 hours. If you miss significantly more of the course than is covered
 by the Temporary Absences Policy, you should consider speaking to an Academic Advisor about
 an authorized withdrawal.
 Assignment regrading policy. After each assignment’s grades have been published, a folder for
 regrading requests will be opened on UM Learn. If you believe that there is an error in the grading
 of your assignment, please write up a summary of the issue and submit it to this folder. You will
 have one week after the grades have been posted to submit your regrading requests. No requests
 past this deadline will be considered. It is your responsibility to review your assignment feedback
 in a timely manner.
 4
Programming Practices
 COMP 2160 A01
 Department of Computer Science
 University of Manitoba
 3.4 Midterm
 A 50-minute midterm exam will take place in person in class. The tentative date for the midterm
 is February 14, 2025, although this may be changed (such a change would be announced in class
 and on the course UMLearn page).
 Illness policy. As per the Self-Declaration for Brief and Temporary Absences Procedure and
 Policy, medical documentation is not required for absences of up to 120 hours. A self-declaration
 form must be submitted instead.
 If you miss the midterm due to illness or other circumstances, please submit this form either in
 person or by email as soon as possible, and no later than 48 hours after the absence. The weight
 of the midterm will be shifted to the final exam.
 In the absence of documentation, a missed midterm will receive a score of 0.
 Additional documentation may be requested from students who claim multiple temporary absences
 or absences for more than 120 hours. If you miss significantly more of the course than is covered
 by the Temporary Absences Policy, you should consider speaking to an Academic Advisor about
 an authorized withdrawal.
 3.5 Final Exam
 A final exam will be scheduled during the Final Exam Period. The final exam will be two hours
 in length. If you miss the final exam due to illness, you must contact an Academic Advisor in the
 Faculty of Science to request a deferred final. Please familiarize yourself with the policies here.
 A passing grade on the final exam is required in order to pass the class.
 3.6 Letter Grades
 Letter grades will be allocated according to the following scale.
 Grade Lower Bound
 A+ 92
 A 82
 B+ 77
 B 70
 C+ 65
 C 60
 D 50
 F 0
 5
Programming Practices
 COMP 2160 A01
 Department of Computer Science
 University of Manitoba
 4 Dates and Policies
 4.1 Important Dates
 January 6, 2025
 January 17, 2025
 January 20, 2025
 February 17, 2025
 First day of classes
 Last date to drop winter term classes
 Last date to register winter term classes
 Louis Riel Day, university closed
 February 18– February 21, 2025 Winter term break
 March 19, 2025
 VWdeadline for winter term classes
 April 11– April 25, 2025
 April 18, 2025
 Exam period
 Good Friday, university closed
 4.2 Academic Accommodations
 The University of Manitoba is committed to providing an accessible academic community. Student
 Accessibility Services (SAS) offers academic accommodation supports and services such as note
taking, interpreting, assistive technology and exam accommodations. Students who have, or think
 they may have, a disability (e.g., mental illness, learning, medical, hearing, injury-related, visual)
 are invited to contact SAS to arrange a confidential consultation.
 520 University Centre
 (204) 474-7423
 Student accessibility@umanitoba.ca
 4.3 Copyright and Class Recordings
 Please respect copyright. We will use copyrighted content in this course. University guidelines
 state that copyrighted works, including those created by the course instructor, are made available
 for private study and research, and must not be distributed in any format without permission.
 Since it is illegal, do not upload copyrighted works to a learning management system (such as UM
 Learn), or any website (such as Course Hero, Chegg, etc.), unless an exception to the Copyright
 Act applies or written permission has been confirmed.
 No audio or video recording of lectures or presentations is allowed in any format, openly or surrep
titiously, in whole or in part without permission from your instructor.
 For more information, see the University’s Copyright Office website.
 4.4 University of Manitoba Policies and Links
 The document ROASS-Appendix.pdf contains a comprehensive list of policies, resources and links.
 This document is available on UM Learn under Content- Syllabus and Schedule.
 6
"""

@app.route("/", methods=["GET"])
def index():
    # Render the main HTML page (index.html)
    return render_template("projPage.html")

@app.route("/submit", methods=["POST"])
def submit():
    # In a more complex example you could extract form data here (email, course selections, etc.)
    # For now, we use a fixed prompt that combines instructions with your syllabus info.
    inp = "Summarize the following content into clean lines and spacings between each one (NO PARAGRAPH FORMAT) [ADD IMPORTANT DETAILS ONLY]: " + info

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [{"role": "user", "content": inp}],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json:
        content = response_json["choices"][0]["message"]["content"]
    else:
        content = "Error: No valid response received."

    # Pass the output to the result page template
    return render_template("result.html", output=content)


if __name__ == "__main__":
    app.run(debug=True)
