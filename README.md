# Full Stack Capstone movies API Backend
# Capstone API

## Capstone Project for Udacity's Full Stack Developer Nanodegree

## About

Welcome to the Movies Management System! This project aims to provide a simple and efficient solution for managing actors and movies in a web application. It allows users to easily store, retrieve, update, and delete information about actors and movies through a user-friendly interface.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

Heroku Link: https://serene-retreat-91427-44e50b468425.herokuapp.com/

While running locally: http://localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Project dependencies
The project depends on the latest version of Python 3.x which we recommend to download and install from their official website and use a virtual environment to install all dependencies.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

## Running the local development server

All necessary credential to run the project are provided in the setup.sh file. The credentials can be enabled by running the following command:

- source setup.sh

Before running the application locally, make the following changes in the `app.py` file in root directory:

- uncomment the line `db_drop_and_create_all()` on the initial run to setup the required tables in the database.

To run the server, execute in linux:

```bash
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload
```

To run the server, execute in window:

```bash
set DATABASE_URL=<database-connection-url>
set FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

Using the `--reload` flag will detect file changes and restart the server automatically.


## API Reference

## Getting Started
Base URL: This application can be run locally. The hosted version is at `https://serene-retreat-91427-44e50b468425.herokuapp.com`.

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, except the root (or health) endpoint, that are passed via the `Bearer` token.

The application has three different types of roles:

- staff
  - can only get and get detail of actor and movie, cannot delete or create, update
- Manager
  - can perform all the actions that `STAFF` can
  - get full access and execute to CRUD

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request
 - 401: Unauthorized
 - 403: Forbidden
 - 404: Not Found
 - 405: Method Not Allowed
 - 422: Unprocessable Entity
 - 500: Internal Server Error

# API Documentation

## Endpoints

### GET /actors

Returns a list of all actors.

#### Permissions

- Requires authentication with the `get:actors` permission.

#### Request

- Method: GET
- URL: `/actors`

#### Response

- Status code: 200 (OK)
- Body:

```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "John Doe",
      "movies": ["Movie 1", "Movie 2"]
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "movies": ["Movie 3", "Movie 4"]
    }
  ]
}
```

## Endpoints

### GET /actors/{actor_id}

Returns information about a specific actor.

#### Permissions

- Requires authentication with the `get:actors-info` permission.

#### Request

- Method: GET
- URL: `/actors/{actor_id}`

- Path Parameters:
  - `actor_id` (integer, required): The ID of the actor.

#### Response

- Status code: 200 (OK)
- Body:

```json
{
    "actor": {
        "age": 56,
        "bio": "Robert John Downey Jr. is an American actor. He is best known for his role as Tony Stark / Iron Man in the Marvel Cinematic Universe.",
        "gender": "Male",
        "movies": [],
        "name": "Robert Downey Jr.",
        "nationality": "American",
        "profile_image": "https://example.com/robert_downey_jr.jpg"
    },
    "success": true
}
```

### POST /actors

Creates a new actor.

#### Permissions

- Requires authentication with the `create:actors` permission with manager token.

#### Request

- Method: POST
- URL: `/actors`

- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {YOUR_ACCESS_TOKEN}`

- Body:

```json
{
    "created": 3,
    "success": true
}
```

### PATCH /actors/{actor_id}

Updates an existing actor.

#### Permissions

- Requires authentication with the `patch:actor` permission.

#### Request

- Method: PATCH
- URL: `/actors/{actor_id}`

- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {YOUR_ACCESS_TOKEN}`

- Path Parameters:
  - `actor_id` (integer, required): The ID of the actor to be updated.

- Body: 

```json
{
    "actor_info": {
        "age": 37,
        "bio": "Scarlett Johansson is an American actress. She is best known for her role as Natasha Romanoff / Black Widow in the Marvel Cinematic Universe.",
        "gender": "Female",
        "name": "Scarlett Johansson",
        "nationality": "American",
        "profile_image": "https://example.com/scarlett_johansson_updated.jpg"
    },
    "success": true
}

```

### DELETE /actors/{actor_id}

Deletes an existing actor.

#### Permissions

- Requires authentication with the `delete:actor` permission.

#### Request

- Method: DELETE
- URL: `/actors/{actor_id}`

- Headers:
  - `Authorization: Bearer {YOUR_ACCESS_TOKEN}`

- Path Parameters:
  - `actor_id` (integer, required): The ID of the actor to be deleted.

#### Response

- Status code: 200 (OK)
- Body:

```json
{
    "deleted_actor_id": 5,
    "success": true
}
```
### GET /movies

Returns a list of all movies.

#### Permissions

- Requires authentication with the `get:movies` permission.

#### Request

- Method: GET
- URL: `/movies`

#### Response

- Status code: 200 (OK)
- Body:

```json
{
    "movies": [
        {
            "actors": [
                "Robert Downey Jr.",
                "Robert Downey Jr.",
                "Scarlett Johansson"
            ],
            "average_rating": 9.3,
            "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "director": "Frank Darabont",
            "genre": "Drama",
            "poster_image": "https://example.com/poster.jpg",
            "release_date": "October 14, 1994",
            "title": "The Shawshank Redemption"
        }
    ],
    "success": true
}
```
### GET /movies/{movie_id}

Returns information about a specific movie.

#### Permissions

- Requires authentication with the `get:movies-info` permission.

#### Request

- Method: GET
- URL: `/movies/{movie_id}`

- Path Parameters:
  - `movie_id` (integer, required): The ID of the movie.

#### Response

- Status code: 200 (OK)
- Body:

```json
{
    "movie": {
        "actors": [
            "Robert Downey Jr.",
            "Robert Downey Jr.",
            "Scarlett Johansson"
        ],
        "average_rating": 9.3,
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "director": "Frank Darabont",
        "genre": "Drama",
        "poster_image": "https://example.com/poster.jpg",
        "release_date": "October 14, 1994",
        "title": "The Shawshank Redemption"
    },
    "success": true
}
```
### POST /movies

Creates a new movie.

#### Permissions

- Requires authentication with the `post:movie` permission.

#### Request

- Method: POST
- URL: `/movies`

- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {YOUR_ACCESS_TOKEN}`

- Body:

```json
{
    "created": 2,
    "success": true
}
```
### PATCH /movies/{movie_id}

Updates an existing movie.

#### Permissions

- Requires authentication with the `patch:movie` permission.

#### Request

- Method: PATCH
- URL: `/movies/{movie_id}`

- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {YOUR_ACCESS_TOKEN}`

- Body (example):

```json
{
    "movie_info": {
        "average_rating": 8.8,
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "director": "Christopher Nolan",
        "genre": "Action",
        "poster_image": "https://example.com/inception_poster.jpg",
        "release_date": "July 16, 2010",
        "title": "Inception"
    },
    "success": true
}
```
### DELETE /movies/{movie_id}

Deletes a movie.

#### Permissions

- Requires authentication with the `delete:movie` permission.

#### Request

- Method: DELETE
- URL: `/movies/{movie_id}`

- Headers:
  - `Authorization: Bearer {YOUR_ACCESS_TOKEN}`

- Path Parameters:
  - `movie_id` (integer, required): The ID of the movie to be deleted.

#### Response

- Status code: 200 (OK)
- Body:

```json
{
    "deleted_actor_id": 3,
    "success": true
}
```
## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'staff' and 'manager' roles.

## Testing
For testing the backend, run the following commands
```
python -m unittest test_app.py
```

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://serene-retreat-91427-44e50b468425.herokuapp.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.