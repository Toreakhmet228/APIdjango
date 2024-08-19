FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry lock --no-update
RUN poetry install


CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
