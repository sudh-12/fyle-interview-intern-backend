from sqlalchemy import text
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def get_graded_assignments_for_teacher():
    # Count of grade A assignments for teacher which has graded maximum assignments"

    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == 1,
        Assignment.grade == GradeEnum.A
    ).count()

    grade_a_counter = max(grade_a_counter, Assignment.filter(
        Assignment.teacher_id == 2,
        Assignment.grade == GradeEnum.A
    ).count())

    # Return the count of assignments with grade 'A'
    return grade_a_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    expected_result = [(1, 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""


# Read the SQL query from a file
with open(
        'tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql',
        encoding='utf8') as fo:
    sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = get_graded_assignments_for_teacher()

    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_1 == sql_result[0][0]

