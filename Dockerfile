FROM python:3.13-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Tell poetry not to make its own venvs
    POETRY_VIRTUALENVS_CREATE=false


RUN apt update
RUN apt install gettext -y


WORKDIR /code

# Install poetry
RUN pip install poetry

# Copy dependency files (even if they only contain Python version info for now)
# Notice I added an asterisk: poetry.lock*. If you haven't run a poetry command yet, you might not have a poetry.lock file. Without that asterisk, Docker will crash saying "File not found." The asterisk tells Docker: "Copy it if it exists, but don't panic if it doesn't."
COPY pyproject.toml poetry.lock* ./

# Install dependencies (will skip if list is empty)
RUN poetry install --no-root --no-interaction

# Copy your App code
COPY . .

EXPOSE 8000

ENTRYPOINT [ "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000" ]