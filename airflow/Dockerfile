#first time build airflow docker gcp
FROM apache/airflow:3


#SETUP AIRFLOW TO HOME DIRECTORY
ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get update -qq && apt-get upgrade -qqq
#Git bash gcc  + g++ =qqq

RUN pip install --no-cache-dir -r requirement.txt 

#airflow-docker-stack
SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

ARG CLOUD_SDK_VERSION=413.0.0
ENV GCLOUD_HOME=home/google-cloud-sdk

ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"


RUN DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/google-cloud-sdk.tar.gz" \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "${TMP_DIR}/google-cloud-sdk.tar.gz" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
       --bash-completion=false \
       --path-update=false \
       --usage-reporting=false \
       --quiet \
    && rm -rf "${TMP_DIR}" \
    && gcloud --version
#google cloud files and variables

RUN apt-get update -qq && apt-get install unzip -qqq

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID