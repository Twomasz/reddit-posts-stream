# docker/spark_consumer/Dockerfile
FROM bitnami/spark:3.5.4

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY spark_consumer.py .

#CMD ["spark-submit", "--master", "local[*]", "spark_consumer.py"]