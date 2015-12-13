
# new docker file; builds the image and installs python dependencies.
# sets the default command for the container to the application.

FROM ubuntu:14.04
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD #application needs to be set as the default command here. 
