FROM python:3.10-alpine

ARG WORKDIR=/wd

RUN #apt update && apt upgrade -y

WORKDIR ${WORKDIR}

COPY requirements.txt ${WORKDIR}/requirements.txt

RUN pip install --requirement requirements.txt

COPY previous_hw/app.py app.py

ENTRYPOINT ["python", "app.py"]