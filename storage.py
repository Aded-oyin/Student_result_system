
import json
from pathlib import Path
from student import Student


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "students.json"


def save_students(students):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    student_data = [
        student.to_dict() for student in students
    ]

    file = None

    try:
        file = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(student_data, file, indent=4)

    except OSError as error:
        raise error

    else:
        return True

    finally:
        if file is not None:
            file.close()


def load_students():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        save_students([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            student_data = json.load(file)

        if not isinstance(student_data, list):
            raise ValueError("Invalid student data format.")

        return [
            Student.from_dict(data) for data in student_data
        ]

    except (json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
        print(f"Warning: Could not load student records: {error}")
        return []
