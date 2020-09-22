# FROM creates a layer from specified  Docker image.
FROM python:3.6-slim
WORKDIR /app


# COPY adds files from your Docker client’s current directory.
COPY ./requirements.txt /app

# install tweepy (package name is in requirements) on the virtual machine 
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD . /app

# CMD specifies what command to run within the container.
CMD ["python", "-u", "get_tweets.py"]
