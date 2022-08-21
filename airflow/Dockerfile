FROM apache/airflow:2.3.3

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update && apt-get install vim -qqq

USER $AIRFLOW_UID
WORKDIR $AIRFLOW_HOME

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID