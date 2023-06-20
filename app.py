from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Actor, Movie, movies_actors
from auth.auth import AuthError, requires_auth
from dotenv import load_dotenv

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    load_dotenv(".env")

    # Uncomment the following line on the initial run to setup
    # the required tables in the database
    # db_drop_and_create_all(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def health():
        return jsonify({'health': 'Running!!'}), 200

    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        actors_data = []

        for actor in actors:
            movies = Movie.query.join(movies_actors).filter(movies_actors.c.actor_id == actor.id).all()
            movie_titles = [movie.title for movie in movies]

            actor_data = actor.short()
            actor_data['movies'] = movie_titles
            actors_data.append(actor_data)

        return jsonify({
            "success": True,
            "actors": actors_data
        }), 200

    @app.route('/actors/<int:actor_id>')
    @requires_auth("get:actors-info")
    def get_actor_by_id(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first_or_404()
        
        movies = Movie.query.join(movies_actors).filter(movies_actors.c.actor_id == actor.id).all()
        movie_titles = [movie.title for movie in movies]

        actor_data = actor.long()
        actor_data['movies'] = movie_titles

        return jsonify({
            "success": True,
            "actor": actor_data
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actor")
    def create_actor(payload):
        try:
            data = request.get_json()
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            bio = data.get('bio')
            nationality = data.get('nationality')
            profile_image = data.get('profile_image')
            movie_ids = data.get('movie_ids')  # List of movie IDs

            actor = Actor(name=name, age=age, gender=gender, bio=bio, nationality=nationality, profile_image=profile_image)

            actor.insert()

            # Associate movies with the actor
            if movie_ids:
                movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
                actor.movies.extend(movies)
                actor.update()

            return jsonify({
                'success': True,
                'created': actor.id
            })
        except Exception:
            abort(500)



    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def update_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first_or_404()

        try:
            request_body = request.get_json()
            if not request_body:
                abort(400, 'No data provided')

            actor.name = request_body.get('name', actor.name)
            actor.age = request_body.get('age', actor.age)
            actor.gender = request_body.get('gender', actor.gender)
            actor.bio = request_body.get('bio', actor.bio)
            actor.nationality = request_body.get('nationality', actor.nationality)
            actor.profile_image = request_body.get('profile_image', actor.profile_image)

            movie_ids = request_body.get('movie_ids')
            if movie_ids:
                movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
                actor.movies = movies

            actor.update()

            return jsonify({
                "success": True,
                "actor_info": actor.long()
            }), 200

        except Exception:
            abort(500)

    

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first_or_404()

        try:
            for movie in actor.movies:
                movie.actors.remove(actor)

            actor.delete()

            return jsonify({
                "success": True,
                "deleted_actor_id": actor.id
            }), 200

        except Exception:
            abort(500)



    #movie api


    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        movies_data = [movie.full_info() for movie in movies]

        return jsonify({
            "success": True,
            "movies": movies_data
        }), 200

    @app.route('/movies/<int:movie_id>')
    @requires_auth("get:movies-info")
    def get_movie_by_id(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first_or_404()

        return jsonify({
            "success": True,
            "movie": movie.full_info()
        }), 200


    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movie")
    def create_movie(payload):
        try:
            data = request.get_json()
            title = data.get('title')
            release_date = data.get('release_date')
            description = data.get('description')
            genre = data.get('genre')
            director = data.get('director')
            poster_image = data.get('poster_image')
            average_rating = data.get('average_rating')
            actor_ids = data.get('actor_ids')  # List of actor IDs

            movie = Movie(title=title, release_date=release_date, description=description,
                        genre=genre, director=director, poster_image=poster_image, average_rating=average_rating)

            movie.insert()

            # Associate actors with the movie
            if actor_ids:
                actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
                movie.actors.extend(actors)
                movie.update()

            return jsonify({
                'success': True,
                'created': movie.id
            })
        except Exception:
            abort(500)


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def update_movie(payload, movie_id):

        movie = Movie.query.filter_by(id=movie_id).first_or_404()    

        errorCode = 500
        try:
            request_body = request.get_json()
            if not request_body:
                abort(400, 'No data provided')

            if 'title' in request_body:
                movie.title = request_body['title']
            if 'release_date' in request_body:
                movie.release_date = request_body['release_date']
            if 'description' in request_body:
                movie.description = request_body['description']
            if 'genre' in request_body:
                movie.genre = request_body['genre']
            if 'director' in request_body:
                movie.director = request_body['director']
            if 'poster_image' in request_body:
                movie.poster_image = request_body['poster_image']
            if 'average_rating' in request_body:
                movie.average_rating = request_body['average_rating']
            if 'actor_ids' in request_body:
                actor_ids = request_body['actor_ids']
                actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()

                if len(actor_ids) == len(actors):
                    movie.actors = actors
                else:
                     errorCode = 422
                     abort(errorCode)

            movie.update()

            return jsonify({
                "success": True,
                "movie_info": movie.long()
            }), 200

        except Exception as e:
            abort(errorCode)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first_or_404()

        try:
            for actor in movie.actors:
                actor.movies.remove(movie)

            movie.delete()

            return jsonify({
                "success": True,
                "deleted_movie_id": movie.id
            }), 200

        except Exception:
            abort(500)

    # Error Handling
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401
    
    @app.errorhandler(500)
    def unauthorized(error):
        return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
        }), 500

    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        print("res")
        return response

    return app


app = create_app()
