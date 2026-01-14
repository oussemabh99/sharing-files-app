FROM python:3.13.5-slim
LABEL maintainer="Oussema Ben Hdid"
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt 
entrypoint ["python", "src/app/run.py"]