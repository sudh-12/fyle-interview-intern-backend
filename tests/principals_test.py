from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
from unittest.mock import patch

# Test for fetching assignments in SUBMITTED or GRADED state for the principal
def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

# Test for fetching the list of teachers for the principal
def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

# Test case where principal tries to grade an assignment in the DRAFT state
@patch('core.models.assignments.Assignment.query')
@patch('core.db.session.commit')
def test_grade_assignment_draft_assignment(mock_commit, mock_assignment, client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """

    assignment = Assignment()
    assignment.id = 5
    assignment.state = AssignmentStateEnum.DRAFT
    mock_assignment.get.return_value=assignment
    mock_commit.return_value = None
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value       # Trying to assign grade A to a draft assignment
        },
        headers=h_principal
    )

    assert response.status_code == 400
    
# Test case for grading a valid assignment by the principal
@patch('core.db.session.commit')
def test_grade_assignment(mock_commit, client, h_principal):

    mock_commit.return_value = None
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C

# Test case for re-grading an already graded assignment by the principal
@patch('core.db.session.commit')
def test_regrade_assignment(mock_commit, client, h_principal):

    mock_commit.return_value = None
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

# Test case for invalid grade assignment by the principal
@patch('core.db.session.commit')   
def test_grade_assignment_invalid_grade(mock_commit, client, h_principal):
    """Only valid grades are A,B,C,D"""

    mock_commit.return_value = None
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'CF'            # Invalid grade not part of GradeEnum
        },
        headers=h_principal
    )   

    assert response.status_code == 400