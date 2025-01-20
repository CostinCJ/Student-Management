import pickle
from src.domain import Student, Discipline, Grade


class StudentNotFound(Exception):
    def __init__(self):
        super().__init__("Student not found")


class Repository:
    def add_student(self, student):
        raise NotImplementedError

    def add_discipline(self, discipline):
        raise NotImplementedError

    def remove_student(self, student):
        raise NotImplementedError

    def remove_discipline(self, discipline):
        raise NotImplementedError

    def update_student(self, student):
        raise NotImplementedError

    def update_discipline(self, discipline):
        raise NotImplementedError

    def list_students(self):
        raise NotImplementedError

    def list_disciplines(self):
        raise NotImplementedError

    def grade_student(self, grade):
        raise NotImplementedError

    def list_grades(self):
        raise NotImplementedError

    def get_student(self, student_id):
        raise NotImplementedError

    def remove_grade(self, grade):
        raise NotImplementedError


class MemoryRepository(Repository):
    def __init__(self):
        self.students = []
        self.disciplines = []
        self.grades = []

    def add_student(self, student):
        self.students.append(student)

    def add_discipline(self, discipline):
        self.disciplines.append(discipline)

    def remove_student(self, student):
        self.students.remove(student)
        self.grades = [grade for grade in self.grades if grade.student_id != student.student_id]

    def remove_discipline(self, discipline):
        self.disciplines.remove(discipline)

    def update_student(self, student):
        for i in range(len(self.students)):
            if self.students[i].student_id == student.student_id:
                self.students[i] = student
                break

    def update_discipline(self, discipline):
        for i in range(len(self.disciplines)):
            if self.disciplines[i].discipline_id == discipline.discipline_id:
                self.disciplines[i] = discipline
                break

    def list_students(self):
        return self.students

    def list_disciplines(self):
        return self.disciplines

    def grade_student(self, grade):
        self.grades.append(grade)

    def list_grades(self):
        return self.grades

    def get_student(self, student_id):
        return next((student for student in self.students if student.student_id == student_id), None)

    def remove_grade(self, grade):
        self.grades.remove(grade)


class TextFileRepository(Repository):
    def __init__(self, students_filename, disciplines_filename, grades_filename):
        self._students_filename = students_filename
        self._disciplines_filename = disciplines_filename
        self._grades_filename = grades_filename
        self.students = self._read_from_file(self._students_filename, Student)
        self.disciplines = self._read_from_file(self._disciplines_filename, Discipline)
        self.grades = self._read_from_file(self._grades_filename, Grade)

    def _write_to_file(self, filename, data):
        with open(filename, 'w') as f:
            for item in data:
                if isinstance(item, Student):
                    f.write(f"{item.student_id},{item.name}\n")
                elif isinstance(item, Discipline):
                    f.write(f"{item.discipline_id},{item.name}\n")
                elif isinstance(item, Grade):
                    f.write(f"{item.student_id},{item.discipline_id},{item.grade}\n")

    def _read_from_file(self, filename, entity_class):
        data = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    item_data = line.strip().split(',')
                    if entity_class == Student:
                        data.append(Student(int(item_data[0]), item_data[1]))
                    elif entity_class == Discipline:
                        data.append(Discipline(int(item_data[0]), item_data[1]))
                    elif entity_class == Grade:
                        data.append(Grade(int(item_data[0]), int(item_data[1]), int(item_data[2])))
        except (EOFError, FileNotFoundError):
            pass
        return data

    def add_student(self, student):
        self.students.append(student)
        self._write_to_file(self._students_filename, self.students)

    def add_discipline(self, discipline):
        self.disciplines.append(discipline)
        self._write_to_file(self._disciplines_filename, self.disciplines)

    def remove_student(self, student):
        self.students = [s for s in self.students if s.student_id != student.student_id]
        self._write_to_file(self._students_filename, self.students)

    def remove_discipline(self, discipline):
        self.disciplines = [d for d in self.disciplines if d.discipline_id != discipline.discipline_id]
        self._write_to_file(self._disciplines_filename, self.disciplines)

    def update_student(self, student):
        for i in range(len(self.students)):
            if self.students[i].student_id == student.student_id:
                self.students[i] = student
                break
        self._write_to_file(self._students_filename, self.students)

    def update_discipline(self, discipline):
        for i in range(len(self.disciplines)):
            if self.disciplines[i].discipline_id == discipline.discipline_id:
                self.disciplines[i] = discipline
                break
        self._write_to_file(self._disciplines_filename, self.disciplines)

    def grade_student(self, grade):
        self.grades.append(grade)
        self._write_to_file(self._grades_filename, self.grades)

    def list_students(self):
        return self.students

    def list_disciplines(self):
        return self.disciplines

    def list_grades(self):
        return self.grades

    def get_student(self, student_id):
        return next((student for student in self.students if student.student_id == student_id), None)

    def remove_grade(self, grade):
        self.grades.remove(grade)


class BinaryFileRepository(Repository):
    def __init__(self, students_filename, disciplines_filename, grades_filename):
        self._students_filename = students_filename
        self._disciplines_filename = disciplines_filename
        self._grades_filename = grades_filename
        self.students = self._read_from_file(self._students_filename)
        self.disciplines = self._read_from_file(self._disciplines_filename)
        self.grades = self._read_from_file(self._grades_filename)

    def _write_to_file(self, filename, data):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def _read_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
        except EOFError:
            data = []
        return data

    def add_student(self, student):
        self.students.append(student)
        self._write_to_file(self._students_filename, self.students)

    def add_discipline(self, discipline):
        self.disciplines.append(discipline)
        self._write_to_file(self._disciplines_filename, self.disciplines)

    def remove_student(self, student):
        self.students = [s for s in self.students if s.student_id != student.student_id]
        self._write_to_file(self._students_filename, self.students)

    def remove_discipline(self, discipline):
        self.disciplines = [d for d in self.disciplines if d.discipline_id != discipline.discipline_id]
        self._write_to_file(self._disciplines_filename, self.disciplines)

    def update_student(self, student):
        for i in range(len(self.students)):
            if self.students[i].student_id == student.student_id:
                self.students[i] = student
                break
        self._write_to_file(self._students_filename, self.students)

    def update_discipline(self, discipline):
        for i in range(len(self.disciplines)):
            if self.disciplines[i].discipline_id == discipline.discipline_id:
                self.disciplines[i] = discipline
                break
        self._write_to_file(self._disciplines_filename, self.disciplines)

    def grade_student(self, grade):
        self.grades.append(grade)
        self._write_to_file(self._grades_filename, self.grades)

    def list_students(self):
        return self.students

    def list_disciplines(self):
        return self.disciplines

    def list_grades(self):
        return self.grades

    def get_student(self, student_id):
        return next((student for student in self.students if student.student_id == student_id), None)

    def remove_grade(self, grade):
        self.grades.remove(grade)()
