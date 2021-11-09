# castingagency
 
    Motivation for the project
"Casting Agency" is an API that tracks movies and actors and additional attributes. Movie attributes include title and release date. Actor attributes include name, age, and gender. Movies and actors can be newly added to the database, updated, deleted, or viewed. Role-based permissions are implemented such that certain resources are accessible only if a particular user has been assigned the appropriate role. See "Documentation of API behavior and RBAC controls" for details.

    URL location for the hosted API
The API is hosted via Heroku and can be found on: https://justincastingagency.herokuapp.com/ 
All endpoints require a bearer token. An example token is included in the setup.sh file and should be replaced (See Step 7 below).

    Project dependencies, local development and hosting instructions. Detailed instructions for scripts to set up authentication, install any project dependencies and run the development server.
1) The prequisites for running this project are python3 and pip3 already installed locally.
2) The following command should be run to install the applicable packages:
pip3 install requirements.txt

3) Run Postgres and use the following command to create the database:
createdb castingagency

4) Create your Auth0 domain and set up your Single Page Application, with the following roles and permissions:
a) Casting Assistant
    GET /actors
    GET /movies
b) Casting Director
    GET /actors
    GET /movies
    POST /actors
    DELETE /actors
    PATCH /actors
    PATCH /movies
c) Executive Producer
    GET /actors
    GET /movies
    POST /actors
    POST /movies
    DELETE /actors
    DELETE /movies
    PATCH /actors
    PATCH /movies
Assign users to the applicable roles to provide them permissions to the resources as needed. 

5) Edit the setup.sh file to include your own AUTH0_DOMAIN and loginURL, including secrets.

6) Use the following command to provide environment variables to the API:
source setup.sh

7) Run the following command to start the application:
python3 app.py

The application runs on http://localhost:8080/. After logging in as a user with the role assigned as applicable via Auth0, use http://localhost:8080/login to generate the bearer token, which you will need to access various endpoints. 

8) Testing
a) Populate the bearer token as the userToken in the setup.sh file. 

b) Use the following command to provide environment variables to the API:
source setup.sh

c) Use the following commands to set up a test database:
dropdb castingagency_test
createdb castingagency_test

d) Run the test file using:
python3 test_app.py
This populates the test database with three sample actors and three sample movies.

Documentation of API behavior and RBAC controls

    GET/login
This endpoint redirects to /landing to generate the bearer token, which you will need to access various endpoints.

    GET/landing
This endpoint generates the bearer token, which you will need to access various endpoints.

    GET/actors
Retrieves list of actors, including id, name, age, and gender.
Request arguments: userToken with correct permissions
Returns: JSON object containing {'success': True, 'actors': []}
This resource requires the role of Casting Assistant, Casting Director, or Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/actors -H "Authorization: Bearer ${userToken}"
Sample response: 
{
    "actors": [
        {
            "id": 1,
            "name": "Actor 1",
            "age": 31,
            "gender": "Male"
        }
    ],
    "success": true
}

    GET/movies
Retrieves list of movies, including id, movie title and release date.
Request arguments: userToken with correct permissions
Returns: JSON object containing {'success': True, 'movies': []}
This resource requires the role of Casting Assistant, Casting Director, or Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/movies -H "Authorization: Bearer ${userToken}"
Sample response: 
{
    "movies": [
        {
            "id": 1,
            "title": "Movie 1",
            "releasedate": "2022-01-31"
        }
    ],
    "success": true
}

    POST/actors
Adds a new actor. Requires name, age, and gender to be filled out.
Request arguments: userToken with correct permissions, JSON object with all values filled out for name, age, and gender.
Returns: JSON object containing {'success': True, 'created': actor.id}
This resource requires the role of Casting Director or Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/actors -X POST -H "Authorization: Bearer ${userToken}" 
-d '{
        "name": "Actor 1",
        "age": 31,
        "gender": "Male"
}'
Sample response: 
{
    "success": true,
    "created": 1
}

    POST/movies
Adds a new movie. Requires title and release date (YYYY-MM-DD) to be filled out.
Request arguments: userToken with correct permissions, JSON object with all values filled out for title and release date (YYYY-MM-DD).
Returns: JSON object containing {'success': True, 'created': movie.id}
This resource requires the role of Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/movies -X POST -H "Authorization: Bearer ${userToken}" 
-d '{
        "title": "Movie 1",
        "releasedate": "2022-01-31"
}'
Sample response: 
{
    "success": true,
    "created": 1
}

    DELETE/actors/<int:actor_id>
Deletes an existing actor by id. 
Request arguments: userToken with correct permissions.
Returns: JSON object containing {'success': True, 'deleted': actor_id}
This resource requires the role of Casting Director or Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/actors/1 -X DELETE -H "Authorization: Bearer ${userToken}"
Sample response: 
{
    "success": true,
    "deleted": 1
}

    DELETE/movies/<int:movie_id>
Deletes an existing movie by id. 
Request arguments: userToken with correct permissions.
Returns: JSON object containing {'success': True, 'deleted': movie_id}
This resource requires the role of Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/movies/1 -X DELETE -H "Authorization: Bearer ${userToken}"
Sample response: 
{
    "success": true,
    "deleted": 1
}

    PATCH/actors/<int:actor_id>
Edits an existing actor by id. Requires name, age, and gender to be filled out.
Request arguments: userToken with correct permissions, JSON object with all values filled out for name, age, and gender.
Returns: JSON object containing {'success': True, 'updated': actor.id}
This resource requires the role of Casting Director or Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/actors/1 -X PATCH -H "Authorization: Bearer ${userToken}" 
-d '{
        "name": "Actor 1",
        "age": 51,
        "gender": "Male"
}'
Sample response: 
{
    "success": true,
    "updated": 1
}

    PATCH/movies/<int:movie_id>
Edits an existing movie by id. Requires title and release date (YYYY-MM-DD) to be filled out.
Request arguments: userToken with correct permissions, JSON object with all values filled out for title and release date (YYYY-MM-DD).
Returns: JSON object containing {'success': True, 'updated': movie.id}
This resource requires the role of Casting Director or Executive Producer.
Sample curl request: curl http://0.0.0.0:8080/movies/1 -X PATCH -H "Authorization: Bearer ${userToken}" 
-d '{
        "title": "Movie 1",
        "releasedate": "2022-06-30"
}'
Sample response: 
{
    "success": true,
    "updated": 1
}