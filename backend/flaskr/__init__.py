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

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

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

  @app.route('/questions', methods=['POST'])
  def create_question():
      new_question = request.get_json().get('question', None)
      new_answer = request.get_json().get('answer', None)
      new_category = request.get_json().get('category', None)
      new_difficulty = request.get_json().get('difficulty', None)      
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
          }), 200
      except Exception:
            abort(400)
 
  
  @app.route('/questions/search', methods=['POST'])
  def questions_search():    
    search_term = request.get_json().get('searchTerm', '')
    if search_term == '':
        abort(422)
    try:
        questions = Question.query.filter(Question.question.ilike("%{}%".format(search_term))).all()
        if len(questions) == 0:
            abort(404)
        paginated_questions = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(Question.query.all()),
            'current_category': None
        }), 200
    except Exception:
        abort(404)

  
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_by_category(category_id):
      try:
          questions = Question.query.filter_by(category = category_id).all()
          questions_format = [question.format() for question in questions]
          if len(questions_format) == 0:
            abort(404)
          
          return jsonify({
            'questions': questions_format,
            'total_questions': len(questions_format),
            'current_category': category_id
          })
      except Exception:
          abort(422)

  
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    try:
      data = request.get_json()
      previous_questions = data['previous_questions']
      quiz_category = data['quiz_category']
      if ((quiz_category is None) or (previous_questions is None)):
          abort(400)
      questions = None
      if (quiz_category['id'] == 0):
          questions = Question.query.order_by(Question.id).all()
      else:
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

  # Error Handling

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
          'message': "An error has occured, please try again"
      }), 500

  return app

    