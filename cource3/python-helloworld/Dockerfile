FROM python:3.11
LABEL maintainer="Leon Guenther"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "app.py" ]