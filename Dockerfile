FROM python

ENV TERRAFORM_VERSION=0.12.19
ENV TERRAFORM_PLUGIN_DIR=/root/.terraform.d/plugins/

RUN mkdir -p "${TERRAFORM_PLUGIN_DIR}" && cd /tmp && \
    curl -sSLO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
        unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -d /usr/bin/ && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*

COPY requirements.txt /app/requirements.txt
COPY __main__.py /app/__main__.py
RUN pip install -r /app/requirements.txt
CMD python /app/__main__.py

