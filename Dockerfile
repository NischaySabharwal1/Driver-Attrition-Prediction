FROM python:3.10-slim-buster

#move into the app working directory
WORKDIR /app

#upgrade pip to install any issues with version mismatch
RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . ./

CMD python3 -m flask run --host=0.0.0.0



