# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Copy local code to the container image.
ENV APP_HOME /app
ENV PYTHONUNBUFFERED TRUE

WORKDIR $APP_HOME
COPY . .

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install functions-framework
RUN pip install -r requirements.txt

# Run the web service on container startup.
CMD exec functions-framework --target=main
