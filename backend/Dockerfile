FROM python:3.11-buster

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "main.py"]

EXPOSE 8000
