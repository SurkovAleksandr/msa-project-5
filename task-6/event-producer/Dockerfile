FROM python:3.12-alpine
WORKDIR /app
COPY app.py app.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]

