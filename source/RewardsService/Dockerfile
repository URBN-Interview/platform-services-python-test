FROM python:3.10.18
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$PYTHONPATH:/code/
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./ /code/
EXPOSE 7050
