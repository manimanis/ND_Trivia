# Full Stack Trivia API Backend

## Getting Started

This project consists of a light-weight backend to the Trivia game. It includes, also, a very minimalistic frontend 
provided for test purpose, only. It is a part of the Fullstack Nanodegree offered by [Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).
Its a practice project for __API Development and Documentation__ lesson.  

### Installing Dependencies

As I am working on Windows 10, I will provide instructions relative to this OS only. 

#### Python 3.7

First install the latest version of python (version 3.7.x is used to develop this backend) from here: [Python Website](https://www.python.org/)

#### Virtual Environment

After __cloning__ this repo, you will need to create a virtual environment.

```
cd [project base directory]
virtualenv env
env\Scripts\activate.bat
```

This will create a new directory called `env` containing a fresh copy of Python containing the basic packages. And, in 
order to work with this copy of python you have to activate it. This step will assure that all the installed packages
will be installed only for this project.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` 
directory and running:

```
cd backend
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

The project is powered by __PosgreSQL__. A set of questions is provided in the file `trivia.psql`. 
In order to setup the database, you have to create it, than load the `trivia.psql`:

```
createdb -U postgres trivia
psql -U postgres trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.
To run the server, execute for Windows platform:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Frontend

Change to the `frontend` folder, install dependencies, than start the development server of the frontend: 

```
cd ..\frontend
npm install
npm start 
```

By default, the frontend will run on localhost:3000. 

## Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
createdb -U posgresql trivia_test
psql -U posgresql trivia_test < trivia.psql
python test_flaskr.py
``` 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started

- __Base URL:__ At present this app can only be run locally and is not hosted as a base URL. 
  The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the 
  frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:

```json
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```

The API will return four errors types when requests fail:
- 400: Bad request
- 404: Not Found
- 405: Not Allowed
- 422: Unprocessable entity

### Endpoints
#### GET /categories
- General:
    - Returns:
        - __categories__: A dictionary of all categories of questions
        - __success__: true
- Example: `curl http://127.0.0.1:5000/categories`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
#### GET /questions[?page=num_page]
- General:
    - Returns:
        - __categories__: a list of all available categories.
        - __current_category__: the respective `id`s of categories of questions being fetched
        - __question__: a list of questions (10 max) of page `page`   
        - __total_questions__: the total number of questions
        - __success__: true
- Example: `curl http://127.0.0.1:5000/questions`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": [
    3,
    4,
    5,
    6
  ],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```
#### POST /questions
- General:
    - Used to insert a new question, if the user post the following information:
```json5
{
  "question": "Your question",
  "answer": "The answer",
  "difficulty": 1,              // the difficulty ranging from 1 to 5
  "category": 1                 // the id of the category
}
```

    - Used for a question containing a term, search is case insensitive:

```json5
{
  "searchTerm": "clay" 
}
```
- Example 1: 
__command__
```
curl -X POST -d "{\"question\":\"What is the color of the sky in the morning?\",\"answer\":\"blue\",\"category\":\"1\",\"
difficulty\":\"1\"}" -H "Content-Type: application/json" http://127.0.0.1:5000/questions
```
__response__
```json
{
  "created": 27,
  "success": true
}
```
- Example 2:
__command__
```
curl -X POST -d "{\"searchTerm\":\"clay\"}" -H "Content-Type: application/json" http://127.0.0.1:5000/questions
```
__response__
```json5
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### DELETE /questions/<question_id>
- General:
    - Used to delete permanently `question_id`
- Example:
__command__
```
curl -X DELETE http://127.0.0.1:5000/questions/27
```
__response__
```json5
{
  "deleted": 27,
  "success": true
}
```

#### GET /categories/<category_id>/questions[?page=num_page]

- General:
    - Return questions page (of max 10 questions) for the given category
- Example:
__command__
```
curl  http://127.0.0.1:5000/categories/1/questions
```
__response__
```json5
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Blue",
      "category": 1,
      "difficulty": 1,
      "id": 25,
      "question": "What's the color of the Sky in the morning?"
    },
    {
      "answer": "180",
      "category": 1,
      "difficulty": 1,
      "id": 26,
      "question": "What the sum of a triangle angles in degrees?"
    }
  ],
  "success": true,
  "total_questions": 5
}
```

#### POST /quizzes

- General: Play trivia game. This request trigger a question.
    - We should send the previous played questions and the chosen category
```json5
{
  "previous_questions": [12, 23],   // the id of the previous played questions
  "quiz_category": {                // the category chosen
    "type": "History", 
    "id": "4"
  }
}
```  
- Example:
__command__
```
curl "http://127.0.0.1:5000/quizzes" -X POST -H "Content-Type: application/json" -d "{\"previous_questions\":[12,23],\"quiz_category\":{\"type\":\"History\",\"id\":\"4\"}}"
```
__response__
```json5
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
```

## Authors
- Coach Caryn (Project Skeleton)
- Mohamed Anis MANI

## Acknowledgements 
- Coach Caryn
- The awesome team at Udacity and all of the students, soon to be full stack extraordinaires! 
