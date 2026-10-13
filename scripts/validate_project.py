#!/usr/bin/env python3
"""Validate notebook syntax and the scheduling input datasets."""

from pathlib import Path
import csv
import json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NOTEBOOKS = ROOT / "notebooks"


def rows(name: str) -> list[list[str]]:
    with (DATA / name).open(newline="", encoding="utf-8-sig") as handle:
        return [row for row in csv.reader(handle) if row]


def main() -> None:
    notebook_path = NOTEBOOKS / "exam-scheduler.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    for number, cell in enumerate(code_cells, start=1):
        compile("".join(cell["source"]), f"exam-scheduler.ipynb:cell-{number}", "exec")

    courses = rows("courses.csv")
    teachers = rows("teachers.csv")
    students = rows("students.csv")
    registrations = rows("student-courses.csv")
    if registrations and registrations[0][1:] == ["Student Name", "Course Code"]:
        registrations = registrations[1:]
    course_codes = {row[0] for row in courses}
    student_names = {row[0] for row in students}

    malformed = [row for row in registrations if len(row) < 3]
    unknown_students = sorted({row[1] for row in registrations if len(row) >= 3} - student_names)
    relevant_registrations = [row for row in registrations if len(row) >= 3 and row[2] in course_codes]
    if malformed or unknown_students or not relevant_registrations:
        raise SystemExit(
            "Dataset validation failed: "
            f"malformed={len(malformed)}, unknown_students={unknown_students}, "
            f"relevant_registrations={len(relevant_registrations)}"
        )

    print(
        f"Validated {len(code_cells)} code cell(s), {len(courses)} courses, "
        f"{len(teachers)} teachers, {len(students)} students, and "
        f"{len(relevant_registrations)} relevant registrations."
    )


if __name__ == "__main__":
    main()
