# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-buster

RUN pip install uwsgi

RUN pip install torch

RUN mkdir aditya/

WORKDIR /aditya

COPY . .

RUN python -m pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]

# EXPOSE 8000

# EXPOSE 6379

# CMD ["python","app.py"]




