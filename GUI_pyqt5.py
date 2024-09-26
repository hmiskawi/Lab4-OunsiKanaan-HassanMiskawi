"""
This module defines the PyQt5 GUI for managing students, instructors, and courses
in a school management system. It provides functions to handle adding students, instructors, 
courses, and registering students to courses, as well as assigning instructors to courses.
It also defines functions to set up and manage tables for displaying students, 
instructors, and courses in a PyQt5-based school management system. It includes 
functionality to edit, delete, and filter records based on user input.

Global Lists:
-------------
- students: List of Student objects.
- instructors: List of Instructor objects.
- courses: List of Course objects.

Functions:
----------
- add_student(): Handles the addition of a student to the system.
- add_instructor(): Handles the addition of an instructor to the system.
- add_course(): Handles the addition of a course to the system.
- update_course_dropdown(): Updates the course dropdowns in the GUI.
- register_student_to_course(student_id_str, course_id_str): Registers a student to a course.
- assign_instructor_to_course(iid, course_id): Assigns an instructor to a course.
- setup_students_table(table): Populates a table with student data.
- setup_instructors_table(table): Populates a table with instructor data.
- setup_courses_table(table): Populates a table with course data.
- set_table(students_table, instructors_table, courses_table): Sets up the tables for students, instructors, and courses.
- filter_records(search_term, students_table, instructors_table, courses_table): Filters and displays records based on a search term.
- setup_table_with_buttons(table, data_type): Adds "Edit" and "Delete" buttons to the table for the provided data type.
- delete_record(row, data_type, table): Deletes rows of instances of objects (Student, Instructor, Course) from the local lists
- load_from_json(): Load into the list from a json file.
- save_to_json():Save to a json file the content of the lists.
- export_to_csv():Save the content of the lists into a csv file.

"""


import sys
from PyQt5.QtWidgets import QScrollArea, QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFormLayout, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QInputDialog
from Classes import *
import json
import csv

# Global lists to store data
students = []
instructors = []
courses = []

def add_student():
    """
    Collects data from input fields and creates a new Student object.
    
    The function validates the following:
    
    - The `name`, `age`, `email`, and `student_id` fields are not empty.
    - `age` and `student_id` are converted to integers.
    
    Upon successful validation, a Student object is created and appended
    to the global `students` list. The input fields are then cleared.
    
    Raises:
    -------
    ValueError : If `age` or `student_id` cannot be converted to integers.
    AssertionError : If validation on the `Student` object fails.
    
    GUI Messages:
    -------------
    - A warning message if input validation fails.
    - A success message once the student is added.
    """
    name = student_name.text()
    age = student_age.text()
    email = student_email.text()
    student_id = student_id_field.text()

    if not name or not age or not email or not student_id:
        QMessageBox.warning(window, "Input Error", "Please fill all fields")
        return
    try:
        age = int(age)
        student_id=int(student_id)
    except:
        QMessageBox.warning(window, "Input Error", "Make sure the age and id are integers")

    try:
        student = Student(name, age, email, student_id)
        students.append(student)
        student_name.clear()
        student_age.clear()
        student_email.clear()
        student_id_field.clear()
        QMessageBox.information(window, "Success", f"Student {name} added successfully!")
        update_course_dropdown()
    except (AssertionError, ValueError) as e:
        QMessageBox.warning(window, "Input Error", str(e))


def add_instructor():
    """
    Collects data from input fields and creates a new Instructor object.
    
    The function validates the following:
    
    - The `name`, `age`, `email`, and `instructor_id` fields are not empty.
    - `age` and `instructor_id` are converted to integers.
    
    Upon successful validation, an Instructor object is created and appended
    to the global `instructors` list. The input fields are then cleared.
    
    Raises:
    -------
    ValueError : If `age` or `instructor_id` cannot be converted to integers.
    AssertionError : If validation on the `Instructor` object fails.
    
    GUI Messages:
    -------------
    - A warning message if input validation fails.
    - A success message once the instructor is added.
    """
    name = instructor_name.text()
    age = instructor_age.text()
    email = instructor_email.text()
    instructor_id = instructor_id_field.text()

    if not name or not age or not email or not instructor_id:
        QMessageBox.warning(window, "Input Error", "Please fill all fields")
        return
    try:
        age = int(age)
        instructor_id=int(instructor_id)
    except:
        QMessageBox.warning(window, "Input Error", "Make sure the age and id are integers")
    
    try:
        instructor = Instructor(name, age, email, instructor_id)
        instructors.append(instructor)
        QMessageBox.information(window, "Success", f"Instructor {name} added successfully!")
        instructor_name.clear()
        instructor_age.clear()
        instructor_email.clear()
        instructor_id_field.clear()
    except (AssertionError, ValueError) as e:
        QMessageBox.warning(window, "Input Error", str(e))


