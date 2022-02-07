FROM python:3.8.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /proj1
WORKDIR /proj1
ADD requirements.txt /proj1/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /proj1/
RUN pip3 install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip3 install Django
RUN pip install django-cors-headers
RUN pip3 install djangorestframework
COPY pratilipi-project-django/backend /proj1

EXPOSE 3306
EXPOSE 3307
EXPOSE 3308
EXPOSE 9090
EXPOSE 9092
