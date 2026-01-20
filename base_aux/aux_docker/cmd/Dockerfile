# select base image
FROM python:3.9-slim

# 1------ COMMON OS PREPARE --------------
RUN \
    pip install --no-cache-dir --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 2------ SPECIAL ----------------------------------
# ENV SETTINGS ------------
ENV FLASK_APP=src.app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# set workdir --------------------
WORKDIR /app
RUN mkdir /var/run/sshd

# copy special files ------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# copy full prj ------------------
COPY .. .

# ---------------------------------
HEALTHCHECK \
    --interval=5m \
    --timeout=3s \
    CMD curl -f http://localhost/ || exit 1


EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
