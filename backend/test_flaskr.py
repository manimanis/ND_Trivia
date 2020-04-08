import os
import random
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
import logging

QUESTIONS_PER_PAGE = 10

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        username = 'postgres'
        password = 'abdou'
        host = 'localhost'
        port = 5432
        database_name = "trivia_test"
        self.database_path = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # """
    # TODO
    # Write at least one test for each test for successful operation and for expected errors.
    # """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue('categories' in data)
        self.assertGreater(len(data['categories']), 0)

    def test_get_questions_page1(self):
        q_count = Question.query.count()
        c_count = Category.query.count()
        res = self.client().get('/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(data['total_questions'], q_count)
        self.assertEqual(len(data['categories']), c_count)

    def test_get_questions_last_page(self):
        q_count = Question.query.count()
        q_count_last = q_count % QUESTIONS_PER_PAGE
        page_num = q_count // QUESTIONS_PER_PAGE + (1 if q_count_last > 0 else 0)
        res = self.client().get(f'/questions?page={page_num}')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), q_count_last if q_count_last > 0 else QUESTIONS_PER_PAGE)

    def test_get_questions_inexistant_page(self):
        q_count = Question.query.count()
        page_num = q_count // QUESTIONS_PER_PAGE + 10
        res = self.client().get(f'/questions?page={page_num}')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        question = Question.query.order_by(Question.id).first()
        new_question = Question(question=question.question,
                                answer=question.answer,
                                category=question.category,
                                difficulty=question.difficulty)
        new_question.insert()
        nq_id = question.id
        res = self.client().delete(f'/questions/{nq_id}')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], nq_id)
        old_question = Question.query.get(nq_id)
        self.assertIsNone(old_question)

    def test_delete_inexistant_question(self):
        question = Question.query.order_by(Question.id).first()
        question_id = question.id - 1  # there is no question with this id
        res = self.client().delete(f'/questions/{question_id}')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_insert_question(self):
        question = Question.query.order_by(Question.id).first()
        new_question = question.format()
        del new_question['id']
        old_questions_count = Question.query.count()
        res = self.client().post('/questions', json=new_question)
        new_questions_count = Question.query.count()
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertNotEqual(data['created'], 0)
        self.assertEqual(new_questions_count, old_questions_count+1)
        question = Question.query.get(data['created'])
        question.delete()

    def test_search_by_term(self):
        # Select random question
        question = random.choice(Question.query.all())
        # split the sentence to words
        terms = set(question.question.split())
        for term in terms:
            rc = Question.query.filter(Question.question.ilike(f'%{term}%')).count()
            res = self.client().post('/questions', json={'searchTerm': term})
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['total_questions'], rc, f'There are {rc} records containing the word {term} your back end returned {data["total_questions"]}')
            self.assertEqual(len(data['questions']), min(QUESTIONS_PER_PAGE, rc))

    def test_questions_by_category(self):
        # select categories_count <= 10 random categories
        categories_count = min(Category.query.count(), QUESTIONS_PER_PAGE)
        categories = random.choices(Category.query.all(), k=categories_count)
        categories_id = [category.id for category in categories]
        for category_id in categories_id:
            qc = Question.query.filter(Question.category == category_id).count()
            res = self.client().get(f'/categories/{category_id}/questions')
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['total_questions'], qc,
                             f'There are {qc} records in the category {categories_id} your back end returned {data["total_questions"]}')
            self.assertEqual(len(data['questions']), min(QUESTIONS_PER_PAGE, qc))
            self.assertEqual(data['current_category'], category_id)

    def test_questions_by_inexistant_category(self):
        category = Category.query.order_by(Category.id).first()
        category_id = category.id - 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_play_quiz_all_questions(self):
        questions_count = Question.query.count()
        previous_questions = []
        quiz_category = {'id': 0, 'type': 'click'}
        while True:
            data = {
                'previous_questions': previous_questions,
                'quiz_category': quiz_category
            }
            res = self.client().post('/quizzes', json=data)
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            if data['question'] is None:
                self.assertEqual(questions_count, 0)
                break
            questions_count -= 1
            self.assertNotIn(data['question']['id'], previous_questions)
            previous_questions.append(data['question']['id'])

    def test_play_quiz_one_category(self):
        # Select a random catageory
        category = random.choice(Category.query.all())
        quiz_category = category.format()
        questions_count = Question.query.filter(Question.category == quiz_category['id']).count()
        previous_questions = []
        while True:
            data = {
                'previous_questions': previous_questions,
                'quiz_category': quiz_category
            }
            res = self.client().post('/quizzes', json=data)
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            if data['question'] is None:
                self.assertEqual(questions_count, 0)
                break
            questions_count -= 1
            self.assertNotIn(data['question']['id'], previous_questions)
            previous_questions.append(data['question']['id'])

    def test_play_quiz_missing_request(self):
        # querying with missing data
        data = {}
        res = self.client().post('/quizzes', json=data)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        # missing quiz_category
        data = {'previous_questions': []}
        res = self.client().post('/quizzes', json=data)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        # missing quiz_category['id']
        data = {'previous_questions': [], 'quiz_category': {}}
        res = self.client().post('/quizzes', json=data)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)

    def test_play_quiz_invalid_category(self):
        # calculating an invalid category_id
        category = Category.query.order_by(self.db.desc(Category.id)).first()
        category_id = category.id + 1
        data = {
            'previous_questions': [],
            'quiz_category': {'id': category_id, 'type': 'dummy_type'}
        }
        res = self.client().post('/quizzes', json=data)
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()