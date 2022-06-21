FROM python:3.10

WORKDIR /app

RUN apt update && apt upgrade -y

COPY requirements.txt requirements.txt

RUN pip install --requirement requirements.txt

COPY ./previous_hw/app.py app.py
COPY ./previous_hw previous_hw

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]