FROM bitnami/spark:3.5.4

WORKDIR /app

ADD https://jdbc.postgresql.org/download/postgresql-42.6.0.jar /opt/spark/jars/postgresql.jar
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.4/spark-sql-kafka-0-10_2.12-3.5.4.jar /opt/spark/jars/kafka.jar

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY spark_consumer.py .

CMD ["spark-submit", "--master", "local[*]", "spark_consumer.py"]