# ASSIGNMENT COMPLETED

Successfully completed the assignment received by FYLE for Backend Intern position, with a Test coverage of 96 % and all test cases passing on it (SCREENSHOT is Attached below). 
- Added missing APIs mentioned in the challenge and passed the automated test.
- Added tests for grading API.
- Resolved Bugs Present in the application.
- Wrote SQL queries in the file given.
- Dockerized the application by creating a Dockerfile and a docker-compose.yml file.

### Steps to run docker-compose 

```bash
# Navigate to project directory : 
  cd fyle-interview-intern-backend
# Check if docker compose is installed , or install it
  #on linux
  sudo apt-get install docker-compose
# Confirm by checking the version
  docker-compose --version
# Run docker file
  docker-compose up

# Check on localhost:7755 if Application is running 
  Response : {"status":"ready","time":"Sun, 22 Sep 2024 16:11:36 GMT"}
```


**Screenshot of the TEST COVERAGE reaching 96 %.**
![Screenshot (205)](https://github.com/user-attachments/assets/05d55c25-b6e2-4b2f-aa39-1402efbf237e)


**Screenshot of the ALL TEST PASSING.**
![Screenshot (206)](https://github.com/user-attachments/assets/cc07c400-a1a4-45f1-ba85-9a5a43c9ba6f)

## Challenges Faced

During the development of this assignment, I encountered several challenges, including:

- **Bug Fixes:** Identified and resolved various bugs that improved application stability.
- **API Integration:** Added missing APIs to ensure full functionality
- **Dockerization:** Dockerized the application to streamline deployment and improve consistency across environments.
- **Running code on windows env:** I faced multiple challenges to start the application on windows as all commands mentioned was of linux environment, I installed docker and created 
                                   linux env inside docker container which helped me to set it up easily.
- **Mock Unit Testing:** While fixing unit tests, I saw that multiple tests were writing/reading the data from database, which should not be the case of unit testing. I moved towards 
                         mocking the relevant function and classes to ensure unit tests works properly in all the scenarios.


## Regards

I would like to express my sincere gratitude for the opportunity to work on this assignment. It was a valuable experience. I look forward to your feedback and hope to hear from you soon regarding the next steps.

## Installation

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```
