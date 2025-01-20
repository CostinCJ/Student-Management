from src.services import Services, StudentIdAlreadyExists, StudentIdInvalidInput, StudentNotFound
from src.services import DisciplineIdAlreadyExists, DisciplineIdInvalidInput, DisciplineNotFound
from src.services import initialize_repository, StudentListIsEmpty, DisciplineListIsEmpty, InvalidSearchString
from src.services.undo_services import UndoRedoError


class UI:
    def __init__(self, services):
        self.services = services

    def add_student(self):
        try:
            student_id = int(input("Enter student id: "))
            name = input("Enter student name: ")
            self.services.add_student(student_id, name)
        except ValueError:
            print("Id must be an integer")
        except StudentIdInvalidInput as ve:
            print(ve)
        except StudentIdAlreadyExists as ve:
            print(ve)

    def add_discipline(self):
        try:
            discipline_id = int(input("Enter discipline id: "))
            name = input("Enter discipline name: ")
            self.services.add_discipline(discipline_id, name)
        except ValueError:
            print("Id must be an integer")
        except DisciplineIdInvalidInput as ve:
            print(ve)
        except DisciplineIdAlreadyExists as ve:
            print(ve)

    def remove_student(self):
        try:
            student_id = int(input("Enter student id: "))
            self.services.remove_student(student_id)
        except ValueError:
            print("Id must be an integer")
        except StudentIdInvalidInput as ve:
            print(ve)
        except StudentNotFound as ve:
            print(ve)

    def remove_discipline(self):
        try:
            discipline_id = int(input("Enter discipline id: "))
            self.services.remove_discipline(discipline_id)
        except ValueError:
            print("Id must be an integer")
        except DisciplineIdInvalidInput as ve:
            print(ve)
        except DisciplineNotFound as ve:
            print(ve)

    def list_students(self):
        try:
            students = self.services.list_students()
            for student in students:
                print(student)
        except StudentListIsEmpty as ve:
            print(ve)

    def list_disciplines(self):
        try:
            disciplines = self.services.list_disciplines()
            for discipline in disciplines:
                print(discipline)
        except DisciplineListIsEmpty as ve:
            print(ve)

    def grade_student(self):
        try:
            student_id = int(input("Enter student id: "))
            discipline_id = int(input("Enter discipline id: "))
            grade = int(input("Enter grade: "))
            self.services.grade_student(student_id, discipline_id, grade)
        except ValueError:
            print("Id, discipline_id, grade must be integers")
        except StudentNotFound as ve:
            print(ve)
        except DisciplineNotFound as ve:
            print(ve)

    def list_students_with_grade(self):
        try:
            students_with_grades = self.services.list_students_with_grades()
            student_discipline_grades = {}
            for student, discipline, grade_value in students_with_grades:
                if (student.name, discipline.name) not in student_discipline_grades:
                    student_discipline_grades[(student.name, discipline.name)] = []
                student_discipline_grades[(student.name, discipline.name)].append(grade_value)
            for (student_name, discipline_name), grades in student_discipline_grades.items():
                print(
                    f"Student name: {student_name}, Discipline name: {discipline_name}, "
                    f"grades: {', '.join(map(str, grades))}")
        except StudentListIsEmpty as ve:
            print(ve)

    def search_students(self):
        try:
            search_string = input("Enter student id or name to search: ")
            matching_students = self.services.search_students(search_string)
            for student in matching_students:
                print(student)
        except InvalidSearchString as ve:
            print(ve)

    def search_disciplines(self):
        try:
            search_string = input("Enter discipline id or name/title to search: ")
            matching_disciplines = self.services.search_disciplines(search_string)
            for discipline in matching_disciplines:
                print(discipline)
        except InvalidSearchString as ve:
            print(ve)

    def get_failing_students(self):
        try:
            failing_students = self.services.get_failing_students()
            for student in failing_students:
                print(student)
        except StudentListIsEmpty as ve:
            print(ve)

    def get_best_students(self):
        try:
            best_students = self.services.get_best_students()
            for student in best_students:
                print(student)
        except StudentListIsEmpty as ve:
            print(ve)

    def get_best_disciplines(self):
        try:
            best_disciplines = self.services.get_best_disciplines()
            for discipline in best_disciplines:
                print(discipline)
        except DisciplineListIsEmpty as ve:
            print(ve)

    def run(self):
        if not self.services.list_students():
            self.services.generate_students(20)
        if not self.services.list_disciplines():
            self.services.generate_disciplines(20)
        if not self.services.list_students_with_grades():
            self.services.generate_grades(20)
        self.services.undo_service.clear()
        while True:
            print("1. Add a student")
            print("2. Add a discipline")
            print("3. Remove a student")
            print("4. Remove a discipline")
            print("5. Display all students")
            print("6. Display all disciplines")
            print("7. Grade a student")
            print("8. Display all students with grades")
            print("9. Search students")
            print("10. Search disciplines")
            print("11. Display failing students")
            print("12. Display best students")
            print("13. Display best disciplines")
            print("14. Undo operation")
            print("15. Redo operation")
            print("0. Exit")
            option = input("Choose an option: ")
            if option == "1":
                self.add_student()
            elif option == "2":
                self.add_discipline()
            elif option == "3":
                self.remove_student()
            elif option == "4":
                self.remove_discipline()
            elif option == "5":
                self.list_students()
            elif option == "6":
                self.list_disciplines()
            elif option == "7":
                self.grade_student()
            elif option == "8":
                self.list_students_with_grade()
            elif option == "9":
                self.search_students()
            elif option == "10":
                self.search_disciplines()
            elif option == "11":
                self.get_failing_students()
            elif option == "12":
                self.get_best_students()
            elif option == "13":
                self.get_best_disciplines()
            elif option == "14":
                try:
                    self.services.undo_service.undo()
                except UndoRedoError as e:
                    print(e)
            elif option == "15":
                try:
                    self.services.undo_service.redo()
                except UndoRedoError as e:
                    print(e)
            elif option == "0":
                break
            else:
                print("Invalid option")


def main():
    repository = initialize_repository()
    services = Services(repository)

    ui = UI(services)
    ui.run()


if __name__ == '__main__':
    main()
