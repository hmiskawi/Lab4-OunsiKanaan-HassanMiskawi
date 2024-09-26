from .person import Person
import json
import re

class Instructor(Person):

    def __init__(self, name, age, email, instructor_id, assigned_courses=None):
        super().__init__(name, age, email)
        if not isinstance(instructor_id, str):
            raise TypeError("Instructor ID must be a string")
        if not instructor_id.strip():
            raise ValueError("Instructor ID cannot be empty")
        if not re.match(r"^[a-zA-Z0-9]+$", instructor_id):
            raise ValueError("Instructor ID must contain only alphanumeric characters")  
        if assigned_courses is None:
            assigned_courses = []
        elif not isinstance(assigned_courses, list):
            raise TypeError("Assigned Courses must be a list")
        
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        from .course import Course
        if not isinstance(course, Course):
            raise TypeError("The course parameter must be an instance of Course")
        if course.instructor is None:
            course.instructor = self
            self.assigned_courses.append(course.course_id)
            course.update('Data/courses.json')
            self.update('Data/instructors.json')
        elif course.instructor.instructor_id == self.instructor_id:
            raise ValueError('You are already assigned to this course')
        else:
            raise ValueError('The course already has an instructor assigned')

    def to_json(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.get_email(),
            'instructor_id': self.instructor_id,
            'assigned_courses': self.assigned_courses
        }

    def save_to_file(self, filename):
        if not self.is_unique_id(filename, self.instructor_id):
            raise ValueError("Instructor ID already exists!")
        if not self.is_unique_email(filename, self.get_email()):
            raise ValueError("Email address already exists!")
        data = self._load_json(filename)
        data.append(self.to_json())
        self._write_json(filename, data)

    @classmethod
    def is_unique_id(cls, filename, instructor_id):
        return instructor_id not in cls.load_existing_ids(filename)

    @classmethod
    def load_existing_ids(cls, filename):
        data = cls._load_json(filename)
        return {instructor['instructor_id'] for instructor in data}

    @classmethod
    def load_instructor_by_id(cls, filename, instructor_id):
        data = cls._load_json(filename)
        for instructor_data in data:
            if instructor_data['instructor_id'] == instructor_id:
                return cls(
                    name=instructor_data['name'],
                    age=instructor_data['age'],
                    email=instructor_data['email'],
                    instructor_id=instructor_data['instructor_id'],
                    assigned_courses=instructor_data.get('assigned_courses', [])
                )
        return None

    @classmethod
    def is_unique_email(cls, filename, email):
        from .student import Student
        existing_emails = cls.load_existing_emails(filename)
        existing_std_emails = Student.get_existing_emails('Data/students.json')
        return email not in existing_emails and email not in existing_std_emails

    @classmethod
    def load_existing_emails(cls, filename):
        data = cls._load_json(filename)
        return {instructor['email'] for instructor in data}

    def update(self, filename):
        data = self._load_json(filename)
        for i, instructor_data in enumerate(data):
            if instructor_data['instructor_id'] == self.instructor_id:
                data[i] = self.to_json()
                break
        else:
            raise ValueError("Instructor ID not found!")
        self._write_json(filename, data)

    @classmethod
    def load_all_instructors(cls, filename):
        data = cls._load_json(filename)
        return [
            cls(
                name=instructor_data['name'],
                age=instructor_data['age'],
                email=instructor_data['email'],
                instructor_id=instructor_data['instructor_id'],
                assigned_courses=instructor_data.get('assigned_courses', [])
            ) for instructor_data in data
        ]

    def delete_from_file(self, filename):
        instructors = self.load_all_instructors(filename)
        instructors = [instructor for instructor in instructors if instructor.instructor_id != self.instructor_id]
        self._write_json(filename, [instructor.to_json() for instructor in instructors])

    @staticmethod
    def _load_json(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def _write_json(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
