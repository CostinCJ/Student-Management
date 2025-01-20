class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return f"Student id: {self.student_id}, Name: {self.name}"


class Discipline:
    def __init__(self, discipline_id, name):
        self.discipline_id = discipline_id
        self.name = name

    def __str__(self):
        return f"Discipline id: {self.discipline_id}, Name: {self.name}"


class Grade:
    def __init__(self, student_id, discipline_id, grade):
        self.student_id = student_id
        self.discipline_id = discipline_id
        self.grade = grade

    def __str__(self):
        return f"Student id: {self.student_id}, Discipline id: {self.discipline_id}, Grade: {self.grade}"
