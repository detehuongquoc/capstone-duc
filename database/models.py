import os
from sqlalchemy import Column, String, Integer, Date, Text, Float
from flask_sqlalchemy import SQLAlchemy
from decouple import config

database_url = config('DATABASE_PATH')
db = SQLAlchemy()

movies_actors = db.Table('movies_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


def db_drop_and_create_all(app):
    with app.app_context():
        db.drop_all()
        db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String(100), nullable=True)
    director = Column(String(255), nullable=True)
    poster_image = Column(String(255), nullable=True)
    average_rating = Column(Float, nullable=True)

    actors = db.relationship('Actor', secondary=movies_actors, backref='movies', lazy=True)


    def __init__(self, title, release_date, description=None, genre=None, director=None, poster_image=None, average_rating=None):
        self.title = title
        self.release_date = release_date
        self.description = description
        self.genre = genre
        self.director = director
        self.poster_image = poster_image
        self.average_rating = average_rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "title": self.title
        }

    def long(self):
        return {
            "title": self.title,
            "release_date": self.release_date.strftime("%B %d, %Y"),
            "description": self.description,
            "genre": self.genre,
            "director": self.director,
            "poster_image": self.poster_image,
            "average_rating": self.average_rating
        }

    def full_info(self):
        return {
            "title": self.title,
            "release_date": self.release_date.strftime("%B %d, %Y"),
            "description": self.description,
            "genre": self.genre,
            "director": self.director,
            "poster_image": self.poster_image,
            "average_rating": self.average_rating,
            "actors": [actor.name for actor in self.actors]
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    bio = Column(Text, nullable=True)
    nationality = Column(String(100), nullable=True)
    profile_image = Column(String(255), nullable=True)

    def __init__(self, name, age, gender, bio=None, nationality=None, profile_image=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.bio = bio
        self.nationality = nationality
        self.profile_image = profile_image

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "bio": self.bio,
            "nationality": self.nationality,
            "profile_image": self.profile_image
        }

    def full_info(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "bio": self.bio,
            "nationality": self.nationality,
            "profile_image": self.profile_image,
            "movies": [movie.title for movie in self.movies]
        }
