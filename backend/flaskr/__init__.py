import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

from models import category_fetch_all, format_list_items, question_fetch_page, question_count, questions_list_categories
from models import question_fetch_page_by_category, question_count_by_category
import random

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        """
        Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
        Use the after_request decorator to set Access-Control-Allow
        """
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authentication, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        """
        Return all available categories.
        """
        categories = category_fetch_all()
        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/questions')
    def get_questions():
        """
        Return a list of questions (max 10 questions per page),
        number of total questions, current category, categories.
        """
        page = request.args.get('page', 1, type=int)
        q_count = question_count()
        num_pages = q_count // QUESTIONS_PER_PAGE + (1 if q_count % QUESTIONS_PER_PAGE > 0 else 0)
        if 1 > page or page > num_pages:
            abort(404)
        questions = format_list_items(question_fetch_page(page=page))
        categories = questions_list_categories(questions)
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': q_count,
            'current_category': categories,
            'categories': category_fetch_all()
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        DELETE question using a question ID.
        """
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(400)

    @app.route('/questions', methods=['POST'])
    def insert_question():
        """
        This endpoint is used to:
        - Add a new question: requires the question and answer text, category, and difficulty score.
        - Search for questions (max 10 per page) for whom the search term is a substring of the question.
        """
        data = request.get_json()
        if 'searchTerm' in data:
            # This is a search request
            page = request.args.get('page', 1, type=int)
            search_term = data.get('searchTerm', '')
            q_count = question_count(search_term)
            num_pages = q_count // QUESTIONS_PER_PAGE + (1 if q_count % QUESTIONS_PER_PAGE > 0 else 0)
            if 1 > page or page > num_pages:
                abort(404)
            questions = format_list_items(question_fetch_page(search_term=search_term, page=page))
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': q_count,
                'categories': category_fetch_all()
            })
        else:
            fields_names = ['question', 'answer', 'difficulty', 'category']
            if all((field in data) for field in fields_names):
                # We want to insert a new question
                question = Question(question=data.get('question', ''),
                                    answer=data.get('answer', ''),
                                    difficulty=int(data.get('difficulty', 1)),
                                    category=int(data.get('category', 1)))
                try:
                    question.insert()
                    return jsonify({
                        'success': True,
                        'created': question.id
                    })
                except:
                    abort(422)
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Get questions (max 10 per page) based on category.
        """
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        questions = question_fetch_page_by_category(category_id)
        q_count = question_count_by_category(category_id)
        return jsonify({
            'success': True,
            'questions': format_list_items(questions),
            'total_questions': q_count,
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """
        Get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        """
        data = request.get_json()
        fields_names = ['previous_questions', 'quiz_category']
        if not all(field in data for field in fields_names):
            abort(400)
        if 'id' not in data['quiz_category']:
            abort(400)
        category_id = int(data['quiz_category']['id'])
        if category_id != 0:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)
            questions = Question.query.filter(Question.category == category_id).all()
        else:
            questions = Question.query.all()
        candidates = [question for question in questions if question.id not in data['previous_questions']]
        if len(candidates) > 0:
            question = random.choice(candidates)
            return jsonify({
                'success': True,
                'question': question.format()
            })
        else:
            return jsonify({
                'success': True,
                'question': None
            })

    # '''
    # Errors handlers for all expected errors
    # including 400, 404, 405 and 422.
    # '''
    @app.errorhandler(400)
    def error_bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def error_not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Not Allowed'
        }), 405

    @app.errorhandler(422)
    def error_not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    return app
