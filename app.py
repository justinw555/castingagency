import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
import json
from sqlalchemy.sql import func

from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth

loginURL = os.environ.get('loginURL')
#loginURL = 'https://dev-o1fi8lp1.us.auth0.com/authorize?audience=castingagency3&response_type=token&client_id=v0a4a71Z9XNdFCpm6F165pqrerbs83a1&redirect_uri=http://0.0.0.0:8080/landing'

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    return response

  #GET /actors 
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def retrieve_actors(payload):
    try:
      all_actors = Actor.query.order_by(Actor.id).all()
      
      actorsList = []
      for some_actor in all_actors:
        addData = {}
        addData["id"] = some_actor.id
        addData["name"] = some_actor.name
        addData["age"] = some_actor.age
        addData["gender"] = some_actor.gender
        actorsList.append(addData)

      return jsonify({
        'success': True,
        'actors': actorsList
      })
    except Exception as e:
      app.logger.error(e)
      abort(404)

  #GET /movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def retrieve_movies(payload):
    try:
      
      all_movies = Movie.query.order_by(Movie.id).all()
      
      moviesList = []
      for some_movie in all_movies:
        addData = {}
        addData["id"] = some_movie.id
        addData["title"] = some_movie.title
        addData["releasedate"] = some_movie.releasedate
        moviesList.append(addData)

      return jsonify({
        'success': True,
        'movies': moviesList
      })
    except Exception as e:
      
      app.logger.error(e)
      abort(404)

  #DELETE /actors/ 
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      db.session.delete(actor)
      db.session.commit()
        
      return jsonify({
        'success': True,
        'deleted': actor_id
      })

    except Exception as e:
      app.logger.error(e)
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()


  #DELETE /movies/
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)

      db.session.delete(movie)
      db.session.commit()
        
      return jsonify({
        'success': True,
        'deleted': movie_id
      })

    except Exception as e:
      app.logger.error(e)
      db.session.rollback()
      abort(422)

    finally:
      db.session.close()

  #POST /actors 
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actors(payload):
    body = request.get_json()  #fills in the json user input
    
    new_name = body.get('name', None) 
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)
      
    if any(field is None or field == "" for field in [new_name, new_age, new_gender]):
      abort(422)
    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      db.session.add(actor)
      db.session.commit()

    
      return jsonify({
        'success': True,
        'created': actor.id
      })

    except Exception as e:
      app.logger.error(e)
      db.session.rollback()
      abort(422)  #error that the request was not able to be processed
      
    finally:
      db.session.close()

  #POST /movies 
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movies(payload):
    body = request.get_json()  #fills in the json user input

    new_title = body.get('title', None) 
    new_releasedate = body.get('releasedate', None)
      
    if any(field is None or field == "" for field in [new_title, new_releasedate]):
      abort(422)
    try:
      movie = Movie(title=new_title, releasedate=new_releasedate)
      db.session.add(movie)
      db.session.commit()
    
      return jsonify({
        'success': True,
        'created': movie.id
      })

    except Exception as e:
      app.logger.error(e)
      db.session.rollback()
      abort(422)  #error that the request was not able to be processed
      
    finally:
      db.session.close()

  #PATCH /actors/ 
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    body = request.get_json()  #fills in the json user input

    updated_name = body.get('name', None) 
    updated_age = body.get('age', None)
    updated_gender = body.get('gender', None)
      
    if any(field is None or field == "" for field in [updated_name, updated_age, updated_gender]):
      abort(422)

    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      actor.name = updated_name
      actor.age = updated_age
      actor.gender = updated_gender
      
      db.session.commit()
        
      return jsonify({
        'success': True,
        'updated': actor.id
      })

    except Exception as e:
      app.logger.error(e)
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()

  #PATCH /movies/ 
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    body = request.get_json()  #fills in the json user input

    updated_title = body.get('title', None) 
    updated_releasedate = body.get('releasedate', None)
      
    if any(field is None or field == "" for field in [updated_title, updated_releasedate]):
      abort(422)

    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)

      movie.title = updated_title
      movie.releasedate = updated_releasedate
      
      db.session.commit()
        
      return jsonify({
        'success': True,
        'updated': movie.id
      })

    except Exception as e:
      app.logger.error(e)
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()

  @app.route('/login')
  def login():
    print(loginURL)
    return redirect(loginURL)

  @app.route('/landing')
  @requires_auth('get:actors')
  def landing(payload):
    return jsonify({
        "success": True,
        "redirect": "you are logged in!"
    }), 200

  @app.errorhandler(404)
  def resourceNotFound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

  @app.errorhandler(405)
  def methodNotAllowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

  @app.errorhandler(500)
  def serverError(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500

  @app.errorhandler(AuthError)
  def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code

    
  return app


app = create_app()

if __name__ == '__main__':
  
  app.run(host='0.0.0.0', port=8080, debug=True)
