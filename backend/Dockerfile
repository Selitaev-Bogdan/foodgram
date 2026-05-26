FROM python:3.9
WORKDIR /app/backend
COPY requirements.txt . 
RUN pip install -r requirements.txt --no-cache-dir
COPY backend/ .
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000"]
