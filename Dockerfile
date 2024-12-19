FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

COPY ./static /static/

COPY ./static/pics /static/pics/


EXPOSE 5555

CMD ["python", "app.py"]

