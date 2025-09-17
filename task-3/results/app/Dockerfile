FROM python:3.12-alpine
RUN pip install psycopg2-binary
RUN mkdir -p /export-data
WORKDIR /app
COPY export_to_csv.py export_to_csv.py
CMD ["python", "export_to_csv.py" ]
# Если надо после выполнения программы зайти в контейнер, то надо использовать эту команду
#CMD ["sh", "-c", "python export_to_csv.py && tail -f /dev/null" ]