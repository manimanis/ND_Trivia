import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

QUESTIONS_PER_PAGE = 10

username = 'postgres'
password = 'abdou'
host = 'localhost'
port = 5432
database_name = "trivia"
database_path = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    """
    Question

    """
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    # def __init__(self, question, answer, category, difficulty):
    #     self.question = question
    #     self.answer = answer
    #     self.category = category
    #     self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

    def __repr__(self):
        return f'<Question\nid: {self.id}\nquestion: {self.question}\nanswer: {self.answer}\ncategory: {self.category}\ndifficulty: {self.difficulty}\n>'


class Category(db.Model):
    """
    Category

    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    # def __init__(self, type):
    #     self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }

    def __repr__(self):
        return f'<Category id: {self.id} - type: {self.type}>'


def format_list_items(items):
    """
    format all of the records in the list
    """
    return [item.format() for item in items]


def category_fetch_all():
    """Return all categories"""
    categories = Category.query.order_by(Category.type).all()
    categories_dict = {category.id: category.type for category in categories}
    return categories_dict


def questions_list_categories(questions):
    return list({question['category'] for question in questions})


def question_fetch_page(search_term=None, page=1, pagesize=QUESTIONS_PER_PAGE):
    """
    Return one 'page' of 'pagesize' elements
    """
    start = pagesize * (page - 1)
    end = start + pagesize
    if search_term is None:
        return Question.query.order_by(Question.id).slice(start, end).all()
    else:
        return (Question.query
                .filter(Question.question.ilike(f'%{search_term}%'))
                .order_by(Question.id)
                .slice(start, end)
                .all())


def question_count(search_term=None):
    """
    Return number of questions in total
    """
    if search_term is None:
        return Question.query.count()
    else:
        return (Question.query
                .filter(Question.question.ilike(f'%{search_term}%'))
                .count())


def question_fetch_page_by_category(categoty, page=1, pagesize=QUESTIONS_PER_PAGE):
    """
    Fetch questions by category
    """
    start = pagesize * (page - 1)
    end = start + pagesize
    return (Question.query
            .filter(Question.category == categoty)
            .order_by(Question.id)
            .slice(start, end)
            .all())


def question_count_by_category(category):
    """
    Return number of questions by category
    """
    return (Question.query
            .filter(Question.category == category)
            .count())