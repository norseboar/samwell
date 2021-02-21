FROM python:3.9.1

WORKDIR /usr/src/app
RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install

COPY . .

CMD [ "python"]