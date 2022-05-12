FROM python:3.10.4-slim-buster

COPY . /app

WORKDIR /app

RUN chmod +x upgrader-cli
RUN pip3 install -r requirements.txt

CMD ["bash"]