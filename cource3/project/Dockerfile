FROM python:3.8
LABEL maintainer="Leon Guenther"

COPY ./techtrends /app
WORKDIR /app
RUN pip install -r requirements.txt

# command to run on container start
CMD python init_db.py ; python app.py
EXPOSE 3111