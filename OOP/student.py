from .person import Person
import json
import re

class Student(Person):
    
    def __init__(self, name, age, email, student_id, registered_courses):
        super().__init__(name, age, email)     
        if not isinstance(student_id, str):
            raise TypeError("Student ID must be a string")
        if not student_id.strip():
            raise ValueError("Student ID cannot be blank")
        if not re.fullmatch(r"^[a-zA-Z0-9]+$", student_id):
            raise ValueError("Student ID can only contain alphanumeric characters")     
        if not isinstance(registered_courses, list):
            raise TypeError("Registered courses should be provided as a list")
        
        self.student_id = student_id
        self.registered_courses = registered_courses
    
    def register_course(self, course):
        from .course import Course
        if not isinstance(course, Course):
            raise TypeError("The course parameter must be an instance of Course")
        if self.student_id in course.enrolled_students:
            raise ValueError("This student is already registered in the course")

        self.registered_courses.append(course.course_id)
        course.add_student(self)

        course.update('Data/courses.json')
        self.update_file('Data/students.json')

    def to_json(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.get_email(),
            'student_id': self.student_id,
            'registered_courses': [course_id for course_id in self.registered_courses]
        }

    def save_to_file(self, filepath):
        from .instructor import Instructor
        if not self.is_id_unique(filepath, self.student_id):
            raise ValueError("Student ID already exists!")
        
        if not self.is_email_unique(filepath, self.get_email()):
            raise ValueError("Email address already exists!")

        try:
            with open(filepath, 'r') as file:
                try:
                    records = json.load(file)
                    if not isinstance(records, list):
                        records = []
                except json.JSONDecodeError:
                    records = []
        except FileNotFoundError:
            records = []

        records.append(self.to_json())

        with open(filepath, 'w') as file:
            json.dump(records, file, indent=4)

    @classmethod
    def is_id_unique(cls, filepath, student_id):
        existing_ids = cls.get_existing_ids(filepath)
        return student_id not in existing_ids

    @classmethod
    def get_existing_ids(cls, filepath):
        try:
            with open(filepath, 'r') as file:
                try:
                    records = json.load(file)
                    if not isinstance(records, list):
                        records = []
                except json.JSONDecodeError:
                    records = []
        except FileNotFoundError:
            records = []
        
        return {student['student_id'] for student in records}
    
    @classmethod
    def get_student_by_id(cls, filepath, student_id):
        with open(filepath, 'r') as file:
            records = json.load(file)
        for student_data in records:
            if student_data['student_id'] == student_id:
                return Student(student_data['name'], student_data['age'], student_data['email'], student_data['student_id'], student_data['registered_courses'])
        return None
    
    @classmethod
    def is_email_unique(cls, filepath, email):
        from .instructor import Instructor
        student_emails = cls.get_existing_emails(filepath)
        instructor_emails = Instructor.load_existing_emails('Data/instructors.json')
        return email not in student_emails and email not in instructor_emails

    @classmethod
    def get_existing_emails(cls, filepath):
        try:
            with open(filepath, 'r') as file:
                try:
                    records = json.load(file)
                    if not isinstance(records, list):
                        records = []
                except json.JSONDecodeError:
                    records = []
        except FileNotFoundError:
            records = []

        return {student['email'] for student in records}

    def update_file(self, filepath):
        if not self.is_id_unique(filepath, self.student_id):
            try:
                with open(filepath, 'r') as file:
                    try:
                        records = json.load(file)
                        if not isinstance(records, list):
                            records = []
                    except json.JSONDecodeError:
                        records = []
            except FileNotFoundError:
                records = []

            for index, student_data in enumerate(records):
                if student_data['student_id'] == self.student_id:
                    records[index] = self.to_json()
                    break
            else:
                raise ValueError("Student ID not found!")

            with open(filepath, 'w') as file:
                json.dump(records, file, indent=4)

    @classmethod
    def load_all_students(cls, filepath):
        students_list = []

        with open(filepath, 'r') as file:
            try:
                records = json.load(file)
                if not isinstance(records, list):
                    records = []
            except json.JSONDecodeError:
                records = []

        for student_data in records:
            student_instance = Student(student_data['name'], student_data['age'], student_data['email'], student_data['student_id'], student_data['registered_courses'])
            students_list.append(student_instance)

        return students_list

    def delete_from_file(self, filepath):
        all_students = Student.load_all_students(filepath)
        updated_students = [student for student in all_students if student.student_id != self.student_id]
        
        with open(filepath, 'w') as file:
            json.dump([student.to_json() for student in updated_students], file, indent=4)
