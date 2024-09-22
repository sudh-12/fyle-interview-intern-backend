import pytest
import json
from tests import app

# Fixture to provide the Flask test client for sending simulated HTTP requests
@pytest.fixture
def client():
    return app.test_client()

# Fixture to simulate headers for Student 1
@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers

# Fixture to simulate headers for Student 2
@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers

# Fixture to simulate headers for Teacher 1
@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers

# Fixture to simulate headers for Teacher 2
@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers

# Fixture to simulate headers for the Principal
@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }
    
# Return the constructed headers
    return headers
