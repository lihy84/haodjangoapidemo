from django.shortcuts import render
from django.http import JsonResponse
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
import json

# Create your views here.

# API endpoint for getting table metadata


def table_metadata(request):

    # Get the database connection string from the request
    db_string = request.GET.get("db_string")

    # If no connection string is provided, return an error
    if not db_string:
        return JsonResponse({"error": "No database connection string provided."}, status=400)

    # If the connection string is not a string, return an error
    try:
        # Try to parse the connection string as JSON
        engine = create_engine(db_string)
        # Get the table metadata
        insp = inspect(engine)

        # Get the table names
        result = []

        # Loop through the tables and get the metadata
        for table_name in insp.get_table_names():
            # Raw SQL for getting the number of rows in the table
            select_sql_raw = f"SELECT COUNT(*) FROM {table_name}"

            # If the database is PostgreSQL, use the public schema and double quote the table name incase it is capitalized
            if (engine.dialect.name == 'postgresql'):
                select_sql_raw = f"SELECT COUNT(*) FROM public.\"{table_name}\""

            # Get the columns and their types
            columns = [{"col_name": c["name"], "col_type": str(
                c["type"])} for c in insp.get_columns(table_name)]

            # Get the number of rows in the table
            num_rows = engine.execute(select_sql_raw).scalar()

            # Add the table metadata to the result
            result.append({"columns": columns, "num_rows": num_rows,
                          "schema": insp.get_schema_names()[0], "database": db_string})

        # Return the result as JSON
        return JsonResponse(result, safe=False)

    # If the connection string is not a string, return an error
    except OperationalError as e:
        # Return the error as JSON, TODO: return the error code
        return JsonResponse({"error": str(e.code)}, status=400)
