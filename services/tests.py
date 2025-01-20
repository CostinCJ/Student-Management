import unittest
from src.repository import MemoryRepository, Repository, StudentNotFound
from src.domain import Student, Discipline, Grade
from src.services import (Services, StudentIdInvalidInput, StudentIdAlreadyExists, StudentNotFound,
                          DisciplineIdInvalidInput, DisciplineIdAlreadyExists, DisciplineNotFound, StudentListIsEmpty,
                          DisciplineListIsEmpty, InvalidSearchString)


class TestServices(unittest.TestCase):
    def setUp(self):
        self.services = Services(MemoryRepository())

    def test_add_student(self):
        self.services.add_student(1, "Costin Joldes")
        self.assertEqual(len(self.services.list_students()), 1)
        self.services.add_student(2, "Cristian Onet")
        self.assertEqual(len(self.services.list_students()), 2)
        self.assertEqual(self.services.list_students()[0].student_id, 1)
        self.assertEqual(self.services.list_students()[1].student_id, 2)
        self.assertEqual(self.services.list_students()[0].name, "Costin Joldes")
        self.assertEqual(self.services.list_students()[1].name, "Cristian Onet")

    def test_add_discipline(self):
        self.services.add_discipline(1, "Math")
        self.assertEqual(len(self.services.list_disciplines()), 1)
        self.services.add_discipline(2, "English")
        self.assertEqual(len(self.services.list_disciplines()), 2)
        self.assertEqual(self.services.list_disciplines()[0].discipline_id, 1)
        self.assertEqual(self.services.list_disciplines()[1].discipline_id, 2)
        self.assertEqual(self.services.list_disciplines()[0].name, "Math")
        self.assertEqual(self.services.list_disciplines()[1].name, "English")

    def test_remove_student(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_student(2, "Cristian Onet")
        self.assertEqual(len(self.services.list_students()), 2)
        self.services.remove_student(1)
        self.assertEqual(len(self.services.list_students()), 1)
        self.assertEqual(self.services.list_students()[0].student_id, 2)
        self.assertEqual(self.services.list_students()[0].name, "Cristian Onet")

    def test_remove_discipline(self):
        self.services.add_discipline(1, "Math")
        self.services.add_discipline(2, "English")
        self.assertEqual(len(self.services.list_disciplines()), 2)
        self.services.remove_discipline(1)
        self.assertEqual(len(self.services.list_disciplines()), 1)
        self.assertEqual(self.services.list_disciplines()[0].discipline_id, 2)
        self.assertEqual(self.services.list_disciplines()[0].name, "English")

    def test_list_students(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_student(2, "Cristian Onet")
        self.assertEqual(len(self.services.list_students()), 2)
        self.assertEqual(self.services.list_students()[0].student_id, 1)
        self.assertEqual(self.services.list_students()[1].student_id, 2)
        self.assertEqual(self.services.list_students()[0].name, "Costin Joldes")
        self.assertEqual(self.services.list_students()[1].name, "Cristian Onet")

    def test_list_disciplines(self):
        self.services.add_discipline(1, "Math")
        self.services.add_discipline(2, "English")
        self.assertEqual(len(self.services.list_disciplines()), 2)
        self.assertEqual(self.services.list_disciplines()[0].discipline_id, 1)
        self.assertEqual(self.services.list_disciplines()[1].discipline_id, 2)
        self.assertEqual(self.services.list_disciplines()[0].name, "Math")
        self.assertEqual(self.services.list_disciplines()[1].name, "English")

    def test_generate_students(self):
        self.services.generate_students(5)
        self.assertEqual(len(self.services.list_students()), 5)

    def test_generate_disciplines(self):
        self.services.generate_disciplines(5)
        self.assertEqual(len(self.services.list_disciplines()), 5)

    def test_generate_grades(self):
        self.services.generate_students(5)
        self.services.generate_disciplines(5)
        self.services.generate_grades(5)
        self.assertEqual(len(self.services.list_grades_1()), 5)

    def test_grade_student(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_discipline(1, "Math")
        self.services.grade_student(1, 1, 10)
        self.assertEqual(len(self.services.list_grades_1()), 1)
        self.assertEqual(self.services.list_grades_1()[0].student_id, 1)
        self.assertEqual(self.services.list_grades_1()[0].discipline_id, 1)
        self.assertEqual(self.services.list_grades_1()[0].grade, 10)

    def test_list_students_with_grades(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_discipline(1, "Math")
        self.services.grade_student(1, 1, 10)
        self.assertEqual(len(self.services.list_students_with_grades()), 1)
        self.assertEqual(self.services.list_students_with_grades()[0][0].student_id, 1)
        self.assertEqual(self.services.list_students_with_grades()[0][1].discipline_id, 1)
        self.assertEqual(self.services.list_students_with_grades()[0][2], 10)

    def test_search_students(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_student(2, "Cristian Onet")
        self.services.add_student(3, "Ionut Burz")
        self.services.add_student(4, "Alexia Goia")
        self.services.add_student(5, "Andra Balea")
        self.assertEqual(len(self.services.search_students("Costin")), 1)
        self.assertEqual(len(self.services.search_students("Burz")), 1)
        self.assertEqual(len(self.services.search_students("a")), 3)

    def test_search_disciplines(self):
        self.services.add_discipline(1, "Math")
        self.services.add_discipline(2, "English")
        self.services.add_discipline(3, "French")
        self.services.add_discipline(4, "German")
        self.services.add_discipline(5, "Spanish")
        self.assertEqual(len(self.services.search_disciplines("Math")), 1)
        self.assertEqual(len(self.services.search_disciplines("French")), 1)
        self.assertEqual(len(self.services.search_disciplines("a")), 3)

    def test_get_failing_students(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_student(2, "Cristian Onet")
        self.services.add_student(3, "Ionut Burz")
        self.services.add_student(4, "Alexia Goia")
        self.services.add_student(5, "Andra Balea")
        self.services.add_discipline(1, "Math")
        self.services.add_discipline(2, "English")
        self.services.add_discipline(3, "French")
        self.services.add_discipline(4, "German")
        self.services.add_discipline(5, "Spanish")
        self.services.grade_student(1, 1, 1)
        self.services.grade_student(1, 2, 2)
        self.services.grade_student(1, 3, 5)
        self.services.grade_student(1, 4, 5)
        self.services.grade_student(1, 5, 5)
        self.services.grade_student(2, 1, 10)
        self.services.grade_student(2, 2, 10)
        self.services.grade_student(2, 3, 10)
        self.services.grade_student(2, 4, 10)
        self.services.grade_student(2, 5, 10)
        self.services.grade_student(3, 1, 5)
        self.services.grade_student(3, 2, 2)
        self.services.grade_student(3, 3, 4)
        self.services.grade_student(3, 4, 2)
        self.services.grade_student(3, 5, 2)
        self.services.grade_student(4, 1, 10)
        self.services.grade_student(4, 2, 10)
        self.services.grade_student(4, 3, 10)
        self.services.grade_student(4, 4, 10)
        self.services.grade_student(4, 5, 10)
        self.services.grade_student(5, 1, 10)
        self.services.grade_student(5, 2, 10)
        self.services.grade_student(5, 3, 10)
        self.services.grade_student(5, 4, 10)
        self.services.grade_student(5, 5, 10)
        self.assertEqual(len(self.services.get_failing_students()), 2)

    def test_get_best_students(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_student(2, "Cristian Onet")
        self.services.add_student(3, "Ionut Burz")
        self.services.add_student(4, "Alexia Goia")
        self.services.add_student(5, "Andra Balea")
        self.services.add_discipline(1, "Math")
        self.services.add_discipline(2, "English")
        self.services.add_discipline(3, "French")
        self.services.add_discipline(4, "German")
        self.services.add_discipline(5, "Spanish")
        self.services.grade_student(1, 1, 1)
        self.services.grade_student(1, 2, 2)
        self.services.grade_student(1, 3, 5)
        self.services.grade_student(1, 4, 5)
        self.services.grade_student(1, 5, 5)
        self.services.grade_student(2, 1, 10)
        self.services.grade_student(2, 2, 10)
        self.services.grade_student(2, 3, 10)
        self.services.grade_student(2, 4, 10)
        self.services.grade_student(2, 5, 10)
        self.services.grade_student(3, 1, 5)
        self.services.grade_student(3, 2, 2)
        self.services.grade_student(3, 3, 4)
        self.services.grade_student(3, 4, 2)
        self.services.grade_student(3, 5, 2)
        self.services.grade_student(4, 1, 10)
        self.services.grade_student(4, 2, 10)
        self.services.grade_student(4, 3, 10)
        self.services.grade_student(4, 4, 10)
        self.services.grade_student(4, 5, 10)
        self.services.grade_student(5, 1, 10)
        self.services.grade_student(5, 2, 10)
        self.services.grade_student(5, 3, 10)
        self.services.grade_student(5, 4, 10)
        self.services.grade_student(5, 5, 10)
        self.assertEqual(len(self.services.get_best_students()), 3)

    def test_get_best_disciplines(self):
        self.services.add_student(1, "Costin Joldes")
        self.services.add_student(2, "Cristian Onet")
        self.services.add_student(3, "Ionut Burz")
        self.services.add_student(4, "Alexia Goia")
        self.services.add_student(5, "Andra Balea")
        self.services.add_discipline(1, "Math")
        self.services.add_discipline(2, "English")
        self.services.add_discipline(3, "French")
        self.services.add_discipline(4, "German")
        self.services.add_discipline(5, "Spanish")
        self.services.grade_student(1, 1, 1)
        self.services.grade_student(1, 2, 2)
        self.services.grade_student(1, 3, 5)
        self.services.grade_student(1, 4, 5)
        self.assertEqual(len(self.services.get_best_disciplines()), 2)

    def test_add_student_invalid_id(self):
        with self.assertRaises(StudentIdInvalidInput):
            self.services.add_student("invalid_id", "Test Student")

    def test_add_student_already_exists(self):
        self.services.add_student(1, "Test Student")
        with self.assertRaises(StudentIdAlreadyExists):
            self.services.add_student(1, "Another Student")

    def test_remove_student_not_found(self):
        with self.assertRaises(StudentNotFound):
            self.services.remove_student(1)

    def test_add_discipline_invalid_id(self):
        with self.assertRaises(DisciplineIdInvalidInput):
            self.services.add_discipline("invalid_id", "Test Discipline")

    def test_add_discipline_already_exists(self):
        self.services.add_discipline(1, "Test Discipline")
        with self.assertRaises(DisciplineIdAlreadyExists):
            self.services.add_discipline(1, "Another Discipline")

    def test_remove_discipline_not_found(self):
        with self.assertRaises(DisciplineNotFound):
            self.services.remove_discipline(1)

    def test_list_students_empty(self):
        with self.assertRaises(StudentListIsEmpty):
            self.services.list_students()

    def test_list_disciplines_empty(self):
        with self.assertRaises(DisciplineListIsEmpty):
            self.services.list_disciplines()

    def test_search_students_invalid_string(self):
        with self.assertRaises(InvalidSearchString):
            self.services.search_students(123)

    def test_search_disciplines_invalid_string(self):
        with self.assertRaises(InvalidSearchString):
            self.services.search_disciplines(123)


class TestMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MemoryRepository()

    def test_update_student(self):
        student = Student(1, "Test Student")
        self.repository.add_student(student)
        updated_student = Student(1, "Updated Student")
        self.repository.update_student(updated_student)
        students = self.repository.list_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].student_id, 1)
        self.assertEqual(students[0].name, "Updated Student")

    def test_update_discipline(self):
        discipline = Discipline(1, "Test Discipline")
        self.repository.add_discipline(discipline)
        updated_discipline = Discipline(1, "Updated Discipline")
        self.repository.update_discipline(updated_discipline)
        disciplines = self.repository.list_disciplines()
        self.assertEqual(len(disciplines), 1)
        self.assertEqual(disciplines[0].discipline_id, 1)
        self.assertEqual(disciplines[0].name, "Updated Discipline")


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.repository = Repository()

    def test_add_student(self):
        with self.assertRaises(NotImplementedError):
            self.repository.add_student(None)

    def test_add_discipline(self):
        with self.assertRaises(NotImplementedError):
            self.repository.add_discipline(None)

    def test_remove_student(self):
        with self.assertRaises(NotImplementedError):
            self.repository.remove_student(None)

    def test_remove_discipline(self):
        with self.assertRaises(NotImplementedError):
            self.repository.remove_discipline(None)

    def test_update_student(self):
        with self.assertRaises(NotImplementedError):
            self.repository.update_student(None)

    def test_update_discipline(self):
        with self.assertRaises(NotImplementedError):
            self.repository.update_discipline(None)

    def test_list_students(self):
        with self.assertRaises(NotImplementedError):
            self.repository.list_students()

    def test_list_disciplines(self):
        with self.assertRaises(NotImplementedError):
            self.repository.list_disciplines()


class TestDomain(unittest.TestCase):
    def test_student(self):
        student = Student(1, "Test Student")
        self.assertEqual(student.student_id, 1)
        self.assertEqual(student.name, "Test Student")
        self.assertEqual(str(student), "Student id: 1, Name: Test Student")

    def test_discipline(self):
        discipline = Discipline(1, "Test Discipline")
        self.assertEqual(discipline.discipline_id, 1)
        self.assertEqual(discipline.name, "Test Discipline")
        self.assertEqual(str(discipline), "Discipline id: 1, Name: Test Discipline")

    def test_grade(self):
        grade = Grade(1, 1, 10)
        self.assertEqual(grade.student_id, 1)
        self.assertEqual(grade.discipline_id, 1)
        self.assertEqual(grade.grade, 10)
        self.assertEqual(str(grade), "Student id: 1, Discipline id: 1, Grade: 10")
