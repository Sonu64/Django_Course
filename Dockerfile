FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Tell poetry not to make its own venvs
    POETRY_VIRTUALENVS_CREATE=false

# Optional, but Best-Practice :)
RUN apt update 
# If you create the .mo files locally and they are sitting in your project folder, they will be copied into the container during the COPY . . step. In that specific scenario, Django would technically work without gettext installed in the container.
# However, relying on this is generally considered risky "DevOps" practice - because of version-mismatch etc. gettext is a Utility, not a pkg. 
RUN apt install gettext -y


RUN mkdir /code
WORKDIR /code

# Install poetry
RUN pip install poetry

RUN pip install "psycopg[binary]"

# Copy dependency files (even if they only contain Python version info for now)
# Notice I added an asterisk: poetry.lock*. If you haven't run a poetry command yet, you might not have a poetry.lock file. Without that asterisk, Docker will crash saying "File not found." The asterisk tells Docker: "Copy it if it exists, but don't panic if it doesn't." If you are inside the container (e.g., using a DevContainer or just running via Compose) and you realize you forgot to translate a new field:
# Without gettext in Docker: You have to stop, go to your host machine, run the command, and restart/rebuild. Yes, compiling the messages absolutely requires the gettext utility. If you try to run python manage.py compilemessages on your Windows machine right now without that utility installed, Django will give you an error like:
# Can't find msgfmt. Make sure you have GNU gettext tools installed.
# The "Ghost" in the Machine
# The reason it "felt" like a Python package is because Django’s Python code acts as the middleman.
# With gettext in Docker: You just run docker-compose exec web python manage.py compilemessages (after making some changes in the PO files.) and the change is live instantly

COPY pyproject.toml poetry.lock* ./

# Install dependencies (will skip if list is empty)
RUN poetry install --no-root --no-interaction

# Copy your App code
COPY . .

EXPOSE 8000

ENTRYPOINT [ "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000" ]