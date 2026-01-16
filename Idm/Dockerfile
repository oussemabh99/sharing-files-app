FROM python:3.13.5
LABEL maintainer="Oussema Ben Hdid"
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["uwsgi","--chdir","/app/src","--http","0.0.0.0:5000","--master","-p","4","-w","run:app"]