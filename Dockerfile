FROM python:3.12.3
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry==1.4.2
RUN poetry config virtualenvs.create false --local

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

COPY mysite .
RUN poetry install

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]