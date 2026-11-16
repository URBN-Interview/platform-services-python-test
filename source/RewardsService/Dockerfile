# Image for the RewardsService API (also reused by the init_data seed container):
# Python 3.10 with the Tornado/Mongo dependencies installed; code lives in /code.

FROM python:3.10.18
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$PYTHONPATH:/code/
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./ /code/
EXPOSE 7050
