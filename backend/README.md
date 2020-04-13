# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.5

We recommend working with a python version which is less than 3.8 because SQLAlchemy doesnot support python version 3.8. 

#### Anaconda Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. This project is using windows operating system. 

* Create a conda environment with python version 3.5
```
conda create env --name py35 python=3.5
```
* To activate the environment
```
conda activate py35
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided.  From the backend folder in terminal run:
```
psql -U postgres
create database trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment. 

To run the server, execute:

```Anaconda Prompt (Windows Environment)
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
```
CORS(app, resources={r"/api/*": {"origins": "*"}})

response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')

response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
```
API is organized around REST with resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes and verbs.

Endpoints 
* GET '/categories' 
* GET '/questions' 
* POST '/questions' 
* DELETE '/questions/int:question_id' 
* POST '/questions/search' 
* GET '/categories/int:category_id/questions' 
* POST '/quizzes'

GET '/categories'

* Handle GET requests for all available categories
* Arguments: None
* Returns: category_string key:value pairs, total_categories
``` Response
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
GET '/questions'

* Handle GET requests for questions, including pagination (every 10 questions)
* Arguments: None
* Returns: return a list of questions, 
  number of total questions, current category, categories.
``` Response
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
    2,
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
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 17
}
```
DELETE '/questions/int:question_id'
* DELETE question using a question ID
* Arguments: int:question_id
* Returns: If successfully deleted lists questionid of deleted question, remaining questions and total numbers of questions and message of success. If resource not found returns 404.

``` Response
{
  "deleted": 5,
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
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "total_questions": 15
}
```


``` Response
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false
}
```
POST '/questions'
* POST a new question, which will require the question and answer text, 
  category, and difficulty score.
* Arguments: Question, answer, category, difficulty
Returns a new question to the database
``` Response
{
    "questions": {
    "question": "What is Coronavirus?",
    "answer": "Respitory Virus",
    "difficulty": 1,
    "category": 1
    },
    "status": 200,
    "success": true
    }
```

POST '/questions/search'

* POST endpoint to get questions based on a search term
* Argument: Takes searchTerm
* Returns any questions for whom the search term is a substring of the question
```
{
        "searchTerm": ""actor
    }    
    }
    {
        "current_category": null,
        "questions" : [
            {
                "answer": "Yes",
                "category": null,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }
        ],
        "success": true,
        "total_questions": 1     
    }
```

GET '/categories/int:category_id/questions'

* GET questions based on category
* Parameter: int:category_id
* Returns: questions, category id
```
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
      "answer": "Respiratory Virus",
      "category": 1,
      "difficulty": 1,
      "id": 77,
      "question": "What is Corona Virus?"
    },
    {
      "answer": "Satelite",
      "category": 1,
      "difficulty": 1,
      "id": 78,
      "question": "what is moon"
    }
  ],
  "total_questions": 5
}
```
POST '/quizzes'

* POST endpoint to get questions to play the quiz. It take category and previous question parameters   and return a random questions within the given category, if provided, and that is not one of the previous questions
* Arguments : None
* Returns: Questions for that category

  ``` Response
    {
        "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 10,
        "question": "What is the largest lake in Africa?"
    },
    "success": true
  ```
    ## Errors

    ### Bad Request: 400
    ```
    "success": False,
    "error": 400,
    "message": "Bad Request"
    ```

    ### Not Found: 404
    ```
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
    ```
    ### Unprocessable request: 422
    ```
    "success": False,
    "error": 422,
    "message": "Unprocessable"
    ```
    ### Internal Server Error: 500
    ```
    "success": False,
    "error": 500,
    "message": "An error has occured, please try again"
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```