from django.db import models

# Create your models here.

class ColumnMetadata:
    def __init__(self, col_name: str, col_type: str):
        self.col_name = col_name
        self.col_type = col_type

    def to_dict(self):
        return {"col_name": self.col_name, "col_type": str(self.col_type)}

class TableMetadata:
    def __init__(self, columns: list, num_rows: int, schema: str, database: str):
        self.columns = columns
        self.num_rows = num_rows
        self.schema = schema
        self.database = database

    def to_dict(self):
        return {
            "columns": [col.to_dict() for col in self.columns],
            "num_rows": self.num_rows,
            "schema": self.schema,
            "database": self.database,
        }
