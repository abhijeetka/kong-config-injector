FROM python:3.12-slim

ENV KONG_ADMIN_PORT=8001
ENV KONG_ADMIN_URL=kong-cp-kong-admin
ENV KONG_NAMESPACE=kong

ENV PYTHONUNBUFFERED=0

WORKDIR /app
COPY requirements.txt ./
COPY kong-injector.py ./
COPY kong-service.json /

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "kong-injector.py"]
