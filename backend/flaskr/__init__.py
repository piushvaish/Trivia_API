import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
'''
References:
https://github.com/cmccarthy15/Workshop_Exercise
https://www.youtube.com/watch?v=cR_FqveTewo
https://gist.github.com/mogproject/fc7c4e94ba505e95fa03
https://knowledge.udacity.com/questions/82978
https://knowledge.udacity.com/questions/83465
https://nodejs.org/api/errors.html#errors_common_system_errors
'''

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [que.format() for que in selection]
  current_ques = questions[start:end]
  return current_ques

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)  
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''

  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories' , methods=['GET'])
  def retrieve_categories():
    categories = Category.query.all()
    category_format = {category.id: category.type for category in categories}
    if len(category_format) == 0:
      abort(404)
    return jsonify({
      'success' : True,
      'categories': category_format,
      'total_categories': len(category_format)
    }), 200


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.   

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    category_format = {category.id: category.type for category in categories}
    current_questions = paginate_questions(request, questions)
    if len(current_questions) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': category_format,
      'current_category': list(set([question['category'] for question in current_questions])),
    }), 200


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      try:
          question = Question.query.filter(Question.id == question_id)\
            .one_or_none()
          if question is None:
              abort(404)
          else:
              question.delete()
              selection = Question.query.order_by(Question.id).all()
              current_questions = paginate_questions(request, selection)
          return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
          }), 200
      except Exception:
          abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)      
      if ((new_question == '') or (new_answer == '') or (new_difficulty == '') or (new_category == '')):
        abort(422)
      try:
          question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
          question.insert()
          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)
          return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'message': 'Question successfully created!'
          }), 200
      except Exception:
            abort(400)

  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def questions_search():    
    # Get search term from request data
    search_term = request.get_json().get('searchTerm', '')

    # Return 422 status code if empty search term is sent
    if search_term == '':
        abort(422)

    try:
        # get all questions that has the search term substring
        questions = Question.query.filter(Question.question.ilike("%{}%".format(search_term))).all()

        # if there are no questions for search term return 404
        if len(questions) == 0:
            abort(404)

        # paginate questions
        paginated_questions = paginate_questions(request, questions)

        # return response if successful
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(Question.query.all()),
            'current_category': None
        }), 200

    except Exception:
        # This error code is returned when 404 abort
        # raises exception from try block
        abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def questions_by_category(category_id):
      try:
          questions = Question.query.filter_by(category=str(category_id)).all()
          current_questions = paginate_questions(request, questions)
          if len(current_questions) == 0:
              abort(404)
          return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions)
          }), 200
      except Exception:
          abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    try:
      data = request.get_json()
      previous_questions = data['previous_questions']
      quiz_category = data['quiz_category']
      if ((quiz_category is None) or (previous_questions is None)):
          abort(400)
      questions = None
      if (quiz_category['id'] != 0):
          questions = Question.query.filter_by(category=quiz_category['id']).all()
      questions_format = [question.format() for question in questions]
      potential_questions = [
        que
        for que in questions_format
        if que['id'] not in previous_questions
      ]
      selected_question = None
      if len(potential_questions) > 0:
          selected_question = random.choice(potential_questions)
      return jsonify({
          'success': True,
          'question': selected_question
        }), 200
    except Exception:
      abort(500)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
      }), 404  

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'An error has occured, please try again'
      }), 500

  return app

    