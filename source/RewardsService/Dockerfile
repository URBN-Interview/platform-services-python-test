FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$PYTHONPATH:/code/
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD ./ /code/
