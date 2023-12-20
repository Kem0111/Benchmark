FROM python:3.11


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"


WORKDIR /code


RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
RUN apt-get update \
    && apt-get install -y gettext

COPY pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction

COPY . /code/

RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]

CMD ["poetry", "run", "python3", "main.py"]