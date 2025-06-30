FROM python:3.10-slim-bullseye
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc build-essential \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app.py /app
RUN pip install --upgrade pip uv streamlit requests 
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]