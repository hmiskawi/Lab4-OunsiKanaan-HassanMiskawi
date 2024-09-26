import json
import csv

class Person:
    """
    A class to represent a person.

    Attributes
    ----------
    name : str
        The name of the person.
    age : int
        The age of the person.
    _email : str
        The email address of the person.
    
    Methods
    -------
    introduce():
        Prints the person's details (name, age, email).
    edit_email(new_email: str):
        Updates the email address.
    validMail(email: str) -> bool:
        Checks and validate the email format.
    to_json() -> dict:
        Converts the person object to a dictionary for json files.
    from_json(data: dict) -> Person:
        Creates a person object from a dictionary or from json files.
    """
    
    def __init__(self, name, age, email):
        """
        Constructs all the necessary attributes for the person object.

        :param name: The name of the person.
        :type name: str
        :param age: The age of the person.
        :type age: int
        :param email: The email address of the person.
        :type email: str
        :raises ValueError: If the email is not valid.
        :raises AssertionError: If the name is not a string or age is not an integer.
        """
        assert type(name) == str, "Name type invalid"
        assert type(age) == int, "Age should be a number"
        if not self.validMail(email):
            raise ValueError("Please enter a valid mail")
        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        Prints the details of the person.
        """
        print("The person's name is:", self.name)
        print("His age is:", self.age)
        print("His mail is:", self._email)

    def edit_email(self, new_email):
        """
        Edits the email address of the person.

        :param new_email: The new email address.
        :type new_email: str
        """
        self._email = new_email

    @staticmethod
    def validMail(email):
        """
        Validates if the provided email is in a correct format.

        :param email: The email to be validated.
        :type email: str
        :return: True if valid, False otherwise.
        :rtype: bool
        """
        isMail = False
        if '@' in email:
            if len(email.split('@')) == 2:
                if len(email.split('@')[1].split('.')) == 2 and len(email.split('@')[1].split('.')[1]) > 0:
                    isMail = True
        return isMail


class Student(Person):
    """
    A class to represent a student, inheriting from the Person class. (A student is a person hopefully)

    Attributes
    ----------
    id : int
        The unique identifier for the student.
    registered_courses : list
        A list of registered courses for the student.
    
    Methods
    -------
    register_courses(course: Course):
        Registers a new course for the student.
    to_json() -> dict:
        Converts the student object to a dictionary/json.
    from_json(data: dict) -> Student:
        Creates a student object from a dictionary/json file.
    """
    
    def __init__(self, name, age, email, id, registered_courses=[]):
        """
        Constructs all the necessary attributes for the student object.

        :param name: The name of the student.
        :type name: str
        :param age: The age of the student.
        :type age: int
        :param email: The email address of the student.
        :type email: str
        :param id: The student ID.
        :type id: int
        :param registered_courses: A list of courses the student is registered in.
        :type registered_courses: list
        :raises ValueError: If any of the registered courses is not of type Course.
        """
        Person.__init__(self, name, age, email)
        assert type(id) == int, "Please enter a valid ID"
        assert type(registered_courses) == list, "Please enter a valid format"
        for course in registered_courses:
            if type(course) != Course:
                raise ValueError("Not a valid course")
        self.id = id
        self.registered_courses = registered_courses

    def register_courses(self, course):
        """
        Registers a new course for the student.

        :param course: The course to register.
        :type course: Course
        """
        self.registered_courses.append(course)

    def to_json(self):
        """
        Converts the student object to a dictionary.

        :return: A dictionary representation of the student.
        :rtype: dict
        """
        return {'name': self.name, 'age': self.age, 'email': self._email,
                'student_id': self.id, 'registered_courses': [course.to_dict() for course in self.registered_courses]}

    @staticmethod
    def from_json(data):
        """
        Creates a student object from a dictionary.

        :param data: The dictionary containing student data.
        :type data: dict
        :return: A Student object.
        :rtype: Student
        """
        student = Student(data['name'], data['age'], data['email'], data['student_id'])
        student.registered_courses = [Course.from_dict(course) for course in data['registered_courses']]
        return student


class Instructor(Person):
    """
    A class to represent an instructor, inheriting from the Person class. (Should be a person)

    Attributes
    ----------
    instructor_id : int
        The unique identifier for the instructor.
    assigned_courses : list
        A list of courses assigned to the instructor.
    
    Methods
    -------
    assign_course(course: Course):
        Assigns a course to the instructor.
    to_json() -> dict:
        Converts the instructor object to a dictionary.
    from_json(data: dict) -> Instructor:
        Creates an instructor object from a dictionary.
    """
    
    def __init__(self, name, age, email, iid, assigned_courses=[]):
        """
        Constructs all the necessary attributes for the instructor object.

        :param name: The name of the instructor.
        :type name: str
        :param age: The age of the instructor.
        :type age: int
        :param email: The email address of the instructor.
        :type email: str
        :param iid: The instructor ID.
        :type iid: int
        :param assigned_courses: A list of courses the instructor is assigned to.
        :type assigned_courses: list
        :raises ValueError: If any of the assigned courses is not of type Course.
        """
        Person.__init__(self, name, age, email)
        assert type(iid) == int, "Please enter a valid IID"
        assert type(assigned_courses) == list, "Please enter a valid format"
        for course in assigned_courses:
            if type(course) != Course:
                raise ValueError("Not a valid course")
        self.instructor_id = iid
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        :param course: The course to assign.
        :type course: Course
        """
        self.assigned_courses.append(course)

    def to_json(self):
        """
        Converts the instructor object to a dictionary.

        :return: A dictionary representation of the instructor.
        :rtype: dict
        """
        return {'name': self.name, 'age': self.age, 'email': self._email,
                'instructor_id': self.instructor_id, 'assigned_courses': [course.to_dict() for course in self.assigned_courses]}

    @staticmethod
    def from_json(data):
        """
        Creates an instructor object from a dictionary.

        :param data: The dictionary containing instructor data.
        :type data: dict
        :return: An Instructor object.
        :rtype: Instructor
        """
        instructor = Instructor(data['name'], data['age'], data['email'], data['instructor_id'])
        instructor.assigned_courses = [Course.from_dict(course) for course in data['assigned_courses']]
        return instructor

