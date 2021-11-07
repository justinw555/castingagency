import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "castingagency"
#database_path = "postgresql://{}/{}".format('postgres:secret@localhost:5432', database_name)
# for Heroku
database_path = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.drop_all()
  db.create_all()

def db_drop_and_create_all():
  db.drop_all()
  db.create_all()
  actor1 = Actor(
    name='Test Actor1',
    age=10,
    gender='Male'
  )
  actor2 = Actor(
    name='Test Actor2',
    age=20,
    gender='Female'
  )
  actor3 = Actor(
    name='Test Actor3',
    age=30,
    gender='Male'
  )
  movie1 = Movie(
    title='Test Movie1',
    releasedate='2022-01-31'
  )
  movie2 = Movie(
    title='Test Movie2',
    releasedate='2023-01-31'
  )
  movie3 = Movie(
    title='Test Movie3',
    releasedate='2024-01-31'
  )
  db.session.add(actor1)
  db.session.add(actor2)
  db.session.add(actor3)
  db.session.add(movie1)
  db.session.add(movie2)
  db.session.add(movie3)
  db.session.commit()
 

#Movies with attributes: title and release date

class Movie(db.Model):
  __tablename__ = 'movies'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), nullable = False)
  releasedate = db.Column(db.Date, nullable=False) 
  #actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)



#Actors with attributes: name, age and gender

class Actor(db.Model):
  __tablename__ = 'actors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable = False)
  age = db.Column(db.Integer, nullable = False)
  gender = db.Column(db.String(), nullable=False) #db.CheckConstraint('gender == "male"' or 'gender == "female"', nullable = False))
  #movie_with_actors = db.relationship('Movie',backref = 'some_actor',lazy='joined')
