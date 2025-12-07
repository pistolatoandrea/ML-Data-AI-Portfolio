# 1. Base Image
# We use a lightweight Linux-based Python image (Slim version)
# This acts as the OS layer.

FROM python:3.10-slim

# 2. Set Working Directory
# This creates a folder named 'code' inside the container 
# and sets it as the default location for subsequent commands.

WORKDIR /code

# 3. Install Dependencies
# We copy requirements.txt first to leverage Docker's caching mechanism.
# If requirements.txt doesn't change, Docker skips re-installing libraries on rebuilds.

COPY ./requirements.txt /code/requirements.txt

# Install the Python packages without caching installation files to keep image small

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Copy Application Code
# We copy the local 'app' folder into the container's '/code/app' folder.
# NOTE: We exclude 'venv' thanks to .dockerignore

COPY ./app /code/app

# 5. Command to Run
# This is the command that executes when the container starts.
# --host 0.0.0.0 is CRITICAL: it allows external access to the container.
# --port 80 tells Uvicorn to listen on port 80 inside the container.

CMD ["uvicorn", "app.test_fastapi:app", "--host", "0.0.0.0", "--port", "80"]