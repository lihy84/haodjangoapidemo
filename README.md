# Django PostgreSQL Metadata API

This Django application provides an API to retrieve metadata from a PostgreSQL database.

## Installation

Before you start, make sure you have Python 3.8 and pip installed.

### Step 1: Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/lihy84/haodjangoapidemo.git
cd haodjangoapidemo
```

### Step 2: Set up a virtual environment

It's a good practice to create a virtual environment for your Python projects. This keeps your projects' dependencies separate from each other.

Create a virtual environment by running:

```bash
python3 -m venv env
```

Then, activate the virtual environment. On Windows, run:

```bash
env\Scripts\activate.bat
```

On Unix or MacOS, run:

```bash
source env/bin/activate
```

### Step 3: Install the dependencies

Install the dependencies by running:

```bash
pip install -r requirements.txt
```

### Step 4: Run migrations

Run the Django migrations to set up your database schema:

```bash
python manage.py migrate
```

### Step 5: Run the server

Run the development server to make sure everything works:

```bash
python manage.py runserver
```

The server will start, and you can access the API at `http://localhost:8000/api/table_metadata`.

## Usage

To use the API, make a GET request to the /api/table_metadata endpoint with your PostgreSQL connection string as the db_string query parameter. The API will return a JSON array of the metadata for all tables in the database.

## Example

```bash
curl -X GET "http://localhost:8000/api/table_metadata?db_string=postgresql://postgres:postgres@localhost:5432/postgres"
```

## Future Improvements

Here are some ideas for future improvements:

- Secure DB Connection Strings: Right now, the API accepts the DB connection string as a GET parameter, which is not safe for production. We should instead use a secure method to accept this sensitive information.
- Error Handling: Improve error handling, possibly including more specific messages for different types of errors and unexpected inputs.
- Logging: Implement a logging system to help with debugging and maintaining the application.
- Tests: Add a suite of tests to ensure the application works as expected and prevent regressions.
- Caching: Implement a caching mechanism for the metadata to improve performance when dealing with large databases.
- CI/CD: Implement a CI/CD pipeline for automated testing and deployment.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