def add_course():
    """
    Collects data from input fields and creates a new Course object.
    
    The function validates the following:
    
    - The `course_id` and `course_name` fields are not empty.
    - `course_id` is converted to an integer.
    
    Optionally, the function allows selecting an instructor by name.
    
    Upon successful validation, a Course object is created and appended
    to the global `courses` list. The input fields are then cleared.
    
    Raises:
    -------
    ValueError : If `course_id` cannot be converted to an integer.
    AssertionError : If validation on the `Course` object fails.
    
    GUI Messages:
    -------------
    - A warning message if input validation fails.
    - A success message once the course is added.
    """
    course_id = course_id_field.text()
    course_name = course_name_field.text()
    instructor_name = instructor_name_for_course.text()

    if not course_id or not course_name:
        QMessageBox.warning(window, "Input Error", "Please fill all fields")
        return
    try:
        course_id=int(course_id)
    except:
        QMessageBox.warning(window, "Input Error", "Make sure the course id is an integer")
    
    instructor = next((i for i in instructors if i.name == instructor_name), None) if instructor_name else None

    try:
        course = Course(course_id, course_name, instructor)
        courses.append(course)
        QMessageBox.information(window, "Success", f"Course {course_name} added successfully!")
        course_id_field.clear()
        course_name_field.clear()
        instructor_name_for_course.clear()
        update_course_dropdown()
    except (AssertionError, ValueError) as e:
        QMessageBox.warning(window, "Input Error", str(e))


def update_course_dropdown():
    """
    Updates the course dropdown options in the GUI.

    This function clears and repopulates the course dropdowns used for
    student registration and instructor assignment.
    """
    course_dropdown.clear()
    course_dropdown_i.clear()
    for course in courses:
        course_dropdown.addItem(course.course_name, course.course_id)
        course_dropdown_i.addItem(course.course_name, course.course_id)


def register_student_to_course(student_id_str, course_id_str):
    """
    Registers a student to a course by their ID.
    
    Parameters:
    -----------
    student_id_str : str
        The student ID as a string.
    
    course_id_str : str
        The course ID as a string.
    
    This function converts the student and course IDs to integers, finds
    the respective objects in `students` and `courses`, registers the student
    to the course, and adds the student to the course's enrolled students list.

    Raises:
    -------
    ValueError : If no student or course is found with the provided ID.

    GUI Messages:
    -------------
    - A success message when the student is registered.
    - A warning message if an error occurs.
    """
    try:
        student_id = int(student_id_str)
        course_id = int(course_id_str)
        
        student = next((s for s in students if s.id == student_id), None)
        course = next((c for c in courses if c.course_id == course_id), None)
        
        if student is None:
            raise ValueError(f"No student found with ID {student_id}")
        if course is None:
            raise ValueError(f"No course found with ID {course_id}")
        
        student.register_courses(course)
        course.add_student(student)
        QMessageBox.information(window, "Success", f"Student {student_id} registered to course {course_id}")
    except ValueError as e:
        QMessageBox.warning(window, "Input Error", str(e))


def assign_instructor_to_course(iid, course_id):
    """
    Assigns an instructor to a course by their ID.
    
    Parameters:
    -----------
    iid : str
        The instructor ID as a string.
    
    course_id : str
        The course ID as a string.
    
    This function converts the instructor and course IDs to integers, finds
    the respective objects in `instructors` and `courses`, and assigns the
    instructor to the course.

    Raises:
    -------
    ValueError : If no instructor or course is found with the provided ID.

    GUI Messages:
    -------------
    - A success message when the instructor is assigned.
    - A warning message if an error occurs.
    """
    try:
        instrcutor_id = int(iid)
        course_id = int(course_id)
        
        instructor = next((s for s in instructors if s.instructor_id == instrcutor_id), None)
        course = next((c for c in courses if c.course_id == course_id), None)
        
        if instructor is None:
            raise ValueError(f"No instructor found with ID {instrcutor_id}")
        if course is None:
            raise ValueError(f"No course found with ID {course_id}")
        
        course.assign_instructor(instructor)
        QMessageBox.information(window, "Success", f"Instructor {instrcutor_id} assigned to course {course_id}")
    except ValueError as e:
        QMessageBox.warning(window, "Input Error", str(e))


