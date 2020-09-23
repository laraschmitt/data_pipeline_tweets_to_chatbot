# install Linux Debian and then install Python 3.6 on top of it (image found on Dockerub)
FROM python:3.6-slim

# rougly the equivalent of mkdir app upon creation of the container:
WORKDIR /app
# COPY adds files from your Docker client’s current directory. (Or if everything in the dir: ADD . /app)

COPY ./requirements.txt /app
COPY ./Dockerfile /app
COPY ./app.py /app


# install tweepy (package name is in requirements) on the virtual machine 
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# CMD specifies what command to run within the container.
CMD ["python", "-u", "app.py"]
