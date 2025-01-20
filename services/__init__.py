import random
from src.domain import Student, Discipline, Grade
from src.repository import MemoryRepository, TextFileRepository, BinaryFileRepository
from src.services.undo_services import UndoService, Command, Operation


class StudentIdInvalidInput(Exception):
    def __init__(self):
        super().__init__("Id must be an integer")


class StudentIdAlreadyExists(Exception):
    def __init__(self):
        super().__init__("A student with this id already exists")


class StudentNotFound(Exception):
    def __init__(self):
        super().__init__("Student with this id does not exist")


class DisciplineIdInvalidInput(Exception):
    def __init__(self):
        super().__init__("Id must be an integer")


class DisciplineIdAlreadyExists(Exception):
    def __init__(self):
        super().__init__("A discipline with this id already exists")


class DisciplineNotFound(Exception):
    def __init__(self):
        super().__init__("Discipline with this id does not exist")


class StudentListIsEmpty(Exception):
    def __init__(self):
        super().__init__("The student list is empty")


class DisciplineListIsEmpty(Exception):
    def __init__(self):
        super().__init__("The discipline list is empty")


class InvalidSearchString(Exception):
    def __init__(self):
        super().__init__("The search string is invalid")


class Services:
    def __init__(self, repository):
        self.repository = repository
        self.undo_service = UndoService()

    def add_student(self, student_id, name):
        """
        Add a student to the repository
        :param student_id: student id
        :param name: student name
        :return: adds the student to the repository
        """
        if not isinstance(student_id, int):
            raise StudentIdInvalidInput
        if any(student.student_id == student_id for student in self.repository.list_students()):
            raise StudentIdAlreadyExists
        student = Student(student_id, name)
        self.repository.add_student(student)
        undo_command = Command(self.repository.remove_student, student)
        redo_command = Command(self.repository.add_student, student)
        operation = Operation(undo_command, redo_command)
        self.undo_service.register(operation)

    def remove_student(self, student_id):
        """
        Remove a student from the repository
        :param student_id: student id
        :return: removes the student from the repository
        """
        student = next((student for student in self.repository.list_students() if student.student_id == student_id), None)
        if student is None:
            raise StudentNotFound
        self.repository.remove_student(student)
        undo_command = Command(self.repository.add_student, student)
        redo_command = Command(self.repository.remove_student, student)
        operation = Operation(undo_command, redo_command)
        self.undo_service.register(operation)

    def add_discipline(self, discipline_id, name):
        """
        Add a discipline to the repository
        :param discipline_id: discipline id
        :param name: discipline name
        :return: adds the discipline to the repository
        """
        if not isinstance(discipline_id, int):
            raise DisciplineIdInvalidInput
        if any(discipline.discipline_id == discipline_id for discipline in self.repository.list_disciplines()):
            raise DisciplineIdAlreadyExists
        discipline = Discipline(discipline_id, name)
        self.repository.add_discipline(discipline)
        undo_command = Command(self.repository.remove_discipline, discipline)
        redo_command = Command(self.repository.add_discipline, discipline)
        operation = Operation(undo_command, redo_command)
        self.undo_service.register(operation)

    def remove_discipline(self, discipline_id):
        """
        Remove a discipline from the repository
        :param discipline_id: the discipline id
        :return: removes the discipline from the repository
        """
        discipline = next(
            (discipline for discipline in self.repository.list_disciplines()
             if discipline.discipline_id == discipline_id), None)
        if discipline is None:
            raise DisciplineNotFound
        self.repository.remove_discipline(discipline)
        undo_command = Command(self.repository.add_discipline, discipline)
        redo_command = Command(self.repository.remove_discipline, discipline)
        operation = Operation(undo_command, redo_command)
        self.undo_service.register(operation)

    def list_students(self):
        students = self.repository.list_students()
        if students:
            return students
        else:
            return []

    def list_disciplines(self):
        disciplines = self.repository.list_disciplines()
        if disciplines:
            return disciplines
        else:
            return []

    def generate_students(self, n):
        family_names = ["Joldes", "Onet", "Burz", "Goia", "Balea", "Pasca", "Vasiu"]
        given_names = ["Costin", "Cristian", "Ionut", "Alexia", "Andra", "Rares", "Andrei"]
        current_id = 1

        while n > 0:
            name = random.choice(family_names) + " " + random.choice(given_names)
            self.add_student(current_id, name)
            current_id += 1
            n -= 1

    def generate_disciplines(self, n):
        disciplines = ["Math", "English", "French", "German", "Spanish", "History", "Geography", "Physics", "Chemistry",
                       "Biology", "Computer Science", "Economics", "Philosophy", "Psychology", "Sociology",
                       "Physical Education", "Music", "Art", "Religion", "Civic Education", "Latin", "Greek",
                       "Romanian"]
        current_id = 1

        while n > 0:
            name = random.choice(disciplines)
            self.add_discipline(current_id, name)
            current_id += 1
            n -= 1

    def grade_student(self, student_id, discipline_id, grade_value):
        student = next((student for student in self.repository.list_students() if student.student_id == student_id),
                       None)
        if student is None:
            raise StudentNotFound
        discipline = next((discipline for discipline in self.repository.list_disciplines() if
                           discipline.discipline_id == discipline_id), None)
        if discipline is None:
            raise DisciplineNotFound
        grade = Grade(student_id, discipline_id, grade_value)
        self.repository.grade_student(grade)
        undo_command = Command(self.repository.remove_grade, grade)
        redo_command = Command(self.repository.grade_student, grade)
        operation = Operation(undo_command, redo_command)
        self.undo_service.register(operation)

    def list_students_with_grades(self):
        grades = self.repository.list_grades()
        students_with_grades = []
        for grade in grades:
            student = next(
                (student for student in self.repository.list_students() if student.student_id == grade.student_id),
                None)
            discipline = next((discipline for discipline in self.repository.list_disciplines() if
                               discipline.discipline_id == grade.discipline_id), None)
            if student and discipline:
                students_with_grades.append((student, discipline, grade.grade))
        return students_with_grades

    def generate_grades(self, n):
        students = self.repository.list_students()
        disciplines = self.repository.list_disciplines()
        current_id = 1

        while n > 0:
            student = random.choice(students)
            discipline = random.choice(disciplines)
            grade_value = random.randint(1, 10)
            grade = Grade(student.student_id, discipline.discipline_id, grade_value)
            self.repository.grade_student(grade)
            current_id += 1
            n -= 1

    def search_students(self, search_string):
        if not isinstance(search_string, str):
            raise InvalidSearchString
        search_string = search_string.lower()
        matching_students = [student for student in self.repository.list_students()
                             if search_string in str(student.student_id).lower() or
                             search_string in student.name.lower()]
        return matching_students

    def search_disciplines(self, search_string):
        if not isinstance(search_string, str):
            raise InvalidSearchString
        search_string = search_string.lower()
        matching_disciplines = [discipline for discipline in self.repository.list_disciplines()
                                if search_string in str(discipline.discipline_id).lower() or
                                search_string in discipline.name.lower()]
        return matching_disciplines

    def get_failing_students(self):
        students = self.repository.list_students()
        grades = self.repository.list_grades()
        failing_students = []
        for student in students:
            student_grades = [grade.grade for grade in grades if grade.student_id == student.student_id]
            if student_grades and sum(student_grades) / len(student_grades) < 5:
                failing_students.append(student)
        if not failing_students:
            raise StudentListIsEmpty
        return failing_students

    def get_best_students(self):
        students = self.repository.list_students()
        grades = self.repository.list_grades()
        student_averages = []
        for student in students:
            student_grades = [grade.grade for grade in grades if grade.student_id == student.student_id]
            if student_grades:
                average = sum(student_grades) / len(student_grades)
                if average >= 5:
                    student_averages.append((student, average))
        student_averages.sort(key=lambda x: x[1], reverse=True)
        if not student_averages:
            raise StudentListIsEmpty
        return [student for student, average in student_averages]

    def get_best_disciplines(self):
        disciplines = self.repository.list_disciplines()
        grades = self.repository.list_grades()
        discipline_averages = []
        for discipline in disciplines:
            discipline_grades = [grade.grade for grade in grades
                                 if grade.discipline_id == discipline.discipline_id]
            if discipline_grades:
                average = sum(discipline_grades) / len(discipline_grades)
                if average >= 5:
                    discipline_averages.append((discipline, average))
        discipline_averages.sort(key=lambda x: x[1], reverse=True)
        if not discipline_averages:
            raise DisciplineListIsEmpty
        return [discipline for discipline, average in discipline_averages]

    def list_grades_1(self):
        return self.repository.list_grades()


def initialize_repository():
    settings = {}
    with open('settings.properties', 'r') as f:
        for line in f:
            key, value = line.strip().split(' = ')
            settings[key] = value

    repository_type = settings['repository']
    students_file = settings['students']
    disciplines_file = settings['disciplines']
    grades_file = settings['grades']

    if repository_type == 'MemoryRepository':
        return MemoryRepository()
    elif repository_type == 'BinaryFileRepository':
        return BinaryFileRepository(students_file, disciplines_file, grades_file)
    elif repository_type == 'TextFileRepository':
        return TextFileRepository(students_file, disciplines_file, grades_file)
    else:
        raise ValueError(f"Invalid repository type: {repository_type}")
