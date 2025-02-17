#!/bin/sh

# Print the uv version
uv --version

# Run the Django application
uv run manage.py runserver 0.0.0.0:8000