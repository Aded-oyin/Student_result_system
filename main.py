
from datetime import datetime

from student import Student
from storage import load_students, save_students
from results import calculate_total, calculate_average, calculate_grade
from reports import (
    generate_student_report,
    generate_class_report,
    generate_class_statistics,
    sort_students,
    save_report
)


def find_student(students, student_id):
    for student in students:
        if student.student_id.lower() == student_id.lower():
            return student

    return None


def get_valid_date(prompt):
    while True:
        date_value = input(prompt).strip()

        try:
            date_object = datetime.strptime(date_value, "%Y-%m-%d")

            if date_object.date() > datetime.today().date():
                print("Date of birth cannot be in the future.")
                continue

            return date_value

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")


def get_valid_score(prompt):
    while True:
        try:
            score = float(input(prompt))

            if 0 <= score <= 100:
                return score

            print("Score must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def add_student(students):
    print("\n========== REGISTER NEW STUDENT ==========")

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if find_student(students, student_id):
        print("A student with this ID already exists.")
        return

    full_name = input("Enter Full Name: ").strip()

    if not full_name:
        print("Full name cannot be empty.")
        return

    class_form = input("Enter Class/Form: ").strip()

    if not class_form:
        print("Class/Form cannot be empty.")
        return

    gender = input("Enter Gender: ").strip()

    if not gender:
        print("Gender cannot be empty.")
        return

    date_of_birth = get_valid_date("Enter Date of Birth (YYYY-MM-DD): ")

    student = Student(
        student_id,
        full_name,
        class_form,
        gender,
        date_of_birth
    )

    students.append(student)
    save_students(students)

    print("\nStudent registered successfully!")


def view_students(students):
    print("\n========== REGISTERED STUDENTS ==========")

    if not students:
        print("No students have been registered.")
        return

    print("-" * 75)
    print(f"{'ID':<15}{'NAME':<25}{'CLASS':<15}{'GENDER':<10}")
    print("-" * 75)

    for student in students:
        print(
            f"{student.student_id:<15}"
            f"{student.full_name:<25}"
            f"{student.class_form:<15}"
            f"{student.gender:<10}"
        )

    print("-" * 75)
    print(f"Total Students: {len(students)}")


def search_student(students):
    print("\n========== SEARCH STUDENT ==========")

    search_term = input("Enter Student ID or Name: ").strip().lower()

    if not search_term:
        print("Search field cannot be empty.")
        return

    matches = [
        student for student in students
        if search_term == student.student_id.lower()
        or search_term in student.full_name.lower()
    ]

    if not matches:
        print("No matching student found.")
        return

    for student in matches:
        print("\nStudent Information")
        print(f"Student ID: {student.student_id}")
        print(f"Full Name: {student.full_name}")
        print(f"Class/Form: {student.class_form}")
        print(f"Gender: {student.gender}")
        print(f"Date of Birth: {student.date_of_birth}")


def update_student(students):
    print("\n========== UPDATE STUDENT INFORMATION ==========")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep the existing information.")

    full_name = input(f"Full Name [{student.full_name}]: ").strip()
    class_form = input(f"Class/Form [{student.class_form}]: ").strip()
    gender = input(f"Gender [{student.gender}]: ").strip()

    while True:
        date_of_birth = input(
            f"Date of Birth [{student.date_of_birth}] (YYYY-MM-DD): "
        ).strip()

        if not date_of_birth:
            date_of_birth = student.date_of_birth
            break

        try:
            parsed_date = datetime.strptime(date_of_birth, "%Y-%m-%d")

            if parsed_date.date() > datetime.today().date():
                print("Date of birth cannot be in the future.")
                continue

            break

        except ValueError:
            print("Invalid date format.")

    student.update_information(
        full_name or student.full_name,
        class_form or student.class_form,
        gender or student.gender,
        date_of_birth
    )

    save_students(students)
    print("Student information updated successfully!")


def delete_student(students):
    print("\n========== DELETE STUDENT ==========")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    print(f"Student: {student.full_name}")

    confirmation = input(
        "Are you sure you want to delete this student? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        students.remove(student)
        save_students(students)
        print("Student record deleted successfully.")
    else:
        print("Deletion cancelled.")


def record_results(students):
    print("\n========== RECORD STUDENT RESULTS ==========")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    if student.scores:
        print("This student already has recorded results.")
        print("Use the Update Scores option to change existing scores.")
        return

    scores = {}

    print("\nEnter scores for five subjects.")

    for number in range(1, 6):
        while True:
            subject = input(f"Enter Subject {number} Name: ").strip()

            if not subject:
                print("Subject name cannot be empty.")
                continue

            if any(
                subject.lower() == existing.lower()
                for existing in scores
            ):
                print("This subject has already been entered.")
                continue

            break

        score = get_valid_score(f"Enter {subject} Score: ")
        scores[subject] = score

    student.record_scores(scores)
    save_students(students)

    print("\nResults recorded successfully!")
    print(f"Total Score: {calculate_total(scores):.2f}")
    print(f"Average Score: {calculate_average(scores):.2f}")
    print(f"Grade: {calculate_grade(calculate_average(scores))}")


def update_scores(students):
    print("\n========== UPDATE STUDENT SCORES ==========")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    if not student.scores:
        print("No results have been recorded for this student.")
        return

    print("\nExisting Subject Scores:")

    for subject, score in student.scores.items():
        print(f"{subject}: {score}")

    subject_name = input(
        "\nEnter the subject you want to update: "
    ).strip()

    matching_subject = next(
        (
            subject for subject in student.scores
            if subject.lower() == subject_name.lower()
        ),
        None
    )

    if not matching_subject:
        print("Subject not found.")
        return

    new_score = get_valid_score("Enter the new score: ")

    updated_scores = student.scores.copy()
    updated_scores[matching_subject] = new_score

    student.record_scores(updated_scores)
    save_students(students)

    print("\nScore updated successfully!")
    print(f"New Total: {calculate_total(student.scores):.2f}")
    print(f"New Average: {calculate_average(student.scores):.2f}")
    print(
        f"New Grade: "
        f"{calculate_grade(calculate_average(student.scores))}"
    )


def view_student_report(students):
    print("\n========== INDIVIDUAL REPORT CARD ==========")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    report = generate_student_report(student)
    print("\n" + report)

    save_choice = input(
        "\nSave this report to a text file? (yes/no): "
    ).strip().lower()

    if save_choice == "yes":
        filename = f"report_{student.student_id}.txt"

        try:
            path = save_report(filename, report)
            print(f"Report saved successfully: {path}")
        except OSError as error:
            print(f"Could not save report: {error}")


def view_all_results(students):
    print("\n" + generate_class_report(students))


def display_rankings(students):
    print("\n========== STUDENT RANKINGS ==========")

    ranked_students = sort_students(students, "average")

    if not ranked_students:
        print("No student results are available.")
        return

    print("-" * 65)
    print(f"{'POSITION':<12}{'STUDENT NAME':<25}{'AVERAGE':<15}{'GRADE'}")
    print("-" * 65)

    for position, student in enumerate(ranked_students, start=1):
        average = calculate_average(student.scores)
        grade = calculate_grade(average)

        print(
            f"{position:<12}"
            f"{student.full_name:<25}"
            f"{average:<15.2f}"
            f"{grade}"
        )

    print("-" * 65)


def display_alphabetical_list(students):
    print("\n========== STUDENTS SORTED BY NAME ==========")

    sorted_students = sort_students(students, "name")

    if not sorted_students:
        print("No students are registered.")
        return

    for number, student in enumerate(sorted_students, start=1):
        print(f"{number}. {student.full_name} ({student.student_id})")


def view_statistics(students):
    print(generate_class_statistics(students))


def save_class_report(students):
    report = generate_class_report(students)

    if report == "No student results are available.":
        print(report)
        return

    try:
        path = save_report("class_result_report.txt", report)
        print(f"Class report saved successfully: {path}")
    except OSError as error:
        print(f"Could not save report: {error}")


def display_menu():
    print("\n")
    print("=" * 55)
    print("       STUDENT RESULT SYSTEM")
    print("=" * 55)
    print("1.  Register New Student")
    print("2.  View All Students")
    print("3.  Search for Student")
    print("4.  Update Student Information")
    print("5.  Delete Student Record")
    print("6.  Record Student Results")
    print("7.  Update Student Scores")
    print("8.  View Individual Report Card")
    print("9.  View All Students' Results")
    print("10. Rank Students by Average")
    print("11. Sort Students by Name")
    print("12. View Class Statistics")
    print("13. Save Class Result Report")
    print("0.  Exit")
    print("=" * 55)


def main():
    students = load_students()

    print("\nWelcome to the Student Result Management System!")
    print(f"{len(students)} student record(s) loaded successfully.")

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_student(students)

            elif choice == "2":
                view_students(students)

            elif choice == "3":
                search_student(students)

            elif choice == "4":
                update_student(students)

            elif choice == "5":
                delete_student(students)

            elif choice == "6":
                record_results(students)

            elif choice == "7":
                update_scores(students)

            elif choice == "8":
                view_student_report(students)

            elif choice == "9":
                view_all_results(students)

            elif choice == "10":
                display_rankings(students)

            elif choice == "11":
                display_alphabetical_list(students)

            elif choice == "12":
                view_statistics(students)

            elif choice == "13":
                save_class_report(students)

            elif choice == "0":
                save_students(students)
                print("\nAll records saved successfully.")
                print("Thank you for using the Result System.")
                break

            else:
                print("Invalid choice. Please select an option from the menu.")

        except (OSError, ValueError, TypeError) as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
