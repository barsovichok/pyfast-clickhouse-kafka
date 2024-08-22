Sure! Below is a revised version of the README file based on your requirements:

---

# PyFast

PyFast is a web API project built with Python and FastAPI. It is designed to provide a robust and scalable RESTful API service. This project uses SQLModel for ORM, PostgreSQL as the database, and other modern Python libraries to deliver high performance and reliability.

## Table of Contents

- [Technologies](#technologies)
- [Libraries and Requirements](#libraries-and-requirements)
- [API Routes](#api-routes)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Examples of HTTP Requests](#examples-of-http-requests)

## Technologies

- **Python 3.x**
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLModel**: A library for interacting with SQL databases, built on top of SQLAlchemy and Pydantic, designed to work seamlessly with FastAPI.
- **PostgreSQL**: An advanced, enterprise-class open-source relational database.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: ASGI server implementation, using `uvloop` and `httptools`.

## Libraries and Requirements

To install the required libraries, use the following command:

```bash
pip install -r requirements.txt
```

### Key Dependencies

- `fastapi`
- `uvicorn`
- `sqlmodel`
- `pydantic`
- `psycopg2-binary` (for PostgreSQL database connectivity)

## API Routes

Here are the main API routes provided by the PyFast application:

- `GET /users/`: Retrieve a list of users.
- `GET /users/{id}`: Retrieve details of a specific user by ID.
- `POST /users/`: Create a new user.
- `PUT /users/{id}`: Update an existing user by ID.
- `DELETE /users/{id}`: Delete a user by ID.

_Note: You can explore the full API documentation using the built-in Swagger UI at `/docs` after running the server._

## Setup

To set up and run this project locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/barsovichok/pyfast.git
    cd pyfast
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root directory and configure the necessary environment variables (you can also find the example in the .env.sample file):

    ```plaintext
    APP_URL = "localhost:8000"
    DATABASE_ENGINE=postgresql+psycopg2://user:password@localhost/dbname
    DATABASE_POOL_SIZE=10
    ```

5. **Start the application**:

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the application**:

    Open your browser and go to `http://127.0.0.1:8000` to see the API in action.

## Running Tests

To run tests, make sure you have `pytest` installed:

```bash
pip install pytest
```

Then, execute the tests using:

```bash
pytest
```

This will run all the tests in the repository and provide you with a report on the outcomes.

## Examples of HTTP Requests

Here are some examples of HTTP requests you can make to the API using models from the project:

### Get All Users

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json'
```

### Get User by ID

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/1' \
  -H 'accept: application/json'
```

### Create a New User

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "newuser",
  "email": "newuser@example.com",
  "first_name": "New",
  "last_name": "User",
  "avatar": "https://example.com/avatar.jpg"
}'
```

### Update a User

```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/users/1' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "updateduser",
  "email": "updateduser@example.com",
  "first_name": "Updated",
  "last_name": "User",
  "avatar": "https://example.com/updated-avatar.jpg"
}'
```

### Delete a User

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/users/1' \
  -H 'accept: application/json'
```

## Work with Docker
We buil docker image by this command: docker build . -t pyfast 
We run project in Docker by this command -  docker run -e DATABASE_ENGINE=postgresql+psycopg2://postgres:example@host.docker.internal:5432/postgres -e DATABASE_POOL_SIZE=100 -p 8002:80 pyfast
or by docker compose up.
Also helping program - docker compose down


## Contributing

Feel free to fork this repository, make changes, and submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README now includes information about `SQLModel` instead of Alembic, uses the correct models in the HTTP request examples, and omits any mention of database migrations, aligning it with your project's requirements.