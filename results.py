
# Tuple containing grade boundaries and their corresponding grades
GRADE_SCALE = (
    (70, "A"),
    (60, "B"),
    (50, "C"),
    (45, "D"),
    (0, "F")
)


def calculate_total(scores):
    return sum(scores.values())


def calculate_average(scores):
    if not scores:
        return 0

    return calculate_total(scores) / len(scores)


def calculate_grade(average):
    for minimum_score, grade in GRADE_SCALE:
        if average >= minimum_score:
            return grade

    return "F"


def get_grade_remark(grade):
    remarks = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Pass",
        "F": "Fail"
    }

    return remarks.get(grade, "Not Available")