def setup_students_table(table):
    """
    Sets up the students table with name, age, email, registered courses, and action buttons.
    
    Parameters:
    -----------
    table : QTableWidget
        The table widget where the student data will be displayed.
    
    The table displays columns for the student's name, age, email, and registered courses. 
    Two additional columns are created for "Edit" and "Delete" buttons.
    """
    table.setRowCount(len(students))
    table.setColumnCount(6)  # name, age, email, registered courses, edit, delete
    table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Registered Courses", "Edit", "Delete"])

    for row, student in enumerate(students):
        table.setItem(row, 0, QTableWidgetItem(student.name))
        table.setItem(row, 1, QTableWidgetItem(str(student.age)))
        table.setItem(row, 2, QTableWidgetItem(student._email))
        courses_str = ", ".join([course.course_name for course in student.registered_courses])
        table.setItem(row, 3, QTableWidgetItem(courses_str))


def setup_instructors_table(table):
    """
    Sets up the instructors table with name, age, email, assigned courses, and action buttons.
    
    Parameters:
    -----------
    table : QTableWidget
        The table widget where the instructor data will be displayed.
    
    The table displays columns for the instructor's name, age, email, and assigned courses.
    Two additional columns are created for "Edit" and "Delete" buttons.
    """
    table.setRowCount(len(instructors))
    table.setColumnCount(6)  # name, age, email, assigned courses, edit, delete
    table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Assigned Courses", "Edit", "Delete"])

    for row, instructor in enumerate(instructors):
        table.setItem(row, 0, QTableWidgetItem(instructor.name))
        table.setItem(row, 1, QTableWidgetItem(str(instructor.age)))
        table.setItem(row, 2, QTableWidgetItem(instructor._email))
        courses_str = ", ".join([course.course_name for course in instructor.assigned_courses])
        table.setItem(row, 3, QTableWidgetItem(courses_str))


def setup_courses_table(table):
    """
    Sets up the courses table with course ID, course name, instructor, enrolled students, and action buttons.
    
    Parameters:
    -----------
    table : QTableWidget
        The table widget where the course data will be displayed.
    
    The table displays columns for the course ID, course name, instructor, and enrolled students.
    Two additional columns are created for "Edit" and "Delete" buttons.
    """
    table.setRowCount(len(courses))
    table.setColumnCount(6)  # course_id, course_name, instructor, enrolled students, edit, delete
    table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor", "Enrolled Students", "Edit", "Delete"])

    for row, course in enumerate(courses):
        table.setItem(row, 0, QTableWidgetItem(str(course.course_id)))
        table.setItem(row, 1, QTableWidgetItem(course.course_name))
        instructor_str = course.instructor.name if course.instructor else "None"
        table.setItem(row, 2, QTableWidgetItem(instructor_str))
        students_str = ", ".join([student.name for student in course.enrolled_students])
        table.setItem(row, 3, QTableWidgetItem(students_str))


def set_table(students_table, instructors_table, courses_table):
    """
    Sets up the tables for students, instructors, and courses.
    
    Parameters:
    -----------
    students_table : QTableWidget
        The table widget for displaying student data.
    
    instructors_table : QTableWidget
        The table widget for displaying instructor data.
    
    courses_table : QTableWidget
        The table widget for displaying course data.
    
    This function calls the setup functions for students, instructors, and courses. It
    also adds "Edit" and "Delete" buttons to each table.
    """
    setup_students_table(students_table)
    setup_instructors_table(instructors_table)
    setup_courses_table(courses_table)
    setup_table_with_buttons(students_table, students)
    setup_table_with_buttons(instructors_table, instructors)
    setup_table_with_buttons(courses_table, courses)


def filter_records(search_term, students_table, instructors_table, courses_table):
    """
    Filters and displays records based on a search term.
    
    Parameters:
    -----------
    search_term : str
        The term to filter the records by.
    
    students_table : QTableWidget
        The table widget for displaying filtered student data.
    
    instructors_table : QTableWidget
        The table widget for displaying filtered instructor data.
    
    courses_table : QTableWidget
        The table widget for displaying filtered course data.
    
    This function filters students by name or ID, instructors by name or ID, 
    and courses by name or course ID. It clears the tables before displaying
    the filtered results.
    """
    # Clear the tables first
    students_table.clearContents()
    instructors_table.clearContents()
    courses_table.clearContents()

    # Filter Students by name or ID
    filtered_students = [student for student in students if search_term.lower() in student.name.lower() or search_term in str(student.id)]
    students_table.setRowCount(len(filtered_students))
    for row, student in enumerate(filtered_students):
        students_table.setItem(row, 0, QTableWidgetItem(student.name))
        students_table.setItem(row, 1, QTableWidgetItem(str(student.age)))
        students_table.setItem(row, 2, QTableWidgetItem(student._email))
        courses_str = ", ".join([course.course_name for course in student.registered_courses])
        students_table.setItem(row, 3, QTableWidgetItem(courses_str))

    # Filter Instructors by name or ID
    filtered_instructors = [instructor for instructor in instructors if search_term.lower() in instructor.name.lower() or search_term in str(instructor.instructor_id)]
    instructors_table.setRowCount(len(filtered_instructors))
    for row, instructor in enumerate(filtered_instructors):
        instructors_table.setItem(row, 0, QTableWidgetItem(instructor.name))
        instructors_table.setItem(row, 1, QTableWidgetItem(str(instructor.age)))
        instructors_table.setItem(row, 2, QTableWidgetItem(instructor._email))
        courses_str = ", ".join([course.course_name for course in instructor.assigned_courses])
        instructors_table.setItem(row, 3, QTableWidgetItem(courses_str))

    # Filter Courses by course name or ID
    filtered_courses = [course for course in courses if search_term.lower() in course.course_name.lower() or search_term in str(course.course_id)]
    courses_table.setRowCount(len(filtered_courses))
    for row, course in enumerate(filtered_courses):
        courses_table.setItem(row, 0, QTableWidgetItem(str(course.course_id)))
        courses_table.setItem(row, 1, QTableWidgetItem(course.course_name))
        instructor_str = course.instructor.name if course.instructor else "None"
        courses_table.setItem(row, 2, QTableWidgetItem(instructor_str))
        students_str = ", ".join([student.name for student in course.enrolled_students])
        courses_table.setItem(row, 3, QTableWidgetItem(students_str))


def setup_table_with_buttons(table, data_type):
    """
    Adds "Edit" and "Delete" buttons to the table for each row.
    
    Parameters:
    -----------
    table : QTableWidget
        The table widget where buttons will be added.
    
    data_type : list
        The list of data items (students, instructors, or courses) to display in the table.
    
    This function iterates over the data and adds an "Edit" and "Delete" button to each row.
    The buttons are connected to respective functions to handle editing and deleting records.
    """
    for row, data in enumerate(data_type):
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        # Add the buttons to the table
        table.setCellWidget(row, 4, edit_button)  # Column for Edit
        table.setCellWidget(row, 5, delete_button)  # Column for Delete

        # Connect the buttons to functions
        edit_button.clicked.connect(lambda ch, r=row: edit_record(r, data_type, table))
        delete_button.clicked.connect(lambda ch, r=row: delete_record(r, data_type, table))
def edit_record(row, data_type, table):
    '''
    Edits the values of the locally stored Students, Instrcutors and Courses.

    Parameters:
    --------------
    row: integer
        The index of the row to be edited

    data_type : list
        The list of data items (students, instructors, or courses) to choose in the table.

    table : QTableWidget
        The table widget where buttons to edit the rows will be added.

    This function takes the value to be edited through the row and object type, loops through the different attributes and parameters and asks the user to input new values.
    For each new value, it asks if the user wants to change it. Depending on their choice, it prompts the new value or goes on to the next.
    '''
    data = data_type[row]  # Get the object to be edited

    if isinstance(data, Student):
        # Edit student details
        new_name, ok = QInputDialog.getText(None, "Edit Student", "Enter new name:", text=data.name)
        if ok:
            data.name = new_name
            table.setItem(row, 0, QTableWidgetItem(new_name))

        new_age, ok = QInputDialog.getInt(None, "Edit Student", "Enter new age:", value=data.age)
        if ok:
            data.age = new_age
            table.setItem(row, 1, QTableWidgetItem(str(new_age)))

        new_email, ok = QInputDialog.getText(None, "Edit Student", "Enter new email:", text=data._email)
        if ok:
            if Person.validMail(new_email):  # Check if email is valid
                data.edit_email(new_email)
                table.setItem(row, 2, QTableWidgetItem(new_email))
            else:
                QMessageBox.warning(None, "Invalid Email", "Please enter a valid email.")

        new_id, ok = QInputDialog.getInt(None, "Edit Student", "Enter new student ID:", value=data.id)
        if ok:
            data.id = new_id
            table.setItem(row, 3, QTableWidgetItem(str(new_id)))

    elif isinstance(data, Instructor):
        # Edit instructor details
        new_name, ok = QInputDialog.getText(None, "Edit Instructor", "Enter new name:", text=data.name)
        if ok:
            data.name = new_name
            table.setItem(row, 0, QTableWidgetItem(new_name))

        new_age, ok = QInputDialog.getInt(None, "Edit Instructor", "Enter new age:", value=data.age)
        if ok:
            data.age = new_age
            table.setItem(row, 1, QTableWidgetItem(str(new_age)))

        new_email, ok = QInputDialog.getText(None, "Edit Instructor", "Enter new email:", text=data._email)
        if ok:
            if Person.validMail(new_email):  # Check if email is valid
                data.edit_email(new_email)
                table.setItem(row, 2, QTableWidgetItem(new_email))
            else:
                QMessageBox.warning(None, "Invalid Email", "Please enter a valid email.")

        new_iid, ok = QInputDialog.getInt(None, "Edit Instructor", "Enter new instructor ID:", value=data.instructor_id)
        if ok:
            data.instructor_id = new_iid
            table.setItem(row, 3, QTableWidgetItem(str(new_iid)))

    elif isinstance(data, Course):
        # Edit course details
        new_course_name, ok = QInputDialog.getText(None, "Edit Course", "Enter new course name:", text=data.course_name)
        if ok:
            data.course_name = new_course_name
            table.setItem(row, 0, QTableWidgetItem(new_course_name))

        new_course_id, ok = QInputDialog.getInt(None, "Edit Course", "Enter new course ID:", value=data.course_id)
        if ok:
            data.course_id = new_course_id
            table.setItem(row, 1, QTableWidgetItem(str(new_course_id)))

        # Since instructor may not always be assigned, check if they want to change the instructor
        if data.instructor:
            new_instructor, ok = QInputDialog.getText(None, "Edit Instructor", "Enter new instructor name:", text=data.instructor.name)
            if ok:
                data.instructor.name = new_instructor
                table.setItem(row, 2, QTableWidgetItem(new_instructor))
        else:
            assign_instructor = QMessageBox.question(None, "Assign Instructor", "Do you want to assign an instructor?",
                                                     QMessageBox.Yes | QMessageBox.No)
            if assign_instructor == QMessageBox.Yes:
                instructor_id, ok = QInputDialog.getText(None, "Assign Instructor", "Enter instructor id:")
                if ok:
                    instructor = next((s for s in students if s.instructor_id == instructor_id), None)
                    if instructor:
                        table.setItem(row, 2, QTableWidgetItem(instructor.name))
                    else:
                        QMessageBox.warning(None, "Invalid Instructor", "Please enter a valid instructor ID.")

