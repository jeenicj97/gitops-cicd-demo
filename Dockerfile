FROM python:3.12-apline
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
RUN ["python", "app.py"]
