
# Student Result Management System

## Project Description

The Student Result Management System is a Python-based application developed to manage student academic records. It allows school administrators to register students, record subject scores, calculate results, generate report cards and manage academic information.

## Features

- Student registration and management.
- Search, update and delete student records.
- Record and update subject scores.
- Automatic calculation of total scores and averages.
- Automatic grade assignment.
- Individual student report cards.
- Class result summaries.
- Student rankings and alphabetical sorting.
- Class performance statistics.
- Report generation and text file export.
- JSON-based data storage.

## Technologies Used

- Python
- JSON
- Python Standard Library

## Project Structure

student_result_system/
- main.py
- student.py
- results.py
- storage.py
- reports.py
- data/students.json
- generated_reports/

## How to Run the Application

1. Install Python on your computer.
2. Open the project folder in Visual Studio Code.
3. Open the VS Code terminal.
4. Run the following command:

   python main.py

5. Use the displayed menu to navigate the application.

## Grading System

| Score | Grade |
|-------|-------|
| 70-100 | A |
| 60-69 | B |
| 50-59 | C |
| 45-49 | D |
| 0-44 | F |

## Data Storage

Student records are stored in a JSON file located in the data folder. The application automatically loads existing records when it starts and saves changes to the database.

## Developer

Developed as an individual practical project for the Introduction to Python Programming course.
