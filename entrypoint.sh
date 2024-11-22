#!/bin/bash
set -e

# Run the tests first
pytest --maxfail=3 --disable-warnings tests/

# If tests pass, start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000