class Course:
    """
    A class to represent a course.

    Attributes
    ----------
    course_id : int
        The unique identifier for the course.
    course_name : str
        The name of the course.
    instructor : Instructor, optional
        The instructor assigned to the course (default is an empty string).
    enrolled_students : list
        A list of students enrolled in the course.
    
    Methods
    -------
    add_student(student: Student):
        Adds a student to the enrolled students list.
    to_json() -> dict:
        Converts the course object to a dictionary.
    from_json(data: dict) -> Course:
        Creates a course object from a dictionary.
    """
    
    def __init__(self, course_id, course_name, instructor="", enrolled_students=[]):
        """
        Constructs all the necessary attributes for the course object.

        :param course_id: The unique identifier for the course.
        :type course_id: int
        :param course_name: The name of the course.
        :type course_name: str
        :param instructor: The instructor for the course (optional).
        :type instructor: Instructor, optional
        :param enrolled_students: A list of students enrolled in the course (optional).
        :type enrolled_students: list
        :raises ValueError: If any of the enrolled students is not of type Student.
        :raises AssertionError: If course_id is not an integer or course_name is not a string.
        """
        assert type(course_id) == int, "Please enter a valid Course_ID"
        assert type(course_name) == str, "Please enter a valid course name"
        assert type(enrolled_students) == list, "Please enter a valid format"
        for student in enrolled_students:
            if type(student) != Student:
                raise ValueError("Not a valid student")
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students

    def add_student(self, student):
        """
        Adds a student to the course.

        :param student: The student to be added to the course.
        :type student: Student
        """
        self.enrolled_students.append(student)

    def to_json(self):
        """
        Converts the course object to a dictionary.

        :return: A dictionary representation of the course.
        :rtype: dict
        """
        return {'course_id': self.course_id, 'course_name': self.course_name,
                'instructor': self.instructor.to_json(), 'enrolled_students': [student.to_json() for student in self.enrolled_students]}

    @staticmethod
    def from_json(data):
        """
        Creates a course object from a dictionary.

        :param data: The dictionary containing course data.
        :type data: dict
        :return: A Course object.
        :rtype: Course
        """
        instructor = Instructor.from_json(data['instructor'])
        course = Course(data['course_id'], data['course_name'], instructor)
        course.enrolled_students = [Student.from_json(student) for student in data['enrolled_students']]
        return course


def save_json_all(filename, data):
    """
    Saves a list of objects (students, instructors, or courses) as a JSON file.

    :param filename: The name of the JSON file to save the data.
    :type filename: str
    :param data: The list of objects to save.
    :type data: list
    """
    with open(filename, 'w') as f:
        json.dump([obj.to_json() for obj in data], f)


def load_json_all(type, filename):
    """
    Loads data from a JSON file, either as courses or persons (students or instructors).

    :param type: True for loading persons (students or instructors), False for loading courses.
    :type type: bool
    :param filename: The name of the JSON file to load the data from.
    :type filename: str
    """
    if type:
        load_json_person(filename)
    else:
        load_json_course(filename)


def load_json_course(filename):
    """
    Loads a list of courses from a JSON file.

    :param filename: The name of the JSON file to load the courses from.
    :type filename: str
    :return: A list of Course objects.
    :rtype: list of Course
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        return [Course.from_json(course) for course in data]


def load_json_person(filename):
    """
    Loads a list of persons (students or instructors) from a JSON file.

    :param filename: The name of the JSON file to load the persons from.
    :type filename: str
    :return: A list of Person objects.
    :rtype: list of Person
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        return [Person.from_json(person) for person in data]


def save_data_csv(filename, courses):
    """
    Saves course data to a CSV file.

    :param filename: The name of the CSV file to save the data.
    :type filename: str
    :param courses: The list of courses to save.
    :type courses: list of Course
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['course_id', 'course_name', 'instructor_name', 'instructor_email', 'enrolled_students'])
        for course in courses:
            instructor = course.instructor
            students = ','.join([student.name for student in course.enrolled_students])
            writer.writerow([course.course_id, course.course_name, instructor.name, instructor._email, students])
