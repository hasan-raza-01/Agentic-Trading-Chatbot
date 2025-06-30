FROM python:3.10-slim-bullseye
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc build-essential curl \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --upgrade pip uv \
 && uv pip install --system -e .
EXPOSE 8000 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]