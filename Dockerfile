FROM python:3.10

ARG WORKDIR=/wd

WORKDIR ${WORKDIR}

RUN apt update && apt upgrade -y

COPY requirements.txt requirements.txt

RUN pip install --requirement requirements.txt

COPY app.py app.py
COPY app_settings app_settings

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]