def delete_record(row, data_type, table):
    """
    Delete a record from the specified data type and table after confirmation.

    This function displays a confirmation dialog to the user. If the user confirms,
    the specified record is removed from the data type list and the table.

    :param row: The index of the record to delete.
    :param data_type: The list of data records (e.g., students, instructors, courses).
    :param table: The table widget from which the row should be removed.

    """
    reply = QMessageBox.question(None, "Delete", "Are you sure you want to delete this record?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        data_type.pop(row)
        table.removeRow(row)

def load_from_json():
    """
    Load data from a JSON file into the global lists of students, instructors, and courses.

    Prompts the user for a filename, reads the JSON file, and populates the global 
    lists with the data. Handles FileNotFoundError and JSONDecodeError exceptions.

    The expected structure of the JSON file is:

    {
        "students": [...],
        "instructors": [...],
        "courses": [...],
    }

    :raises FileNotFoundError: If the specified file cannot be found.
    :raises json.JSONDecodeError: If the file is not a valid JSON.
    """
    global students, instructors, courses
    name, ok = QInputDialog.getText(None, "Input", "Enter file name")
    if ok:
        try:
            filename = name + '.json'
            with open(filename, 'r') as file:
                data = json.load(file)
                students = [Student(**s) for s in data.get('students', [])]
                instructors = [Instructor(**i) for i in data.get('instructors', [])]
                courses = [Course(**c) for c in data.get('courses', [])]
            print(f"Data loaded from {filename}.")
        except FileNotFoundError:
            print(f"{filename} not found. Loading skipped.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {filename}. Loading skipped.")

def save_to_json():
    """
    Save the current lists of students, instructors, and courses to a JSON file.

    Prompts the user for a filename and writes the current state of the data
    to a JSON file. The saved data structure includes lists of students, 
    instructors, and courses.

    :raises Exception: Raises an exception if there's an error writing the file.
    """
    name, ok = QInputDialog.getText(None, "Input", "Enter file name")
    if ok:
        filename = name + '.json'
        data = {
            'students': [student.__dict__ for student in students],
            'instructors': [instructor.__dict__ for instructor in instructors],
            'courses': [course.__dict__ for course in courses]
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}.")

def export_to_csv():
    """
    Export the current lists of students, instructors, and courses to CSV files.

    Prompts the user for filenames for each data type and writes the current state
    to separate CSV files. The exported files will include details such as names, 
    email addresses, and registered courses for students, and similarly for instructors
    and courses.

    :raises Exception: Raises an exception if there's an error writing the files.
    """
    s_name, s_ok = QInputDialog.getText(None, "Student Input", "Enter file name for students")
    if s_ok:
        with open(s_name + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Age', 'Email', 'ID', 'Registered Courses'])
            for student in students:
                courses = ", ".join([course.course_name for course in student.registered_courses])
                writer.writerow([student.name, student.age, student._email, student.id, courses])

    i_name, i_ok = QInputDialog.getText(None, "Instructor Input", "Enter file name for instructors")
    if i_ok:
        with open(i_name + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Age', 'Email', 'Instructor ID', 'Assigned Courses'])
            for instructor in instructors:
                courses = ", ".join([course.course_name for course in instructor.assigned_courses])
                writer.writerow([instructor.name, instructor.age, instructor._email, instructor.instructor_id, courses])

    c_name, c_ok = QInputDialog.getText(None, "Course Input", "Enter file name for courses")
    if c_ok:
        with open(c_name + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Course ID', 'Course Name', 'Instructor', 'Enrolled Students'])
            for course in courses:
                students_list = ", ".join([student.name for student in course.enrolled_students])
                instructor_name = course.instructor.name if course.instructor else "None"
                writer.writerow([course.course_id, course.course_name, instructor_name, students_list])


def main():
    global window, student_name, student_age, student_email, student_id_field
    global instructor_name, instructor_age, instructor_email, instructor_id_field
    global course_id_field, course_name_field, instructor_name_for_course
    global course_dropdown, course_dropdown_i

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("School Management System")
    window.setGeometry(100, 100, 500, 400)

    main_layout = QVBoxLayout()

    # Student form
    student_form = QFormLayout()
    student_name = QLineEdit()
    student_age = QLineEdit()
    student_email = QLineEdit()
    student_id_field = QLineEdit()
    student_form.addRow(QLabel("Name:"), student_name)
    student_form.addRow(QLabel("Age:"), student_age)
    student_form.addRow(QLabel("Email:"), student_email)
    student_form.addRow(QLabel("Student ID:"), student_id_field)
    add_student_button = QPushButton("Add Student")
    add_student_button.clicked.connect(add_student)
    student_form.addWidget(add_student_button)
    main_layout.addLayout(student_form)

    # Instructor form
    instructor_form = QFormLayout()
    instructor_name = QLineEdit()
    instructor_age = QLineEdit()
    instructor_email = QLineEdit()
    instructor_id_field = QLineEdit()
    instructor_form.addRow(QLabel("Name:"), instructor_name)
    instructor_form.addRow(QLabel("Age:"), instructor_age)
    instructor_form.addRow(QLabel("Email:"), instructor_email)
    instructor_form.addRow(QLabel("Instructor ID:"), instructor_id_field)
    add_instructor_button = QPushButton("Add Instructor")
    add_instructor_button.clicked.connect(add_instructor)
    instructor_form.addWidget(add_instructor_button)
    main_layout.addLayout(instructor_form)

    # Course form
    course_form = QFormLayout()
    course_id_field = QLineEdit()
    course_name_field = QLineEdit()
    instructor_name_for_course = QLineEdit()
    course_form.addRow(QLabel("Course ID:"), course_id_field)
    course_form.addRow(QLabel("Course Name:"), course_name_field)
    course_form.addRow(QLabel("Instructor Name:"), instructor_name_for_course)
    add_course_button = QPushButton("Add Course")
    add_course_button.clicked.connect(add_course)
    course_form.addWidget(add_course_button)
    main_layout.addLayout(course_form)

    course_id_label = QLabel("Select Course:", window)
    main_layout.addWidget(course_id_label)
    
    course_dropdown = QComboBox(window)
    
    course_dropdown.addItem("Select Course")
    main_layout.addWidget(course_dropdown)

    # Student ID input box
    student_id_label = QLabel("Enter Student ID:", window)
    main_layout.addWidget(student_id_label)
    student_id_input = QLineEdit(window)
    main_layout.addWidget(student_id_input)
    # Register button
    register_button = QPushButton("Register Student to Course", window)
    main_layout.addWidget(register_button)
    # Connect button to function
    register_button.clicked.connect(lambda: register_student_to_course(student_id_input.text(), course_dropdown.currentData()))
    

    course_id_label_i = QLabel("Select Course:", window)
    main_layout.addWidget(course_id_label_i)
    course_dropdown_i = QComboBox(window)
    
    course_dropdown_i.addItem("Select Course")
    main_layout.addWidget(course_dropdown_i)
    # instrcutor input box
    instructor_id_label = QLabel("Enter Instructor ID:", window)
    main_layout.addWidget(instructor_id_label)
    instrcutor_id_input = QLineEdit(window)
    main_layout.addWidget(instrcutor_id_input)
    # Register button
    register_button_i = QPushButton("Assign instructor to Course", window)
    main_layout.addWidget(register_button_i)
    # Connect button to function
    register_button_i.clicked.connect(lambda: assign_instructor_to_course(instrcutor_id_input.text(), course_dropdown_i.currentData()))
    
    search_label = QLabel("Search by Name, ID, or Course:")
    main_layout.addWidget(search_label)

    search_input = QLineEdit()
    main_layout.addWidget(search_input)

    search_button = QPushButton("Search")
    main_layout.addWidget(search_button)

    students_table = QTableWidget()
    instructors_table = QTableWidget()
    courses_table = QTableWidget()
    # Populate the tables
    set_table(students_table,instructors_table,courses_table)
    # Add the tables to the layout
    main_layout.addWidget(QLabel("Students:"))
    main_layout.addWidget(students_table)

    main_layout.addWidget(QLabel("Instructors:"))
    main_layout.addWidget(instructors_table)

    main_layout.addWidget(QLabel("Courses:"))
    main_layout.addWidget(courses_table)

    refresh_table_button = QPushButton("Refresh Table", window)
    main_layout.addWidget(refresh_table_button)
    refresh_table_button.clicked.connect(lambda: set_table(students_table,instructors_table,courses_table))

    search_button.clicked.connect(lambda: filter_records(search_input.text(), students_table, instructors_table, courses_table))
    setup_table_with_buttons(students_table,students)
    setup_table_with_buttons(instructors_table,instructors)
    setup_table_with_buttons(courses_table,courses)


    save_button = QPushButton("Save")
    load_button = QPushButton("Load")
    export_button = QPushButton("Export to CSV")

    save_button.clicked.connect(save_to_json)
    load_button.clicked.connect(load_from_json)
    export_button.clicked.connect(export_to_csv)

    main_layout.addWidget(save_button)
    main_layout.addWidget(load_button)
    main_layout.addWidget(export_button)
    container_widget = QWidget()
    container_widget.setLayout(main_layout)

    # Create a QScrollArea and set the container_widget as its content
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)  # Makes sure content resizes with the scroll area
    scroll_area.setWidget(container_widget)  # Set the main widget


    # Set the scroll area as the central widget of the main window
    window.setCentralWidget(scroll_area)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
