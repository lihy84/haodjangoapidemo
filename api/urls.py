from django.urls import path

from .views import table_metadata

# Define the URL paths for the API
urlpatterns = [
    path('table_metadata', table_metadata),
]
