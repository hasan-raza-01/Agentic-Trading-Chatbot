FROM python:3.10-slim-bullseye
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc build-essential \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --upgrade pip uv \
 && uv pip install --system -e .
EXPOSE 8000 8501
CMD ["bash","-lc","uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.address 0.0.0.0 --server.port 8501"]
