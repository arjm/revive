FROM docker.io/bitnami/spark:3.3

WORKDIR /opt/bitnami/spark/

COPY compute_segments.py compute_segments.py
COPY data.parquet.gzip data.parquet.gzip
COPY mysql-connector-j-8.0.31.jar /opt/bitnami/spark/jars/mysql-connector-j-8.0.31.jar

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
