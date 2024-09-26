import json
import re

class Course:

    def __init__(self, course_id, course_name, instructor, enrolled_students=None):
        from .instructor import Instructor
        if not isinstance(course_id, str):
            raise TypeError("Course ID must be a string")
        if not course_id.strip():
            raise ValueError("Course ID cannot be empty")
        if not re.match(r"^[a-zA-Z0-9]+$", course_id):
            raise ValueError("Course ID must contain only alphanumeric characters")
        if not isinstance(course_name, str):
            raise TypeError("Course name must be a string")
        if not course_name.strip():
            raise ValueError("Course name cannot be empty")
        if instructor is not None and not isinstance(instructor, Instructor):
            raise TypeError("Instructor must be an instance of Instructor or None")
        if enrolled_students is None:
            enrolled_students = []
        elif not isinstance(enrolled_students, list):
            raise TypeError("Enrolled students must be a list")

        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students

    def add_student(self, student):
        from .student import Student
        if not isinstance(student, Student):
            raise TypeError("The student parameter must be an instance of Student")
        self.enrolled_students.append(student.student_id)

    def to_json(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.to_json() if self.instructor is not None else None,
            'enrolled_students': self.enrolled_students
        }

    def save_to_file(self, filename):
        if not self.is_unique_id(filename, self.course_id):
            raise ValueError("Course ID already exists!")
        if not self.is_unique_name(filename, self.course_name):
            raise ValueError("Course name already exists!") 
        data = self._load_json(filename)
        data.append(self.to_json())
        self._write_json(filename, data)

    @classmethod
    def is_unique_id(cls, filename, course_id):
        existing_ids = cls.load_existing_ids(filename)
        return course_id not in existing_ids

    @classmethod
    def load_existing_ids(cls, filename):
        data = cls._load_json(filename)
        return {course['course_id'] for course in data}

    @classmethod
    def load_course_by_id(cls, filename, course_id):
        from .instructor import Instructor
        data = cls._load_json(filename)
        for course_data in data:
            if course_data['course_id'] == course_id:
                instructor_data = course_data.get('instructor')
                instructor = Instructor(
                    name=instructor_data['name'],
                    age=instructor_data['age'],
                    email=instructor_data['email'],
                    instructor_id=instructor_data['instructor_id'],
                    assigned_courses=instructor_data['assigned_courses']
                ) if instructor_data else None

                return cls(
                    course_id=course_data['course_id'],
                    course_name=course_data['course_name'],
                    instructor=instructor,
                    enrolled_students=course_data.get('enrolled_students', [])
                )
        return None

    @classmethod
    def load_all_courses(cls, filename):
        data = cls._load_json(filename)
        return [course_data['course_id'] for course_data in data]

    @classmethod
    def is_unique_name(cls, filename, course_name):
        existing_names = cls.load_existing_names(filename)
        return course_name not in existing_names

    @classmethod
    def load_existing_names(cls, filename):
        data = cls._load_json(filename)
        return {course['course_name'] for course in data}

    def update(self, filename):
        data = self._load_json(filename)
        for i, course_data in enumerate(data):
            if course_data['course_id'] == self.course_id:
                data[i] = self.to_json()
                break
        else:
            raise ValueError("Course ID not found!")
        self._write_json(filename, data)

    @classmethod
    def load_all_courses_fully(cls, filename):
        from .instructor import Instructor
        data = cls._load_json(filename)
        courses = []
        for course_data in data:
            instructor_data = course_data.get('instructor')
            instructor = Instructor(
                name=instructor_data['name'],
                age=instructor_data['age'],
                email=instructor_data['email'],
                instructor_id=instructor_data['instructor_id'],
                assigned_courses=instructor_data['assigned_courses']
            ) if instructor_data else None

            courses.append(cls(
                course_id=course_data['course_id'],
                course_name=course_data['course_name'],
                instructor=instructor,
                enrolled_students=course_data.get('enrolled_students', [])
            ))
        return courses

    def delete_from_file(self, filename):
        courses = self.load_all_courses_fully(filename)
        courses = [course for course in courses if course.course_id != self.course_id]
        self._write_json(filename, [course.to_json() for course in courses])

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
