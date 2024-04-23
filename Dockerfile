FROM python:3.9

WORKDIR /backup/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl jq && \
    rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

# RUN pip install PyGithub
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY app /backup/app
COPY config /backup/config

CMD ["python", "backup_teams.py"]
