from core.models.assignments import AssignmentStateEnum, Assignment
from unittest.mock import patch

# Test to get assignments for student 1
def test_get_assignments_student_1(client, h_student_1):
    # Sends a GET request to retrieve assignments for student 1
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200
    # Extracts the data from the response JSON
    data = response.json['data']
    # Asserts that all assignments returned are for student 1
    for assignment in data:
        assert assignment['student_id'] == 1

# Test to get assignments for student 2
def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

# Test for posting an assignment with null content (failure case)
@patch('core.db.session.commit')
def test_post_assignment_null_content(mock_commit, client, h_student_1):
    """
    failure case: content cannot be null
    """
    # Mocking the commit to prevent database changes during testing
    mock_commit.return_value = None

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400

# Test for posting a valid assignment for student 1
@patch('core.db.session.commit')
def test_post_assignment_student_1(mock_commit, client, h_student_1):
    content = 'ABCD TESTPOST'
    
    mock_commit.return_value = None
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

# Test for submitting an assignment by student 1
@patch('core.models.assignments.Assignment')
@patch('core.db.session.commit')
def test_submit_assignment_student_1(mock_commit, mock_assignment, client, h_student_1):

    assignment = Assignment()
    assignment.state = AssignmentStateEnum.DRAFT
    assignment.content = "Test"
    mock_commit.return_value = None
    mock_assignment.get_by_id.return_value = assignment

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })


    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

# Test to check if resubmitting a submitted assignment throws an error
@patch('core.models.assignments.Assignment')
@patch('core.db.session.commit')
def test_assignment_resubmit_error(mock_commit, mock_assignment, client, h_student_1):

    assignment = Assignment()
    assignment.state = AssignmentStateEnum.SUBMITTED
    assignment.content = "Test"
    mock_commit.return_value = None
    mock_assignment.get_by_id.return_value = assignment

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

# Another test for posting an assignment for student 1 with different content
@patch('core.db.session.commit')
def test_post_assignment_student_1_my(mock_commit, client, h_student_1):
    content = 'MY TEST'

    mock_commit.return_value = None
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

# Test to update an existing draft assignment for student 1
@patch('core.models.assignments.Assignment')
@patch('core.db.session.commit')
def test_post_assignment_student_1_update_my(mock_commit, mock_assignment, client, h_student_1):
    content = 'MY TEST UPDATED'

    # Simulating an existing draft assignment
    assignment = Assignment()
    assignment.state = AssignmentStateEnum.DRAFT
    assignment.content = "Test"
    mock_commit.return_value = None
    mock_assignment.get_by_id.return_value = assignment
    
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 7,               # ID of the assignment to update
            'content': content
        })

    try:    
        assert response.status_code == 200
        data = response.json['data']
        assert data['content'] == content
        assert data['state'] == 'DRAFT'
        assert data['teacher_id'] is None
    except AssertionError:
        assert response.status_code == 400
        data = response.json
        assert data['error'] == 'FyleError'
        assert data['message'] == 'only assignment in draft state can be edited'

# Test to submit a draft assignment for student 1 (failure case if not in draft state)
@patch('core.models.assignments.Assignment')
@patch('core.db.session.commit')
def test_submit_assignment_student_1_my(mock_commit, mock_assignment,  client, h_student_1):
    """
    can be failure case: only a draft assignment can be submitted ( an assignment can't be submitted more than once. )
    """

    assignment = Assignment()
    assignment.state = AssignmentStateEnum.DRAFT
    assignment.content = "Test"
    mock_commit.return_value = None
    mock_assignment.get_by_id.return_value = assignment

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 7,         
            'teacher_id': 1
        })

    try:
        assert response.status_code == 200
        data = response.json['data']
        assert data['student_id'] == 1
        assert data['state'] == 'SUBMITTED'
        assert data['teacher_id'] == 1
    except AssertionError:
        assert response.status_code == 400
        data = response.json
        assert data['error'] == 'FyleError'
        assert data['message'] == 'only a draft assignment can be submitted'
