FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$PYTHONPATH:/code/
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD ./ /code/
