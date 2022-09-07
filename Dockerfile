FROM python:3.9.13-buster

WORKDIR /appie

COPY . /appie/

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]