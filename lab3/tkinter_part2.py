import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from OOP.course import Course
from OOP.instructor import Instructor
from OOP.student import Student
import re

class SchoolManagementApp:
    '''
    The SchoolManagementApp class creates a GUI for managing students, instructors, and courses.

    :param root: The root window for the application.
    :type root: tkinter.Tk
    '''
    
    def __init__(self, root):
        '''
        Initializes the SchoolManagementApp with a main window and sets up frames for navigation.

        :param root: The root window for the application.
        :type root: tkinter.Tk
        '''
        self.root = root
        self.root.title("School Management System")
        self.root.state('zoomed')

        # Frame setup
        self.main_menu_frame = tk.Frame(self.root)
        self.student_frame = tk.Frame(self.root)
        self.instructor_frame = tk.Frame(self.root)
        self.course_frame = tk.Frame(self.root)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="bottom", pady=10)
        self.display_frame = tk.Frame(self.root)

        # Main menu UI components
        tk.Label(self.main_menu_frame, text="School Management System", font=("Arial", 20, "bold")).pack(pady=20)
        self.student_button = tk.Button(self.main_menu_frame, text="Add Student", command=self.show_student_form)
        self.student_button.pack(pady=5)
        self.instructor_button = tk.Button(self.main_menu_frame, text="Add Instructor", command=self.show_instructor_form)
        self.instructor_button.pack(pady=5)
        self.course_button = tk.Button(self.main_menu_frame, text="Add Course", command=self.show_course_form)
        self.course_button.pack(pady=5)
        self.register_button = tk.Button(self.main_menu_frame, text="Register for Course", command=self.show_register_course_form)
        self.register_button.pack(pady=5)
        self.assign_instructor_button = tk.Button(self.main_menu_frame, text="Assign Instructor", command=self.show_assign_instructor_form)
        self.assign_instructor_button.pack(pady=5)
        self.display_students_button = tk.Button(self.main_menu_frame, text="View All Students", command=self.display_all_students)
        self.display_students_button.pack(pady=5)
        self.display_instructors_button = tk.Button(self.main_menu_frame, text="View All Instructors", command=self.display_all_instructors)
        self.display_instructors_button.pack(pady=5)
        self.display_courses_button = tk.Button(self.main_menu_frame, text="View All Courses", command=self.display_all_courses)
        self.display_courses_button.pack(pady=5)
        self.search_button = tk.Button(self.main_menu_frame, text="Search", command=self.show_search_form)
        self.search_button.pack(pady=5)
        self.main_menu_frame.pack(fill="both", expand=True)

        # Create forms
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()
        self.create_register_course_form()
        self.create_assign_instructor_form()
        self.create_search_form()

    def create_student_form(self):
        '''Creates the UI for adding a new student.'''
        tk.Label(self.student_frame, text="Add Student", font=("Arial", 16)).pack(pady=10)

        self.student_name_var = tk.StringVar()
        self.student_age_var = tk.IntVar()
        self.student_email_var = tk.StringVar()
        self.student_id_var = tk.StringVar()

        tk.Label(self.student_frame, text="Name").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_name_var).pack()

        tk.Label(self.student_frame, text="Age").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_age_var).pack()

        tk.Label(self.student_frame, text="Email").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_email_var).pack()

        tk.Label(self.student_frame, text="Student ID").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_id_var).pack()

        tk.Button(self.student_frame, text="Add", command=self.add_student).pack(pady=10)
        tk.Button(self.student_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def create_instructor_form(self):
        '''Creates the UI for adding a new instructor.'''
        tk.Label(self.instructor_frame, text="Add Instructor", font=("Arial", 16)).pack(pady=10)

        self.instructor_name_var = tk.StringVar()
        self.instructor_age_var = tk.IntVar()
        self.instructor_email_var = tk.StringVar()
        self.instructor_id_var = tk.StringVar()

        tk.Label(self.instructor_frame, text="Name").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_name_var).pack()

        tk.Label(self.instructor_frame, text="Age").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_age_var).pack()

        tk.Label(self.instructor_frame, text="Email").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_email_var).pack()

        tk.Label(self.instructor_frame, text="Instructor ID").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_id_var).pack()

        tk.Button(self.instructor_frame, text="Add", command=self.add_instructor).pack(pady=10)
        tk.Button(self.instructor_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def create_course_form(self):
        '''Creates the UI for adding a new course.'''
        tk.Label(self.course_frame, text="Add Course", font=("Arial", 16)).pack(pady=10)

        self.course_id_var = tk.StringVar()
        self.course_name_var = tk.StringVar()

        tk.Label(self.course_frame, text="Course ID").pack(pady=5)
        tk.Entry(self.course_frame, textvariable=self.course_id_var).pack()

        tk.Label(self.course_frame, text="Course Name").pack(pady=5)
        tk.Entry(self.course_frame, textvariable=self.course_name_var).pack()

        tk.Button(self.course_frame, text="Add", command=self.add_course).pack(pady=10)
        tk.Button(self.course_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def create_register_course_form(self):
        '''Creates the UI for registering a student for a course.'''
        self.register_course_frame = tk.Frame(self.root)

        tk.Label(self.register_course_frame, text="Register for Course", font=("Arial", 16)).pack(pady=10)

        self.register_student_id_var = tk.StringVar()
        self.selected_course_var = tk.StringVar()

        tk.Label(self.register_course_frame, text="Student ID").pack(pady=5)
        tk.Entry(self.register_course_frame, textvariable=self.register_student_id_var).pack()

        tk.Label(self.register_course_frame, text="Select Course").pack(pady=5)

        courses = Course.load_all_courses('Data/courses.json')

        if courses:
            self.selected_course_var.set(courses[0])
            self.course_dropdown = tk.OptionMenu(self.register_course_frame, self.selected_course_var, *courses)
        else:
            self.selected_course_var.set("No available courses")
            self.course_dropdown = tk.OptionMenu(self.register_course_frame, self.selected_course_var, "No available courses")

        self.course_dropdown.pack()

        tk.Button(self.register_course_frame, text="Register", command=self.register_student_for_course).pack(pady=10)
        tk.Button(self.register_course_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def create_assign_instructor_form(self):
        '''Creates the UI for assigning an instructor to a course.'''
        self.assign_instructor_frame = tk.Frame(self.root)

        tk.Label(self.assign_instructor_frame, text="Assign Instructor to Course", font=("Arial", 16)).pack(pady=10)

        self.assign_instructor_id_var = tk.StringVar()
        self.assign_course_var = tk.StringVar()

        tk.Label(self.assign_instructor_frame, text="Instructor ID").pack(pady=5)
        tk.Entry(self.assign_instructor_frame, textvariable=self.assign_instructor_id_var).pack()

        tk.Label(self.assign_instructor_frame, text="Select Course").pack(pady=5)

        courses = Course.load_all_courses('Data/courses.json')
        if courses:
            self.assign_course_var.set(courses[0]) 
            self.assign_course_dropdown = tk.OptionMenu(self.assign_instructor_frame, self.assign_course_var, *courses)
        else:
            self.assign_course_var.set("No available courses")
            self.assign_course_dropdown = tk.OptionMenu(self.assign_instructor_frame, self.assign_course_var, "No available courses")

        self.assign_course_dropdown.pack()

        tk.Button(self.assign_instructor_frame, text="Assign", command=self.assign_instructor_to_course).pack(pady=10)
        tk.Button(self.assign_instructor_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def create_display_treeview(self, headers, data, category):
        '''Creates a Treeview for displaying records.

        :param headers: The column headers for the Treeview.
        :type headers: list
        :param data: The data to display in the Treeview.
        :type data: list of tuples
        :param category: The category of records being displayed.
        :type category: str
        '''
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.display_frame, columns=headers, show='headings')

        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=100)

        for row in data:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(fill="both", expand=True)

        self.save_edit_button = tk.Button(self.display_frame, text="Edit", command=lambda: self.save_edit(category))
        self.save_edit_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.delete_button = tk.Button(self.display_frame, text="Delete", command=lambda: self.delete_record(category))
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(self.display_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5, pady=10)

        self.hide_all_frames()
        self.display_frame.pack(fill="both", expand=True)

    def create_search_form(self):
        '''Creates the UI for searching records.'''
        self.search_frame = tk.Frame(self.root)

        tk.Label(self.search_frame, text="Search", font=("Arial", 16)).pack(pady=10)

        self.search_by_var = tk.StringVar(value="ID")
        tk.Label(self.search_frame, text="Search By").pack(pady=5)
        search_by_dropdown = ttk.Combobox(self.search_frame, textvariable=self.search_by_var, values=["ID", "Name"])
        search_by_dropdown.pack()

        self.search_in_var = tk.StringVar(value="Student")
        tk.Label(self.search_frame, text="Search In").pack(pady=5)
        search_in_dropdown = ttk.Combobox(self.search_frame, textvariable=self.search_in_var, values=["Student", "Instructor", "Course"])
        search_in_dropdown.pack()

        self.search_value_var = tk.StringVar()
        tk.Label(self.search_frame, text="Enter value").pack(pady=5)
        tk.Entry(self.search_frame, textvariable=self.search_value_var).pack()

        tk.Button(self.search_frame, text="Search", command=self.perform_search).pack(pady=10)
        tk.Button(self.search_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def add_student(self):
        '''Adds a new student to the system.

        Retrieves student data from the form and saves it to a file.

        :raises: ValueError: If any field is empty.
        '''
        name = self.student_name_var.get()
        age = self.student_age_var.get()
        email = self.student_email_var.get()
        student_id = self.student_id_var.get()

        if name and age and email and student_id:
            try:
                student = Student(name, age, email, student_id, [])
                student.save_to_file('Data/students.json')
                messagebox.showinfo("Success", "Student added successfully")
                self.clear_student_fields()
                self.show_main_menu() 
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "All fields must be filled")

    def add_instructor(self):
        '''Adds a new instructor to the system.

        Retrieves instructor data from the form and saves it to a file.

        :raises: ValueError: If any field is empty.
        '''
        name = self.instructor_name_var.get()
        age = self.instructor_age_var.get()
        email = self.instructor_email_var.get()
        instructor_id = self.instructor_id_var.get()

        if name and age and email and instructor_id:
            try:
                instructor = Instructor(name, age, email, instructor_id, [])
                instructor.save_to_file('Data/instructors.json')
                messagebox.showinfo("Success", "Instructor added successfully")
                self.clear_instructor_fields()
                self.show_main_menu()  
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "All fields must be filled")

    def add_course(self):
        '''Adds a new course to the system.

        Retrieves course data from the form and saves it to a file.

        :raises: ValueError: If any field is empty.
        '''
        course_id = self.course_id_var.get()
        course_name = self.course_name_var.get()

        if course_id and course_name:
            try:
                course = Course(course_id, course_name, None, [])
                course.save_to_file('Data/courses.json')
                messagebox.showinfo("Success", "Course added successfully")
                self.clear_course_fields()
                self.show_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "All fields must be filled")

    
    def hide_all_frames(self):
        '''
        Hides all frames in the application.

        This method ensures that only one frame is visible at a time by packing
        all frames with `pack_forget()`.
        '''
        self.main_menu_frame.pack_forget()  
        self.student_frame.pack_forget()    
        self.instructor_frame.pack_forget() 
        self.course_frame.pack_forget()    
        self.register_course_frame.pack_forget()  
        self.assign_instructor_frame.pack_forget() 
        self.display_frame.pack_forget()
        self.search_frame.pack_forget()

    def show_student_form(self):
        '''
        Displays the student form for adding a new student.

        This method hides all other frames and displays the student form.
        '''
        self.hide_all_frames()
        self.student_frame.pack(fill="both", expand=True)

    def show_instructor_form(self):
        '''Displays the instructor form for adding a new instructor.

        This method hides all other frames and displays the instructor form.
        '''        
        self.hide_all_frames()
        self.instructor_frame.pack(fill="both", expand=True)

    def show_course_form(self):
        '''Displays the course form for adding a new course.

        This method hides all other frames and displays the course form.
        '''
        self.hide_all_frames()
        self.course_frame.pack(fill="both", expand=True)
    
    def show_search_form(self):
        '''Displays the search form for querying records.

        This method hides all other frames and displays the search form.
        '''
        self.hide_all_frames()
        self.search_frame.pack(fill="both", expand=True)
    
    def show_register_course_form(self):
        '''Displays the form for registering a student in a course.

        This method hides all other frames, creates the registration form, and displays it.
        '''
        self.hide_all_frames()
        self.create_register_course_form()
        self.register_course_frame.pack(fill="both", expand=True)

    def show_assign_instructor_form(self):
        '''Displays the form for assigning an instructor to a course.

        This method hides all other frames, creates the assignment form, and displays it.
        '''
        self.hide_all_frames()
        self.create_assign_instructor_form()
        self.assign_instructor_frame.pack(fill="both", expand=True)

    def show_main_menu(self):
        '''Displays the main menu of the application.

        This method hides all other frames and displays the main menu.
        '''
        self.hide_all_frames()
        self.main_menu_frame.pack(fill="both", expand=True)

    def clear_student_fields(self):
        '''Clears the input fields in the student form.

        Resets the student-related fields to their default values.
        '''
        self.student_name_var.set("")
        self.student_age_var.set(0)
        self.student_email_var.set("")
        self.student_id_var.set("")
    
    def clear_instructor_fields(self):
        '''Clears the input fields in the instructor form.

        Resets the instructor-related fields to their default values.
        '''
        self.instructor_name_var.set("")
        self.instructor_age_var.set(0)
        self.instructor_email_var.set("")
        self.instructor_id_var.set("")
    
    def clear_course_fields(self):
        '''Clears the input fields in the course form.

        Resets the course-related fields to their default values.
        '''
        self.course_id_var.set("")
        self.course_name_var.set("")

    def register_student_for_course(self):
        '''Registers a student for a specific course.

        Retrieves the student ID and selected course ID from the input fields,
        and updates the student's record accordingly.

        :raises: ValueError: If any input field is empty.
        '''
        student_id = self.register_student_id_var.get()
        selected_course_id = self.selected_course_var.get()

        if student_id and selected_course_id:
            try:
                student = Student.get_student_by_id('Data/students.json', student_id)
                course = Course.load_course_by_id('Data/courses.json', selected_course_id)
                if student and course:
                    student.register_course(course)
                    messagebox.showinfo("Success", "Student registered for the course successfully")
                    self.register_student_id_var.set("")
                    self.selected_course_var.set("")
                    self.show_main_menu()
                else:
                    messagebox.showerror("Error", "Student or Course not found")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please fill in all fields")

    def assign_instructor_to_course(self):
        '''Assigns an instructor to a specific course.

        Retrieves the instructor ID and selected course ID from the input fields,
        and updates the instructor's record accordingly.

        :raises: ValueError: If any input field is empty.
        '''
        instructor_id = self.assign_instructor_id_var.get()
        selected_course_id = self.assign_course_var.get()

        if instructor_id and selected_course_id:
            try:
                instructor = Instructor.load_instructor_by_id('Data/instructors.json', instructor_id)
                course = Course.load_course_by_id('Data/courses.json', selected_course_id)
                if instructor and course:
                    instructor.assign_course(course)
                    messagebox.showinfo("Success", f"Instructor {instructor.name} assigned to course {course.course_name} successfully")
                    self.assign_instructor_id_var.set("") 
                    self.assign_course_var.set("") 
                    self.show_main_menu()
                else:
                    messagebox.showerror("Error", "Instructor or Course not found")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please fill in all fields")

    def display_all_students(self):
        '''Displays all students in the system.

        Loads student data from a file and creates a tree view to display it.
        '''
        students = Student.load_all_students('Data/students.json')
        headers = ["Name", "Age", "Email", "Student ID", "Registered Courses"]
        data = [(s.name, s.age, s.get_email(), s.student_id, ', '.join(s.registered_courses)) for s in students]
        self.create_display_treeview(headers, data,"student")

    def display_all_instructors(self):
        '''Displays all instructors in the system.

        Loads instructor data from a file and creates a tree view to display it.
        '''
        instructors = Instructor.load_all_instructors('Data/instructors.json')
        headers = ["Name", "Age", "Email", "Instructor ID", "Courses Taught"]
        data = [(i.name, i.age, i.get_email(), i.instructor_id, ', '.join(i.assigned_courses)) for i in instructors]
        self.create_display_treeview(headers, data,"instructor")

    def display_all_courses(self):
        '''Displays all courses in the system.

        Loads course data from a file and creates a tree view to display it.
        '''
        courses = Course.load_all_courses_fully('Data/courses.json')
        headers = ["Course ID", "Course Name", "Instructor", "Enrolled Students"]
        data = [(c.course_id, c.course_name, c.instructor.name if c.instructor else 'None', ', '.join(c.enrolled_students)) for c in courses]
        self.create_display_treeview(headers, data,"course")
    
    def perform_search(self):
        '''Performs a search for students, instructors, or courses based on user input.

        Searches records according to the specified criteria and displays the results.

        :raises: Warning if no search value is provided.
        '''
        search_by = self.search_by_var.get()
        search_in = self.search_in_var.get()
        search_value = self.search_value_var.get()

        if not search_value:
            messagebox.showwarning("Warning", "Please enter a search value.")
            return

        if search_in == "Student":
            students = Student.load_all_students('Data/students.json')
            if search_by == "ID":
                results = [s for s in students if s.student_id == search_value]
            else:
                results = [s for s in students if s.name == search_value]

            if results:
                headers = ["Name", "Age", "Email", "Student ID", "Registered Courses"]
                data = [(s.name, s.age, s.get_email(), s.student_id, ', '.join(s.registered_courses)) for s in results]
                self.create_display_treeview(headers, data,"student")
            else:
                messagebox.showinfo("No Results", "No student found.")

        elif search_in == "Instructor":
            instructors = Instructor.load_all_instructors('Data/instructors.json')
            if search_by == "ID":
                results = [i for i in instructors if i.instructor_id == search_value]
            else: 
                results = [i for i in instructors if i.name == search_value]

            if results:
                headers = ["Name", "Age", "Email", "Instructor ID", "Courses Taught"]
                data = [(i.name, i.age, i.get_email(), i.instructor_id, ', '.join(i.assigned_courses)) for i in results]
                self.create_display_treeview(headers, data,"instructor")
            else:
                messagebox.showinfo("No Results", "No instructor found.")

        elif search_in == "Course":
            courses = Course.load_all_courses_fully('Data/courses.json')
            if search_by == "ID":
                results = [c for c in courses if c.course_id == search_value]
            else:
                results = [c for c in courses if c.course_name == search_value]

            if results:
                headers = ["Course ID", "Course Name", "Instructor", "Enrolled Students"]
                data = [(c.course_id, c.course_name, c.instructor.name if c.instructor else 'None', ', '.join(c.enrolled_students)) for c in results]
                self.create_display_treeview(headers, data,"course")
            else:
                messagebox.showinfo("No Results", "No course found.")

    def delete_record(self, category):
        '''Deletes a selected record based on the specified category.

        Prompts the user for confirmation before deletion.

        :param category: The type of record to delete ('student', 'instructor', or 'course').
        '''
        if not hasattr(self, 'tree'):
            messagebox.showerror("Error", "No records are currently being displayed.")
            return

        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", f"No {category} selected for deletion.")
            return

        selected_id = self.tree.item(selected_item)['values'][3]
        if (category == "course"):
            selected_id = self.tree.item(selected_item)['values'][0]
        print(selected_id)
        record = None
        if category == "student":
            record = Student.get_student_by_id('Data/students.json', str(selected_id))
        elif category == "instructor":
            record = Instructor.load_instructor_by_id('Data/instructors.json', str(selected_id))
        elif category == "course":
            record = Course.load_course_by_id('Data/courses.json', str(selected_id))
        else:
            messagebox.showerror("Error", "Unknown category")
            return

        if record:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {category}?"):
                try:
                    if category == "student":
                        record.delete_from_file('Data/students.json')
                    elif category == "instructor":
                        record.delete_from_file('Data/instructors.json')
                    elif category == "course":
                        record.delete_from_file('Data/courses.json')

                    messagebox.showinfo("Success", f"{category.capitalize()} record deleted successfully")
                    if (category == "student"):
                        self.display_all_students()
                    elif (category=="instructor"):
                        self.display_all_instructors()
                    elif (category=="course"):
                            self.display_all_courses()
                    
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", f"{category.capitalize()} not found")

    def save_edit(self, category):
        '''Initiates the editing process for a selected record.

        Displays input fields pre-filled with the selected record's data for editing.

        :param category: The type of record to edit ('student', 'instructor', or 'course').
        '''
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", f"No {category} selected for editing.")
            return

        selected_data = self.tree.item(selected_item)['values']

        for widget in self.display_frame.winfo_children():
            widget.destroy()

        self.entry_fields = []
        labels = []

        if category == "student":
            fields_to_edit = ["Name", "Age", "Email"]
            indices = [0, 1, 2]
        elif category == "instructor":
            fields_to_edit = ["Name", "Age", "Email"]
            indices = [0, 1, 2]
        elif category == "course":
            fields_to_edit = ["Course Name"]
            indices = [1]
        else:
            messagebox.showerror("Error", "Unknown category for editing.")
            return

        for idx, field in zip(indices, fields_to_edit):
            label = tk.Label(self.display_frame, text=field)
            label.pack()
            labels.append(label)

            entry = tk.Entry(self.display_frame)
            entry.insert(0, selected_data[idx])
            entry.pack(padx=5, pady=5)
            self.entry_fields.append(entry)

        save_button = tk.Button(self.display_frame, text="Save Changes", command=lambda: self.save_changes(category, selected_data))
        save_button.pack(padx=5, pady=5)

        tk.Button(self.display_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5, pady=10)

    def save_changes(self, category, original_data):
        '''Saves changes made to a selected record.

        Updates the record in the appropriate file and refreshes the display.

        :param category: The type of record being edited ('student', 'instructor', or 'course').
        :param original_data: The original data of the record before editing.
        '''
        updated_data = [entry.get() for entry in self.entry_fields]
        try:
            if category == "student":
                print(original_data[3])
                student = Student.get_student_by_id('Data/students.json', str(original_data[3])) 
                if student:
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    student.name = name
                    age = int(updated_data[1])
                    assert (age >= 0), "Age cannot be negative"
                    student.age = age
                    email = updated_data[2]
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    assert(re.match(regex, email) is not None), "Wrong email format"
                    student._email = email
                    student.update_file('Data/students.json') 
            elif category == "instructor":
                instructor = Instructor.load_instructor_by_id('Data/instructors.json', str(original_data[3]))
                if instructor:
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    instructor.name = name
                    age = int(updated_data[1])
                    assert (age >= 0), "Age cannot be negative"
                    instructor.age = age
                    email = updated_data[2]
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    assert(re.match(regex, email) is not None), "Wrong email format"
                    instructor._email = email
                    instructor.update('Data/instructors.json')
            elif category == "course":
                course = Course.load_course_by_id('Data/courses.json', str(original_data[0]))
                if course:
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    course.course_name = name
                    course.update('Data/courses.json')
        except Exception as e:
             messagebox.showerror("Error "+str(e))
             return

        if category == "student":
            self.display_all_students()
        elif category == "instructor":
            self.display_all_instructors()
        elif category == "course":
            self.display_all_courses()

        messagebox.showinfo("Success", f"{category.capitalize()} updated successfully!")


root = tk.Tk()
app = SchoolManagementApp(root)
root.mainloop()