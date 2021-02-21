FROM python:3.9.1

WORKDIR /samwell

ENV PATH=/home/appuser/.local/bin:$PATH

COPY requirements.txt requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/sh", "bin/run"]
