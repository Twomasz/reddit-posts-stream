FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY reddit_producer.py .

#CMD ["python", "-c", "print('Hello Container!'); import time; time.sleep(1000)"]
CMD ["python", "reddit_producer.py"]