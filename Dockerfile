FROM python:3.6.5
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD ./services/extractor/ /code/
 ADD ./services/transformer/ /code/
 ADD ./services/loader/ /code/
 ADD ./data/ /data/
 VOLUME /data