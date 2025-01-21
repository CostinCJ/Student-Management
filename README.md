# Student-Management
This project is a Python application for managing students, disciplines, and grades, featuring a command-line interface, undo/redo functionality, and error handling for robust data management. It provides a comprehensive system for educational institutions while showcasing key programming concepts such as object-oriented design, file handling, and testing. Below is a detailed description of its components and features.

**Key Features**

**Command-Line Interface:** The application is operated through a user-friendly CLI implemented in the `Services` class. Users can add, remove, and list students and disciplines, as well as assign grades. The interface includes prompts for various operations and handles user input effectively.

**Undo/Redo Functionality:** The application supports undo and redo operations using the `UndoService` class. Each modification to the repository (such as adding or removing a student or discipline) is recorded, allowing users to revert or reapply changes as needed.

**Data Management:** The application manages students, disciplines, and grades using different repository types (`MemoryRepository`, `TextFileRepository`, `BinaryFileRepository`). This modular design allows for flexible data storage options, including in-memory, text files, and binary files.

**Error Handling:** Custom exceptions (e.g., `StudentIdInvalidInput`, `DisciplineIdAlreadyExists`, `StudentNotFound`) ensure that invalid operations (such as adding a student with an existing ID or removing a non-existent discipline) are handled gracefully without crashing the program. Users are notified of errors and prompted to correct their input.

**Unit Testing:** Comprehensive testing is implemented to validate core functionalities such as adding/removing students and disciplines, assigning grades, and performing undo/redo operations. This ensures the correctness and reliability of the application.

**Object-Oriented Design:** The program is modular, with separate classes for students, disciplines, grades, repositories, and services. This structure promotes code reusability and scalability.

**How It Works**

**Initialization:** The program starts by reading configuration settings from a properties file to determine the repository type and file paths. It initializes the appropriate repository and the `Services` class.

**Data Operations:** Users can perform various operations such as adding/removing students and disciplines, listing all students and disciplines, assigning grades, and searching for students or disciplines by ID or name.

**Undo/Redo Operations:** Each data modification is recorded as a command. Users can undo the last operation or redo an undone operation, providing flexibility in managing data changes.

**Error Handling:** The application catches and handles exceptions, providing informative error messages to the user and ensuring the program continues to run smoothly.

**Testing:** Unit tests are written to cover all major functionalities, ensuring that the application behaves as expected under different scenarios.

This project demonstrates key programming concepts such as:
- Modular design using object-oriented programming principles.
- Flexible data storage options with different repository types.
- Error handling with custom exceptions for robust applications.
- Implementation of undo/redo functionality for data management.
- Writing unit tests for validating functionality and ensuring code reliability.
