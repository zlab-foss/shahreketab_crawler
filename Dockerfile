FROM python:3.8-slim-buster

LABEL maintainer="Sina Zamani <sinazamani920@gmail.com>"

RUN apt-get update && \
    pip install --upgrade pip

RUN mkdir /usr/app

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r /usr/app/requirements.txt

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0" ," src.crawler.entrypoints.main:py"]
