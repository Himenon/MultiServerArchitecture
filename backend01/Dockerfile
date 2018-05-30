FROM python:3.6

RUN mkdir -p /code
WORKDIR /code
COPY ./ /code
RUN pip3 install -r /code/requirements.txt

CMD ["python3", "server.py"]
