from core.models.assignments import Assignment, GradeEnum, AssignmentStateEnum
from unittest.mock import patch
from core import db

# Test for fetching assignments assigned to teacher 1
def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1

# Test for fetching assignments assigned to teacher 2
def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

# Test case where teacher 2 attempts to grade an assignment not assigned to them
@patch('core.db.session.commit')
def test_grade_assignment_cross(mock_commit, client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    mock_commit.return_value = None
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": GradeEnum.A.value    # Attempt to grade assignment 1
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'

# Test case for attempting to assign a grade not in the enum
@patch('core.db.session.commit')
def test_grade_assignment_bad_grade(mock_commit, client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    mock_commit.return_value = None
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"     # Invalid grade not part of GradeEnum
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'

# Test case where the teacher tries to grade a non-existent assignment
@patch('core.db.session.commit')
def test_grade_assignment_bad_assignment(mock_commit, client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    mock_commit.return_value = None
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,       # Non-existent assignment ID
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'

# Test case where a teacher attempts to grade an assignment that is still in draft
@patch('core.db.session.commit')
def test_grade_assignment_draft_assignment(mock_commit, client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    mock_commit.return_value = None

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,        # Assignment in 'DRAFT' state
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'

# Test case where a teacher attempts to grade an already graded assignment
@patch('core.models.assignments.Assignment.get_by_id')
@patch('core.db.session.commit')
def test_grade_assignment_by_teacher_my(mock_commit, mock_assignment, client, h_teacher_1):
    """
    can be failure case: an assignment can't be graded more than once by a teacher
    """
    # Create a mock assignment that is already graded
    assignment = Assignment()
    assignment.state = AssignmentStateEnum.GRADED
    assignment.content = "Test"
    assignment.grade = GradeEnum.A
    assignment.id = 7
    mock_assignment.return_value = assignment
    mock_commit.return_value = None

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 7,       # Already graded assignment ID
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Assignment is already graded'
