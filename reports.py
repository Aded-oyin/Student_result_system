
from pathlib import Path
from results import (
    calculate_total,
    calculate_average,
    calculate_grade,
    get_grade_remark
)


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "generated_reports"


def generate_student_report(student):
    if not student.scores:
        return f"No results have been recorded for {student.full_name}."

    total = calculate_total(student.scores)
    average = calculate_average(student.scores)
    grade = calculate_grade(average)
    remark = get_grade_remark(grade)

    report = []
    report.append("=" * 55)
    report.append("           STUDENT REPORT CARD")
    report.append("=" * 55)
    report.append(f"Student ID: {student.student_id}")
    report.append(f"Full Name: {student.full_name}")
    report.append(f"Class/Form: {student.class_form}")
    report.append(f"Gender: {student.gender}")
    report.append(f"Date of Birth: {student.date_of_birth}")
    report.append("-" * 55)
    report.append("SUBJECT RESULTS")
    report.append("-" * 55)

    for subject, score in student.scores.items():
        report.append(f"{subject:<30} {score:>10.2f}")

    report.append("-" * 55)
    report.append(f"Total Score: {total:.2f}")
    report.append(f"Average Score: {average:.2f}")
    report.append(f"Grade: {grade}")
    report.append(f"Remark: {remark}")
    report.append(f"Result Date: {student.result_date}")
    report.append("=" * 55)

    return "\n".join(report)


def generate_class_report(students):
    report = []
    report.append("=" * 75)
    report.append("             CLASS RESULT REPORT")
    report.append("=" * 75)

    students_with_results = [
        student for student in students if student.scores
    ]

    if not students_with_results:
        return "No student results are available."

    sorted_students = sorted(
        students_with_results,
        key=lambda student: calculate_average(student.scores),
        reverse=True
    )

    report.append(
        f"{'Student ID':<15}{'Student Name':<25}"
        f"{'Total':<10}{'Average':<10}{'Grade':<8}"
    )
    report.append("-" * 75)

    for student in sorted_students:
        total = calculate_total(student.scores)
        average = calculate_average(student.scores)
        grade = calculate_grade(average)

        report.append(
            f"{student.student_id:<15}"
            f"{student.full_name:<25}"
            f"{total:<10.2f}"
            f"{average:<10.2f}"
            f"{grade:<8}"
        )

    report.append("=" * 75)

    return "\n".join(report)


def generate_class_statistics(students):
    students_with_results = [
        student for student in students if student.scores
    ]

    if not students_with_results:
        return "No student results are available for statistics."

    all_scores = [
        score
        for student in students_with_results
        for score in student.scores.values()
    ]

    class_average = sum(
        calculate_average(student.scores)
        for student in students_with_results
    ) / len(students_with_results)

    highest = max(all_scores)
    lowest = min(all_scores)

    return (
        "\n========== CLASS STATISTICS ==========\n"
        f"Total Registered Students: {len(students)}\n"
        f"Students With Results: {len(students_with_results)}\n"
        f"Highest Subject Score: {highest:.2f}\n"
        f"Lowest Subject Score: {lowest:.2f}\n"
        f"Class Average: {class_average:.2f}\n"
        "======================================"
    )


def sort_students(students, sort_by="average"):
    students_with_results = [
        student for student in students if student.scores
    ]

    if sort_by == "average":
        return sorted(
            students_with_results,
            key=lambda student: calculate_average(student.scores),
            reverse=True
        )

    elif sort_by == "name":
        return sorted(
            students,
            key=lambda student: student.full_name.lower()
        )

    return students


def save_report(filename, content):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = REPORT_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path
