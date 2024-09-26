import re

class Person:

    def __init__(self, name, age, email):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not name.strip():
            raise ValueError("Name cannot be blank")
        if not re.fullmatch(r"^[a-zA-Z\s]+$", name):
            raise ValueError("Name can only include letters and spaces")

        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 0:
            raise ValueError("Age cannot be less than zero")

        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        if not email.strip():
            raise ValueError("Email cannot be blank")
        if not self.validate_email(email):
            raise ValueError("Invalid email format")

        self.name = name
        self.age = age
        self.__email = email

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email

    def __repr__(self):
        return f"Name: {self.name}\nAge: {self.age}"
