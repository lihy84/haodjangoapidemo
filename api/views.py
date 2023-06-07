from django.http import JsonResponse, HttpResponseBadRequest
from sqlalchemy import create_engine, inspect
import sqlalchemy.exc
from .models import TableMetadata, ColumnMetadata

# Create your views here.

# API endpoint for getting table metadata
def table_metadata(request):
    # Get the database connection string and table name from the GET request
    db_string = request.GET.get("db_string")
    # Get the table name from the GET request
    table_name = request.GET.get("table_name")

    # If no database connection string was provided, return a 400 (Bad Request) response
    if not db_string:
        return HttpResponseBadRequest(content='{"error": "No database connection string provided."}', content_type='application/json')

    # If no table name was provided, return a 400 (Bad Request) response
    if not table_name:
        return HttpResponseBadRequest(content='{"error": "No table name provided."}', content_type='application/json')

    # Try to connect to the database and get the table metadata
    try:
        engine = create_engine(db_string)
        inspector = inspect(engine)
    except Exception as e:
        return HttpResponseBadRequest(content='{"error": "Could not connect to database. Error: ' + str(e) + '"}', content_type='application/json')

    # If the table does not exist in the database, return a 400 (Bad Request) response
    if table_name not in inspector.get_table_names():
        return HttpResponseBadRequest(content='{"error": "Table does not exist in the database."}', content_type='application/json')

    # Raw SQL for getting the number of rows in the table
    select_sql_raw = f"SELECT COUNT(*) FROM {table_name}"

    # If the database is PostgreSQL, use the public schema and double quote the table name incase it is capitalized
    if (engine.dialect.name == 'postgresql'):
        select_sql_raw = f"SELECT COUNT(*) FROM public.\"{table_name}\""

    # Get the table metadata
    try:
        columns = inspector.get_columns(table_name)
        num_rows = engine.execute(select_sql_raw).fetchone()[0]
    except Exception as e:
        return HttpResponseBadRequest(content='{"error": "Could not retrieve table metadata. Error: ' + str(e) + '"}', content_type='application/json')

    # Create the TableMetadata object
    col_metadata = [ColumnMetadata(col['name'], col['type']) for col in columns]
    # Create the TableMetadata object
    table_metadata = TableMetadata(col_metadata, num_rows, inspector.default_schema_name, db_string)

    # Return the table metadata as a JSON response
    return JsonResponse(table_metadata.to_dict(), safe=False)
