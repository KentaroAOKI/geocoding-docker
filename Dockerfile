FROM python:3.7-slim
RUN apt-get update \
    && apt-get install -y ca-certificates
COPY src src
RUN pip install --no-cache-dir -r src/requirements.txt
CMD python src/main.py