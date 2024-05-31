FROM python:3.8

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .

EXPOSE 5000

ENTRYPOINT flask --app main run -h 0.0.0.0